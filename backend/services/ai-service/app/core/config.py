import os

DATABASE_URL = os.environ.get(
    "AI_DATABASE_URL",
    "postgresql+asyncpg://postgres:admin@127.0.0.1:5432/Enterprise_AI_Workflow_and_Automation_Platform_FastAPI_NextJS",
)
INTEGRATION_SERVICE_URL = os.environ.get("INTEGRATION_SERVICE_URL", "http://localhost:8004")
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "mock")  # mock | openai | groq | gemini
LLM_MODEL = os.environ.get("LLM_MODEL", "mock-classifier-v1")
