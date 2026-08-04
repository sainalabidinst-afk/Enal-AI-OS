import os

os.environ["SECRET_KEY"] = "test-secret-key-for-unit-tests-only"
os.environ["TESTING"] = "true"

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/")
    assert response.status_code == 200
    assert "Enal AI OS" in response.json()["message"]


def test_agents_list():
    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "test", "password": "test"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    response = client.get("/agents", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "agents" in response.json()


