# tests/conftest.py
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db  # Import get_db

TEST_DATABASE_URL = "sqlite:///./test_tasks.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override get_db for the FastAPI app
app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="function")
async def client():
    with TestClient(app) as c:
        yield c


@pytest_asyncio.fixture(scope="function")
async def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)  # Clean up after each test
        Base.metadata.create_all(bind=test_engine)  # Recreate tables
