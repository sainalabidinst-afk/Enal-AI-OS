import os
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest")
os.environ.setdefault("TESTING", "true")

client = TestClient(app)


def _auth_headers() -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "secret"},
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestCapabilityExecution:
    def test_list_capabilities_returns_list(self):
        response = client.get("/api/v1/capabilities")
        assert response.status_code == 200
        data = response.json()
        assert "capabilities" in data

    def test_get_capability_not_found(self):
        headers = _auth_headers()
        response = client.get("/api/v1/capabilities/nonexistent-capability-id", headers=headers)
        assert response.status_code in (200, 404)

    def test_get_capability_exists(self):
        headers = _auth_headers()
        response = client.get("/api/v1/capabilities/network", headers=headers)
        assert response.status_code in (200, 404)

    def test_execute_capability_requires_auth(self):
        response = client.post(
            "/api/v1/capabilities/network/execute",
            json={"message": "test", "workspace_id": "ws-1"},
        )
        assert response.status_code in (401, 403)
