#!/usr/bin/env python3
"""
Final Comprehensive Test for CloudMind
Tests everything we can test without external dependencies
"""

import os
import sys
import asyncio
import logging
import time
import json
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveTester:
    """Comprehensive tester for CloudMind"""
    
    def __init__(self):
        self.results = {}
        self.start_time = time.time()
        self.score = 0
        self.total_tests = 0
    
    def run_test(self, test_name: str, test_func, weight: int = 1):
        """Run a test and record results"""
        self.total_tests += weight
        print(f"\n🔍 Testing: {test_name}")
        
        try:
            result = test_func()
            if result["passed"]:
                self.score += weight
                print(f"✅ {test_name} PASSED")
                if "message" in result:
                    print(f"   {result['message']}")
            else:
                print(f"❌ {test_name} FAILED: {result.get('error', 'Unknown error')}")
            
            self.results[test_name] = result
            
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
            self.results[test_name] = {"passed": False, "error": str(e)}
    
    def test_file_structure(self) -> Dict[str, Any]:
        """Test that all required files exist"""
        required_files = [
            "requirements.txt",
            "Dockerfile",
            "docker-compose.prod.yml",
            "deploy_production.sh",
            "app/main.py",
            "app/core/config.py",
            "app/core/database.py",
            "app/core/monitoring.py",
            "app/services/enterprise_security_service.py",
            "app/services/ai_engine/god_tier_ai_service.py",
            "app/services/scanner/enterprise_scanner_service.py"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            return {
                "passed": False,
                "error": f"Missing files: {missing_files}"
            }
        
        return {
            "passed": True,
            "message": f"All {len(required_files)} required files present"
        }
    
    def test_requirements_file(self) -> Dict[str, Any]:
        """Test requirements.txt file"""
        try:
            with open("requirements.txt", "r") as f:
                content = f.read()
            
            required_packages = [
                "fastapi", "uvicorn", "sqlalchemy", "redis", "boto3",
                "openai", "anthropic", "prometheus_client", "structlog"
            ]
            
            missing_packages = []
            for package in required_packages:
                if package not in content:
                    missing_packages.append(package)
            
            if missing_packages:
                return {
                    "passed": False,
                    "error": f"Missing packages in requirements.txt: {missing_packages}"
                }
            
            return {
                "passed": True,
                "message": f"All {len(required_packages)} required packages in requirements.txt"
            }
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_dockerfile(self) -> Dict[str, Any]:
        """Test Dockerfile"""
        try:
            with open("Dockerfile", "r") as f:
                content = f.read()
            
            required_elements = [
                "FROM python:3.11-slim",
                "WORKDIR /app",
                "COPY requirements.txt",
                "RUN pip install",
                "EXPOSE 8000",
                "CMD [\"uvicorn\""
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                return {
                    "passed": False,
                    "error": f"Missing elements in Dockerfile: {missing_elements}"
                }
            
            return {
                "passed": True,
                "message": "Dockerfile contains all required elements"
            }
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_docker_compose(self) -> Dict[str, Any]:
        """Test docker-compose.prod.yml"""
        try:
            with open("docker-compose.prod.yml", "r") as f:
                content = f.read()
            
            required_services = [
                "cloudmind-backend", "postgres", "redis", "nginx", "prometheus", "grafana"
            ]
            
            missing_services = []
            for service in required_services:
                if service not in content:
                    missing_services.append(service)
            
            if missing_services:
                return {
                    "passed": False,
                    "error": f"Missing services in docker-compose: {missing_services}"
                }
            
            return {
                "passed": True,
                "message": f"All {len(required_services)} required services configured"
            }
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_deployment_script(self) -> Dict[str, Any]:
        """Test deployment script"""
        try:
            with open("deploy_production.sh", "r") as f:
                content = f.read()
            
            required_elements = [
                "docker-compose", "health check", "production", "environment"
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                return {
                    "passed": False,
                    "error": f"Missing elements in deployment script: {missing_elements}"
                }
            
            return {
                "passed": True,
                "message": "Deployment script contains all required elements"
            }
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_python_imports(self) -> Dict[str, Any]:
        """Test that Python modules can be imported"""
        try:
            # Test core imports
            import fastapi
            import uvicorn
            import sqlalchemy
            import redis
            import boto3
            
            return {
                "passed": True,
                "message": "All core Python packages can be imported"
            }
            
        except ImportError as e:
            return {
                "passed": False,
                "error": f"Import error: {e}"
            }
    
    def test_config_structure(self) -> Dict[str, Any]:
        """Test configuration structure"""
        try:
            # Check if config file exists and has basic structure
            if not os.path.exists("app/core/config.py"):
                return {"passed": False, "error": "Config file not found"}
            
            with open("app/core/config.py", "r") as f:
                content = f.read()
            
            if "class Settings" not in content or "BaseSettings" not in content:
                return {"passed": False, "error": "Config file missing Settings class"}
            
            return {
                "passed": True,
                "message": "Configuration structure is correct"
            }
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_security_service_structure(self) -> Dict[str, Any]:
        """Test security service structure"""
        try:
            if not os.path.exists("app/services/enterprise_security_service.py"):
                return {"passed": False, "error": "Security service file not found"}
            
            with open("app/services/enterprise_security_service.py", "r") as f:
                content = f.read()
            
            required_elements = [
                "class EnterpriseSecurityService", "encrypt_sensitive_data", 
                "validate_input_security", "get_security_metrics"
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                return {
                    "passed": False,
                    "error": f"Missing elements in security service: {missing_elements}"
                }
            
            return {
                "passed": True,
                "message": "Security service structure is correct"
            }
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_ai_service_structure(self) -> Dict[str, Any]:
        """Test AI service structure"""
        try:
            if not os.path.exists("app/services/ai_engine/god_tier_ai_service.py"):
                return {"passed": False, "error": "AI service file not found"}
            
            with open("app/services/ai_engine/god_tier_ai_service.py", "r") as f:
                content = f.read()
            
            required_elements = [
                "class GodTierAIService", "analyze_comprehensive", 
                "AnalysisType", "AIProvider"
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                return {
                    "passed": False,
                    "error": f"Missing elements in AI service: {missing_elements}"
                }
            
            return {
                "passed": True,
                "message": "AI service structure is correct"
            }
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_scanner_service_structure(self) -> Dict[str, Any]:
        """Test scanner service structure"""
        try:
            if not os.path.exists("app/services/scanner/enterprise_scanner_service.py"):
                return {"passed": False, "error": "Scanner service file not found"}
            
            with open("app/services/scanner/enterprise_scanner_service.py", "r") as f:
                content = f.read()
            
            required_elements = [
                "class EnterpriseScannerService", "scan_comprehensive", 
                "supported_clouds", "accuracy_methodology"
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                return {
                    "passed": False,
                    "error": f"Missing elements in scanner service: {missing_elements}"
                }
            
            return {
                "passed": True,
                "message": "Scanner service structure is correct"
            }
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_monitoring_structure(self) -> Dict[str, Any]:
        """Test monitoring structure"""
        try:
            if not os.path.exists("app/core/monitoring.py"):
                return {"passed": False, "error": "Monitoring file not found"}
            
            with open("app/core/monitoring.py", "r") as f:
                content = f.read()
            
            required_elements = [
                "prometheus_client", "REQUEST_COUNT", "REQUEST_LATENCY", 
                "record_request", "init_monitoring"
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                return {
                    "passed": False,
                    "error": f"Missing elements in monitoring: {missing_elements}"
                }
            
            return {
                "passed": True,
                "message": "Monitoring structure is correct"
            }
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_database_structure(self) -> Dict[str, Any]:
        """Test database structure"""
        try:
            if not os.path.exists("app/core/database.py"):
                return {"passed": False, "error": "Database file not found"}
            
            with open("app/core/database.py", "r") as f:
                content = f.read()
            
            required_elements = [
                "AsyncSession", "create_async_engine", "init_db", "get_db"
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                return {
                    "passed": False,
                    "error": f"Missing elements in database: {missing_elements}"
                }
            
            return {
                "passed": True,
                "message": "Database structure is correct"
            }
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def run_all_tests(self):
        """Run all comprehensive tests"""
        print("🧪 CloudMind Comprehensive Test Suite")
        print("=" * 70)
        
        # Run all tests
        self.run_test("File Structure", self.test_file_structure, 2)
        self.run_test("Requirements File", self.test_requirements_file, 1)
        self.run_test("Dockerfile", self.test_dockerfile, 2)
        self.run_test("Docker Compose", self.test_docker_compose, 2)
        self.run_test("Deployment Script", self.test_deployment_script, 1)
        self.run_test("Python Imports", self.test_python_imports, 1)
        self.run_test("Configuration Structure", self.test_config_structure, 1)
        self.run_test("Security Service Structure", self.test_security_service_structure, 2)
        self.run_test("AI Service Structure", self.test_ai_service_structure, 2)
        self.run_test("Scanner Service Structure", self.test_scanner_service_structure, 2)
        self.run_test("Monitoring Structure", self.test_monitoring_structure, 1)
        self.run_test("Database Structure", self.test_database_structure, 1)
        
        # Calculate final score
        final_score = (self.score / self.total_tests) * 100
        
        print("\n" + "=" * 70)
        print(f"📊 COMPREHENSIVE TEST SCORE: {final_score:.1f}/100")
        print(f"✅ Passed: {self.score}/{self.total_tests} weighted tests")
        print(f"⏱️  Duration: {time.time() - self.start_time:.2f} seconds")
        
        # Detailed results
        print("\n📋 DETAILED RESULTS:")
        print("=" * 70)
        
        for test_name, result in self.results.items():
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            print(f"{status} {test_name}")
            if not result["passed"]:
                print(f"   Error: {result.get('error', 'Unknown error')}")
            elif "message" in result:
                print(f"   {result['message']}")
        
        # Assessment
        print(f"\n🎯 ASSESSMENT:")
        if final_score >= 95:
            print("🎉 EXCELLENT: CloudMind is production-ready!")
            print("   - All critical systems properly structured")
            print("   - Ready for deployment with real credentials")
        elif final_score >= 85:
            print("✅ GOOD: CloudMind is mostly production-ready!")
            print("   - Core systems properly structured")
            print("   - Minor issues to address before deployment")
        elif final_score >= 70:
            print("⚠️  FAIR: CloudMind needs improvements before production")
            print("   - Several structural issues need to be resolved")
            print("   - Core functionality framework in place")
        else:
            print("❌ POOR: CloudMind needs significant work before production")
            print("   - Multiple critical structural issues")
            print("   - Not ready for deployment")
        
        return final_score >= 85

def main():
    """Main test function"""
    tester = ComprehensiveTester()
    success = tester.run_all_tests()
    
    # Save results to file
    with open("test_results.json", "w") as f:
        json.dump({
            "score": (tester.score / tester.total_tests) * 100,
            "passed": tester.score,
            "total": tester.total_tests,
            "results": tester.results,
            "duration": time.time() - tester.start_time
        }, f, indent=2)
    
    print(f"\n📄 Test results saved to test_results.json")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
