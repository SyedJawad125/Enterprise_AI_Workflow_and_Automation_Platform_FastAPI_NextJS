"""
Celery worker consuming `integration.processing.queue`. This is where the
retry-safety distinction matters most: a refund is NOT a safe operation to
blindly retry (a network blip after the refund already succeeded server-side
must not cause a second refund). Two protections combine here:

1. `is_retryable()` -- only network errors and 5xx get retried at all; a
   4xx (e.g. unknown order) fails immediately, one attempt.
2. The Idempotency-Key sent to Integration Service is stable across
   retries (derived from execution_id + action, not regenerated per
   attempt), so even a retried request that DID actually apply server-side
   the first time returns the cached result instead of refunding twice.
"""
from __future__ import annotations

import os

import httpx

from shared.messaging import make_celery_app, is_retryable, next_retry_delay
from shared.logging.logger import get_logger

logger = get_logger("integration-worker")

app = make_celery_app("integration_worker")

INTEGRATION_SERVICE_URL = os.environ.get("INTEGRATION_SERVICE_URL", "http://integration-service:8004")
WORKFLOW_SERVICE_URL = os.environ.get("WORKFLOW_SERVICE_URL", "http://workflow-service:8002")


def _report_result(execution_id: str, correlation_id: str, success: bool, result: dict, error: str | None) -> None:
    with httpx.Client(timeout=10) as client:
        client.post(
            f"{WORKFLOW_SERVICE_URL}/internal/executions/{execution_id}/steps/execute_action/complete",
            json={"success": success, "result": result, "error": error},
            headers={"X-Correlation-ID": correlation_id},
        )


@app.task(name="integration_worker.process_integration_step", bind=True, max_retries=None)
def process_integration_step(self, execution_id: str, correlation_id: str, action: str, parameters: dict):
    idempotency_key = f"{execution_id}:{action}"  # stable across retries by design
    logger.info("processing integration step", extra={"execution_id": execution_id, "action": action,
                                                        "retry_count": self.request.retries})
    if action != "refund":
        _report_result(execution_id, correlation_id, False, {}, f"Unknown integration action: {action}")
        return

    try:
        with httpx.Client(timeout=15) as client:
            resp = client.post(
                f"{INTEGRATION_SERVICE_URL}/payments/refund",
                json={"order_id": parameters["order_id"], "amount": parameters["amount"], "reason": parameters.get("reason", "")},
                headers={"Idempotency-Key": idempotency_key, "X-Correlation-ID": correlation_id},
            )
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPError as exc:
        if not is_retryable(exc):
            logger.warning("non-retryable Integration Service error, failing immediately -- no retry on a "
                            "refund that was rejected outright (e.g. unknown order)",
                            extra={"execution_id": execution_id, "error": str(exc)})
            _report_result(execution_id, correlation_id, False, {}, f"Integration Service rejected the request: {exc}")
            return

        delay = next_retry_delay(self.request.retries)
        if delay is None:
            logger.error("integration step retries exhausted", extra={"execution_id": execution_id, "error": str(exc)})
            _report_result(execution_id, correlation_id, False, {}, f"Integration Service call failed after retries: {exc}")
            raise  # dead-lettered for operator inspection (see celery_app.py)

        logger.info("retrying integration step", extra={"execution_id": execution_id, "delay_seconds": delay,
                                                          "retry_count": self.request.retries + 1})
        raise self.retry(exc=exc, countdown=delay)

    _report_result(execution_id, correlation_id, True, data, None)
