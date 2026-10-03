"""
Speech-to-Text service.

Provides transcription capabilities using multiple providers.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class STTServiceError(Exception):
    """Raised when STT transcription fails."""


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


class STTService:
    """Speech-to-Text service with multiple providers."""

    def __init__(self) -> None:
        self._providers: dict[str, STTProvider] = {
            "whisper": WhisperSTTProvider(),
            "deepgram": DeepgramSTTProvider(),
            "google": GoogleSTTProvider(),
        }

    async def transcribe(
        self,
        audio_data: bytes,
        provider: str = "whisper",
        language: str = "en-US",
    ) -> str:
        stt_provider = self._providers.get(provider)
        if not stt_provider:
            raise STTServiceError(f"Unknown STT provider: {provider}")
        return await stt_provider.transcribe(audio_data, language)


stt_service = STTService()
