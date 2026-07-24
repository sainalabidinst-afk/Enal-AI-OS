"""
Workflow Execution Layer
========================

Reads static workflow definitions and executes them via the Capability Pipeline.

Workflow bukan AI Planner.
Workflow tidak memilih capability.
Workflow hanya membaca definisi workflow yang sudah ditentukan,
kemudian menjalankannya melalui Pipeline.

Flow:
    Workflow Definition (static YAML/dict)
        |
    WorkflowExecutor.execute()
        |
    PipelineRequest ──→ CapabilityPipeline ──→ PipelineResponse
        |
    WorkflowResponse (unified)
"""

import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from apps.organization.capability_pipeline import (
    CapabilityPipeline,
    PipelineRequest,
    PipelineResponse,
    PipelineStep,
    capability_pipeline,
)
from apps.organization.capability_execution_engine import (
    ExecutionStatus,
    TelemetryRecord,
)

logger = logging.getLogger(__name__)

# ─── Built-in workflow definitions ───

_BUILT_IN_WORKFLOWS: dict[str, "WorkflowDefinition"] = {}


def _register_builtin(defn: "WorkflowDefinition") -> None:
    _BUILT_IN_WORKFLOWS[defn.workflow_id] = defn


# ─── Data classes ───


@dataclass
class WorkflowStep:
    """A single step in a workflow definition.

    Attributes:
        capability_id: The capability to execute.
        input_data: Static input data for this step.
        alias: Optional friendly name.
        description: Optional description of what this step does.
    """
    capability_id: str
    input_data: dict[str, Any]
    alias: str = ""
    description: str = ""

    def __post_init__(self) -> None:
        if not self.alias:
            self.alias = self.capability_id


@dataclass
class WorkflowDefinition:
    """Static workflow definition.

    Attributes:
        workflow_id: Unique identifier for this workflow.
        name: Human-readable name.
        description: Optional description.
        ordered_steps: Ordered list of steps to execute sequentially.
        metadata: Additional metadata (tags, version, author, etc.).
    """
    workflow_id: str
    name: str
    description: str = ""
    ordered_steps: list[WorkflowStep] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowStepResult:
    """Result of a single workflow step.

    Attributes:
        step_index: 0-based index in workflow.
        capability_id: The executed capability.
        alias: Friendly step name.
        status: Execution status.
        result: Execution result payload.
        error: Error message if failed.
        execution_time_ms: Time taken.
    """
    step_index: int
    capability_id: str
    alias: str
    status: ExecutionStatus
    result: Any
    error: str | None
    execution_time_ms: float


@dataclass
class WorkflowResponse:
    """Standardized output contract for workflow execution.

    Attributes:
        workflow_id: Matches the workflow definition.
        workflow_name: Human-readable name from definition.
        execution_id: Unique ID for this execution.
        correlation_id: For grouping multi-workflow requests.
        status: Overall status (COMPLETED or FAILED).
        steps: Results for each step in order.
        total_time_ms: Total execution time.
        step_count: Number of steps executed.
        failed_step: Index of failed step (None if all passed).
        error: Overall error message (None on success).
    """
    workflow_id: str
    workflow_name: str
    execution_id: str
    correlation_id: str
    status: ExecutionStatus
    steps: list[WorkflowStepResult]
    total_time_ms: float
    step_count: int
    failed_step: int | None = None
    error: str | None = None


# ─── Executor ───


