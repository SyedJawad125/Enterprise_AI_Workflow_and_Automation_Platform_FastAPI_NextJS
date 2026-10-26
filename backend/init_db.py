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
    print('Initializing auth-service database...')
    import sys
    import os
    auth_service_path = os.path.join(os.path.dirname(__file__), 'services', 'auth-service')
    if auth_service_path not in sys.path:
        sys.path.insert(0, auth_service_path)

    from app.db import engine, Base
    from app import models  # Import all models

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Auth-service tables created!')


async def init_workflow_db():
    """Initialize workflow-service database tables"""
    print('Initializing workflow-service database...')
    import sys
    import os
    workflow_service_path = os.path.join(os.path.dirname(__file__), 'services', 'workflow-service')
    if workflow_service_path not in sys.path:
        sys.path.insert(0, workflow_service_path)

    from app.db import engine, Base
    from app import models  # Import all models

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Workflow-service tables created!')


async def init_ai_db():
    """Initialize ai-service database tables"""
    print('Initializing ai-service database...')
    import sys
    import os
    ai_service_path = os.path.join(os.path.dirname(__file__), 'services', 'ai-service')
    if ai_service_path not in sys.path:
        sys.path.insert(0, ai_service_path)

    from app.db import engine, Base
    from app import models  # Import all models

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('AI-service tables created!')


async def init_audit_db():
    """Initialize audit-service database tables"""
    print('Initializing audit-service database...')
    import sys
    import os
    audit_service_path = os.path.join(os.path.dirname(__file__), 'services', 'audit-service')
    if audit_service_path not in sys.path:
        sys.path.insert(0, audit_service_path)

    from app.db import engine, Base
    from app import models  # Import all models

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Audit-service tables created!')


async def init_db():
    """Initialize all service databases"""
    print("=" * 60)
    print("Initializing Database Tables")
    print("=" * 60)
    print()

    try:
        await init_auth_db()
        await init_workflow_db()
        await init_ai_db()
        await init_audit_db()

        print("\n" + "=" * 60)
        print("All database tables created successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Run: python add_permissions.py")
        print("  2. Run: python populate.py")
    except Exception as e:
        print(f"\nError initializing database: {e}")
        raise


if __name__ == '__main__':
    asyncio.run(init_db())