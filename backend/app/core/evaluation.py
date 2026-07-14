import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class Benchmark:
    id: str
    name: str
    description: str
    test_cases: list[dict[str, Any]]
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


class EvaluationFramework:
    def __init__(self):
        self._benchmarks: dict[str, Benchmark] = {}

    def register_benchmark(self, benchmark: Benchmark):
        self._benchmarks[benchmark.id] = benchmark
        logger.info(f"Benchmark registered: {benchmark.id}")

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
        result.finished_at = datetime.utcnow()
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
        }


evaluation_framework = EvaluationFramework()
