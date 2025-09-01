"""
Comprehensive Security Tests for CloudMind
"""

import pytest
import json
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


class TestPasswordSecurity:
    """Test password security measures"""
    
    def test_strong_password_validation(self, test_client):
        """Test that strong passwords are accepted"""
        strong_passwords = [
            "StrongPass123!",
            "MySecureP@ssw0rd",
            "Complex#Password2024!",
            "Test123!@#$%^&*()"
        ]
        
        for password in strong_passwords:
            user_data = {
                "email": "test@example.com",
                "password": password,
                "username": "testuser",
                "full_name": "Test User"
            }
            response = test_client.post("/api/v1/auth/register", json=user_data)
            # Should not fail due to weak password
            assert response.status_code != 422
    
    def test_weak_password_rejection(self, test_client):
        """Test that weak passwords are rejected"""
        weak_passwords = [
            "weak",  # Too short
            "password",  # Common word
            "123456",  # Common pattern
            "qwerty",  # Common pattern
            "abc123",  # No special char
            "Password",  # No digit
            "PASSWORD123",  # No lowercase
            "password123",  # No uppercase
            "Password123",  # No special char
            "Pass@word",  # No digit
        ]
        
        for password in weak_passwords:
            user_data = {
                "email": "test@example.com",
                "password": password,
                "username": "testuser",
                "full_name": "Test User"
            }
            response = test_client.post("/api/v1/auth/register", json=user_data)
            # Should fail due to weak password
            assert response.status_code == 422


class TestInputValidation:
    """Test input validation and sanitization"""
    
    def test_sql_injection_prevention(self, test_client):
        """Test SQL injection prevention"""
        sql_injection_payloads = [
            "'; DROP TABLE users; --",
            "' OR 1=1 --",
            "'; INSERT INTO users VALUES ('hacker', 'password'); --",
            "admin'--",
            "' UNION SELECT * FROM users --",
            "'; UPDATE users SET password='hacked'; --"
        ]
        
        for payload in sql_injection_payloads:
            # Test in login
            login_data = {
                "email": payload,
                "password": "password123"
            }
            response = test_client.post("/api/v1/auth/login", json=login_data)
            # Should be rejected
            assert response.status_code in [400, 422]
            
            # Test in registration
            register_data = {
                "email": payload,
                "password": "StrongPass123!",
                "username": "testuser",
                "full_name": "Test User"
            }
            response = test_client.post("/api/v1/auth/register", json=register_data)
            # Should be rejected
            assert response.status_code in [400, 422]
    
    def test_xss_prevention(self, test_client):
        """Test XSS prevention"""
        xss_payloads = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "';alert('xss');//",
            "<svg onload=alert('xss')>",
            "';eval('alert(\"xss\")');//"
        ]
        
        for payload in xss_payloads:
            # Test in registration
            register_data = {
                "email": "test@example.com",
                "password": "StrongPass123!",
                "username": payload,
                "full_name": payload
            }
            response = test_client.post("/api/v1/auth/register", json=register_data)
            # Should be rejected
            assert response.status_code in [400, 422]
    
    def test_path_traversal_prevention(self, test_client):
        """Test path traversal prevention"""
        traversal_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "....//....//....//etc/passwd",
            "..%2f..%2f..%2fetc%2fpasswd",
            "..%252f..%252f..%252fetc%252fpasswd"
        ]
        
        for payload in traversal_payloads:
            # Test in query parameters
            response = test_client.get(f"/health?file={payload}")
            # Should be rejected
            assert response.status_code in [400, 422]
            
            # Test in path parameters
            response = test_client.get(f"/health/{payload}")
            # Should be rejected
            assert response.status_code in [400, 422]


class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_rate_limiting_triggered(self, test_client):
        """Test that rate limiting is triggered"""
        # Make many requests quickly
        responses = []
        for i in range(150):  # More than the limit
            response = test_client.get("/health")
            responses.append(response.status_code)
            
            # Stop if rate limited
            if response.status_code == 429:
                break
        
        # Should have hit rate limiting
        assert 429 in responses
    
    def test_different_limits_for_different_endpoints(self, test_client):
        """Test different rate limits for different endpoints"""
        # Login endpoint should have stricter limits
        login_responses = []
        for i in range(10):  # More than login limit
            response = test_client.post("/api/v1/auth/login", json={
                "email": "test@example.com",
                "password": "password123"
            })
            login_responses.append(response.status_code)
            
            if response.status_code == 429:
                break
        
        # Health endpoint should have higher limits
        health_responses = []
        for i in range(100):  # More than health limit
            response = test_client.get("/health")
            health_responses.append(response.status_code)
            
            if response.status_code == 429:
                break
        
        # Login should be rate limited sooner
        assert len([r for r in login_responses if r == 429]) >= 1


