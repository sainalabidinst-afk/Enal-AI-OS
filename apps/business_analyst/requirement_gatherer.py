"""
Business Analyst — Requirement Gatherer.

Collects, structures, and validates business requirements
from natural language inputs and stakeholder notes.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from apps.business_analyst.schemas import (
    StakeholderInput,
    BusinessContext,
    Requirement,
    RequirementType,
    Priority,
)

logger = logging.getLogger(__name__)


# Keywords that indicate functional requirements.
_FUNCTIONAL_KEYWORDS = {
    "must", "shall", "should", "will", "need", "require", "create", "generate",
    "display", "show", "send", "receive", "process", "calculate", "validate",
    "authenticate", "authorize", "store", "retrieve", "update", "delete",
}

# Keywords that indicate non-functional requirements.
_NON_FUNCTIONAL_KEYWORDS = {
    "performance", "latency", "availability", "scalability", "security",
    "reliability", "throughput", "capacity", "response time", "uptime",
    "encryption", "compliance", "audit", "monitoring", "backup",
}


class RequirementGatherer:
    """
    Collects and structures business requirements.

    Usage::

        gatherer = RequirementGatherer()
        requirements = gatherer.gather(inputs, context)
    """

    def gather(
        self,
        inputs: StakeholderInput,
        context: BusinessContext,
    ) -> list[Requirement]:
        """
        Gather and structure requirements from inputs.

        Args:
            inputs: StakeholderInput with requirements, notes, transcripts.
            context: BusinessContext with domain and project info.

        Returns:
            List of structured Requirement objects.
        """
        requirements: list[Requirement] = []

        # Process natural language requirements.
        for i, req_text in enumerate(inputs.natural_language_requirements):
            req = self._parse_requirement(req_text, i, context)
            requirements.append(req)

        # Process stakeholder notes.
        for i, note in enumerate(inputs.stakeholder_notes):
            req = self._parse_requirement(note, len(requirements) + i, context)
            req.source = "stakeholder_note"
            requirements.append(req)

        # Process interview transcripts.
        for i, transcript in enumerate(inputs.interview_transcripts):
            extracted = self._extract_from_transcript(transcript)
            for j, req_text in enumerate(extracted):
                req = self._parse_requirement(req_text, len(requirements) + j, context)
                req.source = f"interview_transcript_{i + 1}"
                requirements.append(req)

        # Apply technical constraints as requirements.
        for i, constraint in enumerate(inputs.technical_constraints):
            req = Requirement(
                title=f"Technical Constraint: {constraint[:50]}",
                description=constraint,
                type=RequirementType.non_functional,
                priority=Priority.must_have,
                clarity_score=0.9,
                source="technical_constraint",
                acceptance_criteria=[f"System must comply with: {constraint}"],
            )
            requirements.append(req)

        return requirements

    def _parse_requirement(self, text: str, index: int, context: BusinessContext) -> Requirement:
        """Parse a single requirement from natural language."""
        text = text.strip()
        req_type = self._classify_type(text)
        priority = self._estimate_priority(text)
        clarity = self._score_clarity(text)
        ambiguity = self._flag_ambiguity(text)
        acceptance = self._generate_acceptance_criteria(text, req_type)

        return Requirement(
            title=text[:100],
            description=text,
            type=req_type,
            priority=priority,
            clarity_score=clarity,
            ambiguity_flags=ambiguity,
            source="natural_language",
            acceptance_criteria=acceptance,
        )

    def _classify_type(self, text: str) -> RequirementType:
        """Classify requirement as functional or non-functional."""
        lowered = text.lower()
        for keyword in _NON_FUNCTIONAL_KEYWORDS:
            if keyword in lowered:
                return RequirementType.non_functional
        for keyword in _FUNCTIONAL_KEYWORDS:
            if keyword in lowered:
                return RequirementType.functional
        return RequirementType.functional

    def _estimate_priority(self, text: str) -> Priority:
        """Estimate requirement priority from text."""
        lowered = text.lower()
        if any(w in lowered for w in ("must", "critical", "essential", "required")):
            return Priority.must_have
        if any(w in lowered for w in ("should", "important")):
            return Priority.should_have
        if any(w in lowered for w in ("could", "nice to have", "optional")):
            return Priority.could_have
        return Priority.should_have

    def _score_clarity(self, text: str) -> float:
        """Score requirement clarity (0-1)."""
        score = 0.7  # baseline
        if len(text) < 20:
            score -= 0.2
        if any(w in text.lower() for w in ("maybe", "possibly", "might", "should be")):
            score -= 0.15
        if any(w in text.lower() for w in ("specifically", "exactly", "must be", "shall be")):
            score += 0.15
        return max(0.0, min(1.0, score))

    def _flag_ambiguity(self, text: str) -> list[str]:
        """Flag ambiguous terms in requirement text."""
        flags: list[str] = []
        ambiguous_terms = {
            "fast": "Define specific performance target",
            "easy": "Define usability criteria",
            "user-friendly": "Define usability criteria",
            "secure": "Define specific security controls",
            "scalable": "Define scale targets (users, data, transactions)",
            "flexible": "Define specific flexibility requirements",
            "robust": "Define specific reliability requirements",
            "quickly": "Define specific time target",
            "sometimes": "Clarify when this applies",
            "probably": "Clarify certainty",
        }
        lowered = text.lower()
        for term, suggestion in ambiguous_terms.items():
            if term in lowered:
                flags.append(f"Ambiguous term '{term}': {suggestion}")
        return flags

    def _generate_acceptance_criteria(self, text: str, req_type: RequirementType) -> list[str]:
        """Generate acceptance criteria from requirement text."""
        criteria: list[str] = []
        if req_type == RequirementType.functional:
            criteria.append(f"Given a user, when they trigger the action, then the system behaves as described: {text[:80]}")
            criteria.append("Given invalid input, when the action is triggered, then the system returns an appropriate error")
        else:
            criteria.append(f"Given load conditions, when the system is tested, then it meets: {text[:80]}")
            criteria.append("Given degraded conditions, when the system is tested, then it degrades gracefully")
        return criteria

    def _extract_from_transcript(self, transcript: str) -> list[str]:
        """Extract individual requirements from interview transcript."""
        sentences = re.split(r'[.!?]+', transcript)
        requirements: list[str] = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and any(w in sentence.lower() for w in _FUNCTIONAL_KEYWORDS | _NON_FUNCTIONAL_KEYWORDS):
                requirements.append(sentence)
        return requirements
