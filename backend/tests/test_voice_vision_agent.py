import pytest

from backend.app.core.voice_vision_agent import (
    VisionAgent,
    VisionAnalysis,
    VoiceAgent,
    VoiceTranscription,
)


class TestVoiceTranscription:
    def test_defaults(self):
        vt = VoiceTranscription(text="hello", confidence=0.9)
        assert vt.language == "en"
        assert vt.duration_ms == 0.0
        assert vt.alternatives is None

    def test_with_alternatives(self):
        vt = VoiceTranscription(text="hello", confidence=0.9, alternatives=["hi", "hey"])
        assert vt.alternatives == ["hi", "hey"]


class TestVisionAnalysis:
    def test_defaults(self):
        va = VisionAnalysis(description="a cat", objects=["cat"], text_detected=[], confidence=0.8)
        assert va.metadata is None

    def test_with_metadata(self):
        va = VisionAnalysis(description="a cat", objects=["cat"], text_detected=[], confidence=0.8, metadata={"size": "large"})  # noqa: E501
        assert va.metadata == {"size": "large"}


class TestVoiceAgent:
    def test_get_supported_languages(self):
        agent = VoiceAgent()
        langs = agent.get_supported_languages()
        assert "en" in langs
        assert "id" in langs

    @pytest.mark.asyncio
    async def test_transcribe_delegates_to_stt_service(self):
        from unittest.mock import AsyncMock, patch

        from backend.app.core.stt_service import TranscriptionResult, stt_service

        mock_result = TranscriptionResult(
            text="halo", confidence=0.9, language="id", provider="test"
        )
        with patch.object(
            stt_service, "transcribe", new_callable=AsyncMock, return_value=mock_result
        ):
            agent = VoiceAgent()
            result = await agent.transcribe(b"audio", language="id")
            assert result.text == "halo"
            assert hasattr(result, "confidence")
            assert hasattr(result, "language")

    @pytest.mark.asyncio
    async def test_speak_delegates_to_tts_service(self):
        from unittest.mock import AsyncMock, patch

        from backend.app.core.tts_service import SynthesisResult, TTSService

        mock_result = SynthesisResult(
            audio_data=b"mock_audio", format="wav", sample_rate=22050, provider="mock"
        )
        with patch.object(TTSService, "speak", new_callable=AsyncMock, return_value=mock_result):
            agent = VoiceAgent()
            result = await agent.speak("hello")
            assert isinstance(result, bytes)
            assert len(result) > 0


class TestVoiceAgentEdgeCases:
    @pytest.mark.asyncio
    async def test_transcribe_unknown_provider_raises(self):
        from unittest.mock import patch

        from backend.app.core.config import settings
        from backend.app.core.stt_service import STTService

        with patch.object(settings, "STT_PROVIDER", "unknown"):
            with pytest.raises(ValueError, match="Unknown STT provider"):
                service = STTService()
                await service.transcribe(b"", language="id")

    @pytest.mark.asyncio
    async def test_speak_unknown_provider_raises(self):
        from unittest.mock import patch

        from backend.app.core.config import settings
        from backend.app.core.tts_service import TTSService

        with patch.object(settings, "TTS_PROVIDER", "invalid_tts"):
            service = TTSService()
            with pytest.raises(ValueError, match="Unknown TTS provider"):
                await service.speak("hello")


class TestVisionAgent:
    def test_get_supported_formats(self):
        agent = VisionAgent()
        formats = agent._supported_formats
        assert "png" in formats
        assert "jpg" in formats

    @pytest.mark.asyncio
    async def test_analyze_raises_for_unsupported_format(self):
        agent = VisionAgent()
        with pytest.raises(ValueError):
            await agent.analyze(b"data", format="bmp")

    @pytest.mark.asyncio
    async def test_analyze_raises_not_implemented(self):
        agent = VisionAgent()
        with pytest.raises(NotImplementedError):
            await agent.analyze(b"data", format="png")

    @pytest.mark.asyncio
    async def test_detect_objects_raises(self):
        agent = VisionAgent()
        with pytest.raises(NotImplementedError):
            await agent.detect_objects(b"data")

    @pytest.mark.asyncio
    async def test_ocr_raises(self):
        agent = VisionAgent()
        with pytest.raises(NotImplementedError):
            await agent.ocr(b"data")
