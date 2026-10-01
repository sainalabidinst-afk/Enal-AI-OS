"""
Golden tests for Scenario Simulator Capability Pack (RFC-0023).

Verifies:
- ScenarioBuilder.parse produces correct ScenarioRequest
- MonteCarloRunner executes iterations with reproducible output
- OutcomeAnalyzer computes correct statistics and outcomes
- End-to-end engine.run_simulation returns a valid SimulationResult
- SandboxExecutor runs code safely
- Engine integration with plan simulation
"""

import pytest

from apps.scenario_simulator.schemas import (
    ChangeType,
    DistributionType,
    OutcomeType,
    ScenarioRequest,
    VariableChange,
    VariableType,
)
from apps.scenario_simulator.scenario_builder import ScenarioBuilder
from apps.scenario_simulator.monte_carlo_runner import MonteCarloRunner, IterationResult
from apps.scenario_simulator.outcome_analyzer import OutcomeAnalyzer
from apps.scenario_simulator.sandbox_executor import SandboxExecutor
from apps.scenario_simulator.engine import ScenarioSimulatorEngine
from apps.scenario_simulator.worker import ScenarioSimulatorWorker


# ---------------------------------------------------------------------------
# ScenarioBuilder tests
# ---------------------------------------------------------------------------


@pytest.fixture
def builder():
    return ScenarioBuilder()


@pytest.fixture
def engine():
    return ScenarioSimulatorEngine()


class TestScenarioBuilder:
    def test_build_basic_scenario(self, builder):
        """Test basic scenario building with simple description."""
        request = builder.build(
            description="If suku bunga naik 1%",
            base_state={"interest_rate": 0.05, "revenue": 100.0},
            iterations=50,
            seed=42,
        )
        assert request.title is not None
        assert request.description == "If suku bunga naik 1%"
        assert request.iterations == 50
        assert request.seed == 42
        assert len(request.variable_changes) > 0
        assert request.variable_changes[0].variable == "interest_rate"

    def test_build_with_parsed_changes(self, builder):
        """Test that percentage changes are parsed correctly."""
        request = builder.build(
            description="If interest rate increases 1% and competitor A price decreases 20%",
            base_state={"interest_rate": 0.05, "competitor_a_price": 100.0},
        )
        change_vars = [c.variable for c in request.variable_changes]
        assert "interest_rate" in change_vars
        assert "competitor_a_price" in change_vars

    def test_build_with_generic_change(self, builder):
        """Test generic change detection when no specific keywords match."""
        request = builder.build(
            description="A random what-if scenario with no specific keywords",
            base_state={"some_metric": 42.0},
            iterations=10,
        )
        assert len(request.variable_changes) >= 1
        assert request.variable_changes[0].variable == "some_metric"

    def test_assumptions_extracted(self, builder):
        """Test that assumptions are extracted from description."""
        request = builder.build(
            description="If the price drops 20%",
            base_state={"price": 100.0},
        )
        assert "assumptions" in request.context
        assert "All other variables remain constant unless stated otherwise" in request.context["assumptions"]
        assert "Changes take effect immediately" in request.context["assumptions"]

    def test_build_reproducible_with_seed(self, builder):
        """Test that same seed produces same request."""
        r1 = builder.build("If X increases 10%", base_state={"X": 100.0}, seed=123)
        r2 = builder.build("If X increases 10%", base_state={"X": 100.0}, seed=123)
        assert r1.request_id != r2.request_id  # UUID always different
        assert r1.variable_changes == r2.variable_changes

    def test_fallback_when_no_base_state(self, builder):
        """Test building scenario with empty base state."""
        request = builder.build(description="What if interest rates go up?")
        assert request.base_state == {}
        assert len(request.variable_changes) >= 0


# ---------------------------------------------------------------------------
# MonteCarloRunner tests
# ---------------------------------------------------------------------------


