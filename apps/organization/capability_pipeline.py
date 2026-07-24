"""
Capability Pipeline
====================

Sequential orchestrator for executing multiple capabilities in order.

Pipeline hanya mengorkestrasi urutan.
Bukan planner.
Tidak memilih capability secara otomatis.
Urutan capability diberikan sebagai input.

Flow:
    PipelineRequest
        ↓
    Step 1: Capability A ──→ ExecutionResponse
        ↓ (pass output as input)
    Step 2: Capability B ──→ ExecutionResponse
        ↓ (pass output as input)
    Step 3: Capability C ──→ ExecutionResponse
        ↓
    Unified PipelineResponse

On failure at any step:
    - Pipeline stops immediately
    - Failure is propagated to the unified response
    - Previous successful results are preserved
"""

import asyncio
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from apps.organization.capability_execution_engine import (
    CapabilityExecutionEngine,
    ExecutionRequest,
    ExecutionResponse,
    ExecutionStatus,
    TelemetryRecord,
    capability_execution_engine,
)

logger = logging.getLogger(__name__)


@dataclass
class PipelineStep:
    """A single step in the pipeline.

    Attributes:
        capability_id: The capability to execute at this step.
        input_data: Input data for this step. Can use {prev.result} template
                    to reference the previous step's result.
        alias: Optional friendly name for this step (used in telemetry).
        metadata: Additional metadata passed to the execution engine.
    """
    capability_id: str
    input_data: dict[str, Any]
    alias: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.alias:
            self.alias = self.capability_id


@dataclass
class PipelineRequest:
    """Standardized input contract for pipeline execution.

    Attributes:
        steps: Ordered list of capabilities to execute sequentially.
        pipeline_id: Unique identifier for this pipeline run.
        correlation_id: Groups multiple pipeline runs under a single request.
        metadata: Additional context (e.g., project_id, user_id).
    """
    steps: list[PipelineStep]
    pipeline_id: str = ""
    correlation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.pipeline_id:
            self.pipeline_id = f"pipeline-{uuid.uuid4().hex[:12]}"
        if not self.correlation_id:
            self.correlation_id = self.pipeline_id


@dataclass
class StepResult:
    """Result of a single pipeline step.

    Attributes:
        step_index: 0-based index in the pipeline.
        capability_id: The capability that was executed.
        alias: Friendly name for this step.
        status: Execution status (COMPLETED or FAILED).
        result: The capability execution result payload.
        error: Error message if failed.
        execution_time_ms: Time taken for this step.
        execution_id: The engine execution ID for this step.
        telemetry: Telemetry record from the engine.
    """
    step_index: int
    capability_id: str
    alias: str
    status: ExecutionStatus
    result: Any
    error: str | None
    execution_time_ms: float
    execution_id: str
    telemetry: TelemetryRecord | None = None


@dataclass
class PipelineResponse:
    """Standardized output contract for pipeline execution.

    Attributes:
        pipeline_id: Matches the request pipeline_id.
        correlation_id: Matches the request correlation_id.
        status: Overall pipeline status (COMPLETED if all steps passed, FAILED otherwise).
        steps: Results for each step in order.
        total_time_ms: Total pipeline execution time.
        step_count: Number of steps executed.
        failed_step: Index of the step that failed (None if all passed).
        error: Overall error message (None on success).
        error_step: The capability_id of the step that failed (None on success).
    """
    pipeline_id: str
    correlation_id: str
    status: ExecutionStatus
    steps: list[StepResult]
    total_time_ms: float
    step_count: int
    failed_step: int | None = None
    error: str | None = None
    error_step: str | None = None


