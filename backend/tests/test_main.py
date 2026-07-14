from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/")
    assert response.status_code == 200
    assert "Enal AI OS" in response.json()["message"]

def test_agents_list():
    response = client.get("/api/v1/agents")
    assert response.status_code == 200
    assert "agents" in response.json()
