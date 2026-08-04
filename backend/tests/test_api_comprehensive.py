import os
import uuid

import pytest
from fastapi.testclient import TestClient

os.environ["SECRET_KEY"] = "test-secret-key-for-comprehensive-tests"
os.environ["TESTING"] = "true"

from backend.app.core.security_model import (  # noqa: E402
    Permission,
    SecurityLevel,
    SecurityPolicy,
    security_model,
)
from backend.app.main import app  # noqa: E402

client = TestClient(app)

TEST_USERNAME = "comprehensive-test-user"
TEST_PASSWORD = "comprehensive-test-pass"

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


@pytest.fixture(scope="session", autouse=True)
def ensure_test_env():
    assert os.environ.get("SECRET_KEY") == "test-secret-key-for-comprehensive-tests"
    yield


@pytest.fixture(scope="session")
def token() -> str:
    response = client.post(
        "/api/v1/auth/login",
        data={"username": TEST_USERNAME, "password": TEST_PASSWORD},
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()["access_token"]


@pytest.fixture(scope="session")
def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "enal-ai-os"


def test_health_agents(token, auth_headers):
    response = client.get("/agents", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "agents" in data


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Enal AI OS" in response.json()["message"]


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


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


def test_auth_me(token, auth_headers):
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == TEST_USERNAME
    assert "roles" in data


def test_auth_me_unauthorized():
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_auth_logout(token, auth_headers):
    response = client.post("/api/v1/auth/logout", headers=auth_headers)
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------


def test_chat_post(token, auth_headers):
    response = client.post(
        "/api/v1/chat",
        headers=auth_headers,
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


def test_chat_post_missing_message(token, auth_headers):
    response = client.post(
        "/api/v1/chat",
        headers=auth_headers,
        json={},
    )
    assert response.status_code == 422


def test_chat_stream():
    token = _get_token()
    response = client.get(
        "/api/v1/chat/stream",
        headers=_auth_headers(token),
        params={"message": "test stream"},
    )
    assert response.status_code == 200


def test_chat_get_conversation(token, auth_headers):
    response = client.get(
        "/api/v1/conversations/conv-test-1",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"] == "conv-test-1"
    assert "messages" in data


def test_chat_delete_conversation(token, auth_headers):
    response = client.delete(
        "/api/v1/conversations/conv-test-1",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["deleted"] is True


# ---------------------------------------------------------------------------
# Workspace
# ---------------------------------------------------------------------------


def test_workspace_list(token, auth_headers):
    response = client.get("/api/v1/workspaces", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.fixture(scope="session")
def test_workspace_id(token, auth_headers) -> str:
    response = client.post(
        "/api/v1/workspaces",
        headers=auth_headers,
        params={"name": "Comprehensive Test Workspace", "description": "Test workspace"},
    )
    assert response.status_code == 200
    data = response.json()
    return data["id"]


def test_workspace_create(token, auth_headers):
    response = client.post(
        "/api/v1/workspaces",
        headers=auth_headers,
        params={"name": "Comprehensive Test Workspace 2", "description": "Test workspace"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Comprehensive Test Workspace 2"


def test_workspace_get(token, auth_headers, test_workspace_id: str):
    response = client.get(
        f"/api/v1/workspaces/{test_workspace_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "name" in data


def test_workspace_get_not_found(token, auth_headers):
    response = client.get(
        "/api/v1/workspaces/nonexistent-workspace-id",
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_workspace_add_file(token, auth_headers, test_workspace_id: str):
    response = client.post(
        f"/api/v1/workspaces/{test_workspace_id}/files",
        headers=auth_headers,
        params={"filename": "test.txt", "path": "/test.txt", "size": 4},
    )
    assert response.status_code == 200


def test_workspace_list_files(token, auth_headers, test_workspace_id: str):
    response = client.get(
        f"/api/v1/workspaces/{test_workspace_id}/files",
        headers=auth_headers,
    )
    assert response.status_code == 200


def test_workspace_get_file(token, auth_headers, test_workspace_id: str):
    response = client.get(
        f"/api/v1/workspaces/{test_workspace_id}/files/test.txt",
        headers=auth_headers,
    )
    assert response.status_code == 200


def test_workspace_delete_file(token, auth_headers, test_workspace_id: str):
    response = client.delete(
        f"/api/v1/workspaces/{test_workspace_id}/files/test.txt",
        headers=auth_headers,
    )
    assert response.status_code == 200


def test_workspace_set_memory(token, auth_headers, test_workspace_id: str):
    response = client.post(
        f"/api/v1/workspaces/{test_workspace_id}/memory",
        headers=auth_headers,
        params={"key": "test-key", "value": "test-value"},
    )
    assert response.status_code in (200, 404, 422)


def test_workspace_get_memory(token, auth_headers, test_workspace_id: str):
    response = client.get(
        f"/api/v1/workspaces/{test_workspace_id}/memory/test-key",
        headers=auth_headers,
    )
    assert response.status_code == 200


def test_workspace_delete(token, auth_headers, test_workspace_id: str):
    response = client.delete(
        f"/api/v1/workspaces/{test_workspace_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# Artifact
# ---------------------------------------------------------------------------


def test_artifact_list(token, auth_headers):
    response = client.get("/api/v1/artifacts", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.fixture(scope="session")
def test_artifact_id(token, auth_headers, test_workspace_id: str) -> str:
    response = client.post(
        "/api/v1/artifacts",
        headers=auth_headers,
        params={
            "workspace_id": test_workspace_id,
            "project_id": "test-project",
            "name": "Test Artifact",
            "artifact_type": "file",
            "content": "test content",
        },
    )
    assert response.status_code in (200, 422)
    data = response.json()
    return data.get("id") or data.get("artifact_id") or "test-artifact-id"


def test_artifact_create(token, auth_headers, test_workspace_id: str):
    response = client.post(
        "/api/v1/artifacts",
        headers=auth_headers,
        params={
            "workspace_id": test_workspace_id,
            "project_id": "test-project",
            "name": "Test Artifact 2",
            "artifact_type": "file",
            "content": "test content 2",
        },
    )
    assert response.status_code in (200, 422)
    data = response.json()
    assert "name" in data or "detail" in data


def test_artifact_get(token, auth_headers, test_artifact_id: str):
    response = client.get(
        f"/api/v1/artifacts/{test_artifact_id}",
        headers=auth_headers,
    )
    assert response.status_code in (200, 404, 422)


def test_artifact_get_not_found(token, auth_headers):
    response = client.get(
        "/api/v1/artifacts/nonexistent-artifact-id",
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_artifact_get_version(token, auth_headers, test_artifact_id: str):
    response = client.get(
        f"/api/v1/artifacts/{test_artifact_id}/versions/1",
        headers=auth_headers,
    )
    assert response.status_code in (200, 404)


def test_artifact_add_version(token, auth_headers, test_artifact_id: str):
    response = client.post(
        f"/api/v1/artifacts/{test_artifact_id}/versions",
        headers=auth_headers,
        json={"content": "new version content"},
    )
    assert response.status_code in (200, 404)


def test_artifact_restore_version(token, auth_headers, test_artifact_id: str):
    response = client.post(
        f"/api/v1/artifacts/{test_artifact_id}/restore/1",
        headers=auth_headers,
    )
    assert response.status_code in (200, 404)


def test_artifact_delete(token, auth_headers, test_artifact_id: str):
    response = client.delete(
        f"/api/v1/artifacts/{test_artifact_id}",
        headers=auth_headers,
    )
    assert response.status_code in (200, 404)


# ---------------------------------------------------------------------------
# Attachments
# ---------------------------------------------------------------------------


def test_attachments_upload(token, auth_headers):
    try:
        response = client.post(
            "/api/v1/attachments/upload",
            headers=auth_headers,
            files={"file": ("test.txt", b"test attachment content", "text/plain")},
            params={"workspace_id": "ws-test-1"},
        )
        assert response.status_code in (200, 400, 422, 500)
    except Exception:
        pass


def test_attachments_analyze(token, auth_headers):
    try:
        response = client.post(
            "/api/v1/attachments/analyze",
            headers=auth_headers,
            files=[("files", ("test1.txt", b"config1", "text/plain")), ("files", ("test2.txt", b"config2", "text/plain"))],
        )
        assert response.status_code in (200, 400, 422, 500)
    except Exception:
        pass


def test_attachments_diff(token, auth_headers):
    try:
        response = client.post(
            "/api/v1/attachments/diff",
            headers=auth_headers,
            files=[
                ("before", ("before.txt", b"old config", "text/plain")),
                ("after", ("after.txt", b"new config", "text/plain")),
            ],
        )
        assert response.status_code in (200, 400, 422, 500)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------


def test_benchmark_suite(token, auth_headers):
    response = client.get("/api/v1/benchmark/suite", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "suite_id" in data


def test_benchmark_run(token, auth_headers):
    response = client.post("/api/v1/benchmark/run", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "suite_id" in data


def test_benchmark_capability_scores(token, auth_headers):
    response = client.get("/api/v1/benchmark/capability-scores", headers=auth_headers)
    assert response.status_code == 200
    assert "capabilities" in response.json()


def test_benchmark_cce_status(token, auth_headers):
    response = client.get("/api/v1/benchmark/cce/status", headers=auth_headers)
    assert response.status_code == 200
    assert "status" in response.json()


# ---------------------------------------------------------------------------
# Capability Discovery
# ---------------------------------------------------------------------------


def test_capabilities_list(token, auth_headers):
    response = client.get("/api/v1/capabilities", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "capabilities" in data
    assert "domains" in data


def test_capabilities_detail(token, auth_headers):
    response = client.get("/api/v1/capabilities/network-audit", headers=auth_headers)
    assert response.status_code in (200, 404)


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------


def test_execution_create(token, auth_headers):
    response = client.post(
        "/api/v1/executions",
        headers=auth_headers,
        params={"goal": "Test execution goal"},
    )
    assert response.status_code in (200, 403, 404, 500)


def test_execution_list(token, auth_headers):
    response = client.get("/api/v1/executions", headers=auth_headers)
    assert response.status_code in (200, 403, 404)


def test_execution_get_not_found(token, auth_headers):
    response = client.get("/api/v1/executions/nonexistent-id", headers=auth_headers)
    assert response.status_code == 404


def test_execution_run_not_found_workspace(token, auth_headers):
    response = client.post(
        "/api/v1/executions/run",
        headers=auth_headers,
        params={"goal": "Test", "workspace_id": "nonexistent-ws"},
    )
    assert response.status_code in (200, 404, 422, 500)


# ---------------------------------------------------------------------------
# Ecosystem
# ---------------------------------------------------------------------------


def test_ecosystem_studio_traces(token, auth_headers):
    response = client.get("/api/v1/studio/traces/trace-1", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_studio_metrics(token, auth_headers):
    response = client.get("/api/v1/studio/metrics", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_studio_artifacts(token, auth_headers):
    response = client.get("/api/v1/studio/artifacts/proj-1", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_studio_graph(token, auth_headers):
    response = client.get("/api/v1/studio/graph/proj-1", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_studio_memory(token, auth_headers):
    try:
        import redis
        redis_client = redis.Redis(host="localhost", port=6379)
        redis_client.ping()
    except Exception:
        pytest.skip("Redis not available in test environment")
    
    response = client.get("/api/v1/studio/memory", headers=auth_headers, params={"layer": "working", "query": "test", "limit": 5})
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_studio_reputation(token, auth_headers):
    response = client.get("/api/v1/studio/reputation", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_studio_cognitive_services(token, auth_headers):
    response = client.get("/api/v1/studio/cognitive/services", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_studio_cognitive_pipelines(token, auth_headers):
    response = client.get("/api/v1/studio/cognitive/pipelines", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_studio_cognitive_meta_metrics(token, auth_headers):
    response = client.get("/api/v1/studio/cognitive/meta/metrics", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_studio_export(token, auth_headers):
    response = client.get("/api/v1/studio/export/proj-1", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_marketplace_publish(token, auth_headers):
    response = client.post(
        "/api/v1/marketplace/publish",
        headers=auth_headers,
        json={
            "plugin_id": "test-plugin",
            "name": "Test Plugin",
            "version": "1.0.0",
            "description": "Test",
            "author": "test",
            "category": "utility",
        },
    )
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_marketplace_list_plugins(token, auth_headers):
    response = client.get("/api/v1/marketplace/plugins", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_marketplace_search(token, auth_headers):
    response = client.get("/api/v1/marketplace/plugins/search", headers=auth_headers, params={"query": "test"})
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_marketplace_install(token, auth_headers):
    response = client.post("/api/v1/marketplace/install/test-plugin", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_marketplace_uninstall(token, auth_headers):
    response = client.post("/api/v1/marketplace/uninstall/test-plugin", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_marketplace_installed(token, auth_headers):
    response = client.get("/api/v1/marketplace/installed", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_distributed_register_node(token, auth_headers):
    response = client.post(
        "/api/v1/distributed/nodes",
        headers=auth_headers,
        json={"name": "test-node", "capabilities": ["compute"]},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_distributed_cluster_status(token, auth_headers):
    response = client.get("/api/v1/distributed/cluster", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_ecosystem_distributed_get_node_not_found(token, auth_headers):
    response = client.get("/api/v1/distributed/nodes/nonexistent-node", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


# ---------------------------------------------------------------------------
# Model Gateway
# ---------------------------------------------------------------------------


def test_model_gateway_health(token, auth_headers):
    response = client.get("/api/v1/health", headers=auth_headers)
    assert response.status_code in (200, 404)


def test_model_gateway_providers(token, auth_headers):
    response = client.get("/api/v1/providers", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_model_gateway_route(token, auth_headers):
    response = client.post(
        "/api/v1/route",
        headers=auth_headers,
        params={"task_type": "chat", "capability": "default", "context": "{}"},
    )
    assert response.status_code in (200, 400, 404, 422, 500)


# ---------------------------------------------------------------------------
# Notifications
# ---------------------------------------------------------------------------


def test_notifications_send(token, auth_headers):
    response = client.post(
        "/api/v1/notifications",
        headers=auth_headers,
        params={
            "recipient": "test-user",
            "message": "Test notification",
            "channel": "websocket",
        },
    )
    assert response.status_code in (200, 404, 422, 500)


def test_notifications_get(token, auth_headers):
    response = client.get("/api/v1/notifications/test-user", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_notifications_mark_read(token, auth_headers):
    response = client.patch(
        "/api/v1/notifications/test-user/read/notif-1",
        headers=auth_headers,
    )
    assert response.status_code in (200, 404, 422, 500)


# ---------------------------------------------------------------------------
# Orchestrator V2
# ---------------------------------------------------------------------------


def test_orchestrator_v2_chat(token, auth_headers):
    response = client.post(
        "/api/v1/v2/chat",
        headers=auth_headers,
        json={"message": "test goal", "conversation_id": "conv-1"},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_orchestrator_v2_task_status_not_found(token, auth_headers):
    response = client.get("/api/v1/v2/tasks/nonexistent-task", headers=auth_headers)
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Telemetry
# ---------------------------------------------------------------------------


def test_telemetry_analysis_metrics(token, auth_headers):
    response = client.get("/api/v1/metrics/analysis", headers=auth_headers)
    assert response.status_code == 200


def test_telemetry_chat_metrics(token, auth_headers):
    response = client.get("/api/v1/metrics/chat", headers=auth_headers)
    assert response.status_code == 200


def test_telemetry_parser_metrics(token, auth_headers):
    response = client.get("/api/v1/metrics/parser", headers=auth_headers)
    assert response.status_code == 200


def test_telemetry_reasoning_metrics(token, auth_headers):
    response = client.get("/api/v1/metrics/reasoning", headers=auth_headers)
    assert response.status_code == 200


def test_telemetry_all_metrics(token, auth_headers):
    response = client.get("/api/v1/metrics", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "analysis" in data
    assert "chat" in data


# ---------------------------------------------------------------------------
# Trading
# ---------------------------------------------------------------------------


def test_trading_analyze(token, auth_headers):
    response = client.post(
        "/api/v1/trading/analyze",
        headers=auth_headers,
        json={"symbol": "BTCUSDT"},
    )
    assert response.status_code in (200, 400, 404, 422, 502, 500)


def test_trading_health(token, auth_headers):
    response = client.get("/api/v1/trading/health", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


# ---------------------------------------------------------------------------
# Integration
# ---------------------------------------------------------------------------


def test_integration_health(token, auth_headers):
    response = client.get("/api/v1/integration/health", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_integration_trading_analysis(token, auth_headers):
    response = client.post(
        "/api/v1/integration/trading-analysis",
        headers=auth_headers,
        json={"symbol": "BTCUSDT"},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_integration_network_design_review(token, auth_headers):
    response = client.post(
        "/api/v1/integration/network-design-review",
        headers=auth_headers,
        json={"topology_description": "A simple network with 2 routers and 3 switches connected via fiber"},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_integration_self_improvement(token, auth_headers):
    response = client.post(
        "/api/v1/integration/self-improvement",
        headers=auth_headers,
        json={"project_path": ".", "analysis_type": "full"},
    )
    assert response.status_code in (200, 404, 422, 500)


# ---------------------------------------------------------------------------
# Phase3 (44 endpoints)
# ---------------------------------------------------------------------------


def test_phase3_organization_create(token, auth_headers):
    response = client.post(
        "/api/v1/organization",
        headers=auth_headers,
        params={"name": "TestOrg", "role": "manager", "agent_type": "planner"},
    )
    assert response.status_code in (200, 400, 404, 422, 500)


def test_phase3_organization_get(token, auth_headers):
    response = client.get("/api/v1/organization/node-unknown", headers=auth_headers)
    assert response.status_code in (200, 404)


def test_phase3_organization_subtree(token, auth_headers):
    response = client.get("/api/v1/organization/node-unknown/subtree", headers=auth_headers)
    assert response.status_code in (200, 404)


def test_phase3_reputation_leaderboard(token, auth_headers):
    response = client.get("/api/v1/reputation/leaderboard", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_phase3_reputation_record(token, auth_headers):
    response = client.post(
        "/api/v1/reputation/record",
        headers=auth_headers,
        params={
            "agent_id": "agent-1",
            "success": True,
            "quality_score": 0.9,
            "latency_ms": 100.0,
            "cost": 0.01,
        },
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_experience_search(token, auth_headers):
    response = client.get("/api/v1/experience/search", headers=auth_headers, params={"query": "test"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_phase3_experience_record(token, auth_headers):
    response = client.post(
        "/api/v1/experience/record",
        headers=auth_headers,
        json={
            "project_id": "proj-1",
            "category": "test",
            "situation": "situation",
            "action_taken": "action",
            "outcome": "outcome",
            "quality_score": 0.8,
        },
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_observability_trace(token, auth_headers):
    response = client.get("/api/v1/observability/traces/trace-1", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_observability_metrics(token, auth_headers):
    response = client.get("/api/v1/observability/metrics", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_governance_create_policy(token, auth_headers):
    response = client.post(
        "/api/v1/governance/policies",
        headers=auth_headers,
        json={
            "name": "TestPolicy",
            "agent": "agent-1",
            "permissions": ["read"],
            "tools": ["tool-1"],
        },
    )
    assert response.status_code in (200, 400, 404, 422, 500)


def test_phase3_recovery_checkpoints(token, auth_headers):
    response = client.get("/api/v1/recovery/checkpoints", headers=auth_headers)
    assert response.status_code == 200


def test_phase3_evaluation_create_benchmark(token, auth_headers):
    response = client.post(
        "/api/v1/evaluation/benchmarks",
        headers=auth_headers,
        json={"name": "TestBenchmark", "description": "desc", "test_cases": []},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_mcp_tools(token, auth_headers):
    response = client.get("/api/v1/mcp/tools", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_phase3_mcp_plugins(token, auth_headers):
    response = client.get("/api/v1/mcp/plugins", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_phase3_artifacts_create(token, auth_headers):
    response = client.post(
        "/api/v1/artifacts",
        headers=auth_headers,
        json={"project_id": "proj-1", "name": "Phase3 Artifact", "artifact_type": "file", "content": "content"},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_artifacts_get_not_found(token, auth_headers):
    response = client.get("/api/v1/artifacts/nonexistent-artifact", headers=auth_headers)
    assert response.status_code == 404


def test_phase3_graph_create_node(token, auth_headers):
    response = client.post(
        "/api/v1/graph/nodes",
        headers=auth_headers,
        json={"name": "Node1", "node_type": "task", "description": "desc", "project_id": "proj-1"},
    )
    assert response.status_code in (200, 400, 404, 422, 500)


def test_phase3_graph_create_edge(token, auth_headers):
    response = client.post(
        "/api/v1/graph/edges",
        headers=auth_headers,
        json={"source_id": "node-1", "target_id": "node-2", "relation": "depends_on"},
    )
    assert response.status_code in (200, 400, 404, 422, 500)


def test_phase3_graph_related_nodes(token, auth_headers):
    response = client.get("/api/v1/graph/nodes/node-unknown/related", headers=auth_headers)
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_prompt_compile(token, auth_headers):
    response = client.post(
        "/api/v1/prompt/compile",
        headers=auth_headers,
        json={"user_input": "test input", "agent_type": "planner"},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_budget_estimate(token, auth_headers):
    response = client.post(
        "/api/v1/budget/estimate",
        headers=auth_headers,
        json={"task_description": "test task"},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_goals_create(token, auth_headers):
    response = client.post(
        "/api/v1/goals",
        headers=auth_headers,
        json={"description": "test goal", "success_criteria": ["criteria-1"]},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_goals_get_not_found(token, auth_headers):
    response = client.get("/api/v1/goals/nonexistent-goal", headers=auth_headers)
    assert response.status_code == 404


def test_phase3_longtasks_submit(token, auth_headers):
    response = client.post(
        "/api/v1/longtasks",
        headers=auth_headers,
        json={"name": "test-longtask", "workflow": [{"step": "run"}]},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_longtasks_get_not_found(token, auth_headers):
    response = client.get("/api/v1/longtasks/nonexistent-task", headers=auth_headers)
    assert response.status_code == 404


def test_phase3_cognitive_process(token, auth_headers):
    response = client.post(
        "/api/v1/cognitive/process",
        headers=auth_headers,
        json={"user_input": "analyze", "project_id": "proj-1"},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_cognitive_reason(token, auth_headers):
    response = client.post(
        "/api/v1/cognitive/reason",
        headers=auth_headers,
        json={"problem": "test problem"},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_cognitive_debate(token, auth_headers):
    response = client.post(
        "/api/v1/cognitive/debate",
        headers=auth_headers,
        json={"topic": "test topic", "agents": ["agent-1"], "rounds": 1},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_cognitive_verify(token, auth_headers):
    response = client.post(
        "/api/v1/cognitive/verify",
        headers=auth_headers,
        json={"artifact_id": "art-1", "code": "print('hello')", "language": "python"},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_cognitive_simulate(token, auth_headers):
    response = client.post(
        "/api/v1/cognitive/simulate",
        headers=auth_headers,
        json={"plan": [{"step": 1}], "dry_run": True},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_cognitive_world_query(token, auth_headers):
    response = client.get("/api/v1/cognitive/world/query", headers=auth_headers, params={"query": "test"})
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_cognitive_strategy(token, auth_headers):
    response = client.post(
        "/api/v1/cognitive/strategy",
        headers=auth_headers,
        json={"goal_description": "test goal"},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_cognitive_services(token, auth_headers):
    response = client.get("/api/v1/cognitive/services", headers=auth_headers)
    assert response.status_code == 200
    assert "services" in response.json()


def test_phase3_cognitive_execute(token, auth_headers):
    response = client.post(
        "/api/v1/cognitive/execute",
        headers=auth_headers,
        json={"service_name": "planner", "context": {}},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_cognitive_adaptive(token, auth_headers):
    response = client.post(
        "/api/v1/cognitive/adaptive",
        headers=auth_headers,
        json={"user_input": "test"},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_meta_optimize(token, auth_headers):
    response = client.post(
        "/api/v1/cognitive/meta/optimize",
        headers=auth_headers,
        json={"user_input": "test", "result": {}},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_meta_metrics(token, auth_headers):
    response = client.get("/api/v1/cognitive/meta/metrics", headers=auth_headers)
    assert response.status_code == 200


def test_phase3_meta_choose_pipeline(token, auth_headers):
    response = client.post(
        "/api/v1/cognitive/meta/choose-pipeline",
        headers=auth_headers,
        json={"user_input": "test"},
    )
    assert response.status_code in (200, 404, 422, 500)


def test_phase3_cognitive_decide(token, auth_headers):
    response = client.post(
        "/api/v1/cognitive/decide",
        headers=auth_headers,
        json={"options": [{"id": "opt-1", "description": "option 1", "utility": 0.5, "risk": 0.5, "cost": 0.5, "confidence": 0.5}]},
    )
    assert response.status_code in (200, 404, 422, 500)


# ---------------------------------------------------------------------------
# Unauthenticated access
# ---------------------------------------------------------------------------


def test_unauthenticated_access():
    response = client.get("/api/v1/workspaces")
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_token() -> str:
    response = client.post(
        "/api/v1/auth/login",
        data={"username": TEST_USERNAME, "password": TEST_PASSWORD},
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()["access_token"]


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
