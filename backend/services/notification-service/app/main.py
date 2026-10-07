"""
Notification Service: a thin delivery abstraction over email / in-app /
webhook. For this portfolio project every "send" is mocked (logged +
appended to an in-memory feed) so the platform never needs a paid email
provider -- the point being demonstrated is the abstraction and the
decoupling from Workflow Service, not real deliverability.
"""
from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel, Field

from shared.exceptions import install_exception_handlers
from shared.logging.logger import RequestContextMiddleware, get_logger

logger = get_logger("notification-service")

app = FastAPI(title="Notification Service")
app.add_middleware(RequestContextMiddleware)
install_exception_handlers(app)

SENT_NOTIFICATIONS: list[dict] = []


class NotificationRequest(BaseModel):
    channel: str = Field(pattern="^(email|in_app|webhook)$")
    recipient: str
    subject: str = ""
    message: str
    execution_id: str | None = None


@app.get("/health")
async def health():
    return {"status": "ok", "service": "notification-service"}


@app.post("/notifications/send", status_code=201)
async def send(payload: NotificationRequest):
    record = {
        **payload.model_dump(),
        "sent_at": datetime.now(timezone.utc).isoformat(),
        "status": "delivered_mock",
    }
    SENT_NOTIFICATIONS.append(record)
    logger.info(
        "notification sent (mock)",
        extra={"channel": payload.channel, "recipient": payload.recipient, "execution_id": payload.execution_id},
    )
    return record


@app.get("/notifications")
async def list_notifications(limit: int = 50):
    return SENT_NOTIFICATIONS[-limit:]
