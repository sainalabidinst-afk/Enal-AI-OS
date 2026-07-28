import json
import logging
from dataclasses import dataclass, field
from typing import Any

from backend.app.core.config import settings
from backend.app.core.model_router import model_router

logger = logging.getLogger(__name__)


@dataclass
class StrategicGoal:
    id: str
    description: str
    success_criteria: list[str]
    constraints: list[str] = field(default_factory=list)
    timeline: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Roadmap:
    id: str
    goal_id: str
    phases: list[dict[str, Any]]
    milestones: list[dict[str, Any]]
    estimated_duration: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class StrategicPlanner:
    def __init__(self):
        self._goals: dict[str, StrategicGoal] = {}
        self._roadmaps: dict[str, Roadmap] = {}

    async def create_strategy(self, goal_description: str, context: dict[str, Any] | None = None) -> Roadmap:
        prompt = (
            "You are a strategic planner. Create a detailed roadmap for the following goal.\n\n"
            f"Goal: {goal_description}\n"
            f"Context: {json.dumps(context or {})}\n\n"
            "Output JSON roadmap with:\n"
            "{\n"
            '  "phases": [{"name": str, "description": str, "duration": str, "deliverables": [str]}],\n'
            '  "milestones": [{"name": str, "criteria": [str], "deadline": str}],\n'
            '  "estimated_duration": str\n'
            "}"
        )
        response = model_router.complete(
            [{"role": "user", "content": prompt}],
            model=settings.DEFAULT_REASONING_MODEL,
            temperature=0.3,
            max_tokens=1024,
        )
        import uuid
        roadmap_id = f"roadmap-{uuid.uuid4().hex[:8]}"
        try:
            roadmap_data = json.loads(response.choices[0].message.content)
            roadmap = Roadmap(
                id=roadmap_id,
                goal_id=roadmap_id,
                phases=roadmap_data.get("phases", []),
                milestones=roadmap_data.get("milestones", []),
                estimated_duration=roadmap_data.get("estimated_duration"),
            )
        except (json.JSONDecodeError, AttributeError):
            roadmap = Roadmap(
                id=roadmap_id,
                goal_id=roadmap_id,
                phases=[{"name": "Execution", "description": goal_description, "duration": "1 week", "deliverables": [goal_description]}],
                milestones=[{"name": "Complete", "criteria": [goal_description], "deadline": "1 week"}],
                estimated_duration="1 week",
            )
        self._roadmaps[roadmap_id] = roadmap
        return roadmap

    async def decompose_to_workflow(self, roadmap: Roadmap) -> list[dict[str, Any]]:
        workflow_steps = []
        for phase in roadmap.phases:
            for deliverable in phase.get("deliverables", []):
                workflow_steps.append({
                    "name": deliverable,
                    "description": phase.get("description", ""),
                    "phase": phase.get("name", ""),
                })
        return workflow_steps

    def get_roadmap(self, roadmap_id: str) -> Roadmap | None:
        return self._roadmaps.get(roadmap_id)


strategic_planner = StrategicPlanner()
