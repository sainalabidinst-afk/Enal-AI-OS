import logging
import json
from typing import Any
from backend.app.core.config import settings
from backend.app.core.model_router import model_router
from backend.app.core.memory_layer import memory_manager
from backend.app.core.skill_registry import skill_registry
from backend.app.core.experience import experience_learning

logger = logging.getLogger(__name__)


class PromptCompiler:
    def __init__(self):
        self.default_sections = ["intent", "context", "constraints", "memory", "tools"]

    async def compile(self, user_input: str, agent_type: str, project_id: str | None = None, context: dict[str, Any] | None = None) -> str:
        sections = {}
        sections["intent"] = await self._extract_intent(user_input)
        sections["context"] = context or {}
        sections["constraints"] = self._get_constraints(agent_type)
        sections["memory"] = await self._gather_memory(user_input, project_id)
        sections["tools"] = self._get_tools_for_agent(agent_type)
        sections["experience"] = await self._gather_experience(user_input, project_id)
        return self._render(sections)

    async def _extract_intent(self, user_input: str) -> dict[str, Any]:
        prompt = (
            "Analyze the user's intent and extract key information.\n"
            "Return JSON: {\"primary_intent\": str, \"secondary_intents\": [str], \"entities\": [str], \"complexity\": str}\n\n"
            f"User input: {user_input}\n"
        )
        response = model_router.complete([{"role": "user", "content": prompt}], temperature=0.3, max_tokens=200)
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"primary_intent": user_input, "secondary_intents": [], "entities": [], "complexity": "medium"}

    def _get_constraints(self, agent_type: str) -> dict[str, Any]:
        return {
            "agent_type": agent_type,
            "max_tokens": settings.MAX_TOKENS,
            "temperature": settings.TEMPERATURE,
            "allowed_tools": self._get_tools_for_agent(agent_type),
        }

    async def _gather_memory(self, user_input: str, project_id: str | None = None) -> list[dict]:
        memories = []
        try:
            working = await memory_manager.search("working", user_input, limit=3)
            memories.extend(working)
        except Exception:
            pass
        try:
            knowledge = await memory_manager.search("knowledge", user_input, limit=3)
            memories.extend(knowledge)
        except Exception:
            pass
        return memories[:5]

    def _get_tools_for_agent(self, agent_type: str) -> list[str]:
        tools = []
        for skill in skill_registry.list_all():
            if skill.agent == agent_type:
                tools.extend(skill.tools)
        return list(set(tools))

    async def _gather_experience(self, user_input: str, project_id: str | None = None) -> list[dict]:
        if not project_id:
            return []
        try:
            lessons = experience_learning.search(user_input, limit=3)
            return [
                {"situation": lesson.situation, "action": lesson.action_taken, "outcome": lesson.outcome, "score": lesson.quality_score}
                for lesson in lessons
            ]
        except Exception:
            return []

    def _render(self, sections: dict[str, Any]) -> str:
        parts = []
        parts.append(f"## Intent\n{sections.get('intent', {}).get('primary_intent', '')}")
        if sections.get('context'):
            parts.append(f"## Context\n{json.dumps(sections['context'], indent=2)}")
        parts.append(f"## Constraints\n{json.dumps(sections.get('constraints', {}), indent=2)}")
        if sections.get('memory'):
            parts.append(f"## Relevant Memory\n{json.dumps(sections['memory'], indent=2)}")
        if sections.get('tools'):
            parts.append(f"## Available Tools\n{', '.join(sections['tools'])}")
        if sections.get('experience'):
            parts.append(f"## Past Experience\n{json.dumps(sections['experience'], indent=2)}")
        return "\n\n".join(parts)


prompt_compiler = PromptCompiler()
