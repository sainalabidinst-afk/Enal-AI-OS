"""
Translator Expert Schemas
=========================

Typed contracts for the Translator Expert capability pack.
Defines input (TranslationRequest) and output (TranslationReport)
contracts for multilingual translation with domain context, style control,
and glossary enforcement.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class TranslationStyle(StrEnum):
    formal = "formal"
    casual = "casual"
    technical = "technical"
    creative = "creative"


class DomainGlossary(StrEnum):
    finance = "finance"
    legal = "legal"
    medical = "medical"
    technical = "technical"
    general = "general"


class SupportedLanguage(StrEnum):
    en = "en"
    id = "id"
    es = "es"
    zh = "zh"
    fr = "fr"
    de = "de"
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
    domain: str
    stakeholder_language: str = "en"


class GlossaryEntry(BaseModel):
    term: str
    translation: str
    domain: DomainGlossary
    language_pair: str
    confidence: float = Field(default=0.95, ge=0, le=1)
    notes: str = ""


class GlossaryConfig(BaseModel):
    domain: DomainGlossary = DomainGlossary.general
    custom_terms: dict[str, str] = Field(default_factory=dict)
    enforce: bool = True


class TranslationRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_language: str | None = None
    target_language: str = "en"
    text: str
    style: TranslationStyle = TranslationStyle.formal
    business_context: BusinessContext
    inputs: GlossaryConfig = Field(default_factory=GlossaryConfig)
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class TranslationResult(BaseModel):
    translated_text: str
    detected_source_language: str | None = None
    confidence: float = Field(default=0.0, ge=0, le=1)
    glossary_terms_used: list[str] = Field(default_factory=list)
    style_applied: TranslationStyle = TranslationStyle.formal
    model_used: str = "rule-based-fallback"


class TranslationReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_language: str | None
    target_language: str
    style: TranslationStyle
    domain: DomainGlossary
    results: list[TranslationResult]
    metadata: dict[str, Any] = Field(default_factory=dict)
    quality_score: float = Field(default=0.90, ge=0, le=1)
    model_version: str = "1.0.0"


class TranslatorExpertRecord(BaseModel):
    pack_id: str = "translator-expert"
    version: str = "1.0.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "language_detection",
        "multilingual_translation",
        "contextual_adaptation",
        "style_control",
        "glossary_enforcement",
    ])


__all__ = [
    "BusinessContext",
    "DomainGlossary",
    "GlossaryConfig",
    "GlossaryEntry",
    "SupportedLanguage",
    "TranslationReport",
    "TranslationRequest",
    "TranslationResult",
    "TranslationStyle",
    "TranslatorExpertRecord",
]
