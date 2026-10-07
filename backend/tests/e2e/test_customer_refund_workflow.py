"""
The complete happy-path E2E scenario from your spec section 25:

    Login -> Create workflow -> Execute -> RabbitMQ -> AI Worker -> AI
    Service -> Integration lookups -> Approval required -> Approve ->
    Integration action -> Notification -> Audit event -> COMPLETED

Requires the full docker-compose stack running (see conftest.py). Uses a
refund amount high enough to trigger the mock provider's risk gate
(>= $100), so this specifically exercises the human-in-the-loop path, not
just the auto-approved low-risk path.
"""
import pytest
import httpx

from tests.e2e.conftest import GATEWAY_URL, poll_execution_status

pytestmark = pytest.mark.e2e


def test_high_value_refund_requires_approval_then_completes(registered_user):
    token = registered_user["token"]
    headers = {"Authorization": f"Bearer {token}"}

    with httpx.Client(base_url=GATEWAY_URL, timeout=15) as client:
        create_resp = client.post("/api/v1/workflows", json={"name": "E2E Customer Refund Workflow"}, headers=headers)
        assert create_resp.status_code == 201, create_resp.text
        workflow_id = create_resp.json()["id"]

        execute_resp = client.post(
            f"/api/v1/workflows/{workflow_id}/execute",
            json={
                "input_text": "I received the wrong product and want a refund of $250.",
                "customer_id": "cust_1001",
                "order_id": "ord_5001",
            },
            headers=headers,
        )
        assert execute_resp.status_code == 202, execute_resp.text
        execution_id = execute_resp.json()["execution_id"]
        correlation_id = execute_resp.json()["correlation_id"]

        status = poll_execution_status(client, execution_id, token)
        assert status["status"] == "WAITING_FOR_APPROVAL", (
            f"expected the $250 refund to require approval, got status={status.get('status')}, "
            f"steps={status.get('steps')}"
        )
        assert status["approval"] is not None
        assert status["approval"]["status"] == "PENDING"
        assert status["approval"]["risk_level"] == "high"
        approval_id = status["approval"]["id"]

        approve_resp = client.post(
            f"/api/v1/approvals/{approval_id}/approve", json={"decided_by": "e2e-approver"}, headers=headers,
        )
        assert approve_resp.status_code == 200, approve_resp.text

        final_status = poll_execution_status(client, execution_id, token)
        assert final_status["status"] == "COMPLETED", (
            f"expected COMPLETED after approval, got {final_status.get('status')}, steps={final_status.get('steps')}"
        )
        step_names = [s["step_name"] for s in final_status["steps"]]
        assert "ai_analysis" in step_names
        assert "execute_action" in step_names
        assert "notify" in step_names
        assert all(s["status"] == "COMPLETED" for s in final_status["steps"])

        # The complete flow must be traceable end-to-end by correlation_id
        # in Audit Service -- this is the payoff of correlation-ID
        # propagation, not just a log-format detail.
        audit_resp = client.get(f"/api/v1/audit/events?execution_id={execution_id}", headers=headers)
        assert audit_resp.status_code == 200, audit_resp.text
        audit_events = audit_resp.json()["items"]
        event_types = {e["event_type"] for e in audit_events}
        assert "workflow.started" in event_types
        assert "approval.requested" in event_types
        assert "approval.completed" in event_types
        assert "workflow.completed" in event_types
        assert all(e["correlation_id"] == correlation_id for e in audit_events)
