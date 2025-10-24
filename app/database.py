# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL (creates a file named tasks.db in the project root)
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

# Create the engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # This is required for SQLite when multiple threads interact with the DB
    connect_args={"check_same_thread": False}
)

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models
Base = declarative_base()

# Dependency to get DB session


def get_db():
    """Provides a fresh database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
