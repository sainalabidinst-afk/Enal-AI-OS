#!/usr/bin/env python3
"""
Engineering Remediation Plan v1.0 — Orchestrator

Runs all gate validators sequentially:
  Gate 0 → Gate 1 → Gate 2 → Gate 3 → Gate 4

Rules:
  - Gate 0 fails: STOP (baseline not stable)
  - Gate 1 fails: RELEASE BLOCKED
  - Gate 2 fails: MERGE BLOCKED
  - Gate 3 fails: CAPABILITY NOT VALIDATED
  - Gate 4 fails: AI NOT PRODUCTION READY

Exit codes:
  0 - all gates passed
  1 - one or more gates failed
  2 - environment missing
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

GATES = [
    {
        "id": 0,
        "name": "Baseline Freeze",
        "script": "validate_baseline.py",
        "blocking": True,
        "description": "Repository must be in a stable, passing state",
    },
    {
        "id": 1,
        "name": "Security Hardening",
        "script": "validate_security.py",
        "blocking": True,
        "description": "All P0 security issues must be addressed",
    },
    {
        "id": 2,
        "name": "Architecture Convergence",
        "script": "validate_architecture.py",
        "blocking": True,
        "description": "Architecture boundaries and contracts must be clean",
    },
    {
        "id": 3,
        "name": "Capability Wiring",
        "script": "validate_capabilities.py",
        "blocking": False,
        "description": "All capabilities must be integrated and validated",
    },
    {
        "id": 4,
        "name": "Cognitive Validation",
        "script": "validate_cognitive.py",
        "blocking": False,
        "description": "Cognitive pipeline components must be functional",
    },
]


def load_validator(script_name: str) -> Any | None:
    script_path = SCRIPTS / script_name
    if not script_path.exists():
        return None

    spec = importlib.util.spec_from_file_location("validator", script_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        return module
    except Exception:
        return None


def run_gate(gate: dict[str, Any]) -> dict[str, Any]:
    module = load_validator(gate["script"])
    if module is None:
        return {
            "id": gate["id"],
            "name": gate["name"],
            "passed": False,
            "detail": f"Validator script not found or failed to load: {gate['script']}",
            "blocking": gate["blocking"],
        }

    try:
        if hasattr(module, "validate"):
            results = module.validate()
            passed = all(r["passed"] for r in results)
            failed_count = sum(1 for r in results if not r["passed"])
            details = [r["detail"] for r in results if r.get("detail")]
            return {
                "id": gate["id"],
                "name": gate["name"],
                "passed": passed,
                "detail": f"{failed_count} checks failed: " + "; ".join(details[:3]) if not passed else "",
                "blocking": gate["blocking"],
            }
        else:
            return {
                "id": gate["id"],
                "name": gate["name"],
                "passed": False,
                "detail": "Validator missing validate() function",
                "blocking": gate["blocking"],
            }
    except Exception as exc:
        return {
            "id": gate["id"],
            "name": gate["name"],
            "passed": False,
            "detail": str(exc),
            "blocking": gate["blocking"],
        }


def print_final_report(results: list[dict[str, Any]]) -> str:
    print()
    print("=" * 60)
    print("Engineering Remediation Plan v1.0 — Final Report")
    print("=" * 60)
    print()

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"Gate {result['id']}  [{status}] {result['name']}")
        if result.get("detail") and not result["passed"]:
            detail = result["detail"].replace("\n", " ")[:300]
            print(f"       {detail}")

    print()
    print("-" * 60)

    failed_gates = [r for r in results if not r["passed"]]
    if not failed_gates:
        print("Overall Status: READY FOR RELEASE")
        print("All gates passed. Platform is ready for production deployment.")
    else:
        blocking_failures = [r for r in failed_gates if r["blocking"]]
        if blocking_failures:
            print("Overall Status: RELEASE BLOCKED")
            print(f"Blocking failures in: {', '.join('Gate ' + str(r['id']) for r in blocking_failures)}")
        else:
            print("Overall Status: PASS WITH WARNING")
            print(f"Non-blocking failures in: {', '.join('Gate ' + str(r['id']) for r in failed_gates)}")
        print()
        print("Action required:")
        for r in failed_gates:
            print(f"  - Fix Gate {r['id']} ({r['name']})")
            if r.get("detail"):
                print(f"    {r['detail'][:200]}")

    print("=" * 60)
    return "RELEASE BLOCKED" if any(r["blocking"] and not r["passed"] for r in results) else "READY FOR RELEASE"


def main() -> int:
    print()
    print("=" * 60)
    print("Engineering Remediation Plan v1.0 — Gate Orchestrator")
    print("=" * 60)
    print()
    print("Running gates sequentially...")
    print()

    results = []
    for gate in GATES:
        print(f"Running Gate {gate['id']}: {gate['name']}...")
        result = run_gate(gate)
        results.append(result)
        status = "PASS" if result["passed"] else "FAIL"
        print(f"Gate {gate['id']} {gate['name']}: {status}")
        if not result["passed"] and result.get("detail"):
            print(f"  {result['detail'][:200]}")
        print()

        if not result["passed"] and result["blocking"]:
            print(f"BLOCKING: Gate {gate['id']} failed. Stopping pipeline.")
            print()
            break

    final_status = print_final_report(results)

    if final_status == "RELEASE BLOCKED":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
