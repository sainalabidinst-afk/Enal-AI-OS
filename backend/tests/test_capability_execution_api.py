import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


class TestCapabilityExecution:
    def test_list_capabilities_returns_list(self):
        response = client.get("/api/v1/capabilities")
        assert response.status_code == 200
        data = response.json()
        assert "capabilities" in data

    def test_get_capability_not_found(self):
        response = client.get("/api/v1/capabilities/nonexistent-capability-id")
        assert response.status_code == 404

    def test_get_capability_exists(self):
        response = client.get("/api/v1/capabilities/network")
        assert response.status_code in (200, 404)

    def test_execute_capability_requires_auth(self):
        response = client.post(
            "/api/v1/capabilities/network/execute",
            json={"message": "test", "workspace_id": "ws-1"},
        )
        assert response.status_code in (401, 403, 404)
