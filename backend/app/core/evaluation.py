import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class QualityGate:
    name: str
    threshold: float  # 0.0 - 1.0
    metric: str
    required: bool = True


@dataclass
class Benchmark:
    id: str
    name: str
    description: str
    test_cases: list[dict[str, Any]]
    quality_gates: list[QualityGate] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkResult:
    benchmark_id: str
    passed: int = 0
    failed: int = 0
    total: int = 0
    results: list[dict[str, Any]] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.utcnow)
    finished_at: datetime | None = None
    gate_results: dict[str, bool] = field(default_factory=dict)


class EvaluationFramework:
    def __init__(self):
        self._benchmarks: dict[str, Benchmark] = {}
        self._gate_history: list[dict[str, Any]] = []

    def register_benchmark(self, benchmark: Benchmark):
        self._benchmarks[benchmark.id] = benchmark
        logger.info(f"Benchmark registered: {benchmark.id}")

    def add_quality_gate(self, benchmark_id: str, gate: QualityGate) -> bool:
        benchmark = self._benchmarks.get(benchmark_id)
        if not benchmark:
            return False
        benchmark.quality_gates.append(gate)
        return True

    async def run_benchmark(self, benchmark_id: str, run_fn) -> BenchmarkResult:
        benchmark = self._benchmarks.get(benchmark_id)
        if not benchmark:
            raise ValueError(f"Benchmark not found: {benchmark_id}")
        result = BenchmarkResult(benchmark_id=benchmark_id, total=len(benchmark.test_cases))
        for case in benchmark.test_cases:
            try:
                output = await run_fn(case)
                passed = self._evaluate(case, output)
                result.results.append({"case": case, "passed": passed, "output": output})
                if passed:
                    result.passed += 1
                else:
                    result.failed += 1
            except Exception as e:
                result.failed += 1
                result.results.append({"case": case, "passed": False, "error": str(e)})
        result.finished_at = datetime.now(timezone.utc)

        # Evaluate quality gates
        pass_rate = result.passed / result.total if result.total > 0 else 0
        for gate in benchmark.quality_gates:
            gate_passed = pass_rate >= gate.threshold
            result.gate_results[gate.name] = gate_passed
            self._gate_history.append({
                "benchmark_id": benchmark_id,
                "gate_name": gate.name,
                "metric": gate.metric,
                "threshold": gate.threshold,
                "actual": pass_rate,
                "passed": gate_passed,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        return result

    def _evaluate(self, case: dict[str, Any], output: Any) -> bool:
        expected = case.get("expected")
        if expected is None:
            return True
        return str(output).strip().lower() == str(expected).strip().lower()

    def get_summary(self, result: BenchmarkResult) -> dict[str, Any]:
        return {
            "benchmark_id": result.benchmark_id,
            "passed": result.passed,
            "failed": result.failed,
            "total": result.total,
            "pass_rate": result.passed / result.total if result.total > 0 else 0,
            "gate_results": result.gate_results,
            "all_gates_passed": all(result.gate_results.values()),
        }

    def get_gate_history(self, benchmark_id: str | None = None) -> list[dict[str, Any]]:
        if benchmark_id:
            return [g for g in self._gate_history if g["benchmark_id"] == benchmark_id]
        return list(self._gate_history)


evaluation_framework = EvaluationFramework()

