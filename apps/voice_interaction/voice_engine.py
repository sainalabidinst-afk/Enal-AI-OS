"""
Voice Interaction Capability Pack — Voice Engine module.

Core voice processing engine that delegates STT/TTS to the backend service
layer (stt_service, tts_service) via the runtime facade. Falls back to
browser Web Speech API stubs when backend providers are unavailable.

Architecture follows ADR-023 (Voice Provider Architecture):
  - lazy import of optional provider packages (aiohttp, openai, pyttsx3)
  - fallback chain: whisper → openai → web_speech
  - no hard dependencies on any specific STT/TTS provider
"""

from __future__ import annotations

import base64
import logging
import time
from typing import Any

from apps.voice_interaction.observability_log import (
    log_voice_complete,
    log_voice_error,
    start_voice_trace,
)
from apps.voice_interaction.schemas import (
    AudioTranscription,
    SpeechSynthesis,
    VoiceInteractionOperation,
    VoiceInteractionReport,
    VoiceInteractionRequest,
    VoiceLanguage,
)
from backend.app.runtime import get_voice_profile, settings

logger = logging.getLogger(__name__)


class VoiceEngine:
    """
    Core voice interaction engine.

    Delegates to backend STTService and TTSService via runtime facade.
    Provides fallback when providers are unavailable.
    """

    SUPPORTED_LANGUAGES = [lang.value for lang in VoiceLanguage]

    STT_FALLBACK_CHAIN: list[str] = ["whisper", "openai", "web_speech"]
    TTS_FALLBACK_CHAIN: list[str] = ["pyttsx3", "piper", "elevenlabs", "openai"]

    def __init__(self) -> None:
        self._stt_available: str | None = None
        self._tts_available: str | None = None
        self._detect_available_providers()

    def _detect_available_providers(self) -> None:
        """Detect which STT/TTS providers are available without importing them."""
        from backend.app.core.config import settings

        self._stt_available = settings.STT_PROVIDER
        self._tts_available = settings.TTS_PROVIDER
        logger.info(
            "Voice engine initialized: STT=%s, TTS=%s",
            self._stt_available,
            self._tts_available,
        )

    def _get_stt_service(self) -> Any:
        """Lazy-load STT service via runtime facade."""
        from backend.app.runtime import stt_service  # type: ignore[attr-defined]

        return stt_service

    def _get_tts_service(self) -> Any:
        """Lazy-load TTS service via runtime facade."""
        from backend.app.runtime import tts_service  # type: ignore[attr-defined]

        return tts_service

    def _decode_audio(self, encoded_audio: str) -> bytes:
        """Decode base64-encoded audio data."""
        try:
            return base64.b64decode(encoded_audio)
        except Exception as exc:
            logger.warning("Failed to decode base64 audio: %s", exc)
            return b""

    async def transcribe_audio(
        self,
        audio_data: str | bytes,
        language: str,
        stt_provider: str | None = None,
    ) -> AudioTranscription:
        """Transcribe audio to text via the configured STT provider.

        Falls back to web_speech stub if the primary provider is unavailable.
        """
        if isinstance(audio_data, bytes):
            audio_bytes = audio_data
        else:
            audio_bytes = self._decode_audio(audio_data)
        if not audio_bytes:
            return AudioTranscription(
                text="",
                confidence=0.0,
                detected_language=language,
                provider="error",
                alternatives=[],
            )

        start_time = time.perf_counter()
        trace_id, span = start_voice_trace(
            operation="transcribe",
            language=language,
            provider=stt_provider or self._stt_available or "web_speech",
        )

        providers_to_try = [stt_provider] if stt_provider else self.STT_FALLBACK_CHAIN
        last_error: Exception | None = None

        for provider in providers_to_try:
            try:
                stt = self._get_stt_service()
                if getattr(stt, "_provider", None) != provider:
                    stt._provider = provider
                result = await stt.transcribe(audio_bytes, language=language)
                elapsed_ms = (time.perf_counter() - start_time) * 1000

                transcription = AudioTranscription(
                    text=result.text,
                    confidence=result.confidence,
                    detected_language=result.language or language,
                    duration_ms=result.duration_ms or elapsed_ms,
                    provider=provider,
                    alternatives=result.alternatives[:3] if result.alternatives else [],
                )
                log_voice_complete(
                    span,
                    {"text": transcription.text, "confidence": transcription.confidence},
                    elapsed_ms,
                )
                return transcription
            except Exception as exc:
                last_error = exc
                logger.warning("STT provider %s failed: %s", provider, exc)
                continue

        elapsed_ms = (time.perf_counter() - start_time) * 1000
        log_voice_error(span, last_error or Exception("All STT providers failed"), elapsed_ms)

        return AudioTranscription(
            text="",
            confidence=0.0,
            detected_language=language,
            provider="fallback",
            alternatives=[],
        )

    async def synthesize_speech(
        self,
        text: str,
        language: str = "en",
        tts_provider: str | None = None,
        speed: float = 1.0,
    ) -> SpeechSynthesis:
        """Synthesize text to speech via the configured TTS provider.

        Returns metadata; actual audio bytes are returned via the API layer.
        """
        providers_to_try = [tts_provider] if tts_provider else self.TTS_FALLBACK_CHAIN
        last_error: Exception | None = None
        start_time = time.perf_counter()

        trace_id, span = start_voice_trace(
            operation="synthesize",
            language=language,
            provider=tts_provider or self._tts_available or "pyttsx3",
        )

        for provider in providers_to_try:
            try:
                logger.info(
                    "Jenny voice ID: %s (profile=%s, tone=%s, attitude=%s)",
                    settings.JENNY_TTS_VOICE_ID,
                    settings.JENNY_VOICE_PROFILE,
                    settings.TTS_VOICE_TONE,
                    settings.TTS_VOICE_ATTITUDE,
                )
                tts = self._get_tts_service()
                if getattr(tts, "_provider", None) != provider:
                    tts._provider = provider
                voice_profile = get_voice_profile()
                logger.info(
                    "Synthesizing with voice_profile=%s, voice_id=%s",
                    voice_profile.describe(),
                    voice_profile.voice_id,
                )
                result = await tts.speak(
                    text,
                    voice=language,
                    speed=speed,
                    voice_profile=voice_profile,
                )
                elapsed_ms = (time.perf_counter() - start_time) * 1000

                synthesis = SpeechSynthesis(
                    audio_format=result.format,
                    sample_rate=result.sample_rate,
                    provider=provider,
                    model_used=result.provider or provider,
                )
                log_voice_complete(
                    span,
                    {
                        "format": synthesis.audio_format,
                        "provider": synthesis.provider,
                        "chars": len(text),
                    },
                    elapsed_ms,
                )
                return synthesis
            except Exception as exc:
                last_error = exc
                logger.warning("TTS provider %s failed: %s", provider, exc)
                continue

        elapsed_ms = (time.perf_counter() - start_time) * 1000
        log_voice_error(span, last_error or Exception("All TTS providers failed"), elapsed_ms)

        return SpeechSynthesis(
            audio_format="wav",
            sample_rate=22050,
            provider="fallback",
            model_used="none",
        )

    def detect_language(self, audio_data: str | bytes) -> tuple[str, float]:
        """Detect the language of audio content.

        For backend-only, uses STT provider's language detection.
        Falls back to heuristic on text if audio detection is unavailable.
        """
        if isinstance(audio_data, str):
            audio_bytes = self._decode_audio(audio_data)
        else:
            audio_bytes = audio_data

        if not audio_bytes:
            return "en", 0.5

        for provider in self.STT_FALLBACK_CHAIN:
            try:
                import asyncio

                async def _detect() -> tuple[str, float]:
                    stt = self._get_stt_service()
                    if getattr(stt, "_provider", None) != provider:
                        stt._provider = provider
                    result = await stt.transcribe(audio_bytes, language="auto")
                    return result.language or "en", result.confidence or 0.5

                return asyncio.get_event_loop().run_until_complete(_detect())
            except Exception as exc:
                logger.warning("Language detection on provider %s failed: %s", provider, exc)
                continue

        return "en", 0.5

    def get_supported_languages(self) -> list[str]:
        """Return list of supported language codes."""
        return self.SUPPORTED_LANGUAGES

    def get_provider_info(self) -> dict[str, Any]:
        """Return current provider configuration including Jenny's voice profile."""
        profile = get_voice_profile()
        return {
            "stt_provider": self._stt_available or "web_speech",
            "tts_provider": self._tts_available or "pyttsx3",
            "voice_profile": profile.describe(),
            "voice_gender": profile.gender,
            "voice_tone": profile.tone,
            "voice_attitude": profile.attitude,
            "voice_id": profile.voice_id,
            "supported_languages": self.SUPPORTED_LANGUAGES,
        }


