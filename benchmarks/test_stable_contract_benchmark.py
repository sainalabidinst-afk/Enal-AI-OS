"""
Pytest suite for stable contract benchmark.

Converts the standalone benchmark script into pytest-collectible tests so it
can run in CI alongside the rest of the test suite.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from benchmarks.stable_contract_benchmark import BenchmarkResult, _BenchApp, main


def test_bench_app_interface() -> None:
    app = _BenchApp()
    assert app.name == "bench-app"
    assert app.version == "1.0.0"
    assert app.get_capabilities() == [{"id": "bench.cap", "name": "Bench"}]


def test_benchmark_result_round_trip() -> None:
    result = BenchmarkResult(
        name="r1",
        dimension="cross_pack",
        passed=True,
        latency_ms=12.5,
        extra={"detail": "ok"},
    )
    data = result.to_dict()
    assert data["name"] == "r1"
    assert data["passed"] is True
    assert data["latency_ms"] == 12.5


@pytest.mark.asyncio
async def test_stable_contract_benchmark_produces_report() -> None:
    report_file = Path("benchmarks/reports/stable_contract_benchmark.json")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    await main()
    assert report_file.exists()
    payload = json.loads(report_file.read_text(encoding="utf-8"))
    assert "overall_pass_rate" in payload
    assert "dimensions" in payload
