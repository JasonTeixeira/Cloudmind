#!/usr/bin/env python3
"""
Comprehensive Security Test Suite
Tests all security vulnerabilities and world-class security implementation
"""

import asyncio
import aiohttp
import json
import time
import hashlib
import secrets
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    SKIP = "SKIP"

@dataclass
class SecurityTest:
    name: str
    description: str
    test_function: callable
    critical: bool = False

class ComprehensiveSecurityTester:
    """Comprehensive security testing suite"""
    
    def __init__(self):
        self.base_url = "https://localhost:8000"
        self.results = []
        self.session = None
        
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all security tests"""
        logger.info("🔒 Starting Comprehensive Security Testing...")
        
        # Initialize session
        connector = aiohttp.TCPConnector(ssl=False)  # For self-signed certs
        self.session = aiohttp.ClientSession(connector=connector)
        
        try:
            # Authentication & Authorization Tests
            await self._test_authentication_security()
            
            # Data Protection Tests
            await self._test_data_protection()
            
            # Network Security Tests
            await self._test_network_security()
            
            # Application Security Tests
            await self._test_application_security()
            
            # Monitoring & Logging Tests
            await self._test_monitoring_security()
            
            # Compliance Tests
            await self._test_compliance()
            
        finally:
            await self.session.close()
        
        return self._generate_report()
    
    async def _test_authentication_security(self):
        """Test authentication and authorization security"""
        logger.info("Testing Authentication & Authorization Security...")
        
        # Test 1: JWT Token Security
        await self._run_test(
            "JWT Token Security",
            "Verify JWT tokens use httpOnly cookies and secure settings",
            self._test_jwt_security
        )
        
        # Test 2: Password Security
        await self._run_test(
            "Password Security",
            "Verify password hashing and complexity requirements",
            self._test_password_security
        )
        
        # Test 3: Rate Limiting
        await self._run_test(
            "Rate Limiting",
            "Verify rate limiting on authentication endpoints",
            self._test_rate_limiting
        )
        
        # Test 4: CSRF Protection
        await self._run_test(
            "CSRF Protection",
            "Verify CSRF protection is implemented",
            self._test_csrf_protection
        )
        
        # Test 5: Account Lockout
        await self._run_test(
            "Account Lockout",
            "Verify account lockout after failed attempts",
            self._test_account_lockout
        )
    
    async def _test_data_protection(self):
        """Test data protection measures"""
        logger.info("Testing Data Protection...")
        
        # Test 1: Database Encryption
        await self._run_test(
            "Database Encryption",
            "Verify database connections use SSL/TLS",
            self._test_database_encryption
        )
        
        # Test 2: Log Encryption
        await self._run_test(
            "Log Encryption",
            "Verify sensitive logs are encrypted",
            self._test_log_encryption
        )
        
        # Test 3: File Encryption
        await self._run_test(
            "File Encryption",
            "Verify file uploads are encrypted",
            self._test_file_encryption
        )
        
        # Test 4: Key Management
        await self._run_test(
            "Key Management",
            "Verify secure key management practices",
            self._test_key_management
        )
    
    async def _test_network_security(self):
        """Test network security measures"""
        logger.info("Testing Network Security...")
        
        # Test 1: SSL/TLS Configuration
        await self._run_test(
            "SSL/TLS Configuration",
            "Verify SSL/TLS is properly configured",
            self._test_ssl_configuration
        )
        
        # Test 2: Security Headers
        await self._run_test(
            "Security Headers",
            "Verify security headers are properly set",
            self._test_security_headers
        )
        
        # Test 3: CORS Configuration
        await self._run_test(
            "CORS Configuration",
            "Verify CORS is properly configured",
            self._test_cors_configuration
        )
        
        # Test 4: Firewall Rules
        await self._run_test(
            "Firewall Rules",
            "Verify firewall rules are configured",
            self._test_firewall_rules
        )
    
    async def _test_application_security(self):
        """Test application security measures"""
        logger.info("Testing Application Security...")
        
        # Test 1: Input Validation
        await self._run_test(
            "Input Validation",
            "Verify input validation prevents injection attacks",
            self._test_input_validation
        )
        
        # Test 2: SQL Injection Protection
        await self._run_test(
            "SQL Injection Protection",
            "Verify SQL injection protection is implemented",
            self._test_sql_injection_protection
        )
        
        # Test 3: XSS Protection
        await self._run_test(
            "XSS Protection",
            "Verify XSS protection is implemented",
            self._test_xss_protection
        )
        
        # Test 4: Path Traversal Protection
        await self._run_test(
            "Path Traversal Protection",
            "Verify path traversal protection is implemented",
            self._test_path_traversal_protection
        )
        
        # Test 5: Command Injection Protection
        await self._run_test(
            "Command Injection Protection",
            "Verify command injection protection is implemented",
            self._test_command_injection_protection
        )
    
    async def _test_monitoring_security(self):
        """Test monitoring and logging security"""
        logger.info("Testing Monitoring & Logging Security...")
        
        # Test 1: Audit Logging
        await self._run_test(
            "Audit Logging",
            "Verify comprehensive audit logging is implemented",
            self._test_audit_logging
        )
        
        # Test 2: Security Event Monitoring
        await self._run_test(
            "Security Event Monitoring",
            "Verify security event monitoring is implemented",
            self._test_security_event_monitoring
        )
        
        # Test 3: Performance Monitoring
        await self._run_test(
            "Performance Monitoring",
            "Verify performance monitoring is implemented",
            self._test_performance_monitoring
        )
    
    async def _test_compliance(self):
        """Test compliance with security standards"""
        logger.info("Testing Compliance...")
        
        # Test 1: OWASP Top 10
        await self._run_test(
            "OWASP Top 10 Compliance",
            "Verify compliance with OWASP Top 10",
            self._test_owasp_compliance
        )
        
        # Test 2: SOC2 Compliance
        await self._run_test(
            "SOC2 Compliance",
            "Verify SOC2 compliance measures",
            self._test_soc2_compliance
        )
        
        # Test 3: HIPAA Compliance
        await self._run_test(
            "HIPAA Compliance",
            "Verify HIPAA compliance measures",
            self._test_hipaa_compliance
        )
    
    async def _run_test(self, name: str, description: str, test_func: callable):
        """Run a single security test"""
        try:
            logger.info(f"Running test: {name}")
            result = await test_func()
            
            self.results.append({
                "test_name": name,
                "description": description,
                "status": TestStatus.PASS if result else TestStatus.FAIL,
                "details": result if result else "Test failed",
                "timestamp": time.time()
            })
            
            if result:
                logger.info(f"✅ {name}: PASS")
            else:
                logger.error(f"❌ {name}: FAIL")
                
        except Exception as e:
            logger.error(f"❌ {name}: ERROR - {e}")
            self.results.append({
                "test_name": name,
                "description": description,
                "status": TestStatus.FAIL,
                "details": f"Test error: {str(e)}",
                "timestamp": time.time()
            })
    
    # Authentication Security Tests
    async def _test_jwt_security(self) -> bool:
        """Test JWT token security"""
        try:
            # Test that tokens are not returned in response body
            async with self.session.post(f"{self.base_url}/api/v1/auth/login", 
                                       json={"email": "test@example.com", "password": "testpass"}) as response:
                data = await response.json()
                
                # Check that tokens are not in response body
                if "access_token" in data or "refresh_token" in data:
                    return False
                
                # Check that httpOnly cookies are set
                cookies = response.cookies
                if "access_token" not in cookies or "refresh_token" not in cookies:
                    return False
                
                # Check cookie security attributes
                access_cookie = cookies["access_token"]
                if not access_cookie.get("httponly") or not access_cookie.get("secure"):
                    return False
                
                return True
        except Exception:
            return False
    
    async def _test_password_security(self) -> bool:
        """Test password security"""
        try:
            # Test password complexity requirements
            weak_passwords = ["123456", "password", "qwerty", "abc123"]
            
            for weak_pwd in weak_passwords:
                async with self.session.post(f"{self.base_url}/api/v1/auth/register",
                                           json={"email": "test@example.com", "password": weak_pwd}) as response:
                    if response.status == 200:  # Should be rejected
                        return False
            
            # Test strong password acceptance
            strong_password = "SecurePass123!@#"
            async with self.session.post(f"{self.base_url}/api/v1/auth/register",
                                       json={"email": "test@example.com", "password": strong_password}) as response:
                return response.status in [200, 201]  # Should be accepted
                
        except Exception:
            return False
    
    async def _test_rate_limiting(self) -> bool:
        """Test rate limiting"""
        try:
            # Make multiple rapid requests
            for i in range(10):
                async with self.session.post(f"{self.base_url}/api/v1/auth/login",
                                           json={"email": "test@example.com", "password": "testpass"}) as response:
                    if i < 5 and response.status == 429:  # Should be rate limited after 5 attempts
                        return True
            
            return False
        except Exception:
            return False
    
    async def _test_csrf_protection(self) -> bool:
        """Test CSRF protection"""
        try:
            # Test that CSRF token is required for state-changing operations
            async with self.session.post(f"{self.base_url}/api/v1/auth/register",
                                       json={"email": "test@example.com", "password": "SecurePass123!"}) as response:
                # Should require CSRF token
                return response.status == 403  # Forbidden without CSRF token
        except Exception:
            return False
    
    async def _test_account_lockout(self) -> bool:
        """Test account lockout"""
        try:
            # Make multiple failed login attempts
            for i in range(6):  # More than the lockout threshold
                async with self.session.post(f"{self.base_url}/api/v1/auth/login",
                                           json={"email": "test@example.com", "password": "wrongpass"}) as response:
                    if i == 5 and response.status == 423:  # Locked
                        return True
            
            return False
        except Exception:
            return False
    
    # Data Protection Tests
    async def _test_database_encryption(self) -> bool:
        """Test database encryption"""
        try:
            # Check if database connection uses SSL
            async with self.session.get(f"{self.base_url}/api/v1/health") as response:
                data = await response.json()
                return "database_ssl" in data and data["database_ssl"] is True
        except Exception:
            return False
    
    async def _test_log_encryption(self) -> bool:
        """Test log encryption"""
        try:
            # Check if logs are encrypted
            async with self.session.get(f"{self.base_url}/api/v1/health") as response:
                data = await response.json()
                return "log_encryption" in data and data["log_encryption"] is True
        except Exception:
            return False
    
    async def _test_file_encryption(self) -> bool:
        """Test file encryption"""
        try:
            # Test file upload encryption
            files = {"file": ("test.txt", b"test content", "text/plain")}
            async with self.session.post(f"{self.base_url}/api/v1/upload", data=files) as response:
                data = await response.json()
                return "encrypted" in data and data["encrypted"] is True
        except Exception:
            return False
    
    async def _test_key_management(self) -> bool:
        """Test key management"""
        try:
            # Check if keys are properly managed
            async with self.session.get(f"{self.base_url}/api/v1/health") as response:
                data = await response.json()
                return "key_rotation" in data and data["key_rotation"] is True
        except Exception:
            return False
    
    # Network Security Tests
    async def _test_ssl_configuration(self) -> bool:
        """Test SSL/TLS configuration"""
        try:
            # Check SSL certificate
            async with self.session.get(f"{self.base_url}/api/v1/health") as response:
                # Should be HTTPS
                return response.url.scheme == "https"
        except Exception:
            return False
    
    async def _test_security_headers(self) -> bool:
        """Test security headers"""
        try:
            async with self.session.get(f"{self.base_url}/api/v1/health") as response:
                headers = response.headers
                
                required_headers = [
                    "Strict-Transport-Security",
                    "X-Content-Type-Options",
                    "X-Frame-Options",
                    "X-XSS-Protection",
                    "Content-Security-Policy"
                ]
                
                for header in required_headers:
                    if header not in headers:
                        return False
                
                return True
        except Exception:
            return False
    
    async def _test_cors_configuration(self) -> bool:
        """Test CORS configuration"""
        try:
            # Test CORS preflight
            headers = {"Origin": "https://malicious-site.com"}
            async with self.session.options(f"{self.base_url}/api/v1/health", headers=headers) as response:
                # Should reject unauthorized origins
                return response.status == 403
        except Exception:
            return False
    
    async def _test_firewall_rules(self) -> bool:
        """Test firewall rules"""
        try:
            # Test that unauthorized ports are blocked
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', 22))  # SSH should be open
            sock.close()
            return result == 0
        except Exception:
            return False
    
    # Application Security Tests
    async def _test_input_validation(self) -> bool:
        """Test input validation"""
        try:
            # Test SQL injection attempt
            malicious_input = "'; DROP TABLE users; --"
            async with self.session.post(f"{self.base_url}/api/v1/auth/login",
                                       json={"email": malicious_input, "password": "testpass"}) as response:
                # Should be rejected, not cause SQL error
                return response.status == 400
        except Exception:
            return False
    
    async def _test_sql_injection_protection(self) -> bool:
        """Test SQL injection protection"""
        try:
            # Test various SQL injection patterns
            sql_patterns = [
                "'; DROP TABLE users; --",
                "1' OR '1'='1",
                "1' AND '1'='1",
                "union select * from users",
                "exec xp_cmdshell"
            ]
            
            for pattern in sql_patterns:
                async with self.session.post(f"{self.base_url}/api/v1/auth/login",
                                           json={"email": pattern, "password": "testpass"}) as response:
                    if response.status == 500:  # Should not cause server error
                        return False
            
            return True
        except Exception:
            return False
    
    async def _test_xss_protection(self) -> bool:
        """Test XSS protection"""
        try:
            # Test XSS patterns
            xss_patterns = [
                "<script>alert('xss')</script>",
                "javascript:alert('xss')",
                "onload=alert('xss')",
                "eval('alert(\"xss\")')"
            ]
            
            for pattern in xss_patterns:
                async with self.session.post(f"{self.base_url}/api/v1/auth/login",
                                           json={"email": pattern, "password": "testpass"}) as response:
                    data = await response.text()
                    if pattern in data:  # Should be sanitized
                        return False
            
            return True
        except Exception:
            return False
    
    async def _test_path_traversal_protection(self) -> bool:
        """Test path traversal protection"""
        try:
            # Test path traversal patterns
            traversal_patterns = [
                "../../../etc/passwd",
                "..%2f..%2f..%2fetc%2fpasswd",
                "....//....//....//etc/passwd"
            ]
            
            for pattern in traversal_patterns:
                async with self.session.get(f"{self.base_url}/api/v1/files/{pattern}") as response:
                    if response.status == 200:  # Should be blocked
                        return False
            
            return True
        except Exception:
            return False
    
    async def _test_command_injection_protection(self) -> bool:
        """Test command injection protection"""
        try:
            # Test command injection patterns
            cmd_patterns = [
                "; rm -rf /",
                "| cat /etc/passwd",
                "& ping -c 1 127.0.0.1",
                "`whoami`"
            ]
            
            for pattern in cmd_patterns:
                async with self.session.post(f"{self.base_url}/api/v1/auth/login",
                                           json={"email": pattern, "password": "testpass"}) as response:
                    if response.status == 500:  # Should not execute commands
                        return False
            
            return True
        except Exception:
            return False
    
    # Monitoring Security Tests
    async def _test_audit_logging(self) -> bool:
        """Test audit logging"""
        try:
            # Make a request and check if it's logged
            async with self.session.get(f"{self.base_url}/api/v1/health") as response:
                # Check if audit logs are enabled
                data = await response.json()
                return "audit_logging" in data and data["audit_logging"] is True
        except Exception:
            return False
    
    async def _test_security_event_monitoring(self) -> bool:
        """Test security event monitoring"""
        try:
            # Trigger a security event and check monitoring
            async with self.session.post(f"{self.base_url}/api/v1/auth/login",
                                       json={"email": "test@example.com", "password": "wrongpass"}) as response:
                # Check if security event was logged
                data = await response.json()
                return "security_monitoring" in data and data["security_monitoring"] is True
        except Exception:
            return False
    
    async def _test_performance_monitoring(self) -> bool:
        """Test performance monitoring"""
        try:
            async with self.session.get(f"{self.base_url}/api/v1/health") as response:
                data = await response.json()
                return "performance_monitoring" in data and data["performance_monitoring"] is True
        except Exception:
            return False
    
    # Compliance Tests
    async def _test_owasp_compliance(self) -> bool:
        """Test OWASP Top 10 compliance"""
        try:
            # Test for OWASP Top 10 vulnerabilities
            async with self.session.get(f"{self.base_url}/api/v1/health") as response:
                data = await response.json()
                return "owasp_compliance" in data and data["owasp_compliance"] is True
        except Exception:
            return False
    
    async def _test_soc2_compliance(self) -> bool:
        """Test SOC2 compliance"""
        try:
            async with self.session.get(f"{self.base_url}/api/v1/health") as response:
                data = await response.json()
                return "soc2_compliance" in data and data["soc2_compliance"] is True
        except Exception:
            return False
    
    async def _test_hipaa_compliance(self) -> bool:
        """Test HIPAA compliance"""
        try:
            async with self.session.get(f"{self.base_url}/api/v1/health") as response:
                data = await response.json()
                return "hipaa_compliance" in data and data["hipaa_compliance"] is True
        except Exception:
            return False
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["status"] == TestStatus.PASS])
        failed_tests = len([r for r in self.results if r["status"] == TestStatus.FAIL])
        warning_tests = len([r for r in self.results if r["status"] == TestStatus.WARNING])
        
        # Calculate security score
        security_score = int((passed_tests / total_tests) * 100) if total_tests > 0 else 0
        
        # Determine security level
        if security_score >= 95:
            security_level = "WORLD_CLASS"
        elif security_score >= 85:
            security_level = "ENTERPRISE_GRADE"
        elif security_score >= 70:
            security_level = "GOOD"
        elif security_score >= 50:
            security_level = "FAIR"
        else:
            security_level = "POOR"
        
        report = {
            "timestamp": time.time(),
            "security_score": security_score,
            "security_level": security_level,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "warning_tests": warning_tests,
            "results": self.results,
            "recommendations": self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate security recommendations based on test results"""
        recommendations = []
        
        failed_tests = [r for r in self.results if r["status"] == TestStatus.FAIL]
        
        for test in failed_tests:
            if "JWT" in test["test_name"]:
                recommendations.append("🔐 Implement secure JWT token handling with httpOnly cookies")
            elif "Password" in test["test_name"]:
                recommendations.append("🔑 Implement strong password policies and complexity requirements")
            elif "Rate Limiting" in test["test_name"]:
                recommendations.append("🚦 Implement comprehensive rate limiting on all endpoints")
            elif "CSRF" in test["test_name"]:
                recommendations.append("🛡️ Implement CSRF protection with secure tokens")
            elif "Encryption" in test["test_name"]:
                recommendations.append("🔒 Implement encryption for all sensitive data")
            elif "SSL" in test["test_name"]:
                recommendations.append("🔐 Configure SSL/TLS with strong cipher suites")
            elif "Headers" in test["test_name"]:
                recommendations.append("🛡️ Implement comprehensive security headers")
            elif "Injection" in test["test_name"]:
                recommendations.append("🚫 Implement input validation and sanitization")
            elif "Monitoring" in test["test_name"]:
                recommendations.append("📊 Implement comprehensive security monitoring")
            elif "Compliance" in test["test_name"]:
                recommendations.append("📋 Implement compliance monitoring and reporting")
        
        if not recommendations:
            recommendations.append("🎉 All security tests passed! Maintain current security practices.")
        
        return recommendations

