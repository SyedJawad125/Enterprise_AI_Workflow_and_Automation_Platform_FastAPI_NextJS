"""
Celery worker consuming `notification.queue`. A failed notification must
never lose or reverse a completed business operation (spec section 14 --
"the workflow should not unnecessarily lose the completed business
operation"): by the time this task runs, any side-effecting action (refund)
has already happened. Retries here only affect whether the customer gets
told, not whether the refund occurred, so this is the least risky worker to
retry aggressively.
"""
from __future__ import annotations

import os

import httpx

from shared.messaging import make_celery_app, is_retryable, next_retry_delay
from shared.logging.logger import get_logger

logger = get_logger("notification-worker")

app = make_celery_app("notification_worker")

NOTIFICATION_SERVICE_URL = os.environ.get("NOTIFICATION_SERVICE_URL", "http://notification-service:8005")
WORKFLOW_SERVICE_URL = os.environ.get("WORKFLOW_SERVICE_URL", "http://workflow-service:8002")


def _report_result(execution_id: str, correlation_id: str, success: bool, result: dict, error: str | None) -> None:
    with httpx.Client(timeout=10) as client:
        client.post(
            f"{WORKFLOW_SERVICE_URL}/internal/executions/{execution_id}/steps/notify/complete",
            json={"success": success, "result": result, "error": error},
            headers={"X-Correlation-ID": correlation_id},
        )


@app.task(name="notification_worker.send_notification_step", bind=True, max_retries=None)
def send_notification_step(self, execution_id: str, correlation_id: str, channel: str, recipient: str, message: str):
    logger.info("sending notification", extra={"execution_id": execution_id, "channel": channel,
                                                 "retry_count": self.request.retries})
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.post(
                f"{NOTIFICATION_SERVICE_URL}/notifications/send",
                json={"channel": channel, "recipient": recipient, "message": message, "execution_id": execution_id},
                headers={"X-Correlation-ID": correlation_id},
            )
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPError as exc:
        if not is_retryable(exc):
            _report_result(execution_id, correlation_id, False, {}, f"Notification Service rejected the request: {exc}")
            return

        delay = next_retry_delay(self.request.retries)
        if delay is None:
            logger.error("notification retries exhausted", extra={"execution_id": execution_id, "error": str(exc)})
            _report_result(execution_id, correlation_id, False, {}, f"Notification Service call failed after retries: {exc}")
            raise  # dead-lettered for operator inspection (see celery_app.py)

        logger.info("retrying notification", extra={"execution_id": execution_id, "delay_seconds": delay,
                                                      "retry_count": self.request.retries + 1})
        raise self.retry(exc=exc, countdown=delay)

    _report_result(execution_id, correlation_id, True, data, None)