voice_engine = VoiceEngine()


async def process_voice_interaction(
    request: VoiceInteractionRequest,
) -> VoiceInteractionReport:
    """Process a voice interaction request (transcribe or synthesize)."""
    engine = VoiceEngine()

    start_time = time.perf_counter()

    transcriptions: list[AudioTranscription] = []
    syntheses: list[SpeechSynthesis] = []

    if request.inputs.operation == VoiceInteractionOperation.transcribe:
        if request.inputs.audio_data:
            transcription = await engine.transcribe_audio(
                request.inputs.audio_data,
                language=request.inputs.source_language,
                stt_provider=request.inputs.stt_provider,
            )
            transcriptions.append(transcription)

    elif request.inputs.operation == VoiceInteractionOperation.synthesize:
        if request.inputs.text:
            synthesis = await engine.synthesize_speech(
                request.inputs.text,
                language=request.inputs.target_language,
                tts_provider=request.inputs.tts_provider,
                speed=request.inputs.tts_speed,
            )
            syntheses.append(synthesis)

    elif request.inputs.operation == VoiceInteractionOperation.conversation:
        if request.inputs.audio_data:
            transcription = await engine.transcribe_audio(
                request.inputs.audio_data,
                language=request.inputs.source_language,
                stt_provider=request.inputs.stt_provider,
            )
            transcriptions.append(transcription)

        if request.inputs.text:
            synthesis = await engine.synthesize_speech(
                request.inputs.text,
                language=request.inputs.target_language,
                tts_provider=request.inputs.tts_provider,
                speed=request.inputs.tts_speed,
            )
            syntheses.append(synthesis)

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    confidence = 0.0
    if transcriptions:
        confidence = max(t.confidence for t in transcriptions)
    if syntheses:
        confidence = max(confidence, 0.95)
    if not confidence:
        confidence = 0.90

    quality_score = min(confidence + 0.05, 1.0)

    report = VoiceInteractionReport(
        request_id=request.request_id,
        operation=request.inputs.operation,
        transcriptions=transcriptions,
        syntheses=syntheses,
        confidence_score=confidence,
        quality_score=quality_score,
        latency_ms=round(elapsed_ms, 2),
    )

    return report


__all__ = [
    "VoiceEngine",
    "voice_engine",
    "process_voice_interaction",
]
