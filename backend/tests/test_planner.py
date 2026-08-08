import json

import pytest

from backend.app.core.cognitive.planner import Planner


class FakeConfig:
    DEFAULT_REASONING_MODEL = "test-reasoning"


class FakeMessage:
    def __init__(self, content):
        self.content = content


class FakeChoice:
    def __init__(self, message):
        self.message = message


class FakeResp:
    def __init__(self, content):
        self.choices = [FakeChoice(FakeMessage(content))]


class TestPlanner:
    @pytest.mark.asyncio
    async def test_create_plan_returns_plan(self, monkeypatch):
        import backend.app.core.cognitive.planner as planner_module
        monkeypatch.setattr(planner_module, "settings", FakeConfig)

        async def fake_acomplete(*args, **kwargs):
            return FakeResp(json.dumps({"description": "plan", "agents": ["planner"], "tasks": [{"description": "task", "agent": "planner"}]}))

        monkeypatch.setattr(planner_module, "model_router", type("MR", (), {"acomplete": staticmethod(fake_acomplete)})())
        planner = Planner()
        plan = await planner.create_plan("build something")
        assert plan["description"] == "plan"
        assert "planner" in plan["agents"]

    @pytest.mark.asyncio
    async def test_create_plan_fallback_on_bad_json(self, monkeypatch):
        import backend.app.core.cognitive.planner as planner_module
        monkeypatch.setattr(planner_module, "settings", FakeConfig)

        async def fake_acomplete(*args, **kwargs):
            return FakeResp("not json")

        monkeypatch.setattr(planner_module, "model_router", type("MR", (), {"acomplete": staticmethod(fake_acomplete)})())
        planner = Planner()
        plan = await planner.create_plan("build something")
        assert plan["description"] == "Direct response"
        assert plan["agents"] == ["planner"]

    @pytest.mark.asyncio
    async def test_review_result_returns_content(self, monkeypatch):
        import backend.app.core.cognitive.planner as planner_module
        monkeypatch.setattr(planner_module, "settings", FakeConfig)

        async def fake_acomplete(*args, **kwargs):
            return FakeResp("PASS")

        monkeypatch.setattr(planner_module, "model_router", type("MR", (), {"acomplete": staticmethod(fake_acomplete)})())
        planner = Planner()
        result = await planner.review_result("task", "result")
        assert result == "PASS"
