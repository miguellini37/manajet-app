"""
Database Configuration for PostgreSQL
Handles connection to PostgreSQL database with fallback to JSON
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# Get database URL from environment variable
DATABASE_URL = os.environ.get('DATABASE_URL', '')

# DigitalOcean provides postgres:// but SQLAlchemy needs postgresql://
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Check if we should use PostgreSQL or JSON
USE_POSTGRES = bool(DATABASE_URL)

# Create SQLAlchemy base
Base = declarative_base()

# Database engine and session
engine = None
SessionLocal = None

if USE_POSTGRES:
    # Create engine with connection pooling
    engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,  # Disable pooling for serverless environments
        echo=False,  # Set to True for SQL query logging
        pool_pre_ping=True,  # Verify connections before using
    )

    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get database session"""
    if not USE_POSTGRES or not SessionLocal:
        return None

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database - create all tables"""
    if USE_POSTGRES and engine:
        Base.metadata.create_all(bind=engine)
        print("✅ PostgreSQL database initialized")
    else:
        print("ℹ️  Using JSON file storage (DATABASE_URL not set)")
