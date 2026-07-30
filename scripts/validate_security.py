#!/usr/bin/env python3
"""
Gate 1 — Security Hardening Acceptance Validator

Verifies that all P0 security issues have been addressed.
This gate must pass before any release or merge to main.

Exit codes:
  0 - all security checks passed
  1 - one or more security checks failed
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def check_authentication() -> dict[str, Any]:
    main_py = _read(BACKEND / "app" / "main.py")
    has_auth = (
        "HTTPBearer" in main_py
        or "get_current_user" in main_py
        or "AuthenticationMiddleware" in main_py
        or "jwt" in main_py.lower()
    )
    return {
        "passed": has_auth,
        "detail": "No authentication framework detected in main.py" if not has_auth else "",
    }


def check_authorization() -> dict[str, Any]:
    security_model = _read(BACKEND / "app" / "core" / "security_model.py")
    has_rbac = (
        "check_permission" in security_model
        or "RBAC" in security_model
        or "Permission" in security_model
    )
    return {
        "passed": has_rbac,
        "detail": "No RBAC/authorization model detected" if not has_rbac else "",
    }


def check_rate_limiting() -> dict[str, Any]:
    main_py = _read(BACKEND / "app" / "main.py")
    has_rate_limit = (
        "slowapi" in main_py
        or "RateLimit" in main_py
        or "rate_limit" in main_py.lower()
    )
    return {
        "passed": has_rate_limit,
        "detail": "No rate limiting middleware detected" if not has_rate_limit else "",
    }


def check_security_headers() -> dict[str, Any]:
    main_py = _read(BACKEND / "app" / "main.py")
    headers = ["X-Frame-Options", "X-Content-Type-Options", "Strict-Transport-Security", "Content-Security-Policy"]
    has_headers = any(h in main_py for h in headers)
    return {
        "passed": has_headers,
        "detail": "No security headers middleware detected" if not has_headers else "",
    }


def check_sandbox_injection() -> dict[str, Any]:
    sandbox = _read(BACKEND / "app" / "core" / "sandbox.py")
    has_shell = "create_subprocess_shell" in sandbox
    has_exec = "create_subprocess_exec" in sandbox
    passed = not has_shell and has_exec
    return {
        "passed": passed,
        "detail": "create_subprocess_shell still present (command injection risk)" if has_shell else "",
    }


def check_ssrf_protection() -> dict[str, Any]:
    browser_agent = _read(BACKEND / "app" / "core" / "browser_agent.py")
    has_validation = (
        "private" in browser_agent.lower()
        or "169.254" in browser_agent
        or "127.0.0.1" in browser_agent
        or "allowlist" in browser_agent.lower()
        or "blocklist" in browser_agent.lower()
    )
    return {
        "passed": has_validation,
        "detail": "No SSRF protection detected in browser_agent.py" if not has_validation else "",
    }


def check_directory_traversal() -> dict[str, Any]:
    benchmark = _read(BACKEND / "app" / "api" / "benchmark.py")
    workspace = _read(BACKEND / "app" / "api" / "workspace.py")
    has_traversal_check = (
        "resolve()" in benchmark or "resolve()" in workspace
    ) and (
        "parent" in benchmark or "parent" in workspace
    )
    return {
        "passed": has_traversal_check,
        "detail": "No directory traversal protection detected" if not has_traversal_check else "",
    }


def check_workspace_isolation() -> dict[str, Any]:
    workspace = _read(BACKEND / "app" / "api" / "workspace.py")
    has_isolation = "chroot" in workspace.lower() or "resolve()" in workspace
    return {
        "passed": has_isolation,
        "detail": "No workspace isolation detected" if not has_isolation else "",
    }


def check_secrets_scan() -> dict[str, Any]:
    config = _read(BACKEND / "app" / "core" / "config.py")
    compose = _read(ROOT / "docker-compose.yml")
    hardcoded_patterns = [
        r'postgresql://postgres:postgres@',
        r'POSTGRES_PASSWORD:\s*postgres',
        r'SECRET_KEY:\s*""',
        r'OPENAI_API_KEY:\s*""',
    ]
    violations = []
    for pattern in hardcoded_patterns:
        if re.search(pattern, config) or re.search(pattern, compose):
            violations.append(pattern)
    return {
        "passed": len(violations) == 0,
        "detail": f"Hardcoded secrets found: {violations}" if violations else "",
    }


def validate() -> list[dict[str, Any]]:
    checks = [
        {"name": "Authentication Framework", "func": check_authentication},
        {"name": "Authorization (RBAC/ABAC)", "func": check_authorization},
        {"name": "Rate Limiting", "func": check_rate_limiting},
        {"name": "Security Headers", "func": check_security_headers},
        {"name": "Sandbox Injection Fix", "func": check_sandbox_injection},
        {"name": "SSRF Protection", "func": check_ssrf_protection},
        {"name": "Directory Traversal Fix", "func": check_directory_traversal},
        {"name": "Workspace Isolation", "func": check_workspace_isolation},
        {"name": "Secrets Scan", "func": check_secrets_scan},
    ]

    results = []
    for check in checks:
        try:
            result = check["func"]()
            result["name"] = check["name"]
            results.append(result)
        except Exception as exc:
            results.append({"name": check["name"], "passed": False, "detail": str(exc)})
    return results


def print_report(checks: list[dict[str, Any]]) -> bool:
    print("=" * 60)
    print("Gate 1 — Security Hardening Acceptance")
    print("=" * 60)
    for check in checks:
        status = "PASS" if check["passed"] else "FAIL"
        print(f"  [{status}] {check['name']}")
        if check.get("detail") and not check["passed"]:
            print(f"       {check['detail'][:200]}")
    print()
    all_passed = all(c["passed"] for c in checks)
    overall = "PASS — Security hardening complete" if all_passed else "FAIL — Security hardening incomplete"
    print(f"Overall: {overall}")
    print("=" * 60)
    return all_passed


def main() -> int:
    results = validate()
    passed = print_report(results)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