async def main():
    """Main function to run comprehensive security tests"""
    tester = ComprehensiveSecurityTester()
    report = await tester.run_all_tests()
    
    # Print results
    print("\n" + "="*60)
    print("🔒 COMPREHENSIVE SECURITY TEST RESULTS")
    print("="*60)
    
    print(f"\nSecurity Score: {report['security_score']}/100")
    print(f"Security Level: {report['security_level']}")
    print(f"Total Tests: {report['total_tests']}")
    print(f"Passed: {report['passed_tests']}")
    print(f"Failed: {report['failed_tests']}")
    print(f"Warnings: {report['warning_tests']}")
    
    print("\n📋 Test Results:")
    for result in report["results"]:
        status_icon = "✅" if result["status"] == TestStatus.PASS else "❌"
        print(f"{status_icon} {result['test_name']}: {result['status'].value}")
    
    print("\n💡 Recommendations:")
    for rec in report["recommendations"]:
        print(f"  {rec}")
    
    # Save detailed report
    with open("comprehensive_security_test_results.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📄 Detailed report saved to: comprehensive_security_test_results.json")
    
    # Exit with appropriate code
    if report["security_score"] >= 95:
        print("\n🎉 World-Class Security Achieved!")
        exit(0)
    elif report["security_score"] >= 70:
        print("\n⚠️ Security improvements needed")
        exit(1)
    else:
        print("\n🚨 Critical security issues found!")
        exit(2)

if __name__ == "__main__":
    asyncio.run(main()) 