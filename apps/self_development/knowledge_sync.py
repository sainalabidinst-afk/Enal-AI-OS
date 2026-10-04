"""
Knowledge Sync
==============

Privacy-aware knowledge abstraction and federated memory sync for Pilar 4.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)

PII_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "<EMAIL>"),
    (re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"), "<PHONE>"),
    (re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"), "<IP>"),
    (re.compile(r"(password|secret|api_key|token)\s*[:=]\s*[^\s]+", re.IGNORECASE), "<SECRET>"),
    (re.compile(r"\b\d{4}[-]\d{4}[-]\d{4}[-]\d{4}\b"), "<CARD>"),
]


@dataclass
class KnowledgeInsight:
    insight_id: str
    source_node: str
    insight_type: str
    payload: dict[str, Any]
    pii_removed: bool = False
    accepted: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class KnowledgeAbstractor:
    """Removes PII from knowledge payloads before sync."""

    def abstract(self, payload: dict[str, Any]) -> tuple[dict[str, Any], bool]:
        text = str(payload)
        pii_removed = False
        for pattern, replacement in PII_PATTERNS:
            if pattern.search(text):
                pii_removed = True
                text = pattern.sub(replacement, text)
        if pii_removed:
            payload = dict(payload)
            payload["abstracted_text"] = text
        return payload, pii_removed


class FederatedMemorySync:
    """Distributes sanitized insights across nodes."""

    def __init__(self, abstractor: KnowledgeAbstractor | None = None) -> None:
        self.abstractor = abstractor or KnowledgeAbstractor()
        self._insights: list[KnowledgeInsight] = []

    def publish(
        self, source_node: str, insight_type: str, payload: dict[str, Any]
    ) -> KnowledgeInsight:
        abstracted, pii_removed = self.abstractor.abstract(payload)
        insight = KnowledgeInsight(
            insight_id=f"insight-{datetime.now(UTC).timestamp()}",
            source_node=source_node,
            insight_type=insight_type,
            payload=abstracted,
            pii_removed=pii_removed,
            accepted=True,
        )
        self._insights.append(insight)
        logger.info(
            "Federated insight published: %s from %s (pii_removed=%s)",
            insight.insight_id,
            source_node,
            pii_removed,
        )
        return insight

    def list_insights(self) -> list[dict[str, Any]]:
        return [
            {
                "insight_id": i.insight_id,
                "source_node": i.source_node,
                "insight_type": i.insight_type,
                "pii_removed": i.pii_removed,
                "accepted": i.accepted,
                "created_at": i.created_at.isoformat(),
            }
            for i in self._insights
        ]


federated_memory_sync = FederatedMemorySync()
