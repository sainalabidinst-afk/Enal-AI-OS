"""
Citation Quality Assessor
===========================

Assesses citation completeness, format accuracy, and provenance.
"""

import logging
import re
from typing import Any

from apps.research_assistant.schemas import Citation, CitationStyle, Evidence

logger = logging.getLogger(__name__)


class CitationQualityAssessor:
    """Assesses citation completeness, format accuracy, and provenance."""

    def assess(self, evidence_list: list[Evidence], style: CitationStyle) -> list[Citation]:
        citations: list[Citation] = []

        for ev in evidence_list:
            text = self._format_citation(ev, style)
            completeness = self._score_completeness(ev)
            format_accuracy = self._score_format(text, style)
            provenance = self._score_provenance(ev)

            overall = (completeness * 0.4) + (format_accuracy * 0.35) + (provenance * 0.25)
            issues: list[str] = []
            if completeness < 0.8:
                issues.append("Missing author or publication details")
            if format_accuracy < 0.8:
                issues.append("Citation format deviates from style guide")
            if provenance < 0.8:
                issues.append("Weak provenance traceability")

            citations.append(Citation(
                evidence_id=ev.id,
                style=style,
                text=text,
                completeness=completeness,
                format_accuracy=format_accuracy,
                provenance_traceability=provenance,
                overall_quality=overall,
                issues=issues,
            ))

        return citations

    def _format_citation(self, ev: Evidence, style: CitationStyle) -> str:
        authors = ", ".join(ev.authors) if ev.authors else "Unknown Author"
        year_str = str(ev.year) if ev.year else "n.d."
        if style == CitationStyle.apa:
            return f"{authors} ({year_str}). {ev.title}."
        if style == CitationStyle.mla:
            return f'{authors}. "{ev.title}." {year_str}.'
        if style == CitationStyle.ieee:
            return f'{authors}, "{ev.title}," {year_str}.'
        return f"{authors} ({year_str}). {ev.title}."

    def _score_completeness(self, ev: Evidence) -> float:
        score = 0.0
        if ev.authors:
            score += 0.4
        if ev.year > 0:
            score += 0.3
        if ev.url:
            score += 0.2
        if ev.source_type:
            score += 0.1
        return min(1.0, score)

    def _score_format(self, text: str, style: CitationStyle) -> float:
        if not text:
            return 0.0
        if style == CitationStyle.apa:
            return 1.0 if re.search(r"\(\d{4}\)", text) else 0.7
        if style == CitationStyle.ieee:
            return 1.0 if re.search(r'",\s*\d{4}', text) else 0.7
        return 0.85

    def _score_provenance(self, ev: Evidence) -> float:
        score = 0.0
        if ev.url:
            score += 0.5
        if ev.citation:
            score += 0.3
        if ev.metadata:
            score += 0.2
        return min(1.0, score)