class WorkflowExecutor:
    """Executes static workflow definitions via the Capability Pipeline.

    WorkflowExecutor is NOT a planner.
    It only reads pre-defined workflows and executes them.
    """

    def __init__(
        self,
        pipeline: CapabilityPipeline | None = None,
    ):
        self._pipeline = pipeline or capability_pipeline
        self._workflows: dict[str, WorkflowDefinition] = {}
        self._execution_history: dict[str, WorkflowResponse] = {}

        # Register built-in workflows
        for wid, defn in _BUILT_IN_WORKFLOWS.items():
            self._workflows[wid] = defn

    # ── Workflow registration ──

    def register(self, definition: WorkflowDefinition) -> None:
        """Register a workflow definition."""
        if not definition.workflow_id:
            raise ValueError("workflow_id is required")
        if not definition.ordered_steps:
            raise ValueError(f"Workflow '{definition.workflow_id}' must have at least one step")
        for step in definition.ordered_steps:
            if not step.capability_id:
                raise ValueError(f"Step in workflow '{definition.workflow_id}' has empty capability_id")
        self._workflows[definition.workflow_id] = definition
        logger.info("Workflow registered: %s (%s)", definition.workflow_id, definition.name)

    def register_from_dict(self, data: dict[str, Any]) -> WorkflowDefinition:
        """Register a workflow from a dictionary (e.g., loaded from JSON/YAML)."""
        steps_data = data.get("ordered_steps", [])
        steps = [
            WorkflowStep(
                capability_id=s["capability_id"],
                input_data=s.get("input_data", {}),
                alias=s.get("alias", ""),
                description=s.get("description", ""),
            )
            for s in steps_data
        ]
        definition = WorkflowDefinition(
            workflow_id=data["workflow_id"],
            name=data.get("name", data["workflow_id"]),
            description=data.get("description", ""),
            ordered_steps=steps,
            metadata=data.get("metadata", {}),
        )
        self.register(definition)
        return definition

    def register_from_json(self, json_str: str) -> WorkflowDefinition:
        """Register a workflow from a JSON string."""
        data = json.loads(json_str)
        return self.register_from_dict(data)

    def register_from_file(self, filepath: str) -> WorkflowDefinition:
        """Register a workflow from a JSON file."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Workflow file not found: {filepath}")
        content = path.read_text(encoding="utf-8")
        return self.register_from_json(content)

    # ── Workflow lookup ──

    def get(self, workflow_id: str) -> WorkflowDefinition | None:
        """Get a registered workflow definition."""
        return self._workflows.get(workflow_id)

    def list_workflows(self) -> list[dict[str, Any]]:
        """List all registered workflows."""
        return [
            {
                "workflow_id": wf.workflow_id,
                "name": wf.name,
                "description": wf.description,
                "step_count": len(wf.ordered_steps),
                "metadata": wf.metadata,
            }
            for wf in self._workflows.values()
        ]

    # ── Execution ──

    async def execute(
        self,
        workflow_id: str,
        input_data: dict[str, Any] | None = None,
        execution_id: str | None = None,
        correlation_id: str | None = None,
    ) -> WorkflowResponse:
        """Execute a registered workflow.

        Args:
            workflow_id: ID of the registered workflow to execute.
            input_data: Optional base input data merged into each step.
            execution_id: Optional explicit execution ID.
            correlation_id: Optional correlation ID for grouping.

        Returns:
            WorkflowResponse with step-by-step results.
        """
        # ── 1. Resolve workflow definition ──
        definition = self._workflows.get(workflow_id)
        if definition is None:
            return WorkflowResponse(
                workflow_id=workflow_id,
                workflow_name="unknown",
                execution_id=execution_id or f"wf-{uuid.uuid4().hex[:12]}",
                correlation_id=correlation_id or "",
                status=ExecutionStatus.FAILED,
                steps=[],
                total_time_ms=0.0,
                step_count=0,
                failed_step=0,
                error=f"Workflow '{workflow_id}' not found",
            )

        start_time = time.monotonic()
        exec_id = execution_id or f"wf-{uuid.uuid4().hex[:12]}"
        corr_id = correlation_id or exec_id

        # ── 2. Build pipeline steps ──
        base_input = input_data or {}
        pipeline_steps: list[PipelineStep] = []
        for step in definition.ordered_steps:
            merged_input = {**base_input, **step.input_data}
            pipeline_steps.append(
                PipelineStep(
                    capability_id=step.capability_id,
                    input_data=merged_input,
                    alias=step.alias,
                    metadata={
                        "workflow_id": workflow_id,
                        "workflow_name": definition.name,
                        "step_description": step.description,
                    },
                )
            )

        # ── 3. Execute via pipeline ──
        pipeline_request = PipelineRequest(
            steps=pipeline_steps,
            pipeline_id=f"pipe-{exec_id[:8]}",
            correlation_id=corr_id,
            metadata={
                "workflow_id": workflow_id,
                "workflow_name": definition.name,
                "execution_id": exec_id,
            },
        )

        try:
            pipeline_response: PipelineResponse = await self._pipeline.execute(pipeline_request)
        except Exception as exc:
            logger.exception("Workflow execution crashed: %s", workflow_id)
            return WorkflowResponse(
                workflow_id=workflow_id,
                workflow_name=definition.name,
                execution_id=exec_id,
                correlation_id=corr_id,
                status=ExecutionStatus.FAILED,
                steps=[],
                total_time_ms=(time.monotonic() - start_time) * 1000,
                step_count=0,
                failed_step=0,
                error=f"Workflow infrastructure error: {exc}",
            )

        # ── 4. Build workflow response ──
        total_time_ms = (time.monotonic() - start_time) * 1000
        step_results = [
            WorkflowStepResult(
                step_index=ps.step_index,
                capability_id=ps.capability_id,
                alias=ps.alias,
                status=ps.status,
                result=ps.result,
                error=ps.error,
                execution_time_ms=ps.execution_time_ms,
            )
            for ps in pipeline_response.steps
        ]

        response = WorkflowResponse(
            workflow_id=workflow_id,
            workflow_name=definition.name,
            execution_id=exec_id,
            correlation_id=corr_id,
            status=pipeline_response.status,
            steps=step_results,
            total_time_ms=total_time_ms,
            step_count=pipeline_response.step_count,
            failed_step=pipeline_response.failed_step,
            error=pipeline_response.error,
        )

        # ── 5. Record in history ──
        self._execution_history[exec_id] = response

        logger.info(
            "Workflow executed: %s (%s) status=%s steps=%d time=%.2fms",
            workflow_id,
            definition.name,
            response.status.value,
            response.step_count,
            total_time_ms,
        )

        return response

    # ── History ──

    def get_execution(self, execution_id: str) -> WorkflowResponse | None:
        """Get a previous workflow execution result."""
        return self._execution_history.get(execution_id)

    def get_history(
        self,
        workflow_id: str | None = None,
    ) -> list[WorkflowResponse]:
        """Get all execution history, optionally filtered by workflow_id."""
        if workflow_id:
            return [r for r in self._execution_history.values() if r.workflow_id == workflow_id]
        return list(self._execution_history.values())

    def summarize(self, response: WorkflowResponse) -> dict[str, Any]:
        """Produce a human-readable summary of the workflow execution."""
        return {
            "workflow_id": response.workflow_id,
            "workflow_name": response.workflow_name,
            "execution_id": response.execution_id,
            "status": response.status.value,
            "total_time_ms": round(response.total_time_ms, 2),
            "steps_executed": response.step_count,
            "failed": response.failed_step is not None,
            "failed_step": response.error if response.failed_step is not None else None,
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


# ─── Singleton ───

workflow_executor = WorkflowExecutor()
