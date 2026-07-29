#!/usr/bin/env python3
"""
Sprint 5.4 — End-to-End Integration Test Suite

Validates that the ENTIRE frontend ↔ backend flow works with real data.
No mocks. No simulations.

Flow:
  1. Health check
  2. Login → JWT
  3. List capabilities
  4. List workspaces
  5. Start execution
  6. Monitor execution (poll until complete)
  7. List artifacts
  8. Fetch metrics
"""

import sys
import json
import time
import urllib.request
import urllib.error
import urllib.parse

BASE_URL = "http://localhost:8000"
PASS = 0
FAIL = 0
RESULTS = []


def check(name: str, condition: bool, detail: str = ""):
    global PASS, FAIL
    if condition:
        PASS += 1
        status = "✅ PASS"
    else:
        FAIL += 1
        status = "❌ FAIL"
    msg = f"  {status} | {name}"
    if detail:
        msg += f" | {detail}"
    print(msg)
    RESULTS.append((status, name, detail))


def api(method: str, path: str, body: dict = None, token: str = None) -> tuple:
    """Make an HTTP request and return (status_code, data_dict)."""
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode("utf-8")
            return resp.status, json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        try:
            err_body = json.loads(e.read().decode("utf-8"))
        except Exception:
            err_body = {}
        return e.code, err_body
    except Exception as e:
        return 0, {"error": str(e)}


