"""
Alembic environment for Workflow Service. Async-engine aware (asyncpg),
following the standard SQLAlchemy 2.x async-migration pattern: Alembic's
migration runner is itself synchronous, so we bridge it onto the async
engine via `run_sync`.

Why this exists as the reference Alembic setup and not `create_all()`:
`Base.metadata.create_all()` (still used at startup for local-dev speed) is
fine for a fresh database but has no concept of *changing* an existing
schema -- add a column to a model and every existing deployed database
silently never gets it. Alembic gives you `alembic upgrade head` as a
reproducible, versioned schema change, which is why `docker-compose.yml`
runs it before starting the app (see workflow-service's Dockerfile CMD).
"""
from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import DATABASE_URL
from app.db import Base
# Import every model module so Base.metadata is fully populated before
# autogenerate compares it against the live database.
from app import models  # noqa: F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema="workflow",
        include_schemas=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def _do_run_migrations(connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table_schema="workflow",
        include_schemas=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = create_async_engine(DATABASE_URL)
    async with connectable.connect() as connection:
        await connection.run_sync(_do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
