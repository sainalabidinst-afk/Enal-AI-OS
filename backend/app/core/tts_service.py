"""
Text-to-Speech Service
======================

Provides text-to-speech synthesis using multiple provider backends.
Uses lazy imports to avoid hard dependencies on provider-specific packages.

ADR-023: Voice Provider Architecture — each provider is a thin adapter over the
         underlying TTS service. Providers are lazily loaded based on configuration.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


@dataclass
class SynthesisResult:
    """Result of a text-to-speech synthesis."""

    audio_data: bytes
    format: str = "wav"
    sample_rate: int = 22050
    provider: str = ""
    metadata: dict[str, Any] | None = None


class TTSService:
    """Unified TTS service that routes to the configured provider."""

    def __init__(self) -> None:
        self._provider = settings.TTS_PROVIDER
        self._voice = settings.TTS_VOICE
        self._speed = settings.TTS_SPEED
        self._api_key = settings.TTS_API_KEY

    async def speak(
        self,
        text: str,
        voice: str | None = None,
        speed: float | None = None,
    ) -> SynthesisResult:
        """Synthesize text to speech audio bytes.

        Args:
            text: The text to synthesize.
            voice: Override voice (e.g. "en", "id"). Defaults to config.
            speed: Override speed multiplier. Defaults to config.

        Returns:
            SynthesisResult with audio_data, format, and metadata.
        """
        v = voice or self._voice
        s = speed or self._speed

        if self._provider == "pyttsx3":
            return self._speak_pyttsx3(text, v, s)
        elif self._provider == "piper":
            return await self._speak_piper(text, v, s)
        elif self._provider == "elevenlabs":
            return await self._speak_elevenlabs(text, v, s)
        elif self._provider == "openai":
            return await self._speak_openai_tts(text, v, s)
        else:
            raise ValueError(f"Unknown TTS provider: {self._provider}")

    def _speak_pyttsx3(
        self,
        text: str,
        voice: str,
        speed: float,
    ) -> SynthesisResult:
        """Synthesize using pyttsx3 (local, offline)."""
        try:
            import io

            import pyttsx3

            engine = pyttsx3.init()
            voices = engine.getProperty("voices")
            voice_lang_prefix = voice.split("-")[0]
            selected = None
            for v in voices:
                v_name = v.name.lower()
                v_id = v.id.lower()
                if voice_lang_prefix in v_name or voice_lang_prefix in v_id:
                    selected = v
                    break
            if selected:
                engine.setProperty("voice", selected.id)

            rate = engine.getProperty("rate")
            engine.setProperty("rate", int(rate * speed))

            buf = io.BytesIO()
            engine.save_to_file(text, buf)
            engine.runAndWait()
            audio_data = buf.getvalue()
            return SynthesisResult(
                audio_data=audio_data,
                format="wav",
                sample_rate=22050,
                provider="pyttsx3",
            )
        except Exception as e:
            logger.error("pyttsx3 TTS failed: %s", e)
            raise RuntimeError(f"TTS synthesis failed: {e}") from e

    async def _speak_piper(
        self,
        text: str,
        voice: str,
        speed: float,
    ) -> SynthesisResult:
        """Synthesize using Piper TTS (local, neural, high quality)."""
        try:
            import aiohttp
        except ImportError as e:
            raise RuntimeError(
                "TTS provider 'piper' requires aiohttp. Install with: pip install aiohttp"
            ) from e


        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "text": text,
                    "voice": voice,
                    "speed": speed,
                }
                async with session.post(
                    f"{settings.LOCAL_TTS_URL}/synthesize",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as resp:
                    if resp.status != 200:
                        raise RuntimeError(f"Piper TTS error: HTTP {resp.status}")
                    raw = await resp.read()
            return SynthesisResult(
                audio_data=raw,
                format="wav",
                sample_rate=22050,
                provider="piper",
            )
        except Exception as e:
            logger.error("Piper TTS failed: %s", e)
            raise RuntimeError(f"Piper TTS synthesis failed: {e}") from e

    async def _speak_elevenlabs(
        self,
        text: str,
        voice: str,
        speed: float,
    ) -> SynthesisResult:
        """Synthesize using ElevenLabs API."""
        try:
            import aiohttp
        except ImportError as e:
            raise RuntimeError(
                "TTS provider 'elevenlabs' requires aiohttp. Install with: pip install aiohttp"
            ) from e

        voice_id = settings.TTS_ELEVENLABS_VOICE_ID or voice

        headers = {}
        if self._api_key:
            headers["xi-api-key"] = self._api_key

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                    json={
                        "text": text,
                        "model_id": "eleven_multilingual_v2",
                        "voice_settings": {
                            "stability": 0.75,
                            "similarity_boost": 0.75,
                            "speed": speed,
                        },
                    },
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=20),
                ) as resp:
                    if resp.status != 200:
                        raise RuntimeError(f"ElevenLabs TTS error: HTTP {resp.status}")
                    audio_data = await resp.read()
            return SynthesisResult(
                audio_data=audio_data,
                format="mp3",
                sample_rate=44100,
                provider="elevenlabs",
            )
        except Exception as e:
            logger.error("ElevenLabs TTS failed: %s", e)
            raise RuntimeError(f"ElevenLabs TTS synthesis failed: {e}") from e

    async def _speak_openai_tts(
        self,
        text: str,
        voice: str,
        speed: float,
    ) -> SynthesisResult:
        """Synthesize using OpenAI TTS API."""
        try:
            import openai
        except ImportError as e:
            raise RuntimeError(
                "TTS provider 'openai' requires openai package. Install with: pip install openai"
            ) from e

        voice_map = {
            "en": "alloy",
            "id": "nova",
            "es": "echo",
            "fr": "fable",
            "de": "onyx",
        }
        openai_voice = voice_map.get(voice, "nova")

        client = openai.AsyncOpenAI(api_key=self._api_key or settings.OPENAI_API_KEY)
        try:
            response = await client.audio.speech.create(
                model="tts-1",
                voice=openai_voice,
                input=text,
                speed=speed,
                response_format="wav",
            )
            audio_data = response.read()
            return SynthesisResult(
                audio_data=audio_data,
                format="wav",
                sample_rate=22050,
                provider="openai-tts",
            )
        finally:
            await client.close()


tts_service = TTSService()
