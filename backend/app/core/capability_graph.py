import logging
from collections import defaultdict

from backend.app.core.skill_registry import Skill, skill_registry

logger = logging.getLogger(__name__)


class CapabilityGraph:
    def __init__(self):
        self.graph: dict[str, set[str]] = defaultdict(set)
        self._build()

    def _build(self):
        skills = skill_registry.list_all()
        for skill in skills:
            for cap in skill.capabilities:
                self.graph[cap].add(skill.name)

    async def get_required_capabilities(self, task_description: str) -> list[str]:
        from backend.app.core.model_router import model_router
        prompt = (
            "Given the following task description, list the capabilities required to complete it.\n"
            "Return only a comma-separated list of capability names.\n\n"
            f"Task: {task_description}\n"
        )
        response = await model_router.acomplete(
            [{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200,
        )
        content = response.choices[0].message.content.strip()
        return [c.strip() for c in content.split(",") if c.strip()]

    def get_skills_for_capabilities(self, capabilities: list[str]) -> list[Skill]:
        skills: dict[str, Skill] = {}
        for cap in capabilities:
            for skill_name in self.graph.get(cap, []):
                skill = skill_registry.get(skill_name)
                if skill:
                    skills[skill_name] = skill
        return list(skills.values())

    async def get_execution_plan(self, task_description: str) -> list[Skill]:
        capabilities = await self.get_required_capabilities(task_description)
        skills = self.get_skills_for_capabilities(capabilities)
        return sorted(skills, key=lambda s: s.cost_weight)


capability_graph = CapabilityGraph()
