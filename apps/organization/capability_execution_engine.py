"""
Capability Execution Engine
============================

Standardized execution engine for capabilities.

Accept flow:
    1. ExecutionRequest
    2. find capability in registry (capability_graph)
    3. validate input against capability contract
    4. route to domain worker
    5. execute via ExecutionRuntime
    6. record telemetry (observer pattern)
    7. return ExecutionResponse

Contract:
    - ExecutionRequest    → standardized input contract
    - ExecutionResponse   → standardized output contract
    - ExecutionStatus     → matches documented lifecycle

This engine is an EXECUTOR, not a planner.
It delegates planning to ExecutionPlanner and execution to ExecutionRuntime.
"""

import asyncio
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from apps.organization.capability_contract import (
    CapabilityContractError,
    CapabilityNode,
    validate_capability_node,
)
from apps.organization.capability_graph import capability_graph
from apps.organization.execution_planner import (
    ExecutionPlan,
    ExecutionStage,
)
from apps.organization.execution_runtime import (
    ExecutionContext,
    ExecutionRuntime,
    SubtaskResult,
    SubtaskStatus,
    execution_runtime,
)
from apps.organization.kernel import organization_kernel
from apps.organization.metrics import organizational_metrics
from apps.organization.task_planner import SubTask
from apps.society.intent_router import Intent, IntentComplexity, IntentDomain
from apps.society.society import WORKER_REGISTRY

logger = logging.getLogger(__name__)


class ExecutionStatus(str, Enum):
    """Standardized execution lifecycle matching documented flow.

    CREATED → QUEUED → RUNNING → COMPLETED
                                    → FAILED
                                    → CANCELLED
    """
    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ExecutionRequest:
    """Standardized input contract for capability execution.

    Attributes:
        capability_id: The capability to execute (must exist in capability_graph).
        input_data: The input payload for the capability.
        execution_id: Unique identifier for this execution (auto-generated if empty).
        correlation_id: Groups multiple executions under a single user request.
        metadata: Additional context (e.g., project_id, user_id, constraints).
    """
    capability_id: str
    input_data: dict[str, Any]
    execution_id: str = ""
    correlation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.execution_id:
            self.execution_id = f"exec-{uuid.uuid4().hex[:12]}"
        if not self.correlation_id:
            self.correlation_id = self.execution_id


@dataclass
class TelemetryRecord:
    """Immutable telemetry record for a single execution."""
    execution_id: str
    correlation_id: str
    capability_id: str
    status: ExecutionStatus
    execution_time_ms: float
    started_at: datetime
    finished_at: datetime | None = None
    worker_domain: str = ""
    retry_count: int = 0
    error_type: str = ""
    error_message: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionResponse:
    """Standardized output contract for capability execution.

    Attributes:
        status: Final execution status (COMPLETED, FAILED, CANCELLED).
        result: Execution result payload (None on failure).
        error: Error message (None on success).
        execution_time_ms: Total execution time in milliseconds.
        execution_id: Matches the request execution_id.
        correlation_id: Matches the request correlation_id.
        telemetry: Immutable telemetry snapshot.
    """
    status: ExecutionStatus
    result: Any
    error: str | None
    execution_time_ms: float
    execution_id: str
    correlation_id: str
    telemetry: TelemetryRecord | None = None


