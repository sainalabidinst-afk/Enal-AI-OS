"""
Text-to-Speech service.

Provides speech synthesis capabilities using multiple providers.
Supports Jenny's sexy/bratty voice personality through VoiceProfile
configuration that adjusts acoustic parameters and voice selection.
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import httpx

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
    """ElevenLabs TTS provider — calls real ElevenLabs API when key is configured."""

    async def synthesize(
        self,
        text: str,
        voice: str = "alloy",
        speed: float = 1.0,
        voice_profile: Any = None,
    ) -> bytes:
        params = {}
        voice_id = settings.TTS_ELEVENLABS_VOICE_ID or settings.JENNY_TTS_VOICE_ID
        api_key = settings.TTS_API_KEY

        if voice_profile is not None:
            params = voice_profile.acoustic_params.to_provider_overrides()
            params["voice_id"] = voice_profile.voice_id
            model = "eleven_multilingual_low_latency_2025" if voice else "eleven_flash_v2.5"
            params["model_id"] = model

        if not api_key:
            logger.warning("ElevenLabs API key not configured; returning placeholder audio")
            return b"[ElevenLabs audio placeholder -- configure TTS_API_KEY for real synthesis]"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
                body = {
                    "text": text,
                    "model_id": params.get("model_id", "eleven_flash_v2.5"),
                    "voice_settings": {
                        "stability": settings.TTS_STABILITY,
                        "similarity_boost": settings.TTS_SIMILARITY_BOOST,
                        "speed": speed,
                    },
                }
                if voice_id:
                    body["voice_id"] = voice_id
                response = await client.post(
                    "https://api.elevenlabs.io/v1/text-to-speech/stream",
                    json=body,
                    headers=headers,
                )
                response.raise_for_status()
                return response.content
        except Exception as exc:
            logger.error("ElevenLabs synthesis failed: %s", exc)
            return f"[ElevenLabs error: {exc}]".encode()


class AzureTTSProvider(TTSProvider):
    """Azure Cognitive Services TTS provider."""

    async def synthesize(
        self,
        text: str,
        voice: str = "alloy",
        speed: float = 1.0,
        voice_profile: Any = None,
    ) -> bytes:
        api_key = settings.TTS_API_KEY
        if not api_key:
            logger.warning("Azure TTS API key not configured; returning placeholder audio")
            return b"[Azure audio placeholder -- configure TTS_API_KEY for real synthesis]"
        try:
            profile_desc = voice_profile.describe() if voice_profile else "none"
            logger.info(
                "Synthesizing speech with Azure TTS (voice=%s, speed=%.2f, profile=%s)",
                voice,
                speed,
                profile_desc,
            )
            return b"[Azure audio placeholder -- SDK integration pending]"
        except Exception as exc:
            logger.error("Azure TTS synthesis failed: %s", exc)
            return f"[Azure error: {exc}]".encode()


class OpenAITTSProvider(TTSProvider):
    """OpenAI TTS provider — calls real OpenAI API when key is configured."""

    async def synthesize(
        self,
        text: str,
        voice: str = "alloy",
        speed: float = 1.0,
        voice_profile: Any = None,
    ) -> bytes:
        api_key = settings.OPENAI_API_KEY or settings.TTS_API_KEY
        if not api_key:
            logger.warning("OpenAI TTS API key not configured; returning placeholder audio")
            return b"[OpenAI audio placeholder -- configure OPENAI_API_KEY for real synthesis]"
        try:
            openai_voice = "nova" if voice_profile and voice_profile.gender == "female" else voice
            adjusted_speed = speed * (voice_profile.acoustic_params.speed if voice_profile else 1.0)
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/audio/speech",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": "tts-1",
                        "input": text,
                        "voice": openai_voice,
                        "speed": adjusted_speed,
                    },
                )
                response.raise_for_status()
                return response.content
        except Exception as exc:
            logger.error("OpenAI TTS synthesis failed: %s", exc)
            return f"[OpenAI error: {exc}]".encode()


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
        return b"[pyttsx3 audio placeholder -- local engine integration pending]"


class PiperTTSProvider(TTSProvider):
    """Piper TTS provider (local HTTP server)."""

    async def synthesize(
        self,
        text: str,
        voice: str = "alloy",
        speed: float = 1.0,
        voice_profile: Any = None,
    ) -> bytes:
        api_key = settings.TTS_API_KEY
        if not api_key:
            logger.warning("Piper TTS local server not configured; returning placeholder audio")
            return b"[Piper audio placeholder -- configure local Piper server for real synthesis]"
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{settings.LOCAL_TTS_URL}/api/synthesize",
                    json={"text": text, "voice": voice, "speed": speed},
                )
                response.raise_for_status()
                return response.content
        except Exception as exc:
            logger.error("Piper TTS synthesis failed: %s", exc)
            return f"[Piper error: {exc}]".encode()


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
