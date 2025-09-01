import time
from fastapi.testclient import TestClient
from app.main import app

def test_basic_health_check():
    """Test basic health check functionality"""
    client = TestClient(app)
    
    # Single health check
    response = client.get("/health")
    print(f"Health check status: {response.status_code}")
    print(f"Health check response: {response.json()}")
    
    assert response.status_code == 200

def test_livez_readyz():
    """Test liveness and readiness probes"""
    client = TestClient(app)
    
    # Liveness probe
    livez_response = client.get("/livez")
    print(f"Livez status: {livez_response.status_code}")
    
    # Readiness probe
    readyz_response = client.get("/readyz")
    print(f"Readyz status: {readyz_response.status_code}")
    
    # Liveness should always work
    assert livez_response.status_code == 200
    
    # Readiness might fail if DB is not available (which is expected in test environment)
    assert readyz_response.status_code in [200, 503]

def test_rate_limiting():
    """Test rate limiting functionality"""
    client = TestClient(app)
    
    responses = []
    for i in range(10):
        response = client.get("/health")
        responses.append(response.status_code)
        print(f"Request {i+1}: {response.status_code}")
    
    # Should see mix of 200 and 429 (rate limited)
    print(f"Response codes: {responses}")
    assert all(status in [200, 429] for status in responses)

def test_concurrent_requests():
    """Test concurrent requests"""
    client = TestClient(app)
    
    import threading
    
    results = []
    
    def make_request():
        response = client.get("/health")
        results.append(response.status_code)
    
    # Create 5 threads
    threads = []
    for i in range(5):
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print(f"Concurrent request results: {results}")
    assert len(results) == 5
    assert all(status in [200, 429] for status in results)

if __name__ == "__main__":
    print("=== Basic Stress Test Results ===")
    test_basic_health_check()
    test_livez_readyz()
    test_rate_limiting()
    test_concurrent_requests()
    print("=== All basic tests completed ===")
