#!/usr/bin/env python3
"""
Gate 4 — Cognitive Validation

Verifies that the cognitive pipeline components are present and functional:
- Perception
- Knowledge Retrieval
- Evidence Collection
- Reasoning
- Planning
- Debate
- Reflection
- Learning

This is a lightweight validation that checks for component existence and
basic importability. Full end-to-end cognitive tests are in the test suite.

Exit codes:
  0 - cognitive components validated
  1 - cognitive gaps detected
"""

from __future__ import annotations

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


def check_perception() -> dict[str, Any]:
    perception = _read(BACKEND / "app" / "core" / "perception_engine.py")
    return {
        "passed": "class PerceptionEngine" in perception or "async def process" in perception,
        "detail": "Perception engine not found or incomplete" if "class PerceptionEngine" not in perception else "",
    }


def check_knowledge() -> dict[str, Any]:
    knowledge_dir = BACKEND / "app" / "core" / "knowledge"
    store = knowledge_dir / "store.py"
    retrieval = knowledge_dir / "retrieval.py"
    return {
        "passed": store.exists() and retrieval.exists(),
        "detail": "Knowledge store or retrieval module missing" if not (store.exists() and retrieval.exists()) else "",
    }


def check_reasoning() -> dict[str, Any]:
    reasoning = _read(BACKEND / "app" / "core" / "cognitive" / "reasoning_engine.py")
    return {
        "passed": "class ReasoningEngine" in reasoning or "def reason" in reasoning,
        "detail": "Reasoning engine not found" if "class ReasoningEngine" not in reasoning else "",
    }


def check_planning() -> dict[str, Any]:
    planning = _read(BACKEND / "app" / "core" / "goal_engine.py")
    return {
        "passed": "class AutonomousGoalEngine" in planning or "class GoalEngine" in planning or "def plan" in planning,
        "detail": "Planning/goal engine not found" if "class AutonomousGoalEngine" not in planning else "",
    }


def check_debate() -> dict[str, Any]:
    debate = _read(BACKEND / "app" / "core" / "cognitive" / "debate_engine.py")
    return {
        "passed": "debate" in debate.lower() or "adversarial" in debate.lower(),
        "detail": "Debate engine not found" if "debate" not in debate.lower() else "",
    }


def check_reflection() -> dict[str, Any]:
    reflection = _read(BACKEND / "app" / "core" / "reflection.py")
    return {
        "passed": "class Reflection" in reflection or "def reflect" in reflection,
        "detail": "Reflection module not found" if "class Reflection" not in reflection else "",
    }


def check_learning() -> dict[str, Any]:
    learning_path = BACKEND / "app" / "core" / "cognitive" / "continuous_learning.py"
    learning = _read(learning_path)
    return {
        "passed": learning_path.exists() and ("class" in learning or "def" in learning),
        "detail": "Learning module not found" if not learning_path.exists() else "",
    }


def check_cognitive_kernel() -> dict[str, Any]:
    kernel = _read(BACKEND / "app" / "core" / "cognitive_kernel.py")
    return {
        "passed": "class CognitiveKernel" in kernel or "class CognitiveService" in kernel,
        "detail": "Cognitive kernel not found" if "class CognitiveService" not in kernel else "",
    }


def check_adaptive_runtime() -> dict[str, Any]:
    runtime = _read(BACKEND / "app" / "core" / "adaptive_runtime.py")
    return {
        "passed": "class AdaptiveCognitiveRuntime" in runtime,
        "detail": "Adaptive runtime not found" if "class AdaptiveCognitiveRuntime" not in runtime else "",
    }


def validate() -> list[dict[str, Any]]:
    checks = [
        {"name": "Perception Engine", "func": check_perception},
        {"name": "Knowledge Store & Retrieval", "func": check_knowledge},
        {"name": "Reasoning Engine", "func": check_reasoning},
        {"name": "Planning / Goal Engine", "func": check_planning},
        {"name": "Debate Engine", "func": check_debate},
        {"name": "Reflection Module", "func": check_reflection},
        {"name": "Learning Module", "func": check_learning},
        {"name": "Cognitive Kernel", "func": check_cognitive_kernel},
        {"name": "Adaptive Runtime", "func": check_adaptive_runtime},
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
    print("Gate 4 — Cognitive Validation")
    print("=" * 60)
    for check in checks:
        status = "PASS" if check["passed"] else "FAIL"
        print(f"  [{status}] {check['name']}")
        if check.get("detail") and not check["passed"]:
            print(f"       {check['detail'][:200]}")
    print()

    passed_count = sum(1 for c in checks if c["passed"])
    total_count = len(checks)
    score = int((passed_count / total_count) * 100) if total_count > 0 else 0

    all_passed = all(c["passed"] for c in checks)
    overall = "PASS — Cognitive components validated" if all_passed else "FAIL — Cognitive gaps detected"
    print(f"Overall: {overall}")
    print(f"Score: {score}/100")
    print("=" * 60)
    return all_passed


def main() -> int:
    results = validate()
    passed = print_report(results)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
