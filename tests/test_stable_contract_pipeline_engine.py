"""
Tests for backend/app/core/pipeline_engine.py — RFC-0001 Pipeline Engine.
"""

import pytest

from backend.app.core.pipeline_engine import PipelineEngine, PipelineStage, pipeline_engine
from backend.app.core.schemas import TaskIntentRequest


class TestPipelineEngine:
    @pytest.fixture
    def engine(self):
        eng = PipelineEngine(use_redis=False)
        eng.clear()
        return eng

    @pytest.fixture
    def task(self):
        return TaskIntentRequest(intent="code_engineer.generate")

    def test_define_and_get_pipeline(self, engine):
        stages = [
            PipelineStage(name="parse", capability="parse"),
            PipelineStage(name="analyze", capability="analyze"),
        ]
        engine.define_pipeline("test_pack", stages)
        assert engine.get_pipeline("test_pack") == stages

    def test_register_stage_handler(self, engine):
        async def handler(ctx):
            return {"parsed": True}

        engine.register_stage_handler("parse", handler)
        assert engine.get_pipeline("test_pack") == []

    @pytest.mark.asyncio
    async def test_execute_pipeline_success(self, engine, task):
        engine.define_pipeline(
            "test_pack",
            [
                PipelineStage(name="parse", capability="parse"),
                PipelineStage(name="analyze", capability="analyze"),
            ],
        )

        results = {}

        def make_handler(stage_name):
            async def handler(ctx):
                results[stage_name] = True
                return {"status": "done", "stage": stage_name}

            return handler

        engine.register_stage_handler("parse", make_handler("parse"))
        engine.register_stage_handler("analyze", make_handler("analyze"))

        result = await engine.execute_pipeline(task, "test_pack")
        assert result.status == "success"
        assert len(results) == 2
        assert result.result.payload["pack_id"] == "test_pack"
        assert result.metrics.latency_ms >= 0

    @pytest.mark.asyncio
    async def test_execute_pipeline_missing_handler(self, engine, task):
        engine.define_pipeline(
            "test_pack",
            [
                PipelineStage(name="parse", capability="parse"),
            ],
        )
        # No handler registered for "parse"

        result = await engine.execute_pipeline(task, "test_pack")
        assert result.status == "failure"
        assert result.error is not None
        assert result.error.code == "PIPELINE_STAGE_FAILED"

    @pytest.mark.asyncio
    async def test_execute_pipeline_handler_error(self, engine, task):
        engine.define_pipeline(
            "test_pack",
            [
                PipelineStage(name="parse", capability="parse"),
            ],
        )

        async def bad_handler(ctx):
            raise RuntimeError("handler crashed")

        engine.register_stage_handler("parse", bad_handler)
        result = await engine.execute_pipeline(task, "test_pack")
        assert result.status == "failure"
        assert "handler crashed" in result.error.message

    @pytest.mark.asyncio
    async def test_events_emitted_during_pipeline(self, engine, task):
        engine.define_pipeline(
            "test_pack",
            [
                PipelineStage(name="parse", capability="parse"),
            ],
        )

        async def handler(ctx):
            return {"ok": True}

        engine.register_stage_handler("parse", handler)

        result = await engine.execute_pipeline(task, "test_pack")
        event_types = [e.event_type for e in result.events_emitted]
        assert "pipeline.stage.started" in event_types
        assert "pipeline.stage.completed" in event_types

    @pytest.mark.asyncio
    async def test_empty_pipeline(self, engine, task):
        engine.define_pipeline("empty_pack", [])

        result = await engine.execute_pipeline(task, "empty_pack")
        assert result.status == "success"
        assert len(result.events_emitted) >= 2  # started + completed

    @pytest.mark.asyncio
    async def test_get_history(self, engine, task):
        engine.define_pipeline(
            "test_pack",
            [
                PipelineStage(name="parse", capability="parse"),
            ],
        )

        async def handler(ctx):
            return {"ok": True}

        engine.register_stage_handler("parse", handler)
        await engine.execute_pipeline(task, "test_pack")

        history = engine.get_history(task.task_id)
        assert len(history) == 1

    @pytest.mark.asyncio
    async def test_handler_output_passed_to_next_stage(self, engine, task):
        engine.define_pipeline(
            "test_pack",
            [
                PipelineStage(name="step1", capability="cap1"),
                PipelineStage(name="step2", capability="cap2"),
            ],
        )

        async def cap1_handler(ctx):
            return {"intermediate": "value"}

        async def cap2_handler(ctx):
            # stage_results from previous stages are flattened into ctx
            intermediate = ctx.get("cap1", {}).get("intermediate")
            return {"received": intermediate}

        engine.register_stage_handler("cap1", cap1_handler)
        engine.register_stage_handler("cap2", cap2_handler)

        result = await engine.execute_pipeline(task, "test_pack")
        assert result.status == "success"
        stage_results = result.result.payload["stage_results"]
        assert stage_results["cap2"]["received"] == "value"

    def test_global_pipeline_engine_singleton(self):
        assert pipeline_engine is not None
        assert isinstance(pipeline_engine, PipelineEngine)
