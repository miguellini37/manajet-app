"""
Initialize PostgreSQL Database
Creates all tables based on SQLAlchemy models
"""

import sys
from db_config import init_db, USE_POSTGRES, DATABASE_URL

def main():
    """Initialize the database"""
    if not USE_POSTGRES:
        print("❌ ERROR: DATABASE_URL environment variable not set")
        print("\nTo use PostgreSQL, set DATABASE_URL:")
        print("  export DATABASE_URL='postgresql://user:password@host:port/database'")
        print("\nOr continue using JSON file storage (no action needed)")
        sys.exit(1)

    print("🗄️  Initializing PostgreSQL database...")
    print(f"📍 Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'hidden'}")

    try:
        # Import models to register them with Base
        import db_models

        # Create all tables
        init_db()

        print("\n✅ Database initialized successfully!")
        print("\nNext steps:")
        print("1. Run: python migrate_from_json.py  (to migrate existing data)")
        print("2. Or run: python setup_initial_data.py  (for fresh sample data)")

    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
