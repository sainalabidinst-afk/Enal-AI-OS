import os

from fastapi.testclient import TestClient
from backend.app.main import app

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-unit-tests-only")

client = TestClient(app)

def test_health():
    response = client.get("/")
    assert response.status_code == 200
    assert "Enal AI OS" in response.json()["message"]

def test_agents_list():
    response = client.get("/agents", headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 200
    assert "agents" in response.json()
