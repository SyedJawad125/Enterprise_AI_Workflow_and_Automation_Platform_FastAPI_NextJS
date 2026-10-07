"""
The workflow state machine. Plain Python/SQLAlchemy -- deliberately NOT
LangGraph, per the architecture rule that deterministic orchestration stays
out of the AI framework. This module is the only place execution status
transitions happen, which is what makes the state machine auditable and
testable in isolation (see tests/unit/test_orchestrator.py).

Step sequence for the built-in "Customer Request" workflow:

    ai_analysis -> [approval gate if required] -> execute_action -> notify -> COMPLETED

`execute_action` is skipped when the AI decision does not recommend a
side-effecting action (e.g. a plain support-ticket response) -- the graph
goes straight to `notify`.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.events import emit
from app.models import Approval, StepExecution, WorkflowExecution
from app.tasks_client import dispatch_ai_step, dispatch_integration_step, dispatch_notification_step
from shared.logging.logger import get_logger

logger = get_logger("workflow-service.orchestrator")

SIDE_EFFECTING_ACTIONS = {"refund"}


async def start_execution(db: AsyncSession, execution: WorkflowExecution) -> None:
    execution.status = "RUNNING"
    execution.current_step = "ai_analysis"
    db.add(StepExecution(execution_id=execution.id, step_name="ai_analysis", status="RUNNING"))
    await db.commit()

    await emit("workflow.started", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                {"input_data": execution.input_data})
    await emit("workflow.step.started", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                {"step_name": "ai_analysis"})

    dispatch_ai_step(
        execution_id=str(execution.id),
        correlation_id=execution.correlation_id,
        input_text=execution.input_data.get("input_text", ""),
        customer_id=execution.input_data.get("customer_id"),
        order_id=execution.input_data.get("order_id"),
    )
    logger.info("execution started", extra={"execution_id": str(execution.id)})


async def handle_ai_step_result(db: AsyncSession, execution: WorkflowExecution, success: bool, result: dict, error: str | None) -> None:
    step = StepExecution(
        execution_id=execution.id, step_name="ai_analysis",
        status="COMPLETED" if success else "FAILED", result=result or {}, error=error,
        completed_at=datetime.now(timezone.utc),
    )
    db.add(step)

    if not success:
        execution.status = "FAILED"
        await db.commit()
        await emit("workflow.step.failed", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                    {"step_name": "ai_analysis", "error": error})
        await emit("workflow.failed", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                    {"reason": error})
        return

    await db.commit()
    await emit("workflow.step.completed", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                {"step_name": "ai_analysis", "result": result})
    await emit("ai.completed", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                {"decision": result.get("decision"), "requires_approval": result.get("requires_approval")})

    decision = result.get("decision", {})

    if result.get("requires_approval"):
        execution.status = "WAITING_FOR_APPROVAL"
        approval = Approval(
            execution_id=execution.id,
            recommendation={
                "decision": decision,
                "intent": result.get("intent"),
                "evidence": result.get("tool_results"),
            },
            risk_level=decision.get("risk_level", "low"),
        )
        db.add(approval)
        await db.commit()
        await emit("approval.requested", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                    {"risk_level": approval.risk_level, "recommendation": approval.recommendation})
        dispatch_notification_step(
            execution_id=str(execution.id), correlation_id=execution.correlation_id,
            channel="in_app", recipient="approver-queue",
            message=f"Approval required for execution {execution.id}: {decision.get('reasoning', '')}",
        )
        logger.info("execution waiting for approval", extra={"execution_id": str(execution.id)})
        return

    await _proceed_after_decision(db, execution, decision)


async def _proceed_after_decision(db: AsyncSession, execution: WorkflowExecution, decision: dict) -> None:
    action = decision.get("recommended_action", "")

    if action == "fail":
        # AI explicitly determined the step cannot proceed (e.g. a lookup
        # failed, or output validation failed even after a repair attempt).
        # This is a terminal failure, not a success path -- do NOT fall
        # through to the notify-as-success branch below.
        execution.status = "FAILED"
        await db.commit()
        await emit("workflow.step.failed", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                    {"step_name": "ai_analysis", "reason": decision.get("reasoning", "")})
        await emit("workflow.failed", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                    {"reason": decision.get("reasoning", "AI analysis failed")})
        await _dispatch_notify(db, execution, message="We were unable to process your request automatically. Our team has been notified.")
        return

    if action in SIDE_EFFECTING_ACTIONS:
        execution.current_step = "execute_action"
        db.add(StepExecution(execution_id=execution.id, step_name="execute_action", status="RUNNING"))
        await db.commit()
        await emit("workflow.step.started", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                    {"step_name": "execute_action"})
        order_id = execution.input_data.get("order_id")
        dispatch_integration_step(
            execution_id=str(execution.id), correlation_id=execution.correlation_id,
            action="refund",
            parameters={"order_id": order_id, "amount": decision.get("amount", 0) or 50.0, "reason": decision.get("reasoning", "")},
        )
    else:
        await _dispatch_notify(db, execution, message=decision.get("reasoning", "Your request has been processed."))


async def handle_approval_decision(db: AsyncSession, execution: WorkflowExecution, approval: Approval, approved: bool, decided_by: str) -> None:
    approval.status = "APPROVED" if approved else "REJECTED"
    approval.decided_at = datetime.now(timezone.utc)
    approval.decided_by = decided_by
    await db.commit()
    await emit("approval.completed", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                {"approval_id": str(approval.id), "approved": approved, "approved_by": decided_by})

    if not approved:
        execution.status = "CANCELLED"
        await db.commit()
        await _dispatch_notify(db, execution, message="Your request was reviewed and could not be approved.")
        return

    execution.status = "RUNNING"
    await db.commit()
    await _proceed_after_decision(db, execution, approval.recommendation.get("decision", {}))


async def handle_integration_step_result(db: AsyncSession, execution: WorkflowExecution, success: bool, result: dict, error: str | None) -> None:
    step = StepExecution(
        execution_id=execution.id, step_name="execute_action",
        status="COMPLETED" if success else "FAILED", result=result or {}, error=error,
        completed_at=datetime.now(timezone.utc),
    )
    db.add(step)
    if not success:
        execution.status = "FAILED"
        await db.commit()
        await emit("workflow.step.failed", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                    {"step_name": "execute_action", "error": error})
        await emit("workflow.failed", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                    {"reason": error})
        return

    await db.commit()
    await emit("workflow.step.completed", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                {"step_name": "execute_action", "result": result})
    await emit("integration.completed", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                {"action": "refund", "success": True, "result": result})

    await _dispatch_notify(db, execution, message=f"Your refund of ${result.get('amount', 0)} has been processed.")


def _to_utc_aware(dt: datetime) -> datetime:
    """Normalizes a datetime to timezone-aware UTC. Guards against DB
    backends (e.g. SQLite, used in tests) that round-trip
    DateTime(timezone=True) columns as naive datetimes -- Postgres (used in
    every real deployment) preserves tzinfo, but this function makes the
    duration calculation correct regardless of backend."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


