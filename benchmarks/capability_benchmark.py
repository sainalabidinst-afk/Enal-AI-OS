"""
Capability Benchmark
=====================

Framework for measuring Capability Pack quality.

Benchmark types:
- Synthetic Benchmark: Structured scenarios with known expected outputs.
- Real-world Benchmark: Cases from actual usage stored in real_cases/.

Quality dimensions:
- Accuracy: correctness of outputs
- Completeness: coverage of domain knowledge
- Explainability: clarity of reasoning
- Safety: adherence to Human Approval and governance rules
- Efficiency: token usage, latency, cost
- Consistency: stability of outputs across repeated runs

Usage:
    from benchmarks.capability_benchmark import CapabilityBenchmark, BenchmarkResult

    class NetworkBenchmark(CapabilityBenchmark):
        capability_id = "network"
        name = "Network Engineer Benchmark"
        description = "Measures network analysis quality across real configs"

        async def run_benchmark(self) -> BenchmarkResult:
            ...

    benchmark = NetworkBenchmark()
    result = await benchmark.run()
    print(f"Score: {result.score}/100")

Real-world cases:
    Store real usage cases in real_cases/<capability_id>/.
    Each case folder should contain input, output, and evaluation.
    See real_cases/README.md for the case template.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from benchmarks.performance_benchmark import Benchmark


@dataclass
class BenchmarkResult:
    capability_id: str
    benchmark_id: str
    name: str
    score: float = 0.0
    max_score: float = 100.0
    accuracy: float = 0.0
    completeness: float = 0.0
    explainability: float = 0.0
    safety: float = 0.0
    efficiency: float = 0.0
    consistency: float = 0.0
    details: dict[str, Any] | None = None
    passed: bool = False

    def __post_init__(self) -> None:
        self.details = self.details or {}


class CapabilityBenchmark(Benchmark, ABC):
    capability_id: str = ""
    name: str = ""
    description: str = ""

    @abstractmethod
    async def run_benchmark(self) -> BenchmarkResult:
        pass

    async def run(self) -> BenchmarkResult:
        result = await self.run_benchmark()
        result.passed = result.score >= 80.0
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "name": self.name,
            "description": self.description,
        }


class CapabilityBenchmarkRegistry:
    def __init__(self) -> None:
        self._benchmarks: dict[str, CapabilityBenchmark] = {}

    def register(self, benchmark: CapabilityBenchmark) -> None:
        if not benchmark.capability_id:
            raise ValueError("capability_id is required")
        self._benchmarks[benchmark.capability_id] = benchmark

    def get(self, capability_id: str) -> CapabilityBenchmark | None:
        return self._benchmarks.get(capability_id)

    def all(self) -> list[CapabilityBenchmark]:
        return list(self._benchmarks.values())


capability_benchmark_registry = CapabilityBenchmarkRegistry()
