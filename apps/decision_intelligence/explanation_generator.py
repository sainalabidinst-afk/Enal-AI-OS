"""
Explainable Decision — produce a traceable, human-readable chain.

Generates the full explainability chain:
    evidence summary → reasoning steps → simulation/scoring details
    → risk assessment → alternatives → final rationale
"""

from __future__ import annotations

from typing import Any

from apps.decision_intelligence.schemas import (
    Alternative,
    ConfidenceScore,
    Explanation,
)


class ExplanationGenerator:
    """
    Builds human-readable explanations for a decision.

    Usage::

        gen = ExplanationGenerator()
        explanation = gen.generate(request, evidence_set, scored_alts, risk_desc, confidence)
    """

    def generate(
        self,
        decision_id: str,
        context: str,
        evidence_set: Any,
        scored_alternatives: list[dict[str, Any]],
        confidence: ConfidenceScore,
        constraints: list[str],
    ) -> Explanation:
        """
        Generate the full explanation chain.

        Args:
            decision_id: Decision identifier.
            context: Decision context text.
            evidence_set: Processed EvidenceSet.
            scored_alternatives: List sorted by score desc.
            confidence: ConfidenceScore estimate.
            constraints: Hard constraints.

        Returns:
            Explanation with evidence_summary, reasoning_chain,
            simulation_results, risk_assessment, final_rationale.
        """
        # 1. Evidence summary.
        evidence_summary = self._summarize_evidence(evidence_set)

        # 2. Reasoning chain.
        chain: list[str] = []
        chain.append(f"Decision requested: {context}")
        if evidence_set is not None:
            chain.append(
                f"Collected {evidence_set.count} evidence item(s) across sources "
                f"with average quality {evidence_set.avg_quality:.0%}."
            )
        else:
            chain.append("Collected 0 evidence item(s).")
        if evidence_set is not None and evidence_set.count > 0:
            chain.append(
                f"Weighted evidence direction: {evidence_set.dominant_sentiment} "
                f"(positive {evidence_set.positive_weight:.0%}, "
                f"negative {evidence_set.negative_weight:.0%}, "
                f"neutral {evidence_set.neutral_weight:.0%})."
            )
        if constraints:
            chain.append(f"Applied {len(constraints)} hard constraint(s): " + "; ".join(constraints))
        chain.append("Generated and scored alternatives against weighted objectives.")
        chain.append("Risk profiles computed for each alternative (probability × impact).")
        chain.append(f"Selected best alternative with {confidence.score:.0%} confidence.")

        # 3. Simulation results (scoring details).
        def _alt_risk(alt: dict[str, Any]) -> float:
            rp = alt.get("risk_profile")
            return rp.overall_risk if rp is not None else 0.0

        simulation: dict[str, Any] = {
            "top_alternatives": [
                {
                    "description": alt["description"],
                    "score": alt.get("score", 0.0),
                    "risk": _alt_risk(alt),
                }
                for alt in scored_alternatives[:3]
            ],
            "confidence": confidence.score,
            "uncertainty_bound": confidence.uncertainty_bound,
        }

        # 4. Risk assessment.
        if scored_alternatives:
            best = scored_alternatives[0]
            rp = best.get("risk_profile")
            if rp is not None:
                risk_level = (
                    "high" if rp.overall_risk >= 0.5 else
                    ("medium" if rp.overall_risk >= 0.25 else "low")
                )
                risk_assessment = (
                    f"Selected alternative carries {risk_level} risk "
                    f"(overall {rp.overall_risk:.0%}; probability {rp.probability:.0%}, "
                    f"impact {rp.impact:.0%})."
                )
                if rp.risk_factors:
                    risk_assessment += " Key factors: " + "; ".join(rp.risk_factors)
            else:
                risk_assessment = "No risk profile computed."
        else:
            risk_assessment = "No alternatives survived filtering."

        # 5. Final rationale.
        if scored_alternatives:
            best = scored_alternatives[0]
            final_rationale = (
                f"Recommendation: {best['description']} "
                f"(score {best.get('score', 0.0):.0%}). "
                f"Confidence {confidence.score:.0%} with uncertainty "
                f"±{confidence.uncertainty_bound:.0%}. "
                f"{confidence.explanation}"
            )
        else:
            final_rationale = (
                "No feasible alternative found. Consider relaxing constraints "
                "or gathering additional evidence."
            )

        return Explanation(
            evidence_summary=evidence_summary,
            reasoning_chain=chain,
            simulation_results=simulation,
            risk_assessment=risk_assessment,
            final_rationale=final_rationale,
        )

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _summarize_evidence(self, evidence_set: Any) -> str:
        if evidence_set is None or evidence_set.count == 0:
            return "No evidence was supplied."
        summary = (
            f"{evidence_set.count} evidence item(s) from "
            f"{len({i.source_id for i in evidence_set.items})} source(s). "
            f"Average quality {evidence_set.avg_quality:.0%}. "
            f"Directional weight: positive {evidence_set.positive_weight:.0%}, "
            f"negative {evidence_set.negative_weight:.0%}, "
            f"neutral {evidence_set.neutral_weight:.0%}."
        )
        return summary
