"""
Synthesis Engine
=================

Synthesizes multi-source findings into coherent narrative.
"""

import logging
from typing import Any

from apps.research_assistant.schemas import (
    Contradiction,
    Evidence,
    Finding,
    Synthesis,
)

logger = logging.getLogger(__name__)


class SynthesisEngine:
    """Synthesizes multi-source findings into coherent narrative."""

    def synthesize(self, query: str, evidence_list: list[Evidence], findings: list[Finding], contradictions: list[Contradiction]) -> Synthesis:
        narrative_parts = [
            f"## Synthesis: {query}",
            "",
            "### Overview",
            f"This synthesis integrates {len(evidence_list)} sources and {len(findings)} findings to address the research query.",
            "",
            "### Key Findings",
        ]

        for finding in findings[:5]:
            narrative_parts.append(f"- **{finding.title}**: {finding.description} (confidence: {finding.confidence:.0%})")

        if contradictions:
            narrative_parts.extend([
                "",
                "### Contradictions and Uncertainties",
                f"{len(contradictions)} contradictions were identified:",
            ])
            for c in contradictions[:3]:
                narrative_parts.append(f"- {c.description}")

        narrative_parts.extend([
            "",
            "### Research Gaps",
            "- Further validation needed for conflicting results",
            "- Additional longitudinal studies recommended",
            "",
            "### Conclusion",
            "The evidence suggests moderate-to-high confidence in the primary findings, with noted uncertainties that warrant further investigation.",
        ])

        narrative = "\n".join(narrative_parts)

        return Synthesis(
            query=query,
            narrative=narrative,
            supporting_evidence=[ev.id for ev in evidence_list[:10]],
            contradicted_evidence=[],
            confidence=0.85,
            gaps_identified=["conflicting_results", "limited_longitudinal_data"],
            future_work=["Longitudinal validation", "Cross-cultural replication"],
        )
