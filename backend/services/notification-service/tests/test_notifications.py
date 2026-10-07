"""Notification Service: mock delivery + retrieval, per spec section 29."""
from fastapi.testclient import TestClient

from app.main import app, SENT_NOTIFICATIONS

client = TestClient(app)


def setup_function():
    SENT_NOTIFICATIONS.clear()


def test_send_email_notification_is_recorded():
    resp = client.post("/notifications/send", json={
        "channel": "email", "recipient": "cust_1001", "message": "Your refund was processed.",
        "execution_id": "exec-1",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "delivered_mock"
    assert data["channel"] == "email"


def test_invalid_channel_is_rejected():
    resp = client.post("/notifications/send", json={
        "channel": "carrier_pigeon", "recipient": "cust_1001", "message": "hi",
    })
    assert resp.status_code == 422


def test_list_notifications_returns_sent_items():
    client.post("/notifications/send", json={"channel": "in_app", "recipient": "approver-queue", "message": "Approval needed"})
    client.post("/notifications/send", json={"channel": "email", "recipient": "cust_1002", "message": "Update"})
    resp = client.get("/notifications")
    assert resp.status_code == 200
    assert len(resp.json()) == 2
