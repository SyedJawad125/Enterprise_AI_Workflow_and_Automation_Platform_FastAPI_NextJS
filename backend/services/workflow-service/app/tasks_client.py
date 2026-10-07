"""
Workflow Service dispatches work to Celery workers *by task name* -- it does
NOT import worker code. This keeps the services independently deployable:
Workflow Service only needs to agree with the workers on a task name and
argument shape (the contract), never on shared Python code.
"""
from __future__ import annotations

from shared.messaging import make_celery_app

celery_client = make_celery_app("workflow-service-client")


def dispatch_ai_step(execution_id: str, correlation_id: str, input_text: str, customer_id: str | None, order_id: str | None) -> None:
    celery_client.send_task(
        "ai_worker.process_ai_step",
        kwargs={
            "execution_id": execution_id,
            "correlation_id": correlation_id,
            "input_text": input_text,
            "customer_id": customer_id,
            "order_id": order_id,
        },
        queue="ai.processing.queue",
    )


def dispatch_integration_step(execution_id: str, correlation_id: str, action: str, parameters: dict) -> None:
    celery_client.send_task(
        "integration_worker.process_integration_step",
        kwargs={
            "execution_id": execution_id,
            "correlation_id": correlation_id,
            "action": action,
            "parameters": parameters,
        },
        queue="integration.processing.queue",
    )


def dispatch_notification_step(execution_id: str, correlation_id: str, channel: str, recipient: str, message: str) -> None:
    celery_client.send_task(
        "notification_worker.send_notification_step",
        kwargs={
            "execution_id": execution_id,
            "correlation_id": correlation_id,
            "channel": channel,
            "recipient": recipient,
            "message": message,
        },
        queue="notification.queue",
    )
