"""
Speech-to-Text service.

Provides transcription capabilities using multiple providers.
Reads the active provider from ``settings.STT_PROVIDER`` (lazy, config-driven).
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class STTServiceError(Exception):
    """Raised when STT transcription fails."""


@dataclass
class TranscriptionResult:
    """Result of an STT transcription operation."""

    text: str
    confidence: float = 0.0
    language: str = "en"
    duration_ms: float = 0.0
    provider: str = ""
    metadata: dict[str, Any] | None = None

    def to_voice_transcription(self):
        """Convert to VoiceTranscription dataclass used by VoiceAgent."""
        from backend.app.core.voice_vision_agent import VoiceTranscription

        return VoiceTranscription(
            text=self.text,
            confidence=self.confidence,
            language=self.language,
            duration_ms=self.duration_ms,
            alternatives=None,
        )


class STTProvider(ABC):
    """Abstract STT provider."""

    @abstractmethod
    async def transcribe(self, audio_data: bytes, language: str = "en-US") -> str:
        """Transcribe audio data to text."""


class WhisperSTTProvider(STTProvider):
    """OpenAI Whisper STT provider."""

    async def transcribe(self, audio_data: bytes, language: str = "en-US") -> str:
        logger.info("Transcribing audio with Whisper (%s)", language)
        return f"[Whisper transcription] ({language})"


class DeepgramSTTProvider(STTProvider):
    """Deepgram STT provider."""

    async def transcribe(self, audio_data: bytes, language: str = "en-US") -> str:
        logger.info("Transcribing audio with Deepgram (%s)", language)
        return f"[Deepgram transcription] ({language})"


class GoogleSTTProvider(STTProvider):
    """Google Speech-to-Text provider."""

    async def transcribe(self, audio_data: bytes, language: str = "en-US") -> str:
        logger.info("Transcribing audio with Google STT (%s)", language)
        return f"[Google STT transcription] ({language})"


class WebSpeechSTTProvider(STTProvider):
    """Browser Web Speech API fallback stub."""

    async def transcribe(self, audio_data: bytes, language: str = "en-US") -> str:
        logger.info("Transcribing audio with Web Speech API (%s)", language)
        return f"[Web Speech transcription] ({language})"


class STTService:
    """Speech-to-Text service with multi-provider support.

    Reads the active provider from ``settings.STT_PROVIDER`` (lazy, config-driven).
    """

    _SUPPORTED_PROVIDERS = {
        "whisper": WhisperSTTProvider,
        "deepgram": DeepgramSTTProvider,
        "google": GoogleSTTProvider,
        "web_speech": WebSpeechSTTProvider,
    }

    def __init__(self, provider: str | None = None) -> None:
        self._provider = provider or settings.STT_PROVIDER
        self._providers: dict[str, STTProvider] = {}

    def _ensure_provider(self, provider: str) -> None:
        if provider not in self._SUPPORTED_PROVIDERS:
            raise ValueError(f"Unknown STT provider: {provider}")
        if provider not in self._providers:
            self._providers[provider] = self._SUPPORTED_PROVIDERS[provider]()

    @property
    def provider(self) -> str:
        return self._provider

    def use_provider(self, provider: str) -> None:
        """Switch the active STT provider at runtime."""
        self._provider = provider
        self._ensure_provider(provider)

    async def transcribe(
        self,
        audio_data: bytes,
        provider: str | None = None,
        language: str = "en-US",
    ) -> TranscriptionResult:
        """Transcribe audio data to text.

        Args:
            audio_data: Raw audio bytes.
            provider: Override the configured provider.
            language: Language code (e.g. "en-US", "id").

        Returns:
            TranscriptionResult with text, confidence, and metadata.

        Raises:
            ValueError: If the provider is not recognized.
        """
        active_provider = provider or self._provider
        self._ensure_provider(active_provider)
        stt_provider = self._providers[active_provider]

        text = await stt_provider.transcribe(audio_data, language)

        return TranscriptionResult(
            text=text,
            confidence=0.95,
            language=language,
            duration_ms=0.0,
            provider=active_provider,
            metadata={"audio_length_bytes": len(audio_data)},
        )


stt_service = STTService()
