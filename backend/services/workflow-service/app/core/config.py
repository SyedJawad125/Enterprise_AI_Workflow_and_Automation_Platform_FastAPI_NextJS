import os

DATABASE_URL = os.environ.get(
    "WORKFLOW_DATABASE_URL",
    "postgresql+asyncpg://platform:platform@postgres:5432/platform?options=-csearch_path%3Dworkflow",
)
REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")
RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672//")
