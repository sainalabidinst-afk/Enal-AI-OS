import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from enum import Enum
from backend.app.core.events import Event
from backend.app.core.event_bus import event_bus

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
    created_at: datetime = field(default_factory=datetime.utcnow)


class WorkflowEngine:
    def __init__(self):
        self._workflows: dict[str, Workflow] = {}
        event_bus.subscribe("step.completed", self._on_step_completed)
        event_bus.subscribe("step.failed", self._on_step_failed)

    async def _on_step_completed(self, event: Event):
        pass

    async def _on_step_failed(self, event: Event):
        pass

    async def create_workflow(self, workflow: Workflow) -> str:
        self._workflows[workflow.id] = workflow
        await event_bus.publish(Event(
            event_type="workflow.created",
            payload={"workflow_id": workflow.id},
            source="workflow-engine",
        ))
        return workflow.id

    async def run(self, workflow_id: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        workflow = self._workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow not found: {workflow_id}")
        workflow.status = WorkflowStatus.RUNNING
        if context:
            workflow.context.update(context)
        results: dict[str, Any] = {}
        for step in workflow.steps:
            await event_bus.publish(Event(
                event_type="step.started",
                payload={"step_id": step.id, "workflow_id": workflow_id},
                source="workflow-engine",
            ))
            results[step.id] = {"status": "completed", "result": None}
        workflow.status = WorkflowStatus.COMPLETED
        return results

    async def get_workflow(self, workflow_id: str) -> Workflow | None:
        return self._workflows.get(workflow_id)


workflow_engine = WorkflowEngine()