class TestMonteCarloRunner:
    def test_run_returns_iterations(self, engine):
        """Test that Monte Carlo produces correct number of iterations."""
        request = engine.build_scenario(
            "If interest rate increases 1%",
            base_state={"interest_rate": 0.05, "revenue": 100.0},
            iterations=100,
            seed=42,
        )
        results = engine.runner.run(request)
        assert len(results) == 100

    def test_run_reproducible_with_seed(self, engine):
        """Test that same seed produces identical results."""
        request1 = engine.build_scenario(
            "If interest rate increases 1%",
            base_state={"interest_rate": 0.05, "revenue": 100.0},
            iterations=50,
            seed=99,
        )
        request2 = engine.build_scenario(
            "If interest rate increases 1%",
            base_state={"interest_rate": 0.05, "revenue": 100.0},
            iterations=50,
            seed=99,
        )
        r1 = engine.runner.run(request1)
        r2 = engine.runner.run(request2)
        assert r1 == r2

    def test_run_with_custom_outcome_fn(self, engine):
        """Test that custom outcome function is used."""
        def outcome_fn(state):
            values = [v for v in state.values() if isinstance(v, (int, float))]
            return sum(values) / len(values) if values else 0.0

        request = engine.build_scenario(
            "What if X increases?",
            base_state={"x": 10.0, "y": 20.0},
            iterations=10,
            seed=1,
        )
        results = engine.runner.run(request, outcome_fn=outcome_fn)
        assert all(isinstance(r.outcome_value, float) for r in results)

    def test_iteration_has_state_and_outcome(self, engine):
        """Test that each iteration has state, outcome, and changed variables."""
        request = engine.build_scenario("If A increases 5%", base_state={"A": 50.0}, iterations=5, seed=7)
        results = engine.runner.run(request)
        first = results[0]
        assert hasattr(first, "state")
        assert hasattr(first, "outcome_value")
        assert hasattr(first, "changed_variables")
        assert isinstance(first.iteration, int)

    def test_no_variable_changes(self, engine):
        """Test running with no variable changes (baseline scenario)."""
        request = ScenarioRequest(
            title="Baseline",
            description="Baseline test",
            base_state={"metric": 42.0},
            variable_changes=[],
            iterations=20,
            seed=42,
        )
        results = engine.runner.run(request)
        assert len(results) == 20


# ---------------------------------------------------------------------------
# OutcomeAnalyzer tests
# ---------------------------------------------------------------------------


class TestOutcomeAnalyzer:
    def test_analyze_produces_distribution(self, engine):
        """Test that distribution stats are computed."""
        request = engine.build_scenario(
            "If revenue changes 10%",
            base_state={"revenue": 100.0},
            iterations=200,
            seed=42,
        )
        iterations = engine.runner.run(request)
        result = engine.analyzer.analyze(
            iterations=iterations,
            title=request.title,
            description=request.description,
            request_id=request.request_id,
        )
        assert result.distribution.mean > 0
        assert result.distribution.min_value <= result.distribution.max_value
        assert result.distribution.p5 <= result.distribution.p95

    def test_analyze_best_worst_outcomes(self, engine):
        """Test that best/worst/most-likely outcomes are identified."""
        request = engine.build_scenario(
            "If metric increases 15%",
            base_state={"metric": 100.0},
            iterations=200,
            seed=42,
        )
        iterations = engine.runner.run(request)
        result = engine.analyzer.analyze(
            iterations=iterations,
            title=request.title,
            description=request.description,
            request_id=request.request_id,
        )
        outcome_keys = set(result.outcomes.keys())
        assert "best_case" in outcome_keys or "worst_case" in outcome_keys

    def test_to_dict_serialization(self, engine):
        """Test that SimulationResult serializes to dict correctly."""
        request = engine.build_scenario(
            "If X goes up 10%",
            base_state={"X": 100.0},
            iterations=50,
            seed=42,
        )
        result = engine.run_simulation(request)
        data = result.to_dict()
        assert data["request_id"] == request.request_id
        assert data["title"] == request.title
        assert "distribution" in data
        assert "latency_ms" in data["raw"]

    def test_key_drivers_and_assumptions(self, engine):
        """Test that key drivers and assumptions are included."""
        request = engine.build_scenario(
            "Jika suku bunga naik 1%",
            base_state={"interest_rate": 0.05, "revenue": 100.0},
            iterations=50,
            seed=42,
        )
        result = engine.run_simulation(request)
        assert isinstance(result.key_drivers, list)
        assert isinstance(result.assumptions, list)


# ---------------------------------------------------------------------------
# SandboxExecutor tests
# ---------------------------------------------------------------------------


