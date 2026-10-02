"""
Voice Interaction Capability Pack — Worker
=============================================

Adapts the VoiceInteractionEngine for agent access through the
ECP cognitive pipeline.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.voice_interaction.engine import VoiceInteractionEngine
from apps.voice_interaction.schemas import (
    BusinessContext,
    VoiceInteractionInputs,
    VoiceInteractionOperation,
    VoiceInteractionRequest,
)

logger = logging.getLogger(__name__)


class VoiceInteractionWorker:
    """Worker adapter for the Voice Interaction capability pack."""

    def __init__(self) -> None:
        self.engine = VoiceInteractionEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """Execute a voice interaction task from the cognitive pipeline.

        Args:
            task: Task dict with keys:
                - user_input: str (text to synthesize or transcription result)
                - operation: VoiceInteractionOperation or str
                - audio_data: base64-encoded audio (for transcription)
                - source_language: str
                - target_language: str
                - stt_provider: str
                - tts_provider: str
                - tts_voice: str | None
                - tts_speed: float
                - domain: str
                - project_name: str

        Returns:
            Dict with transcriptions, syntheses, confidence, quality_score, latency_ms.
        """
        operation = task.get("operation", "transcribe")
        try:
            operation = VoiceInteractionOperation(operation)
        except ValueError:
            operation = VoiceInteractionOperation.transcribe

        inputs = VoiceInteractionInputs(
            operation=operation,
            audio_data=task.get("audio_data"),
            text=task.get("user_input", task.get("text", "")),
            source_language=task.get("source_language", "auto"),
            target_language=task.get("target_language", "en"),
            stt_provider=task.get("stt_provider", "whisper"),
            tts_provider=task.get("tts_provider", "pyttsx3"),
            tts_voice=task.get("tts_voice"),
            tts_speed=task.get("tts_speed", 1.0),
            enforce_glossary=task.get("enforce_glossary", False),
        )

        request = VoiceInteractionRequest(
            operation=operation.value,
            business_context=BusinessContext(
                project_name=task.get("project_name", "voice-session"),
                domain=task.get("domain", "general"),
            ),
            inputs=inputs,
        )

        try:
            report = self.engine.execute(request)
            return {
                "status": "ok",
                "operation": operation.value,
                "transcriptions": [t.model_dump() for t in report.transcriptions],
                "syntheses": [s.model_dump() for s in report.syntheses],
                "confidence_score": report.confidence_score,
                "quality_score": report.quality_score,
                "latency_ms": report.latency_ms,
                "model_version": report.model_version,
            }
        except Exception as exc:
            logger.error("Voice interaction worker failed: %s", exc)
            return {
                "status": "error",
                "operation": operation.value,
                "error": str(exc),
                "confidence_score": 0.0,
                "quality_score": 0.0,
            }


__all__ = ["VoiceInteractionWorker"]
