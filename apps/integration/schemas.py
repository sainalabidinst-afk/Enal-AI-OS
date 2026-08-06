"""
Integration Capability Schemas
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorkflowStep:
    step_id: str
    capability_id: str
    input: dict[str, Any] = field(default_factory=dict)
    output: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowResult:
    workflow_id: str
    status: str
    steps: list[WorkflowStep] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkflowEngine:
    steps: list[WorkflowStep] = field(default_factory=list)

    def execute(self, context: dict[str, Any]) -> WorkflowResult:
        return WorkflowResult(workflow_id="demo", status="completed")
