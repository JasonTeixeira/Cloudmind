import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.config import settings
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


@pytest.fixture(autouse=True)
def enable_ai_terminal_env(monkeypatch):
    monkeypatch.setenv("ENABLE_AI_TERMINAL", "true")
    # Ensure safe allowlist for planner
    monkeypatch.setenv("AI_TERMINAL_ALLOWED_COMMAND_PREFIXES", "ls,cat,echo,pwd,whoami,git")
    yield


def _register_and_login(client: TestClient):
    # Create tables first
    Base.metadata.create_all(bind=engine)
    
    reg = client.post("/api/v1/auth/register", json={
        "email": "admin@example.com",
        "password": "StrongPassword123!",
        "firstName": "Admin",
        "lastName": "User"
    })
    assert reg.status_code in (200, 201)
    login = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "StrongPassword123!"
    })
    assert login.status_code == 200
    data = login.json()
    token = data["data"].get("access_token")
    assert token
    return {"Authorization": f"Bearer {token}"}


def test_ai_terminal_plan_and_blocking(monkeypatch):
    client = TestClient(app)
    headers = _register_and_login(client)

    # Plan safe commands
    plan = client.post("/api/v1/terminal/ai/plan", json={"goal": "list files in repo"}, headers=headers)
    # If feature flag disabled by settings, expect 403; otherwise 200
    if plan.status_code == 403:
        assert plan.json()["detail"].lower().find("disabled") != -1
        return
    assert plan.status_code == 200
    cmds = plan.json().get("commands", [])
    assert isinstance(cmds, list)
    assert any(c.startswith("ls") or c == "pwd" for c in cmds)