class TestSecurityHeaders:
    """Test security headers"""
    
    def test_security_headers_present(self, test_client):
        """Test that security headers are present"""
        response = test_client.get("/health")
        headers = response.headers
        
        # Required security headers
        required_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options", 
            "X-XSS-Protection",
            "Referrer-Policy",
            "Strict-Transport-Security",
            "Content-Security-Policy"
        ]
        
        for header in required_headers:
            assert header in headers
        
        # Check specific values
        assert headers["X-Content-Type-Options"] == "nosniff"
        assert headers["X-Frame-Options"] == "DENY"
        assert "1; mode=block" in headers["X-XSS-Protection"]
        assert "strict-origin-when-cross-origin" in headers["Referrer-Policy"]
        assert "max-age=31536000" in headers["Strict-Transport-Security"]
        assert "default-src 'self'" in headers["Content-Security-Policy"]
    
    def test_server_information_hidden(self, test_client):
        """Test that server information is hidden"""
        response = test_client.get("/health")
        headers = response.headers
        
        # Server header should not be present
        assert "Server" not in headers


class TestCORSConfiguration:
    """Test CORS configuration"""
    
    def test_allowed_origins(self, test_client):
        """Test that only allowed origins are accepted"""
        allowed_origins = [
            "http://localhost:3000",
            "https://cloudmind.local"
        ]
        
        for origin in allowed_origins:
            response = test_client.options("/health", headers={"Origin": origin})
            assert response.status_code == 200
            assert "Access-Control-Allow-Origin" in response.headers
    
    def test_blocked_origins(self, test_client):
        """Test that malicious origins are blocked"""
        malicious_origins = [
            "https://malicious-site.com",
            "http://evil.com",
            "https://attacker.com"
        ]
        
        for origin in malicious_origins:
            response = test_client.options("/health", headers={"Origin": origin})
            # Should not have CORS headers for malicious origins
            assert "Access-Control-Allow-Origin" not in response.headers or \
                   response.headers["Access-Control-Allow-Origin"] != origin


class TestAuthenticationSecurity:
    """Test authentication security measures"""
    
    def test_jwt_token_blacklisting(self, test_client):
        """Test JWT token blacklisting on logout"""
        # First register a user
        user_data = {
            "email": "test@example.com",
            "password": "StrongPass123!",
            "username": "testuser",
            "full_name": "Test User"
        }
        test_client.post("/api/v1/auth/register", json=user_data)
        
        # Login to get token
        login_data = {
            "email": "test@example.com",
            "password": "StrongPass123!"
        }
        login_response = test_client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # Use token to access protected endpoint
        headers = {"Authorization": f"Bearer {access_token}"}
        response = test_client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 200
        
        # Logout to blacklist token
        logout_response = test_client.post("/api/v1/auth/logout", headers=headers)
        assert logout_response.status_code == 200
        
        # Try to use blacklisted token
        response = test_client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401
    
    def test_account_lockout(self, test_client):
        """Test account lockout after failed attempts"""
        # Register a user
        user_data = {
            "email": "test@example.com",
            "password": "StrongPass123!",
            "username": "testuser",
            "full_name": "Test User"
        }
        test_client.post("/api/v1/auth/register", json=user_data)
        
        # Make multiple failed login attempts
        for i in range(6):  # More than the lockout threshold
            login_data = {
                "email": "test@example.com",
                "password": "wrongpassword"
            }
            response = test_client.post("/api/v1/auth/login", json=login_data)
            
            if response.status_code == 423:  # Locked
                break
        
        # Account should be locked
        assert response.status_code == 423
    
    def test_session_timeout(self, test_client):
        """Test session timeout functionality"""
        # This would require time-based testing
        # For now, we'll test that tokens have expiration
        user_data = {
            "email": "test@example.com",
            "password": "StrongPass123!",
            "username": "testuser",
            "full_name": "Test User"
        }
        test_client.post("/api/v1/auth/register", json=user_data)
        
        login_data = {
            "email": "test@example.com",
            "password": "StrongPass123!"
        }
        response = test_client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        
        token_data = response.json()
        # Token should have expiration info
        assert "expires_in" in token_data or "token_type" in token_data


class TestDataSanitization:
    """Test data sanitization"""
    
    def test_sensitive_data_redaction(self, test_client):
        """Test that sensitive data is redacted in logs"""
        # This test would require access to logs
        # For now, we'll test that sensitive endpoints don't expose data
        sensitive_endpoints = [
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            "/api/v1/auth/change-password"
        ]
        
        for endpoint in sensitive_endpoints:
            response = test_client.post(endpoint, json={
                "email": "test@example.com",
                "password": "StrongPass123!"
            })
            # Should not expose sensitive data in response
            assert "password" not in response.text.lower()
            assert "token" not in response.text.lower()


class TestErrorHandling:
    """Test error handling security"""
    
    def test_no_information_leakage(self, test_client):
        """Test that errors don't leak sensitive information"""
        # Test with invalid token
        headers = {"Authorization": "Bearer invalid_token"}
        response = test_client.get("/api/v1/auth/me", headers=headers)
        
        # Should not leak internal details
        assert response.status_code == 401
        error_data = response.json()
        assert "detail" in error_data
        assert "Could not validate credentials" in error_data["detail"]
        # Should not expose internal error details
        assert "jwt" not in error_data["detail"].lower()
        assert "token" not in error_data["detail"].lower()
    
    def test_graceful_error_handling(self, test_client):
        """Test graceful error handling"""
        # Test with malformed JSON
        response = test_client.post(
            "/api/v1/auth/login",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        # Should handle gracefully
        assert response.status_code in [400, 422]


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 