"""
test_db.py
──────────
Test PostgreSQL connection and setup for the Enterprise AI Platform.
This script creates the database and enables required extensions.

Usage:
    python test_db.py
"""
import psycopg2
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration - use .env values
DB_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
DB_NAME = os.getenv("POSTGRES_DB", "Enterprise_AI_Workflow_and_Automation_Platform_FastAPI_NextJS")


def test_connection():
    """Test connection to PostgreSQL server"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database="postgres"  # Connect to default DB first
        )
        print("✅ Connected to PostgreSQL successfully!")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        return False


def create_database():
    """Create the platform database if it doesn't exist"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute('SELECT 1 FROM pg_database WHERE datname = %s', (DB_NAME,))
        exists = cursor.fetchone()

        if exists:
            print(f"✅ Database '{DB_NAME}' already exists!")
        else:
            cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
            print(f"✅ Database '{DB_NAME}' created successfully!")

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False


def enable_extensions():
    """Enable required PostgreSQL extensions"""
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

        # Enable pgvector for vector operations
        cursor.execute('CREATE EXTENSION IF NOT EXISTS vector;')
        print("✅ pgvector extension enabled!")

        # Enable uuid-ossp for UUID generation
        cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        print("✅ uuid-ossp extension enabled!")

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error enabling extensions: {e}")
        return False


def create_schemas():
    """Create schemas for each service"""
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

        schemas = ['auth', 'workflow', 'ai', 'audit', 'integration']
        for schema in schemas:
            cursor.execute(f'CREATE SCHEMA IF NOT EXISTS {schema};')
            print(f"✅ Schema '{schema}' created/verified!")

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error creating schemas: {e}")
        return False


def main():
    print("=" * 60)
    print("🔧 Testing PostgreSQL Setup")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  Host: {DB_HOST}")
    print(f"  Port: {DB_PORT}")
    print(f"  User: {DB_USER}")
    print(f"  Database: {DB_NAME}")
    print()

    if not test_connection():
        sys.exit(1)

    if not create_database():
        sys.exit(1)

    if not enable_extensions():
        sys.exit(1)

    if not create_schemas():
        sys.exit(1)

    print("\n" + "=" * 60)
    print("✅ Database setup completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Run: python add_permissions.py")
    print("  2. Run: python populate.py")
    print("  3. Start services: python start.py auth")
    print("  4. Or start all: docker compose up")


if __name__ == "__main__":
    main()