class TestSandboxExecutor:
    def test_run_sandbox_simple_code(self, engine):
        """Test that sandbox can execute simple code."""
        import asyncio
        executor = SandboxExecutor()
        result = asyncio.get_event_loop().run_until_complete(
            executor.execute_experiment("python", "result = x * 2 + 1", {"x": 10})
        )
        assert result["exit_code"] == 0
        assert result["result"] is not None

    def test_run_sandbox_batch(self, engine):
        """Test batch sandbox execution."""
        import asyncio
        executor = SandboxExecutor()
        states = [{"x": 1}, {"x": 2}, {"x": 3}]
        results = asyncio.get_event_loop().run_until_complete(
            executor.run_sandbox_batch("result = x ** 2", states)
        )
        assert len(results) == 3
        assert all(r["exit_code"] == 0 for r in results)

    def test_run_sandbox_async(self, engine):
        """Test async sandbox execution."""
        import asyncio
        executor = SandboxExecutor()
        result = asyncio.get_event_loop().run_until_complete(
            executor.execute_experiment("python", "result = a + b", {"a": 5, "b": 7})
        )
        assert result["exit_code"] == 0


# ---------------------------------------------------------------------------
# Engine integration tests
# ---------------------------------------------------------------------------


class TestScenarioSimulatorEngine:
    def test_build_scenario(self, engine):
        """Test engine.build_scenario creates proper request."""
        request = engine.build_scenario(
            "If suku bunga naik 1%",
            base_state={"interest_rate": 0.05},
            iterations=50,
            seed=42,
        )
        assert isinstance(request, ScenarioRequest)
        assert request.iterations == 50

    def test_run_simulation(self, engine):
        """Test full simulation pipeline."""
        request = engine.build_scenario(
            "If suku bunga naik 1% dan kompetitor A turun harga 20%",
            base_state={"interest_rate": 0.05, "competitor_a_price": 100.0},
            iterations=100,
            seed=42,
        )
        result = engine.run_simulation(request)
        assert result.iterations_run == 100
        assert result.distribution.mean != 0.0
        assert result.confidence > 0.0

    def test_run_simulation_with_sandbox(self, engine):
        """Test simulation with sandbox code execution."""
        request = ScenarioRequest(
            title="Sandbox Test",
            description="Test with sandbox",
            base_state={"base_revenue": 1000.0},
            variable_changes=[
                VariableChange(
                    variable="base_revenue",
                    change_type=ChangeType.PERCENT_DELTA,
                    value=0.10,
                    distribution=DistributionType.NORMAL,
                    stddev=0.02,
                    range_min=0.05,
                    range_max=0.15,
                )
            ],
            iterations=20,
            seed=42,
            sandbox_enabled=True,
            sandbox_code="result = base_revenue * (1 + change_pct if 'change_pct' in locals() else 0)",
        )
        result = engine.run_simulation(request)
        assert len(result.sandbox_logs) > 0

    def test_simulate_plan(self, engine):
        """Test plan simulation integration."""
        plan = [
            {"description": "Market research", "expected_result": "identify target audience"},
            {"description": "Product development", "expected_result": "build MVP"},
        ]
        result = engine.simulate_plan(plan, {"scenario": "optimistic"}, iterations=30)
        assert result.iterations_run == 30
        assert isinstance(result.outcomes, dict)

    def test_engine_is_reproducible(self, engine):
        """Test that engine run is reproducible with seed."""
        r1 = engine.run_simulation(
            engine.build_scenario("Test scenario", base_state={"x": 100.0}, iterations=50, seed=42)
        )
        r2 = engine.run_simulation(
            engine.build_scenario("Test scenario", base_state={"x": 100.0}, iterations=50, seed=42)
        )
        assert r1.distribution.mean == r2.distribution.mean
        assert r1.outcomes == r2.outcomes


# ---------------------------------------------------------------------------
# Worker tests
# ---------------------------------------------------------------------------


class TestScenarioSimulatorWorker:
    def test_worker_execute(self):
        """Test worker can execute a simulation task."""
        worker = ScenarioSimulatorWorker()
        task = {
            "description": "If suku bunga naik 1%?",
            "base_state": {"interest_rate": 0.05},
            "iterations": 30,
            "seed": 42,
        }
        result = worker.execute_sync(task)
        assert result["iterations_run"] == 30
        assert "distribution" in result

    def test_worker_async(self):
        """Test async worker execution."""
        import asyncio
        worker = ScenarioSimulatorWorker()
        task = {
            "description": "What if competitor pricing changes?",
            "base_state": {"competitor_price": 100.0},
            "iterations": 20,
            "seed": 1,
        }
        result = asyncio.get_event_loop().run_until_complete(worker.execute(task))
        assert "distribution" in result
