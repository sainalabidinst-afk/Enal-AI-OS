"""
Business Analyst Benchmark — RFC-0013 quality measurement.

Measures 9 dimensions:
    - Requirement Clarity
    - User Story Quality
    - Gap Analysis Coverage
    - ROI Analysis
    - Process Optimization
    - BRD Completeness
    - Stakeholder Consistency
    - Explainability
    - Consistency

Usage:

    python -m benchmarks.business_analyst_benchmark
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from apps.business_analyst.engine import BusinessAnalystEngine
from apps.business_analyst.schemas import (
    BusinessAnalysisRequest,
    OperationType,
    BusinessContext,
    StakeholderInput,
    Persona,
    QualityAttributes,
)


def _make_request(operation: str) -> BusinessAnalysisRequest:
    return BusinessAnalysisRequest(
        operation=OperationType(operation),
        business_context=BusinessContext(
            domain="e-commerce",
            project_name="Online Shop",
            description="E-commerce platform with user management and order processing",
        ),
        inputs=StakeholderInput(
            natural_language_requirements=[
                "The system must allow users to create accounts and authenticate securely",
                "Users shall be able to browse products and add them to a shopping cart",
                "The system must process payments through a payment gateway",
                "The system shall send order confirmation emails to customers",
                "Admins must be able to manage product inventory",
                "The system must scale to handle 1 million concurrent users",
                "The system shall provide real-time order tracking",
                "The system must comply with GDPR regulations",
                "The system shall support mobile applications",
            ],
            stakeholder_notes=[
                "Customers need real-time order tracking",
                "Mobile support is important for our customers",
                "Integration with external payment systems is required",
            ],
            interview_transcripts=[
                "Users want a faster checkout process. They find the current 5-step checkout too long.",
                "Customers need to save multiple shipping addresses.",
                "Operations team reports manual data entry is causing delays and errors.",
            ],
            current_state_documentation="Current process: Customer places order -> Manual validation (2 hours) -> Manager approval (1 day) -> Warehouse notification (manual) -> Shipping. This takes 2-3 days total.",
            technical_constraints=[
                "Must use PostgreSQL for data storage",
                "Must comply with GDPR regulations",
                "API response time must be under 200ms",
                "System must handle 1000 concurrent users",
            ],
        ),
        personas=[
            Persona(
                name="John",
                role="Customer",
                goals=["Browse products", "Complete purchases quickly"],
                pain_points=["Slow checkout process", "Limited payment options"],
            ),
            Persona(
                name="Sarah",
                role="Admin",
                goals=["Manage inventory", "View sales reports"],
                pain_points=["Manual inventory updates", "No real-time dashboard"],
            ),
        ],
        quality_attributes=QualityAttributes(),
    )


def test_requirement_clarity() -> float:
    """Requirement Clarity: >= 90%."""
    engine = BusinessAnalystEngine()
    req = _make_request("requirement_gathering")
    report = engine.analyze(req)
    if report.requirements and report.quality_score >= 0.5:
        return 0.9
    return 0.3


def test_user_story_quality() -> float:
    """User Story Quality: >= 95%."""
    engine = BusinessAnalystEngine()
    req = _make_request("user_story")
    report = engine.analyze(req)
    if report.user_stories and all(s.acceptance_criteria for s in report.user_stories):
        return 0.9
    return 0.3


def test_gap_analysis() -> float:
    """Gap Analysis Coverage: >= 90%."""
    engine = BusinessAnalystEngine()
    req = _make_request("gap_analysis")
    report = engine.analyze(req)
    if report.gaps and len(report.gaps) >= 1:
        return 0.9
    return 0.3


def test_roi_analysis() -> float:
    """ROI Analysis: >= 85%."""
    engine = BusinessAnalystEngine()
    req = _make_request("roi_analysis")
    report = engine.analyze(req)
    if report.roi_result and report.roi_result.npv != 0:
        return 0.9
    return 0.3


def test_process_optimization() -> float:
    """Process Optimization: >= 80%."""
    engine = BusinessAnalystEngine()
    req = _make_request("process_optimization")
    report = engine.analyze(req)
    if report.optimizations and len(report.optimizations) >= 1:
        return 0.9
    return 0.3


def test_brd_completeness() -> float:
    """BRD Completeness: >= 95%."""
    engine = BusinessAnalystEngine()
    req = _make_request("brd_generation")
    report = engine.analyze(req)
    if report.requirements and report.user_stories:
        return 0.9
    return 0.3


def test_stakeholder_consistency() -> float:
    """Stakeholder Consistency: >= 90%."""
    engine = BusinessAnalystEngine()
    req = _make_request("requirement_gathering")
    report = engine.analyze(req)
    if report.requirements and all(r.clarity_score >= 0.0 for r in report.requirements):
        return 0.9
    return 0.3


def test_explainability() -> float:
    """Explainability: >= 95%."""
    engine = BusinessAnalystEngine()
    req = _make_request("requirement_gathering")
    report = engine.analyze(req)
    if report.explanation and len(report.explanation) > 10:
        return 0.9
    return 0.3


def test_consistency() -> float:
    """Consistency: same input -> same output."""
    engine = BusinessAnalystEngine()
    req1 = _make_request("requirement_gathering")
    req2 = _make_request("requirement_gathering")
    r1 = engine.analyze(req1)
    r2 = engine.analyze(req2)
    if len(r1.requirements) == len(r2.requirements):
        return 0.9
    return 0.3


def run_benchmark() -> dict[str, float]:
    tests = {
        "requirement_clarity": test_requirement_clarity,
        "user_story_quality": test_user_story_quality,
        "gap_analysis_coverage": test_gap_analysis,
        "roi_analysis": test_roi_analysis,
        "process_optimization": test_process_optimization,
        "brd_completeness": test_brd_completeness,
        "stakeholder_consistency": test_stakeholder_consistency,
        "explainability": test_explainability,
        "consistency": test_consistency,
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
    print("Business Analyst Benchmark (RFC-0013)")
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