async def _dispatch_notify(db: AsyncSession, execution: WorkflowExecution, message: str) -> None:
    execution.current_step = "notify"
    db.add(StepExecution(execution_id=execution.id, step_name="notify", status="RUNNING"))
    await db.commit()
    await emit("workflow.step.started", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                {"step_name": "notify"})
    dispatch_notification_step(
        execution_id=str(execution.id), correlation_id=execution.correlation_id,
        channel="email", recipient=execution.input_data.get("customer_id", "unknown"), message=message,
    )


async def handle_notification_step_result(db: AsyncSession, execution: WorkflowExecution, success: bool, result: dict, error: str | None) -> None:
    step = StepExecution(
        execution_id=execution.id, step_name="notify",
        status="COMPLETED" if success else "FAILED", result=result or {}, error=error,
        completed_at=datetime.now(timezone.utc),
    )
    db.add(step)

    if execution.status == "WAITING_FOR_APPROVAL":
        # This was the "notify the approver queue" side-notification, not the
        # final customer notification -- execution stays WAITING_FOR_APPROVAL.
        await db.commit()
        return

    if not success:
        execution.status = "FAILED"
        await db.commit()
        await emit("workflow.step.failed", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                    {"step_name": "notify", "error": error})
        return

    already_terminal = execution.status in ("CANCELLED", "FAILED")
    execution.status = "COMPLETED" if not already_terminal else execution.status
    execution.current_step = "completed"
    execution.completed_at = datetime.now(timezone.utc)
    await db.commit()
    await emit("workflow.step.completed", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                {"step_name": "notify", "result": result})

    if already_terminal:
        # workflow.failed / a CANCELLED transition already emitted its own
        # terminal event earlier in the flow -- don't also emit
        # workflow.completed for a workflow that didn't actually complete.
        logger.info("final notification sent for non-completed execution",
                    extra={"execution_id": str(execution.id), "status": execution.status})
        return

    duration_ms = int(
        (_to_utc_aware(execution.completed_at) - _to_utc_aware(execution.created_at)).total_seconds() * 1000
    )
    await emit("workflow.completed", execution.correlation_id, str(execution.workflow_id), str(execution.id),
                {"duration_ms": duration_ms})
    logger.info("execution completed", extra={"execution_id": str(execution.id), "status": execution.status})