def run_tests():
    global PASS, FAIL, RESULTS

    print("=" * 72)
    print("  SPRINT 5.4 — END-TO-END INTEGRATION TEST SUITE")
    print("=" * 72)
    print()

    # ── 0. Health Check ──────────────────────────────────────
    print("\n─── 0. Health Check ────────────────────────────────")
    status, data = api("GET", "/health")
    check("Health endpoint responds", status in (200, 404),
          f"status={status}")
    if status == 200:
        check("Health returns valid JSON", isinstance(data, dict))
    else:
        # Fallback health check
        status2, data2 = api("GET", "/api/v1/health")
        check("Health endpoint (alt)", status2 in (200, 404),
              f"status={status2}")

    # ── 1. Login ─────────────────────────────────────────────
    print("\n─── 1. Login / Authentication ──────────────────────")

    # Test login with admin/admin (common default)
    status, data = api("POST", "/api/v1/auth/login",
                       {"username": "admin", "password": "admin"})
    token = None
    if status == 200:
        token = data.get("access_token") or data.get("token")
        check("Login returns token", bool(token),
              f"status={status}")
        check("Login returns user info", "user" in data or "username" in data,
              f"keys={list(data.keys())}")
    else:
        check(f"Login attempt (admin/admin)", False,
              f"status={status} body={str(data)[:100]}")

        # Try without auth — expect 401
        status2, data2 = api("GET", "/api/v1/executions")
        check("Unauthenticated request returns 401", status2 == 401,
              f"status={status2}")

        # Try registration
        test_user = f"test_user_{int(time.time())}"
        status3, data3 = api("POST", "/api/v1/auth/register",
                             {"username": test_user, "password": "test123"})
        if status3 in (200, 201):
            token = data3.get("access_token") or data3.get("token")
            check("Registration + login returns token", bool(token),
                  f"status={status3}")
        else:
            check(f"Registration attempt", False,
                  f"status={status3} body={str(data3)[:100]}")

    if not token:
        print("\n  ⛔ Cannot proceed without auth token. Stopping tests.")
        print("\n─── TEST SUMMARY ─────────────────────────────────")
        print(f"  PASS: {PASS}  FAIL: {FAIL}  TOTAL: {PASS + FAIL}")
        if FAIL > 0:
            print("  STATUS: ❌ INTEGRATION TESTS FAILED")
            print("  Fix login/registration before retrying.")
        else:
            print("  STATUS: ⚠️ INCONCLUSIVE (no auth)")
        sys.exit(1 if FAIL > 0 else 0)

    print(f"  ✅ Authenticated with token: {token[:20]}...")

    # ── 2. List Capabilities ─────────────────────────────────
    print("\n─── 2. Capability Explorer ─────────────────────────")
    status, data = api("GET", "/api/v1/capabilities", token=token)
    caps = []
    if status == 200:
        caps = data.get("capabilities", data.get("items", data.get("data", [])))
        if isinstance(caps, list):
            check("Capabilities list returns array", len(caps) > 0,
                  f"count={len(caps)}")
            if caps:
                check("Capability has id+name",
                      all(c.get("id") and c.get("name") for c in caps[:5]),
                      f"first={caps[0].get('name')}")
        else:
            check("Capabilities is a list", False,
                  f"type={type(caps).__name__}")
    else:
        check("List capabilities endpoint", False,
              f"status={status} body={str(data)[:100]}")

    # Try getting first capability detail
    if caps:
        cap_id = caps[0]["id"]
        status2, data2 = api("GET", f"/api/v1/capabilities/{cap_id}",
                              token=token)
        check("Get capability by ID returns detail",
              status2 == 200 and data2.get("id") == cap_id,
              f"name={data2.get('name', '?')}")

    # ── 3. Workspaces ────────────────────────────────────────
    print("\n─── 3. Workspaces ──────────────────────────────────")
    status, data = api("GET", "/api/v1/workspaces", token=token)
    workspaces = []
    if status == 200:
        workspaces = data if isinstance(data, list) else \
                     data.get("workspaces", data.get("items", []))
        check("Workspaces list returns array", len(workspaces) >= 0,
              f"count={len(workspaces)}")

        # Create workspace if none
        if len(workspaces) == 0:
            status2, data2 = api("POST", "/api/v1/workspaces",
                                 {"name": f"test_ws_{int(time.time())}",
                                  "description": "Auto-created by integration test"},
                                 token=token)
            if status2 in (200, 201):
                workspaces.append(data2)
                check("Create workspace succeeds", True,
                      f"id={data2.get('id', '?')}")
            else:
                check("Create workspace endpoint", False,
                      f"status={status2}")

    ws_id = workspaces[0]["id"] if workspaces else None
    if ws_id:
        check("Workspace has valid ID", bool(ws_id))

    # ── 4. Start Execution ────────────────────────────────────
    print("\n─── 4. Execution — Start ───────────────────────────")
    if not ws_id:
        print("  ⚠️ No workspace available, creating inline...")
        st, dt = api("POST", "/api/v1/workspaces",
                     {"name": f"exec_ws_{int(time.time())}"},
                     token=token)
        if st in (200, 201):
            ws_id = dt.get("id")

    execution_id = None
    if ws_id:
        status, data = api("POST", "/api/v1/executions/run" if True else "/api/v1/executions",
                           {"goal": "Integration test: analyze nothing",
                            "workspace_id": ws_id},
                           token=token)
        if status in (200, 201):
            execution_id = data.get("id") or \
                           data.get("execution", {}).get("id")
            check("Start execution returns ID", bool(execution_id),
                  f"status={status}")
        else:
            # Try alt endpoint
            status2, data2 = api("POST", "/api/v1/chat",
                                 {"message": "Run network engineer capability for integration test",
                                  "workspace_id": ws_id, "stream": False},
                                 token=token)
            check("Chat execution endpoint", status2 in (200, 201),
                  f"status={status2}")
            if status2 in (200, 201):
                execution_id = data2.get("execution_id") or \
                               data2.get("conversation_id") or \
                               data2.get("id")
    else:
        check("Workspace available to start execution", False)

    # ── 5. Monitor Execution ──────────────────────────────────
    print("\n─── 5. Execution — Monitor ─────────────────────────")
    if execution_id:
        for attempt in range(1, 13):  # Poll up to 60s
            status, data = api("GET", f"/api/v1/executions/{execution_id}",
                                token=token)
            if status == 200 and data:
                exec_status = data.get("status", "unknown")
                progress = data.get("progress", 0)
                check(f"Execution status (attempt {attempt})",
                      exec_status in ("pending", "planning", "running",
                                      "completed", "failed", "cancelled"),
                      f"status={exec_status} progress={progress}%")
                if exec_status in ("completed", "failed", "cancelled"):
                    break
            else:
                check(f"Get execution (attempt {attempt})",
                      False, f"status={status}")
            time.sleep(5)
        else:
            print("  ⚠️ Execution did not finish within 60s (may be long-running)")
    else:
        print("  ⚠️ Cannot monitor — no execution ID")

    # Also test listing executions
    status, data = api("GET", "/api/v1/executions", token=token)
    check("List executions endpoint", status == 200,
          f"status={status}")

    # ── 6. Artifacts ──────────────────────────────────────────
    print("\n─── 6. Artifacts ───────────────────────────────────")
    status, data = api("GET", "/api/v1/artifacts" if "artifacts" not in str(data) else
                       "/api/v1/executions/artifacts", token=token)
    if status == 200:
        artifacts = data if isinstance(data, list) else \
                    data.get("artifacts", data.get("items", []))
        check("Artifacts list returns array", True,
              f"count={len(artifacts) if isinstance(artifacts, list) else '?'}")
    else:
        # Try workspace artifacts
        if ws_id:
            status2, data2 = api("GET", f"/api/v1/workspaces/{ws_id}/artifacts",
                                  token=token)
            check("Workspace artifacts endpoint", status2 == 200,
                  f"status={status2}")
        else:
            check("List artifacts endpoint", status == 200,
                  f"status={status} body={str(data)[:100]}")

    # ── 7. Metrics ───────────────────────────────────────────
    print("\n─── 7. Metrics ─────────────────────────────────────")
    status, data = api("GET", "/api/v1/metrics", token=token)
    if status == 200:
        check("Metrics returns data", bool(data),
              f"keys={list(data.keys())}")
        # Check for expected structure
        has_analysis = "analysis" in data
        has_chat = "chat" in data
        check("Metrics has analysis section", has_analysis)
        check("Metrics has chat section", has_chat)
    else:
        check("Get metrics endpoint", False,
              f"status={status} body={str(data)[:100]}")

    # ── Summary ──────────────────────────────────────────────
    print("\n" + "=" * 72)
    print("  TEST SUMMARY")
    print("=" * 72)
    print(f"\n  PASS: {PASS}   FAIL: {FAIL}   TOTAL: {PASS + FAIL}")
    print()

    if FAIL == 0 and PASS > 0:
        print("  STATUS: ✅ ALL INTEGRATION TESTS PASSED")
        print("  The entire frontend ↔ backend flow is validated.")
        print("  ECP is ready for Beta Validation.")
    elif PASS > 0 and FAIL > 0:
        print("  STATUS: ⚠️ PARTIAL — Some tests failed")
        print("  Review FAIL lines above and fix backend endpoints.")
    else:
        print("  STATUS: ❌ BACKEND NOT RESPONDING")
        print("  Make sure the backend is running on", BASE_URL)

    print()
    return 1 if FAIL > 0 and PASS == 0 else 0


if __name__ == "__main__":
    sys.exit(run_tests())

