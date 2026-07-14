"""
Benchmark: Agent Response Quality
===================================

This benchmark measures the quality of agent responses across different task types.
"""

import asyncio
from typing import Any
from backend.app.core.evaluation import Benchmark, evaluation_framework
from backend.app.core.adaptive_runtime import adaptive_runtime


async def run_agent_task(case: dict[str, Any]) -> str:
    user_input = case.get("input", "")
    result = await adaptive_runtime.execute(user_input)
    return result.get("decision", {}).get("decision", "")


async def main():
    benchmark = Benchmark(
        id="agent-quality-001",
        name="Agent Response Quality",
        description="Measures agent response quality across task types",
        test_cases=[
            {"input": "Calculate 2 + 2", "expected": "4"},
            {"input": "Write a hello world function", "expected": "def"},
            {"input": "List files", "expected": "files"},
        ],
    )

    evaluation_framework.register_benchmark(benchmark)
    result = await evaluation_framework.run_benchmark(benchmark.id, run_agent_task)

    print(f"Benchmark: {benchmark.name}")
    print(f"Passed: {result.passed}/{result.total}")
    print(f"Pass Rate: {result.passed/result.total:.2%}")


if __name__ == "__main__":
    asyncio.run(main())
