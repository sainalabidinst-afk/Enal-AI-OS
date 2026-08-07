import sys

import pytest

from backend.app.core.model_router import ModelRouter


class FakeConfig:
    DEFAULT_MODEL = "test-model"
    DEFAULT_REASONING_MODEL = "test-reasoning"
    DEFAULT_EMBEDDING_MODEL = "test-embedding"
    OPENAI_API_KEY = "sk-test"
    ANTHROPIC_API_KEY = "sk-ant-test"
    GOOGLE_API_KEY = "sk-goog-test"
    OLLAMA_BASE_URL = "http://localhost:11434"


class TestModelRouter:
    def test_get_provider_config_gpt(self, monkeypatch):
        import backend.app.core.model_router as mr_module
        monkeypatch.setattr(mr_module, "settings", FakeConfig)
        router = ModelRouter()
        config = router.get_provider_config("gpt-4")
        assert config["api_key"] == "sk-test"

    def test_get_provider_config_claude(self, monkeypatch):
        import backend.app.core.model_router as mr_module
        monkeypatch.setattr(mr_module, "settings", FakeConfig)
        router = ModelRouter()
        config = router.get_provider_config("claude-3")
        assert config["api_key"] == "sk-ant-test"

    def test_get_provider_config_gemini(self, monkeypatch):
        import backend.app.core.model_router as mr_module
        monkeypatch.setattr(mr_module, "settings", FakeConfig)
        router = ModelRouter()
        config = router.get_provider_config("gemini-pro")
        assert config["api_key"] == "sk-goog-test"

    def test_get_provider_config_ollama(self, monkeypatch):
        import backend.app.core.model_router as mr_module
        monkeypatch.setattr(mr_module, "settings", FakeConfig)
        router = ModelRouter()
        config = router.get_provider_config("ollama/llama2")
        assert config["api_base"] == "http://localhost:11434"

    def test_complete_raises_on_failure(self, monkeypatch):
        import backend.app.core.model_router as mr_module
        monkeypatch.setattr(mr_module, "settings", FakeConfig)
        monkeypatch.setattr(mr_module, "completion", lambda **kwargs: (_ for _ in ()).throw(ValueError("fail")))
        router = ModelRouter()
        with pytest.raises(ValueError):
            router.complete([{"role": "user", "content": "hi"}])

    @pytest.mark.asyncio
    async def test_acomplete_raises_on_failure(self, monkeypatch):
        import backend.app.core.model_router as mr_module
        monkeypatch.setattr(mr_module, "settings", FakeConfig)

        async def fake_acompletion(**kwargs):
            raise ValueError("fail")

        monkeypatch.setattr(mr_module, "acompletion", fake_acompletion)
        router = ModelRouter()
        with pytest.raises(ValueError):
            await router.acomplete([{"role": "user", "content": "hi"}])
