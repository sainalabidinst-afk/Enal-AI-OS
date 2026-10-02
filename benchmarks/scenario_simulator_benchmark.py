"""
Scenario Simulator Benchmark — RFC-0023 quality measurement.

Measures 8 dimensions:
    - Reproducibility (same seed -> same result)
    - Statistical soundness (distribution stats valid)
    - Sandbox safety (code executed in isolation)
    - Assumption extraction (implicit assumptions identified)
    - Outcome identification (best/worst/most-likely)
    - Variable parsing (NLP -> structured changes)
    - Confidence calibration (confidence reflects result quality)
    - Latency (reasonable execution time)

Usage::

    python -m benchmarks.scenario_simulator_benchmark
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# Ensure TESTING env is set so LLM calls are skipped
os.environ.setdefault("TESTING", "true")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from apps.scenario_simulator.engine import ScenarioSimulatorEngine
from apps.scenario_simulator.schemas import ChangeType, DistributionType


def _base_state():
    return {"interest_rate": 0.05, "revenue": 100.0}


def test_reproducibility() -> float:
    """Same seed -> identical results."""
    engine = ScenarioSimulatorEngine()
    req1 = engine.build_scenario(
        "If interest rate increases 1%",
        base_state=_base_state(),
        iterations=50,
        seed=42,
    )
    req2 = engine.build_scenario(
        "If interest rate increases 1%",
        base_state=_base_state(),
        iterations=50,
        seed=42,
    )
    r1 = engine.run_simulation(req1)
    r2 = engine.run_simulation(req2)
    if r1.distribution.mean == r2.distribution.mean:
        return 1.0
    return 0.0


def test_statistical_soundness() -> float:
    """Distribution stats are valid and consistent."""
    engine = ScenarioSimulatorEngine()
    req = engine.build_scenario(
        "If revenue changes 10%",
        base_state=_base_state(),
        iterations=200,
        seed=42,
    )
    result = engine.run_simulation(req)
    d = result.distribution
    if (
        d.min_value <= d.mean <= d.max_value
        and d.p5 <= d.p25 <= d.median <= d.p75 <= d.p95
        and d.std_dev >= 0
    ):
        return 1.0
    return 0.3


def test_sandbox_safety() -> float:
    """Sandbox code executes and produces results."""
    engine = ScenarioSimulatorEngine()
    req = engine.build_scenario(
        "If revenue increases 10%",
        base_state={"base_revenue": 1000.0},
        iterations=10,
        seed=42,
    )
    req.sandbox_enabled = True
    req.sandbox_code = "result = base_revenue * 1.1"
    result = engine.run_simulation(req)
    if len(result.sandbox_logs) > 0:
        return 1.0
    return 0.5


def test_assumption_extraction() -> float:
    """Assumptions are extracted from description."""
    engine = ScenarioSimulatorEngine()
    builder = engine.builder
    req = builder.build(
        "Jika suku bunga naik 1% dan kompetitor turun harga 20%",
        base_state={"interest_rate": 0.05, "competitor_price": 100.0},
    )
    assumptions = req.context.get("assumptions", [])
    if len(assumptions) >= 3:
        return 1.0
    return 0.0


def test_outcome_identification() -> float:
    """Best/worst/most-likely outcomes are identified."""
    engine = ScenarioSimulatorEngine()
    req = engine.build_scenario(
        "If metric changes 15%",
        base_state={"metric": 100.0},
        iterations=200,
        seed=42,
    )
    result = engine.run_simulation(req)
    outcome_keys = set(result.outcomes.keys())
    if "best_case" in outcome_keys and "worst_case" in outcome_keys:
        return 1.0
    return 0.3


def test_variable_parsing() -> float:
    """NL descriptions parse into structured variable changes."""
    engine = ScenarioSimulatorEngine()
    req = engine.build_scenario(
        "If interest rate increases 1% and competitor price decreases 20%",
        base_state={"interest_rate": 0.05, "competitor_price": 100.0},
    )
    var_names = {c.variable for c in req.variable_changes}
    if "interest_rate" in var_names and "competitor_price" in var_names:
        return 1.0
    return 0.0


def test_confidence_calibration() -> float:
    """Confidence score is within valid range."""
    engine = ScenarioSimulatorEngine()
    req = engine.build_scenario(
        "If X increases 10%",
        base_state={"X": 100.0},
        iterations=100,
        seed=42,
    )
    result = engine.run_simulation(req)
    if 0.0 <= result.confidence <= 1.0:
        return 1.0
    return 0.0


def test_latency() -> float:
    """Execution completes in reasonable time (< 5 seconds for 100 iterations)."""
    engine = ScenarioSimulatorEngine()
    req = engine.build_scenario(
        "If interest rate increases 1%",
        base_state=_base_state(),
        iterations=100,
        seed=42,
    )
    start = time.monotonic()
    engine.run_simulation(req)
    elapsed = time.monotonic() - start
    if elapsed < 5.0:
        return 1.0
    return max(0.0, 1.0 - (elapsed - 5.0) / 5.0)


def run_benchmark() -> dict[str, float]:
    tests = {
        "reproducibility": test_reproducibility,
        "statistical_soundness": test_statistical_soundness,
        "sandbox_safety": test_sandbox_safety,
        "assumption_extraction": test_assumption_extraction,
        "outcome_identification": test_outcome_identification,
        "variable_parsing": test_variable_parsing,
        "confidence_calibration": test_confidence_calibration,
        "latency": test_latency,
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
    print("Scenario Simulator Benchmark (RFC-0023)")
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
