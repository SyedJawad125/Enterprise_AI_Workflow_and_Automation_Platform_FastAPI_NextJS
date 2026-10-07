"""
Verifies Integration Service's idempotency guarantee: the same
Idempotency-Key must not execute the refund twice (spec section 20).

Run from services/integration-service/: PYTHONPATH=.:../.. pytest tests/ -v
"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_duplicate_refund_request_is_idempotent():
    headers = {"Idempotency-Key": "test-key-123"}
    body = {"order_id": "ord_5001", "amount": 50.0, "reason": "test"}

    first = client.post("/payments/refund", json=body, headers=headers)
    second = client.post("/payments/refund", json=body, headers=headers)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["payment_id"] == second.json()["payment_id"]
    assert second.json()["idempotent_replay"] is True


def test_refund_requires_idempotency_key():
    body = {"order_id": "ord_5002", "amount": 25.0, "reason": "test"}
    resp = client.post("/payments/refund", json=body)
    assert resp.status_code == 422


def test_unknown_order_returns_404():
    headers = {"Idempotency-Key": "test-key-unknown-order"}
    body = {"order_id": "ord_9999", "amount": 10.0, "reason": "test"}
    resp = client.post("/payments/refund", json=body, headers=headers)
    assert resp.status_code == 404
