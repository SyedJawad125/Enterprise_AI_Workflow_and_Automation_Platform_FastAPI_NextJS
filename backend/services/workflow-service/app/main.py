import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import uuid

from fastapi import Depends, FastAPI, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.exceptions import NotFoundError, ValidationAppError, install_exception_handlers
from shared.health import check_postgres, check_rabbitmq, check_redis
from shared.logging.logger import RequestContextMiddleware, get_logger

from app.core.config import RABBITMQ_URL, REDIS_URL
from app.db import get_db, engine
from app.models import Approval, StepExecution, Workflow, WorkflowExecution
from app.orchestrator import (
    handle_ai_step_result,
    handle_approval_decision,
    handle_integration_step_result,
    handle_notification_step_result,
    start_execution,
)
from app.schemas import (
    ApprovalDecisionRequest,
    CreateWorkflowRequest,
    ExecuteWorkflowRequest,
    ExecuteWorkflowResponse,
    ExecutionStatusResponse,
    WorkflowResponse,
)

logger = get_logger("workflow-service")

app = FastAPI(title="Workflow Service")
app.add_middleware(RequestContextMiddleware)
install_exception_handlers(app)


@app.on_event("startup")
async def on_startup():
    # Schema is now owned by Alembic (run as the Dockerfile's CMD, before
    # this process starts -- see ADR-011), not by create_all() here. This
    # service is the reference implementation the other three services'
    # create_all()-at-startup approach should be migrated to next.
    logger.info("workflow-service started")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "workflow-service"}


@app.get("/ready")
async def ready():
    postgres_status = await check_postgres(engine)
    redis_status = await check_redis(REDIS_URL)
    rabbitmq_status = await check_rabbitmq(RABBITMQ_URL)
    deps = {"postgres": postgres_status, "redis": redis_status, "rabbitmq": rabbitmq_status}
    status = "ready" if all(v == "healthy" for v in deps.values()) else "not_ready"
    return JSONResponse(
        status_code=200 if status == "ready" else 503,
        content={"status": status, "service": "workflow-service", "dependencies": deps},
    )


# ---------------------------------------------------------------- Workflows

@app.post("/workflows", response_model=WorkflowResponse, status_code=201)
async def create_workflow(payload: CreateWorkflowRequest, db: AsyncSession = Depends(get_db)):
    workflow = Workflow(name=payload.name, description=payload.description, created_by="system")
    db.add(workflow)
    await db.commit()
    await db.refresh(workflow)
    return WorkflowResponse(id=str(workflow.id), name=workflow.name, status=workflow.status, version=workflow.version)


@app.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    workflow = await db.get(Workflow, workflow_id)
    if not workflow:
        raise NotFoundError("Workflow not found")
    return WorkflowResponse(id=str(workflow.id), name=workflow.name, status=workflow.status, version=workflow.version)


