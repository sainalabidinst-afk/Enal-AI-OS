"""
Regression test for benchmark adapter runtime contract.

Ensures the benchmark correctly consumes:
- result["decision"]["selected_description"]
- result["action"]["action"]

And NOT the stale assumption:
- result["decision"]["decision"]
"""

import asyncio
from unittest.mock import AsyncMock

import pytest

from benchmarks.performance_benchmark import run_with_metrics, BenchmarkMetrics


def _make_result(decision: dict | None = None, action: dict | None = None, **extra):
    result = {}
    if decision is not None:
        result["decision"] = decision
    if action is not None:
        result["action"] = action
    result.update(extra)
    return result


class TestBenchmarkAdapterRuntimeContract:
    @pytest.mark.asyncio
    async def test_uses_selected_description(self, monkeypatch):
        metrics = BenchmarkMetrics()
        fake_result = _make_result(
            decision={"selected_description": "The answer is 42"},
            action={"action": "calculate"},
        )

        async def fake_execute(user_input: str):
            return fake_result

        monkeypatch.setattr(
            "benchmarks.performance_benchmark.adaptive_runtime.execute",
            fake_execute,
        )

        result = await run_with_metrics("Calculate 2 + 2", metrics)
        assert result["decision"]["selected_description"] == "The answer is 42"
        assert metrics.successes[-1] is True
        assert metrics.latencies[-1] >= 0

    @pytest.mark.asyncio
    async def test_falls_back_to_action_action_when_no_selected_description(self, monkeypatch):
        metrics = BenchmarkMetrics()
        fake_result = _make_result(
            decision={},
            action={"action": "fallback action"},
        )

        async def fake_execute(user_input: str):
            return fake_result

        monkeypatch.setattr(
            "benchmarks.performance_benchmark.adaptive_runtime.execute",
            fake_execute,
        )

        result = await run_with_metrics("Do something", metrics)
        assert result["action"]["action"] == "fallback action"
        assert metrics.successes[-1] is True

    @pytest.mark.asyncio
    async def test_old_decision_decision_is_not_used(self, monkeypatch):
        metrics = BenchmarkMetrics()
        # Only provide the stale field. The benchmark must NOT rely on it.
        fake_result = _make_result(
            decision={"decision": "stale value"},
            action={"action": "real action"},
        )

        captured_output = None

        async def fake_execute(user_input: str):
            return fake_result

        monkeypatch.setattr(
            "benchmarks.performance_benchmark.adaptive_runtime.execute",
            fake_execute,
        )

        result = await run_with_metrics("Legacy path", metrics)
        assert result["action"]["action"] == "real action"
        assert metrics.successes[-1] is True

    @pytest.mark.asyncio
    async def test_success_false_on_error_in_output(self, monkeypatch):
        metrics = BenchmarkMetrics()
        fake_result = _make_result(
            decision={"selected_description": "Error: model not available"},
            action={"action": "error"},
        )

        async def fake_execute(user_input: str):
            return fake_result

        monkeypatch.setattr(
            "benchmarks.performance_benchmark.adaptive_runtime.execute",
            fake_execute,
        )

        await run_with_metrics("Bad request", metrics)
        assert metrics.successes[-1] is False