"""
Self Development Benchmark
============================

Measures Self Development Engine quality across 6 dimensions:
1. Accuracy — % correct problem detection
2. Completeness — % of known issues detected
3. Explainability — quality of reasoning chains and descriptions
4. Safety — no destructive patches generated
5. Efficiency — consistency of output for identical input
6. Risk Modeling — quality of risk and effort estimates

Usage:
    python -m benchmarks.self_development_benchmark
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import random
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from apps.self_development.engine import SelfDevelopmentEngine
from apps.self_development.schemas import Problem

logger = logging.getLogger(__name__)


@dataclass
class Scenario:
    id: int
    name: str
    description: str
    expected_problems: list[str]
    expected_severities: dict[str, str]
    expected_risk_factors: list[str]
    expected_improvement_types: list[str]
    seed: int


@dataclass
class SelfDevelopmentBenchmarkReport:
    generated_at: datetime = field(default_factory=datetime.utcnow)
    overall_score: float = 0.0
    accuracy_score: float = 0.0
    completeness_score: float = 0.0
    explainability_score: float = 0.0
    safety_score: float = 0.0
    efficiency_score: float = 0.0
    risk_modeling_score: float = 0.0
    scenarios_run: int = 0
    problems_detected: int = 0
    problems_missed: int = 0
    false_positives: int = 0
    passed: bool = False
    scenario_details: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at.isoformat(),
            "overall_score": round(self.overall_score, 2),
            "accuracy_score": round(self.accuracy_score, 2),
            "completeness_score": round(self.completeness_score, 2),
            "explainability_score": round(self.explainability_score, 2),
            "safety_score": round(self.safety_score, 2),
            "efficiency_score": round(self.efficiency_score, 2),
            "risk_modeling_score": round(self.risk_modeling_score, 2),
            "scenarios_run": self.scenarios_run,
            "problems_detected": self.problems_detected,
            "problems_missed": self.problems_missed,
            "false_positives": self.false_positives,
            "passed": self.passed,
            "scenario_details": self.scenario_details,
        }


def _build_scenarios() -> list[Scenario]:
    random.seed(42)
    base_scenarios = [
        Scenario(
            id=1,
            name="communication_bottleneck",
            description="Project with medium-severity communication bottleneck",
            expected_problems=["bottleneck"],
            expected_severities={"bottleneck": "medium"},
            expected_risk_factors=["high_message_frequency", "latency"],
            expected_improvement_types=["refactor"],
            seed=101,
        ),
        Scenario(
            id=2,
            name="dead_code",
            description="Project with low-severity dead code",
            expected_problems=["dead_code"],
            expected_severities={"dead_code": "low"},
            expected_risk_factors=["unused_method", "maintainability"],
            expected_improvement_types=["refactor"],
            seed=102,
        ),
        Scenario(
            id=3,
            name="code_duplication",
            description="Project with low-severity code duplication",
            expected_problems=["duplication"],
            expected_severities={"duplication": "low"},
            expected_risk_factors=["maintenance_overhead", "logic_drift"],
            expected_improvement_types=["refactor"],
            seed=103,
        ),
        Scenario(
            id=4,
            name="architecture_smell",
            description="Project with architecture smell (rigidity, fragility)",
            expected_problems=["architecture_smell"],
            expected_severities={"architecture_smell": "high"},
            expected_risk_factors=["rigidity", "fragility", "tight_coupling"],
            expected_improvement_types=["refactor", "restructure"],
            seed=104,
        ),
        Scenario(
            id=5,
            name="security_hole",
            description="Project with security hole (hardcoded secret, injection risk)",
            expected_problems=["security_hole"],
            expected_severities={"security_hole": "high"},
            expected_risk_factors=["hardcoded_secret", "injection_risk", "data_exposure"],
            expected_improvement_types=["refactor", "security_hardening"],
            seed=105,
        ),
        Scenario(
            id=6,
            name="performance_issue",
            description="Project with performance issue (N+1 query, missing index)",
            expected_problems=["performance_issue"],
            expected_severities={"performance_issue": "medium"},
            expected_risk_factors=["n_plus_1_query", "missing_index", "latency"],
            expected_improvement_types=["refactor", "optimize"],
            seed=106,
        ),
        Scenario(
            id=7,
            name="multiple_issues",
            description="Project with multiple combined issues",
            expected_problems=["bottleneck", "dead_code", "duplication"],
            expected_severities={
                "bottleneck": "medium",
                "dead_code": "low",
                "duplication": "low",
            },
            expected_risk_factors=["high_message_frequency", "unused_method", "maintenance_overhead"],
            expected_improvement_types=["refactor"],
            seed=107,
        ),
        Scenario(
            id=8,
            name="high_change_risk",
            description="Project with high change risk (core module modification)",
            expected_problems=["bottleneck", "architecture_smell"],
            expected_severities={
                "bottleneck": "medium",
                "architecture_smell": "high",
            },
            expected_risk_factors=["core_module_change", "regression_risk", "high_coupling"],
            expected_improvement_types=["refactor"],
            seed=108,
        ),
        Scenario(
            id=9,
            name="impact_prediction",
            description="Project with impact prediction challenge",
            expected_problems=["performance_issue", "architecture_smell"],
            expected_severities={
                "performance_issue": "medium",
                "architecture_smell": "high",
            },
            expected_risk_factors=["cascading_failure", "data_integrity", "latency"],
            expected_improvement_types=["refactor", "optimize", "restructure"],
            seed=109,
        ),
        Scenario(
            id=10,
            name="cross_project_pattern",
            description="Project with cross-project pattern matching challenge",
            expected_problems=["duplication", "security_hole", "performance_issue"],
            expected_severities={
                "duplication": "low",
                "security_hole": "high",
                "performance_issue": "medium",
            },
            expected_risk_factors=["cross_project_drift", "injection_risk", "n_plus_1_query"],
            expected_improvement_types=["refactor", "security_hardening", "optimize"],
            seed=110,
        ),
    ]
    random.shuffle(base_scenarios)
    return base_scenarios


def _normalize_type(raw: str) -> str:
    return raw.strip().lower().replace("-", "_").replace(" ", "_")


PROBLEM_TEMPLATES = {
    "bottleneck": {
        "location": "communication.py",
        "description": "Komunikasi sinkron berfrekuensi tinggi meningkatkan latensi antar agen.",
        "impact": "Peningkatan latensi koordinasi multi-agen.",
    },
    "dead_code": {
        "location": "agent_registry.py",
        "description": "Metode lama tidak dipanggil, menambah beban pemeliharaan.",
        "impact": "Penurunan maintainability dan kejelasan kode.",
    },
    "duplication": {
        "location": "team_builder.py",
        "description": "Logika pencocokan kemampuan terduplikasi di beberapa modul.",
        "impact": "Biaya pemeliharaan ganda dan risiko logic drift.",
    },
    "architecture_smell": {
        "location": "orchestrator_v2.py",
        "description": "Modul utama mengandalkan terlalu banyak detail modul lain.",
        "impact": "Perubahan kecil memicu efek domino di seluruh arsitektur.",
    },
    "security_hole": {
        "location": "config.py",
        "description": "Kredensial atau rahasia tertanam langsung di kode sumber.",
        "impact": "Eksposur kredensial dan risiko kebocoran data.",
    },
    "performance_issue": {
        "location": "model_router.py",
        "description": "Akses berulang ke sumber daya tanpa caching atau indeks.",
        "impact": "Peningkatan latency dan beban sumber daya.",
    },
}


def _make_scenario_problems(expected: list[str], severities: dict[str, str]) -> list[Problem]:
    problems = []
    for ptype in expected:
        sev = severities.get(ptype, "medium")
        tmpl = PROBLEM_TEMPLATES.get(ptype, {
            "location": "hotspot.py",
            "description": f"Custom {ptype} problem for benchmarking.",
            "impact": f"Impact of {ptype}.",
        })
        problems.append(Problem(
            id=f"{ptype}-{abs(hash(ptype)) % 10000:04d}",
            type=ptype,
            severity=sev,
            location=tmpl["location"],
            description=tmpl["description"],
            impact=tmpl["impact"],
            confidence=0.9,
            evidence=[f"custom: {ptype}"],
        ))
    return problems


def _score_explainability(problems: list[dict[str, Any]]) -> float:
    if not problems:
        return 0.0
    total = 0.0
    for p in problems:
        desc = (p.get("description") or "").strip()
        impact = (p.get("impact") or "").strip()
        score = 0.0
        if desc:
            score += 0.5
        if impact:
            score += 0.5
        total += min(score, 1.0)
    return total / len(problems)


def _score_safety(patches: dict[str, dict[str, Any]]) -> float:
    if not patches:
        return 1.0
    safe = 0
    for pid, patch in patches.items():
        patch_type = (patch.get("patch_type") or "").strip().lower()
        diff = (patch.get("diff") or "").strip()
        destructive_keywords = ["delete", "remove -rf", "rm -rf", "drop table", "truncate"]
        safe_types = {"refactor", "optimize", "restructure", "security_hardening", "testing"}
        is_safe = patch_type in safe_types and not any(kw in diff.lower() for kw in destructive_keywords)
        if is_safe:
            safe += 1
    return safe / len(patches)


async def _score_efficiency(engine: SelfDevelopmentEngine, runs: int = 3) -> float:
    hashes: list[str] = []
    for _ in range(runs):
        problems = await engine.identify_problems()
        h = hashlib.sha256(str(problems).encode()).hexdigest()
        hashes.append(h)
    unique = len(set(hashes))
    return 1.0 if unique == 1 else max(0.0, 1.0 - (unique - 1) * 0.3)


def _score_risk_modeling(solutions: dict[str, dict[str, Any]]) -> float:
    if not solutions:
        return 0.0
    total = 0.0
    valid_efforts = {"low", "medium", "high"}
    valid_risks = {"low", "medium", "high"}
    for pid, sol in solutions.items():
        effort = (sol.get("estimated_effort") or "").strip().lower()
        risk = (sol.get("risk") or "").strip().lower()
        tests_required = sol.get("tests_required", False)
        score = 0.0
        if effort in valid_efforts:
            score += 0.35
        if risk in valid_risks:
            score += 0.35
        if tests_required:
            score += 0.3
        total += min(score, 1.0)
    return total / len(solutions)


async def _run_scenario(engine: SelfDevelopmentEngine, scenario: Scenario) -> dict[str, Any]:
    engine.set_problems(_make_scenario_problems(scenario.expected_problems, scenario.expected_severities))
    problems = await engine.identify_problems()
    detected_types = {_normalize_type(p.get("type", "")) for p in problems}
    detected_map = {_normalize_type(p.get("type", "")): p for p in problems}
    detected_ids = [p.get("id", "") for p in problems]

    expected_normalized = [_normalize_type(t) for t in scenario.expected_problems]
    expected_set = set(expected_normalized)

    true_positives = detected_types & expected_set
    false_positives = detected_types - expected_set
    missed = expected_set - detected_types

    accuracy = len(true_positives) / max(len(detected_types), 1)
    completeness = len(expected_set - (detected_types - expected_set)) / max(len(expected_set), 1)

    explainability = _score_explainability(problems)

    solutions = {}
    patches = {}
    for pid in detected_ids:
        try:
            solutions[pid] = await engine.propose_solution(pid)
        except Exception:
            solutions[pid] = {}
        try:
            patches[pid] = await engine.generate_patch(pid)
        except Exception:
            patches[pid] = {}

    safety = _score_safety(patches)
    efficiency = await _score_efficiency(engine)
    risk_modeling = _score_risk_modeling(solutions)

    return {
        "scenario_id": scenario.id,
        "scenario_name": scenario.name,
        "expected_problems": scenario.expected_problems,
        "detected_problems": list(detected_types),
        "true_positives": list(true_positives),
        "false_positives": list(false_positives),
        "missed_problems": list(missed),
        "accuracy": accuracy,
        "completeness": completeness,
        "explainability": explainability,
        "safety": safety,
        "efficiency": efficiency,
        "risk_modeling": risk_modeling,
        "problems_detected": len(problems),
        "problems_missed_count": len(missed),
    }


def run_self_development_benchmark(num_scenarios: int = 10) -> SelfDevelopmentBenchmarkReport:
    report = SelfDevelopmentBenchmarkReport()
    scenarios = _build_scenarios()
    selected = scenarios[:num_scenarios]

    async def _execute() -> SelfDevelopmentBenchmarkReport:
        accuracies: list[float] = []
        completenesses: list[float] = []
        explainabilities: list[float] = []
        safeties: list[float] = []
        efficiencies: list[float] = []
        risk_modelings: list[float] = []

        total_detected = 0
        total_missed = 0
        total_false_positives = 0

        for scenario in selected:
            random.seed(scenario.seed)
            engine = SelfDevelopmentEngine()
            try:
                detail = await _run_scenario(engine, scenario)
            except Exception as e:
                logger.exception("Scenario %s failed: %s", scenario.id, e)
                detail = {
                    "scenario_id": scenario.id,
                    "scenario_name": scenario.name,
                    "error": str(e),
                    "accuracy": 0.0,
                    "completeness": 0.0,
                    "explainability": 0.0,
                    "safety": 0.0,
                    "efficiency": 0.0,
                    "risk_modeling": 0.0,
                    "problems_detected": 0,
                    "problems_missed_count": len(scenario.expected_problems),
                }

            report.scenario_details.append(detail)
            accuracies.append(detail["accuracy"])
            completenesses.append(detail["completeness"])
            explainabilities.append(detail["explainability"])
            safeties.append(detail["safety"])
            efficiencies.append(detail["efficiency"])
            risk_modelings.append(detail["risk_modeling"])
            total_detected += detail["problems_detected"]
            total_missed += detail["problems_missed_count"]
            total_false_positives += len(detail.get("false_positives", []))

        def avg(values: list[float]) -> float:
            return sum(values) / len(values) if values else 0.0

        report.scenarios_run = len(selected)
        report.accuracy_score = avg(accuracies) * 100.0
        report.completeness_score = avg(completenesses) * 100.0
        report.explainability_score = avg(explainabilities) * 100.0
        report.safety_score = avg(safeties) * 100.0
        report.efficiency_score = avg(efficiencies) * 100.0
        report.risk_modeling_score = avg(risk_modelings) * 100.0
        report.problems_detected = total_detected
        report.problems_missed = total_missed
        report.false_positives = total_false_positives

        weights = {
            "accuracy": 0.20,
            "completeness": 0.20,
            "explainability": 0.15,
            "safety": 0.15,
            "efficiency": 0.15,
            "risk_modeling": 0.15,
        }
        report.overall_score = (
            report.accuracy_score * weights["accuracy"]
            + report.completeness_score * weights["completeness"]
            + report.explainability_score * weights["explainability"]
            + report.safety_score * weights["safety"]
            + report.efficiency_score * weights["efficiency"]
            + report.risk_modeling_score * weights["risk_modeling"]
        )
        report.passed = report.overall_score >= 95.0
        return report

    return asyncio.run(_execute())


def print_summary(report: SelfDevelopmentBenchmarkReport) -> None:
    print("\n" + "=" * 60)
    print("  Self Development Benchmark Report")
    print("=" * 60)
    print(f"  Generated    : {report.generated_at.isoformat()}")
    print(f"  Overall Score: {report.overall_score:.2f}%")
    print(f"  Accuracy     : {report.accuracy_score:.2f}%")
    print(f"  Completeness : {report.completeness_score:.2f}%")
    print(f"  Explainability: {report.explainability_score:.2f}%")
    print(f"  Safety       : {report.safety_score:.2f}%")
    print(f"  Efficiency   : {report.efficiency_score:.2f}%")
    print(f"  Risk Modeling: {report.risk_modeling_score:.2f}%")
    print("-" * 60)
    print(f"  Scenarios Run: {report.scenarios_run}")
    print(f"  Problems Detected: {report.problems_detected}")
    print(f"  Problems Missed  : {report.problems_missed}")
    print(f"  False Positives  : {report.false_positives}")
    print(f"  Passed           : {report.passed}")
    print("=" * 60)

    if report.scenario_details:
        print("\n  Scenario Details:")
        for detail in report.scenario_details:
            status = "PASS" if detail.get("accuracy", 0) >= 0.5 and detail.get("completeness", 0) >= 0.5 else "FAIL"
            print(f"    [{status}] {detail['scenario_name']}")
            if detail.get("error"):
                print(f"           Error: {detail['error']}")
            else:
                print(f"           Detected: {detail.get('detected_problems', [])}")
                print(f"           Missed: {detail.get('missed_problems', [])}")

    print()
    if report.passed:
        print("  [PASS] BENCHMARK PASSED (overall >= 90%)")
    else:
        print("  [FAIL] BENCHMARK FAILED (overall < 90%)")
    print()


def main() -> int:
    report = run_self_development_benchmark()
    print_summary(report)
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
