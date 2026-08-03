import os

from fastapi.testclient import TestClient
from backend.app.main import app

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-unit-tests-only")

# Re-import settings after env is set so SECRET_KEY is picked up.
from backend.app.core.config import settings
assert settings.SECRET_KEY, "SECRET_KEY must be configured for integration tests"

from backend.app.api.auth import _create_access_token

client = TestClient(app)


def _auth_headers() -> dict[str, str]:
    token = _create_access_token({"sub": "test-user", "roles": ["default"], "permissions": ["default"]})
    return {"Authorization": f"Bearer {token}"}


def test_integration_health():
    response = client.get("/api/v1/integration/health", headers=_auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["module"] == "capability_integration"
    assert "trading_analysis_with_knowledge" in data["workflows"]
    assert "network_design_review_with_knowledge" in data["workflows"]
    assert "self_improvement_cycle" in data["workflows"]
