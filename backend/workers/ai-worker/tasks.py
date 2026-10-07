"""
Celery worker consuming `ai.processing.queue`. Retries only on transient
failures (network errors, 5xx) using the shared fixed schedule (5s/15s/30s
by default); a 4xx from AI Service fails immediately -- see
shared/messaging/retry_policy.py for why. After the schedule is exhausted,
this reports failure to Workflow Service (so the business workflow moves to
FAILED) AND re-raises, so Celery/RabbitMQ dead-letters the raw message for
operator inspection (see shared/messaging/celery_app.py).
"""
from __future__ import annotations

import os

import httpx

from shared.messaging import make_celery_app, is_retryable, next_retry_delay
from shared.logging.logger import get_logger

logger = get_logger("ai-worker")

app = make_celery_app("ai_worker")

AI_SERVICE_URL = os.environ.get("AI_SERVICE_URL", "http://ai-service:8003")
WORKFLOW_SERVICE_URL = os.environ.get("WORKFLOW_SERVICE_URL", "http://workflow-service:8002")


def _report_result(execution_id: str, correlation_id: str, success: bool, result: dict, error: str | None) -> None:
    with httpx.Client(timeout=10) as client:
        client.post(
            f"{WORKFLOW_SERVICE_URL}/internal/executions/{execution_id}/steps/ai_analysis/complete",
            json={"success": success, "result": result, "error": error},
            headers={"X-Correlation-ID": correlation_id},
        )


@app.task(name="ai_worker.process_ai_step", bind=True, max_retries=None)
def process_ai_step(self, execution_id: str, correlation_id: str, input_text: str,
                     customer_id: str | None, order_id: str | None):
    logger.info("processing ai step", extra={"execution_id": execution_id, "correlation_id": correlation_id,
                                              "retry_count": self.request.retries})
    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(
                f"{AI_SERVICE_URL}/ai/execute",
                json={
                    "execution_id": execution_id, "input_text": input_text,
                    "customer_id": customer_id, "order_id": order_id,
                },
                headers={"X-Correlation-ID": correlation_id},
            )
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPError as exc:
        if not is_retryable(exc):
            logger.warning("non-retryable AI Service error, failing immediately",
                            extra={"execution_id": execution_id, "error": str(exc)})
            _report_result(execution_id, correlation_id, False, {}, f"AI Service rejected the request: {exc}")
            return

        delay = next_retry_delay(self.request.retries)
        if delay is None:
            logger.error("ai step retries exhausted", extra={"execution_id": execution_id, "error": str(exc)})
            _report_result(execution_id, correlation_id, False, {}, f"AI Service call failed after retries: {exc}")
            raise  # let Celery/RabbitMQ dead-letter the raw message (see celery_app.py)

        logger.info("retrying ai step", extra={"execution_id": execution_id, "delay_seconds": delay,
                                                "retry_count": self.request.retries + 1})
        raise self.retry(exc=exc, countdown=delay)

    _report_result(execution_id, correlation_id, True, data, None)
