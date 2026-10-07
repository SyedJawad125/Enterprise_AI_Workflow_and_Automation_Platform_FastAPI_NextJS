"""
Auth Service tests run against SQLite in-memory instead of Postgres, so
`pytest` works with zero external services. Docker-compose Postgres is still
what runs in production/dev -- this override exists only for fast, hermetic
unit/API tests (a very common real-world pattern worth naming in an
interview: "the schema is portable because we only use SQLAlchemy Core
types, not Postgres-only features, in this service's models... except the
UUID column type, which we special-case for the SQLite test engine below").
"""
import asyncio
import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base
import app.db as db_module
import app.main as main_module


@pytest_asyncio.fixture()
async def test_app():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # SQLite has no schemas -- strip the Postgres-only schema= table arg for tests.
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
