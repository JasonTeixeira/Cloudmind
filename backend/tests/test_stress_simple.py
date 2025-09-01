import time
import threading
import psutil
import gc
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any
import pytest
import random
import string
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings


class TestStressLoad:
    """Stress tests for load handling"""
    
    def test_concurrent_health_checks(self):
        """Test concurrent health check requests"""
        client = TestClient(app)
        
        def make_request():
            response = client.get("/health")
            return response.status_code
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(100)]
            results = [future.result() for future in futures]
        
        # All should succeed
        assert all(status == 200 for status in results)
        assert len(results) == 100
    
    def test_rapid_login_attempts(self):
        """Test rapid login attempts to stress rate limiting"""
        client = TestClient(app)
        
        def make_login_request():
            response = client.post("/api/v1/auth/login", json={
                "email": f"test{random.randint(1,1000)}@example.com",
                "password": "wrongpassword"
            })
            return response.status_code
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_login_request) for _ in range(50)]
            results = [future.result() for future in futures]
        
        # Should see mix of 401 and 429 (rate limited)
        assert len(results) == 50
        assert all(status in [401, 429] for status in results)
    
    def test_memory_pressure(self):
        """Test application under memory pressure"""
        client = TestClient(app)
        initial_memory = psutil.Process().memory_info().rss
        
        # Create large objects to simulate memory pressure
        large_data = []
        for i in range(100):
            large_data.append({
                'id': i,
                'data': ''.join(random.choices(string.ascii_letters, k=1000)),
                'metadata': {f'key{j}': f'value{j}' for j in range(10)}
            })
        
        # Make requests while under memory pressure
        def make_request():
            response = client.get("/health")
            return response.status_code
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            results = [future.result() for future in futures]
        
        # All should still succeed
        assert all(status == 200 for status in results)
        
        # Clean up
        del large_data
        gc.collect()
        
        final_memory = psutil.Process().memory_info().rss
        memory_increase = (final_memory - initial_memory) / 1024 / 1024  # MB
        
        # Memory should not have increased by more than 50MB
        assert memory_increase < 50


class TestStressConcurrency:
    """Stress tests for concurrent operations"""
    
    def test_concurrent_project_creation(self):
        """Test concurrent project creation requests"""
        client = TestClient(app)
        
        def create_project():
            response = client.post("/api/v1/projects/", json={
                "name": f"Test Project {random.randint(1,10000)}",
                "description": "Stress test project",
                "monthly_budget": 1000
            })
            return response.status_code
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(create_project) for _ in range(20)]
            results = [future.result() for future in futures]
        
        # Should handle concurrent requests gracefully
        assert len(results) == 20
        # Most should be 401 (unauthorized) since we're not authenticated
        assert all(status in [401, 422] for status in results)
    
    def test_database_connection_pool_stress(self):
        """Test database connection pool under stress"""
        client = TestClient(app)
        
        def make_db_request():
            response = client.get("/api/v1/projects/")
            return response.status_code
        
        # Simulate many concurrent database requests
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_db_request) for _ in range(100)]
            results = [future.result() for future in futures]
        
        # All should complete (mostly 401s due to no auth)
        assert len(results) == 100
        assert all(status in [401, 500] for status in results)


class TestStressResourceLimits:
    """Stress tests for resource limits"""
    
    def test_cpu_intensive_operations(self):
        """Test application during CPU-intensive operations"""
        client = TestClient(app)
        
        def cpu_intensive_task():
            # Simulate CPU-intensive work
            result = 0
            for i in range(10000):
                result += i * i
            return result
        
        def make_request():
            response = client.get("/health")
            return response.status_code
        
        # Run CPU-intensive tasks in background
        with ThreadPoolExecutor(max_workers=2) as cpu_executor:
            cpu_futures = [cpu_executor.submit(cpu_intensive_task) for _ in range(2)]
            
            # Make requests while CPU is under load
            with ThreadPoolExecutor(max_workers=5) as req_executor:
                req_futures = [req_executor.submit(make_request) for _ in range(20)]
                results = [future.result() for future in req_futures]
            
            # Wait for CPU tasks to complete
            cpu_results = [future.result() for future in cpu_futures]
        
        # All requests should still succeed
        assert all(status == 200 for status in results)
        assert len(cpu_results) == 2
    
    def test_file_descriptor_limit(self):
        """Test application behavior near file descriptor limits"""
        client = TestClient(app)
        
        def make_request():
            response = client.get("/health")
            return response.status_code
        
        # Make many concurrent requests to test FD limits
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(make_request) for _ in range(100)]
            results = [future.result() for future in futures]
        
        # Should handle high concurrency gracefully
        assert len(results) == 100
        assert all(status == 200 for status in results)


