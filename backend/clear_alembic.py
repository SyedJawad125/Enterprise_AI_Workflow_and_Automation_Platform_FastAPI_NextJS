"""
clear_alembic.py
────────────────
Clear stale alembic migration records from the database.
Use this when you get "Can't locate revision" errors.

Usage:
    python clear_alembic.py
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration - use .env values
DB_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
DB_NAME = os.getenv("POSTGRES_DB", "Enterprise_AI_Workflow_and_Automation_Platform_FastAPI_NextJS")

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Drop alembic_version table from auth schema
    cursor.execute('DROP TABLE IF EXISTS auth.alembic_version CASCADE;')
    print("✅ Dropped auth.alembic_version table")

    # Drop alembic_version table from workflow schema (if exists)
    cursor.execute('DROP TABLE IF EXISTS workflow.alembic_version CASCADE;')
    print("✅ Dropped workflow.alembic_version table")

    # Drop alembic_version table from ai schema (if exists)
    cursor.execute('DROP TABLE IF EXISTS ai.alembic_version CASCADE;')
    print("✅ Dropped ai.alembic_version table")

    # Drop alembic_version table from audit schema (if exists)
    cursor.execute('DROP TABLE IF EXISTS audit.alembic_version CASCADE;')
    print("✅ Dropped audit.alembic_version table")

    cursor.close()
    conn.close()

    print("\n✅ All alembic_version tables cleared successfully!")
    print("\nNow you can run: alembic upgrade head")

except Exception as e:
    print(f"❌ Error: {e}")
