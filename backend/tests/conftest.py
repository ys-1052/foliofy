"""Test fixtures and configuration."""

from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.dependencies.auth import get_current_user
from app.main import app
from app.models import User

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Test user ID (same as the old HARDCODED_USER_ID)
TEST_USER_ID = UUID("a12336b9-edcc-43fc-b564-ca1fe6897ebc")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with test database."""

    def override_get_db():
        try:
            yield db
        finally:
            pass

    def override_get_current_user():
        """Mock authentication - return test user"""
        return {
            "sub": str(TEST_USER_ID),
            "email": "test@example.com",
            "email_verified": True,
        }

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db):
    """Create a test user."""
    user = User(id=TEST_USER_ID, email="test@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
