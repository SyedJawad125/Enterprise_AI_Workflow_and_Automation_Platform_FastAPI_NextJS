from datetime import datetime

from pydantic import BaseModel


class CreateWorkflowRequest(BaseModel):
    name: str
    description: str = ""


class WorkflowResponse(BaseModel):
    id: str
    name: str
    status: str
    version: int


class ExecuteWorkflowRequest(BaseModel):
    input_text: str
    customer_id: str | None = None
    order_id: str | None = None


class ExecuteWorkflowResponse(BaseModel):
    execution_id: str
    correlation_id: str
    status: str
    idempotent_replay: bool = False


class ExecutionStatusResponse(BaseModel):
    execution_id: str
    workflow_id: str
    status: str
    current_step: str
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None
    steps: list[dict]
    approval: dict | None


class ApprovalDecisionRequest(BaseModel):
    decided_by: str = "approver"
