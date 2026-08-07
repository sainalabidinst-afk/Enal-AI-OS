import json

import pytest

from backend.app.core.reflection import SelfReflection


class TestSelfReflection:
    @pytest.mark.asyncio
    async def test_review_returns_fallback_on_json_decode_error(self, monkeypatch):
        class FakeResponse:
            class Message:
                content = "not json"

            choices = [type("Choice", (), {"message": Message()})]

        class FakeRouter:
            async def acomplete(self, messages, **kwargs):
                return FakeResponse()

        monkeypatch.setattr(
            "backend.app.core.reflection.model_router",
            FakeRouter(),
        )
        reflection = SelfReflection()
        review = await reflection.review("task", "result")
        assert review["passed"] is True
        assert review["score"] == 7
        assert review["issues"] == []

    @pytest.mark.asyncio
    async def test_review_returns_fallback_on_exception(self, monkeypatch):
        class FakeRouter:
            async def acomplete(self, messages, **kwargs):
                raise Exception("model error")

        monkeypatch.setattr(
            "backend.app.core.reflection.model_router",
            FakeRouter(),
        )
        reflection = SelfReflection()
        review = await reflection.review("task", "result")
        assert review["passed"] is True
        assert review["score"] == 7
        assert review["issues"] == []

    @pytest.mark.asyncio
    async def test_improve_returns_original_on_exception(self, monkeypatch):
        class FakeRouter:
            async def acomplete(self, messages, **kwargs):
                raise Exception("model error")

        monkeypatch.setattr(
            "backend.app.core.reflection.model_router",
            FakeRouter(),
        )
        reflection = SelfReflection()
        result = await reflection.improve("task", "result", {"issues": []})
        assert result == "result"

    @pytest.mark.asyncio
    async def test_reflect_stops_on_passed_review(self, monkeypatch):
        class FakeResponse:
            class Message:
                content = json.dumps({"passed": True, "score": 9, "issues": [], "suggestions": []})

            choices = [type("Choice", (), {"message": Message()})]

        class FakeRouter:
            async def acomplete(self, messages, **kwargs):
                return FakeResponse()

        monkeypatch.setattr(
            "backend.app.core.reflection.model_router",
            FakeRouter(),
        )
        reflection = SelfReflection(max_iterations=3)
        output = await reflection.reflect("task", "result")
        assert output["final_result"] == "result"
        assert output["iterations"] == 1
        assert len(output["history"]) == 1

    @pytest.mark.asyncio
    async def test_reflect_loops_on_low_score(self, monkeypatch):
        responses = [
            {"passed": False, "score": 3, "issues": ["issue1"], "suggestions": ["fix1"]},
            {"passed": True, "score": 8, "issues": [], "suggestions": []},
        ]
        call_count = 0

        class FakeResponse:
            def __init__(self, content):
                self.choices = [type("Choice", (), {"message": type("Message", (), {"content": content})()})]

        class FakeRouter:
            async def acomplete(self, messages, **kwargs):
                nonlocal call_count
                content = json.dumps(responses[call_count % len(responses)])
                call_count += 1
                return FakeResponse(content)

        monkeypatch.setattr(
            "backend.app.core.reflection.model_router",
            FakeRouter(),
        )
        reflection = SelfReflection(max_iterations=3)
        output = await reflection.reflect("task", "result")
        assert output["iterations"] >= 2
        assert len(output["history"]) >= 2

    def test_get_feedback_summary_empty(self):
        reflection = SelfReflection()
        summary = reflection.get_feedback_summary()
        assert summary["total"] == 0
        assert summary["avg_score"] == 0.0

    @pytest.mark.asyncio
    async def test_feedback_loop_returns_original_when_score_high(self, monkeypatch):
        class FakeResponse:
            class Message:
                content = json.dumps({"passed": True, "score": 9, "issues": [], "suggestions": []})

            choices = [type("Choice", (), {"message": Message()})]

        class FakeRouter:
            async def acomplete(self, messages, **kwargs):
                return FakeResponse()

        monkeypatch.setattr(
            "backend.app.core.reflection.model_router",
            FakeRouter(),
        )
        reflection = SelfReflection()
        result = await reflection.feedback_loop("service", "task", {"result": "result"})
        assert result["improved"] == "result"
