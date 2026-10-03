"""
Voice agent runtime.

Executes voice agents through the STT → LLM → TTS pipeline.
Applies Jenny's voice personality (sexy, bratty) during TTS synthesis.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from backend.app.core.latency_monitor import latency_monitor
from backend.app.core.jenny_voice_config import get_voice_profile

logger = logging.getLogger(__name__)


class VoiceAgentRuntimeError(Exception):
    """Raised when voice agent execution fails."""


class VoiceAgentRuntime:
    """Execute a voice agent through the STT → LLM → TTS pipeline.

    TTS synthesis applies Jenny's voice personality profile (sexy, bratty)
    so that all spoken output carries her distinctive character.
    """

    async def run(
        self,
        audio_data: bytes,
        agent_config: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        started = time.perf_counter()
        try:
            stt_start = time.perf_counter()
            from backend.app.core.stt_service import STTService

            stt = STTService(provider=agent_config.get("sttProvider", "whisper"))
            transcribed = await stt.transcribe(
                audio_data,
                language=agent_config.get("language", "en-US"),
            )
            text = transcribed.text
            stt_latency = (time.perf_counter() - stt_start) * 1000
            latency_monitor.record(stt_latency, stage="stt")

            llm_start = time.perf_counter()
            response_text = f"Simulated LLM response to: {text}"
            llm_latency = (time.perf_counter() - llm_start) * 1000
            latency_monitor.record(llm_latency, stage="llm")

            tts_start = time.perf_counter()
            from backend.app.core.tts_service import TTSService

            tts = TTSService(provider=agent_config.get("ttsProvider", "elevenlabs"))
            voice_profile = get_voice_profile(agent_config.get("voiceProfile", "jenny"))
            speed = float(agent_config.get("speed", 1.0))
            result = await tts.speak(
                response_text,
                voice=agent_config.get("voice", "en"),
                speed=speed,
                voice_profile=voice_profile,
            )
            audio_output = result.audio_data
            tts_latency = (time.perf_counter() - tts_start) * 1000
            latency_monitor.record(tts_latency, stage="tts")

            total_latency = (time.perf_counter() - started) * 1000
            latency_monitor.record(total_latency, stage="total")

            return {
                "success": True,
                "input_text": text,
                "response_text": response_text,
                "audio_output": audio_output,
                "voice_profile": voice_profile.describe(),
                "latency": {
                    "stt_ms": round(stt_latency, 2),
                    "llm_ms": round(llm_latency, 2),
                    "tts_ms": round(tts_latency, 2),
                    "total_ms": round(total_latency, 2),
                },
            }
        except Exception as exc:
            logger.error("Voice agent runtime error: %s", exc)
            return {
                "success": False,
                "error": str(exc),
                "latency": {
                    "total_ms": round((time.perf_counter() - started) * 1000, 2),
                },
            }


voice_agent_runtime = VoiceAgentRuntime()
