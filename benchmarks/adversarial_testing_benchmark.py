"""
Adversarial Testing Benchmark — RFC-0025 quality measurement.

Measures 8 dimensions:
    - Attack diversity (multiple attack categories generated)
    - Attack structure (each vector has required fields)
    - Assumption auditing (hidden assumptions identified)
    - Vulnerability detection (vulnerabilities scored by severity)
    - Hardening recommendations (mitigations provided)
    - Gate evaluation (pass/fail logic correct)
    - Explanation completeness (reasoning chain produced)
    - Critical detection rate (CRITICAL vulnerabilities flagged)

Usage::

    python -m benchmarks.adversarial_testing_benchmark
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("TESTING", "true")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from apps.adversarial_testing.engine import AdversarialTestingEngine
from apps.adversarial_testing.schemas import (
    AttackCategory,
    GateResult,
    Priority,
    Severity,
)

SAMPLE_PLAN = (
    "Deploy a new microservice that processes customer payments. "
    "The service will be deployed in a single AWS region with a PostgreSQL database. "
    "We'll use the provider's default security settings and rely on existing monitoring."
)


def test_attack_diversity() -> float:
    """Attacks span multiple categories."""
    engine = AdversarialTestingEngine()
    vectors = engine.generator.generate(
        subject=SAMPLE_PLAN,
        subject_type="plan",
        categories=None,
        budget=18,
    )
    categories = set(v.category.value for v in vectors)
    ratio = len(categories) / len(AttackCategory)
    return min(1.0, ratio)


def test_attack_structure() -> float:
    """Each attack vector has all required fields."""
    engine = AdversarialTestingEngine()
    vectors = engine.generator.generate(
        subject=SAMPLE_PLAN,
        subject_type="plan",
        budget=10,
    )
    for v in vectors:
        assert v.id is not None
        assert v.description is not None
        assert v.severity in Severity
        assert isinstance(v.assumptions, list)
        assert v.worst_case_impact is not None
    return 1.0


def test_assumption_auditing() -> float:
    """Assumptions are audited from the subject."""
    engine = AdversarialTestingEngine()
    assumptions = engine.auditor.audit(SAMPLE_PLAN, evidence=None, context=None, constraints=[])
    if len(assumptions) >= 1:
        return 1.0
    return 0.0


def test_vulnerability_detection() -> float:
    """Vulnerabilities are detected and scored."""
    engine = AdversarialTestingEngine()
    vectors = engine.generator.generate(subject=SAMPLE_PLAN, subject_type="plan", budget=10)
    vulns = engine.scanner.scan(SAMPLE_PLAN, vectors, evidence=None, constraints=None)
    if len(vulns) >= 1:
        for v in vulns:
            assert 0.0 <= v.confidence <= 1.0
            assert v.severity in Severity
        return 1.0
    return 0.5


def test_hardening_recommendations() -> float:
    """Hardening actions are generated."""
    engine = AdversarialTestingEngine()
    vectors = engine.generator.generate(subject=SAMPLE_PLAN, subject_type="plan", budget=10)
    vulns = engine.scanner.scan(SAMPLE_PLAN, vectors, {}, [])
    actions = engine.advisor.recommend(vulns, vectors, constraints=[], existing_hardening=[])
    if len(actions) >= 1:
        for a in actions:
            assert a.priority in Priority
            assert isinstance(a.estimated_effort, str)
        return 1.0
    return 0.5


def test_gate_evaluation() -> float:
    """Gate evaluation produces valid pass/fail result."""
    engine = AdversarialTestingEngine()
    result = engine.test(
        subject=SAMPLE_PLAN,
        subject_type="plan",
        attack_budget=10,
    )
    if result.gate_result in GateResult and 0.0 <= result.pass_score <= 1.0:
        return 1.0
    return 0.0


def test_explanation_completeness() -> float:
    """Explanation chain is produced."""
    engine = AdversarialTestingEngine()
    result = engine.test(
        subject=SAMPLE_PLAN,
        subject_type="plan",
        attack_budget=10,
    )
    if isinstance(result.explanation_chain, dict) and len(result.explanation_chain) > 0:
        return 1.0
    return 0.0


def test_critical_detection() -> float:
    """CRITICAL vulnerabilities are detected."""
    engine = AdversarialTestingEngine()
    critical_plan = (
        "Deploy with no security, no backups, single region, and assume "
        "nothing will fail. Critical customer data will be stored unencrypted."
    )
    result = engine.test(
        subject=critical_plan,
        subject_type="plan",
        attack_budget=15,
    )
    has_critical = any(
        v.get("severity") == Severity.CRITICAL.value for v in result.vulnerabilities_found
    )
    if has_critical or result.gate_result == GateResult.FAIL:
        return 1.0
    return 0.5


def run_benchmark() -> dict[str, float]:
    tests = {
        "attack_diversity": test_attack_diversity,
        "attack_structure": test_attack_structure,
        "assumption_auditing": test_assumption_auditing,
        "vulnerability_detection": test_vulnerability_detection,
        "hardening_recommendations": test_hardening_recommendations,
        "gate_evaluation": test_gate_evaluation,
        "explanation_completeness": test_explanation_completeness,
        "critical_detection": test_critical_detection,
    }
    results: dict[str, float] = {}
    n_pass = 0
    for name, fn in tests.items():
        try:
            score = fn()
            results[name] = score
            if score >= 0.7:
                n_pass += 1
        except Exception as e:
            results[name] = 0.0
            print(f"  [FAIL] {name}: {e}")
    results["overall"] = round(sum(results.values()) / len(results), 4)
    results["pass_rate"] = round(n_pass / len(tests), 4)
    return results


def main():
    print("=" * 60)
    print("Adversarial Testing Benchmark (RFC-0025)")
    print("=" * 60)
    results = run_benchmark()
    print()
    print(f"{'Dimension':<30} {'Score':<10} {'Pass':<10}")
    print("-" * 50)
    for name, score in results.items():
        if name in ("overall", "pass_rate"):
            continue
        passed = "PASS" if score >= 0.7 else "FAIL"
        print(f"{name:<30} {score:<10.2%} {passed:<10}")
    print("-" * 50)
    print(f"Overall: {results.get('overall', 0.0):.2%}")
    print(f"Pass rate: {results.get('pass_rate', 0.0):.2%}")
    target = 0.85
    if results.get("overall", 0.0) >= target:
        print(f"\n[PASS] BENCHMARK PASSED (overall >= {target:.0%})")
    else:
        print(f"\n[FAIL] BENCHMARK FAILED (overall < {target:.0%})")
    return 0 if results.get("overall", 0.0) >= target else 1


if __name__ == "__main__":
    sys.exit(main())
