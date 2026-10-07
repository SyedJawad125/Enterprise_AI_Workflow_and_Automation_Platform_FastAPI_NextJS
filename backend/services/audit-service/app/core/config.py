import os

DATABASE_URL = os.environ.get(
    "AUDIT_DATABASE_URL",
    "postgresql+asyncpg://platform:platform@postgres:5432/platform?options=-csearch_path%3Daudit",
)
RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")
