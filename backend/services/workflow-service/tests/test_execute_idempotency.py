"""
Verifies POST /workflows/{id}/execute honors Idempotency-Key: a repeated
request with the same key returns the existing execution instead of
starting a second one (spec's idempotency requirement extended from just
the refund endpoint to the execute endpoint itself).

Dispatch calls and audit publishing are mocked via conftest.py fixtures so
this test never touches a real broker.
"""
import pytest
from httpx import AsyncClient, ASGITransport

import app.main as main_module


@pytest.mark.asyncio
async def test_repeated_execute_with_same_idempotency_key_does_not_duplicate(test_app, dispatch_recorder):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post("/workflows", json={"name": "Customer Request Workflow"})
        workflow_id = create_resp.json()["id"]

        body = {"input_text": "refund please", "customer_id": "cust_1001", "order_id": "ord_5001"}
        headers = {"Idempotency-Key": "client-key-abc"}

        first = await client.post(f"/workflows/{workflow_id}/execute", json=body, headers=headers)
        second = await client.post(f"/workflows/{workflow_id}/execute", json=body, headers=headers)

    assert first.status_code == 202
    assert second.status_code == 202
    assert first.json()["execution_id"] == second.json()["execution_id"]
    assert first.json()["idempotent_replay"] is False
    assert second.json()["idempotent_replay"] is True

    # Only ONE ai_analysis dispatch should have happened, not two.
    ai_dispatches = [c for c in dispatch_recorder.calls if c[0] == "ai_step"]
    assert len(ai_dispatches) == 1


@pytest.mark.asyncio
async def test_execute_without_idempotency_key_always_creates_new_execution(test_app, dispatch_recorder):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post("/workflows", json={"name": "Customer Request Workflow"})
        workflow_id = create_resp.json()["id"]

        body = {"input_text": "refund please", "customer_id": "cust_1001", "order_id": "ord_5001"}
        first = await client.post(f"/workflows/{workflow_id}/execute", json=body)
        second = await client.post(f"/workflows/{workflow_id}/execute", json=body)

    assert first.json()["execution_id"] != second.json()["execution_id"]
