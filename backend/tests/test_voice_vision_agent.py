import pytest

from backend.app.core.voice_vision_agent import (
    VoiceAgent,
    VoiceTranscription,
    VisionAgent,
    VisionAnalysis,
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
        va = VisionAnalysis(description="a cat", objects=["cat"], text_detected=[], confidence=0.8, metadata={"size": "large"})
        assert va.metadata == {"size": "large"}


class TestVoiceAgent:
    def test_get_supported_languages(self):
        agent = VoiceAgent()
        langs = agent.get_supported_languages()
        assert "en" in langs
        assert "id" in langs

    async def test_transcribe_raises(self):
        agent = VoiceAgent()
        with pytest.raises(NotImplementedError):
            await agent.transcribe(b"audio")

    async def test_speak_raises(self):
        agent = VoiceAgent()
        with pytest.raises(NotImplementedError):
            await agent.speak("hello")


class TestVisionAgent:
    def test_get_supported_formats(self):
        agent = VisionAgent()
        formats = agent._supported_formats
        assert "png" in formats
        assert "jpg" in formats

    async def test_analyze_raises_for_unsupported_format(self):
        agent = VisionAgent()
        with pytest.raises(ValueError):
            await agent.analyze(b"data", format="bmp")

    async def test_analyze_raises_not_implemented(self):
        agent = VisionAgent()
        with pytest.raises(NotImplementedError):
            await agent.analyze(b"data", format="png")

    async def test_detect_objects_raises(self):
        agent = VisionAgent()
        with pytest.raises(NotImplementedError):
            await agent.detect_objects(b"data")

    async def test_ocr_raises(self):
        agent = VisionAgent()
        with pytest.raises(NotImplementedError):
            await agent.ocr(b"data")
