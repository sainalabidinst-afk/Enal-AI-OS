"""
Outcome Analyzer — computes statistics from Monte Carlo iteration results.

Analyzes the distribution of simulation outcomes to produce:
- Best case / worst case / most likely scenarios
- Statistical summary (mean, median, std dev, percentiles)
- Histogram for visualization
- Key drivers and assumptions
"""

from __future__ import annotations

import logging
import statistics
from typing import Any

from apps.scenario_simulator.monte_carlo_runner import IterationResult
from apps.scenario_simulator.schemas import (
    DistributionStats,
    OutcomeResult,
    OutcomeType,
    SimulationResult,
)

logger = logging.getLogger(__name__)


class OutcomeAnalyzer:
    """
    Computes statistical analysis from simulation iteration results.

    Usage::

        analyzer = OutcomeAnalyzer()
        distribution = analyzer.compute_distribution(iterations)
        best = analyzer.find_best_case(iterations, distribution)
    """

    HISTOGRAM_BUCKETS = 10

    def analyze(
        self,
        iterations: list[IterationResult],
        title: str,
        description: str,
        request_id: str,
        assumptions: list[str] | None = None,
    ) -> SimulationResult:
        """
        Perform full analysis of simulation results.

        Args:
            iterations: All Monte Carlo iteration results.
            title: Scenario title.
            description: Scenario description.
            request_id: Original request ID.
            assumptions: List of assumptions.

        Returns:
            Complete SimulationResult.
        """
        values = [it.outcome_value for it in iterations]
        distribution = self._compute_distribution(values)

        best_case = self._find_extreme(iterations, values, OutcomeType.BEST_CASE)
        worst_case = self._find_extreme(iterations, values, OutcomeType.WORST_CASE)
        most_likely = self._find_most_likely(iterations, values, distribution)

        key_drivers = self._identify_drivers(iterations)
        confidence = self._compute_confidence(values, len(iterations))

        explanation_chain = self._build_explanation_chain(
            title, description, assumptions or [], key_drivers, distribution,
        )

        return SimulationResult(
            request_id=request_id,
            title=title,
            description=description,
            iterations_run=len(iterations),
            outcomes={
                "best_case": best_case.__dict__,
                "worst_case": worst_case.__dict__,
                "most_likely": most_likely.__dict__,
            },
            distribution=distribution,
            assumptions=assumptions or [],
            key_drivers=key_drivers,
            confidence=confidence,
            explanation_chain=explanation_chain,
        )

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _compute_distribution(self, values: list[float]) -> DistributionStats:
        """Compute statistical distribution from outcome values."""
        if not values:
            return DistributionStats()

        sorted_vals = sorted(values)
        n = len(sorted_vals)

        mean = statistics.mean(values)
        median = statistics.median(values)
        std_dev = statistics.stdev(values) if n > 1 else 0.0
        min_val = min(values)
        max_val = max(values)

        def percentile(data: list[float], p: float) -> float:
            k = (n - 1) * p
            f = int(k)
            c = f + 1 if f + 1 < n else f
            if f == c:
                return data[f]
            weight = k - f
            return data[f] * (1 - weight) + data[c] * weight

        histogram = self._build_histogram(sorted_vals)

        return DistributionStats(
            mean=round(mean, 4),
            median=round(median, 4),
            std_dev=round(std_dev, 4),
            min_value=round(min_val, 4),
            max_value=round(max_val, 4),
            p5=round(percentile(sorted_vals, 0.05), 4),
            p25=round(percentile(sorted_vals, 0.25), 4),
            p75=round(percentile(sorted_vals, 0.75), 4),
            p95=round(percentile(sorted_vals, 0.95), 4),
            histogram=histogram,
        )

    def _build_histogram(self, sorted_values: list[float]) -> list[dict[str, Any]]:
        """Build histogram buckets from sorted values."""
        if not sorted_values:
            return []

        min_val = sorted_values[0]
        max_val = sorted_values[-1]
        if max_val == min_val:
            return [{"bucket": f"[{min_val:.2f}]", "count": len(sorted_values), "range_start": min_val, "range_end": max_val}]

        bucket_size = (max_val - min_val) / self.HISTOGRAM_BUCKETS
        buckets: list[dict[str, Any]] = []

        for i in range(self.HISTOGRAM_BUCKETS):
            lo = min_val + i * bucket_size
            hi = min_val + (i + 1) * bucket_size
            count = sum(1 for v in sorted_values if lo <= v < hi or (i == self.HISTOGRAM_BUCKETS - 1 and v == hi))
            buckets.append({
                "bucket": f"[{lo:.2f}, {hi:.2f}]",
                "count": count,
                "range_start": round(lo, 4),
                "range_end": round(hi, 4),
            })

        return buckets

    def _find_extreme(
        self,
        iterations: list[IterationResult],
        values: list[float],
        outcome_type: OutcomeType,
    ) -> OutcomeResult:
        """Find the best-case or worst-case iteration."""
        if not iterations:
            return OutcomeResult(
                outcome_type=outcome_type,
                value=0.0,
                variables={},
                explanation="No iterations completed.",
            )

        if outcome_type == OutcomeType.BEST_CASE:
            idx = values.index(max(values))
        else:
            idx = values.index(min(values))

        it = iterations[idx]
        explanation = self._format_outcome_explanation(it, outcome_type)

        return OutcomeResult(
            outcome_type=outcome_type,
            value=it.outcome_value,
            variables=it.changed_variables,
            explanation=explanation,
            iteration_index=it.iteration,
        )

    def _find_most_likely(
        self,
        iterations: list[IterationResult],
        values: list[float],
        distribution: DistributionStats,
    ) -> OutcomeResult:
        """Find the iteration closest to the median (most likely)."""
        if not iterations:
            return OutcomeResult(
                outcome_type=OutcomeType.MOST_LIKELY,
                value=0.0,
                variables={},
                explanation="No iterations completed.",
            )

        target = distribution.median
        idx = min(range(len(values)), key=lambda i: abs(values[i] - target))
        it = iterations[idx]

        return OutcomeResult(
            outcome_type=OutcomeType.MOST_LIKELY,
            value=it.outcome_value,
            variables=it.changed_variables,
            explanation=self._format_outcome_explanation(it, OutcomeType.MOST_LIKELY),
            iteration_index=it.iteration,
        )

    def _format_outcome_explanation(
        self, iteration: IterationResult, outcome_type: OutcomeType
    ) -> str:
        """Generate a human-readable explanation for an outcome."""
        parts = []
        for var, val in iteration.changed_variables.items():
            parts.append(f"{var}={val:.4f}")

        label = outcome_type.value.replace("_", " ").title()
        return f"{label}: outcome={iteration.outcome_value:.4f} | variables: {', '.join(parts)}"

    def _identify_drivers(self, iterations: list[IterationResult]) -> list[str]:
        """Identify the most impactful variables across iterations."""
        var_importance: dict[str, list[float]] = {}

        for it in iterations:
            for var, val in it.changed_variables.items():
                var_importance.setdefault(var, []).append(
                    abs(it.outcome_value * val / 100.0) if val != 0 else 0.0
                )

        ranked = sorted(
            var_importance.items(),
            key=lambda x: statistics.mean(x[1]) if x[1] else 0,
            reverse=True,
        )

        return [f"{var}: avg_impact={statistics.mean(vals):.4f}" for var, vals in ranked[:5]]

    def _compute_confidence(self, values: list[float], n: int) -> float:
        """Compute confidence based on sample size and distribution stability."""
        if n < 2:
            return 0.0

        # Confidence increases with sample size, decreases with high variance
        cv = statistics.stdev(values) / (abs(statistics.mean(values)) + 1e-9)
        size_factor = min(1.0, n / 1000.0)
        variance_factor = max(0.0, 1.0 - cv)

        return round(size_factor * variance_factor, 4)

    def _build_explanation_chain(
        self,
        title: str,
        description: str,
        assumptions: list[str],
        drivers: list[str],
        distribution: DistributionStats,
    ) -> dict[str, Any]:
        """Build the axiom → assumption → simulation → prediction chain."""
        return {
            "axioms": [
                f"Scenario: {title}",
                f"Description: {description}",
                f"Based on {distribution.mean:.4f} mean of {distribution.min_value:.4f} to {distribution.max_value:.4f}",
            ],
            "assumptions": assumptions,
            "simulation_logic": (
                f"Ran {distribution.min_value} to {distribution.max_value} range "
                f"with {distribution.histogram[-1]['count'] if distribution.histogram else 0} buckets. "
                f"Mean: {distribution.mean:.4f}, StdDev: {distribution.std_dev:.4f}, "
                f"Median: {distribution.median:.4f}"
            ),
            "outcome_interpretation": (
                f"Best case: {distribution.max_value:.4f}, "
                f"Worst case: {distribution.min_value:.4f}, "
                f"Most likely (median): {distribution.median:.4f}"
            ),
            "key_drivers": drivers,
        }