@app.post("/workflows/{workflow_id}/execute", response_model=ExecuteWorkflowResponse, status_code=202)
async def execute_workflow(
    workflow_id: uuid.UUID,
    payload: ExecuteWorkflowRequest,
    db: AsyncSession = Depends(get_db),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    workflow = await db.get(Workflow, workflow_id)
    if not workflow:
        raise NotFoundError("Workflow not found")

    if idempotency_key:
        existing = await db.scalar(
            select(WorkflowExecution).where(
                WorkflowExecution.workflow_id == workflow_id,
                WorkflowExecution.idempotency_key == idempotency_key,
            )
        )
        if existing:
            logger.info("idempotent replay of workflow execution",
                        extra={"execution_id": str(existing.id), "idempotency_key": idempotency_key})
            return ExecuteWorkflowResponse(
                execution_id=str(existing.id), correlation_id=existing.correlation_id,
                status=existing.status, idempotent_replay=True,
            )

    correlation_id = str(uuid.uuid4())
    execution = WorkflowExecution(
        workflow_id=workflow.id,
        correlation_id=correlation_id,
        idempotency_key=idempotency_key,
        status="QUEUED",
        input_data=payload.model_dump(),
    )
    db.add(execution)
    await db.commit()
    await db.refresh(execution)

    await start_execution(db, execution)

    return ExecuteWorkflowResponse(
        execution_id=str(execution.id), correlation_id=correlation_id, status=execution.status, idempotent_replay=False,
    )


async def _load_execution(db: AsyncSession, execution_id: uuid.UUID) -> WorkflowExecution:
    execution = await db.get(WorkflowExecution, execution_id)
    if not execution:
        raise NotFoundError("Workflow execution not found")
    return execution


@app.get("/workflows/executions/{execution_id}/status", response_model=ExecutionStatusResponse)
async def get_execution_status(execution_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    execution = await _load_execution(db, execution_id)
    steps = (await db.scalars(
        select(StepExecution).where(StepExecution.execution_id == execution_id).order_by(StepExecution.started_at)
    )).all()
    approval = await db.scalar(select(Approval).where(Approval.execution_id == execution_id))

    return ExecutionStatusResponse(
        execution_id=str(execution.id),
        workflow_id=str(execution.workflow_id),
        status=execution.status,
        current_step=execution.current_step,
        created_at=execution.created_at,
        updated_at=execution.updated_at,
        completed_at=execution.completed_at,
        steps=[
            {
                "step_name": s.step_name, "status": s.status, "result": s.result,
                "error": s.error, "retry_count": s.retry_count,
                "started_at": s.started_at.isoformat(),
                "completed_at": s.completed_at.isoformat() if s.completed_at else None,
            }
            for s in steps
        ],
        approval=(
            {
                "id": str(approval.id), "status": approval.status, "risk_level": approval.risk_level,
                "recommendation": approval.recommendation,
            }
            if approval else None
        ),
    )


# ---------------------------------------------------------------- Approvals

@app.post("/approvals/{approval_id}/approve")
async def approve(approval_id: uuid.UUID, payload: ApprovalDecisionRequest, db: AsyncSession = Depends(get_db)):
    approval = await db.get(Approval, approval_id)
    if not approval:
        raise NotFoundError("Approval not found")
    if approval.status != "PENDING":
        raise ValidationAppError("Approval has already been decided")
    execution = await _load_execution(db, approval.execution_id)
    await handle_approval_decision(db, execution, approval, approved=True, decided_by=payload.decided_by)
    return {"status": "approved"}


@app.post("/approvals/{approval_id}/reject")
async def reject(approval_id: uuid.UUID, payload: ApprovalDecisionRequest, db: AsyncSession = Depends(get_db)):
    approval = await db.get(Approval, approval_id)
    if not approval:
        raise NotFoundError("Approval not found")
    if approval.status != "PENDING":
        raise ValidationAppError("Approval has already been decided")
    execution = await _load_execution(db, approval.execution_id)
    await handle_approval_decision(db, execution, approval, approved=False, decided_by=payload.decided_by)
    return {"status": "rejected"}


@app.get("/approvals")
async def list_pending_approvals(db: AsyncSession = Depends(get_db)):
    rows = (await db.scalars(select(Approval).where(Approval.status == "PENDING"))).all()
    return [
        {"id": str(a.id), "execution_id": str(a.execution_id), "risk_level": a.risk_level, "recommendation": a.recommendation}
        for a in rows
    ]


# ---------------------------------------------------- Internal worker callbacks
# Called only by ai-worker / integration-worker / notification-worker, never
# by the public Gateway. In a hardened build these would sit behind a
# service-to-service auth secret (see ADR on service auth) -- omitted here
# to keep the demo runnable without extra credential wiring.

class StepResultPayload(BaseModel):
    success: bool
    result: dict = {}
    error: str | None = None


@app.post("/internal/executions/{execution_id}/steps/ai_analysis/complete")
async def internal_ai_step_complete(execution_id: uuid.UUID, payload: StepResultPayload, db: AsyncSession = Depends(get_db)):
    execution = await _load_execution(db, execution_id)
    await handle_ai_step_result(db, execution, payload.success, payload.result, payload.error)
    return {"status": "ok"}


@app.post("/internal/executions/{execution_id}/steps/execute_action/complete")
async def internal_integration_step_complete(execution_id: uuid.UUID, payload: StepResultPayload, db: AsyncSession = Depends(get_db)):
    execution = await _load_execution(db, execution_id)
    await handle_integration_step_result(db, execution, payload.success, payload.result, payload.error)
    return {"status": "ok"}


@app.post("/internal/executions/{execution_id}/steps/notify/complete")
async def internal_notify_step_complete(execution_id: uuid.UUID, payload: StepResultPayload, db: AsyncSession = Depends(get_db)):
    execution = await _load_execution(db, execution_id)
    await handle_notification_step_result(db, execution, payload.success, payload.result, payload.error)
    return {"status": "ok"}
