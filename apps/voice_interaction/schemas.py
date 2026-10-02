"""
Voice Interaction Capability Pack — Schemas
=============================================

Typed contracts for the Voice Interaction capability pack.
Defines input (VoiceInteractionRequest) and output (VoiceInteractionReport)
contracts for speech-to-text transcription and text-to-speech synthesis
with confidence scoring and multi-provider support.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class VoiceInteractionOperation(StrEnum):
    transcribe = "transcribe"
    synthesize = "synthesize"
    conversation = "conversation"


class VoiceProvider(StrEnum):
    whisper = "whisper"
    openai = "openai"
    web_speech = "web_speech"
    pyttsx3 = "pyttsx3"
    piper = "piper"
    elevenlabs = "elevenlabs"


class VoiceLanguage(StrEnum):
    en = "en"
    id = "id"
    es = "es"
    fr = "fr"
    de = "de"
    zh = "zh"
    ja = "ja"
    ar = "ar"
    pt = "pt"
    ru = "ru"
    it = "it"
    nl = "nl"
    ko = "ko"
    vi = "vi"
    th = "th"
    tr = "tr"
    pl = "pl"
    hi = "hi"
    ms = "ms"
    sw = "sw"
    ur = "ur"
    bn = "bn"


class BusinessContext(BaseModel):
    project_name: str
    domain: str = "general"
    stakeholder_language: str = "en"


class VoiceInteractionInputs(BaseModel):
    operation: VoiceInteractionOperation
    audio_data: str | None = None
    text: str = ""
    source_language: str = "auto"
    target_language: str = "en"
    stt_provider: str = "whisper"
    tts_provider: str = "pyttsx3"
    tts_voice: str | None = None
    tts_speed: float = Field(default=1.0, ge=0.5, le=2.0)
    enforce_glossary: bool = False


class AudioTranscription(BaseModel):
    text: str
    confidence: float = Field(default=0.0, ge=0, le=1)
    detected_language: str | None = None
    duration_ms: float = 0.0
    provider: str = ""
    alternatives: list[str] = Field(default_factory=list)


class SpeechSynthesis(BaseModel):
    audio_format: str = "wav"
    sample_rate: int = 22050
    provider: str = ""
    model_used: str = "fallback"


class VoiceInteractionReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operation: VoiceInteractionOperation
    transcriptions: list[AudioTranscription] = Field(default_factory=list)
    syntheses: list[SpeechSynthesis] = Field(default_factory=list)
    confidence_score: float = Field(default=0.90, ge=0, le=1)
    quality_score: float = Field(default=0.90, ge=0, le=1)
    latency_ms: float = 0.0
    model_version: str = "1.0.0"


class VoiceInteractionRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "transcribe"
    business_context: BusinessContext
    inputs: VoiceInteractionInputs
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class VoiceInteractionRecord(BaseModel):
    pack_id: str = "voice-interaction"
    version: str = "1.0.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "speech_to_text",
        "text_to_speech",
        "voice_conversation",
        "language_detection",
    ])


__all__ = [
    "BusinessContext",
    "VoiceInteractionInputs",
    "VoiceInteractionOperation",
    "VoiceInteractionRequest",
    "VoiceInteractionReport",
    "VoiceInteractionRecord",
    "VoiceLanguage",
    "VoiceProvider",
    "AudioTranscription",
    "SpeechSynthesis",
]
