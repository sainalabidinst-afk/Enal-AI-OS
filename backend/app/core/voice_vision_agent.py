"""
Voice & Vision Agent
====================

Speech-to-text, text-to-speech, and vision capabilities.

Delegates STT/TTS to dedicated service layers (stt_service, tts_service)
that support multiple provider backends via lazy import.
"""

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class VoiceTranscription:
    text: str
    confidence: float
    language: str = "en"
    duration_ms: float = 0.0
    alternatives: list[str] | None = None


@dataclass
class VisionAnalysis:
    description: str
    objects: list[str]
    text_detected: list[str]
    confidence: float
    metadata: dict[str, Any] | None = None


class VoiceAgent:
    """Voice agent that provides speech-to-text and text-to-speech capabilities.

    Delegates to STTService and TTSService for actual provider calls.
    """

    def __init__(self):
        self._supported_languages: list[str] = ["en", "id", "es", "fr", "de"]

    async def transcribe(self, audio_data: bytes, language: str = "en") -> VoiceTranscription:
        """Transcribe audio to text using the configured STT provider.

        Args:
            audio_data: Raw audio bytes (WAV format recommended).
            language: Language code (e.g. "en", "id").

        Returns:
            VoiceTranscription with text, confidence, and alternatives.
        """
        from backend.app.core.stt_service import stt_service

        result = await stt_service.transcribe(audio_data, language=language)
        return result.to_voice_transcription()

    async def speak(self, text: str, voice: str = "default", speed: float = 1.0) -> bytes:
        """Synthesize text to speech audio using the configured TTS provider.

        Args:
            text: The text to synthesize.
            voice: Voice identifier (e.g. "en", "id").
            speed: Speech rate multiplier.

        Returns:
            Raw audio bytes (WAV or MP3 depending on provider).
        """
        from backend.app.core.tts_service import tts_service

        resolved_voice = None if voice == "default" else voice
        result = await tts_service.speak(text, voice=resolved_voice, speed=speed)
        return result.audio_data

    def get_supported_languages(self) -> list[str]:
        return list(self._supported_languages)


class VisionAgent:
    """Vision agent for image analysis and OCR.

    Vision capabilities require a vision model service (e.g. GPT-4V, Claude 3 Vision).
    Currently a skeleton — providers to be implemented based on demand.
    """

    def __init__(self):
        self._supported_formats: list[str] = ["png", "jpg", "jpeg", "gif", "webp"]

    async def analyze(self, image_data: bytes, format: str = "png") -> VisionAnalysis:
        if format not in self._supported_formats:
            raise ValueError(f"Unsupported format: {format}")
        raise NotImplementedError("Vision analysis requires vision model service")

    async def detect_objects(self, image_data: bytes) -> list[str]:
        raise NotImplementedError("Object detection requires vision model")

    async def ocr(self, image_data: bytes) -> str:
        raise NotImplementedError("OCR requires vision model service")


voice_agent = VoiceAgent()
vision_agent = VisionAgent()
