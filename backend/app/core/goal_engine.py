import logging
import json
from datetime import datetime
from typing import Any
from dataclasses import dataclass, field
from backend.app.core.model_router import model_router
from backend.app.core.event_bus import Event, event_bus
from backend.app.core.task_queue import Task, task_queue
from backend.app.core.state_recovery import state_recovery

logger = logging.getLogger(__name__)


@dataclass
class Goal:
    id: str
    description: str
    success_criteria: list[str]
    constraints: list[str] = field(default_factory=list)
    status: str = "active"
    progress: float = 0.0
    iterations: int = 0
    max_iterations: int = 10
    project_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class AutonomousGoalEngine:
    def __init__(self):
        self._goals: dict[str, Goal] = {}
        event_bus.subscribe("task.completed", self._on_task_completed)
        event_bus.subscribe("task.failed", self._on_task_failed)

    async def create_goal(self, description: str, success_criteria: list[str], project_id: str | None = None) -> Goal:
        goal_id = f"goal-{datetime.utcnow().timestamp()}"
        goal = Goal(
            id=goal_id,
            description=description,
            success_criteria=success_criteria,
            project_id=project_id,
        )
        self._goals[goal_id] = goal
        logger.info(f"Goal created: {goal_id} - {description}")
        return goal

    async def execute(self, goal_id: str) -> dict[str, Any]:
        goal = self._goals.get(goal_id)
        if not goal:
            raise ValueError(f"Goal not found: {goal_id}")
        while goal.status == "active" and goal.iterations < goal.max_iterations:
            goal.iterations += 1
            await state_recovery.save(goal_id, f"iteration-{goal.iterations}", {"goal": goal.description, "iteration": goal.iterations})
            task_id = await task_queue.enqueue(Task(
                name=f"goal-{goal_id}-iter-{goal.iterations}",
                agent="goal-executor",
                payload={"goal": goal.description, "iteration": goal.iterations},
            ))
            result = await task_queue.get_task(task_id)
            if result and result.status.value == "completed":
                evaluation = await self._evaluate_progress(goal, result.result)
                goal.progress = evaluation.get("progress", 0.0)
                if evaluation.get("success", False):
                    goal.status = "completed"
                    break
                if goal.progress >= 100.0:
                    goal.status = "completed"
                    break
            else:
                logger.warning(f"Goal iteration {goal.iterations} failed for {goal_id}")
        return {
            "goal_id": goal_id,
            "status": goal.status,
            "progress": goal.progress,
            "iterations": goal.iterations,
            "description": goal.description,
        }

    async def _evaluate_progress(self, goal: Goal, result: str) -> dict[str, Any]:
        prompt = (
            "Evaluate the progress toward the goal based on the result.\n"
            f"Goal: {goal.description}\n"
            f"Success Criteria: {', '.join(goal.success_criteria)}\n"
            f"Result: {result}\n\n"
            "Return JSON: {\"success\": bool, \"progress\": float(0-100), \"reasoning\": str}"
        )
        response = model_router.complete([{"role": "user", "content": prompt}], temperature=0.3, max_tokens=200)
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"success": False, "progress": 0.0, "reasoning": "Evaluation failed"}

    async def _on_task_completed(self, event: Event):
        pass

    async def _on_task_failed(self, event: Event):
        pass

    def get_goal(self, goal_id: str) -> Goal | None:
        return self._goals.get(goal_id)

    def list_goals(self, project_id: str | None = None) -> list[Goal]:
        goals = list(self._goals.values())
        if project_id:
            goals = [g for g in goals if g.project_id == project_id]
        return goals


goal_engine = AutonomousGoalEngine()
