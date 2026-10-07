import os

DATABASE_URL = os.environ.get(
    "AUTH_DATABASE_URL",
    "postgresql+asyncpg://platform:platform@postgres:5432/platform?options=-csearch_path%3Dauth",
)
