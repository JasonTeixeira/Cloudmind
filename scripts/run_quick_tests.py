#!/usr/bin/env python3
"""
Quick Test Runner for CloudMind
Runs essential tests for rapid feedback during development
"""

import os
import sys
import time
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
    """Test result data class"""
    test_name: str
    status: str  # 'passed', 'failed', 'error'
    duration: float
    error_message: Optional[str] = None

class QuickTestRunner:
    """Quick test runner for essential tests only"""
    
    def __init__(self):
        self.results: List[TestResult] = []
        self.start_time = time.time()
        self.project_root = Path(__file__).parent.parent
        
    def run_command(self, command: List[str], test_name: str, cwd: Optional[str] = None) -> TestResult:
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
            
            stdout, stderr = process.communicate(timeout=300)
            duration = time.time() - start_time
            
            if process.returncode == 0:
                status = 'passed'
                error_message = None
            else:
                status = 'failed'
                error_message = stderr if stderr else stdout
            
            return TestResult(
                test_name=test_name,
                status=status,
                duration=duration,
                error_message=error_message
            )
            
        except subprocess.TimeoutExpired:
            process.kill()
            return TestResult(
                test_name=test_name,
                status='error',
                duration=300,
                error_message=f'Command timed out after 300 seconds'
            )
        except Exception as e:
            return TestResult(
                test_name=test_name,
                status='error',
                duration=time.time() - start_time,
                error_message=str(e)
            )
    
    def run_essential_tests(self):
        """Run only essential tests for quick feedback"""
        logger.info("🚀 Running essential tests for quick feedback...")
        
        # Essential backend tests
        essential_tests = [
            ("Backend Linting", ["python", "-m", "flake8", "backend/app", "--max-line-length=100"]),
            ("Backend Type Check", ["python", "-m", "mypy", "backend/app"]),
            ("Backend Format Check", ["python", "-m", "black", "--check", "backend/app"]),
            ("Backend Unit Tests (Core)", ["python", "-m", "pytest", "backend/tests/test_setup.py", "-v"]),
            ("Frontend Type Check", ["npm", "run", "type-check"], str(self.project_root / "frontend")),
            ("Frontend Linting", ["npm", "run", "lint"], str(self.project_root / "frontend")),
            ("Frontend Build Test", ["npm", "run", "build"], str(self.project_root / "frontend")),
        ]
        
        # Run tests
        for test_name, command in essential_tests:
            cwd = None
            if len(command) > 2 and command[0] == "npm":
                cwd = str(self.project_root / "frontend")
            
            logger.info(f"🔍 Running: {test_name}")
            result = self.run_command(command, test_name, cwd)
            self.results.append(result)
            
            if result.status == 'passed':
                logger.info(f"✅ {test_name} PASSED ({result.duration:.2f}s)")
            else:
                logger.error(f"❌ {test_name} FAILED ({result.duration:.2f}s): {result.error_message}")
        
        self.generate_report()
    
    def generate_report(self):
        """Generate quick test report"""
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.status == 'passed'])
        failed_tests = len([r for r in self.results if r.status == 'failed'])
        error_tests = len([r for r in self.results if r.status == 'error'])
        
        total_duration = time.time() - self.start_time
        score = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Print summary
        logger.info("\n" + "="*50)
        logger.info("📊 QUICK TEST REPORT")
        logger.info("="*50)
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"✅ Passed: {passed_tests}")
        logger.info(f"❌ Failed: {failed_tests}")
        logger.info(f"⚠️ Errors: {error_tests}")
        logger.info(f"📈 Score: {score:.1f}%")
        logger.info(f"⏱️ Total Duration: {total_duration:.2f}s")
        logger.info("="*50)
        
        # Print failed tests
        if failed_tests > 0 or error_tests > 0:
            logger.info("\n❌ FAILED TESTS:")
            for result in self.results:
                if result.status in ['failed', 'error']:
                    logger.error(f"  - {result.test_name}: {result.error_message}")
            logger.info("\n💡 Run 'python scripts/run_all_tests.py' for comprehensive testing")
        else:
            logger.info("🎉 All essential tests passed! Ready for development!")

def main():
    runner = QuickTestRunner()
    runner.run_essential_tests()

if __name__ == "__main__":
    main()
