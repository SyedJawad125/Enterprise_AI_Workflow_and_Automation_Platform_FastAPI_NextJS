import os

DATABASE_URL = os.environ.get(
    "WORKFLOW_DATABASE_URL",
    "postgresql+asyncpg://postgres:admin@127.0.0.1:5432/Enterprise_AI_Workflow_and_Automation_Platform_FastAPI_NextJS",
)
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")
