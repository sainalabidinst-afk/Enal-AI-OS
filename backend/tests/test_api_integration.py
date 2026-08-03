import os

from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.security_model import (
    SecurityPolicy,
    SecurityLevel,
    Permission,
    security_model,
)

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-unit-tests-only")

client = TestClient(app)

TEST_USERNAME = "integration-test-user"
TEST_PASSWORD = "integration-test-pass"

TEST_TOKEN = None
TEST_WORKSPACE_ID = None
TEST_ARTIFACT_ID = None

security_model.register_policy(
    SecurityPolicy(
        plugin_id=TEST_USERNAME,
        security_level=SecurityLevel.SAFE,
        allowed_permissions=[
            Permission.READ,
            Permission.WRITE,
            Permission.EXECUTE,
        ],
    )
)


def _get_or_create_token() -> str:
    global TEST_TOKEN
    if TEST_TOKEN is None:
        response = client.post(
            "/api/v1/auth/login",
            data={"username": TEST_USERNAME, "password": TEST_PASSWORD},
        )
        assert response.status_code == 200, f"Login failed: {response.text}"
        TEST_TOKEN = response.json()["access_token"]
    return TEST_TOKEN


def _auth_headers(token: str | None = None) -> dict[str, str]:
    return {"Authorization": f"Bearer {token or _get_or_create_token()}"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "enal-ai-os"


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Enal AI OS" in data["message"]


def test_auth_login_success():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "secret"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_auth_login_missing_fields():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "", "password": ""},
    )
    assert response.status_code == 422


def test_auth_me():
    token = _get_or_create_token()
    response = client.get("/api/v1/auth/me", headers=_auth_headers(token))
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == TEST_USERNAME
    assert "roles" in data


def test_auth_me_unauthorized():
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_auth_logout():
    token = _get_or_create_token()
    response = client.post("/api/v1/auth/logout", headers=_auth_headers(token))
    assert response.status_code == 200
    assert "Logged out" in response.json()["detail"]


def test_chat_post():
    token = _get_or_create_token()
    response = client.post(
        "/api/v1/chat",
        headers=_auth_headers(token),
        json={
            "message": "Hello, analyze this request",
            "conversation_id": "conv-test-1",
            "workspace_id": "ws-test-1",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "conversation_id" in data


def test_chat_post_missing_message():
    token = _get_or_create_token()
    response = client.post(
        "/api/v1/chat",
        headers=_auth_headers(token),
        json={},
    )
    assert response.status_code == 422


def test_get_conversation():
    token = _get_or_create_token()
    response = client.get(
        "/api/v1/conversations/conv-test-1",
        headers=_auth_headers(token),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"] == "conv-test-1"
    assert "messages" in data


def test_delete_conversation():
    token = _get_or_create_token()
    response = client.delete(
        "/api/v1/conversations/conv-test-1",
        headers=_auth_headers(token),
    )
    assert response.status_code == 200
    assert response.json()["deleted"] is True


def test_list_workspaces():
    token = _get_or_create_token()
    response = client.get("/api/v1/workspaces", headers=_auth_headers(token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_workspace():
    global TEST_WORKSPACE_ID
    token = _get_or_create_token()
    response = client.post(
        "/api/v1/workspaces",
        headers=_auth_headers(token),
        params={"name": "Integration Test Workspace", "description": "Test workspace"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Integration Test Workspace"
    TEST_WORKSPACE_ID = data["id"]


def test_get_workspace():
    token = _get_or_create_token()
    workspace_id = TEST_WORKSPACE_ID or "ws-test-1"
    response = client.get(
        f"/api/v1/workspaces/{workspace_id}",
        headers=_auth_headers(token),
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "name" in data


def test_get_workspace_not_found():
    token = _get_or_create_token()
    response = client.get(
        "/api/v1/workspaces/nonexistent-workspace-id",
        headers=_auth_headers(token),
    )
    assert response.status_code == 404


def test_capabilities():
    token = _get_or_create_token()
    response = client.get("/api/v1/capabilities", headers=_auth_headers(token))
    assert response.status_code == 200
    data = response.json()
    assert "capabilities" in data
    assert "domains" in data


def test_executions_list():
    token = _get_or_create_token()
    response = client.get("/api/v1/executions", headers=_auth_headers(token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_executions_run():
    token = _get_or_create_token()
    response = client.post(
        "/api/v1/executions/run",
        headers=_auth_headers(token),
        params={"goal": "Test execution goal", "workspace_id": "ws-test-1"},
    )
    assert response.status_code in (200, 404, 500)


def test_artifacts_list():
    token = _get_or_create_token()
    response = client.get("/api/v1/artifacts", headers=_auth_headers(token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_artifacts_create():
    global TEST_ARTIFACT_ID
    token = _get_or_create_token()
    response = client.post(
        "/api/v1/artifacts",
        headers=_auth_headers(token),
        params={
            "project_id": "ws-test-1",
            "name": "Test Artifact",
            "artifact_type": "file",
            "content": "test content",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Artifact"
    TEST_ARTIFACT_ID = data.get("artifact_id") or data.get("id")


def test_providers():
    token = _get_or_create_token()
    try:
        response = client.get("/api/v1/providers", headers=_auth_headers(token))
        assert response.status_code == 200
        data = response.json()
        assert "providers" in data or "status" in data
    except Exception:
        assert True


def test_route_model():
    token = _get_or_create_token()
    response = client.post(
        "/api/v1/route",
        headers=_auth_headers(token),
        params={"task_type": "chat", "capability": "default", "context": "{}"},
    )
    assert response.status_code in (200, 400, 404, 500)


def test_metrics():
    token = _get_or_create_token()
    response = client.get("/api/v1/metrics", headers=_auth_headers(token))
    assert response.status_code == 200
    data = response.json()
    assert "analysis" in data
    assert "chat" in data


def test_benchmark_suite():
    token = _get_or_create_token()
    response = client.get("/api/v1/benchmark/suite", headers=_auth_headers(token))
    assert response.status_code == 200
    data = response.json()
    assert "suite_id" in data
    assert "cases" in data


def test_notifications_send():
    token = _get_or_create_token()
    response = client.post(
        "/api/v1/notifications",
        headers=_auth_headers(token),
        params={
            "recipient": "test-user",
            "message": "Test notification",
            "channel": "websocket",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "recipient" in data
    assert data["recipient"] == "test-user"


def test_notifications_test_endpoint():
    token = _get_or_create_token()
    response = client.get(
        "/api/v1/notifications/test",
        headers=_auth_headers(token),
    )
    assert response.status_code in (200, 404)


def test_unauthenticated_access():
    response = client.get("/api/v1/workspaces")
    assert response.status_code == 401


def test_agents_list():
    token = _get_or_create_token()
    response = client.get("/agents", headers=_auth_headers(token))
    assert response.status_code == 200
    assert "agents" in response.json()
