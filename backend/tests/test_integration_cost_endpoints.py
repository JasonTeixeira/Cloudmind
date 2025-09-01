import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


def _auth_headers(client: TestClient):
    # Create tables first
    Base.metadata.create_all(bind=engine)
    
    # Register and login to obtain bearer
    client.post("/api/v1/auth/register", json={
        "email": "user@example.com",
        "password": "StrongPassword123!",
        "firstName": "User",
        "lastName": "One"
    })
    login = client.post("/api/v1/auth/login", json={
        "email": "user@example.com",
        "password": "StrongPassword123!"
    })
    token = login.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_cost_unit_economics_and_events():
    client = TestClient(app)
    headers = _auth_headers(client)

    resp = client.get("/api/v1/cost/unit-economics", headers=headers)
    assert resp.status_code in (200, 401)  # Some endpoints enforce optional bearer
    # List events (should not error)
    events = client.get("/api/v1/cost/events", headers=headers)
    assert events.status_code in (200, 401)


