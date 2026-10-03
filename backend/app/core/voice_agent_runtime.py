"""
Voice agent runtime.

Executes voice agents through the STT → LLM → TTS pipeline.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from backend.app.core.latency_monitor import latency_monitor
from backend.app.core.stt_service import stt_service
from backend.app.core.tts_service import tts_service

logger = logging.getLogger(__name__)


class VoiceAgentRuntimeError(Exception):
    """Raised when voice agent execution fails."""


class VoiceAgentRuntime:
    """Execute a voice agent through the STT → LLM → TTS pipeline."""

    async def run(
        self,
        audio_data: bytes,
        agent_config: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        started = time.perf_counter()
        try:
            stt_start = time.perf_counter()
            text = await stt_service.transcribe(
                audio_data,
                provider=agent_config.get("sttProvider", "whisper"),
                language=agent_config.get("language", "en-US"),
            )
            stt_latency = (time.perf_counter() - stt_start) * 1000
            latency_monitor.record(stt_latency, stage="stt")

            llm_start = time.perf_counter()
            response_text = f"Simulated LLM response to: {text}"
            llm_latency = (time.perf_counter() - llm_start) * 1000
            latency_monitor.record(llm_latency, stage="llm")

            tts_start = time.perf_counter()
            audio_output = await tts_service.synthesize(
                response_text,
                provider=agent_config.get("ttsProvider", "elevenlabs"),
                voice=agent_config.get("voice", "alloy"),
            )
            tts_latency = (time.perf_counter() - tts_start) * 1000
            latency_monitor.record(tts_latency, stage="tts")

            total_latency = (time.perf_counter() - started) * 1000
            latency_monitor.record(total_latency, stage="total")

            return {
                "success": True,
                "input_text": text,
                "response_text": response_text,
                "audio_output": audio_output,
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
