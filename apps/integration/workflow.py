"""
Workflow Engine
================

Executes integration workflows as a sequence of capability steps.

This is intentionally simple:
- sequential execution
- shared context across steps
- each step is a callable that receives context and returns updated context
- workflow definition is a list of step names/descriptors

Future: this can be extended with YAML definitions, branching, parallelism,
and rollback without changing capability implementations.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Coroutine

from apps.integration.context import CapabilityContext

logger = logging.getLogger(__name__)

StepFunc = Callable[[CapabilityContext], Coroutine[Any, Any, CapabilityContext]]


@dataclass
class WorkflowStep:
    name: str
    func: StepFunc
    description: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class WorkflowResult:
    workflow_id: str
    success: bool
    context: CapabilityContext
    error: str | None = None
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: str | None = None
    latency_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "success": self.success,
            "context": self.context.to_dict(),
            "error": self.error,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "latency_ms": self.latency_ms,
        }


class WorkflowEngine:
    """
    Runs a sequence of capability steps against a shared context.

    Usage:
        engine = WorkflowEngine()
        result = await engine.run("my_workflow", [
            Step("trading_analysis", trading_step),
            Step("knowledge_query", knowledge_step),
            Step("reasoning", reasoning_step),
        ], initial_context)
    """

    def __init__(self) -> None:
        self._steps: dict[str, WorkflowStep] = {}

    def register_step(self, step: WorkflowStep) -> None:
        self._steps[step.name] = step
        logger.debug("Registered workflow step: %s", step.name)

    async def run(
        self,
        workflow_name: str,
        steps: list[WorkflowStep],
        initial_context: CapabilityContext | None = None,
    ) -> WorkflowResult:
        context = initial_context or CapabilityContext(workflow_type=workflow_name)
        context.workflow_type = workflow_name
        start = time.monotonic()

        for step in steps:
            logger.info("Workflow '%s' executing step: %s", workflow_name, step.name)
            context.set_metadata(f"step.{step.name}.status", "running")
            try:
                context = await step.func(context)
                context.set_metadata(f"step.{step.name}.status", "completed")
            except Exception as e:
                logger.exception("Workflow step failed: %s", step.name)
                context.set_metadata(f"step.{step.name}.status", "failed")
                context.set_metadata(f"step.{step.name}.error", str(e))
                return WorkflowResult(
                    workflow_id=context.workflow_id,
                    success=False,
                    context=context,
                    error=f"Step '{step.name}' failed: {e}",
                    completed_at=datetime.now(timezone.utc).isoformat(),
                    latency_ms=(time.monotonic() - start) * 1000,
                )

        context.mark_completed()
        return WorkflowResult(
            workflow_id=context.workflow_id,
            success=True,
            context=context,
            completed_at=datetime.now(timezone.utc).isoformat(),
            latency_ms=(time.monotonic() - start) * 1000,
        )
