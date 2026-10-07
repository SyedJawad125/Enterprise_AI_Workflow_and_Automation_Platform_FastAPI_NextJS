"""
The one genuine raw-AMQP consumer in the platform (everything else async
uses Celery, which manages its own retry/redelivery -- see ADR-003/005 for
why these are deliberately different mechanisms). This consumer implements
the classic RabbitMQ retry cascade your spec asks for explicitly:

    audit.queue --(processing fails)--> audit.retry.queue (TTL: 5s/15s/30s)
        --(TTL expires, dead-lettered)--> back into events.exchange
        --(re-delivered)--> audit.queue
        ... up to MAX_RETRIES attempts ...
        --(still failing)--> audit.queue.dlq  (terminal, operator-inspectable)

The retry count travels on the message as a header (`x-audit-retry-count`)
that we increment ourselves each time we hand it to the retry queue -- this
is what lets one retry queue serve all three delay tiers (5s/15s/30s)
instead of needing three separate queues: each message carries its own
per-message TTL (`expiration`) chosen from that header, rather than relying
on a fixed queue-level TTL.

Duplicate-delivery safety: the Postgres insert is `ON CONFLICT DO NOTHING`
on the unique `event_id`, so a message that gets redelivered (after a crash
between DB commit and ack, for instance) is a no-op the second time --
this is what "at-least-once delivery, idempotent consumer" means in
practice, not just in the docstring.
"""
from __future__ import annotations

import asyncio
import json

import aio_pika
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.core.config import RABBITMQ_URL
from app.db import SessionLocal
from app.models import AuditEvent
from shared.logging.logger import get_logger
from shared.messaging.retry_policy import next_retry_delay

logger = get_logger("audit-service.consumer")

EXCHANGE_NAME = "events.exchange"
QUEUE_NAME = "audit.queue"
DLX_NAME = "events.dlx"
DLQ_NAME = "audit.queue.dlq"
RETRY_EXCHANGE_NAME = "audit.retry.exchange"
RETRY_QUEUE_NAME = "audit.retry.queue"
RETRY_COUNT_HEADER = "x-audit-retry-count"


async def _persist_event(data: dict) -> None:
    async with SessionLocal() as session:
        stmt = (
            pg_insert(AuditEvent)
            .values(
                event_id=data["event_id"],
                event_type=data["event_type"],
                correlation_id=data["correlation_id"],
                workflow_id=data.get("workflow_id"),
                execution_id=data.get("execution_id"),
                payload=data.get("payload", {}),
            )
            .on_conflict_do_nothing(index_elements=["event_id"])  # idempotent on duplicate delivery
        )
        await session.execute(stmt)
        await session.commit()


class AuditConsumer:
    """Bundles the channel-scoped exchange handles _handle_message needs to
    publish a failed message onward to the retry queue or the DLQ."""

    def __init__(self, retry_exchange: aio_pika.abc.AbstractExchange, dlx_exchange: aio_pika.abc.AbstractExchange):
        self.retry_exchange = retry_exchange
        self.dlx_exchange = dlx_exchange

    async def handle_message(self, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        async with message.process(requeue=False, ignore_processed=True):
            try:
                data = json.loads(message.body)
            except json.JSONDecodeError:
                logger.error("dropping unparseable audit message -- not retryable")
                return

            retry_count = int((message.headers or {}).get(RETRY_COUNT_HEADER, 0))
            try:
                await _persist_event(data)
                logger.info("audit event persisted", extra={"event_type": data["event_type"], "retry_count": retry_count})
            except Exception as exc:  # noqa: BLE001 -- DB down, constraint error, etc.
                await self._handle_failure(message, data, retry_count, exc)

    async def _handle_failure(self, message, data: dict, retry_count: int, exc: Exception) -> None:
        delay = next_retry_delay(retry_count)
        if delay is not None:
            logger.warning(
                "audit event processing failed, scheduling retry",
                extra={"event_type": data.get("event_type"), "retry_count": retry_count + 1,
                       "delay_seconds": delay, "error": str(exc)},
            )
            await self.retry_exchange.publish(
                aio_pika.Message(
                    body=message.body,
                    headers={**(message.headers or {}), RETRY_COUNT_HEADER: retry_count + 1},
                    content_type="application/json",
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    expiration=str(delay * 1000),  # per-message TTL in ms -- this queue's own delay tier
                ),
                routing_key=RETRY_QUEUE_NAME,
            )
        else:
            logger.error(
                "audit event exhausted all retries, sending to DLQ",
                extra={"event_type": data.get("event_type"), "retry_count": retry_count, "error": str(exc)},
            )
            await self.dlx_exchange.publish(
                aio_pika.Message(
                    body=message.body,
                    headers={**(message.headers or {}), RETRY_COUNT_HEADER: retry_count},
                    content_type="application/json",
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                ),
                routing_key=DLQ_NAME,
            )


async def run_consumer() -> None:
    while True:
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            async with connection:
                channel = await connection.channel()
                await channel.set_qos(prefetch_count=10)

                # Terminal dead-letter exchange + queue -- where events land
                # after exhausting retries, or immediately for anything the
                # retry loop can't help (an unparseable message never enters
                # this path at all; it's dropped, logged, and acked above).
                dlx = await channel.declare_exchange(DLX_NAME, aio_pika.ExchangeType.DIRECT, durable=True)
                dlq = await channel.declare_queue(DLQ_NAME, durable=True)
                await dlq.bind(dlx, routing_key=DLQ_NAME)

                # Main topic exchange + queue, catching every event type.
                exchange = await channel.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.TOPIC, durable=True)
                queue = await channel.declare_queue(
                    QUEUE_NAME, durable=True,
                    arguments={"x-dead-letter-exchange": DLX_NAME, "x-dead-letter-routing-key": DLQ_NAME},
                )
                await queue.bind(exchange, routing_key="#")

                # Retry queue: no queue-level TTL (each message carries its
                # own `expiration`, chosen per attempt from RETRY_DELAYS).
                # When a message's TTL expires, RabbitMQ dead-letters it back
                # into `events.exchange` using the routing key it was
                # published to THIS queue with (`audit.retry.queue`, set
                # below) -- not the original event's routing key. That's
                # fine here specifically because audit.queue is bound with
                # the catch-all "#", so it still matches and gets
                # re-delivered; a system with more selective bindings on
                # events.exchange would need `x-dead-letter-routing-key` set
                # explicitly per event type instead of relying on this.
                retry_exchange = await channel.declare_exchange(RETRY_EXCHANGE_NAME, aio_pika.ExchangeType.DIRECT, durable=True)
                retry_queue = await channel.declare_queue(
                    RETRY_QUEUE_NAME, durable=True,
                    arguments={"x-dead-letter-exchange": EXCHANGE_NAME},
                )
                await retry_queue.bind(retry_exchange, routing_key=RETRY_QUEUE_NAME)

                consumer = AuditConsumer(retry_exchange=retry_exchange, dlx_exchange=dlx)

                logger.info("audit consumer connected, listening on audit.queue (retry: 5s/15s/30s, then DLQ)")
                await queue.consume(consumer.handle_message)
                await asyncio.Future()  # run forever until connection drops
        except Exception as exc:  # noqa: BLE001
            logger.error("audit consumer disconnected, retrying in 5s", extra={"error": str(exc)})
            await asyncio.sleep(5)
