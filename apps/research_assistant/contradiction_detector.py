"""
Contradiction Detector
=======================

Detects conflicting claims between evidence items.
"""

import logging
import random
import re
from typing import Any

from apps.research_assistant.schemas import (
    Contradiction,
    ContradictionType,
    Evidence,
    FindingSeverity,
)

logger = logging.getLogger(__name__)


class ContradictionDetector:
    """Detects conflicting claims between evidence items."""

    def detect(self, evidence_list: list[Evidence]) -> list[Contradiction]:
        contradictions: list[Contradiction] = []
        seen: set[tuple[str, str]] = set()

        for i, a in enumerate(evidence_list):
            for b in evidence_list[i + 1:]:
                pair = (a.id, b.id)
                if pair in seen:
                    continue
                seen.add(pair)

                if self._are_contradictory(a, b):
                    contradictions.append(Contradiction(
                        type=self._classify_contradiction(a, b),
                        evidence_a=a.id,
                        evidence_b=b.id,
                        description=self._describe_contradiction(a, b),
                        severity=FindingSeverity.high,
                        confidence=0.8,
                        resolution_suggestion="Further investigation needed; compare methodologies and sample sizes.",
                    ))

        return contradictions

    def _are_contradictory(self, a: Evidence, b: Evidence) -> bool:
        a_text = a.content.lower()
        b_text = b.content.lower()

        opposition_patterns = [
            (r"\b(improve|increase|enhance|boost|positive)\b", r"\b(no\s+\w+.*effect|decrease|reduce|negative|ineffective|no\s+significant)\b"),
            (r"\b(significant|strong|effective)\b", r"\b(no\s+significant|weak|ineffective|no\s+effect)\b"),
        ]
        for positive_pattern, negative_pattern in opposition_patterns:
            a_has_positive = bool(re.search(positive_pattern, a_text))
            a_has_negative = bool(re.search(negative_pattern, a_text))
            b_has_positive = bool(re.search(positive_pattern, b_text))
            b_has_negative = bool(re.search(negative_pattern, b_text))
            if (a_has_positive and b_has_negative) or (a_has_negative and b_has_positive):
                return True
        return False

    def _classify_contradiction(self, a: Evidence, b: Evidence) -> ContradictionType:
        types = list(ContradictionType)
        return random.choice(types)

    def _describe_contradiction(self, a: Evidence, b: Evidence) -> str:
        return (
            f"Conflicting claims between '{a.title}' and '{b.title}'. "
            f"Further investigation is needed to reconcile differences in methodology, sample, or interpretation."
        )
