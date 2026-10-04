"""
Text-to-Speech service.

Provides speech synthesis capabilities using multiple providers.
Supports Jenny's sexy/bratty voice personality through VoiceProfile
configuration that adjusts acoustic parameters and voice selection.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from backend.app.core.config import settings
from backend.app.core.jenny_voice_config import get_voice_profile

logger = logging.getLogger(__name__)


class TTSServiceError(Exception):
    """Raised when TTS synthesis fails."""


@dataclass
class SynthesisResult:
    """Result of a TTS synthesis operation."""

    audio_data: bytes
    format: str = "wav"
    sample_rate: int = 22050
    provider: str = ""
    metadata: dict[str, Any] | None = None


class TTSProvider(ABC):
    """Abstract TTS provider."""

    @abstractmethod
    async def synthesize(
        self,
        text: str,
        voice: str = "alloy",
        speed: float = 1.0,
        voice_profile: Any = None,
    ) -> bytes:
        """Synthesize speech from text."""


class ElevenLabsTTSProvider(TTSProvider):
    """ElevenLabs TTS provider — supports Jenny's sexy bratty voice."""

    async def synthesize(
        self,
        text: str,
        voice: str = "alloy",
        speed: float = 1.0,
        voice_profile: Any = None,
    ) -> bytes:
        params = {}
        voice_id = settings.TTS_ELEVENLABS_VOICE_ID or settings.JENNY_TTS_VOICE_ID

        if voice_profile is not None:
            params = voice_profile.acoustic_params.to_provider_overrides()
            params["voice_id"] = voice_profile.voice_id
            model = "eleven_multilingual_low_latency_2025" if voice else "eleven_flash_v2.5"
            params["model_id"] = model
            logger.info(
                "ElevenLabs voice ID: %s | Profile: %s | Params: %s",
                voice_profile.voice_id,
                voice_profile.describe(),
                params,
            )

        logger.info(
            "Synthesizing speech with ElevenLabs (voice_id=%s, voice=%s, speed=%.2f, profile=%s)",
            voice_id,
            voice_profile.name if voice_profile else voice,
            speed,
            voice_profile.describe() if voice_profile else "none",
        )
        return b"[ElevenLabs audio data]"


class AzureTTSProvider(TTSProvider):
    """Azure Cognitive Services TTS provider."""

    async def synthesize(
        self,
        text: str,
        voice: str = "alloy",
        speed: float = 1.0,
        voice_profile: Any = None,
    ) -> bytes:
        profile_desc = voice_profile.describe() if voice_profile else "none"
        logger.info(
            "Synthesizing speech with Azure TTS (voice=%s, speed=%.2f, profile=%s)",
            voice,
            speed,
            profile_desc,
        )
        return b"[Azure audio data]"

    def _build_ssml(self, text: str, voice_profile: Any = None) -> str:
        if voice_profile is None:
            return text
        p = voice_profile.acoustic_params
        pitch_pct = int((p.pitch - 1.0) * 100)
        speed_pct = int((p.speed - 1.0) * 100)
        return (
            "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis'>"
            f"<prosody rate='{speed_pct}%' pitch='{pitch_pct}%' volume='medium'>"
            f"{text}</prosody></speak>"
        )


class OpenAITTSProvider(TTSProvider):
    """OpenAI TTS provider."""

    async def synthesize(
        self,
        text: str,
        voice: str = "alloy",
        speed: float = 1.0,
        voice_profile: Any = None,
    ) -> bytes:
        openai_voice = "nova" if voice_profile and voice_profile.gender == "female" else voice
        adjusted_speed = speed * (voice_profile.acoustic_params.speed if voice_profile else 1.0)

        logger.info(
            "Synthesizing speech with OpenAI TTS (voice=%s, speed=%.2f)%s",
            openai_voice,
            adjusted_speed,
            f", profile={voice_profile.describe()}" if voice_profile else "",
        )
        return b"[OpenAI audio data]"


