"""
Voice Interaction Capability Pack — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.voice_interaction.engine import VoiceInteractionEngine
from apps.voice_interaction.schemas import (
    AudioTranscription,
    BusinessContext,
    SpeechSynthesis,
    VoiceInteractionInputs,
    VoiceInteractionOperation,
    VoiceInteractionRecord,
    VoiceInteractionReport,
    VoiceInteractionRequest,
    VoiceLanguage,
    VoiceProvider,
)
from apps.voice_interaction.worker import VoiceInteractionWorker


class VoiceInteractionApp(BaseReferenceApp):
    name = "voice-interaction"
    version = "1.0.0"
    description = (
        "Speech-to-text transcription and text-to-speech synthesis with "
        "multi-provider support, language detection, and conversation turn management"
    )
    category = "interaction"
    pipeline = ["perception", "memory", "decision", "action"]

    def __init__(self) -> None:
        self.worker = VoiceInteractionWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> VoiceInteractionApp:
    return VoiceInteractionApp()


__all__ = [
    "VoiceInteractionApp",
    "get_app",
    "VoiceInteractionEngine",
    "VoiceInteractionWorker",
    "VoiceInteractionRequest",
    "VoiceInteractionReport",
    "VoiceInteractionInputs",
    "VoiceInteractionOperation",
    "VoiceInteractionRecord",
    "VoiceLanguage",
    "VoiceProvider",
    "AudioTranscription",
    "SpeechSynthesis",
    "BusinessContext",
]
