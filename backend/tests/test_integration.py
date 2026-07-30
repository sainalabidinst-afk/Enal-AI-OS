from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_integration_health():
    response = client.get("/api/v1/integration/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["module"] == "capability_integration"
    assert "trading_analysis_with_knowledge" in data["workflows"]
    assert "network_design_review_with_knowledge" in data["workflows"]
    assert "self_improvement_cycle" in data["workflows"]
