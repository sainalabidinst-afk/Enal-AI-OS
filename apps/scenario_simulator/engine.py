"""
Scenario Simulator Engine — domain engine orchestrator.

Orchestrates the full scenario simulation pipeline:
    1. ScenarioBuilder (parse natural language → structured scenario)
    2. MonteCarloRunner (run N iterations with distribution sampling)
    3. SandboxExecutor (optional isolated code experiments)
    4. OutcomeAnalyzer (distribution, best/worst/most-likely, statistics)

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from typing import Any

from apps.scenario_simulator.monte_carlo_runner import MonteCarloRunner
from apps.scenario_simulator.outcome_analyzer import OutcomeAnalyzer
from apps.scenario_simulator.sandbox_executor import SandboxExecutor
from apps.scenario_simulator.scenario_builder import ScenarioBuilder
from apps.scenario_simulator.schemas import (
    ChangeType,
    DistributionType,
    ScenarioRequest,
    SimulationResult,
    VariableChange,
)

logger = logging.getLogger(__name__)


class ScenarioSimulatorEngine:
    """
    Orchestrates the full scenario simulation pipeline.

    Public API::

        engine = ScenarioSimulatorEngine()
        request = engine.build_scenario("If X increases 10%...", base_state)
        result = engine.run_simulation(request)
    """

    def __init__(self) -> None:
        self.builder = ScenarioBuilder()
        self.runner = MonteCarloRunner()
        self.analyzer = OutcomeAnalyzer()
        self.executor = SandboxExecutor()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_scenario(
        self,
        description: str,
        base_state: dict[str, Any] | None = None,
        iterations: int = 100,
        seed: int | None = None,
        use_llm: bool = False,
    ) -> ScenarioRequest:
        """
        Build a structured scenario from natural language.

        Args:
            description: Natural language what-if description.
            base_state: Known base state variables.
            iterations: Monte Carlo iteration count.
            seed: Random seed for reproducibility.
            use_llm: Use LLM parsing (slower but more nuanced).

        Returns:
            ScenarioRequest ready for simulation.
        """
        if use_llm:
            return self.builder.parse_with_llm(description, base_state, iterations, seed)
        return self.builder.build(description, base_state, iterations, seed)

    def run_simulation(
        self,
        request: ScenarioRequest,
        outcome_fn: Callable[[dict[str, Any]], float] | None = None,
    ) -> SimulationResult:
        """
        Run the full simulation pipeline.

        Args:
            request: Structured scenario request.
            outcome_fn: Optional function to compute outcome from state.

        Returns:
            SimulationResult with distribution and outcomes.
        """
        started = time.monotonic()

        # Step 1: Run Monte Carlo iterations
        iterations = self.runner.run(request, outcome_fn)
        logger.info(
            f"Monte Carlo: {len(iterations)} iterations in {time.monotonic() - started:.2f}s"
        )  # noqa: E501

        # Step 2: Optional sandbox experiment
        sandbox_logs: list[dict[str, Any]] = []
        if request.sandbox_enabled and request.sandbox_code:
            import asyncio

            async def _run_sandbox():
                return await self.executor.run_sandbox_batch(
                    request.sandbox_code,
                    [it.state for it in iterations[: min(10, len(iterations))]],
                )

            try:
                loop = asyncio.get_event_loop()
                sandbox_logs = loop.run_until_complete(_run_sandbox())
            except RuntimeError:
                # No running loop
                sandbox_logs = []

        # Step 3: Analyze outcomes
        result = self.analyzer.analyze(
            iterations=iterations,
            title=request.title,
            description=request.description,
            request_id=request.request_id,
            assumptions=request.context.get("assumptions", []),
        )

        # Step 4: Attach sandbox logs
        result.sandbox_logs = sandbox_logs

        # Step 5: Attach timing metadata
        total_ms = (time.monotonic() - started) * 1000.0
        result.raw["latency_ms"] = round(total_ms, 2)
        result.raw["iterations"] = request.iterations
        result.raw["seed"] = request.seed
        result.raw["sandbox_enabled"] = request.sandbox_enabled

        logger.info(
            f"Scenario simulation complete: {total_ms:.1f}ms for {request.iterations} iterations"
        )  # noqa: E501

        return result

    async def run_simulation_async(
        self,
        request: ScenarioRequest,
        outcome_fn: Callable[[dict[str, Any]], float] | None = None,
    ) -> SimulationResult:
        """
        Run the full simulation pipeline (async variant for sandbox support).

        Args:
            request: Structured scenario request.
            outcome_fn: Optional function to compute outcome from state.

        Returns:
            SimulationResult with distribution and outcomes.
        """
        started = time.monotonic()

        # Step 1: Run Monte Carlo iterations (sync, fast)
        iterations = self.runner.run(request, outcome_fn)

        # Step 2: Optional sandbox experiment
        sandbox_logs: list[dict[str, Any]] = []
        if request.sandbox_enabled and request.sandbox_code:
            sandbox_logs = await self.executor.run_sandbox_batch(
                request.sandbox_code,
                [it.state for it in iterations[: min(10, len(iterations))]],
            )

        # Step 3: Analyze outcomes
        result = self.analyzer.analyze(
            iterations=iterations,
            title=request.title,
            description=request.description,
            request_id=request.request_id,
            assumptions=request.context.get("assumptions", []),
        )

        result.sandbox_logs = sandbox_logs

        total_ms = (time.monotonic() - started) * 1000.0
        result.raw["latency_ms"] = round(total_ms, 2)
        result.raw["iterations"] = request.iterations
        result.raw["seed"] = request.seed
        result.raw["sandbox_enabled"] = request.sandbox_enabled

        return result

    def simulate_plan(
        self,
        plan: list[dict[str, Any]],
        context: dict[str, Any],
        iterations: int = 100,
        seed: int | None = None,
    ) -> SimulationResult:
        """
        Simulate a plan under variable conditions (for integration with
        core simulation_engine).

        This wraps the plan steps into a scenario and runs Monte Carlo.
        """
        # Convert plan steps to base state
        base_state: dict[str, Any] = {}
        for step in plan:
            if "expected_result" in step:
                base_state[step.get("description", "unknown")] = 1.0  # baseline success

        # Inject variability based on context
        changes: list[Any] = []  # noqa: F841
        request = ScenarioRequest(
            title="Plan Simulation",
            description=f"Simulating plan under variable conditions: {context.get('scenario', 'unknown')}",  # noqa: E501
            base_state=base_state,
            variable_changes=[],  # Plans are deterministic, no variable changes
            iterations=iterations,
            sandbox_enabled=False,
            seed=seed,
            context=context,
        )

        # Use plan-based outcome function
        def plan_outcome_fn(state: dict[str, Any]) -> float:
            """Simple outcome: fraction of plan steps that succeed."""
            total = len(state)
            if total == 0:
                return 0.5
            successful = sum(1 for v in state.values() if isinstance(v, (int, float)) and v > 0.5)
            return successful / total if total > 0 else 0.5

        return self.run_simulation(request, outcome_fn=plan_outcome_fn)

    def run_trading_analysis(
        self,
        asset: str,
        initial_price: float,
        volatility: float,
        iterations: int = 1000,
        seed: int | None = None,
    ) -> SimulationResult:
        """
        Run Monte Carlo price simulation for Trading Analyst integration.

        Simulates asset price paths using geometric Brownian motion
        with log-normal price distribution.

        Args:
            asset: Asset name (e.g., "BTC-USD").
            initial_price: Starting price of the asset.
            volatility: Annualized volatility (e.g., 0.15 for 15%).
            iterations: Number of Monte Carlo paths.
            seed: Random seed for reproducibility.

        Returns:
            SimulationResult with final price distribution and risk metrics.
        """
        base_state = {"price": initial_price, "volatility": volatility}
        request = ScenarioRequest(
            title=f"Trading Analysis: {asset}",
            description=f"Price simulation for {asset} with volatility {volatility}",
            base_state=base_state,
            variable_changes=[],
            iterations=iterations,
            sandbox_enabled=False,
            seed=seed,
            context={"asset": asset, "type": "trading"},
        )

        def trading_outcome_fn(state: dict[str, Any]) -> float:
            price = state.get("price", initial_price)
            return price

        result = self.run_simulation(request, outcome_fn=trading_outcome_fn)
        result.raw["asset"] = asset
        result.raw["analysis_type"] = "monte_carlo_price"
        return result

    def run_network_simulation(
        self,
        topology: str,
        link_count: int,
        base_latency_ms: float,
        failure_rate: float,
        iterations: int = 100,
        seed: int | None = None,
    ) -> SimulationResult:
        """
        Run network resilience simulation for Network Engineer integration.

        Simulates end-to-end latency under link failures and traffic patterns.

        Args:
            topology: Network topology name (e.g., "mesh", "ring", "star").
            link_count: Number of network links.
            base_latency_ms: Base latency per link in milliseconds.
            failure_rate: Probability of a link failure (0.0–1.0).
            iterations: Number of simulation iterations.
            seed: Random seed for reproducibility.

        Returns:
            SimulationResult with latency distribution and failure impact.
        """
        base_state = {
            "base_latency_ms": base_latency_ms,
            "link_count": link_count,
            "failure_rate": failure_rate,
        }
        request = ScenarioRequest(
            title=f"Network Simulation: {topology}",
            description=f"End-to-end latency for {topology} topology with {link_count} links, {failure_rate:.0%} failure rate",  # noqa: E501
            base_state=base_state,
            variable_changes=[
                VariableChange(
                    variable="effective_latency",
                    change_type=ChangeType.ABSOLUTE_DELTA,
                    value=0,
                    distribution=DistributionType.NORMAL,
                    stddev=base_latency_ms * 0.3,
                )
            ],
            iterations=iterations,
            sandbox_enabled=False,
            seed=seed,
            context={"topology": topology, "type": "network"},
        )

        def network_outcome_fn(state: dict[str, Any]) -> float:
            base = state.get("base_latency_ms", base_latency_ms)
            latency_delta = state.get("effective_latency", 0)
            return base + latency_delta

        result = self.run_simulation(request, outcome_fn=network_outcome_fn)
        result.raw["topology"] = topology
        result.raw["link_count"] = link_count
        result.raw["analysis_type"] = "network_resilience"
        return result

    def run_architecture_review(
        self,
        component_criticality: dict[str, float],
        budget: float,
        risk_tolerance: float = 0.1,
        iterations: int = 100,
        seed: int | None = None,
    ) -> SimulationResult:
        """
        Run architecture risk simulation for System Architect integration.

        Simulates system failure scenarios based on component criticality
        and budget constraints.

        Args:
            component_criticality: Dict mapping component name to criticality score (0-1).
            budget: Available budget for risk mitigation.
            risk_tolerance: Maximum acceptable risk score.
            iterations: Number of simulations.
            seed: Random seed for reproducibility.

        Returns:
            SimulationResult with system risk distribution and budget adequacy.
        """
        base_state = {name: score for name, score in component_criticality.items()}

        request = ScenarioRequest(
            title="Architecture Risk Review",
            description=f"Risk simulation for {len(component_criticality)} components, budget {budget}, risk tolerance {risk_tolerance}",  # noqa: E501
            base_state=base_state,
            variable_changes=[],
            iterations=iterations,
            sandbox_enabled=False,
            seed=seed,
            context={"budget": budget, "risk_tolerance": risk_tolerance, "type": "architecture"},
        )

        def arch_outcome_fn(state: dict[str, Any]) -> float:
            risk_score = sum(v for v in state.values() if isinstance(v, (int, float)))
            budget_used = min(budget / 10.0, 1.0) if budget > 0 else 0.0
            return risk_score - budget_used

        result = self.run_simulation(request, outcome_fn=arch_outcome_fn)
        result.raw["budget"] = budget
        result.raw["risk_tolerance"] = risk_tolerance
        result.raw["analysis_type"] = "architecture_risk"
        return result