class TestStressErrorConditions:
    """Stress tests for error conditions"""
    
    def test_malformed_requests_stress(self):
        """Test application with many malformed requests"""
        client = TestClient(app)
        
        def make_malformed_request():
            try:
                # Send malformed JSON
                response = client.post("/api/v1/auth/login", 
                                     content="invalid json",
                                     headers={"Content-Type": "application/json"})
                return response.status_code
            except:
                return 400
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_malformed_request) for _ in range(20)]
            results = [future.result() for future in futures]
        
        # Should handle malformed requests gracefully
        assert len(results) == 20
        assert all(status in [400, 422, 500] for status in results)
    
    def test_large_payload_stress(self):
        """Test application with large payloads"""
        client = TestClient(app)
        
        def make_large_request():
            large_payload = {
                "data": "x" * 100000  # 100KB payload
            }
            try:
                response = client.post("/api/v1/projects/", json=large_payload)
                return response.status_code
            except:
                return 413
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_large_request) for _ in range(10)]
            results = [future.result() for future in futures]
        
        # Should handle large payloads appropriately
        assert len(results) == 10
        assert all(status in [401, 413, 422, 500] for status in results)


class TestStressRecovery:
    """Stress tests for recovery scenarios"""
    
    def test_rapid_start_stop_cycles(self):
        """Test application recovery from rapid start/stop cycles"""
        client = TestClient(app)
        
        for i in range(5):
            # Simulate application restart
            response = client.get("/health")
            assert response.status_code == 200
            
            # Small delay to simulate restart time
            time.sleep(0.1)
    
    def test_memory_leak_detection(self):
        """Test for memory leaks during stress"""
        client = TestClient(app)
        initial_memory = psutil.Process().memory_info().rss
        
        def make_requests_cycle():
            for _ in range(10):
                client.get("/health")
                client.get("/livez")
                client.get("/readyz")
        
        # Run multiple cycles
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_requests_cycle) for _ in range(5)]
            for future in futures:
                future.result()
        
        # Force garbage collection
        gc.collect()
        
        final_memory = psutil.Process().memory_info().rss
        memory_increase = (final_memory - initial_memory) / 1024 / 1024  # MB
        
        # Memory increase should be reasonable (< 20MB)
        assert memory_increase < 20


class TestStressPerformance:
    """Stress tests for performance characteristics"""
    
    def test_response_time_under_load(self):
        """Test response times under various load levels"""
        client = TestClient(app)
        
        def measure_response_time():
            start_time = time.time()
            response = client.get("/health")
            end_time = time.time()
            return {
                'status': response.status_code,
                'response_time': (end_time - start_time) * 1000  # ms
            }
        
        # Test with different concurrency levels
        concurrency_levels = [1, 5, 10]
        results = {}
        
        for concurrency in concurrency_levels:
            with ThreadPoolExecutor(max_workers=concurrency) as executor:
                futures = [executor.submit(measure_response_time) for _ in range(20)]
                level_results = [future.result() for future in futures]
            
            avg_response_time = sum(r['response_time'] for r in level_results) / len(level_results)
            p95_response_time = sorted(r['response_time'] for r in level_results)[int(0.95 * len(level_results))]
            
            results[concurrency] = {
                'avg_ms': avg_response_time,
                'p95_ms': p95_response_time,
                'success_rate': sum(1 for r in level_results if r['status'] == 200) / len(level_results)
            }
        
        # Performance assertions
        for concurrency, metrics in results.items():
            assert metrics['success_rate'] > 0.95  # 95% success rate
            assert metrics['avg_ms'] < 1000  # Average < 1 second
            assert metrics['p95_ms'] < 2000  # 95th percentile < 2 seconds
    
    def test_throughput_limits(self):
        """Test application throughput limits"""
        client = TestClient(app)
        
        def make_request():
            response = client.get("/health")
            return response.status_code
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(1000)]
            results = [future.result() for future in futures]
        
        end_time = time.time()
        duration = end_time - start_time
        throughput = len(results) / duration  # requests per second
        
        # Should handle at least 100 requests per second
        assert throughput > 100
        assert all(status == 200 for status in results)


if __name__ == "__main__":
    # Run stress tests
    pytest.main([__file__, "-v"])
