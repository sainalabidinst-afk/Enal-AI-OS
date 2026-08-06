import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from backend.app.core.event_bus import event_bus
from backend.app.core.events import Event

logger = logging.getLogger(__name__)


class WorkflowStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class WorkflowStep:
    id: str
    name: str
    agent: str
    action: str
    parameters: dict[str, Any] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)
    condition: str | None = None
    retry_policy: dict[str, Any] = field(default_factory=dict)


@dataclass
class Workflow:
    id: str
    name: str
    description: str
    steps: list[WorkflowStep]
    status: WorkflowStatus = WorkflowStatus.DRAFT
    context: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now(UTC))


class WorkflowEngine:
    def __init__(self):
        self._workflows: dict[str, Workflow] = {}
        self._execution_history: dict[str, dict] = {}
        try:
            event_bus.subscribe("step.completed", self._on_step_completed)
            event_bus.subscribe("step.failed", self._on_step_failed)
        except Exception:
            pass  # Event bus may not be available

    async def _publish_event(self, event_type: str, payload: dict, source: str = "workflow-engine"):
        """Publish event safely, ignoring Redis errors."""
        try:
            await event_bus.publish(Event(
                event_type=event_type,
                payload=payload,
                source=source,
            ))
        except Exception:
            pass  # Silently ignore event bus errors

    async def _on_step_completed(self, event: Event):
        workflow_id = event.payload.get("workflow_id")
        if workflow_id and workflow_id in self._workflows:
            self._workflows[workflow_id].status = WorkflowStatus.ACTIVE

    async def _on_step_failed(self, event: Event):
        workflow_id = event.payload.get("workflow_id")
        if workflow_id and workflow_id in self._workflows:
            self._workflows[workflow_id].status = WorkflowStatus.FAILED

    async def create_workflow(self, workflow: Workflow) -> str:
        self._workflows[workflow.id] = workflow
        await self._publish_event(
            "workflow.created",
            {"workflow_id": workflow.id},
        )
        return workflow.id

    async def run(self, workflow_id: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        workflow = self._workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow not found: {workflow_id}")
        workflow.status = WorkflowStatus.RUNNING
        if context:
            workflow.context.update(context)

        results: dict[str, Any] = {}
        failed_steps: list[str] = []

        executed: set[str] = set()

        while len(executed) < len(workflow.steps):
            runnable = [
                s for s in workflow.steps
                if s.id not in executed and all(d in executed for d in s.depends_on)
            ]
            if not runnable:
                break

            for step in runnable:
                await self._publish_event(
                    "step.started",
                    {"step_id": step.id, "workflow_id": workflow_id},
                )

                step_result = await self._execute_step(step, workflow.context)
                results[step.id] = step_result

                if step_result.get("status") == "failed":
                    failed_steps.append(step.id)
                    if not self._should_retry(step, step_result.get("error", "")):
                        workflow.status = WorkflowStatus.FAILED
                        await self._publish_event(
                            "workflow.failed",
                            {"workflow_id": workflow_id, "failed_step": step.id},
                        )
                        return {"status": "failed", "results": results, "error": f"Step {step.id} failed"}
                else:
                    executed.add(step.id)
                    await self._publish_event(
                        "step.completed",
                        {"step_id": step.id, "workflow_id": workflow_id},
                    )

        workflow.status = WorkflowStatus.COMPLETED
        self._execution_history[workflow_id] = {
            "completed_at": datetime.now(UTC).isoformat(),
            "results": results,
        }
        return {"status": "completed", "results": results}

    async def _execute_step(self, step: WorkflowStep, context: dict[str, Any]) -> dict[str, Any]:
        """Execute a single workflow step."""
        max_retries = step.retry_policy.get("max_retries", 0)
        retry_count = 0

        while retry_count <= max_retries:
            try:
                # Merge step parameters with context
                merged_params = {**context, **step.parameters}
                result = await self._call_tool(step.agent, step.action, merged_params)
                return {"status": "success", "result": result}
            except Exception as e:
                retry_count += 1
                if retry_count > max_retries:
                    return {"status": "failed", "error": str(e)}

        return {"status": "failed", "error": "Max retries exceeded"}

    async def _call_tool(self, agent: str, action: str, params: dict[str, Any]) -> Any:
        """Call a tool/capability by agent and action name."""
        # Import inside to avoid circular import
        from backend.app.core.tool_registry import tool_registry
        tool = tool_registry.get(action)
        if tool and tool.handler:
            return await tool.handler(**params)
        return {"agent": agent, "action": action, "params": params, "simulated": True}

    def _should_retry(self, step: WorkflowStep, error: str) -> bool:
        if not step.retry_policy:
            return False
        max_retries = step.retry_policy.get("max_retries", 0)
        return max_retries > 0

    async def get_workflow(self, workflow_id: str) -> Workflow | None:
        return self._workflows.get(workflow_id)

    def list_workflows(self) -> list[dict[str, Any]]:
        return [
            {
                "id": w.id,
                "name": w.name,
                "description": w.description,
                "status": w.status.value,
                "step_count": len(w.steps),
            }
            for w in self._workflows.values()
        ]

    async def cancel(self, workflow_id: str) -> bool:
        workflow = self._workflows.get(workflow_id)
        if workflow:
            workflow.status = WorkflowStatus.CANCELLED
            return True
        return False


workflow_engine = WorkflowEngine()

