import pytest

from backend.app.core.decision_engine import DecisionEngine, DecisionOption, DecisionResult


class TestDecisionOption:
    def test_defaults(self):
        option = DecisionOption(id="opt1", description="Option 1")
        assert option.utility == 0.0
        assert option.risk == 0.0
        assert option.cost == 0.0
        assert option.confidence == 0.0
        assert option.expected_value == 0.0
        assert option.metadata == {}

    def test_custom_values(self):
        option = DecisionOption(id="opt1", description="Option 1", utility=0.8, risk=0.2, cost=0.1, confidence=0.9)
        assert option.utility == 0.8
        assert option.risk == 0.2


class TestDecisionResult:
    def test_defaults(self):
        result = DecisionResult(selected_option_id=None, selected_description=None)
        assert result.confidence == 0.0
        assert result.expected_value == 0.0
        assert result.reasoning == ""
        assert result.all_options == []


class TestDecisionEngine:
    async def test_decide_empty_options(self):
        engine = DecisionEngine()
        result = await engine.decide([])
        assert result.selected_option_id is None
        assert result.selected_description is None

    async def test_decide_single_option(self):
        engine = DecisionEngine()
        options = [DecisionOption(id="opt1", description="Only option", confidence=0.8, expected_value=0.5)]
        result = await engine.decide(options)
        assert result.selected_option_id == "opt1"
        assert result.selected_description == "Only option"
        assert result.confidence == 0.8
        assert result.expected_value == 0.5

    async def test_decide_multiple_options_selects_best(self):
        engine = DecisionEngine()
        options = [
            DecisionOption(id="opt1", description="Low", utility=0.3, confidence=0.5, risk=0.1, cost=0.1),
            DecisionOption(id="opt2", description="High", utility=0.9, confidence=0.9, risk=0.1, cost=0.1),
        ]
        result = await engine.decide(options)
        assert result.selected_option_id == "opt2"
        assert "expected value" in result.reasoning.lower()
        assert len(result.all_options) == 2

    def test_calculate_expected_value(self):
        engine = DecisionEngine()
        option = DecisionOption(id="opt1", description="Option 1", utility=0.8, confidence=0.9, risk=0.2, cost=0.1)
        ev = engine._calculate_expected_value(option)
        assert ev == (0.8 * 0.9) - (0.2 + 0.1)

    async def test_evaluate_options_returns_list(self, monkeypatch):
        engine = DecisionEngine()

        async def fake_score(task_description, alternative):
            return {"utility": 0.7, "risk": 0.3, "cost": 0.2, "confidence": 0.8}

        monkeypatch.setattr(engine, "_score_alternative", staticmethod(fake_score))
        options = await engine.evaluate_options("test task", ["alt1", "alt2"])
        assert len(options) == 2
        assert options[0].id == "opt-0"
        assert options[0].expected_value is not None

    async def test_score_alternative_returns_fallback_on_bad_json(self, monkeypatch):
        import backend.app.core.decision_engine as de_module
        engine = DecisionEngine()

        class FakeResponse:
            class Message:
                content = "not json"

            choices = [type("Choice", (), {"message": Message()})]

        class FakeRouter:
            async def acomplete(self, *args, **kwargs):
                return FakeResponse()

        monkeypatch.setattr(de_module, "model_router", FakeRouter())
        result = await engine._score_alternative("task", "alt")
        assert result["utility"] == 0.5
        assert result["risk"] == 0.5
