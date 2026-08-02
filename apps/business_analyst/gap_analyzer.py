"""
Business Analyst — Gap Analyzer.

Identifies gaps between business needs and technical capabilities.
Produces prioritized gap analysis reports.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.business_analyst.schemas import (
    StakeholderInput,
    GapItem,
    Priority,
    Requirement,
)

logger = logging.getLogger(__name__)


class GapAnalyzer:
    """
    Analyzes gaps between business needs and technical capabilities.

    Usage::

        analyzer = GapAnalyzer()
        gaps = analyzer.analyze(inputs, technical_constraints)
    """

    def analyze(
        self,
        inputs: StakeholderInput,
        technical_constraints: list[str] | None = None,
    ) -> list[GapItem]:
        """
        Perform gap analysis.

        Args:
            inputs: StakeholderInput with requirements and current state.
            technical_constraints: List of technical constraints.

        Returns:
            List of GapItem objects.
        """
        gaps: list[GapItem] = []
        constraints = technical_constraints or []

        # Analyze requirements against constraints.
        for req_text in inputs.natural_language_requirements:
            gaps.extend(self._check_requirement_gaps(req_text, constraints))

        # Analyze stakeholder notes.
        for note in inputs.stakeholder_notes:
            gaps.extend(self._check_note_gaps(note, constraints))

        # Analyze interview transcripts for unaddressed needs.
        for transcript in inputs.interview_transcripts:
            gaps.extend(self._check_transcript_gaps(transcript, constraints))

        return gaps

    def _check_requirement_gaps(
        self, req_text: str, constraints: list[str]
    ) -> list[GapItem]:
        """Check a requirement against technical constraints."""
        gaps: list[GapItem] = []
        lowered = req_text.lower()

        # Check for high-scale requirements without scale tech.
        if any(w in lowered for w in ("scale", "million", "thousand concurrent", "high volume")):
            gaps.append(GapItem(
                business_need="High-scale operation",
                current_capability="Not specified in technical constraints",
                required_capability="Distributed architecture, caching, CDN, load balancing",
                gap_description="Requirement indicates high-scale needs but no scaling technology is mentioned in constraints",
                priority=Priority.must_have,
                estimated_effort="High (3-6 months)",
                impact_if_unaddressed="System failure under load; poor user experience",
            ))

        # Check for real-time requirements without real-time tech.
        if any(w in lowered for w in ("real-time", "live", "instant", "immediate")):
            gaps.append(GapItem(
                business_need="Real-time data processing",
                current_capability="Not specified in technical constraints",
                required_capability="WebSocket, streaming platform (Kafka), event-driven architecture",
                gap_description="Real-time requirement lacks enabling technology in constraints",
                priority=Priority.must_have,
                estimated_effort="Medium (1-3 months)",
                impact_if_unaddressed="Delayed data; stale information for users",
            ))

        # Check for compliance requirements without security tech.
        if any(w in lowered for w in ("compliance", "audit", "regulation", "pci", "gdpr", "hipaa")):
            gaps.append(GapItem(
                business_need="Regulatory compliance",
                current_capability="Not specified in technical constraints",
                required_capability="Audit logging, encryption, access controls, data retention",
                gap_description="Compliance requirement lacks security and audit technology in constraints",
                priority=Priority.must_have,
                estimated_effort="High (2-4 months)",
                impact_if_unaddressed="Regulatory penalties; data breach liability",
            ))

        # Check for mobile requirements without mobile tech.
        if any(w in lowered for w in ("mobile", "ios", "android", "app")):
            gaps.append(GapItem(
                business_need="Mobile application support",
                current_capability="Not specified in technical constraints",
                required_capability="Mobile SDK, responsive API, offline sync",
                gap_description="Mobile requirement lacks mobile-specific technology in constraints",
                priority=Priority.should_have,
                estimated_effort="Medium (2-3 months)",
                impact_if_unaddressed="Poor mobile UX; limited market reach",
            ))

        return gaps

    def _check_note_gaps(self, note: str, constraints: list[str]) -> list[GapItem]:
        """Check stakeholder note for gaps."""
        gaps: list[GapItem] = []
        lowered = note.lower()

        if "integration" in lowered and not any("integration" in c.lower() for c in constraints):
            gaps.append(GapItem(
                business_need="System integration",
                current_capability="No integration technology specified",
                required_capability="API gateway, message broker, event streaming",
                gap_description="Integration need mentioned but no integration tech in constraints",
                priority=Priority.should_have,
                estimated_effort="Medium (1-2 months)",
                impact_if_unaddressed="Data silos; manual workarounds",
            ))

        return gaps

    def _check_transcript_gaps(self, transcript: str, constraints: list[str]) -> list[GapItem]:
        """Check interview transcript for unaddressed needs."""
        gaps: list[GapItem] = []
        lowered = transcript.lower()

        # Check for reporting/analytics needs.
        if any(w in lowered for w in ("report", "dashboard", "analytics", "metrics", "kpi")):
            if not any(w in c.lower() for c in constraints for w in ("report", "dashboard", "analytics")):
                gaps.append(GapItem(
                    business_need="Reporting and analytics",
                    current_capability="No analytics technology specified",
                    required_capability="BI tool, data warehouse, ETL pipeline",
                    gap_description="Analytics need expressed but no analytics tech in constraints",
                    priority=Priority.should_have,
                    estimated_effort="Medium (1-2 months)",
                    impact_if_unaddressed="Data-driven decisions impaired",
                ))

        return gaps
