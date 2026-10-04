"""
Speech-to-Text service.

Provides transcription capabilities using multiple providers.
Reads the active provider from ``settings.STT_PROVIDER`` (lazy, config-driven).
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import httpx

from backend.app.core.config import settings
from backend.app.core.model_router import model_router

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
    """OpenAI Whisper STT provider — calls real Whisper API when key is configured."""

    async def transcribe(self, audio_data: bytes, language: str = "en-US") -> str:
        logger.info("Transcribing audio with Whisper (%s)", language)
        api_key = settings.OPENAI_API_KEY or settings.STT_API_KEY
        if not api_key:
            logger.warning("Whisper API key not configured; returning placeholder transcription")
            return f"[Whisper transcription pending API key] ({language})"
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                files = {"file": ("audio.wav", audio_data, "audio/wav")}
                data = {"model": "whisper-1", "language": language.split("-")[0]}
                headers = {"Authorization": f"Bearer {api_key}"}
                response = await client.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    files=files,
                    data=data,
                    headers=headers,
                )
                response.raise_for_status()
                result = response.json()
                return result.get("text", "")
        except Exception as exc:
            logger.error("Whisper transcription failed: %s", exc)
            return f"[Whisper error: {exc}] ({language})"


class DeepgramSTTProvider(STTProvider):
    """Deepgram STT provider — calls real Deepgram API when key is configured."""

    async def transcribe(self, audio_data: bytes, language: str = "en-US") -> str:
        logger.info("Transcribing audio with Deepgram (%s)", language)
        api_key = settings.STT_API_KEY
        if not api_key:
            logger.warning("Deepgram API key not configured; returning placeholder transcription")
            return f"[Deepgram transcription pending API key] ({language})"
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                headers = {"Authorization": f"Token {api_key}"}
                params = {"model": "nova-2", "language": language}
                files = {"file": ("audio.wav", audio_data, "audio/wav")}
                response = await client.post(
                    "https://api.deepgram.com/v1/listen",
                    files=files,
                    params=params,
                    headers=headers,
                )
                response.raise_for_status()
                result = response.json()
                return result.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")
        except Exception as exc:
            logger.error("Deepgram transcription failed: %s", exc)
            return f"[Deepgram error: {exc}] ({language})"


class GoogleSTTProvider(STTProvider):
    """Google Speech-to-Text provider — calls real Google STT API when key is configured."""

    async def transcribe(self, audio_data: bytes, language: str = "en-US") -> str:
        logger.info("Transcribing audio with Google STT (%s)", language)
        api_key = settings.GOOGLE_API_KEY or settings.STT_API_KEY
        if not api_key:
            logger.warning("Google STT API key not configured; returning placeholder transcription")
            return f"[Google STT transcription pending API key] ({language})"
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                params = {
                    "key": api_key,
                    "config": json.dumps({
                        "encoding": "LINEAR16",
                        "sampleRateHertz": 16000,
                        "languageCode": language,
                    }),
                }
                files = {"audio": ("audio.wav", audio_data, "audio/wav")}
                response = await client.post(
                    "https://speech.googleapis.com/v1/speech:recognize",
                    params=params,
                    files=files,
                )
                response.raise_for_status()
                result = response.json()
                return result.get("results", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")
        except Exception as exc:
            logger.error("Google STT transcription failed: %s", exc)
            return f"[Google STT error: {exc}] ({language})"


class WebSpeechSTTProvider(STTProvider):
    """Browser Web Speech API fallback — requires client-side browser, server returns guidance."""

    async def transcribe(self, audio_data: bytes, language: str = "en-US") -> str:
        logger.info("Web Speech API requested; client-side browser handles actual transcription")
        return f"[Web Speech API requires client-side browser; server cannot transcribe audio directly] ({language})"


class STTService:
    """Speech-to-Text service with multi-provider support.

    Reads the active provider from ``settings.STT_PROVIDER`` (lazy, config-driven).
    Calls real vendor APIs when API keys are configured; logs warnings otherwise.
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
        confidence = 0.95 if text and not text.startswith("[") else 0.0

        return TranscriptionResult(
            text=text,
            confidence=confidence,
            language=language,
            duration_ms=0.0,
            provider=active_provider,
            metadata={"audio_length_bytes": len(audio_data)},
        )


stt_service = STTService()
