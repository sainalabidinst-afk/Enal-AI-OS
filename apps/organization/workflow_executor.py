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

from apps.organization.capability_execution_engine import ExecutionStatus
from apps.organization.capability_pipeline import (
    CapabilityPipeline,
    PipelineRequest,
    PipelineResponse,
    PipelineStep,
    capability_pipeline,
)

logger = logging.getLogger(__name__)

_BUILT_IN_WORKFLOWS: dict[str, "WorkflowDefinition"] = {}


def _register_builtin(defn: "WorkflowDefinition") -> None:
    _BUILT_IN_WORKFLOWS[defn.workflow_id] = defn


@dataclass
class WorkflowStep:
    capability_id: str
    input_data: dict[str, Any]
    alias: str = ""
    description: str = ""

    def __post_init__(self) -> None:
        if not self.alias:
            self.alias = self.capability_id


@dataclass
class WorkflowDefinition:
    workflow_id: str
    name: str
    description: str = ""
    ordered_steps: list[WorkflowStep] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowStepResult:
    step_index: int
    capability_id: str
    alias: str
    status: ExecutionStatus
    result: Any
    error: str | None
    execution_time_ms: float


@dataclass
class WorkflowResponse:
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


class WorkflowExecutor:
    def __init__(
        self,
        pipeline: CapabilityPipeline | None = None,
    ):
        self._pipeline = pipeline or capability_pipeline
        self._workflows: dict[str, WorkflowDefinition] = {}
        self._execution_history: dict[str, WorkflowResponse] = {}
        for wid, defn in _BUILT_IN_WORKFLOWS.items():
            self._workflows[wid] = defn

    def register(self, definition: WorkflowDefinition) -> None:
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
        data = json.loads(json_str)
        return self.register_from_dict(data)

    def register_from_file(self, filepath: str) -> WorkflowDefinition:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Workflow file not found: {filepath}")
        content = path.read_text(encoding="utf-8")
        return self.register_from_json(content)

    def get(self, workflow_id: str) -> WorkflowDefinition | None:
        return self._workflows.get(workflow_id)

    def list_workflows(self) -> list[dict[str, Any]]:
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

    async def execute(
        self,
        workflow_id: str,
        input_data: dict[str, Any] | None = None,
        execution_id: str | None = None,
        correlation_id: str | None = None,
    ) -> WorkflowResponse:
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

    def get_execution(self, execution_id: str) -> WorkflowResponse | None:
        return self._execution_history.get(execution_id)

    def get_history(
        self,
        workflow_id: str | None = None,
    ) -> list[WorkflowResponse]:
        if workflow_id:
            return [r for r in self._execution_history.values() if r.workflow_id == workflow_id]
        return list(self._execution_history.values())

    def summarize(self, response: WorkflowResponse) -> dict[str, Any]:
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

    def create_checkpoint(self, response: WorkflowResponse) -> dict[str, Any]:
        return {
            "execution_id": response.execution_id,
            "workflow_id": response.workflow_id,
            "completed_steps": response.step_count - (1 if response.failed_step else 0),
            "total_steps": response.step_count,
            "status": response.status.value,
            "timestamp": time.time(),
        }

    async def resume_from_checkpoint(
        self,
        checkpoint: dict[str, Any],
        workflow_id: str,
        input_data: dict[str, Any] | None = None,
    ) -> WorkflowResponse:
        definition = self._workflows.get(workflow_id)
        if not definition:
            raise ValueError(f"Workflow '{workflow_id}' not found")

        start_idx = checkpoint.get("completed_steps", 0)
        if start_idx >= len(definition.ordered_steps):
            return WorkflowResponse(
                workflow_id=workflow_id,
                workflow_name=definition.name,
                execution_id=f"wf-{uuid.uuid4().hex[:12]}",
                correlation_id=checkpoint.get("correlation_id", ""),
                status=ExecutionStatus.COMPLETED,
                steps=[],
                total_time_ms=0.0,
                step_count=0,
                failed_step=None,
                error=None,
            )

        remaining_steps = definition.ordered_steps[start_idx:]
        pipeline_steps = [
            PipelineStep(
                capability_id=step.capability_id,
                input_data={**(input_data or {}), **step.input_data},
                alias=step.alias,
                metadata={"resumed_from": checkpoint.get("execution_id")},
            )
            for step in remaining_steps
        ]

        pipeline_request = PipelineRequest(
            steps=pipeline_steps,
            pipeline_id=f"pipe-resume-{checkpoint.get('execution_id', '')[:8]}",
        )

        response = await self._pipeline.execute(pipeline_request)
        step_results = [
            WorkflowStepResult(
                step_index=ps.step_index + start_idx,
                capability_id=ps.capability_id,
                alias=ps.alias,
                status=ps.status,
                result=ps.result,
                error=ps.error,
                execution_time_ms=ps.execution_time_ms,
            )
            for ps in response.steps
        ]

        return WorkflowResponse(
            workflow_id=workflow_id,
            workflow_name=definition.name,
            execution_id=f"wf-{uuid.uuid4().hex[:12]}",
            correlation_id=checkpoint.get("correlation_id", ""),
            status=response.status,
            steps=step_results,
            total_time_ms=response.total_time_ms,
            step_count=response.step_count,
            failed_step=response.failed_step,
            error=response.error,
        )

    async def execute_with_retry(
        self,
        workflow_id: str,
        input_data: dict[str, Any] | None = None,
        max_retries: int = 3,
    ) -> WorkflowResponse:
        last_response: WorkflowResponse | None = None
        for attempt in range(max_retries):
            last_response = await self.execute(workflow_id, input_data)
            if last_response.status.value == "completed":
                return last_response
            logger.warning(
                "Workflow %s failed (attempt %d/%d)",
                workflow_id,
                attempt + 1,
                max_retries,
            )
        return last_response  # type: ignore[return-value]


workflow_executor = WorkflowExecutor()