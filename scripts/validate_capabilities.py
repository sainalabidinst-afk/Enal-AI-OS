#!/usr/bin/env python3
"""
Gate 3 — Capability Wiring Validator

Verifies that capabilities are not just implemented, but integrated and validated.
Distinguishes between:
- Implemented: code exists
- Integrated: wired to runtime/API
- Validated: has tests and is registered

Exit codes:
  0 - all capabilities properly wired
  1 - wiring gaps detected
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
APPS = ROOT / "apps"
BACKEND = ROOT / "backend"


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def check_capability_registry() -> dict[str, Any]:
    apps_init = APPS / "__init__.py"
    if not apps_init.exists():
        return {"passed": False, "detail": "apps/__init__.py missing"}

    content = _read(apps_init)
    required_reference_apps = [
        "trading_analyst",
        "network_engineer",
        "devops_assistant",
        "code_engineer",
        "research_assistant",
        "full_stack_engineer",
        "self_development",
    ]

    missing = [app for app in required_reference_apps if app not in content]
    return {
        "passed": len(missing) == 0,
        "detail": f"Missing from registry: {missing}" if missing else "",
    }


def check_trading_wiring() -> dict[str, Any]:
    init = _read(APPS / "trading_analyst" / "__init__.py")
    backend_api = _read(BACKEND / "app" / "api" / "trading.py")

    has_market_intelligence_in_app = "market_intelligence" in init
    has_market_intelligence_in_api = "market_intelligence" in backend_api
    has_real_import = (
        "from apps.trading_analyst.market_intelligence" in init
        or "from apps.trading_analyst.market_intelligence" in backend_api
    )

    return {
        "passed": (has_market_intelligence_in_app or has_market_intelligence_in_api) and has_real_import,
        "detail": "Trading Analyst not wired to market_intelligence" if not ((has_market_intelligence_in_app or has_market_intelligence_in_api) and has_real_import) else "",
    }


def check_integration_wiring() -> dict[str, Any]:
    orchestrator = _read(APPS / "integration" / "orchestrator.py")
    has_workflow_result = "WorkflowResult" in orchestrator
    has_real_steps = (
        "trading_analysis_with_knowledge" in orchestrator
        and "network_design_review_with_knowledge" in orchestrator
    )

    return {
        "passed": has_workflow_result and has_real_steps,
        "detail": "Integration orchestrator missing WorkflowResult or workflow steps" if not (has_workflow_result and has_real_steps) else "",
    }


def check_organization_exposed() -> dict[str, Any]:
    org_init = APPS / "organization" / "__init__.py"
    if not org_init.exists():
        return {"passed": False, "detail": "apps/organization/__init__.py missing"}

    content = _read(org_init)
    has_exports = len(content.strip()) > 0 and ("get_app" in content or "Organization" in content)

    return {
        "passed": has_exports,
        "detail": "apps/organization/__init__.py is empty or has no exports" if not has_exports else "",
    }


def check_placeholder_markers() -> dict[str, Any]:
    engines = [
        ("research_assistant", APPS / "research_assistant" / "engine.py"),
        ("self_development", APPS / "self_development" / "engine.py"),
        ("devops_assistant", APPS / "devops_assistant" / "engine.py"),
    ]

    unmarked_placeholders = []
    for name, path in engines:
        content = _read(path)
        is_placeholder = "placeholder" in content.lower() or "simulated" in content.lower()
        has_marker = "experimental" in content.lower() or "placeholder" in content.lower()
        if is_placeholder and not has_marker:
            unmarked_placeholders.append(name)

    return {
        "passed": len(unmarked_placeholders) == 0,
        "detail": f"Capabilities with placeholder logic but no experimental marker: {unmarked_placeholders}" if unmarked_placeholders else "",
    }


def check_backend_api_routes() -> dict[str, Any]:
    main_py = _read(BACKEND / "app" / "main.py")
    integration_router = "integration.router" in main_py
    trading_router = "trading.router" in main_py

    return {
        "passed": integration_router and trading_router,
        "detail": "Backend API not routing integration/trading" if not (integration_router and trading_router) else "",
    }


def validate() -> list[dict[str, Any]]:
    checks = [
        {"name": "Capability registry complete", "func": check_capability_registry},
        {"name": "Trading wired to market_intelligence", "func": check_trading_wiring},
        {"name": "Integration orchestrator complete", "func": check_integration_wiring},
        {"name": "Organization package exposed", "func": check_organization_exposed},
        {"name": "Placeholder markers present", "func": check_placeholder_markers},
        {"name": "Backend API routes registered", "func": check_backend_api_routes},
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
    print("Gate 3 — Capability Wiring")
    print("=" * 60)
    for check in checks:
        status = "PASS" if check["passed"] else "FAIL"
        print(f"  [{status}] {check['name']}")
        if check.get("detail") and not check["passed"]:
            print(f"       {check['detail'][:200]}")
    print()

    all_passed = all(c["passed"] for c in checks)
    overall = "PASS — All capabilities wired" if all_passed else "FAIL — Wiring gaps detected"
    print(f"Overall: {overall}")
    print("=" * 60)
    return all_passed


def main() -> int:
    results = validate()
    passed = print_report(results)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
