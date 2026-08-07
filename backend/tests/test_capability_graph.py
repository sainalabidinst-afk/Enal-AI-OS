import sys

import pytest

from backend.app.core.capability_graph import CapabilityGraph
from backend.app.core.skill_registry import Skill, SkillRegistry


class TestCapabilityGraph:
    def test_build_graph_from_skills(self, monkeypatch):
        fake_registry = SkillRegistry.__new__(SkillRegistry)
        fake_registry.skills = {
            "skill-a": Skill(name="skill-a", category="test", agent="a", description="desc", capabilities=["cap-x"]),
        }
        monkeypatch.setattr(
            "backend.app.core.capability_graph.skill_registry",
            fake_registry,
        )
        graph = CapabilityGraph()
        assert "cap-x" in graph.graph
        assert "skill-a" in graph.graph["cap-x"]

    def test_get_skills_for_capabilities(self, monkeypatch):
        fake_registry = SkillRegistry.__new__(SkillRegistry)
        fake_registry.skills = {
            "skill-b": Skill(name="skill-b", category="test", agent="a", description="desc", capabilities=["cap-y"]),
        }
        monkeypatch.setattr(
            "backend.app.core.capability_graph.skill_registry",
            fake_registry,
        )
        graph = CapabilityGraph()
        skills = graph.get_skills_for_capabilities(["cap-y"])
        assert len(skills) == 1
        assert skills[0].name == "skill-b"

    def test_get_skills_for_unknown_capability(self, monkeypatch):
        fake_registry = SkillRegistry.__new__(SkillRegistry)
        fake_registry.skills = {}
        monkeypatch.setattr(
            "backend.app.core.capability_graph.skill_registry",
            fake_registry,
        )
        graph = CapabilityGraph()
        skills = graph.get_skills_for_capabilities(["unknown-cap"])
        assert skills == []

    @pytest.mark.asyncio
    async def test_get_required_capabilities(self, monkeypatch):
        fake_registry = SkillRegistry.__new__(SkillRegistry)
        fake_registry.skills = {}
        monkeypatch.setattr(
            "backend.app.core.capability_graph.skill_registry",
            fake_registry,
        )

        class FakeResponse:
            class Message:
                content = "cap-a, cap-b"

            choices = [type("Choice", (), {"message": Message()})]

        class FakeModelRouter:
            async def acomplete(self, messages, **kwargs):
                return FakeResponse()

        fake_router = FakeModelRouter()
        monkeypatch.setitem(
            sys.modules,
            "backend.app.core.model_router",
            type("module", (), {"model_router": fake_router}),
        )
        graph = CapabilityGraph()
        capabilities = await graph.get_required_capabilities("do something")
        assert capabilities == ["cap-a", "cap-b"]

    @pytest.mark.asyncio
    async def test_get_execution_plan(self, monkeypatch):
        fake_registry = SkillRegistry.__new__(SkillRegistry)
        fake_registry.skills = {
            "skill-c": Skill(name="skill-c", category="test", agent="a", description="desc", capabilities=["cap-z"], cost_weight=1.0),
            "skill-d": Skill(name="skill-d", category="test", agent="a", description="desc", capabilities=["cap-z"], cost_weight=0.5),
        }
        monkeypatch.setattr(
            "backend.app.core.capability_graph.skill_registry",
            fake_registry,
        )

        class FakeResponse:
            class Message:
                content = "cap-z"

            choices = [type("Choice", (), {"message": Message()})]

        class FakeModelRouter:
            async def acomplete(self, messages, **kwargs):
                return FakeResponse()

        fake_router = FakeModelRouter()
        monkeypatch.setitem(
            sys.modules,
            "backend.app.core.model_router",
            type("module", (), {"model_router": fake_router}),
        )
        graph = CapabilityGraph()
        plan = await graph.get_execution_plan("do something")
        assert len(plan) == 2
        assert plan[0].name == "skill-d"
        assert plan[1].name == "skill-c"
