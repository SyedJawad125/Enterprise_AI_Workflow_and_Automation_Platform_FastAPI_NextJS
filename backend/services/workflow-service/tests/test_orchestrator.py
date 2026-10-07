"""
Tests the workflow state machine (app/orchestrator.py) in isolation --
RabbitMQ/Celery dispatch calls and audit publishing are mocked (see
conftest.py) so this verifies pure state-transition logic: the same logic
that decides CREATED -> RUNNING -> WAITING_FOR_APPROVAL -> COMPLETED/FAILED.
"""
import pytest
from sqlalchemy import select

from app.models import Approval, StepExecution, Workflow, WorkflowExecution
from app.orchestrator import (
    handle_ai_step_result,
    handle_approval_decision,
    handle_integration_step_result,
    handle_notification_step_result,
    start_execution,
)


async def _make_execution(db_session, input_data=None) -> WorkflowExecution:
    workflow = Workflow(name="Customer Request Workflow", created_by="test")
    db_session.add(workflow)
    await db_session.commit()
    await db_session.refresh(workflow)

    execution = WorkflowExecution(
        workflow_id=workflow.id,
        correlation_id="corr-1",
        status="QUEUED",
        input_data=input_data or {"input_text": "wrong item", "customer_id": "cust_1001", "order_id": "ord_5001"},
    )
    db_session.add(execution)
    await db_session.commit()
    await db_session.refresh(execution)
    return execution


@pytest.mark.asyncio
async def test_start_execution_dispatches_ai_step_and_sets_running(db_session, dispatch_recorder):
    execution = await _make_execution(db_session)
    await start_execution(db_session, execution)

    assert execution.status == "RUNNING"
    assert execution.current_step == "ai_analysis"
    assert dispatch_recorder.calls[0][0] == "ai_step"
    assert dispatch_recorder.calls[0][1]["execution_id"] == str(execution.id)


@pytest.mark.asyncio
async def test_ai_step_failure_marks_execution_failed(db_session, dispatch_recorder):
    execution = await _make_execution(db_session)
    await start_execution(db_session, execution)

    await handle_ai_step_result(db_session, execution, success=False, result={}, error="LLM timeout")

    assert execution.status == "FAILED"
    steps = (await db_session.scalars(select(StepExecution).where(StepExecution.execution_id == execution.id))).all()
    assert any(s.status == "FAILED" for s in steps)


@pytest.mark.asyncio
async def test_high_risk_decision_creates_pending_approval_and_pauses_execution(db_session, dispatch_recorder):
    execution = await _make_execution(db_session)
    await start_execution(db_session, execution)

    ai_result = {
        "requires_approval": True,
        "decision": {"recommended_action": "refund", "risk_level": "high", "reasoning": "amount over threshold"},
        "intent": {"intent": "refund_request"},
        "tool_results": {},
    }
    await handle_ai_step_result(db_session, execution, success=True, result=ai_result, error=None)

    assert execution.status == "WAITING_FOR_APPROVAL"
    approval = await db_session.scalar(select(Approval).where(Approval.execution_id == execution.id))
    assert approval is not None
    assert approval.status == "PENDING"
    assert approval.risk_level == "high"
    # Approver gets pinged via a notification dispatch, but the execution
    # itself must NOT have moved on to execute_action yet.
    assert not any(name == "integration_step" for name, _ in dispatch_recorder.calls)


@pytest.mark.asyncio
async def test_low_risk_decision_skips_approval_and_dispatches_refund(db_session, dispatch_recorder):
    execution = await _make_execution(db_session)
    await start_execution(db_session, execution)

    ai_result = {
        "requires_approval": False,
        "decision": {"recommended_action": "refund", "risk_level": "low", "reasoning": "small amount, auto-approved"},
        "intent": {"intent": "refund_request"},
        "tool_results": {},
    }
    await handle_ai_step_result(db_session, execution, success=True, result=ai_result, error=None)

    assert execution.status == "RUNNING"
    assert execution.current_step == "execute_action"
    assert any(name == "integration_step" for name, _ in dispatch_recorder.calls)


@pytest.mark.asyncio
async def test_approval_approved_proceeds_to_execute_action(db_session, dispatch_recorder):
    execution = await _make_execution(db_session)
    await start_execution(db_session, execution)
    ai_result = {
        "requires_approval": True,
        "decision": {"recommended_action": "refund", "risk_level": "high", "reasoning": "large amount"},
        "intent": {"intent": "refund_request"}, "tool_results": {},
    }
    await handle_ai_step_result(db_session, execution, success=True, result=ai_result, error=None)
    approval = await db_session.scalar(select(Approval).where(Approval.execution_id == execution.id))

    await handle_approval_decision(db_session, execution, approval, approved=True, decided_by="approver-1")

    assert approval.status == "APPROVED"
    assert execution.current_step == "execute_action"
    assert any(name == "integration_step" for name, _ in dispatch_recorder.calls)


