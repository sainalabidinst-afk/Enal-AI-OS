import json

import pytest

from backend.app.core.prompt_compiler import PromptCompiler


class FakeConfig:
    MAX_TOKENS = 4096
    TEMPERATURE = 0.7


class TestPromptCompiler:
    @pytest.mark.asyncio
    async def test_compile_returns_string(self, monkeypatch):
        import backend.app.core.prompt_compiler as pc_module
        monkeypatch.setattr(pc_module, "settings", FakeConfig)

        async def fake_acomplete(*args, **kwargs):
            return type("Resp", (), {"choices": [type("Choice", (), {"message": type("Message", (), {"content": "{}"})()})]})()

        monkeypatch.setattr(pc_module, "model_router", type("M", (), {"acomplete": staticmethod(fake_acomplete)})())
        monkeypatch.setattr(pc_module, "memory_manager", type("MM", (), {"search": staticmethod(lambda *a, **k: [])})())
        monkeypatch.setattr(pc_module, "skill_registry", type("SR", (), {"list_all": staticmethod(lambda: [])})())
        monkeypatch.setattr(pc_module, "experience_learning", type("EL", (), {"gather": staticmethod(lambda *a, **k: [])})())
        compiler = PromptCompiler()
        result = await compiler.compile("do something", "test-agent")
        assert isinstance(result, str)
        assert "## Intent" in result

    @pytest.mark.asyncio
    async def test_extract_intent_returns_fallback_on_bad_json(self, monkeypatch):
        import backend.app.core.prompt_compiler as pc_module
        monkeypatch.setattr(pc_module, "settings", FakeConfig)

        class FakeResponse:
            class Message:
                content = "not json"

            choices = [type("Choice", (), {"message": Message()})]

        async def fake_acomplete(*args, **kwargs):
            return FakeResponse()

        monkeypatch.setattr(pc_module, "model_router", type("M", (), {"acomplete": staticmethod(fake_acomplete)})())
        compiler = PromptCompiler()
        intent = await compiler._extract_intent("test input")
        assert intent["primary_intent"] == "test input"
        assert intent["complexity"] == "medium"

    def test_get_constraints_returns_dict(self, monkeypatch):
        import backend.app.core.prompt_compiler as pc_module
        monkeypatch.setattr(pc_module, "settings", FakeConfig)
        monkeypatch.setattr(pc_module, "skill_registry", type("SR", (), {"list_all": staticmethod(lambda: [])})())
        compiler = PromptCompiler()
        constraints = compiler._get_constraints("test-agent")
        assert constraints["agent_type"] == "test-agent"
        assert constraints["max_tokens"] == 4096
        assert constraints["temperature"] == 0.7

    @pytest.mark.asyncio
    async def test_gather_memory_handles_exceptions(self, monkeypatch):
        import backend.app.core.prompt_compiler as pc_module
        monkeypatch.setattr(pc_module, "settings", FakeConfig)
        monkeypatch.setattr(pc_module, "memory_manager", type("MM", (), {"search": staticmethod(lambda *a, **k: (_ for _ in ()).throw(Exception("fail")))})())
        compiler = PromptCompiler()
        memories = await compiler._gather_memory("test")
        assert memories == []

    def test_get_tools_for_agent_filters_by_agent(self, monkeypatch):
        import backend.app.core.prompt_compiler as pc_module
        from backend.app.core.skill_registry import Skill

        fake_skills = [
            Skill(name="s1", category="test", agent="agent-a", description="d", tools=["tool1"]),
            Skill(name="s2", category="test", agent="agent-b", description="d", tools=["tool2"]),
        ]
        monkeypatch.setattr(pc_module, "skill_registry", type("SR", (), {"list_all": staticmethod(lambda: fake_skills)})())
        compiler = PromptCompiler()
        tools = compiler._get_tools_for_agent("agent-a")
        assert tools == ["tool1"]

    @pytest.mark.asyncio
    async def test_gather_experience_returns_list(self, monkeypatch):
        import backend.app.core.prompt_compiler as pc_module
        monkeypatch.setattr(pc_module, "experience_learning", type("EL", (), {"gather": staticmethod(lambda *a, **k: [])})())
        compiler = PromptCompiler()
        experience = await compiler._gather_experience("test", "proj-1")
        assert experience == []