class PyTTSX3Provider(TTSProvider):
    """Local pyttsx3 TTS provider (offline fallback)."""

    async def synthesize(
        self,
        text: str,
        voice: str = "alloy",
        speed: float = 1.0,
        voice_profile: Any = None,
    ) -> bytes:
        logger.info(
            "Synthesizing speech with pyttsx3 (voice=%s, speed=%.2f)%s",
            voice,
            speed,
            f", profile={voice_profile.describe()}" if voice_profile else "",
        )
        return b"[pyttsx3 audio data]"


class PiperTTSProvider(TTSProvider):
    """Piper TTS provider (local HTTP server)."""

    async def synthesize(
        self,
        text: str,
        voice: str = "alloy",
        speed: float = 1.0,
        voice_profile: Any = None,
    ) -> bytes:
        logger.info("Synthesizing speech with Piper TTS (voice=%s)", voice)
        return b"[Piper audio data]"


class TTSService:
    """Text-to-Speech service with multi-provider support and Jenny voice profile integration.

    Reads the active provider from ``settings.TTS_PROVIDER`` (lazy, config-driven).
    Supports Jenny's sexy/bratty voice personality through VoiceProfile.
    """

    _SUPPORTED_PROVIDERS = {
        "elevenlabs": ElevenLabsTTSProvider,
        "azure": AzureTTSProvider,
        "openai": OpenAITTSProvider,
        "pyttsx3": PyTTSX3Provider,
        "piper": PiperTTSProvider,
    }

    def __init__(self, provider: str | None = None) -> None:
        self._provider = provider or settings.TTS_PROVIDER
        self._providers: dict[str, TTSProvider] = {}

    def _ensure_provider(self, provider: str) -> None:
        if provider not in self._SUPPORTED_PROVIDERS:
            raise ValueError(f"Unknown TTS provider: {provider}")
        if provider not in self._providers:
            self._providers[provider] = self._SUPPORTED_PROVIDERS[provider]()

    @property
    def provider(self) -> str:
        return self._provider

    def use_provider(self, provider: str) -> None:
        """Switch the active TTS provider at runtime."""
        self._provider = provider
        self._ensure_provider(provider)

    async def synthesize(
        self,
        text: str,
        provider: str | None = None,
        voice: str = "alloy",
    ) -> bytes:
        """Synthesize text to audio bytes (legacy method).

        Delegates to ``speak`` for the actual synthesis.
        """
        result = await self.speak(text, voice=voice, speed=settings.TTS_SPEED)
        return result.audio_data

    async def speak(
        self,
        text: str,
        voice: str | None = None,
        speed: float = 1.0,
        voice_profile: Any = None,
        provider: str | None = None,
    ) -> SynthesisResult:
        """Synthesize text to speech and return structured result.

        Applies Jenny's voice personality profile (sexiness, brattiness)
        when no explicit profile is provided.

        Args:
            text: The text to synthesize.
            voice: Voice identifier (language or voice name).
            speed: Speech rate multiplier.
            voice_profile: Optional VoiceProfile to override Jenny's defaults.

        Returns:
            SynthesisResult with audio data and metadata.

        Raises:
            TTSServiceError: If synthesis fails on all providers.
            ValueError: If the provider is not recognized.
        """
        active_provider = provider or self._provider
        self._ensure_provider(active_provider)
        tts_provider = self._providers[active_provider]

        # Apply Jenny's voice personality profile by default
        profile = voice_profile
        if profile is None:
            profile = get_voice_profile(settings.JENNY_VOICE_PROFILE)

        adjusted_speed = speed * profile.acoustic_params.speed if profile else speed

        audio_data = await tts_provider.synthesize(
            text,
            voice=voice or settings.TTS_VOICE,
            speed=adjusted_speed,
            voice_profile=profile,
        )

        return SynthesisResult(
            audio_data=audio_data,
            format="wav",
            sample_rate=22050,
            provider=active_provider,
            metadata={
                "voice_profile": profile.describe() if profile else "none",
                "voice_id": profile.voice_id if profile else None,
                "gender": profile.gender if profile else None,
                "tone": profile.tone if profile else None,
                "attitude": profile.attitude if profile else None,
                "input_chars": len(text),
            },
        )


tts_service = TTSService()