@pytest.mark.asyncio
async def test_approval_rejected_cancels_and_notifies_without_refund(db_session, dispatch_recorder):
    execution = await _make_execution(db_session)
    await start_execution(db_session, execution)
    ai_result = {
        "requires_approval": True,
        "decision": {"recommended_action": "refund", "risk_level": "high", "reasoning": "large amount"},
        "intent": {"intent": "refund_request"}, "tool_results": {},
    }
    await handle_ai_step_result(db_session, execution, success=True, result=ai_result, error=None)
    approval = await db_session.scalar(select(Approval).where(Approval.execution_id == execution.id))

    await handle_approval_decision(db_session, execution, approval, approved=False, decided_by="approver-1")

    assert approval.status == "REJECTED"
    assert execution.status == "CANCELLED"
    assert not any(name == "integration_step" for name, _ in dispatch_recorder.calls)
    assert any(name == "notification_step" for name, _ in dispatch_recorder.calls)


@pytest.mark.asyncio
async def test_integration_step_success_dispatches_notify(db_session, dispatch_recorder):
    execution = await _make_execution(db_session)
    await start_execution(db_session, execution)
    ai_result = {
        "requires_approval": False,
        "decision": {"recommended_action": "refund", "risk_level": "low", "reasoning": "auto"},
        "intent": {"intent": "refund_request"}, "tool_results": {},
    }
    await handle_ai_step_result(db_session, execution, success=True, result=ai_result, error=None)

    await handle_integration_step_result(
        db_session, execution, success=True, result={"payment_id": "pay_1", "amount": 20.0}, error=None
    )

    assert execution.current_step == "notify"
    assert any(name == "notification_step" for name, _ in dispatch_recorder.calls)


@pytest.mark.asyncio
async def test_integration_step_failure_marks_execution_failed(db_session, dispatch_recorder):
    execution = await _make_execution(db_session)
    await start_execution(db_session, execution)
    ai_result = {
        "requires_approval": False,
        "decision": {"recommended_action": "refund", "risk_level": "low", "reasoning": "auto"},
        "intent": {"intent": "refund_request"}, "tool_results": {},
    }
    await handle_ai_step_result(db_session, execution, success=True, result=ai_result, error=None)

    await handle_integration_step_result(db_session, execution, success=False, result={}, error="payment API down")

    assert execution.status == "FAILED"


@pytest.mark.asyncio
async def test_final_notification_completes_execution(db_session, dispatch_recorder):
    execution = await _make_execution(db_session)
    await start_execution(db_session, execution)
    ai_result = {
        "requires_approval": False,
        "decision": {"recommended_action": "refund", "risk_level": "low", "reasoning": "auto"},
        "intent": {"intent": "refund_request"}, "tool_results": {},
    }
    await handle_ai_step_result(db_session, execution, success=True, result=ai_result, error=None)
    await handle_integration_step_result(db_session, execution, success=True, result={"payment_id": "pay_1"}, error=None)

    await handle_notification_step_result(db_session, execution, success=True, result={"status": "delivered_mock"}, error=None)

    assert execution.status == "COMPLETED"
    assert execution.current_step == "completed"
    assert execution.completed_at is not None


@pytest.mark.asyncio
async def test_ai_fail_decision_marks_execution_failed_and_still_notifies(db_session, dispatch_recorder):
    """
    Covers the audit fix: a failed customer/order lookup (or invalid AI
    output that couldn't be repaired) must FAIL the workflow, not silently
    complete it and not ask a human to approve a decision built on missing
    data.
    """
    execution = await _make_execution(db_session)
    await start_execution(db_session, execution)

    ai_result = {
        "requires_approval": False,
        "decision": {"recommended_action": "fail", "risk_level": "high", "reasoning": "order_lookup failed: 404"},
        "intent": {"intent": "refund_request"},
        "tool_results": {"order_lookup": {"error": "404"}},
    }
    await handle_ai_step_result(db_session, execution, success=True, result=ai_result, error=None)

    assert execution.status == "FAILED"
    # Must not have proceeded to the side-effecting refund call.
    assert not any(name == "integration_step" for name, _ in dispatch_recorder.calls)
    # Customer still gets told something went wrong.
    assert any(name == "notification_step" for name, _ in dispatch_recorder.calls)

    await handle_notification_step_result(db_session, execution, success=True, result={"status": "delivered_mock"}, error=None)

    # Status must remain FAILED -- the final notification must not flip it to COMPLETED.
    assert execution.status == "FAILED"
