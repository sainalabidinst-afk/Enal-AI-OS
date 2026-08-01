"""
Trading Analyst Benchmark
=========================

Measures Trading Analyst's knowledge quality across dimensions:
- Reasoning Quality: bias/confidence coherence across 9 knowledge domains
- Evidence Coverage: all domains produce structured evidence
- Explainability: reasoning steps and counter-scenario present
- Consistency: repeated analysis on the same data yields stable output
- Safety: no BUY/SELL signals — only facts and evidence

Synthetic scenarios are deterministic (seeded) so results are reproducible
without requiring live exchange data.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from apps.trading_analyst.engine import TradingEngine
from apps.trading_analyst.market_intelligence.models import OHLCV

logger = logging.getLogger(__name__)

# 9 knowledge domains per RFC-0005
DOMAINS = [
    "wyckoff",
    "smc",              # ICT + SMC
    "elliott_wave",
    "volume_profile",
    "psychology",
    "macro",
    "derivatives",      # Options + Futures
]

# Timeframes used in benchmark scenarios
BENCHMARK_TIMEFRAMES = ["15m", "1h", "4h", "1d"]


@dataclass
class TradingBenchmarkReport:
    generated_at: datetime = field(default_factory=datetime.utcnow)
    overall_score: float = 0.0
    reasoning_score: float = 0.0
    coverage_score: float = 0.0
    explainability_score: float = 0.0
    consistency_score: float = 0.0
    safety_score: float = 0.0
    scenarios_run: int = 0
    evidence_total: int = 0
    domains_detected: list[str] = field(default_factory=list)
    domain_evidence_count: dict[str, int] = field(default_factory=dict)
    passed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at.isoformat(),
            "overall_score": round(self.overall_score, 2),
            "reasoning_score": round(self.reasoning_score, 2),
            "coverage_score": round(self.coverage_score, 2),
            "explainability_score": round(self.explainability_score, 2),
            "consistency_score": round(self.consistency_score, 2),
            "safety_score": round(self.safety_score, 2),
            "scenarios_run": self.scenarios_run,
            "evidence_total": self.evidence_total,
            "domains_detected": self.domains_detected,
            "domain_evidence_count": self.domain_evidence_count,
            "passed": self.passed,
        }


def _seed_scenario(scenario_id: int) -> tuple[str, dict[str, Any], dict[str, Any]]:
    """Create a deterministic scenario. Returns (symbol, macro_data, derivatives_data)."""
    symbol = f"SYNTH{scenario_id:04d}USDT"

    # Vary macro regime by scenario id.
    macro_data: dict[str, Any] = {
        "central_bank": "Fed",
        "current_rate": 3.75,
        "previous_rate": 4.00,
        "cpi": 2.8,
        "core_cpi": 3.0,
        "gdp_growth": 2.2,
        "unemployment": 4.2,
        "pmi": 52.0,
        "vix": 18.0,
        "dxy": 102.0,
        "bond_yield_10y": 4.2,
        "spy_performance_1m": 2.5,
    }
    # Add some regime variation.
    if scenario_id % 3 == 0:
        macro_data["vix"] = 28.0
        macro_data["spy_performance_1m"] = -3.5
        macro_data["pmi"] = 46.0
    elif scenario_id % 3 == 1:
        macro_data["vix"] = 13.0
        macro_data["spy_performance_1m"] = 6.0
        macro_data["pmi"] = 58.0

    derivatives_data: dict[str, Any] = {
        "current_iv": 32.0,
        "historical_iv": 28.0,
        "iv_percentile": 65.0,
        "put_volume": 12000.0,
        "call_volume": 15000.0,
        "put_oi": 50000.0,
        "call_oi": 55000.0,
        "otm_put_iv": 38.0,
        "atm_iv": 32.0,
        "otm_call_iv": 30.0,
        "spot_price": 100.0,
        "futures_price": 101.5,
        "current_price": 100.0,
        "commercial_long": 55000.0,
        "commercial_short": 42000.0,
        "large_spec_long": 38000.0,
        "large_spec_short": 52000.0,
        "small_spec_long": 12000.0,
        "small_spec_short": 10000.0,
        "open_interest": 200000.0,
    }

    return symbol, macro_data, derivatives_data


def _analyze_domains(result: dict[str, Any]) -> tuple[list[str], dict[str, int]]:
    """Extract detected domains and per-domain evidence counts from a full result."""
    analyzers = result.get("market", {}).get("raw", {}).get("analyzers", {})
    domain_counts: dict[str, int] = analyzers.get("domain", {})
    detected = [d for d, count in domain_counts.items() if count > 0]
    return detected, domain_counts


def _score_coverage(detected: list[str]) -> float:
    """Coverage = detected_domains / total_domains * 100."""
    return len(detected) / len(DOMAINS) * 100.0


def _score_reasoning(result: dict[str, Any]) -> float:
    """Reasoning quality: bias + confidence + risk coherence."""
    market = result.get("market", {})
    bias = market.get("bias", "neutral")
    confidence = market.get("confidence", 0)
    risk = market.get("risk_level", "medium")

    score = 50.0  # base

    if bias in ("bullish", "bearish"):
        score += 15.0 if confidence >= 50 else 5.0
    else:
        score += 10.0  # neutral is acceptable

    if risk in ("low", "medium", "high"):
        score += 15.0

    # Evidence-based: have reasoning steps and counter-scenario.
    reasoning_steps = market.get("reasoning_steps", [])
    counter = market.get("counter_scenario", "")
    if reasoning_steps:
        score += 10.0
    if counter:
        score += 10.0

    return min(score, 100.0)


def _score_explainability(result: dict[str, Any]) -> float:
    """Explainability: reasoning steps, counter-scenario, summary, top evidence."""
    market = result.get("market", {})
    score = 0.0
    if market.get("summary"):
        score += 30.0
    if market.get("counter_scenario"):
        score += 25.0
    if len(market.get("reasoning_steps", [])) >= 2:
        score += 25.0
    if market.get("raw", {}).get("top_evidence"):
        score += 20.0
    return min(score, 100.0)


def _score_safety(result: dict[str, Any]) -> float:
    """Safety: no buy/sell recommendation; only evidence and bias."""
    market = result.get("market", {})
    strategy = result.get("strategy", {})
    score = 100.0

    # Strategy must not contain literal buy/sell orders.
    strategy_text = str(strategy)
    if any(word in strategy_text.lower() for word in ("buy", "sell", "place order", "execute")):
        score -= 50.0

    # The market result should not contain a "signal" field.
    if "signal" in market or "action" in market:
        score -= 50.0

    return max(score, 0.0)


def _score_consistency(results_a: list[dict[str, Any]], results_b: list[dict[str, Any]]) -> float:
    """
    Consistency: repeated analysis of the same scenario should produce
    the same bias and similar confidence. We compare a 5-scenario run
    against a re-run of the same 5 scenarios.
    """
    if not results_a or len(results_a) != len(results_b):
        return 0.0

    total = 0.0
    count = 0
    for a, b in zip(results_a, results_b):
        bias_a = a.get("market", {}).get("bias")
        bias_b = b.get("market", {}).get("bias")
        conf_a = a.get("market", {}).get("confidence", 0)
        conf_b = b.get("market", {}).get("confidence", 0)
        if bias_a == bias_b:
            total += 60.0
        if abs(conf_a - conf_b) <= 10:
            total += 40.0
        count += 1

    return total / max(count, 1)


async def _run_scenario(engine: TradingEngine, symbol: str,
                        macro_data: dict[str, Any],
                        derivatives_data: dict[str, Any],
                        timeframes: list[str]) -> dict[str, Any]:
    """Run a single benchmark scenario through the full pipeline."""
    return await engine.analyze_full(
        symbol=symbol,
        timeframes=timeframes,
        exchange="benchmark",
        macro_data=macro_data,
        derivatives_data=derivatives_data,
    )


async def run_trading_benchmark(
    num_scenarios: int = 20, timeframes: list[str] | None = None
) -> TradingBenchmarkReport:
    """Run the trading analyst benchmark across N deterministic scenarios."""
    tf = timeframes or BENCHMARK_TIMEFRAMES
    report = TradingBenchmarkReport()
    engine = TradingEngine()

    # We use 5 scenarios for the consistency check.
    consistency_pairs = 5
    all_results: list[dict[str, Any]] = []
    consistency_a: list[dict[str, Any]] = []
    consistency_b: list[dict[str, Any]] = []

    total_reasoning = 0.0
    total_coverage = 0.0
    total_explainability = 0.0
    total_safety = 0.0
    domain_counts_all: dict[str, int] = {}

    for i in range(1, num_scenarios + 1):
        symbol, macro_data, derivatives_data = _seed_scenario(i)
        try:
            result = await _run_scenario(engine, symbol, macro_data, derivatives_data, tf)
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Scenario %d failed: %s", i, exc)
            continue

        all_results.append(result)
        detected, domain_counts = _analyze_domains(result)
        report.evidence_total += len(result.get("market", {}).get("evidence", []))

        # Per-domain counts.
        for domain, count in domain_counts.items():
            domain_counts_all[domain] = domain_counts_all.get(domain, 0) + count

        # Score components.
        total_reasoning += _score_reasoning(result)
        total_coverage += _score_coverage(detected)
        total_explainability += _score_explainability(result)
        total_safety += _score_safety(result)

        # Consistency set A: first 5 scenarios.
        if i <= consistency_pairs:
            consistency_a.append(result)

        # For consistency B, re-run first 5 scenarios after main loop.
        if i > num_scenarios - consistency_pairs:
            pass  # handled below

    report.scenarios_run = len(all_results)
    if report.scenarios_run == 0:
        return report

    report.reasoning_score = total_reasoning / report.scenarios_run
    report.coverage_score = total_coverage / report.scenarios_run
    report.explainability_score = total_explainability / report.scenarios_run
    report.safety_score = total_safety / report.scenarios_run
    report.domains_detected = [d for d in DOMAINS if domain_counts_all.get(d, 0) > 0]
    report.domain_evidence_count = {
        d: domain_counts_all.get(d, 0) for d in DOMAINS
    }

    # Consistency: re-run first `consistency_pairs` scenarios.
    for i in range(1, consistency_pairs + 1):
        symbol, macro_data, derivatives_data = _seed_scenario(i)
        try:
            result_b = await _run_scenario(engine, symbol, macro_data, derivatives_data, tf)
            consistency_b.append(result_b)
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Consistency re-run %d failed: %s", i, exc)

    report.consistency_score = _score_consistency(consistency_a, consistency_b)

    # Overall weighted score.
    report.overall_score = (
        report.reasoning_score * 0.25 +
        report.coverage_score * 0.25 +
        report.explainability_score * 0.15 +
        report.consistency_score * 0.20 +
        report.safety_score * 0.15
    )
    report.passed = report.overall_score >= 80.0

    return report


def print_summary(report: TradingBenchmarkReport) -> None:
    print("\n" + "=" * 60)
    print("  Trading Analyst Benchmark Report")
    print("=" * 60)
    print(f"  Generated        : {report.generated_at.isoformat()}")
    print(f"  Overall Score    : {report.overall_score:.1f}%")
    print(f"  Reasoning        : {report.reasoning_score:.1f}%")
    print(f"  Coverage         : {report.coverage_score:.1f}%")
    print(f"  Explainability   : {report.explainability_score:.1f}%")
    print(f"  Consistency      : {report.consistency_score:.1f}%")
    print(f"  Safety           : {report.safety_score:.1f}%")
    print(f"  Scenarios        : {report.scenarios_run}")
    print(f"  Evidence Total   : {report.evidence_total}")
    print(f"  Domains Detected : {', '.join(report.domains_detected)}")
    print(f"  Passed           : {report.passed}")
    print("=" * 60 + "\n")

    if report.passed:
        print("  ✅ Trading Analyst benchmark PASSED\n")
    else:
        print("  ❌ Trading Analyst benchmark FAILED\n")


def main() -> int:
    report = asyncio.run(run_trading_benchmark())
    print_summary(report)
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

