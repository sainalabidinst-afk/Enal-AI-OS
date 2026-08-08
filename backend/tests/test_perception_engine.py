import pytest

from backend.app.core.perception_engine import (
    PerceptionEngine,
    PerceptionInput,
    PerceptionResult,
)


class TestPerceptionInput:
    def test_defaults(self):
        inp = PerceptionInput(source="test", content="hello")
        assert inp.content_type == "text/plain"
        assert inp.metadata == {}

    def test_custom_values(self):
        inp = PerceptionInput(source="img", content=b"data", content_type="image/png", metadata={"size": 1024})
        assert inp.content_type == "image/png"
        assert inp.metadata["size"] == 1024


class TestPerceptionResult:
    def test_defaults(self):
        result = PerceptionResult(source="test")
        assert result.entities == []
        assert result.intents == []
        assert result.sentiment == 0.0
        assert result.confidence == 0.0
        assert result.extracted_data == {}
        assert result.metadata == {}


class TestPerceptionEngine:
    async def test_process_text(self):
        engine = PerceptionEngine()
        inp = PerceptionInput(source="test", content="find and create something great")
        result = await engine.process(inp)
        assert result.source == "test"
        assert "find" in result.entities or "create" in result.entities
        assert "search" in result.intents or "create" in result.intents
        assert result.confidence == 0.8

    async def test_process_image(self):
        engine = PerceptionEngine()
        inp = PerceptionInput(source="img", content=b"fake-bytes", content_type="image/png")
        result = await engine.process(inp)
        assert result.entities == ["image_detected"]
        assert result.intents == ["analyze_image"]
        assert result.confidence == 0.5

    async def test_process_json(self):
        engine = PerceptionEngine()
        inp = PerceptionInput(source="json", content='{"key": "value", "number": 42}', content_type="application/json")
        result = await engine.process(inp)
        assert "key" in result.entities
        assert result.extracted_data["key"] == "value"
        assert result.confidence == 0.9

    async def test_process_json_invalid(self):
        engine = PerceptionEngine()
        inp = PerceptionInput(source="json", content="not json", content_type="application/json")
        result = await engine.process(inp)
        assert result.confidence == 0.1

    async def test_process_unknown_content_type(self):
        engine = PerceptionEngine()
        inp = PerceptionInput(source="test", content="hello", content_type="application/pdf")
        result = await engine.process(inp)
        assert result.source == "test"

    async def test_process_includes_metadata(self):
        engine = PerceptionEngine()
        inp = PerceptionInput(source="test", content="hello", metadata={"lang": "en"})
        result = await engine.process(inp)
        assert result.metadata["lang"] == "en"

    def test_infer_intents_search(self):
        engine = PerceptionEngine()
        intents = engine._infer_intents("find and search for something")
        assert "search" in intents

    def test_infer_intents_create(self):
        engine = PerceptionEngine()
        intents = engine._infer_intents("make and build a new feature")
        assert "create" in intents

    def test_infer_intents_analyze(self):
        engine = PerceptionEngine()
        intents = engine._infer_intents("analyze and review the data")
        assert "analyze" in intents

    def test_infer_intents_execute(self):
        engine = PerceptionEngine()
        intents = engine._infer_intents("run and execute the task")
        assert "execute" in intents

    def test_infer_intents_general(self):
        engine = PerceptionEngine()
        intents = engine._infer_intents("hello world")
        assert intents == ["general"]

    def test_analyze_sentiment_positive(self):
        engine = PerceptionEngine()
        sentiment = engine._analyze_sentiment("good great excellent success")
        assert sentiment > 0

    def test_analyze_sentiment_negative(self):
        engine = PerceptionEngine()
        sentiment = engine._analyze_sentiment("bad poor fail error negative")
        assert sentiment < 0

    def test_analyze_sentiment_neutral(self):
        engine = PerceptionEngine()
        sentiment = engine._analyze_sentiment("hello world")
        assert sentiment == 0.0

    def test_analyze_sentiment_clamps_to_range(self):
        engine = PerceptionEngine()
        sentiment = engine._analyze_sentiment("good " * 100)
        assert sentiment <= 1.0
        sentiment2 = engine._analyze_sentiment("bad " * 100)
        assert sentiment2 >= -1.0
