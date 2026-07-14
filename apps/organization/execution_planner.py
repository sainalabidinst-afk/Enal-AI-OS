"""
Execution Planner
=================

Converts a TaskPlan into an ordered ExecutionPlan.
Groups subtasks into stages that can run in parallel or must run serially,
respecting dependencies and domain strategy hints.

Output is consumed by SocietyRuntime / run_project to decide how
to form and dispatch teams.
"""

import logging
import uuid
from dataclasses import dataclass, field
from typing import Any

from apps.organization.task_planner import SubTask, TaskPlan

logger = logging.getLogger(__name__)


@dataclass
class ExecutionStage:
    stage_id: str
    stage_index: int
    subtasks: list[SubTask]
    mode: str = "serial"
    estimated_duration_minutes: float = 0.0

    def __post_init__(self) -> None:
        if not self.stage_id:
            self.stage_id = f"stage-{uuid.uuid4().hex[:8]}"
        if not self.estimated_duration_minutes:
            if self.mode == "parallel":
                self.estimated_duration_minutes = max(
                    (s.estimated_duration_minutes for s in self.subtasks), default=0.0
                )
            else:
                self.estimated_duration_minutes = sum(
                    s.estimated_duration_minutes for s in self.subtasks
                )


@dataclass
class ExecutionPlan:
    intent: Any
    stages: list[ExecutionStage]
    total_duration_minutes: float = 0.0
    parallelism_factor: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.total_duration_minutes:
            self.total_duration_minutes = float(sum(s.estimated_duration_minutes for s in self.stages))
        if not self.parallelism_factor and self.stages:
            serial_sum = sum(s.estimated_duration_minutes for s in self.stages)
            if serial_sum > 0:
                self.parallelism_factor = serial_sum / max(self.total_duration_minutes, 1.0)


class ExecutionPlanner:
    """Plans execution order from TaskPlan."""

    def plan(self, task_plan: TaskPlan) -> ExecutionPlan:
        subtasks = list(task_plan.subtasks)
        strategy = task_plan.strategy or "mixed"

        stages: list[ExecutionStage] = []
        if strategy == "serial":
            for idx, subtask in enumerate(subtasks):
                stages.append(ExecutionStage(
                    stage_id=f"stage-{idx+1}-{subtask.subtask_id[:6]}",
                    stage_index=idx + 1,
                    subtasks=[subtask],
                    mode="serial",
                ))
        elif strategy == "parallel":
            stages.append(ExecutionStage(
                stage_id=f"stage-1-{uuid.uuid4().hex[:6]}",
                stage_index=1,
                subtasks=subtasks,
                mode="parallel",
            ))
        else:
            serial_subtasks = [s for s in subtasks if not s.can_parallelize]
            parallel_subtasks = [s for s in subtasks if s.can_parallelize]
            stage_idx = 1
            if serial_subtasks:
                stages.append(ExecutionStage(
                    stage_id=f"stage-{stage_idx}-serial",
                    stage_index=stage_idx,
                    subtasks=serial_subtasks,
                    mode="serial",
                ))
                stage_idx += 1
            if parallel_subtasks:
                stages.append(ExecutionStage(
                    stage_id=f"stage-{stage_idx}-parallel",
                    stage_index=stage_idx,
                    subtasks=parallel_subtasks,
                    mode="parallel",
                ))

        logger.info(
            "ExecutionPlan created: stages=%d, parallel_factor=%.2f, strategy=%s",
            len(stages),
            0.0,
            strategy,
        )
        return ExecutionPlan(intent=task_plan.intent, stages=stages)

    def optimize_for_latency(self, execution_plan: ExecutionPlan) -> ExecutionPlan:
        for stage in execution_plan.stages:
            if stage.mode == "serial" and len(stage.subtasks) > 1:
                stage.mode = "parallel"
        execution_plan.__post_init__()
        return execution_plan

    def optimize_for_cost(self, execution_plan: ExecutionPlan) -> ExecutionPlan:
        for stage in execution_plan.stages:
            if stage.mode == "parallel" and len(stage.subtasks) > 2:
                stage.subtasks = stage.subtasks[:2]
                stage.mode = "serial"
        execution_plan.__post_init__()
        return execution_plan


execution_planner = ExecutionPlanner()
