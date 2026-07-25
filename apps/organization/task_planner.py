"""
Task Planner
============

Decomposes a user intent / capability into executable subtasks
using the Capability Graph. Produces a TaskPlan that the Execution
Planner and Team Builder can consume.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from apps.organization.capability_graph import (
    capability_graph,
)

if TYPE_CHECKING:
    from apps.society.intent_router import Intent

logger = logging.getLogger(__name__)


@dataclass
class SubTask:
    subtask_id: str
    name: str
    description: str
    required_skills: list[str] = field(default_factory=list)
    produces_artifact: str = ""
    estimated_duration_minutes: int = 30
    priority: int = 5
    can_parallelize: bool = True
    depends_on: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskPlan:
    intent: Intent
    subtasks: list[SubTask]
    strategy: str = "mixed"
    estimated_total_minutes: int = 0
    domain: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.domain:
            self.domain = self.intent.domain.value
        self.estimated_total_minutes = sum(s.estimated_duration_minutes for s in self.subtasks)


class TaskPlanner:
    """Plans task decomposition using CapabilityGraph."""

    def __init__(self, graph: Any = None):
        self._graph = graph or capability_graph

    def plan(self, intent: Intent, capability_pack: Any = None) -> TaskPlan | None:
        domain = intent.domain.value
        templates = self._graph.get_subtask_templates(domain)
        if not templates:
            logger.info("No subtask templates for domain=%s; returning simple plan", domain)
            subtask = SubTask(
                subtask_id=f"subtask-{uuid.uuid4().hex[:8]}",
                name=intent.raw_input[:64],
                description=intent.raw_input,
                required_skills=intent.entities[:3],
                produces_artifact="result",
                estimated_duration_minutes=30,
                priority=1,
                can_parallelize=False,
                depends_on=[],
            )
            return TaskPlan(
                intent=intent,
                subtasks=[subtask],
                strategy="serial",
                estimated_total_minutes=30,
                domain=domain,
            )

        from apps.society.intent_router import IntentComplexity
        complexity_map = {
            IntentComplexity.SIMPLE: 3,
            IntentComplexity.MEDIUM: 5,
            IntentComplexity.COMPLEX: 7,
        }
        max_subtasks = complexity_map.get(intent.complexity, 5)
        selected = templates[:max_subtasks]

        subtasks: list[SubTask] = []
        seen_ids: set[str] = set()
        for template in selected:
            if template.subtask_id in seen_ids:
                continue
            seen_ids.add(template.subtask_id)
            deps = [
                prev.subtask_id
                for prev in subtasks
                if not template.can_parallelize or prev.priority < template.priority
            ]
            subtasks.append(SubTask(
                subtask_id=template.subtask_id,
                name=template.name,
                description=template.description,
                required_skills=list(template.required_skills),
                produces_artifact=template.produces_artifact,
                estimated_duration_minutes=template.estimated_duration_minutes,
                priority=template.priority,
                can_parallelize=template.can_parallelize,
                depends_on=deps,
            ))

        parallel_count = sum(1 for s in subtasks if s.can_parallelize)
        strategy = "parallel" if parallel_count == len(subtasks) and len(subtasks) > 1 else ("serial" if parallel_count == 0 else "mixed")

        logger.info("TaskPlan created: domain=%s, subtasks=%d, strategy=%s", domain, len(subtasks), strategy)
        return TaskPlan(
            intent=intent,
            subtasks=subtasks,
            strategy=strategy,
            domain=domain,
        )

    def refine(self, task_plan: TaskPlan, feedback: dict[str, Any]) -> TaskPlan:
        max_cost = feedback.get("max_cost")
        max_latency = feedback.get("max_latency_minutes")
        if max_latency is not None:
            filtered = [s for s in task_plan.subtasks if s.estimated_duration_minutes <= max_latency]
            if filtered:
                task_plan.subtasks = filtered
        if max_cost is not None:
            filtered = task_plan.subtasks[: max(1, len(task_plan.subtasks) // 2)]
            task_plan.subtasks = filtered
        task_plan.estimated_total_minutes = sum(s.estimated_duration_minutes for s in task_plan.subtasks)
        return task_plan


task_planner = TaskPlanner()
