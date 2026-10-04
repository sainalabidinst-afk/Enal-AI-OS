"""Thin Worker adapter for the Benchmark Capability Pack.

The benchmark pack is synthesized at runtime, so there is no static engine type
to import. The worker depends on a minimal ``execute`` protocol and fails loudly
when no engine has been attached, instead of raising
``AttributeError: 'NoneType' object has no attribute 'execute'``.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class BenchmarkEngine(Protocol):
    """Minimal contract the benchmark pack engine satisfies."""

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]: ...


class BenchmarkPackWorker:
    """Executes benchmark tasks against the synthesized engine."""

    def __init__(self, engine: BenchmarkEngine | None = None) -> None:
        self.engine = engine

    async def run(self, task: dict) -> dict:
        if self.engine is None:
            raise RuntimeError(
                "BenchmarkPackWorker has no engine attached. Call "
                "attach_engine(engine) before run()."
            )
        return await self.engine.execute(task)

    def attach_engine(self, engine: BenchmarkEngine) -> None:
        """Bind the synthesized engine that backs this worker."""
        self.engine = engine


benchmark_pack_worker = BenchmarkPackWorker()
