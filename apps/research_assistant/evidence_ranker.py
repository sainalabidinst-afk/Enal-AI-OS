"""
Evidence Ranker
================

Ranks evidence by source quality, recency, and methodology.
"""

import logging
from datetime import datetime, timezone
from typing import Any

from apps.research_assistant.schemas import Evidence, SourceQuality

logger = logging.getLogger(__name__)


class EvidenceRanker:
    """Ranks evidence by source quality, recency, and methodology."""

    def rank(self, evidence_list: list[Evidence], query_terms: list[str]) -> list[Evidence]:
        scored: list[tuple[float, Evidence]] = []
        current_year = datetime.now(timezone.utc).year

        for ev in evidence_list:
            recency = ev.recency_score
            if ev.year > 0:
                age = max(0, current_year - ev.year)
                recency = max(recency, 1.0 - (age / 50.0))

            methodology = ev.methodology_score
            quality_map = {
                SourceQuality.peer_reviewed: 1.0,
                SourceQuality.expert_review: 0.85,
                SourceQuality.editorial: 0.7,
                SourceQuality.unverified: 0.4,
            }
            source_quality = quality_map.get(ev.source_quality, 0.5)

            relevance = ev.relevance_score
            if query_terms:
                title_lower = ev.title.lower()
                content_lower = ev.content.lower()
                keyword_hits = sum(1 for term in query_terms if term in title_lower or term in content_lower)
                relevance = max(relevance, min(1.0, keyword_hits / max(1, len(query_terms))))

            composite = (source_quality * 0.4) + (recency * 0.25) + (methodology * 0.2) + (relevance * 0.15)
            scored.append((composite, ev))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        ranked: list[Evidence] = []
        for composite, ev in scored:
            data = ev.model_dump()
            data["confidence"] = round(composite, 4)
            updated = Evidence(**data)
            ranked.append(updated)
        return ranked
