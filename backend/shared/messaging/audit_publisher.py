"""
Lightweight fire-and-forget publisher onto `events.exchange` (topic exchange)
for anything that should show up in the audit trail. Audit Service is the
sole consumer, bound to `audit.queue` with routing key `#` (everything).

This is deliberately a raw aio_pika publish (not a Celery task): audit
writes must never block or fail the primary operation, and they don't need
retries/backoff semantics -- if RabbitMQ is briefly unavailable we log and
move on rather than let audit logging take down a workflow step.
"""
from __future__ import annotations

import json
import os

import aio_pika

from shared.event_contracts import EventEnvelope
from shared.logging.logger import get_logger

logger = get_logger("shared.messaging.audit_publisher")

EXCHANGE_NAME = "events.exchange"


async def publish_audit_event(envelope: EventEnvelope) -> None:
    rabbitmq_url = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")
    try:
        connection = await aio_pika.connect_robust(rabbitmq_url, timeout=5)
        async with connection:
            channel = await connection.channel()
            exchange = await channel.declare_exchange(
                EXCHANGE_NAME, aio_pika.ExchangeType.TOPIC, durable=True
            )
            body = envelope.model_dump_json().encode()
            await exchange.publish(
                aio_pika.Message(
                    body=body,
                    content_type="application/json",
                    message_id=envelope.event_id,
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                ),
                routing_key=envelope.event_type,
            )
    except Exception as exc:  # noqa: BLE001 -- audit publishing must never raise upstream
        logger.error(
            "failed to publish audit event",
            extra={"event_type": envelope.event_type, "error": str(exc)},
        )