class CapabilityPipeline:
    """Sequential pipeline that orchestrates capability execution.

    Pipeline adalah EXECUTOR ORCHESTRATOR, bukan planner.
    Ia hanya menjalankan urutan capability yang diberikan.

    Responsibilities:
        - Accept PipelineRequest with ordered steps
        - Execute each step sequentially via CapabilityExecutionEngine
        - Pass previous step's result as input to next step
        - Stop on first failure and propagate error
        - Collect telemetry from all steps
        - Return unified PipelineResponse
    """

    def __init__(
        self,
        engine: CapabilityExecutionEngine | None = None,
    ):
        self._engine = engine or capability_execution_engine

    async def execute(self, request: PipelineRequest) -> PipelineResponse:
        """Execute all pipeline steps sequentially.

        Flow:
            1. For each step in order:
                a. Resolve input (pass previous result if applicable)
                b. Create ExecutionRequest
                c. Execute via engine
                d. Collect step result
                e. If failed → break
            2. Build unified PipelineResponse

        Args:
            request: The pipeline request with ordered steps.

        Returns:
            PipelineResponse with results for all executed steps.
        """
        start_time = time.monotonic()
        step_results: list[StepResult] = []
        previous_result: dict[str, Any] | None = None
        failed_step: int | None = None
        error_message: str | None = None
        error_step: str | None = None

        for idx, step in enumerate(request.steps):
            # ── Resolve input data ──
            resolved_input = self._resolve_input(
                step.input_data,
                previous_result,
                idx,
            )

            # ── Build execution request ──
            exec_request = ExecutionRequest(
                capability_id=step.capability_id,
                input_data=resolved_input,
                execution_id=f"exec-{request.pipeline_id[:8]}-step{idx}",
                correlation_id=request.correlation_id,
                metadata={
                    "pipeline_id": request.pipeline_id,
                    "step_index": idx,
                    "step_alias": step.alias,
                    **request.metadata,
                    **step.metadata,
                },
            )

            # ── Execute via engine ──
            logger.info(
                "Pipeline step %d/%d: executing capability '%s' (%s)",
                idx + 1,
                len(request.steps),
                step.capability_id,
                step.alias,
            )

            try:
                response: ExecutionResponse = await self._engine.execute(exec_request)
            except Exception as exc:
                # Engine-level crash (not a capability error, but infrastructure)
                logger.exception(
                    "Pipeline step %d crashed: capability='%s' error=%s",
                    idx,
                    step.capability_id,
                    exc,
                )
                response = ExecutionResponse(
                    status=ExecutionStatus.FAILED,
                    result=None,
                    error=f"Pipeline infrastructure error: {exc}",
                    execution_time_ms=0.0,
                    execution_id=exec_request.execution_id,
                    correlation_id=request.correlation_id,
                )

            # ── Record step result ──
            step_result = StepResult(
                step_index=idx,
                capability_id=step.capability_id,
                alias=step.alias,
                status=response.status,
                result=response.result,
                error=response.error,
                execution_time_ms=response.execution_time_ms,
                execution_id=response.execution_id,
                telemetry=response.telemetry,
            )
            step_results.append(step_result)

            # ── Check for failure ──
            if response.status in (ExecutionStatus.FAILED, ExecutionStatus.CANCELLED):
                failed_step = idx
                error_message = response.error or f"Step '{step.alias}' failed"
                error_step = step.capability_id
                logger.warning(
                    "Pipeline stopped at step %d/%d: capability='%s' failed: %s",
                    idx + 1,
                    len(request.steps),
                    step.capability_id,
                    error_message,
                )
                break

            # ── Store result for next step ──
            previous_result = response.result

        # ── Build unified response ──
        total_time_ms = (time.monotonic() - start_time) * 1000
        overall_status = (
            ExecutionStatus.COMPLETED
            if failed_step is None
            else ExecutionStatus.FAILED
        )

        logger.info(
            "Pipeline completed: pipeline_id=%s status=%s steps=%d total_time=%.2fms",
            request.pipeline_id,
            overall_status.value,
            len(step_results),
            total_time_ms,
        )

        return PipelineResponse(
            pipeline_id=request.pipeline_id,
            correlation_id=request.correlation_id,
            status=overall_status,
            steps=step_results,
            total_time_ms=total_time_ms,
            step_count=len(step_results),
            failed_step=failed_step,
            error=error_message,
            error_step=error_step,
        )

    # ──────────────────────────────────────────────
    # Internal
    # ──────────────────────────────────────────────

    def _resolve_input(
        self,
        step_input: dict[str, Any],
        previous_result: dict[str, Any] | None,
        step_index: int,
    ) -> dict[str, Any]:
        """Resolve input data for a step.

        If this is a subsequent step (index > 0) and the input contains
        special keys like `use_previous_result`, the previous step's
        result is merged into the input.

        Otherwise, the input is passed as-is.
        """
        if step_index == 0 or previous_result is None:
            return dict(step_input)

        # If input explicitly asks to use previous result
        if step_input.get("use_previous_result", False):
            merged = dict(step_input)
            merged["previous_step_result"] = previous_result
            del merged["use_previous_result"]
            return merged

        # Default: pass input as-is, but also inject previous result
        # so downstream steps can access it if they need to
        resolved = dict(step_input)
        resolved["_pipeline_previous_result"] = previous_result
        return resolved

    def get_pipeline_telemetry(
        self,
        response: PipelineResponse,
    ) -> list[TelemetryRecord]:
        """Extract all telemetry records from a pipeline response.

        Useful for auditing and observability.
        """
        return [
            s.telemetry
            for s in response.steps
            if s.telemetry is not None
        ]

    def summarize(
        self,
        response: PipelineResponse,
    ) -> dict[str, Any]:
        """Produce a human-readable summary of the pipeline execution."""
        return {
            "pipeline_id": response.pipeline_id,
            "status": response.status.value,
            "total_time_ms": round(response.total_time_ms, 2),
            "steps_executed": response.step_count,
            "steps_planned": len(response.steps) + (
                response.step_count if response.failed_step is None
                else 0
            ),
            "failed": response.failed_step is not None,
            "failed_step": response.error_step if response.failed_step is not None else None,
            "error": response.error,
            "details": [
                {
                    "index": s.step_index,
                    "capability": s.capability_id,
                    "alias": s.alias,
                    "status": s.status.value,
                    "time_ms": round(s.execution_time_ms, 2),
                    "error": s.error,
                }
                for s in response.steps
            ],
        }


# Singleton instance
capability_pipeline = CapabilityPipeline()