class CapabilityExecutionEngine:
    """Standardized engine for executing capabilities.

    Responsibilities:
        - Accept ExecutionRequest
        - Find capability in CapabilityGraph (registry)
        - Validate input against capability contract
        - Route to domain worker via worker registry
        - Execute via ExecutionRuntime
        - Record telemetry as observer (does not affect flow)
        - Return standardized ExecutionResponse
    """

    def __init__(
        self,
        graph: Any = None,
        runtime: ExecutionRuntime | None = None,
    ):
        self._graph = graph or capability_graph
        self._runtime = runtime or execution_runtime
        self._telemetry: list[TelemetryRecord] = []

    async def execute(self, request: ExecutionRequest) -> ExecutionResponse:
        """Main entry point. Executes a capability end-to-end.

        Flow:
            1. Validate request structure
            2. Find capability in registry
            3. Validate input
            4. Prepare execution context
            5. Execute via runtime
            6. Record telemetry (observer — does not block)
            7. Return standardized response
        """
        start_time = time.monotonic()
        telemetry = TelemetryRecord(
            execution_id=request.execution_id,
            correlation_id=request.correlation_id,
            capability_id=request.capability_id,
            status=ExecutionStatus.CREATED,
            execution_time_ms=0.0,
            started_at=datetime.now(UTC),
        )

        try:
            # ── 1. Find capability in registry ──
            telemetry.status = ExecutionStatus.QUEUED
            capability_node = self._find_capability(request.capability_id)
            if capability_node is None:
                return self._fail(
                    request, start_time, telemetry,
                    error=f"Capability '{request.capability_id}' not found in registry",
                    error_type="capability_not_found",
                )

            # ── 2. Validate input ──
            validation_error = self._validate_input(capability_node, request.input_data)
            if validation_error:
                return self._fail(
                    request, start_time, telemetry,
                    error=validation_error,
                    error_type="validation_error",
                )

            # ── 3. Prepare execution context ──
            telemetry.status = ExecutionStatus.RUNNING
            context = self._prepare_execution(request, capability_node)

            # ── 4. Execute via runtime ──
            subtask_results = await self._runtime.execute(context)

            # ── 5. Aggregate results ──
            result = self._aggregate_results(subtask_results)
            has_failure = any(
                r.status in (SubtaskStatus.FAILED, SubtaskStatus.CANCELLED)
                for r in subtask_results
            )

            elapsed_ms = (time.monotonic() - start_time) * 1000
            telemetry.execution_time_ms = elapsed_ms
            telemetry.finished_at = datetime.now(UTC)
            telemetry.worker_domain = context.metadata.get("domain", "")
            telemetry.retry_count = sum(r.attempts - 1 for r in subtask_results)

            if has_failure:
                errors = [
                    r.error for r in subtask_results
                    if r.status in (SubtaskStatus.FAILED, SubtaskStatus.CANCELLED) and r.error
                ]
                return self._fail(
                    request, start_time, telemetry,
                    error="; ".join(errors) if errors else "Execution failed",
                    error_type="execution_failed",
                    result=result,
                )

            # ── 6. Record telemetry (observer) ──
            telemetry.status = ExecutionStatus.COMPLETED
            self._record_telemetry(telemetry)

            return ExecutionResponse(
                status=ExecutionStatus.COMPLETED,
                result=result,
                error=None,
                execution_time_ms=elapsed_ms,
                execution_id=request.execution_id,
                correlation_id=request.correlation_id,
                telemetry=telemetry,
            )

        except asyncio.CancelledError:
            elapsed_ms = (time.monotonic() - start_time) * 1000
            telemetry.status = ExecutionStatus.CANCELLED
            telemetry.execution_time_ms = elapsed_ms
            telemetry.finished_at = datetime.now(UTC)
            self._record_telemetry(telemetry)
            return ExecutionResponse(
                status=ExecutionStatus.CANCELLED,
                result=None,
                error="Execution cancelled",
                execution_time_ms=elapsed_ms,
                execution_id=request.execution_id,
                correlation_id=request.correlation_id,
                telemetry=telemetry,
            )

        except Exception as exc:
            elapsed_ms = (time.monotonic() - start_time) * 1000
            telemetry.status = ExecutionStatus.FAILED
            telemetry.execution_time_ms = elapsed_ms
            telemetry.finished_at = datetime.now(UTC)
            telemetry.error_type = "runtime_error"
            telemetry.error_message = str(exc)
            self._record_telemetry(telemetry)
            logger.exception("Capability execution failed: %s", request.capability_id)
            return ExecutionResponse(
                status=ExecutionStatus.FAILED,
                result=None,
                error=str(exc),
                execution_time_ms=elapsed_ms,
                execution_id=request.execution_id,
                correlation_id=request.correlation_id,
                telemetry=telemetry,
            )

    # ──────────────────────────────────────────────
    # Internal steps
    # ──────────────────────────────────────────────

    def _find_capability(self, capability_id: str) -> CapabilityNode | None:
        """Step 1: Find capability in the registry (CapabilityGraph)."""
        all_caps = self._graph.get_all_capabilities()
        if capability_id not in all_caps:
            return None
        return self._graph.get_capability_node(capability_id)

    def _validate_input(
        self,
        capability_node: CapabilityNode,
        input_data: dict[str, Any],
    ) -> str | None:
        """Step 2: Validate input against capability contract.

        Returns error string or None if valid.
        """
        # Validate the capability node itself first
        try:
            validate_capability_node(capability_node)
        except CapabilityContractError as e:
            return f"Capability contract violation: {e}"

        # Validate that input_data is a dict
        if not isinstance(input_data, dict):
            return "input_data must be a dictionary"

        # Check required skills are reflected in input
        required_skills = capability_node.required_skills
        provided_skills = input_data.get("skills", [])
        if isinstance(provided_skills, list):
            missing = [s for s in required_skills if s not in provided_skills]
            if missing and len(missing) == len(required_skills):
                # Only warn if ALL required skills are missing
                logger.warning(
                    "Input missing all required skills for '%s': %s",
                    capability_node.capability_id,
                    missing,
                )

        return None

    def _prepare_execution(
        self,
        request: ExecutionRequest,
        capability_node: CapabilityNode,
    ) -> ExecutionContext:
        """Step 3: Prepare execution context for the runtime.

        Builds a minimal ExecutionPlan with one subtask and routes
        to the appropriate worker. This is NOT planning — it's
        preparing the execution environment.
        """
        # Determine domain from capability tags or node data
        tags = capability_node.tags or []
        domain_hint = tags[0] if tags else "general"
        # Map common tags to domains
        domain_map = {
            "network": IntentDomain.NETWORK,
            "code": IntentDomain.CODE,
            "research": IntentDomain.RESEARCH,
            "devops": IntentDomain.DEVOPS,
            "trading": IntentDomain.TRADING,
            "security": IntentDomain.SECURITY,
            "data": IntentDomain.DATA,
            "self-development": IntentDomain.SELF_DEVELOPMENT,
        }
        domain = domain_map.get(domain_hint, IntentDomain.GENERAL)

        # Find the worker for this domain
        worker = self._route_to_worker(domain.value)
        if worker is None:
            raise ValueError(f"No worker found for domain '{domain.value}' (capability: {request.capability_id})")

        # Build a single subtask representing this capability execution
        subtask = SubTask(
            subtask_id=f"cap-{request.capability_id}-{uuid.uuid4().hex[:6]}",
            name=capability_node.name,
            description=capability_node.description,
            required_skills=list(capability_node.required_skills),
            produces_artifact="result",
            estimated_duration_minutes=30,
            priority=1,
            can_parallelize=False,
            depends_on=[],
            metadata={
                "capability_id": request.capability_id,
                "execution_id": request.execution_id,
                "correlation_id": request.correlation_id,
                "input_data": request.input_data,
            },
        )

        # Build minimal ExecutionPlan (single stage, serial)
        stage = ExecutionStage(
            stage_id=f"stage-{request.execution_id[:8]}",
            stage_index=1,
            subtasks=[subtask],
            mode="serial",
        )
        plan = ExecutionPlan(
            intent=Intent(
                raw_input=capability_node.description,
                domain=domain,
                complexity=IntentComplexity.MEDIUM,
            ),
            stages=[stage],
        )

        # Build ExecutionContext
        context = ExecutionContext(
            execution_id=request.execution_id,
            plan=plan,
            worker=worker.execute,
            concurrency=1,
            retry_limit=2,
            retry_delay_seconds=1.0,
            timeout_seconds=120.0,
            metadata={
                "domain": domain.value,
                "capability_id": request.capability_id,
                "correlation_id": request.correlation_id,
                "input_data": request.input_data,
            },
        )

        # Track in organizational metrics (start)
        project_id = request.metadata.get("project_id", f"proj-{request.execution_id[:8]}")
        organizational_metrics.start_project(project_id, f"team-{domain.value}")
        organizational_metrics.record_task(project_id, success=True, tokens=0, cost=0.0)

        # Track in kernel
        organization_kernel.allocate_budget(
            100.0,
            request.execution_id,
            f"Execute capability: {request.capability_id}",
        )

        return context

    def _route_to_worker(self, domain: str) -> Any | None:
        """Step 4: Route to the appropriate domain worker.

        Uses the existing WORKER_REGISTRY from society module.
        """
        return WORKER_REGISTRY.get(domain)

    def _record_telemetry(self, record: TelemetryRecord) -> None:
        """Step 5: Record telemetry as an observer.

        This is a pure observer — it does not affect execution flow.
        Telemetry is stored and also pushed to organizational_metrics.
        """
        self._telemetry.append(record)

        # Also push to organizational metrics
        project_id = record.metadata.get("project_id", f"proj-{record.execution_id[:8]}")
        if record.status == ExecutionStatus.COMPLETED:
            organizational_metrics.record_task(
                project_id,
                success=True,
                tokens=0,
                cost=0.0,
            )
        elif record.status == ExecutionStatus.FAILED:
            organizational_metrics.record_task(
                project_id,
                success=False,
                tokens=0,
                cost=0.0,
            )

        logger.info(
            "Telemetry: capability=%s status=%s time=%.2fms execution=%s correlation=%s",
            record.capability_id,
            record.status.value,
            record.execution_time_ms,
            record.execution_id,
            record.correlation_id,
        )

    # ──────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────

    def _aggregate_results(self, subtask_results: list[SubtaskResult]) -> dict[str, Any]:
        """Aggregate subtask results into a single result dict."""
        results = {}
        for r in subtask_results:
            results[r.subtask_id] = {
                "status": r.status.value,
                "result": r.result,
                "error": r.error,
                "duration_seconds": r.duration_seconds,
                "attempts": r.attempts,
            }
        return {
            "subtask_count": len(subtask_results),
            "subtasks": results,
        }

    def _fail(
        self,
        request: ExecutionRequest,
        start_time: float,
        telemetry: TelemetryRecord,
        error: str,
        error_type: str = "execution_failed",
        result: Any = None,
    ) -> ExecutionResponse:
        """Build a failed response and record telemetry."""
        elapsed_ms = (time.monotonic() - start_time) * 1000
        telemetry.status = ExecutionStatus.FAILED
        telemetry.execution_time_ms = elapsed_ms
        telemetry.finished_at = datetime.now(UTC)
        telemetry.error_type = error_type
        telemetry.error_message = error
        self._record_telemetry(telemetry)

        logger.warning(
            "Execution failed: capability=%s error_type=%s error=%s",
            request.capability_id,
            error_type,
            error,
        )

        return ExecutionResponse(
            status=ExecutionStatus.FAILED,
            result=result,
            error=error,
            execution_time_ms=elapsed_ms,
            execution_id=request.execution_id,
            correlation_id=request.correlation_id,
            telemetry=telemetry,
        )

    def get_telemetry(
        self,
        execution_id: str | None = None,
        correlation_id: str | None = None,
    ) -> list[TelemetryRecord]:
        """Retrieve telemetry records, optionally filtered."""
        records = self._telemetry
        if execution_id:
            records = [r for r in records if r.execution_id == execution_id]
        if correlation_id:
            records = [r for r in records if r.correlation_id == correlation_id]
        return list(records)

    def clear_telemetry(self) -> None:
        """Clear stored telemetry (useful for testing)."""
        self._telemetry.clear()


# Singleton instance
capability_execution_engine = CapabilityExecutionEngine()

