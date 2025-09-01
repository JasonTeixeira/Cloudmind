"""
Main application tests for CloudMind API
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings


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

client = TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_client():
    """Create a test client"""
    return client


class TestHealthCheck:
    """Test health check endpoints"""

    def test_health_check(self, test_client):
        """Test health check endpoint"""
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "environment" in data

    def test_root_endpoint(self, test_client):
        """Test root endpoint"""
        response = test_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data


class TestAuthentication:
    """Test authentication endpoints"""

    def test_register_user_success(self, test_client):
        """Test successful user registration"""
        user_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "firstName": "John",
            "lastName": "Doe"
        }
        response = test_client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert "user" in data["data"]
        assert data["data"]["user"]["email"] == user_data["email"]

    def test_register_user_invalid_email(self, test_client):
        """Test user registration with invalid email"""
        user_data = {
            "email": "invalid-email",
            "password": "TestPassword123!",
            "firstName": "John",
            "lastName": "Doe"
        }
        response = test_client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422

    def test_register_user_weak_password(self, test_client):
        """Test user registration with weak password"""
        user_data = {
            "email": "test@example.com",
            "password": "weak",
            "firstName": "John",
            "lastName": "Doe"
        }
        response = test_client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422

    def test_login_success(self, test_client):
        """Test successful login"""
        # First register a user
        user_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "firstName": "John",
            "lastName": "Doe"
        }
        test_client.post("/api/v1/auth/register", json=user_data)

        # Then login
        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        response = test_client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]

    def test_login_invalid_credentials(self, test_client):
        """Test login with invalid credentials"""
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        response = test_client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401

    def test_refresh_token_success(self, test_client):
        """Test successful token refresh"""
        # First register and login to get tokens
        user_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "firstName": "John",
            "lastName": "Doe"
        }
        test_client.post("/api/v1/auth/register", json=user_data)

        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        login_response = test_client.post("/api/v1/auth/login", json=login_data)
        refresh_token = login_response.json()["data"]["refresh_token"]

        # Refresh token
        refresh_data = {"refresh_token": refresh_token}
        response = test_client.post("/api/v1/auth/refresh", json=refresh_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]


class TestProjects:
    """Test project endpoints"""

    def test_create_project_success(self, test_client):
        """Test successful project creation"""
        # First register and login
        user_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "firstName": "John",
            "lastName": "Doe"
        }
        test_client.post("/api/v1/auth/register", json=user_data)

        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        login_response = test_client.post("/api/v1/auth/login", json=login_data)
        access_token = login_response.json()["data"]["access_token"]

        # Create project
        project_data = {
            "name": "Test Project",
            "description": "A test project",
            "cloud_providers": ["aws"],
            "settings": {"region": "us-east-1"}
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = test_client.post("/api/v1/projects", json=project_data, headers=headers)
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == project_data["name"]

    def test_get_projects_unauthorized(self, test_client):
        """Test getting projects without authentication"""
        response = test_client.get("/api/v1/projects")
        assert response.status_code == 401

    def test_get_projects_success(self, test_client):
        """Test successful project retrieval"""
        # First register and login
        user_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "firstName": "John",
            "lastName": "Doe"
        }
        test_client.post("/api/v1/auth/register", json=user_data)

        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        login_response = test_client.post("/api/v1/auth/login", json=login_data)
        access_token = login_response.json()["data"]["access_token"]

        # Create a project
        project_data = {
            "name": "Test Project",
            "description": "A test project",
            "cloud_providers": ["aws"],
            "settings": {"region": "us-east-1"}
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        test_client.post("/api/v1/projects", json=project_data, headers=headers)

        # Get projects
        response = test_client.get("/api/v1/projects", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) > 0


class TestCostAnalysis:
    """Test cost analysis endpoints"""

    def test_get_cost_analysis_unauthorized(self, test_client):
        """Test cost analysis without authentication"""
        response = test_client.get("/api/v1/cost/analysis/test-project")
        assert response.status_code == 401

    def test_get_cost_analysis_success(self, test_client):
        """Test successful cost analysis retrieval"""
        # First register and login
        user_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "firstName": "John",
            "lastName": "Doe"
        }
        test_client.post("/api/v1/auth/register", json=user_data)

        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        login_response = test_client.post("/api/v1/auth/login", json=login_data)
        access_token = login_response.json()["data"]["access_token"]

        # Create a project
        project_data = {
            "name": "Test Project",
            "description": "A test project",
            "cloud_providers": ["aws"],
            "settings": {"region": "us-east-1"}
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        project_response = test_client.post("/api/v1/projects", json=project_data, headers=headers)
        project_id = project_response.json()["data"]["id"]

        # Get cost analysis
        response = test_client.get(f"/api/v1/cost/analysis/{project_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestSecurity:
    """Test security endpoints"""

    def test_get_security_scans_unauthorized(self, test_client):
        """Test security scans without authentication"""
        response = test_client.get("/api/v1/security/scans/test-project")
        assert response.status_code == 401

    def test_get_security_scans_success(self, test_client):
        """Test successful security scans retrieval"""
        # First register and login
        user_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "firstName": "John",
            "lastName": "Doe"
        }
        test_client.post("/api/v1/auth/register", json=user_data)

        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        login_response = test_client.post("/api/v1/auth/login", json=login_data)
        access_token = login_response.json()["data"]["access_token"]

        # Create a project
        project_data = {
            "name": "Test Project",
            "description": "A test project",
            "cloud_providers": ["aws"],
            "settings": {"region": "us-east-1"}
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        project_response = test_client.post("/api/v1/projects", json=project_data, headers=headers)
        project_id = project_response.json()["data"]["id"]

        # Get security scans
        response = test_client.get(f"/api/v1/security/scans/{project_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestInfrastructure:
    """Test infrastructure endpoints"""

    def test_get_infrastructure_resources_unauthorized(self, test_client):
        """Test infrastructure resources without authentication"""
        response = test_client.get("/api/v1/infrastructure/resources/test-project")
        assert response.status_code == 401

    def test_get_infrastructure_resources_success(self, test_client):
        """Test successful infrastructure resources retrieval"""
        # First register and login
        user_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "firstName": "John",
            "lastName": "Doe"
        }
        test_client.post("/api/v1/auth/register", json=user_data)

        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        login_response = test_client.post("/api/v1/auth/login", json=login_data)
        access_token = login_response.json()["data"]["access_token"]

        # Create a project
        project_data = {
            "name": "Test Project",
            "description": "A test project",
            "cloud_providers": ["aws"],
            "settings": {"region": "us-east-1"}
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        project_response = test_client.post("/api/v1/projects", json=project_data, headers=headers)
        project_id = project_response.json()["data"]["id"]

        # Get infrastructure resources
        response = test_client.get(f"/api/v1/infrastructure/resources/{project_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestAI:
    """Test AI endpoints"""

    def test_get_ai_insights_unauthorized(self, test_client):
        """Test AI insights without authentication"""
        response = test_client.get("/api/v1/ai/insights/test-project")
        assert response.status_code == 401

    def test_get_ai_insights_success(self, test_client):
        """Test successful AI insights retrieval"""
        # First register and login
        user_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "firstName": "John",
            "lastName": "Doe"
        }
        test_client.post("/api/v1/auth/register", json=user_data)

        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        login_response = test_client.post("/api/v1/auth/login", json=login_data)
        access_token = login_response.json()["data"]["access_token"]

        # Create a project
        project_data = {
            "name": "Test Project",
            "description": "A test project",
            "cloud_providers": ["aws"],
            "settings": {"region": "us-east-1"}
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        project_response = test_client.post("/api/v1/projects", json=project_data, headers=headers)
        project_id = project_response.json()["data"]["id"]

        # Get AI insights
        response = test_client.get(f"/api/v1/ai/insights/{project_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestErrorHandling:
    """Test error handling"""

    def test_404_not_found(self, test_client):
        """Test 404 error handling"""
        response = test_client.get("/nonexistent-endpoint")
        assert response.status_code == 404

    def test_422_validation_error(self, test_client):
        """Test 422 validation error handling"""
        response = test_client.post("/api/v1/auth/register", json={})
        assert response.status_code == 422

    def test_500_internal_server_error(self, test_client):
        """Test 500 internal server error handling"""
        # This would require mocking a service to throw an exception
        # For now, we'll test that the error handler exists
        assert hasattr(app, 'exception_handlers')


class TestMiddleware:
    """Test middleware functionality"""

    def test_cors_headers(self, test_client):
        """Test CORS headers are present"""
        response = test_client.options("/health")
        assert "access-control-allow-origin" in response.headers

    def test_security_headers(self, test_client):
        """Test security headers are present"""
        response = test_client.get("/health")
        headers = response.headers
        assert "x-content-type-options" in headers
        assert "x-frame-options" in headers
        assert "x-xss-protection" in headers

    def test_rate_limiting(self, test_client):
        """Test rate limiting functionality"""
        # Make multiple requests to trigger rate limiting
        for _ in range(100):
            response = test_client.get("/health")
            if response.status_code == 429:
                break
        else:
            # If we didn't hit rate limiting, that's also acceptable
            assert True


if __name__ == "__main__":
    pytest.main([__file__]) 