"""
NLU Intent Recognition — Core Service.

Classifies user intent from text input for the E2E scenario
and general-purpose dialogue management.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class IntentResult(BaseModel):
    """Result of intent classification."""

    intent: str = "unknown"
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    entities: list[dict[str, Any]] = Field(default_factory=list)
    fallback_intent: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)


class NLUService:
    """Natural Language Understanding service for intent classification."""

    VERSION = "1.0.0"

    INTENT_PATTERNS: dict[str, list[str]] = {
        "open_and_summarize_document": [
            r"\b(buka|open)\b.*\b(laporan|report|document|file)\b",
            r"\b(ringkas|summarize|summary)\b",
        ],
        "send_email": [
            r"\b(kirim|send)\b.*\b(email|mail|pesan)\b",
            r"\b(tim|team|kelompok)\b",
        ],
        "search_document": [
            r"\b(cari|search|find)\b.*\b(file|document|laporan)\b",
        ],
        "create_event": [
            r"\b(buat|create|schedule|jadwalkan)\b.*\b(meeting|event|rapat|kegiatan)\b",
        ],
        "analyze_data": [
            r"\b(analisis|analyze|analysis)\b.*\b(data|grafik|chart|tren)\b",
        ],
        "general": [
            r".*",
        ],
    }

    def classify(self, text: str) -> IntentResult:
        """Classify user intent from text."""
        text_lower = text.lower().strip()
        best_intent = "unknown"
        best_confidence = 0.0
        best_pattern_count = 0

        for intent, patterns in self.INTENT_PATTERNS.items():
            match_count = sum(1 for pattern in patterns if re.search(pattern, text_lower))
            if match_count > 0:
                confidence = min(match_count / len(patterns), 1.0)
                if match_count > best_pattern_count or (
                    match_count == best_pattern_count and confidence > best_confidence
                ):
                    best_intent = intent
                    best_confidence = confidence
                    best_pattern_count = match_count

        if best_intent == "unknown":
            best_confidence = 0.3
            best_intent = "general"
            fallback = "open_and_summarize_document"
        else:
            fallback = None

        entities = self._extract_entities(text_lower)
        params = self._extract_parameters(text_lower, best_intent, entities)

        return IntentResult(
            intent=best_intent,
            confidence=best_confidence,
            entities=entities,
            fallback_intent=fallback,
            parameters=params,
        )

    def _extract_entities(self, text: str) -> list[dict[str, Any]]:
        """Extract named entities from text."""
        entities: list[dict[str, Any]] = []
        email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
        for match in email_pattern.finditer(text):
            entities.append({"type": "email", "value": match.group(0)})

        folder_pattern = re.compile(r"(?:folder|directory|path)[:\s]+([^\s,]+)", re.IGNORECASE)
        for match in folder_pattern.finditer(text):
            entities.append({"type": "folder", "value": match.group(1)})

        return entities

    def _extract_parameters(
        self, text: str, intent: str, entities: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Extract intent parameters from text."""
        params: dict[str, Any] = {}
        if intent == "open_and_summarize_document":
            params["query"] = text
            params["folder"] = "Documents/Finance"
            params["recipients"] = []
            for entity in entities:
                if entity["type"] == "email":
                    params["recipients"].append(entity["value"])
        elif intent == "send_email":
            params["recipients"] = [e["value"] for e in entities if e["type"] == "email"]
        elif intent == "create_event":
            params["title"] = text[:50]
        elif intent == "search_document":
            params["query"] = text
        elif intent == "analyze_data":
            params["data_source"] = "unknown"
        return params

    def get_supported_intents(self) -> list[str]:
        """Return list of supported intents."""
        return list(self.INTENT_PATTERNS.keys())

    def get_record(self) -> dict[str, Any]:
        """Return a capability record for registry/memory."""
        return {
            "pack_id": "nlu-intent-recognition",
            "version": self.VERSION,
            "capabilities": ["classify", "extract_entities", "extract_parameters"],
        }


nlu_service = NLUService()
