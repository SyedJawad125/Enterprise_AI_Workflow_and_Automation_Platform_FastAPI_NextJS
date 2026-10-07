"""
Versioned event contracts shared by every producer/consumer in the platform.

Every event that goes onto RabbitMQ is an EventEnvelope. The envelope never
changes shape; only `payload` differs per `event_type`. `event_version`
lets a consumer branch on schema changes without breaking older producers.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _uuid() -> str:
    return str(uuid.uuid4())


EventType = Literal[
    "workflow.created",
    "workflow.started",
    "workflow.step.started",
    "workflow.step.completed",
    "workflow.step.failed",
    "ai.requested",
    "ai.completed",
    "integration.requested",
    "integration.completed",
    "approval.requested",
    "approval.completed",
    "notification.requested",
    "workflow.completed",
    "workflow.failed",
]


class EventEnvelope(BaseModel):
    event_id: str = Field(default_factory=_uuid)
    event_type: EventType
    event_version: int = 1
    timestamp: datetime = Field(default_factory=_now)
    correlation_id: str
    workflow_id: Optional[str] = None
    execution_id: Optional[str] = None
    payload: dict[str, Any] = Field(default_factory=dict)


# ---- Individual payload schemas (used for validation before publish) ----

class WorkflowCreatedPayload(BaseModel):
    workflow_id: str
    name: str
    created_by: str


class WorkflowStartedPayload(BaseModel):
    execution_id: str
    workflow_id: str
    input_data: dict[str, Any] = {}


class WorkflowStepStartedPayload(BaseModel):
    execution_id: str
    step_name: str


class WorkflowStepCompletedPayload(BaseModel):
    execution_id: str
    step_name: str
    result: dict[str, Any] = {}
    duration_ms: int


class WorkflowStepFailedPayload(BaseModel):
    execution_id: str
    step_name: str
    error_type: str
    error_message: str
    retry_count: int


class AIRequestedPayload(BaseModel):
    execution_id: str
    step_name: str
    input_data: dict[str, Any]


class AICompletedPayload(BaseModel):
    execution_id: str
    step_name: str
    decision: dict[str, Any]
    requires_approval: bool
    tokens_used: int
    estimated_cost: float


class IntegrationRequestedPayload(BaseModel):
    execution_id: str
    action: str
    parameters: dict[str, Any]
    idempotency_key: str


class IntegrationCompletedPayload(BaseModel):
    execution_id: str
    action: str
    success: bool
    result: dict[str, Any] = {}


class ApprovalRequestedPayload(BaseModel):
    execution_id: str
    approval_id: str
    recommendation: dict[str, Any]
    risk_level: str


class ApprovalCompletedPayload(BaseModel):
    execution_id: str
    approval_id: str
    approved: bool
    approved_by: str


class NotificationRequestedPayload(BaseModel):
    execution_id: str
    channel: Literal["email", "in_app", "webhook"]
    recipient: str
    message: str


class WorkflowCompletedPayload(BaseModel):
    execution_id: str
    duration_ms: int


class WorkflowFailedPayload(BaseModel):
    execution_id: str
    reason: str
