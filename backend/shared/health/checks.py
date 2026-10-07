"""
Cheap, bounded dependency checks for /ready endpoints.

Health (/health) means "the process is alive" -- no dependency calls, ever.
Readiness (/ready) means "this process can currently serve requests" -- a
handful of fast checks with tight timeouts, so a readiness probe hitting
every few seconds never becomes expensive load on its own dependencies.
Every check here has an explicit timeout and never raises past its own
try/except -- a broken dependency shows up as "unhealthy" in the response,
not as a 500 from the readiness endpoint itself.
"""
from __future__ import annotations

import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine


async def check_postgres(engine: AsyncEngine, timeout: float = 2.0) -> str:
    try:
        async def _ping():
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        await asyncio.wait_for(_ping(), timeout=timeout)
        return "healthy"
    except Exception:  # noqa: BLE001
        return "unhealthy"


async def check_redis(redis_url: str, timeout: float = 2.0) -> str:
    try:
        import redis.asyncio as redis
        client = redis.from_url(redis_url, socket_connect_timeout=timeout)
        await asyncio.wait_for(client.ping(), timeout=timeout)
        await client.aclose()
        return "healthy"
    except Exception:  # noqa: BLE001
        return "unhealthy"


async def check_rabbitmq(rabbitmq_url: str, timeout: float = 2.0) -> str:
    try:
        import aio_pika
        connection = await asyncio.wait_for(aio_pika.connect_robust(rabbitmq_url, timeout=timeout), timeout=timeout)
        await connection.close()
        return "healthy"
    except Exception:  # noqa: BLE001
        return "unhealthy"
