#!/usr/bin/env python3
"""
Security Testing Script for CloudMind
"""

import requests
import json
import sys
from typing import Dict, List, Any
from urllib.parse import urljoin


class SecurityTester:
    """Comprehensive security testing for CloudMind API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
    
    def test_cors_configuration(self) -> Dict[str, Any]:
        """Test CORS configuration"""
        print("🔒 Testing CORS configuration...")
        
        test_origins = [
            "http://localhost:3000",
            "https://cloudmind.local",
            "https://malicious-site.com",
            "http://evil.com"
        ]
        
        results = {
            "test": "CORS Configuration",
            "passed": True,
            "details": []
        }
        
        for origin in test_origins:
            headers = {"Origin": origin}
            response = self.session.options(f"{self.base_url}/health", headers=headers)
            
            acao = response.headers.get("Access-Control-Allow-Origin")
            if acao:
                if origin in ["http://localhost:3000", "https://cloudmind.local"]:
                    if acao == origin or acao == "*":
                        results["details"].append(f"✅ Origin {origin} allowed correctly")
                    else:
                        results["details"].append(f"❌ Origin {origin} incorrectly allowed")
                        results["passed"] = False
                else:
                    if acao == "*":
                        results["details"].append(f"❌ Malicious origin {origin} allowed")
                        results["passed"] = False
                    else:
                        results["details"].append(f"✅ Malicious origin {origin} correctly blocked")
            else:
                results["details"].append(f"✅ Origin {origin} blocked (no CORS headers)")
        
        return results
    
    def test_security_headers(self) -> Dict[str, Any]:
        """Test security headers"""
        print("🔒 Testing security headers...")
        
        response = self.session.get(f"{self.base_url}/health")
        headers = response.headers
        
        required_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload"
        }
        
        results = {
            "test": "Security Headers",
            "passed": True,
            "details": []
        }
        
        for header, expected_value in required_headers.items():
            actual_value = headers.get(header)
            if actual_value:
                if expected_value in actual_value:
                    results["details"].append(f"✅ {header}: {actual_value}")
                else:
                    results["details"].append(f"❌ {header}: expected '{expected_value}', got '{actual_value}'")
                    results["passed"] = False
            else:
                results["details"].append(f"❌ {header}: missing")
                results["passed"] = False
        
        # Check for server information leakage
        if "Server" in headers:
            results["details"].append(f"❌ Server header exposed: {headers['Server']}")
            results["passed"] = False
        else:
            results["details"].append("✅ Server header properly hidden")
        
        return results
    
    def test_input_validation(self) -> Dict[str, Any]:
        """Test input validation"""
        print("🔒 Testing input validation...")
        
        malicious_inputs = [
            "<script>alert('xss')</script>",
            "'; DROP TABLE users; --",
            "../../../etc/passwd",
            "javascript:alert('xss')",
            "{{7*7}}",
            "{{config.items()}}",
            "{{''.__class__.__mro__[2].__subclasses__()}}"
        ]
        
        results = {
            "test": "Input Validation",
            "passed": True,
            "details": []
        }
        
        for malicious_input in malicious_inputs:
            # Test query parameters
            response = self.session.get(f"{self.base_url}/health?test={malicious_input}")
            if response.status_code == 400:
                results["details"].append(f"✅ Malicious query param blocked: {malicious_input[:20]}...")
            else:
                results["details"].append(f"❌ Malicious query param allowed: {malicious_input[:20]}...")
                results["passed"] = False
            
            # Test path parameters
            response = self.session.get(f"{self.base_url}/health/{malicious_input}")
            if response.status_code == 400:
                results["details"].append(f"✅ Malicious path param blocked: {malicious_input[:20]}...")
            else:
                results["details"].append(f"❌ Malicious path param allowed: {malicious_input[:20]}...")
                results["passed"] = False
        
        return results
    
    def test_rate_limiting(self) -> Dict[str, Any]:
        """Test rate limiting"""
        print("🔒 Testing rate limiting...")
        
        results = {
            "test": "Rate Limiting",
            "passed": True,
            "details": []
        }
        
        # Make multiple requests to trigger rate limiting
        rate_limited = False
        for i in range(150):  # More than the 100/minute limit
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 429:
                rate_limited = True
                results["details"].append(f"✅ Rate limiting triggered after {i+1} requests")
                break
        
        if not rate_limited:
            results["details"].append("❌ Rate limiting not triggered")
            results["passed"] = False
        else:
            results["details"].append("✅ Rate limiting working correctly")
        
        return results
    
    def test_authentication(self) -> Dict[str, Any]:
        """Test authentication endpoints"""
        print("🔒 Testing authentication...")
        
        results = {
            "test": "Authentication",
            "passed": True,
            "details": []
        }
        
        # Test weak password rejection
        weak_password_data = {
            "email": "test@example.com",
            "password": "weak",
            "username": "testuser",
            "full_name": "Test User"
        }
        
        response = self.session.post(f"{self.base_url}/api/v1/auth/register", json=weak_password_data)
        if response.status_code == 422:
            results["details"].append("✅ Weak password correctly rejected")
        else:
            results["details"].append("❌ Weak password allowed")
            results["passed"] = False
        
        # Test SQL injection in login
        sql_injection_data = {
            "email": "'; DROP TABLE users; --",
            "password": "password123"
        }
        
        response = self.session.post(f"{self.base_url}/api/v1/auth/login", json=sql_injection_data)
        if response.status_code == 400:
            results["details"].append("✅ SQL injection attempt blocked")
        else:
            results["details"].append("❌ SQL injection attempt allowed")
            results["passed"] = False
        
        return results
    
    def run_all_tests(self) -> List[Dict[str, Any]]:
        """Run all security tests"""
        print("🚀 Starting comprehensive security testing...")
        
        tests = [
            self.test_cors_configuration,
            self.test_security_headers,
            self.test_input_validation,
            self.test_rate_limiting,
            self.test_authentication
        ]
        
        for test in tests:
            try:
                result = test()
                self.results.append(result)
            except Exception as e:
                self.results.append({
                    "test": test.__name__,
                    "passed": False,
                    "details": [f"❌ Test failed with error: {str(e)}"]
                })
        
        return self.results
    
    def print_results(self):
        """Print test results"""
        print("\n" + "="*60)
        print("🔒 SECURITY TEST RESULTS")
        print("="*60)
        
        passed = 0
        total = len(self.results)
        
        for result in self.results:
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            print(f"\n{status} - {result['test']}")
            
            for detail in result["details"]:
                print(f"  {detail}")
            
            if result["passed"]:
                passed += 1
        
        print(f"\n{'='*60}")
        print(f"📊 SUMMARY: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All security tests passed!")
            return True
        else:
            print("⚠️  Some security tests failed. Please review the results.")
            return False


def main():
    """Main function"""
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    tester = SecurityTester(base_url)
    results = tester.run_all_tests()
    success = tester.print_results()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 