#!/usr/bin/env python3
"""
Comprehensive Test Runner for CloudMind
Executes unit tests, integration tests, stress tests, and chaos engineering tests
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

# Add the backend directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

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

class ComprehensiveTestRunner:
    """Comprehensive test runner for all test types"""
    
    def __init__(self, args):
        self.args = args
        self.results: List[TestResult] = []
        self.start_time = time.time()
        self.test_processes: List[subprocess.Popen] = []
        
    def run_command(self, command: List[str], timeout: int = 300) -> TestResult:
        """Run a command and capture the result"""
        start_time = time.time()
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(Path(__file__).parent.parent)
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
    
    def run_unit_tests(self) -> TestResult:
        """Run unit tests with pytest"""
        print("🔬 Running unit tests...")
        
        command = [
            'python3', '-m', 'pytest',
            'tests/',
            '-v',
            '--tb=short',
            '--maxfail=5',
            '--durations=10'
        ]
        
        if self.args.coverage:
            command.extend(['--cov=app', '--cov-report=html', '--cov-report=term'])
        
        return self.run_command(command, timeout=600)
    
    def run_stress_tests(self) -> TestResult:
        """Run stress tests"""
        print("💪 Running stress tests...")
        
        command = [
            'python3', '-m', 'pytest',
            'tests/test_stress.py',
            '-v',
            '--tb=short',
            '-x'  # Stop on first failure
        ]
        
        return self.run_command(command, timeout=900)
    
    def run_chaos_tests(self) -> TestResult:
        """Run chaos engineering tests"""
        print("🌪️ Running chaos engineering tests...")
        
        command = [
            'python3', '-m', 'pytest',
            'tests/test_chaos.py',
            '-v',
            '--tb=short',
            '-x'  # Stop on first failure
        ]
        
        return self.run_command(command, timeout=600)
    
    def run_security_tests(self) -> TestResult:
        """Run security tests"""
        print("🔒 Running security tests...")
        
        command = [
            'python3', '-m', 'pytest',
            'tests/test_security.py',
            '-v',
            '--tb=short'
        ]
        
        return self.run_command(command, timeout=300)
    
    def run_integration_tests(self) -> TestResult:
        """Run integration tests"""
        print("🔗 Running integration tests...")
        
        command = [
            'python3', '-m', 'pytest',
            'tests/test_main.py',
            'tests/test_phase*.py',
            '-v',
            '--tb=short'
        ]
        
        return self.run_command(command, timeout=600)
    
    def run_k6_load_test(self) -> TestResult:
        """Run k6 load testing"""
        print("🚀 Running k6 load tests...")
        
        # Check if k6 is installed
        try:
            subprocess.run(['k6', 'version'], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return TestResult(
                test_type='k6_load',
                test_name='k6 load test',
                status='skipped',
                duration=0,
                output='k6 not installed. Install from https://k6.io/docs/getting-started/installation/',
                error_message='k6 not found'
            )
        
        # Run k6 test
        command = [
            'k6', 'run',
            '--out', 'json=results/k6-results.json',
            '--out', 'influxdb=http://localhost:8086/k6',
            'tests/k6_load_test.js'
        ]
        
        return self.run_command(command, timeout=1800)  # 30 minutes
    
    def run_performance_tests(self) -> TestResult:
        """Run performance tests"""
        print("⚡ Running performance tests...")
        
        # Start the application for performance testing
        app_process = None
        try:
            # Start the application
            app_process = subprocess.Popen(
                ['python3', '-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for app to start
            time.sleep(10)
            
            # Run performance tests
            command = [
                'python3', '-m', 'pytest',
                'tests/test_stress.py::TestStressPerformance',
                '-v',
                '--tb=short'
            ]
            
            result = self.run_command(command, timeout=300)
            
            return result
            
        finally:
            if app_process:
                app_process.terminate()
                app_process.wait()
    
    def run_memory_tests(self) -> TestResult:
        """Run memory leak detection tests"""
        print("🧠 Running memory tests...")
        
        command = [
            'python3', '-m', 'pytest',
            'tests/test_stress.py::TestStressRecovery::test_memory_leak_detection',
            '-v',
            '--tb=short'
        ]
        
        return self.run_command(command, timeout=300)
    
    def run_concurrency_tests(self) -> TestResult:
        """Run concurrency tests"""
        print("🔄 Running concurrency tests...")
        
        command = [
            'python3', '-m', 'pytest',
            'tests/test_stress.py::TestStressConcurrency',
            '-v',
            '--tb=short'
        ]
        
        return self.run_command(command, timeout=600)
    
    def run_system_health_check(self) -> TestResult:
        """Run system health check"""
        print("🏥 Running system health check...")
        
        # Check system resources
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        metrics = {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available_gb': memory.available / (1024**3),
            'disk_percent': disk.percent,
            'disk_free_gb': disk.free / (1024**3)
        }
        
        # Check if system is healthy
        is_healthy = (
            cpu_percent < 90 and
            memory.percent < 90 and
            disk.percent < 90
        )
        
        status = 'passed' if is_healthy else 'failed'
        error_message = None if is_healthy else f"System resources: CPU {cpu_percent}%, Memory {memory.percent}%, Disk {disk.percent}%"
        
        return TestResult(
            test_type='system_health',
            test_name='System health check',
            status=status,
            duration=1.0,
            output=f"CPU: {cpu_percent}%, Memory: {memory.percent}%, Disk: {disk.percent}%",
            error_message=error_message,
            metrics=metrics
        )
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test suites"""
        print("🚀 Starting comprehensive test suite...")
        print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Create results directory
        results_dir = Path('results')
        results_dir.mkdir(exist_ok=True)
        
        # System health check
        self.results.append(self.run_system_health_check())
        
        # Unit tests
        self.results.append(self.run_unit_tests())
        
        # Integration tests
        self.results.append(self.run_integration_tests())
        
        # Security tests
        self.results.append(self.run_security_tests())
        
        # Stress tests
        self.results.append(self.run_stress_tests())
        
        # Chaos tests
        self.results.append(self.run_chaos_tests())
        
        # Concurrency tests
        self.results.append(self.run_concurrency_tests())
        
        # Memory tests
        self.results.append(self.run_memory_tests())
        
        # Performance tests
        self.results.append(self.run_performance_tests())
        
        # k6 load tests (if requested)
        if self.args.load_test:
            self.results.append(self.run_k6_load_test())
        
        # Generate summary
        return self.generate_summary()
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate test summary"""
        total_duration = time.time() - self.start_time
        
        # Count results by status
        status_counts = {}
        for result in self.results:
            status_counts[result.status] = status_counts.get(result.status, 0) + 1
        
        # Calculate success rate
        total_tests = len(self.results)
        passed_tests = status_counts.get('passed', 0)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Collect metrics
        all_metrics = {}
        for result in self.results:
            if result.metrics:
                all_metrics[result.test_name] = result.metrics
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_duration_seconds': total_duration,
            'total_tests': total_tests,
            'status_counts': status_counts,
            'success_rate_percent': success_rate,
            'results': [
                {
                    'test_type': r.test_type,
                    'test_name': r.test_name,
                    'status': r.status,
                    'duration': r.duration,
                    'error_message': r.error_message,
                    'metrics': r.metrics
                }
                for r in self.results
            ],
            'metrics': all_metrics
        }
        
        return summary
    
    def print_summary(self, summary: Dict[str, Any]):
        """Print test summary"""
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("="*80)
        
        print(f"⏱️  Total Duration: {summary['total_duration_seconds']:.2f} seconds")
        print(f"🧪 Total Tests: {summary['total_tests']}")
        print(f"✅ Success Rate: {summary['success_rate_percent']:.1f}%")
        
        print("\n📈 Status Breakdown:")
        for status, count in summary['status_counts'].items():
            emoji = {
                'passed': '✅',
                'failed': '❌',
                'skipped': '⏭️',
                'error': '💥'
            }.get(status, '❓')
            print(f"  {emoji} {status.capitalize()}: {count}")
        
        print("\n🔍 Detailed Results:")
        for result in summary['results']:
            emoji = {
                'passed': '✅',
                'failed': '❌',
                'skipped': '⏭️',
                'error': '💥'
            }.get(result['status'], '❓')
            
            print(f"  {emoji} {result['test_name']} ({result['test_type']}) - {result['status']} ({result['duration']:.2f}s)")
            
            if result['error_message']:
                print(f"     💬 {result['error_message'][:100]}...")
        
        # System metrics
        if 'metrics' in summary and summary['metrics']:
            print("\n💻 System Metrics:")
            for test_name, metrics in summary['metrics'].items():
                if 'cpu_percent' in metrics:
                    print(f"  🖥️  {test_name}: CPU {metrics['cpu_percent']:.1f}%, "
                          f"Memory {metrics.get('memory_percent', 0):.1f}%, "
                          f"Disk {metrics.get('disk_percent', 0):.1f}%")
        
        # Overall assessment
        print("\n🎯 Overall Assessment:")
        if summary['success_rate_percent'] >= 95:
            print("  🏆 EXCELLENT - System is highly reliable and robust!")
        elif summary['success_rate_percent'] >= 85:
            print("  👍 GOOD - System is reliable with minor issues")
        elif summary['success_rate_percent'] >= 70:
            print("  ⚠️  FAIR - System has some reliability concerns")
        else:
            print("  🚨 POOR - System has significant reliability issues")
        
        print("="*80)
    
    def save_results(self, summary: Dict[str, Any]):
        """Save test results to file"""
        results_file = Path('results') / f"comprehensive-test-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        
        with open(results_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"💾 Results saved to: {results_file}")
    
    def cleanup(self):
        """Cleanup test processes"""
        for process in self.test_processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()

def signal_handler(signum, frame):
    """Handle interrupt signals"""
    print("\n🛑 Received interrupt signal. Cleaning up...")
    sys.exit(1)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Comprehensive Test Runner for CloudMind')
    parser.add_argument('--load-test', action='store_true', help='Include k6 load testing')
    parser.add_argument('--coverage', action='store_true', help='Generate coverage reports')
    parser.add_argument('--save-results', action='store_true', help='Save detailed results to file')
    parser.add_argument('--quick', action='store_true', help='Run only essential tests')
    
    args = parser.parse_args()
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    runner = ComprehensiveTestRunner(args)
    
    try:
        # Run tests
        summary = runner.run_all_tests()
        
        # Print summary
        runner.print_summary(summary)
        
        # Save results if requested
        if args.save_results:
            runner.save_results(summary)
        
        # Exit with appropriate code
        if summary['success_rate_percent'] >= 85:
            print("🎉 Tests completed successfully!")
            sys.exit(0)
        else:
            print("⚠️  Tests completed with issues!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)
    finally:
        runner.cleanup()

if __name__ == '__main__':
    main()
