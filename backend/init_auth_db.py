"""
init_auth_db.py
───────────────
Initialize auth-service database tables.
Creates tables for users, roles, permissions, companies, and refresh tokens.

Usage:
    python init_auth_db.py
"""
import asyncio
import sys
import os

# Windows fix
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def init_db():
    """Initialize auth-service database tables"""
    print("=" * 60)
    print("Initializing Auth-Service Database Tables")
    print("=" * 60)
    print()

    try:
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
        print("\n" + "=" * 60)
        print("Database initialization completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Run: python add_permissions.py")
        print("  2. Run: python populate.py")
        print("  3. Start service: python start.py auth")
    except Exception as e:
        print(f"\nError initializing database: {e}")
        raise


if __name__ == '__main__':
    asyncio.run(init_db())
