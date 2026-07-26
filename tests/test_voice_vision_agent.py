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
    async def test_transcribe_raises(self):
        from backend.app.core.voice_vision_agent import VoiceAgent
        va = VoiceAgent()
        with pytest.raises(NotImplementedError):
            await va.transcribe(b"fake_audio")

    @pytest.mark.asyncio
    async def test_speak_raises(self):
        from backend.app.core.voice_vision_agent import VoiceAgent
        va = VoiceAgent()
        with pytest.raises(NotImplementedError):
            await va.speak("hello")


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