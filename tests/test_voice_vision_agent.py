"""
Tests for Voice & Vision Agent
==============================
Tests for speech-to-text, text-to-speech, and vision capabilities.
"""

import pytest


class TestVoiceAgent:
    """Tests for VoiceAgent."""

    def test_voice_agent_init(self):
        from backend.app.core.voice_vision_agent import VoiceAgent
        va = VoiceAgent()
        assert len(va._supported_languages) > 0

    def test_supported_languages(self):
        from backend.app.core.voice_vision_agent import VoiceAgent
        va = VoiceAgent()
        langs = va.get_supported_languages()
        assert "en" in langs
        assert "id" in langs

    @pytest.mark.asyncio
    async def test_transcribe_delegates_to_stt_service(self):
        from backend.app.core.stt_service import TranscriptionResult, stt_service
        from backend.app.core.voice_vision_agent import VoiceAgent
        from unittest.mock import AsyncMock, patch

        mock_result = TranscriptionResult(
            text="halo dunia", confidence=0.92, language="id", provider="test"
        )
        with patch.object(stt_service, "transcribe", new_callable=AsyncMock, return_value=mock_result):
            agent = VoiceAgent()
            result = await agent.transcribe(b"fake_audio", language="id")
            assert result.text == "halo dunia"
            assert result.confidence == 0.92
            assert hasattr(result, "language")

    @pytest.mark.asyncio
    async def test_speak_delegates_to_tts_service(self):
        from backend.app.core.config import settings
        from backend.app.core.tts_service import SynthesisResult
        from unittest.mock import patch, AsyncMock

        mock_result = SynthesisResult(
            audio_data=b"mock_audio",
            format="wav",
            sample_rate=22050,
            provider="mock",
        )
        with patch.object(settings, "TTS_PROVIDER", "mock"):
            with patch(
                "backend.app.core.tts_service.TTSService.speak",
                new_callable=AsyncMock,
                return_value=mock_result,
            ) as mock_speak:
                from backend.app.core.voice_vision_agent import VoiceAgent
                va = VoiceAgent()
                result = await va.speak("hello")
                assert isinstance(result, bytes)
                assert len(result) > 0
                mock_speak.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_transcribe_with_unknown_provider_raises(self):
        from backend.app.core.config import settings
        from backend.app.core.stt_service import STTService
        from unittest.mock import patch

        with patch.object(settings, "STT_PROVIDER", "unknown_provider"):
            service = STTService()
            with pytest.raises(ValueError, match="Unknown STT provider"):
                await service.transcribe(b"fake_audio")


class TestSTTService:
    """Tests for STTService."""

    def test_stt_service_init(self):
        from backend.app.core.stt_service import STTService
        service = STTService()
        assert service._provider is not None

    def test_transcription_result_fields(self):
        from backend.app.core.stt_service import TranscriptionResult
        result = TranscriptionResult(
            text="hello world",
            confidence=0.95,
            language="en",
            duration_ms=1500,
            provider="test",
        )
        assert result.text == "hello world"
        assert result.confidence == 0.95
        assert result.language == "en"
        assert result.duration_ms == 1500
        assert result.provider == "test"

    def test_transcription_result_to_voice_transcription(self):
        from backend.app.core.stt_service import TranscriptionResult
        result = TranscriptionResult(
            text="hello", confidence=0.9, language="id", duration_ms=1000, provider="stub"
        )
        vt = result.to_voice_transcription()
        assert vt.text == "hello"
        assert vt.confidence == 0.9
        assert vt.language == "id"
        assert vt.duration_ms == 1000


class TestTTSService:
    """Tests for TTSService."""

    def test_tts_service_init(self):
        from backend.app.core.tts_service import TTSService
        service = TTSService()
        assert service._provider is not None

    def test_synthesis_result_fields(self):
        from backend.app.core.tts_service import SynthesisResult
        result = SynthesisResult(
            audio_data=b"fake_audio_data",
            format="wav",
            sample_rate=22050,
            provider="test",
        )
        assert result.audio_data == b"fake_audio_data"
        assert result.format == "wav"
        assert result.sample_rate == 22050
        assert result.provider == "test"

    def test_synthesis_result_default_fields(self):
        from backend.app.core.tts_service import SynthesisResult
        result = SynthesisResult(audio_data=b"")
        assert result.format == "wav"
        assert result.sample_rate == 22050
        assert result.provider == ""
        assert result.metadata is None


class TestVisionAgent:
    """Tests for VisionAgent."""

    def test_vision_agent_init(self):
        from backend.app.core.voice_vision_agent import VisionAgent
        va = VisionAgent()
        assert "png" in va._supported_formats

    def test_supported_formats(self):
        from backend.app.core.voice_vision_agent import VisionAgent
        va = VisionAgent()
        assert "png" in va._supported_formats
        assert "jpg" in va._supported_formats

    def test_unsupported_format_raises(self):
        from backend.app.core.voice_vision_agent import VisionAgent
        va = VisionAgent()
        # Check format validation logic directly
        assert "bmp" not in va._supported_formats
        # The analyze method validates before raising NotImplementedError
        with pytest.raises(ValueError):
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(va.analyze(b"fake", "bmp"))
            finally:
                loop.close()

    @pytest.mark.asyncio
    async def test_analyze_raises(self):
        from backend.app.core.voice_vision_agent import VisionAgent
        va = VisionAgent()
        with pytest.raises(NotImplementedError):
            await va.analyze(b"fake_image", "png")

    @pytest.mark.asyncio
    async def test_ocr_raises(self):
        from backend.app.core.voice_vision_agent import VisionAgent
        va = VisionAgent()
        with pytest.raises(NotImplementedError):
            await va.ocr(b"fake_image")


class TestVoiceTranscription:
    """Tests for VoiceTranscription dataclass."""

    def test_transcription_creation(self):
        from backend.app.core.voice_vision_agent import VoiceTranscription
        vt = VoiceTranscription(text="hello", confidence=0.95)
        assert vt.text == "hello"
        assert vt.confidence == 0.95


class TestVisionAnalysis:
    """Tests for VisionAnalysis dataclass."""

    def test_vision_analysis_creation(self):
        from backend.app.core.voice_vision_agent import VisionAnalysis
        va = VisionAnalysis(description="a cat", objects=["cat"], text_detected=[], confidence=0.9)
        assert va.description == "a cat"
        assert "cat" in va.objects
