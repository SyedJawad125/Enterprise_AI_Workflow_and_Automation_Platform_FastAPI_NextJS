"""Thin async wrapper so route handlers don't need to know publish_audit_event's
signature -- builds a valid EventEnvelope and fires it (best-effort)."""
from __future__ import annotations

from shared.event_contracts import EventEnvelope
from shared.messaging import publish_audit_event


async def emit(event_type: str, correlation_id: str, workflow_id: str | None, execution_id: str | None, payload: dict) -> None:
    envelope = EventEnvelope(
        event_type=event_type,  # type: ignore[arg-type]
        correlation_id=correlation_id,
        workflow_id=workflow_id,
        execution_id=execution_id,
        payload=payload,
    )
    await publish_audit_event(envelope)
