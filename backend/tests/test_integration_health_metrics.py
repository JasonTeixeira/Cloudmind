from fastapi.testclient import TestClient

from app.main import app


def test_health_and_metrics_endpoints():
    client = TestClient(app)
    h = client.get("/health")
    assert h.status_code == 200
    m = client.get("/metrics")
    assert m.status_code == 200
    assert b"http_requests_total" in m.content or b"cloudmind_http_requests_total" in m.content


