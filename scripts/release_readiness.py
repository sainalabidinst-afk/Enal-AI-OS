#!/usr/bin/env python3
"""
Release Readiness Dashboard
============================

Aggregates project status across all layers and gates.
Produces a simple terminal dashboard and JSON report.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

LAYERS = [
    {
        "id": "platform-foundation",
        "name": "Platform Foundation",
        "weight": 100,
        "checks": [
            ("backend/pyproject.toml", "Backend packaging"),
            ("frontend/package.json", "Frontend packaging"),
            ("pyproject.toml", "Workspace config"),
            ("docker-compose.yml", "Docker compose"),
            (".github/workflows/ci.yml", "CI pipeline"),
            ("Makefile", "Makefile targets"),
        ],
    },
    {
        "id": "product-platform",
        "name": "Product Platform",
        "weight": 100,
        "checks": [
            ("frontend/app/page.tsx", "Chat page"),
            ("frontend/app/workspace/page.tsx", "Workspace page"),
            ("frontend/app/executions/page.tsx", "Executions page"),
            ("frontend/app/artifacts/page.tsx", "Artifacts page"),
            ("frontend/app/metrics/page.tsx", "Metrics page"),
            ("frontend/app/capabilities/page.tsx", "Capabilities page"),
            ("frontend/app/settings/page.tsx", "Settings page"),
        ],
    },
    {
        "id": "runtime-configuration",
        "name": "Runtime Configuration",
        "weight": 100,
        "checks": [
            ("backend/Dockerfile", "Backend Dockerfile"),
            ("frontend/Dockerfile", "Frontend Dockerfile"),
            ("backend/.dockerignore", "Backend dockerignore"),
            ("frontend/.dockerignore", "Frontend dockerignore"),
            ("backend/wait-for-dependencies.sh", "Wait script"),
            ("backend/app/core/config.py", "Config module"),
            (".env.example", "Env template"),
        ],
    },
    {
        "id": "developer-tooling",
        "name": "Developer Tooling",
        "weight": 100,
        "checks": [
            ("scripts/gate0_validate.py", "Gate 0 script"),
            ("benchmarks/network_engineer_benchmark.py", "Network benchmark"),
            ("setup.sh", "Linux setup"),
            ("setup.ps1", "Windows setup"),
            ("docs/DEPENDENCY_AUDIT.md", "Dependency audit"),
            ("docs/SPRINT_5A_PLAN.md", "Sprint 5A plan"),
        ],
    },
    {
        "id": "runtime-certification",
        "name": "Runtime Certification",
        "weight": 100,
        "checks": [
            ("scripts/gate0_validate.py", "Gate 0 automation"),
            ("docker-compose.yml", "Compose healthchecks"),
            (".github/workflows/ci.yml", "CI completeness"),
        ],
    },
    {
        "id": "ai-capability-layer",
        "name": "AI Capability Layer",
        "weight": 100,
        "checks": [
            ("apps/network_engineer/__init__.py", "Network Engineer app"),
            ("apps/network_engineer/analyzer.py", "Network analyzer"),
            ("apps/code_engineer/__init__.py", "Code Engineer app"),
            ("apps/trading_analyst/engine.py", "Trading Analyst engine"),
            ("apps/research_assistant/__init__.py", "Research Assistant app"),
            ("apps/devops_assistant/__init__.py", "DevOps Assistant app"),
            ("apps/self_development/__init__.py", "Self Development app"),
        ],
    },
    {
        "id": "knowledge-base",
        "name": "Knowledge Base",
        "weight": 100,
        "checks": [
            ("real_cases/README.md", "Real cases README"),
            ("real_cases/schema.py", "Real cases schema"),
            ("real_cases/benchmark.py", "Benchmark harness"),
            ("real_cases/kpi.py", "KPI engine"),
            ("real_cases/collector.py", "Case collector"),
        ],
    },
    {
        "id": "benchmark-dataset",
        "name": "Benchmark Dataset",
        "weight": 100,
        "checks": [
            ("real_cases/mikrotik/", "MikroTik cases"),
            ("real_cases/network/", "Network cases"),
            ("real_cases/code/", "Code cases"),
            ("real_cases/devops/", "DevOps cases"),
            ("real_cases/research/", "Research cases"),
            ("real_cases/trading/", "Trading cases"),
            ("benchmarks/network_engineer_benchmark.py", "Benchmark runner"),
        ],
    },
]


@dataclass
class LayerResult:
    layer_id: str
    name: str
    weight: int
    passed: int
    total: int
    checks: list[dict[str, Any]]


def check_exists(rel_path: str) -> bool:
    return (ROOT / rel_path).exists()


def evaluate_layer(layer: dict[str, Any]) -> LayerResult:
    checks = []
    passed = 0
    for rel_path, label in layer["checks"]:
        exists = check_exists(rel_path)
        checks.append({
            "path": rel_path,
            "label": label,
            "status": "pass" if exists else "fail",
        })
        if exists:
            passed += 1
    return LayerResult(
        layer_id=layer["id"],
        name=layer["name"],
        weight=layer["weight"],
        passed=passed,
        total=len(layer["checks"]),
        checks=checks,
    )


def render_dashboard(results: list[LayerResult]) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append("  Enal AI OS — Release Readiness Dashboard")
    lines.append("=" * 70)
    lines.append("")
    for result in results:
        pct = result.passed / result.total if result.total else 0.0
        bar_filled = int(pct * 20)
        bar = "█" * bar_filled + "░" * (20 - bar_filled)
        lines.append(f"  {result.name:.<30} {bar} {pct:.0%}")
    lines.append("")
    lines.append("-" * 70)

    overall_passed = sum(r.passed for r in results)
    overall_total = sum(r.total for r in results)
    overall_pct = overall_passed / overall_total if overall_total else 0.0
    lines.append(f"  Overall Readiness: {overall_pct:.0%} ({overall_passed}/{overall_total})")
    lines.append("=" * 70)
    return "\n".join(lines)


def build_report(results: list[LayerResult]) -> dict[str, Any]:
    layers = {}
    for r in results:
        layers[r.layer_id] = {
            "name": r.name,
            "passed": r.passed,
            "total": r.total,
            "score": round(r.passed / r.total, 4) if r.total else 0.0,
            "checks": r.checks,
        }
    overall_passed = sum(r.passed for r in results)
    overall_total = sum(r.total for r in results)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall": {
            "passed": overall_passed,
            "total": overall_total,
            "score": round(overall_passed / overall_total, 4) if overall_total else 0.0,
        },
        "layers": layers,
    }


def main() -> int:
    results = [evaluate_layer(layer) for layer in LAYERS]
    print(render_dashboard(results))

    report = build_report(results)
    report_path = ROOT / "docs" / "release_readiness.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"  Report written: {report_path}")

    failed = [r for r in results if r.passed < r.total]
    if failed:
        print("\n  ❌ Not ready — missing items:")
        for r in failed:
            for check in r.checks:
                if check["status"] == "fail":
                    print(f"    - [{r.name}] {check['label']} ({check['path']})")
        return 1
    print("\n  ✅ All layers ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
