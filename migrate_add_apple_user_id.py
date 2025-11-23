"""
Database Migration: Add apple_user_id to users table
Run this script to add the apple_user_id column to existing production databases
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from db_config import get_database_url

# Load environment variables
load_dotenv()

def migrate():
    """Add apple_user_id column to users table"""
    database_url = get_database_url()
    engine = create_engine(database_url)

    print("=" * 60)
    print("Database Migration: Add apple_user_id to users table")
    print("=" * 60)

    try:
        with engine.connect() as conn:
            # Check if column already exists
            check_column = text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='users' AND column_name='apple_user_id'
            """)

            result = conn.execute(check_column)
            if result.fetchone():
                print("✓ Column 'apple_user_id' already exists in users table")
                return

            # Add the column
            print("\nAdding apple_user_id column to users table...")
            add_column = text("""
                ALTER TABLE users
                ADD COLUMN apple_user_id VARCHAR(255) UNIQUE
            """)
            conn.execute(add_column)
            conn.commit()

            # Add index
            print("Creating index on apple_user_id...")
            add_index = text("""
                CREATE INDEX IF NOT EXISTS idx_users_apple_user_id
                ON users(apple_user_id)
            """)
            conn.execute(add_index)
            conn.commit()

            print("\n✓ Migration completed successfully!")
            print("\nChanges made:")
            print("  - Added 'apple_user_id' column to users table (VARCHAR(255), UNIQUE)")
            print("  - Created index on apple_user_id column")

    except Exception as e:
        print(f"\n✗ Migration failed: {str(e)}")
        print("\nIf the error is about the column already existing, you can ignore this.")
        return False

    return True

if __name__ == '__main__':
    print("\nThis script will add the apple_user_id column to your users table.")
    print("Make sure you have a backup of your database before proceeding.\n")

    response = input("Continue with migration? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        migrate()
    else:
        print("Migration cancelled.")
