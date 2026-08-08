import json
import logging
from typing import Any

from backend.app.core.agent_reputation import agent_reputation
from backend.app.core.config import settings
from backend.app.core.model_router import model_router

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = (
    "You are a Meta Planner for an AI Operating System. "
    "Your job is to decompose large projects into organizational units.\n\n"
    "You have access to an organization tree with roles:\n"
    "- CEO: Overall project ownership\n"
    "- CTO: Technical leadership\n"
    "- Manager: Team coordination\n"
    "- Lead: Technical lead for a domain\n"
    "- Specialist: Deep expertise in one area\n"
    "- Worker: Execution agent\n\n"
    "For a given request, output a JSON org structure:\n"
    "{\n"
    '  "root": {\n'
    '    "name": "Project Name",\n'
    '    "role": "ceo",\n'
    '    "children": [\n'
    "      {\n"
    '        "name": "Division Name",\n'
    '        "role": "cto",\n'
    '        "children": [\n'
    '          {"name": "Team Name", "role": "lead", "children": [\n'
    '            {"name": "Worker Name", "role": "worker"}\n'
    "          ]}\n"
    "        ]\n"
    "      }\n"
    "    ]\n"
    "  }\n"
    "}\n\n"
    "Only include necessary divisions and teams."
)


class MetaPlanner:
    async def create_organization(self, project_description: str) -> dict[str, Any]:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Create an organization for: {project_description}"},
        ]
        response = await model_router.acomplete(
            messages,
            model=settings.DEFAULT_REASONING_MODEL,
            temperature=0.3,
        )
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"root": {"name": "Default", "role": "ceo", "children": []}}

    async def assign_agents(self, task_description: str) -> list[dict[str, Any]]:
        from backend.app.core.capability_graph import capability_graph
        skills = await capability_graph.get_execution_plan(task_description)
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
