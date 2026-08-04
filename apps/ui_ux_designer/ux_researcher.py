"""
UI/UX Designer — UX Research Module.

Conducts user experience research:
- Persona analysis
- User journey mapping
- Usability issue detection
- Opportunity identification
- Research confidence scoring
"""

from __future__ import annotations

import logging
from typing import Any

from apps.ui_ux_designer.schemas import (
    Persona,
    UXResearchResult,
    BusinessContext,
    StakeholderInput,
)

logger = logging.getLogger(__name__)


class UXResearcher:
    """
    Conducts UX research analysis from raw user data.

    Generates personas, user journeys, pain points, and opportunities
    from product requirements and user research data.
    """

    def __init__(self) -> None:
        self._research_methods = ["interviews", "surveys", "usability_tests", "analytics"]

    def research(
        self,
        inputs: StakeholderInput,
        personas: list[Persona],
        context: BusinessContext,
    ) -> UXResearchResult:
        """
        Conduct UX research analysis.

        Args:
            inputs: Stakeholder input including user research data
            personas: List of user personas
            context: Business context

        Returns:
            UXResearchResult with findings, pain points, opportunities
        """
        pain_points: list[str] = []
        opportunities: list[str] = []
        usability_issues: list[str] = []
        key_findings: list[str] = []

        research_data = inputs.user_research_data
        if research_data:
            key_findings.append(f"Ditemukan {len(research_data)} catatan riset UX")
            for data in research_data:
                if "kesulitan" in data.lower() or "masalah" in data.lower():
                    pain_points.append(data)
                if "harapan" in data.lower() or "ingin" in data.lower():
                    opportunities.append(data)
                if "tidak intuitif" in data.lower() or "bingung" in data.lower():
                    usability_issues.append(data)

        if not personas:
            personas = [self._default_persona(context)]

        for persona in personas:
            for pain in persona.pain_points:
                if pain not in pain_points:
                    pain_points.append(pain)
            for goal in persona.goals:
                opportunity = f"Memudahkan {persona.name} mencapai: {goal}"
                if opportunity not in opportunities:
                    opportunities.append(opportunity)

        if not key_findings:
            key_findings.append("Riset UX dihasilkan dari persona dan requirements")

        user_journeys = self._build_user_journeys(personas, context)

        research_confidence = self._compute_research_confidence(
            len(research_data),
            len(personas),
            len(key_findings),
        )

        return UXResearchResult(
            user_personas=personas,
            user_journeys=user_journeys,
            key_findings=key_findings,
            pain_points=pain_points,
            opportunities=opportunities,
            usability_issues=usability_issues,
            research_confidence=research_confidence,
        )

    def _default_persona(self, context: BusinessContext) -> Persona:
        """Generate a default persona from context."""
        return Persona(
            name=f"Pengguna {context.domain}",
            role=f"Pengguna utama — {context.project_name}",
            goals=["Menyelesaikan tugas dengan efisien", "Memahami antarmuka tanpa bantuan"],
            pain_points=["Antarmuka tidak intuitif", "Informasi sulit ditemukan"],
            technical_proficiency="medium",
        )

    def _build_user_journeys(
        self,
        personas: list[Persona],
        context: BusinessContext,
    ) -> list[dict[str, Any]]:
        """Build user journey maps for each persona."""
        journeys: list[dict[str, Any]] = []
        stages = ["Awareness", "Consideration", "Adoption", "Usage", "Advocacy"]

        for persona in personas:
            journey = {
                "persona": persona.name,
                "role": persona.role,
                "stages": [],
            }
            for stage in stages:
                journey["stages"].append(
                    {
                        "stage": stage,
                        "actions": [f"Aksi di {stage} untuk {persona.name}"],
                        "touchpoints": [f"Touchpoint {stage}"],
                        "pain_points": [p for p in persona.pain_points[:2]],
                        "opportunities": [f"Optimalkan {stage} untuk {persona.name}"],
                    }
                )
            journeys.append(journey)

        return journeys

    def _compute_research_confidence(
        self,
        data_count: int,
        persona_count: int,
        findings_count: int,
    ) -> float:
        """Compute confidence score for research results."""
        confidence = 0.5
        if data_count > 0:
            confidence += min(0.2, data_count * 0.02)
        if persona_count > 0:
            confidence += min(0.2, persona_count * 0.1)
        if findings_count > 0:
            confidence += min(0.1, findings_count * 0.02)
        return max(0.0, min(1.0, round(confidence, 4)))
