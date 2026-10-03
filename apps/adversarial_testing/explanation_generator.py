"""
Explanation Generator — builds the Devil's Advocate explanation chain.

Produces a structured explanation of the adversarial testing process,
including assumptions audited, attacks survived/failed, and the
final hardening summary.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.adversarial_testing.schemas import (
    AttackVector,
    GateResult,
    HardeningAction,
    Severity,
    Vulnerability,
)

logger = logging.getLogger(__name__)


class ExplanationGenerator:
    """
    Generates human-readable explanations for adversarial test results.

    Usage::

        generator = ExplanationGenerator()
        explanation = generator.generate(result)
    """

    def generate(
        self,
        subject: str,
        subject_type: str,
        attack_vectors: list[AttackVector],
        vulnerabilities: list[Vulnerability],
        hardening_actions: list[HardeningAction],
        gate_result: dict[str, Any],
        assumptions: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Generate the full explanation chain.

        Args:
            subject: The tested subject.
            subject_type: Type of subject.
            attack_vectors: Generated attack vectors.
            vulnerabilities: Found vulnerabilities.
            hardening_actions: Recommended actions.
            gate_result: Gate evaluation result.
            assumptions: Audited assumptions.

        Returns:
            Explanation dict with reasoning chain and summary.
        """
        # Build reasoning chain
        reasoning_chain = [
            f"Subject: {subject_type} — {subject[:100]}...",
            f"Generated {len(attack_vectors)} attack vectors across "
            f"{len(set(v.category.value for v in attack_vectors))} categories",
            f"Found {len(vulnerabilities)} vulnerabilities",
            f"Generated {len(hardening_actions)} hardening recommendations",
        ]

        # Attacks survived vs failed
        attacked_ids = {v.attack_id for v in vulnerabilities}
        survived = [v for v in attack_vectors if v.id not in attacked_ids]
        failed = [v for v in vulnerabilities]

        # Assumptions audited
        assumption_summary = []
        if assumptions:
            for a in assumptions:
                assumption_summary.append(
                    f"[{a['severity'].upper() if isinstance(a.get('severity'), str) else Severity(a.get('risk', 'low')).value.upper()}] "  # noqa: E501
                    f"{a.get('description', a.get('id', ''))}"
                )

        # Final hardening summary
        gate_summary = (
            f"Gate result: {gate_result.get('gate_result', 'unknown').upper() if isinstance(gate_result.get('gate_result'), str) else gate_result.get('gate_result', 'unknown')}\n"  # noqa: E501
            f"Pass score: {gate_result.get('pass_score', 0.0)}\n"
            f"Confidence: {gate_result.get('confidence', 0.0)}\n"
            f"Vulnerabilities: {gate_result.get('vulnerability_summary', {})}"
        )

        if gate_result.get("gate_result") == GateResult.PASS:
            verdict = "Subject withstood adversarial testing. Ready for review."
        elif gate_result.get("gate_result") == GateResult.FAIL:
            verdict = "Subject FAILED adversarial testing. Critical issues must be resolved."
        else:
            verdict = "Gate requires review. Some hardening actions pending."

        all_attacks_description = []
        for v in attack_vectors:
            all_attacks_description.append(
                {
                    "id": v.id,
                    "category": v.category.value,
                    "description": v.description,
                    "severity": v.severity.value,
                    "survived": v.id not in attacked_ids,
                }
            )

        return {
            "assumptions_audited": assumption_summary,
            "attacks_survived": [
                {"id": a.id, "category": a.category.value, "description": a.description}
                for a in survived[:10]
            ],
            "attacks_failed": [
                {
                    "id": v.attack_id,
                    "vulnerability": v.vulnerability,
                    "severity": v.severity.value,
                    "exploitable": v.exploitable,
                }
                for v in failed[:10]
            ],
            "all_attack_vectors": all_attacks_description,
            "final_hardening_summary": gate_summary,
            "verdict": verdict,
            "reasoning_chain": reasoning_chain,
        }
