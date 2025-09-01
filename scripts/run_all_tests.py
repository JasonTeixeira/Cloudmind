#!/usr/bin/env python3
"""
Master Test Runner for CloudMind
Executes ALL types of tests to ensure the project is production-ready
"""

import os
import sys
import time
import subprocess
import json
import argparse
import signal
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import psutil
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_results.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
    """Test result data class"""
    test_type: str
    test_name: str
    status: str  # 'passed', 'failed', 'skipped', 'error'
    duration: float
    output: str
    error_message: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None

class MasterTestRunner:
    """Master test runner that executes all test types"""
    
    def __init__(self, args):
        self.args = args
        self.results: List[TestResult] = []
        self.start_time = time.time()
        self.test_processes: List[subprocess.Popen] = []
        self.project_root = Path(__file__).parent.parent
        
    def run_command(self, command: List[str], timeout: int = 600, cwd: Optional[str] = None) -> TestResult:
        """Run a command and capture the result"""
        start_time = time.time()
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=cwd or str(self.project_root)
            )
            
            self.test_processes.append(process)
            
            stdout, stderr = process.communicate(timeout=timeout)
            duration = time.time() - start_time
            
            if process.returncode == 0:
                status = 'passed'
                error_message = None
            else:
                status = 'failed'
                error_message = stderr if stderr else stdout
            
            return TestResult(
                test_type='command',
                test_name=' '.join(command),
                status=status,
                duration=duration,
                output=stdout,
                error_message=error_message
            )
            
        except subprocess.TimeoutExpired:
            process.kill()
            return TestResult(
                test_type='command',
                test_name=' '.join(command),
                status='error',
                duration=timeout,
                output='',
                error_message=f'Command timed out after {timeout} seconds'
            )
        except Exception as e:
            return TestResult(
                test_type='command',
                test_name=' '.join(command),
                status='error',
                duration=time.time() - start_time,
                output='',
                error_message=str(e)
            )
    
    def run_backend_unit_tests(self) -> TestResult:
        """Run backend unit tests with pytest"""
        logger.info("🔬 Running backend unit tests...")
        return self.run_command([
            "python", "-m", "pytest", 
            "backend/tests/", 
            "-v", 
            "--tb=short",
            "--cov=backend/app",
            "--cov-report=html:backend/coverage_html",
            "--cov-report=term-missing"
        ], cwd=str(self.project_root))
    
    def run_backend_integration_tests(self) -> TestResult:
        """Run backend integration tests"""
        logger.info("🔗 Running backend integration tests...")
        return self.run_command([
            "python", "backend/tests/test_final_comprehensive.py"
        ], cwd=str(self.project_root))
    
    def run_backend_stress_tests(self) -> TestResult:
        """Run backend stress tests"""
        logger.info("💪 Running backend stress tests...")
        return self.run_command([
            "python", "backend/tests/test_stress.py"
        ], cwd=str(self.project_root))
    
    def run_backend_chaos_tests(self) -> TestResult:
        """Run backend chaos engineering tests"""
        logger.info("🌪️ Running backend chaos tests...")
        return self.run_command([
            "python", "backend/tests/test_chaos.py"
        ], cwd=str(self.project_root))
    
    def run_backend_security_tests(self) -> TestResult:
        """Run backend security tests"""
        logger.info("🔒 Running backend security tests...")
        return self.run_command([
            "python", "backend/tests/test_security.py"
        ], cwd=str(self.project_root))
    
    def run_backend_ml_tests(self) -> TestResult:
        """Run backend ML/AI tests"""
        logger.info("🤖 Running backend ML/AI tests...")
        return self.run_command([
            "python", "backend/tests/test_ml_framework.py"
        ], cwd=str(self.project_root))
    
    def run_frontend_unit_tests(self) -> TestResult:
        """Run frontend unit tests with Jest"""
        logger.info("🎨 Running frontend unit tests...")
        return self.run_command([
            "npm", "test", "--", "--coverage", "--watchAll=false"
        ], cwd=str(self.project_root / "frontend"))
    
    def run_frontend_type_check(self) -> TestResult:
        """Run frontend TypeScript type checking"""
        logger.info("📝 Running frontend type checking...")
        return self.run_command([
            "npm", "run", "type-check"
        ], cwd=str(self.project_root / "frontend"))
    
    def run_frontend_lint(self) -> TestResult:
        """Run frontend linting"""
        logger.info("🧹 Running frontend linting...")
        return self.run_command([
            "npm", "run", "lint"
        ], cwd=str(self.project_root / "frontend"))
    
    def run_frontend_build_test(self) -> TestResult:
        """Test frontend build process"""
        logger.info("🏗️ Testing frontend build...")
        return self.run_command([
            "npm", "run", "build"
        ], cwd=str(self.project_root / "frontend"))
    
    def run_backend_lint(self) -> TestResult:
        """Run backend linting with flake8"""
        logger.info("🧹 Running backend linting...")
        return self.run_command([
            "python", "-m", "flake8", "backend/app", "--max-line-length=100"
        ], cwd=str(self.project_root))
    
    def run_backend_type_check(self) -> TestResult:
        """Run backend type checking with mypy"""
        logger.info("📝 Running backend type checking...")
        return self.run_command([
            "python", "-m", "mypy", "backend/app"
        ], cwd=str(self.project_root))
    
    def run_backend_format_check(self) -> TestResult:
        """Check backend code formatting"""
        logger.info("🎨 Checking backend code formatting...")
        return self.run_command([
            "python", "-m", "black", "--check", "backend/app"
        ], cwd=str(self.project_root))
    
    def run_docker_build_test(self) -> TestResult:
        """Test Docker builds"""
        logger.info("🐳 Testing Docker builds...")
        
        # Test backend Docker build
        backend_result = self.run_command([
            "docker", "build", "-t", "cloudmind-backend-test", "backend/"
        ], cwd=str(self.project_root))
        
        if backend_result.status != 'passed':
            return backend_result
        
        # Test frontend Docker build
        frontend_result = self.run_command([
            "docker", "build", "-t", "cloudmind-frontend-test", "frontend/"
        ], cwd=str(self.project_root))
        
        return frontend_result
    
    def run_load_tests(self) -> TestResult:
        """Run load tests with k6"""
        logger.info("📊 Running load tests...")
        return self.run_command([
            "k6", "run", "backend/tests/k6_load_test.js"
        ], cwd=str(self.project_root))
    
    def run_database_migration_test(self) -> TestResult:
        """Test database migrations"""
        logger.info("🗄️ Testing database migrations...")
        return self.run_command([
            "python", "-m", "alembic", "upgrade", "head"
        ], cwd=str(self.project_root / "backend"))
    
    def run_security_scan(self) -> TestResult:
        """Run security vulnerability scan"""
        logger.info("🔍 Running security vulnerability scan...")
        return self.run_command([
            "python", "scripts/security/vulnerability_assessment.py"
        ], cwd=str(self.project_root))
    
    def run_performance_tests(self) -> TestResult:
        """Run performance tests"""
        logger.info("⚡ Running performance tests...")
        return self.run_command([
            "python", "scripts/testing/performance_test.py"
        ], cwd=str(self.project_root))
    
    def run_api_tests(self) -> TestResult:
        """Run API endpoint tests"""
        logger.info("🌐 Running API endpoint tests...")
        return self.run_command([
            "python", "backend/tests/test_main.py"
        ], cwd=str(self.project_root))
    
    def run_infrastructure_tests(self) -> TestResult:
        """Run infrastructure tests"""
        logger.info("🏗️ Running infrastructure tests...")
        return self.run_command([
            "python", "backend/tests/test_production_ready.py"
        ], cwd=str(self.project_root))
    
    def run_ai_service_tests(self) -> TestResult:
        """Run AI service tests"""
        logger.info("🧠 Running AI service tests...")
        return self.run_command([
            "python", "backend/tests/test_ensemble_ai.py"
        ], cwd=str(self.project_root))
    
    def run_monitoring_tests(self) -> TestResult:
        """Run monitoring and observability tests"""
        logger.info("📈 Running monitoring tests...")
        return self.run_command([
            "python", "backend/tests/test_setup.py"
        ], cwd=str(self.project_root))
    
    def run_all_tests(self):
        """Run all test categories"""
        logger.info("🚀 Starting comprehensive test suite...")
        
        test_categories = [
            ("Backend Unit Tests", self.run_backend_unit_tests),
            ("Backend Integration Tests", self.run_backend_integration_tests),
            ("Backend Security Tests", self.run_backend_security_tests),
            ("Backend ML/AI Tests", self.run_backend_ml_tests),
            ("Backend Linting", self.run_backend_lint),
            ("Backend Type Checking", self.run_backend_type_check),
            ("Backend Format Check", self.run_backend_format_check),
            ("Frontend Unit Tests", self.run_frontend_unit_tests),
            ("Frontend Type Check", self.run_frontend_type_check),
            ("Frontend Linting", self.run_frontend_lint),
            ("Frontend Build Test", self.run_frontend_build_test),
            ("Docker Build Test", self.run_docker_build_test),
            ("Database Migration Test", self.run_database_migration_test),
            ("API Tests", self.run_api_tests),
            ("Infrastructure Tests", self.run_infrastructure_tests),
            ("AI Service Tests", self.run_ai_service_tests),
            ("Monitoring Tests", self.run_monitoring_tests),
        ]
        
        # Add optional tests based on arguments
        if self.args.include_stress:
            test_categories.append(("Backend Stress Tests", self.run_backend_stress_tests))
        
        if self.args.include_chaos:
            test_categories.append(("Backend Chaos Tests", self.run_backend_chaos_tests))
        
        if self.args.include_load:
            test_categories.append(("Load Tests", self.run_load_tests))
        
        if self.args.include_security_scan:
            test_categories.append(("Security Vulnerability Scan", self.run_security_scan))
        
        if self.args.include_performance:
            test_categories.append(("Performance Tests", self.run_performance_tests))
        
        # Run tests
        for test_name, test_func in test_categories:
            if self.args.test_type and self.args.test_type.lower() not in test_name.lower():
                continue
                
            result = test_func()
            self.results.append(result)
            
            if result.status == 'passed':
                logger.info(f"✅ {test_name} PASSED ({result.duration:.2f}s)")
            else:
                logger.error(f"❌ {test_name} FAILED ({result.duration:.2f}s): {result.error_message}")
        
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.status == 'passed'])
        failed_tests = len([r for r in self.results if r.status == 'failed'])
        error_tests = len([r for r in self.results if r.status == 'error'])
        
        total_duration = time.time() - self.start_time
        
        # Calculate score
        score = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "errors": error_tests,
                "score": round(score, 2),
                "total_duration": round(total_duration, 2)
            },
            "results": [
                {
                    "test_type": r.test_type,
                    "test_name": r.test_name,
                    "status": r.status,
                    "duration": round(r.duration, 2),
                    "error_message": r.error_message
                }
                for r in self.results
            ]
        }
        
        # Save report
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        logger.info("\n" + "="*60)
        logger.info("📊 COMPREHENSIVE TEST REPORT")
        logger.info("="*60)
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"✅ Passed: {passed_tests}")
        logger.info(f"❌ Failed: {failed_tests}")
        logger.info(f"⚠️ Errors: {error_tests}")
        logger.info(f"📈 Score: {score:.1f}%")
        logger.info(f"⏱️ Total Duration: {total_duration:.2f}s")
        logger.info(f"📄 Report saved to: {report_file}")
        logger.info("="*60)
        
        # Print failed tests
        if failed_tests > 0 or error_tests > 0:
            logger.info("\n❌ FAILED TESTS:")
            for result in self.results:
                if result.status in ['failed', 'error']:
                    logger.error(f"  - {result.test_name}: {result.error_message}")
        
        # Exit with appropriate code
        if failed_tests > 0 or error_tests > 0:
            sys.exit(1)
        else:
            logger.info("🎉 All tests passed! Project is ready for production!")

def main():
    parser = argparse.ArgumentParser(description="Master Test Runner for CloudMind")
    parser.add_argument("--test-type", help="Run only tests containing this string")
    parser.add_argument("--include-stress", action="store_true", help="Include stress tests")
    parser.add_argument("--include-chaos", action="store_true", help="Include chaos engineering tests")
    parser.add_argument("--include-load", action="store_true", help="Include load tests")
    parser.add_argument("--include-security-scan", action="store_true", help="Include security vulnerability scan")
    parser.add_argument("--include-performance", action="store_true", help="Include performance tests")
    parser.add_argument("--quick", action="store_true", help="Run only essential tests")
    
    args = parser.parse_args()
    
    # Set up signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        logger.info("Received interrupt signal, shutting down gracefully...")
        sys.exit(1)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run tests
    runner = MasterTestRunner(args)
    runner.run_all_tests()

if __name__ == "__main__":
    main()
