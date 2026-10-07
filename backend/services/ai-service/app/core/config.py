import os

DATABASE_URL = os.environ.get(
    "AI_DATABASE_URL",
    "postgresql+asyncpg://platform:platform@postgres:5432/platform?options=-csearch_path%3Dai",
)
INTEGRATION_SERVICE_URL = os.environ.get("INTEGRATION_SERVICE_URL", "http://integration-service:8004")
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "mock")  # mock | openai | groq | gemini
LLM_MODEL = os.environ.get("LLM_MODEL", "mock-classifier-v1")
