"""
Distributed rate limiting via Redis, fixed-window counter keyed by
(bucket, client identity). Fixed-window is simple and good enough for a
portfolio project; the known trade-off (bursts at window boundaries) is
worth naming in an interview -- a sliding-window-log or token-bucket would
smooth that out at the cost of more Redis calls per request.
"""
from __future__ import annotations

import time

import redis.asyncio as redis

from app.core.config import RATE_LIMITS, REDIS_URL
from shared.exceptions import AppError

_redis = redis.from_url(REDIS_URL, decode_responses=True)


class RateLimitExceeded(AppError):
    status_code = 429
    code = "RATE_LIMIT_EXCEEDED"


async def check_rate_limit(bucket: str, identity: str) -> None:
    limit, window = RATE_LIMITS.get(bucket, RATE_LIMITS["default"])
    window_id = int(time.time() // window)
    key = f"ratelimit:{bucket}:{identity}:{window_id}"

    count = await _redis.incr(key)
    if count == 1:
        await _redis.expire(key, window)
    if count > limit:
        raise RateLimitExceeded(f"Rate limit exceeded for {bucket}: {limit} requests per {window}s")
