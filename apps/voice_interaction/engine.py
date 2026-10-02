"""
Voice Interaction Capability Pack — Engine
=============================================

Orchestration engine for voice interaction operations.
Delegates to VoiceEngine for STT/TTS processing.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from apps.voice_interaction.schemas import (
    VoiceInteractionInputs,
    VoiceInteractionOperation,
    VoiceInteractionReport,
    VoiceInteractionRequest,
    VoiceInteractionRecord,
)
from apps.voice_interaction.voice_engine import VoiceEngine, process_voice_interaction
from apps.voice_interaction.observability_log import (
    start_voice_trace,
    log_voice_complete,
    log_voice_error,
)

logger = logging.getLogger(__name__)


class VoiceInteractionEngine:
    """
    Orchestration engine for the Voice Interaction capability pack.

    Provides a synchronous execute() interface compatible with the
    ECP capability pack convention. Delegates to async process_voice_interaction
    via asyncio.run.
    """

    def __init__(self) -> None:
        self.voice_engine = VoiceEngine()

    def execute(self, request: VoiceInteractionRequest) -> VoiceInteractionReport:
        """Process a voice interaction request synchronously.

        Wraps the async voice engine for compatibility with the
        ECP orchestration pipeline.
        """
        start_time = time.perf_counter()

        trace_id, span = start_voice_trace(
            operation=request.inputs.operation,
            language=request.inputs.source_language,
            provider=request.inputs.stt_provider or "whisper",
        )

        try:
            import asyncio

            report = asyncio.get_event_loop().run_until_complete(
                process_voice_interaction(request)
            )
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            log_voice_error(span, exc, elapsed_ms)
            raise

        elapsed_ms = (time.perf_counter() - start_time) * 1000
        log_voice_complete(
            span,
            {"quality_score": report.quality_score, "transcriptions": len(report.transcriptions)},
            elapsed_ms,
        )

        return report

    def get_record(self) -> VoiceInteractionRecord:
        return VoiceInteractionRecord()

    def get_supported_languages(self) -> list[str]:
        return self.voice_engine.get_supported_languages()

    def get_provider_info(self) -> dict[str, Any]:
        return self.voice_engine.get_provider_info()


__all__ = [
    "VoiceInteractionEngine",
]
