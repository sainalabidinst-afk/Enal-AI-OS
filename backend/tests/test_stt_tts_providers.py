"""Tests for STT/TTS providers real API integration."""

import pytest

from backend.app.core.config import Settings
from backend.app.core.stt_service import (
    DeepgramSTTProvider,
    GoogleSTTProvider,
    STTService,
    WhisperSTTProvider,
    WebSpeechSTTProvider,
)
from backend.app.core.tts_service import (
    AzureTTSProvider,
    ElevenLabsTTSProvider,
    OpenAITTSProvider,
    PiperTTSProvider,
    TTSService,
)


class TestSTTProviders:
    @pytest.mark.asyncio
    async def test_whisper_returns_placeholder_without_api_key(self, monkeypatch):
        monkeypatch.setattr("backend.app.core.stt_service.settings.STT_API_KEY", "")
        monkeypatch.setattr("backend.app.core.stt_service.settings.OPENAI_API_KEY", "")
        provider = WhisperSTTProvider()
        result = await provider.transcribe(b"audio_data", language="id")
        assert "Whisper" in result
        assert "API key" in result

    @pytest.mark.asyncio
    async def test_deepgram_returns_placeholder_without_api_key(self, monkeypatch):
        monkeypatch.setattr("backend.app.core.stt_service.settings.STT_API_KEY", "")
        provider = DeepgramSTTProvider()
        result = await provider.transcribe(b"audio_data", language="id")
        assert "Deepgram" in result
        assert "API key" in result

    @pytest.mark.asyncio
    async def test_google_returns_placeholder_without_api_key(self, monkeypatch):
        monkeypatch.setattr("backend.app.core.stt_service.settings.STT_API_KEY", "")
        monkeypatch.setattr("backend.app.core.stt_service.settings.GOOGLE_API_KEY", "")
        provider = GoogleSTTProvider()
        result = await provider.transcribe(b"audio_data", language="id")
        assert "Google STT" in result
        assert "API key" in result

    @pytest.mark.asyncio
    async def test_web_speech_returns_client_guidance(self):
        provider = WebSpeechSTTProvider()
        result = await provider.transcribe(b"audio_data", language="en-US")
        assert "client-side browser" in result

    @pytest.mark.asyncio
    async def test_stt_service_confidence_zero_for_placeholder(self, monkeypatch):
        monkeypatch.setattr("backend.app.core.stt_service.settings.STT_API_KEY", "")
        service = STTService(provider="whisper")
        result = await service.transcribe(b"audio_data", language="id")
        assert result.confidence == 0.0
        assert result.provider == "whisper"

    @pytest.mark.asyncio
    async def test_stt_service_confidence_high_for_real_text(self, monkeypatch):
        monkeypatch.setattr("backend.app.core.stt_service.settings.STT_API_KEY", "")
        service = STTService(provider="whisper")

        async def fake_transcribe(self, audio_data, language):
            return "Ini adalah transkripsi nyata"

        monkeypatch.setattr(WhisperSTTProvider, "transcribe", fake_transcribe)
        result = await service.transcribe(b"audio_data", language="id")
        assert result.confidence == 0.95
        assert result.text == "Ini adalah transkripsi nyata"


class TestTTSProviders:
    @pytest.mark.asyncio
    async def test_elevenlabs_returns_placeholder_without_api_key(self, monkeypatch):
        monkeypatch.setattr("backend.app.core.tts_service.settings.TTS_API_KEY", "")
        monkeypatch.setattr("backend.app.core.tts_service.settings.OPENAI_API_KEY", "")
        provider = ElevenLabsTTSProvider()
        result = await provider.synthesize("Hello world")
        assert b"placeholder" in result

    @pytest.mark.asyncio
    async def test_openai_returns_placeholder_without_api_key(self, monkeypatch):
        monkeypatch.setattr("backend.app.core.tts_service.settings.TTS_API_KEY", "")
        monkeypatch.setattr("backend.app.core.tts_service.settings.OPENAI_API_KEY", "")
        provider = OpenAITTSProvider()
        result = await provider.synthesize("Hello world")
        assert b"placeholder" in result

    @pytest.mark.asyncio
    async def test_azure_returns_placeholder_without_api_key(self, monkeypatch):
        monkeypatch.setattr("backend.app.core.tts_service.settings.TTS_API_KEY", "")
        provider = AzureTTSProvider()
        result = await provider.synthesize("Hello world")
        assert b"placeholder" in result

    @pytest.mark.asyncio
    async def test_piper_returns_placeholder_without_api_key(self, monkeypatch):
        monkeypatch.setattr("backend.app.core.tts_service.settings.TTS_API_KEY", "")
        provider = PiperTTSProvider()
        result = await provider.synthesize("Hello world")
        assert b"placeholder" in result

    @pytest.mark.asyncio
    async def test_tts_service_speak_returns_synthesis_result(self, monkeypatch):
        monkeypatch.setattr("backend.app.core.tts_service.settings.TTS_API_KEY", "")
        service = TTSService(provider="openai")
        result = await service.speak("Hello world")
        assert hasattr(result, "audio_data")
        assert hasattr(result, "provider")
        assert hasattr(result, "metadata")
        assert result.provider == "openai"

    @pytest.mark.asyncio
    async def test_tts_service_applies_jenny_voice_profile_by_default(self, monkeypatch):
        monkeypatch.setattr("backend.app.core.tts_service.settings.TTS_API_KEY", "")
        service = TTSService(provider="openai")
        result = await service.speak("Hello")
        assert result.metadata is not None
        assert "voice_profile" in result.metadata
        assert result.metadata["voice_profile"] != "none"
