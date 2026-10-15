import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get(
    "AUTH_DATABASE_URL",
    "postgresql+asyncpg://postgres:admin@127.0.0.1:5432/Enterprise_AI_Workflow_and_Automation_Platform_FastAPI_NextJS?options=-csearch_path%3Dauth",
)
