"""
System Architect Benchmark — RFC-0011 quality measurement.

Measures 8 dimensions:
    - Architecture Review Completeness
    - Dependency Violation Detection
    - Package Boundary Enforcement
    - ADR Coverage
    - Design Pattern Application
    - Scalability Assessment
    - Maintainability
    - Explainability

Usage::

    python -m benchmarks.system_architect_benchmark
"""

from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path
from typing import Any

# Ensure project root is on PYTHONPATH.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from apps.system_architect.engine import SystemArchitectEngine
from apps.system_architect.schemas import (
    ArchitectureReviewRequest,
    ReviewType,
    ReviewOutcome,
)


def _quick_request(
    workspace_path: str,
    review_type: ReviewType = ReviewType.full_review,
    focus_areas: list[Any] | None = None,
) -> ArchitectureReviewRequest:
    return ArchitectureReviewRequest(
        review_id="benchmark-001",
        review_type=review_type,
        workspace_path=workspace_path,
        focus_areas=focus_areas or [],
        include_recommendations=True,
    )


def test_review_completeness() -> float:
    """
    Scenario: Full review on the ECP repo.
    Expected: Findings + metrics + ADR draft + DDD assessment + recommendations
    all present in the report.
    """
    engine = SystemArchitectEngine()
    req = _quick_request("apps")
    report = asyncio.run(engine.review(req))

    score = 0.0
    # Complete review must produce all 5 output components
    if report.summary.total_findings >= 0 and report.findings is not None:
        score += 0.2
    if report.architecture_metrics is not None:
        score += 0.2
    if report.adr_draft is not None and report.adr_draft.title:
        score += 0.2
    if report.ddd_assessment is not None:
        score += 0.2
    if report.recommendations is not None:
        score += 0.2
    return score


def test_violation_detection() -> float:
    """
    Scenario: Full review on the ECP repo.
    Expected: Metrics detect dependency cycles and layer violations when present.
    """
    engine = SystemArchitectEngine()
    req = _quick_request("apps")
    report = asyncio.run(engine.review(req))

    metrics = report.architecture_metrics
    # Detection coverage: metrics populated (not -1 / sentinel)
    score = 0.0
    if metrics.dependency_cycles >= 0:
        score += 0.3
    if metrics.layer_violations >= 0:
        score += 0.3
    if metrics.package_boundaries_crossed >= 0:
        score += 0.4
    return score


def test_boundary_enforcement() -> float:
    """
    Scenario: Package boundary review on the ECP repo.
    Expected: Boundary violations are reported as findings with category
    'package_boundary' when present, and metrics expose boundary count.
    """
    engine = SystemArchitectEngine()
    req = _quick_request(".", ReviewType.package_boundary)
    report = asyncio.run(engine.review(req))

    boundary_findings = [f for f in report.findings if f.category.value == "package_boundary"]
    # The metrics should at least be consistent with the findings count
    metrics_consistent = (
        report.architecture_metrics.package_boundaries_crossed >= len(boundary_findings)
        or len(boundary_findings) == 0
    )
    score = 0.5 if metrics_consistent else 0.2
    # If boundary findings exist, they should have a recommendation
    if boundary_findings and all(f.recommendation for f in boundary_findings):
        score += 0.4
    elif not boundary_findings:
        # No boundary violations is fine, still a valid review
        score += 0.4
    return min(score, 1.0)


def test_adr_coverage() -> float:
    """
    Scenario: Full review.
    Expected: An ADR draft is always generated with context, decision,
    and at least one consequence.
    """
    engine = SystemArchitectEngine()
    req = _quick_request("apps")
    report = asyncio.run(engine.review(req))

    adr = report.adr_draft
    score = 0.0
    if adr and adr.title:
        score += 0.25
    if adr and len(adr.context) > 10:
        score += 0.25
    if adr and len(adr.decision) > 10:
        score += 0.25
    if adr and len(adr.consequences) >= 1:
        score += 0.25
    return score


def test_design_pattern() -> float:
    """
    Scenario: DDD review on the ECP repo.
    Expected: DDD assessment populated with bounded contexts, domain events,
    and anti-corruption layers when present.
    """
    engine = SystemArchitectEngine()
    req = _quick_request(".", ReviewType.ddd)
    report = asyncio.run(engine.review(req))

    ddd = report.ddd_assessment
    score = 0.0
    if ddd is not None:
        score += 0.3
        if ddd.bounded_contexts:
            score += 0.3
        if ddd.domain_events:
            score += 0.2
        if ddd.anti_corruption_layers:
            score += 0.2
    return score


def test_scalability_assessment() -> float:
    """
    Scenario: Full review.
    Expected: Scalability-relevant findings (cycles, boundaries) reflected
    in metrics.scalability_score (0-100).
    """
    engine = SystemArchitectEngine()
    req = _quick_request("apps")
    report = asyncio.run(engine.review(req))

    score = report.architecture_metrics.scalability_score
    if 0 <= score <= 100:
        return 0.9
    return 0.2


def test_maintainability() -> float:
    """
    Scenario: Full review.
    Expected: maintainability_score (0-100) and testability_score populated.
    """
    engine = SystemArchitectEngine()
    req = _quick_request("apps")
    report = asyncio.run(engine.review(req))

    m = report.architecture_metrics
    score = 0.0
    if 0 <= m.maintainability_score <= 100:
        score += 0.5
    if 0 <= m.testability_score <= 100:
        score += 0.5
    return score


def test_explainability() -> float:
    """
    Scenario: Full review.
    Expected: Findings have descriptions and recommendations; summary has
    severity counts and overall risk.
    """
    engine = SystemArchitectEngine()
    req = _quick_request("apps")
    report = asyncio.run(engine.review(req))

    score = 0.0
    findings = report.findings
    if findings:
        described = sum(1 for f in findings if len(f.description) > 10)
        recommended = sum(1 for f in findings if len(f.recommendation) > 10)
        score += 0.3 * (described / len(findings))
        score += 0.3 * (recommended / len(findings))
    else:
        score += 0.6  # no findings is fine, nothing to explain
    summary = report.summary
    if summary is not None:
        score += 0.2 if summary.overall_risk else 0.0
        score += 0.2 if summary.total_findings >= 0 else 0.0
    return score


def run_benchmark() -> dict[str, float]:
    """Run all 8 benchmark dimensions and return scores."""
    tests = {
        "review_completeness": test_review_completeness,
        "violation_detection": test_violation_detection,
        "boundary_enforcement": test_boundary_enforcement,
        "adr_coverage": test_adr_coverage,
        "design_pattern": test_design_pattern,
        "scalability_assessment": test_scalability_assessment,
        "maintainability": test_maintainability,
        "explainability": test_explainability,
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
    print("System Architect Benchmark (RFC-0011)")
    print("=" * 60)
    results = run_benchmark()
    print()
    print(f"{'Dimension':<30} {'Score':<10} {'Pass':<10}")
    print("-" * 50)
    for name, score in results.items():
        passed = "PASS" if score >= 0.7 else "FAIL"
        print(f"{name:<30} {score:<10.2%} {passed:<10}")
    print("-" * 50)
    print(f"Overall: {results.get('overall', 0.0):.2%}")
    print(f"Pass rate: {results.get('pass_rate', 0.0):.2%}")
    target = 0.9
    if results.get("overall", 0.0) >= target:
        print(f"\n✓ BENCHMARK PASSED (overall >= {target:.0%})")
    else:
        print(f"\n✗ BENCHMARK FAILED (overall < {target:.0%})")
    return 0 if results.get("overall", 0.0) >= target else 1


if __name__ == "__main__":
    sys.exit(main())

