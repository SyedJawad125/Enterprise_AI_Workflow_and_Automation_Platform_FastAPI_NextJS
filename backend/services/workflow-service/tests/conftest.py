"""
Workflow Service tests run against SQLite in-memory (same pattern as Auth
Service's tests) and monkeypatch the Celery dispatch calls + audit event
publisher, so the state machine (app/orchestrator.py) can be exercised in
complete isolation from RabbitMQ, Celery, and the network.
"""
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base
import app.db as db_module
import app.main as main_module
import app.orchestrator as orchestrator_module
import app.events as events_module


class DispatchRecorder:
    """Records every dispatch_* call instead of hitting a real broker."""
    def __init__(self):
        self.calls = []

    def record(self, name):
        def _fn(**kwargs):
            self.calls.append((name, kwargs))
        return _fn


@pytest_asyncio.fixture()
async def db_session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    for table in Base.metadata.tables.values():
        table.schema = None

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
    async with SessionLocal() as session:
        yield session
    await engine.dispose()


@pytest.fixture()
def dispatch_recorder(monkeypatch):
    recorder = DispatchRecorder()
    # Patch the names as bound *inside orchestrator's own module namespace*
    # (it did `from app.tasks_client import dispatch_ai_step, ...`), not on
    # tasks_client itself -- patching tasks_client wouldn't affect a name
    # orchestrator already imported by value.
    monkeypatch.setattr(orchestrator_module, "dispatch_ai_step", recorder.record("ai_step"))
    monkeypatch.setattr(orchestrator_module, "dispatch_integration_step", recorder.record("integration_step"))
    monkeypatch.setattr(orchestrator_module, "dispatch_notification_step", recorder.record("notification_step"))
    return recorder


@pytest.fixture(autouse=True)
def no_real_audit_publish(monkeypatch):
    async def _noop(envelope):
        return None
    monkeypatch.setattr(events_module, "publish_audit_event", _noop)


@pytest_asyncio.fixture()
async def test_app(dispatch_recorder):
    """A full FastAPI app (HTTP layer, not just direct function calls) wired
    to an isolated SQLite engine -- used for tests that need to exercise
    routing/header-parsing (e.g. Idempotency-Key), not just orchestrator
    logic. dispatch_recorder is requested here too so Celery dispatch is
    mocked for every request made through this app."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    for table in Base.metadata.tables.values():
        table.schema = None

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestSession = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db():
        async with TestSession() as session:
            yield session

    main_module.app.dependency_overrides[db_module.get_db] = override_get_db
    yield main_module.app
    main_module.app.dependency_overrides.clear()
    await engine.dispose()
