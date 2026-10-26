import os

DATABASE_URL = os.environ.get(
    "AUDIT_DATABASE_URL",
    "postgresql+asyncpg://postgres:admin@127.0.0.1:5432/Enterprise_AI_Workflow_and_Automation_Platform_FastAPI_NextJS",
)
RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")
