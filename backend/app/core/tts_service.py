"""
Text-to-Speech service.

Provides speech synthesis capabilities using multiple providers.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class TTSServiceError(Exception):
    """Raised when TTS synthesis fails."""


class TTSProvider(ABC):
    """Abstract TTS provider."""

    @abstractmethod
    async def synthesize(self, text: str, voice: str = "alloy") -> bytes:
        """Synthesize speech from text."""


class ElevenLabsTTSProvider(TTSProvider):
    """ElevenLabs TTS provider."""

    async def synthesize(self, text: str, voice: str = "alloy") -> bytes:
        logger.info("Synthesizing speech with ElevenLabs (voice=%s)", voice)
        return b"[ElevenLabs audio data]"


class AzureTTSProvider(TTSProvider):
    """Azure Cognitive Services TTS provider."""

    async def synthesize(self, text: str, voice: str = "alloy") -> bytes:
        logger.info("Synthesizing speech with Azure TTS (voice=%s)", voice)
        return b"[Azure audio data]"


class OpenAITTSProvider(TTSProvider):
    """OpenAI TTS provider."""

    async def synthesize(self, text: str, voice: str = "alloy") -> bytes:
        logger.info("Synthesizing speech with OpenAI TTS (voice=%s)", voice)
        return b"[OpenAI audio data]"


class TTSService:
    """Text-to-Speech service with multiple providers."""

    def __init__(self) -> None:
        self._providers: dict[str, TTSProvider] = {
            "elevenlabs": ElevenLabsTTSProvider(),
            "azure": AzureTTSProvider(),
            "openai": OpenAITTSProvider(),
        }

    async def synthesize(
        self,
        text: str,
        provider: str = "elevenlabs",
        voice: str = "alloy",
    ) -> bytes:
        tts_provider = self._providers.get(provider)
        if not tts_provider:
            raise TTSServiceError(f"Unknown TTS provider: {provider}")
        return await tts_provider.synthesize(text, voice)


tts_service = TTSService()
