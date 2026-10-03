"""
Monte Carlo Runner — runs repeated simulation iterations.

For each iteration, variable changes are sampled from their distributions
and combined with the base state to produce a scenario state. The outcome
for each iteration is computed and collected for statistical analysis.
"""

from __future__ import annotations

import logging
import random
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any

from apps.scenario_simulator.schemas import (
    ChangeType,
    DistributionType,
    ScenarioRequest,
    VariableChange,
)

logger = logging.getLogger(__name__)


@dataclass
class IterationResult:
    """Result of a single Monte Carlo iteration."""

    iteration: int
    state: dict[str, Any]
    outcome_value: float
    changed_variables: dict[str, float]
    assumptions_met: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


class MonteCarloRunner:
    """
    Runs Monte Carlo iterations over a scenario specification.

    Usage::

        runner = MonteCarloRunner()
        results = runner.run(request, outcome_fn)
    """

    def __init__(self) -> None:
        self._rng: random.Random = random.Random()

    def run(
        self,
        request: ScenarioRequest,
        outcome_fn: Callable[[dict[str, Any]], float] | None = None,
    ) -> list[IterationResult]:
        """
        Run Monte Carlo iterations for the given scenario.

        Args:
            request: The scenario request with variables and changes.
            outcome_fn: Optional function that computes the outcome value
                        from a state dict. If None, uses heuristic scoring.

        Returns:
            List of IterationResult, one per iteration.
        """
        self._rng = random.Random(request.seed) if request.seed else random.Random()
        self._changes_by_var = {c.variable: c for c in request.variable_changes}

        base_state = dict(request.base_state) if request.base_state else {}
        outcomes: list[IterationResult] = []

        for i in range(request.iterations):
            changed_vars = self._sample_changes(request.variable_changes)
            state = self._apply_changes(base_state, changed_vars)
            outcome_value = self._compute_outcome(state, outcome_fn)

            outcomes.append(
                IterationResult(
                    iteration=i,
                    state=dict(state),
                    outcome_value=outcome_value,
                    changed_variables=changed_vars,
                    assumptions_met=[],
                )
            )

        return outcomes

    def run_parallel(
        self,
        request: ScenarioRequest,
        outcome_fn: Callable[[dict[str, Any]], float] | None = None,
        max_workers: int = 4,
    ) -> list[IterationResult]:
        """
        Run Monte Carlo iterations in parallel using a thread pool.

        Use this when the outcome function is I/O-bound (e.g., calling external
        services or APIs). For CPU-bound pure-Python outcome functions, prefer
        ``run()`` to avoid GIL contention overhead.

        Args:
            request: The scenario request with variables and changes.
            outcome_fn: Optional function that computes the outcome value.
            max_workers: Thread pool size (default 4).

        Returns:
            List of IterationResult, one per iteration (ordered by iteration index).
        """
        self._rng = random.Random(request.seed) if request.seed else random.Random()
        self._changes_by_var = {c.variable: c for c in request.variable_changes}
        base_state = dict(request.base_state) if request.base_state else {}

        def _run_single(i: int) -> IterationResult:
            changed_vars = self._sample_changes(request.variable_changes)
            state = self._apply_changes(base_state, changed_vars)
            outcome_value = self._compute_outcome(state, outcome_fn)
            return IterationResult(
                iteration=i,
                state=dict(state),
                outcome_value=outcome_value,
                changed_variables=changed_vars,
                assumptions_met=[],
            )

        results: list[IterationResult] = [None] * request.iterations  # type: ignore[list-item]
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_run_single, i): i for i in range(request.iterations)}
            for future in as_completed(futures):
                idx = futures[future]
                results[idx] = future.result()

        return results

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _sample_changes(self, changes: list[VariableChange]) -> dict[str, float]:
        """Sample values for each variable change from its distribution."""
        sampled: dict[str, float] = {}
        for change in changes:
            sampled[change.variable] = self._sample_value(change)
        return sampled

    def _sample_value(self, change: VariableChange) -> float:
        """Sample a single value from a variable change's distribution."""
        if change.distribution == DistributionType.FIXED:
            return change.value

        if change.distribution == DistributionType.UNIFORM:
            lo = change.range_min if change.range_min is not None else change.value * 0.5
            hi = change.range_max if change.range_max is not None else change.value * 1.5
            return self._rng.uniform(lo, hi)

        if change.distribution == DistributionType.NORMAL:
            std = change.stddev if change.stddev is not None else abs(change.value) * 0.1
            return self._rng.gauss(change.value, std)

        if change.distribution == DistributionType.TRIANGULAR:
            lo = change.range_min if change.range_min is not None else 0.0
            hi = change.range_max if change.range_max is not None else change.value * 2
            mode = change.mode if change.mode is not None else change.value
            return self._rng.triangular(lo, hi, mode)

        if change.distribution == DistributionType.BETA:
            alpha = max(1.0, change.value * 10)
            beta = max(1.0, (1.0 - change.value) * 10)
            return self._rng.betavariate(alpha, beta)

        if change.distribution == DistributionType.LOGNORMAL:
            mu = change.value
            sigma = change.stddev if change.stddev is not None else 0.5
            return self._rng.lognormvariate(mu, sigma)

        return change.value

    def _apply_changes(
        self, base_state: dict[str, Any], changes: dict[str, float]
    ) -> dict[str, Any]:
        """Apply sampled changes to the base state."""
        state = dict(base_state)
        changes_by_var = getattr(self, "_changes_by_var", {})
        for var_name, new_value in changes.items():
            if var_name not in state:
                state[var_name] = new_value
            else:
                original = state[var_name]
                change = changes_by_var.get(var_name)

                if isinstance(original, (int, float)):
                    if change and change.change_type == ChangeType.PERCENT_DELTA:
                        state[var_name] = original * (1 + new_value)
                    elif change and change.change_type == ChangeType.SET_VALUE:
                        state[var_name] = new_value
                    else:
                        state[var_name] = original + new_value
                else:
                    state[var_name] = new_value
        return state

    def _compute_outcome(
        self,
        state: dict[str, Any],
        outcome_fn: Callable[[dict[str, Any]], float] | None,
    ) -> float:
        """Compute the outcome value for a given state."""
        if outcome_fn:
            try:
                return float(outcome_fn(state))
            except (TypeError, ValueError):
                logger.warning("Outcome function failed, using heuristic")

        # Heuristic: simple weighted sum of numeric changes
        total_change = 0.0
        for key, value in state.items():
            if isinstance(value, (int, float)):
                total_change += float(value)
        return total_change
