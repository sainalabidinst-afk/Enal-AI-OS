import json
import logging
from typing import Any

from backend.app.core.agent_reputation import agent_reputation
from backend.app.core.config import settings
from backend.app.core.model_router import model_router

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are a Meta Planner for an AI Operating System. Your job is to decompose large projects into organizational units.

You have access to an organization tree with roles:
- CEO: Overall project ownership
- CTO: Technical leadership
- Manager: Team coordination
- Lead: Technical lead for a domain
- Specialist: Deep expertise in one area
- Worker: Execution agent

For a given request, output a JSON org structure:
{
  "root": {
    "name": "Project Name",
    "role": "ceo",
    "children": [
      {
        "name": "Division Name",
        "role": "cto",
        "children": [
          {"name": "Team Name", "role": "lead", "children": [
            {"name": "Worker Name", "role": "worker"}
          ]}
        ]
      }
    ]
  }
}

Only include necessary divisions and teams."""


class MetaPlanner:
    async def create_organization(self, project_description: str) -> dict[str, Any]:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Create an organization for: {project_description}"},
        ]
        response = model_router.complete(messages, model=settings.DEFAULT_REASONING_MODEL, temperature=0.3)
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"root": {"name": "Default", "role": "ceo", "children": []}}

    async def assign_agents(self, task_description: str) -> list[dict[str, Any]]:
        from backend.app.core.capability_graph import capability_graph
        skills = capability_graph.get_execution_plan(task_description)
        assignments = []
        for skill in skills:
            best_agent = agent_reputation.get_best_agent(skill.agent, [skill.agent])
            assignments.append({
                "skill": skill.name,
                "agent": best_agent or skill.agent,
                "capabilities": skill.capabilities,
            })
        return assignments


meta_planner = MetaPlanner()
