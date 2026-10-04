"""Thin Worker adapter for dynamically synthesized Capability Packs.

The pack is generated at runtime by the Pilar 4 synthesizer, so there is no
static engine type to import. The worker therefore depends on a minimal
``execute`` protocol and fails loudly when no engine has been attached, instead
of raising ``AttributeError: 'NoneType' object has no attribute 'execute'``.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class PackEngine(Protocol):
    """Minimal contract every synthesized pack engine satisfies."""

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]: ...


class SynthesizedPackWorker:
    """Executes tasks against a synthesized pack engine."""

    def __init__(self, engine: PackEngine | None = None) -> None:
        self.engine = engine

    async def run(self, task: dict) -> dict:
        if self.engine is None:
            raise RuntimeError(
                "SynthesizedPackWorker has no engine attached. Call "
                "attach_engine(engine) before run()."
            )
        return await self.engine.execute(task)

    def attach_engine(self, engine: PackEngine) -> None:
        """Bind the synthesized engine that backs this worker."""
        self.engine = engine


synthesized_worker = SynthesizedPackWorker()
