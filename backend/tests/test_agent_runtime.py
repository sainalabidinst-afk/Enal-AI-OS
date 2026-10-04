"""Tests for AgentRuntime real execution."""

import pytest

from backend.app.core.agent_runtime import AgentRuntime, AgentRuntimeError
from backend.app.core.agent_validator import AgentValidationError


class TestAgentRuntime:
    @pytest.fixture
    def runtime(self):
        return AgentRuntime()

    @pytest.mark.asyncio
    async def test_run_returns_error_for_invalid_blueprint(self, runtime):
        result = await runtime.run({"name": "", "model": "", "prompt": ""})
        assert result["success"] is False
        assert "error" in result
        assert "latency_ms" in result

    @pytest.mark.asyncio
    async def test_run_calls_model_router_for_valid_blueprint(self, runtime, monkeypatch):
        from unittest.mock import AsyncMock

        class FakeMessage:
            content = "Hello from agent"

        class FakeChoice:
            message = FakeMessage()

        fake_response = type("ModelResponse", (), {"choices": [FakeChoice()], "usage": None})()
        fake_router = AsyncMock(return_value=fake_response)
        monkeypatch.setattr(
            "backend.app.core.agent_runtime.model_router",
            type("module", (), {"acomplete": fake_router})(),
        )

        blueprint = {
            "id": "agent-1",
            "name": "TestAgent",
            "model": "gpt-4o",
            "prompt": "You are a test agent.",
            "temperature": 0.7,
            "max_tokens": 1024,
            "tools": [],
            "knowledge_base_ids": [],
            "metadata": {},
        }

        result = await runtime.run(blueprint, task="Say hello")
        assert result["success"] is True
        assert result["result"] == "Hello from agent"
        assert result["name"] == "TestAgent"
        assert result["model"] == "gpt-4o"
        fake_router.assert_called_once()
        call_kwargs = fake_router.call_args[1]
        assert call_kwargs["temperature"] == 0.7
        assert call_kwargs["max_tokens"] == 1024

    @pytest.mark.asyncio
    async def test_run_handles_llm_failure_gracefully(self, runtime, monkeypatch):
        from unittest.mock import AsyncMock

        async def fail_router(*args, **kwargs):
            raise RuntimeError("LLM unavailable")

        monkeypatch.setattr(
            "backend.app.core.agent_runtime.model_router",
            type("module", (), {"acomplete": fail_router})(),
        )

        blueprint = {
            "id": "agent-1",
            "name": "TestAgent",
            "model": "gpt-4o",
            "prompt": "You are a test agent.",
            "temperature": 0.7,
            "max_tokens": 1024,
            "tools": [],
            "knowledge_base_ids": [],
            "metadata": {},
        }

        result = await runtime.run(blueprint, task="Say hello")
        assert result["success"] is False
        assert "LLM execution failed" in result["error"]

    @pytest.mark.asyncio
    async def test_run_uses_context_when_no_task(self, runtime, monkeypatch):
        from unittest.mock import AsyncMock

        class FakeMessage:
            content = "Context-based response"

        class FakeChoice:
            message = FakeMessage()

        fake_response = type("ModelResponse", (), {"choices": [FakeChoice()], "usage": None})()
        fake_router = AsyncMock(return_value=fake_response)
        monkeypatch.setattr(
            "backend.app.core.agent_runtime.model_router",
            type("module", (), {"acomplete": fake_router})(),
        )

        blueprint = {
            "id": "agent-1",
            "name": "TestAgent",
            "model": "gpt-4o",
            "prompt": "You are a test agent.",
            "temperature": 0.7,
            "max_tokens": 1024,
            "tools": [],
            "knowledge_base_ids": [],
            "metadata": {},
        }

        result = await runtime.run(blueprint, context={"user_input": "Help me"})
        assert result["success"] is True
        assert result["result"] == "Context-based response"
        messages = fake_router.call_args[0][0]
        assert messages[-1]["content"] == "Help me"

    @pytest.mark.asyncio
    async def test_run_handles_empty_response(self, runtime, monkeypatch):
        from unittest.mock import AsyncMock

        class FakeMessage:
            content = ""

        class FakeChoice:
            message = FakeMessage()

        fake_response = type("ModelResponse", (), {"choices": [FakeChoice()], "usage": None})()
        fake_router = AsyncMock(return_value=fake_response)
        monkeypatch.setattr(
            "backend.app.core.agent_runtime.model_router",
            type("module", (), {"acomplete": fake_router})(),
        )

        blueprint = {
            "id": "agent-1",
            "name": "TestAgent",
            "model": "gpt-4o",
            "prompt": "You are a test agent.",
            "temperature": 0.7,
            "max_tokens": 1024,
            "tools": [],
            "knowledge_base_ids": [],
            "metadata": {},
        }

        result = await runtime.run(blueprint, task="Say hello")
        assert result["success"] is True
        assert result["result"] == "Agent executed but returned empty response."
