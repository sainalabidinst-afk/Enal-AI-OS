import json
import sys

import pytest

from backend.app.agents.meta_planner import MetaPlanner, SYSTEM_PROMPT


class TestMetaPlanner:
    @pytest.mark.asyncio
    async def test_create_organization_returns_default_on_invalid_json(self, monkeypatch):
        class FakeResponse:
            class Message:
                content = "not json"

            choices = [type("Choice", (), {"message": Message()})]

        class FakeRouter:
            async def acomplete(self, messages, **kwargs):
                return FakeResponse()

        monkeypatch.setattr(
            "backend.app.agents.meta_planner.model_router",
            FakeRouter(),
        )
        planner = MetaPlanner()
        result = await planner.create_organization("build a web app")
        assert result == {"root": {"name": "Default", "role": "ceo", "children": []}}

    @pytest.mark.asyncio
    async def test_create_organization_parses_valid_json(self, monkeypatch):
        org_json = json.dumps({"root": {"name": "Project", "role": "ceo", "children": []}})

        class FakeResponse:
            class Message:
                content = org_json

            choices = [type("Choice", (), {"message": Message()})]

        class FakeRouter:
            async def acomplete(self, messages, **kwargs):
                return FakeResponse()

        monkeypatch.setattr(
            "backend.app.agents.meta_planner.model_router",
            FakeRouter(),
        )
        planner = MetaPlanner()
        result = await planner.create_organization("build a web app")
        assert result["root"]["name"] == "Project"

    @pytest.mark.asyncio
    async def test_assign_agents_returns_assignments(self, monkeypatch):
        from backend.app.core.skill_registry import Skill, SkillRegistry

        fake_registry = SkillRegistry.__new__(SkillRegistry)
        fake_registry.skills = {
            "skill-a": Skill(name="skill-a", category="test", agent="agent-x", description="desc", capabilities=["cap-a"], cost_weight=1.0),
        }

        class FakeSkill:
            def __init__(self, skill):
                self.name = skill.name
                self.agent = skill.agent
                self.capabilities = skill.capabilities
                self.cost_weight = skill.cost_weight

        class FakeGraph:
            async def get_execution_plan(self, task_description):
                return [FakeSkill(fake_registry.skills["skill-a"])]

        class FakeReputation:
            def get_best_agent(self, capability, agents):
                return agents[0] if agents else None

        monkeypatch.setitem(
            sys.modules,
            "backend.app.core.capability_graph",
            type("module", (), {"capability_graph": FakeGraph()}),
        )
        monkeypatch.setattr(
            "backend.app.agents.meta_planner.agent_reputation",
            FakeReputation(),
        )
        planner = MetaPlanner()
        assignments = await planner.assign_agents("do something")
        assert len(assignments) == 1
        assert assignments[0]["skill"] == "skill-a"
        assert assignments[0]["agent"] == "agent-x"
