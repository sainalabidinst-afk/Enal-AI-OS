"""Tests for the local GPU inference provider (ADR-037).

These tests must pass on machines with no CUDA device and no downloaded weights,
because the whole point of the design is that GPU inference degrades instead of
breaking the platform.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from backend.app.core.gpu_inference_service import (
    GPUInferenceError,
    GPUInferenceService,
    GPUUnavailableError,
    get_gpu_service,
    reset_gpu_service,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


class TestLazyImports:
    def test_import_does_not_load_torch_or_transformers(self):
        """Module import must not drag torch/transformers into the process.

        Regression guard for the 25s startup tax described in ADR-037: the Model
        Router imports this module eagerly, so a heavy module-scope import slows
        every backend startup and every test collection.
        """
        code = (
            "import sys, backend.app.core.gpu_inference_service as m; "
            "print('torch' in sys.modules, 'transformers' in sys.modules)"
        )
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=300,
            check=True,
        )
        assert result.stdout.strip() == "False False"

    def test_initialize_raises_typed_error_without_torch(self, monkeypatch):
        service = GPUInferenceService(model_path=str(REPO_ROOT))

        def _no_torch():
            raise GPUUnavailableError("torch is not installed")

        monkeypatch.setattr(service, "_import_torch", staticmethod(_no_torch))
        with pytest.raises(GPUUnavailableError):
            service.initialize()
        assert service.initialized is False


class TestAvailability:
    def test_missing_model_directory_raises_unavailable(self, tmp_path):
        service = GPUInferenceService(model_path=str(tmp_path / "absent"))
        with pytest.raises(GPUUnavailableError, match="model directory not found"):
            service.initialize()

    def test_initialize_is_idempotent_flag(self, tmp_path):
        service = GPUInferenceService(model_path=str(tmp_path / "absent"))
        assert service.initialized is False
        with pytest.raises(GPUUnavailableError):
            service.initialize()
        assert service.initialized is False

    def test_generate_before_initialize_raises(self, tmp_path):
        service = GPUInferenceService(model_path=str(tmp_path))
        with pytest.raises(GPUInferenceError, match="not initialized"):
            service._generate("hello")

    def test_format_messages_requires_tokenizer(self, tmp_path):
        service = GPUInferenceService(model_path=str(tmp_path))
        with pytest.raises(GPUInferenceError, match="not initialized"):
            service._format_messages([{"role": "user", "content": "hi"}])


class TestStatus:
    def test_status_reports_health_snapshot(self, tmp_path):
        model_dir = tmp_path / "qwen2.5-3b"
        model_dir.mkdir()
        service = GPUInferenceService(model_path=str(model_dir))

        status = service.status()

        assert status["model_path"] == str(model_dir)
        assert status["model_exists"] is True
        assert status["initialized"] is False
        assert status["quantized"] is True
        assert status["max_context_tokens"] > 0
        assert "fallback_model" in status

    def test_status_reports_missing_weights(self, tmp_path):
        service = GPUInferenceService(model_path=str(tmp_path / "absent"))
        assert service.status()["model_exists"] is False


class TestSingleton:
    def test_disabled_by_default_returns_none(self, monkeypatch):
        from backend.app.core import config

        monkeypatch.setattr(config.settings, "GPU_INFERENCE_ENABLED", False)
        reset_gpu_service()
        assert get_gpu_service() is None

    def test_enabled_returns_singleton_and_resets(self, monkeypatch, tmp_path):
        from backend.app.core import config

        monkeypatch.setattr(config.settings, "GPU_INFERENCE_ENABLED", True)
        monkeypatch.setattr(config.settings, "GPU_MODEL_PATH", str(tmp_path))
        reset_gpu_service()

        first = get_gpu_service()
        second = get_gpu_service()

        assert first is not None
        assert first is second
        assert first.model_path == str(tmp_path)

        reset_gpu_service()
        assert get_gpu_service() is not first

    def teardown_method(self):
        reset_gpu_service()


class TestModelRouterFallback:
    @pytest.mark.asyncio
    async def test_gpu_request_falls_back_when_disabled(self, monkeypatch):
        from backend.app.core import config
        from backend.app.core.model_router import ModelRouter

        monkeypatch.setattr(config.settings, "GPU_INFERENCE_ENABLED", False)
        monkeypatch.setattr(config.settings, "GPU_FALLBACK_ENABLED", True)

        captured: dict = {}

        async def _fake_acompletion(**kwargs):
            captured.update(kwargs)
            return {"choices": [{"message": {"content": "fallback"}}]}

        monkeypatch.setattr("backend.app.core.model_router.acompletion", _fake_acompletion)

        result = await ModelRouter().acomplete(
            [{"role": "user", "content": "hi"}],
            model="gpu/qwen2.5-3b",
            max_tokens=32,
        )

        assert result["choices"][0]["message"]["content"] == "fallback"
        assert captured["model"] == config.settings.FALLBACK_MODEL

    @pytest.mark.asyncio
    async def test_gpu_request_raises_when_fallback_disabled(self, monkeypatch):
        from backend.app.core import config
        from backend.app.core.model_router import ModelRouter

        monkeypatch.setattr(config.settings, "GPU_INFERENCE_ENABLED", False)
        monkeypatch.setattr(config.settings, "GPU_FALLBACK_ENABLED", False)

        with pytest.raises(GPUUnavailableError):
            await ModelRouter().acomplete(
                [{"role": "user", "content": "hi"}],
                model="gpu/qwen2.5-3b",
            )
