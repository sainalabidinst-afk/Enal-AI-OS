"""
Adversarial Gate — pass/fail gate for adversarial testing.

Determines whether a subject passes adversarial testing based on
vulnerability scores, hardening status, and configured thresholds.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.adversarial_testing.schemas import (
    GateResult,
    HardeningAction,
    Priority,
    Severity,
    Vulnerability,
)

logger = logging.getLogger(__name__)


class AdversarialGate:
    """
    Evaluates whether a subject passes adversarial testing.

    Usage::

        gate = AdversarialGate()
        result = gate.evaluate(vulnerabilities, hardening_actions, budget)
    """

    CRITICAL_THRESHOLD = 0  # Zero critical vulnerabilities allowed
    HIGH_THRESHOLD_RATIO = 0.3  # No more than 30% high-severity issues
    MIN_PASS_SCORE = 0.7
    MIN_HARDENING_COMPLETION = 0.8  # 80% of high/critical actions must be addressed

    def evaluate(
        self,
        vulnerabilities: list[Vulnerability],
        hardening_actions: list[HardeningAction],
        attack_budget: int,
        existing_hardening: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Evaluate whether the subject passes the adversarial gate.

        Args:
            vulnerabilities: Discovered vulnerabilities.
            hardening_actions: Recommended hardening actions.
            attack_budget: Total number of attacks attempted.
            existing_hardening: Already-applied mitigations.

        Returns:
            Dict with gate_result, pass_score, confidence, and explanations.
        """
        existing = existing_hardening or []

        critical_count = sum(1 for v in vulnerabilities if v.severity == Severity.CRITICAL)
        high_count = sum(1 for v in vulnerabilities if v.severity == Severity.HIGH)
        medium_count = sum(1 for v in vulnerabilities if v.severity == Severity.MEDIUM)
        low_count = sum(1 for v in vulnerabilities if v.severity == Severity.LOW)

        score = 1.0
        score -= critical_count * 0.35
        score -= high_count * 0.15
        score -= medium_count * 0.05
        score -= low_count * 0.01

        if existing:
            score = min(1.0, score + 0.05 * len(existing))

        score = max(0.0, min(1.0, round(score, 4)))
        confidence = round(min(1.0, attack_budget / 10.0), 4)

        high_critical_actions = [
            a for a in hardening_actions if a.priority in (Priority.CRITICAL, Priority.HIGH)
        ]
        applied_count = sum(
            1
            for action in high_critical_actions
            if any(
                existing.lower() in action.recommendation.lower()
                or action.recommendation.lower() in existing.lower()
                for existing in existing
            )
        )

        hardening_completion = (
            applied_count / len(high_critical_actions) if high_critical_actions else 1.0
        )

        gate_result, reason = self._determine_gate(
            score, critical_count, high_count, high_critical_actions, hardening_completion, existing
        )

        return {
            "gate_result": gate_result,
            "pass_score": round(score, 4),
            "confidence": confidence,
            "vulnerability_summary": {
                "total": len(vulnerabilities),
                "critical": critical_count,
                "high": high_count,
                "medium": medium_count,
                "low": low_count,
            },
            "hardening_required": len(high_critical_actions),
            "hardening_applied": applied_count,
            "hardening_completion": round(hardening_completion, 4),
            "reason": reason,
            "recommendations_count": len(hardening_actions),
        }

    def _determine_gate(
        self,
        score: float,
        critical_count: int,
        high_count: int,
        high_critical_actions: list[HardeningAction],
        hardening_completion: float,
        existing: list[str],
    ) -> tuple[GateResult, str]:
        """Determine the gate result and reason."""

        if critical_count > self.CRITICAL_THRESHOLD:
            return (
                GateResult.FAIL,
                f"{critical_count} critical vulnerability(s) found. "
                f"Must be resolved before proceeding.",
            )

        if score < self.MIN_PASS_SCORE:
            return (
                GateResult.FAIL,
                f"Pass score {score:.2f} below threshold {self.MIN_PASS_SCORE}. "
                f"{len(high_critical_actions)} high/critical actions require attention.",
            )

        if high_critical_actions and hardening_completion < self.MIN_HARDENING_COMPLETION:
            remaining = len(high_critical_actions) - int(
                hardening_completion * len(high_critical_actions)
            )  # noqa: E501
            return (
                GateResult.REVIEW_REQUIRED,
                f"{remaining} high/critical hardening action(s) not yet applied. "
                f"Recommended to apply before proceeding.",
            )

        return (
            GateResult.PASS,
            f"Subject passed adversarial testing. Score: {score:.2f}, "
            f"confidence: {len(existing)} hardening measure(s) applied.",
        )
