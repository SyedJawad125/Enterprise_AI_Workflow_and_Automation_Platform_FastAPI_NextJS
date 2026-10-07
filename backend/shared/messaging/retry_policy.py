"""
Shared retry classification + schedule for every Celery worker.

Two things live here on purpose, together:

1. `is_retryable(exc)` -- the answer to your spec's "don't blindly retry"
   requirement. A 4xx from a downstream service (404 order not found, 422
   bad request) will NEVER succeed on retry -- retrying it just burns time
   and, for a side-effecting call like a refund, adds needless risk. Only
   network-level failures (timeouts, connection errors) and 5xx responses
   are retried. A 4xx fails the step immediately, one attempt, no retry.

2. `RETRY_DELAYS` -- your suggested fixed schedule (5s, 15s, 30s) rather
   than Celery's default exponential backoff, so the retry timing matches
   what you specified and is easy to reason about/demo. Configurable via
   env (comma-separated seconds) without touching worker code.
"""
from __future__ import annotations

import os

import httpx

_raw = os.environ.get("RETRY_DELAYS_SECONDS", "5,15,30")
RETRY_DELAYS: list[int] = [int(x.strip()) for x in _raw.split(",") if x.strip()]
MAX_RETRIES = len(RETRY_DELAYS)


def is_retryable(exc: Exception) -> bool:
    """True for network-level failures and 5xx responses; False for 4xx
    (client errors that retrying will never fix) and anything else."""
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code >= 500
    if isinstance(exc, httpx.HTTPError):
        # ConnectError, ConnectTimeout, ReadTimeout, etc. -- transient by nature.
        return True
    return False


def next_retry_delay(retry_count: int) -> int | None:
    """retry_count is 0-indexed (Celery's `self.request.retries`). Returns
    the delay in seconds before the next attempt, or None if retries are
    exhausted and the task should fail terminally instead."""
    if retry_count >= MAX_RETRIES:
        return None
    return RETRY_DELAYS[retry_count]
