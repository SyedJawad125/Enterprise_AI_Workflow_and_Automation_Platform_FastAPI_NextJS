"""
Structured JSON logging shared across every service.

Design notes (say this in an interview):
- Every log line is one JSON object -> trivially queryable in any log
  aggregator (ELK, Loki, CloudWatch Insights) without custom parsing rules.
- request_id and correlation_id are stored in contextvars so any code deep
  in a call stack (a repository, a provider, a Celery task) can log with the
  right IDs attached without threading them through every function signature.
- Never log secrets. Callers pass structured `extra` fields; this module
  does not inspect payloads for secrets, so services must not put raw
  passwords/JWTs/API keys into log calls. Documented, not auto-redacted,
  because auto-redaction gives false confidence -- explicit discipline is
  more reliable than a regex that will eventually miss a field name.
"""
from __future__ import annotations

import contextvars
import json
import logging
import os
import sys
import time
import uuid
from typing import Any, Optional

request_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "request_id", default=None
)
correlation_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "correlation_id", default=None
)

SERVICE_NAME = os.environ.get("SERVICE_NAME", "unknown-service")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base: dict[str, Any] = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "service": SERVICE_NAME,
            "environment": ENVIRONMENT,
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "request_id": request_id_var.get(),
            "correlation_id": correlation_id_var.get(),
        }
        # Anything passed via logging's `extra={...}` shows up on the record
        # as plain attributes; merge known extras in without leaking
        # logging-internal attributes.
        reserved = set(vars(logging.makeLogRecord({})).keys()) | {"message", "asctime"}
        for key, value in vars(record).items():
            if key not in reserved and key not in base:
                base[key] = value
        if record.exc_info:
            base["error_type"] = record.exc_info[0].__name__ if record.exc_info[0] else None
            base["error_message"] = str(record.exc_info[1])
        return json.dumps(base, default=str)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
        logger.propagate = False
    return logger


class RequestContextMiddleware:
    """
    ASGI middleware: generates/propagates X-Request-ID and X-Correlation-ID,
    stores them in contextvars for the duration of the request, and logs
    latency + status on the way out.
    """

    def __init__(self, app):
        self.app = app
        self.logger = get_logger(f"{SERVICE_NAME}.http")

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers") or [])
        request_id = headers.get(b"x-request-id", b"").decode() or str(uuid.uuid4())
        correlation_id = headers.get(b"x-correlation-id", b"").decode() or request_id

        req_token = request_id_var.set(request_id)
        corr_token = correlation_id_var.set(correlation_id)
        start = time.time()
        status_holder = {"status": None}

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_holder["status"] = message["status"]
                message["headers"] = list(message.get("headers", [])) + [
                    (b"x-request-id", request_id.encode()),
                    (b"x-correlation-id", correlation_id.encode()),
                ]
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            latency_ms = int((time.time() - start) * 1000)
            self.logger.info(
                "request completed",
                extra={
                    "endpoint": scope.get("path"),
                    "method": scope.get("method"),
                    "status": status_holder["status"],
                    "latency_ms": latency_ms,
                },
            )
            request_id_var.reset(req_token)
            correlation_id_var.reset(corr_token)
