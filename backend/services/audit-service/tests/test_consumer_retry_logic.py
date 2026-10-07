"""
Tests the audit consumer's retry/DLQ decision logic in isolation, using
fake exchange objects instead of a real RabbitMQ connection -- verifies the
same behavior the live consumer would exhibit: retry on failure up to
MAX_RETRIES with the correct per-message TTL, then dead-letter.
"""
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.consumer import AuditConsumer, RETRY_COUNT_HEADER, RETRY_QUEUE_NAME, DLQ_NAME
from shared.messaging.retry_policy import RETRY_DELAYS, MAX_RETRIES


def _fake_message(body: bytes, headers: dict | None = None):
    return SimpleNamespace(body=body, headers=headers or {})


@pytest.mark.asyncio
async def test_first_failure_is_scheduled_for_retry_with_first_delay_tier():
    retry_exchange = AsyncMock()
    dlx_exchange = AsyncMock()
    consumer = AuditConsumer(retry_exchange=retry_exchange, dlx_exchange=dlx_exchange)

    message = _fake_message(b'{"event_type": "workflow.completed"}')
    await consumer._handle_failure(message, {"event_type": "workflow.completed"}, retry_count=0, exc=RuntimeError("db down"))

    retry_exchange.publish.assert_awaited_once()
    dlx_exchange.publish.assert_not_awaited()
    published_message = retry_exchange.publish.call_args.args[0]
    assert published_message.headers[RETRY_COUNT_HEADER] == 1
    assert published_message.expiration == str(RETRY_DELAYS[0] * 1000)
    assert retry_exchange.publish.call_args.kwargs["routing_key"] == RETRY_QUEUE_NAME


@pytest.mark.asyncio
async def test_middle_failure_uses_escalating_delay_tier():
    retry_exchange = AsyncMock()
    dlx_exchange = AsyncMock()
    consumer = AuditConsumer(retry_exchange=retry_exchange, dlx_exchange=dlx_exchange)

    message = _fake_message(b'{}')
    await consumer._handle_failure(message, {"event_type": "x"}, retry_count=1, exc=RuntimeError("still down"))

    published_message = retry_exchange.publish.call_args.args[0]
    assert published_message.expiration == str(RETRY_DELAYS[1] * 1000)
    assert published_message.headers[RETRY_COUNT_HEADER] == 2


@pytest.mark.asyncio
async def test_exhausted_retries_go_to_dlq_not_retry_queue():
    retry_exchange = AsyncMock()
    dlx_exchange = AsyncMock()
    consumer = AuditConsumer(retry_exchange=retry_exchange, dlx_exchange=dlx_exchange)

    message = _fake_message(b'{}')
    await consumer._handle_failure(message, {"event_type": "x"}, retry_count=MAX_RETRIES, exc=RuntimeError("permanently down"))

    retry_exchange.publish.assert_not_awaited()
    dlx_exchange.publish.assert_awaited_once()
    assert dlx_exchange.publish.call_args.kwargs["routing_key"] == DLQ_NAME
