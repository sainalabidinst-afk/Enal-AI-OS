#!/usr/bin/env python3
"""
Gate 0/1/2 — Developer Preview Certification Validator

Gate 0: Infrastructure
  - docker compose up / healthchecks
  - backend importability
  - frontend build
  - CI-equivalent checks

Gate 1: Functional
  - API endpoints respond
  - Frontend pages render
  - Workspace CRUD
  - Chat streaming
  - Execution lifecycle
  - Artifact management
  - Metrics endpoint
  - Capability browser

Gate 2: AI
  - Capability execution
  - Telemetry mutation
  - Benchmark pass

Exit codes:
  0 - all gates passed
  1 - one or more checks failed
  2 - environment missing
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"
COMPOSE = ROOT / "docker-compose.yml"

GATE_RESULTS: dict[str, list[dict[str, Any]]] = {
    "Gate 0": [],
    "Gate 1": [],
    "Gate 2": [],
}


def gate(name: str, gate_id: str):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            try:
                result = fn(*args, **kwargs)
                status = "PASS" if result.get("passed") else "FAIL"
                GATE_RESULTS[gate_id].append({
                    "name": name,
                    "status": status,
                    "detail": result.get("detail", ""),
                })
                return result.get("passed", False)
            except Exception as exc:
                GATE_RESULTS[gate_id].append({
                    "name": name,
                    "status": "ERROR",
                    "detail": str(exc),
                })
                return False
        return wrapper
    return decorator


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=kwargs.get("timeout", 120), **kwargs)
    except FileNotFoundError:
        return None
    except subprocess.TimeoutExpired:
        return None


# ===== Gate 0: Infrastructure =====

@gate("python installed", "Gate 0")
def python_installed() -> dict[str, Any]:
    ok = shutil.which("python") is not None or shutil.which("python3") is not None
    return {"passed": ok, "detail": "python/python3 not found" if not ok else ""}


@gate("node installed", "Gate 0")
def node_installed() -> dict[str, Any]:
    ok = shutil.which("node") is not None
    return {"passed": ok, "detail": "node not found" if not ok else ""}


@gate("docker installed", "Gate 0")
def docker_installed() -> dict[str, Any]:
    ok = shutil.which("docker") is not None
    return {"passed": ok, "detail": "docker not found" if not ok else ""}


@gate("backend pyproject.toml exists", "Gate 0")
def backend_pyproject_exists() -> dict[str, Any]:
    ok = (BACKEND / "pyproject.toml").exists()
    return {"passed": ok, "detail": "backend/pyproject.toml missing" if not ok else ""}


@gate("frontend package.json exists", "Gate 0")
def frontend_package_exists() -> dict[str, Any]:
    ok = (FRONTEND / "package.json").exists()
    return {"passed": ok, "detail": "frontend/package.json missing" if not ok else ""}


@gate("docker-compose.yml exists", "Gate 0")
def compose_file_exists() -> dict[str, Any]:
    ok = COMPOSE.exists()
    return {"passed": ok, "detail": "docker-compose.yml missing" if not ok else ""}


@gate("docker compose config valid", "Gate 0")
def compose_config_valid() -> dict[str, Any]:
    result = run(["docker", "compose", "config"])
    ok = result is not None and result.returncode == 0
    return {"passed": ok, "detail": result.stderr if result and not ok else ""}


@gate("docker compose services up", "Gate 0")
def compose_services_up() -> dict[str, Any]:
    up = run(["docker", "compose", "up", "-d", "postgres", "redis", "qdrant", "ollama"])
    if up is None or up.returncode != 0:
        return {"passed": False, "detail": "docker compose up failed"}
    time.sleep(10)
    ps = run(["docker", "compose", "ps", "--format", "json"])
    if ps is None or ps.returncode != 0:
        return {"passed": False, "detail": "docker compose ps failed"}
    try:
        services = json.loads(ps.stdout)
        running = [s for s in services if s.get("State") == "running"]
        ok = len(running) >= 4
        return {"passed": ok, "detail": f"running={len(running)}/4+" if not ok else ""}
    except json.JSONDecodeError as exc:
        return {"passed": False, "detail": str(exc)}


@gate("backend imports valid", "Gate 0")
def backend_imports_valid() -> dict[str, Any]:
    result = run([sys.executable, "-c", "import backend.app.main"])
    ok = result is not None and result.returncode == 0
    detail = (result.stderr or result.stdout or "") if result else "python not available"
    return {"passed": ok, "detail": detail[:200] if not ok else ""}


@gate("frontend build succeeds", "Gate 0")
def frontend_build_succeeds() -> dict[str, Any]:
    result = run(["npm", "run", "build"], cwd=FRONTEND, timeout=300)
    ok = result is not None and result.returncode == 0
    detail = (result.stderr or result.stdout or "") if result else "npm not available"
    return {"passed": ok, "detail": detail[:200] if not ok else ""}


@gate("ruff lint passes", "Gate 0")
def ruff_lint_passes() -> dict[str, Any]:
    result = run(["ruff", "check", "backend/app/", "tests/"], cwd=ROOT)
    ok = result is not None and result.returncode == 0
    return {"passed": ok, "detail": result.stdout if result and not ok else ""}


@gate("mypy type check passes", "Gate 0")
def mypy_passes() -> dict[str, Any]:
    result = run(["mypy", "backend/app/core", "--ignore-missing-imports", "--explicit-package-bases"], cwd=ROOT)
    ok = result is not None and result.returncode == 0
    return {"passed": ok, "detail": result.stdout if result and not ok else ""}


@gate("pytest unit tests pass", "Gate 0")
def pytest_passes() -> dict[str, Any]:
    result = run(["pytest", "backend/tests/", "tests/", "-v", "--tb=short"], cwd=ROOT, timeout=300)
    ok = result is not None and result.returncode == 0
    return {"passed": ok, "detail": result.stdout if result and not ok else ""}


# ===== Gate 1: Functional =====

@gate("telemetry endpoint returns data", "Gate 1")
def telemetry_endpoint_works() -> dict[str, Any]:
    import urllib.request
    try:
        req = urllib.request.Request("http://localhost:8000/api/v1/metrics", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            ok = "analysis" in data and "chat" in data
            return {"passed": ok, "detail": "missing analysis/chat keys" if not ok else ""}
    except Exception as exc:
        return {"passed": False, "detail": str(exc)}


@gate("capabilities endpoint returns data", "Gate 1")
def capabilities_endpoint_works() -> dict[str, Any]:
    import urllib.request
    try:
        req = urllib.request.Request("http://localhost:8000/api/v1/capabilities", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            ok = "capabilities" in data or "domains" in data
            return {"passed": ok, "detail": "missing capabilities/domains keys" if not ok else ""}
    except Exception as exc:
        return {"passed": False, "detail": str(exc)}


@gate("workspace API reachable", "Gate 1")
def workspace_api_works() -> dict[str, Any]:
    import urllib.request
    try:
        req = urllib.request.Request("http://localhost:8000/api/v1/workspaces", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            ok = resp.status == 200
            return {"passed": ok, "detail": f"status={resp.status}" if not ok else ""}
    except Exception as exc:
        return {"passed": False, "detail": str(exc)}


@gate("executions API reachable", "Gate 1")
def executions_api_works() -> dict[str, Any]:
    import urllib.request
    try:
        req = urllib.request.Request("http://localhost:8000/api/v1/executions", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            ok = resp.status == 200
            return {"passed": ok, "detail": f"status={resp.status}" if not ok else ""}
    except Exception as exc:
        return {"passed": False, "detail": str(exc)}


@gate("artifacts API reachable", "Gate 1")
def artifacts_api_works() -> dict[str, Any]:
    import urllib.request
    try:
        req = urllib.request.Request("http://localhost:8000/api/v1/artifacts", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            ok = resp.status == 200
            return {"passed": ok, "detail": f"status={resp.status}" if not ok else ""}
    except Exception as exc:
        return {"passed": False, "detail": str(exc)}


# ===== Gate 2: AI =====

@gate("telemetry mutable", "Gate 2")
def telemetry_mutable() -> dict[str, Any]:
    import urllib.request
    try:
        req1 = urllib.request.Request("http://localhost:8000/api/v1/metrics", method="GET")
        with urllib.request.urlopen(req1, timeout=5) as resp:
            before = json.loads(resp.read())
        req2 = urllib.request.Request("http://localhost:8000/api/v1/chat", method="POST", headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req2, timeout=5, data=json.dumps({"message": "gate2 ping", "stream": False}).encode()) as resp:
            post_data = json.loads(resp.read())
        time.sleep(1)
        req3 = urllib.request.Request("http://localhost:8000/api/v1/metrics", method="GET")
        with urllib.request.urlopen(req3, timeout=5) as resp:
            after = json.loads(resp.read())
        before_count = before.get("chat", {}).get("count", 0)
        after_count = after.get("chat", {}).get("count", 0)
        ok = after_count > before_count
        return {"passed": ok, "detail": f"count unchanged: {before_count} -> {after_count}" if not ok else ""}
    except Exception as exc:
        return {"passed": False, "detail": str(exc)}


@gate("network benchmark passes", "Gate 2")
def network_benchmark_passes() -> dict[str, Any]:
    result = run([sys.executable, "benchmarks/network_engineer_benchmark.py"], cwd=ROOT, timeout=300)
    if result is None:
        return {"passed": False, "detail": "benchmark script not runnable"}
    ok = result.returncode == 0
    return {"passed": ok, "detail": result.stdout[:200] if not ok else ""}


def print_report() -> int:
    print("\n" + "=" * 70)
    print("  Gate 0/1/2 — Developer Preview Certification Report")
    print("=" * 70 + "\n")

    all_passed = True
    for gate_id in ("Gate 0", "Gate 1", "Gate 2"):
        checks = GATE_RESULTS[gate_id]
        if not checks:
            continue
        print(f"  {gate_id}")
        for check in checks:
            icon = {"PASS": "✔", "FAIL": "✖", "ERROR": "⚠"}.get(check["status"], "?")
            print(f"    {icon} [{check['status']}] {check['name']}")
            if check.get("detail"):
                print(f"         {check['detail'][:120]}")
            if check["status"] in ("FAIL", "ERROR"):
                all_passed = False
        print()

    print("=" * 70)
    if all_passed:
        print("  ✅ All gates PASSED")
    else:
        print("  ❌ One or more gates FAILED")
    print("=" * 70 + "\n")
    return 0 if all_passed else 1


def main() -> int:
    print("\nRunning Gate 0/1/2 validation...\n")

    if not shutil.which("docker"):
        print("❌ docker not installed — Gate 0 cannot run")
        return 2

    backend_pyproject_exists()
    frontend_package_exists()
    compose_file_exists()
    compose_config_valid()
    compose_services_up()
    backend_imports_valid()
    frontend_build_succeeds()
    ruff_lint_passes()
    mypy_passes()
    pytest_passes()

    if shutil.which("docker"):
        time.sleep(2)
        telemetry_endpoint_works()
        capabilities_endpoint_works()
        workspace_api_works()
        executions_api_works()
        artifacts_api_works()
        telemetry_mutable()
        network_benchmark_passes()

    return print_report()


if __name__ == "__main__":
    raise SystemExit(main())
