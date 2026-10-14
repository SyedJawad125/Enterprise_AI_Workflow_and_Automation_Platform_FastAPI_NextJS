# # init_db.py
# from app.database import Base, engine
# from app import models # ensure all models are imported
# # from app.models.rank import Rank
# # Create all tables
# Base.metadata.create_all(bind=engine)
# print("✅ Database tables created successfully.")




"""
init_db.py
───────────
Initialize database tables for all services.
Creates tables for auth-service, workflow-service, ai-service, and audit-service.

Usage:
    python init_db.py
"""
import asyncio
import sys
import os

# Windows fix
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def init_auth_db():
    """Initialize auth-service database tables"""
    print('🔧 Initializing auth-service database...')
    from services.auth_service.app.db import engine, Base
    from services.auth_service.app import models  # Import all models

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('✅ Auth-service tables created!')


async def init_workflow_db():
    """Initialize workflow-service database tables"""
    print('🔧 Initializing workflow-service database...')
    from services.workflow_service.app.db import engine, Base
    from services.workflow_service.app import models  # Import all models

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('✅ Workflow-service tables created!')


async def init_ai_db():
    """Initialize ai-service database tables"""
    print('🔧 Initializing ai-service database...')
    from services.ai_service.app.db import engine, Base
    from services.ai_service.app import models  # Import all models

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('✅ AI-service tables created!')


async def init_audit_db():
    """Initialize audit-service database tables"""
    print('🔧 Initializing audit-service database...')
    from services.audit_service.app.db import engine, Base
    from services.audit_service.app import models  # Import all models

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('✅ Audit-service tables created!')


async def init_db():
    """Initialize all service databases"""
    print("=" * 60)
    print("🚀 Initializing Database Tables")
    print("=" * 60)
    print()

    try:
        await init_auth_db()
        await init_workflow_db()
        await init_ai_db()
        await init_audit_db()

        print("\n" + "=" * 60)
        print("✅ All database tables created successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Run: python add_permissions.py")
        print("  2. Run: python populate.py")
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        raise


if __name__ == '__main__':
    asyncio.run(init_db())