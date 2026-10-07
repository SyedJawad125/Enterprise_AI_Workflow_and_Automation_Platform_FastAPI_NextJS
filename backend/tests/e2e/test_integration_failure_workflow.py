"""
The failure E2E scenario from your spec section 26: an integration lookup
fails (nonexistent order), and the workflow must reach a clean terminal
FAILED state -- not silently hang, not get marked COMPLETED, and not ask a
human to approve a decision built on missing data (see the audit fix in
app/langgraph_flow.py's node_decision / app/orchestrator.py's
_proceed_after_decision "fail" branch).

Also exercises the retry-safety fix directly: `ord_9999` doesn't exist, so
Integration Service returns 404 for the order_lookup tool call during AI
analysis. Per shared/messaging/retry_policy.py, a 404 is NOT retried -- this
test's tight timeout would fail if that classification regressed and the
call started burning through 5s/15s/30s retries it was never going to win.
"""
import pytest
import httpx

from tests.e2e.conftest import GATEWAY_URL, poll_execution_status

pytestmark = pytest.mark.e2e


def test_lookup_failure_marks_workflow_failed_not_completed_or_waiting(registered_user):
    token = registered_user["token"]
    headers = {"Authorization": f"Bearer {token}"}

    with httpx.Client(base_url=GATEWAY_URL, timeout=15) as client:
        create_resp = client.post("/api/v1/workflows", json={"name": "E2E Integration Failure Workflow"}, headers=headers)
        workflow_id = create_resp.json()["id"]

        execute_resp = client.post(
            f"/api/v1/workflows/{workflow_id}/execute",
            json={
                "input_text": "I want a refund for my order.",
                "customer_id": "cust_1001",
                "order_id": "ord_9999",  # does not exist in Integration Service's mock data
            },
            headers=headers,
        )
        assert execute_resp.status_code == 202
        execution_id = execute_resp.json()["execution_id"]

        # Bounded to well under what 3 retries with backoff would take, so a
        # regression back to "retry everything blindly" would show up as a
        # timeout here, not just a wrong final status.
        status = poll_execution_status(client, execution_id, token, timeout_seconds=10.0)

        assert status["status"] == "FAILED", (
            f"expected FAILED for an unresolvable order lookup, got {status.get('status')}, "
            f"steps={status.get('steps')}"
        )
        assert status["approval"] is None, "a failed lookup must not create a pending approval"

        ai_step = next(s for s in status["steps"] if s["step_name"] == "ai_analysis")
        assert ai_step["status"] == "COMPLETED"  # the AI step itself ran fine; its DECISION was "fail"

        audit_resp = client.get(f"/api/v1/audit/events?execution_id={execution_id}", headers=headers)
        event_types = {e["event_type"] for e in audit_resp.json()["items"]}
        assert "workflow.step.failed" in event_types
        assert "workflow.failed" in event_types
        assert "workflow.completed" not in event_types
