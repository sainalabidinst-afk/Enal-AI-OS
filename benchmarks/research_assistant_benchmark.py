"""
Research Assistant Benchmark — measures 6 benchmark dimensions.

Dimensions:
- Accuracy: correctness of evidence ranking and findings
- Completeness: coverage of research operations
- Explainability: clarity of reports and citations
- Safety: adherence to confidence thresholds and uncertainty quantification
- Efficiency: latency and resource usage
- Consistency: stable outputs across repeated runs

Usage:

    python -m benchmarks.research_assistant_benchmark
"""

from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from apps.research_assistant.engine import ResearchEngine
from apps.research_assistant.schemas import (
    CitationStyle,
    ConfidenceLevel,
    ResearchOperation,
    ResearchRequest,
)


def _make_request(query: str, operation: str = "literature_review", **kwargs: object) -> ResearchRequest:
    return ResearchRequest(
        query=query,
        operation=ResearchOperation(operation),
        max_sources=kwargs.get("max_sources", 10),
        min_confidence=kwargs.get("min_confidence", 0.5),
        include_contradictions=kwargs.get("include_contradictions", True),
        include_citations=kwargs.get("include_citations", True),
        citation_style=kwargs.get("citation_style", CitationStyle.apa),
        sources=kwargs.get("sources", []),
    )


def test_accuracy() -> float:
    """Accuracy: evidence ranking and findings correctness."""
    engine = ResearchEngine()
    request = _make_request("AI software engineering productivity")
    report = asyncio.run(engine.analyze(request))

    score = 0.0
    if len(report.evidence) > 0:
        score += 0.3
    if len(report.findings) > 0:
        score += 0.3
    if report.confidence > 0.5:
        score += 0.2
    if report.report_markdown and len(report.report_markdown) > 100:
        score += 0.2
    return score


def test_completeness() -> float:
    """Completeness: coverage of all research operations."""
    engine = ResearchEngine()
    operations = [
        "literature_review",
        "evidence_gathering",
        "contradiction_analysis",
        "citation_assessment",
        "confidence_estimation",
        "synthesis",
        "report_generation",
    ]
    passed = 0
    for op in operations:
        request = _make_request("software engineering", operation=op, max_sources=5)
        report = asyncio.run(engine.analyze(request))
        if report.report_markdown and len(report.report_markdown) > 50:
            passed += 1
    return passed / len(operations)


def test_explainability() -> float:
    """Explainability: clarity of reports and citations."""
    engine = ResearchEngine()
    request = _make_request("AI software engineering")
    report = asyncio.run(engine.analyze(request))

    score = 0.0
    if report.report_markdown and len(report.report_markdown) > 200:
        score += 0.4
    if report.findings and all(f.description for f in report.findings):
        score += 0.3
    if report.citations and all(c.text for c in report.citations):
        score += 0.3
    return score


def test_safety() -> float:
    """Safety: confidence thresholds and uncertainty quantification."""
    engine = ResearchEngine()
    request = _make_request("AI software engineering", min_confidence=0.9)
    report = asyncio.run(engine.analyze(request))

    score = 0.0
    if 0.0 <= report.confidence <= 1.0:
        score += 0.4
    if report.uncertainty_factors is not None and isinstance(report.uncertainty_factors, list):
        score += 0.3
    if report.raw and "confidence" in report.raw:
        score += 0.3
    return score


def test_efficiency() -> float:
    """Efficiency: latency and resource usage."""
    engine = ResearchEngine()
    request = _make_request("AI software engineering", max_sources=10)

    start = time.perf_counter()
    report = asyncio.run(engine.analyze(request))
    latency_ms = (time.perf_counter() - start) * 1000.0

    if latency_ms < 1000:
        return 0.9
    if latency_ms < 5000:
        return 0.6
    return 0.3


def test_consistency() -> float:
    """Consistency: stable outputs across repeated runs."""
    engine = ResearchEngine()
    request = _make_request("AI software engineering", max_sources=5)

    r1 = asyncio.run(engine.analyze(request))
    r2 = asyncio.run(engine.analyze(request))

    if len(r1.evidence) == len(r2.evidence):
        return 0.9
    if abs(len(r1.evidence) - len(r2.evidence)) <= 1:
        return 0.6
    return 0.3


def run_benchmark() -> dict[str, float]:
    tests = {
        "accuracy": test_accuracy,
        "completeness": test_completeness,
        "explainability": test_explainability,
        "safety": test_safety,
        "efficiency": test_efficiency,
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


def main() -> int:
    print("=" * 60)
    print("Research Assistant Benchmark")
    print("=" * 60)
    results = run_benchmark()
    print()
    print(f"{'Dimension':<20} {'Score':<10} {'Pass':<10}")
    print("-" * 40)
    for name, score in results.items():
        if name in ("overall", "pass_rate"):
            continue
        passed = "PASS" if score >= 0.7 else "FAIL"
        print(f"{name:<20} {score:<10.2%} {passed:<10}")
    print("-" * 40)
    print(f"Overall: {results.get('overall', 0.0):.2%}")
    print(f"Pass rate: {results.get('pass_rate', 0.0):.2%}")
    target = 0.9
    if results.get("overall", 0.0) >= target:
        print(f"\n[PASS] BENCHMARK PASSED (overall >= {target:.0%})")
        return 0
    print(f"\n[FAIL] BENCHMARK FAILED (overall < {target:.0%})")
    return 1


if __name__ == "__main__":
    sys.exit(main())
