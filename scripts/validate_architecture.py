#!/usr/bin/env python3
"""
Gate 2 — Architecture Convergence Validator

Verifies that the codebase follows the canonical architecture boundary:
- No circular imports between major packages
- Single capability contract (apps/ vs backend/app/ boundary respected)
- No god objects (single file with too many responsibilities)
- Dependency direction is correct (apps -> backend, not backend -> apps)

Exit codes:
  0 - architecture is converged
  1 - architecture violations detected
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
APPS = ROOT / "apps"


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def check_circular_imports() -> dict[str, Any]:
    cognitive_init = _read(BACKEND / "app" / "core" / "cognitive" / "__init__.py")
    adaptive_runtime = _read(BACKEND / "app" / "core" / "adaptive_runtime.py")
    cognitive_kernel = _read(BACKEND / "app" / "core" / "cognitive_kernel.py")

    init_import_at_top = "from backend.app.core.adaptive_runtime import adaptive_runtime" in cognitive_init.split("class ")[0]
    runtime_import_at_top = "from backend.app.core.cognitive_kernel import cognitive_kernel" in adaptive_runtime.split("class ")[0]
    kernel_import_at_top = "from backend.app.core.cognitive.world_model import world_model" in cognitive_kernel.split("class ")[0]

    circular = init_import_at_top and runtime_import_at_top and kernel_import_at_top

    if circular:
        return {
            "passed": False,
            "detail": "Circular import detected: cognitive/__init__.py -> adaptive_runtime.py -> cognitive_kernel.py -> cognitive/__init__.py",
        }

    return {"passed": True, "detail": ""}


def check_backend_imports_apps() -> dict[str, Any]:
    backend_files = list(BACKEND.rglob("*.py"))
    violations = []
    for filepath in backend_files:
        content = _read(filepath)
        for line in content.splitlines():
            if line.strip().startswith("from apps.") or line.strip().startswith("import apps."):
                violations.append(f"{filepath.relative_to(ROOT)}: {line.strip()[:100]}")
                break

    return {
        "passed": len(violations) == 0,
        "detail": f"Backend importing apps/ (boundary violation): {violations[:3]}" if violations else "",
    }


def check_phase3_god_object() -> dict[str, Any]:
    phase3 = BACKEND / "app" / "api" / "phase3.py"
    if not phase3.exists():
        return {"passed": False, "detail": "phase3.py not found"}

    content = _read(phase3)
    lines = content.splitlines()
    line_count = len(lines)

    if line_count > 300:
        return {
            "passed": False,
            "detail": f"phase3.py is {line_count} lines (threshold: 300). Consider splitting into smaller routers.",
        }

    return {"passed": True, "detail": ""}


def check_capability_contract() -> dict[str, Any]:
    base_py = _read(APPS / "base.py")
    has_base = "BaseReferenceApp" in base_py and "def run(" in base_py

    app_dirs = [d for d in APPS.iterdir() if d.is_dir() and d.name != "__pycache__"]
    violations = []
    for app_dir in app_dirs:
        init = app_dir / "__init__.py"
        if not init.exists():
            violations.append(f"{app_dir.name}/__init__.py missing")
            continue
        content = _read(init)
        if "BaseReferenceApp" not in content and "get_app" not in content:
            violations.append(f"{app_dir.name} does not follow BaseReferenceApp contract")

    return {
        "passed": has_base and len(violations) == 0,
        "detail": f"Contract violations: {violations}" if violations else "",
    }


def check_organization_init() -> dict[str, Any]:
    org_init = APPS / "organization" / "__init__.py"
    if not org_init.exists():
        return {"passed": False, "detail": "apps/organization/__init__.py missing"}

    content = _read(org_init)
    if len(content.strip()) == 0:
        return {"passed": False, "detail": "apps/organization/__init__.py is empty"}

    return {"passed": True, "detail": ""}


def check_no_duplicate_workflow_files() -> dict[str, Any]:
    test_integration = BACKEND / "tests" / "test_integration.py"
    test_integration_api = BACKEND / "tests" / "test_integration_api.py"

    if test_integration.exists() and test_integration_api.exists():
        content1 = _read(test_integration)
        content2 = _read(test_integration_api)
        if content1 == content2:
            return {
                "passed": False,
                "detail": "test_integration.py and test_integration_api.py are identical (duplicate)",
            }

    return {"passed": True, "detail": ""}


def validate() -> list[dict[str, Any]]:
    checks = [
        {"name": "No circular imports", "func": check_circular_imports},
        {"name": "No backend -> apps imports", "func": check_backend_imports_apps},
        {"name": "phase3.py not a god object", "func": check_phase3_god_object},
        {"name": "Capability contract consistency", "func": check_capability_contract},
        {"name": "Organization package exposed", "func": check_organization_init},
        {"name": "No duplicate test files", "func": check_no_duplicate_workflow_files},
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
    print("Gate 2 — Architecture Convergence")
    print("=" * 60)
    for check in checks:
        status = "PASS" if check["passed"] else "FAIL"
        print(f"  [{status}] {check['name']}")
        if check.get("detail") and not check["passed"]:
            print(f"       {check['detail'][:200]}")
    print()
    all_passed = all(c["passed"] for c in checks)
    overall = "PASS — Architecture converged" if all_passed else "FAIL — Architecture violations detected"
    print(f"Overall: {overall}")
    print("=" * 60)
    return all_passed


def main() -> int:
    results = validate()
    passed = print_report(results)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
