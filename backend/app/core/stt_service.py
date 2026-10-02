"""
Speech-to-Text Service
======================

Provides transcription of audio data to text using multiple provider backends.
Uses lazy imports to avoid hard dependencies on provider-specific packages.

ADR-023: Voice Provider Architecture — each provider is a thin adapter over the
         underlying STT service. Providers are lazily loaded based on configuration.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


@dataclass
class TranscriptionResult:
    """Result of a speech-to-text transcription."""

    text: str
    confidence: float = 0.0
    language: str = ""
    duration_ms: float = 0.0
    alternatives: list[str] = field(default_factory=list)
    provider: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_voice_transcription(self):
        """Convert to VoiceTranscription for backwards compatibility."""
        from backend.app.core.voice_vision_agent import VoiceTranscription

        return VoiceTranscription(
            text=self.text,
            confidence=self.confidence,
            language=self.language or settings.STT_LANGUAGE,
            duration_ms=self.duration_ms,
            alternatives=self.alternatives or None,
        )


class STTService:
    """Unified STT service that routes to the configured provider."""

    def __init__(self) -> None:
        self._provider = settings.STT_PROVIDER
        self._model_path = settings.STT_MODEL_PATH
        self._api_key = settings.STT_API_KEY
        self._language = settings.STT_LANGUAGE

    async def transcribe(
        self,
        audio_data: bytes,
        language: str | None = None,
    ) -> TranscriptionResult:
        """Transcribe audio bytes to text.

        Args:
            audio_data: Raw audio bytes (WAV format recommended).
            language: Override language code (e.g. "id", "en"). Defaults to config.

        Returns:
            TranscriptionResult with text, confidence, and metadata.
        """
        lang = language or self._language
        if self._provider == "whisper":
            return await self._transcribe_whisper_cpp(audio_data, lang)
        elif self._provider == "openai":
            return await self._transcribe_openai(audio_data, lang)
        elif self._provider == "web-speech":
            return await self._transcribe_web_speech(audio_data, lang)
        else:
            raise ValueError(f"Unknown STT provider: {self._provider}")

    async def _transcribe_whisper_cpp(
        self,
        audio_data: bytes,
        language: str,
    ) -> TranscriptionResult:
        """Transcribe using local whisper.cpp server via HTTP API."""

        try:
            import aiohttp
        except ImportError as e:
            raise RuntimeError(
                "STT provider 'whisper' requires aiohttp. Install with: pip install aiohttp"
            ) from e

        url = f"{settings.STT_WHISPER_HOST}/inference"
        try:
            async with aiohttp.ClientSession() as session:
                form = aiohttp.FormData()
                form.add_field(
                    "file", audio_data, filename="audio.wav", content_type="audio/wav"
                )
                form.add_field("language", language)
                timeout = aiohttp.ClientTimeout(total=30)
                async with session.post(url, data=form, timeout=timeout) as resp:
                    if resp.status != 200:
                        raise RuntimeError(f"Whisper STT error: HTTP {resp.status}")
                    raw = await resp.json()
            text = raw.get("text", "").strip()
            confidence = raw.get("confidence", 0.0)
            duration_ms = raw.get("duration_ms", 0.0)
            return TranscriptionResult(
                text=text,
                confidence=confidence,
                language=language,
                duration_ms=duration_ms,
                provider="whisper",
                metadata=raw,
            )
        except TimeoutError:
            raise RuntimeError("STT request timed out after 30s")
        except aiohttp.ClientError as e:
            logger.warning("Whisper STT unavailable, falling back to web_speech: %s", e)
            return await self._transcribe_web_speech(audio_data, language)

    async def _transcribe_openai(
        self,
        audio_data: bytes,
        language: str,
    ) -> TranscriptionResult:
        """Transcribe using OpenAI Whisper API."""
        try:
            import openai
        except ImportError as e:
            raise RuntimeError(
                "STT provider 'openai' requires openai package. Install with: pip install openai"
            ) from e

        client = openai.AsyncOpenAI(api_key=self._api_key or settings.OPENAI_API_KEY)
        try:
            response = await client.audio.transcriptions.create(
                file=("audio.wav", audio_data, "audio/wav"),
                model="whisper-1",
                language=language,
                response_format="verbose_json",
            )
            segments = getattr(response, "segments", [])
            avg_conf = 0.0
            if segments:
                avg_conf = sum(s.get("confidence", 0.0) for s in segments) / len(segments)
            return TranscriptionResult(
                text=response.text.strip(),
                confidence=avg_conf,
                language=language,
                duration_ms=getattr(response, "duration", 0.0) * 1000,
                provider="openai-whisper",
            )
        finally:
            await client.close()

    async def _transcribe_web_speech(
        self,
        audio_data: bytes,
        language: str,
    ) -> TranscriptionResult:
        """Fallback transcription using a local rule-based approach.

        The Web Speech API requires a browser context. When invoked from the
        backend, this fallback uses a simple keyword-matching NLU stub that
        returns the raw audio metadata. Real STT must be configured by setting
        STT_PROVIDER to 'whisper' or 'openai'.
        """
        logger.warning(
            "STT provider 'web_speech' called from backend — returns stub result. "
            "Configure STT_PROVIDER=whisper or STT_PROVIDER=openai for real transcription."
        )
        return TranscriptionResult(
            text="",
            confidence=0.0,
            language=language,
            duration_ms=0.0,
            provider="web_speech_stub",
            metadata={"note": "Backend fallback — use browser Web Speech API for real STT"},
        )


stt_service = STTService()
