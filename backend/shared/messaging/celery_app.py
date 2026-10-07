"""
One Celery app factory reused by every worker.

Broker = RabbitMQ (so `task.delay(...)` publishes onto a real AMQP queue,
giving us the exchange/routing-key/queue mechanics the architecture calls
for). Result backend = Redis (fast, ephemeral -- exactly what result
backends are for, never the system of record; the system of record for
execution state is Postgres, updated via the callback the task makes to
Workflow Service).

Retry policy: each task calls `self.retry(countdown=...)` explicitly using
`shared.messaging.retry_policy` (5s/15s/30s, only for retryable errors)
rather than Celery's default exponential `retry_backoff` -- see that module
for why. Retry itself is Celery's job (a task framework re-delivering its
own message via the broker, per ADR-005/006's "why Celery, not raw AMQP
retry queues" distinction). What RabbitMQ contributes on top is the
*terminal* case: `task_acks_on_failure_or_timeout=False` below means that
when a task is done retrying and still fails, Celery does not ack the
message -- combined with `task_acks_late=True`, RabbitMQ then routes it via
each queue's dead-letter-exchange to a `<queue>.dlq`, where it's inspectable
in the RabbitMQ management UI. That DLQ is the operator-visible record your
spec asks for; it is not something the application code writes to directly.
"""
from __future__ import annotations

import os

from celery import Celery
from kombu import Exchange, Queue

# Every Celery processing queue gets its own dead-letter binding onto this
# single DLX, each landing in its own `<queue>.dlq` for easy inspection.
TASKS_DLX_NAME = "tasks.dlx"
PROCESSING_QUEUE_NAMES = ["ai.processing.queue", "integration.processing.queue", "notification.queue"]


def _build_task_queues() -> list[Queue]:
    dlx = Exchange(TASKS_DLX_NAME, type="direct", durable=True)
    default_exchange = Exchange("celery", type="direct", durable=True)

    queues: list[Queue] = []
    for name in PROCESSING_QUEUE_NAMES:
        dead_routing_key = f"{name}.dead"
        queues.append(Queue(
            name, exchange=default_exchange, routing_key=name, durable=True,
            queue_arguments={
                "x-dead-letter-exchange": TASKS_DLX_NAME,
                "x-dead-letter-routing-key": dead_routing_key,
            },
        ))
        queues.append(Queue(
            f"{name}.dlq", exchange=dlx, routing_key=dead_routing_key, durable=True,
        ))
    return queues


def make_celery_app(name: str) -> Celery:
    broker_url = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")
    backend_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

    app = Celery(name, broker=broker_url, backend=backend_url)
    app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_acks_late=True,                    # ack only after the task finishes -> crash-safe redelivery
        task_acks_on_failure_or_timeout=False,   # do NOT ack a terminally-failed task -> it dead-letters (see docstring)
        worker_prefetch_multiplier=1,            # don't hoard messages away from other workers
        task_reject_on_worker_lost=True,
        task_queues=_build_task_queues(),
        task_default_queue="ai.processing.queue",
        broker_transport_options={
            "confirm_publish": True,
        },
    )
    return app
