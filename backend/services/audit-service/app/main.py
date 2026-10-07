import asyncio

from fastapi import Depends, FastAPI, Query
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.exceptions import install_exception_handlers
from shared.health import check_postgres, check_rabbitmq
from shared.logging.logger import RequestContextMiddleware, get_logger

from app.consumer import run_consumer
from app.core.config import RABBITMQ_URL
from app.db import get_db, init_models, engine
from app.models import AuditEvent

logger = get_logger("audit-service")

app = FastAPI(title="Audit Service")
app.add_middleware(RequestContextMiddleware)
install_exception_handlers(app)


@app.on_event("startup")
async def on_startup():
    await init_models()
    asyncio.create_task(run_consumer())
    logger.info("audit-service started, consumer task scheduled")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "audit-service"}


@app.get("/ready")
async def ready():
    postgres_status = await check_postgres(engine)
    rabbitmq_status = await check_rabbitmq(RABBITMQ_URL)
    deps = {"postgres": postgres_status, "rabbitmq": rabbitmq_status}
    status = "ready" if all(v == "healthy" for v in deps.values()) else "not_ready"
    return JSONResponse(
        status_code=200 if status == "ready" else 503,
        content={"status": status, "service": "audit-service", "dependencies": deps},
    )


@app.get("/audit/events")
async def list_events(
    workflow_id: str | None = None,
    execution_id: str | None = None,
    event_type: str | None = None,
    page: int = 1,
    page_size: int = Query(default=50, le=200),
    db: AsyncSession = Depends(get_db),
):
    """Requires audit:read permission -- enforced by the Gateway before this
    is ever reached, and re-checked here in a full build via a shared
    dependency that inspects the forwarded X-User-Permissions header."""
    stmt = select(AuditEvent).order_by(AuditEvent.received_at.desc())
    if workflow_id:
        stmt = stmt.where(AuditEvent.workflow_id == workflow_id)
    if execution_id:
        stmt = stmt.where(AuditEvent.execution_id == execution_id)
    if event_type:
        stmt = stmt.where(AuditEvent.event_type == event_type)
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)

    rows = (await db.scalars(stmt)).all()
    return {
        "page": page,
        "page_size": page_size,
        "items": [
            {
                "event_id": r.event_id,
                "event_type": r.event_type,
                "correlation_id": r.correlation_id,
                "workflow_id": r.workflow_id,
                "execution_id": r.execution_id,
                "payload": r.payload,
                "received_at": r.received_at.isoformat(),
            }
            for r in rows
        ],
    }
