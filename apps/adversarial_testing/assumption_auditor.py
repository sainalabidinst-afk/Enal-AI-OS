"""
Assumption Auditor — identifies hidden assumptions in plans and strategies.

Reviews the subject and evidence to surface implicit assumptions that
the analysis or plan depends on, then evaluates which assumptions
are most risky if violated.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


class AssumptionAuditor:
    """
    Audits plans and strategies for hidden assumptions.

    Usage::

        auditor = AssumptionAuditor()
        assumptions = auditor.audit(subject, evidence, context)
    """

    def audit(
        self,
        subject: str,
        evidence: dict[str, Any] | None = None,
        context: str | None = None,
        constraints: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Audit the subject for hidden assumptions.

        Args:
            subject: The plan/strategy/recommendation being audited.
            evidence: Supporting evidence.
            context: Additional context.
            constraints: Hard constraints.

        Returns:
            List of assumption dicts with id, description, risk, and confidence.
        """
        assumptions = self._extract_assumptions(subject, evidence, context, constraints)

        # Score each assumption for risk
        scored = []
        for i, assumption in enumerate(assumptions):
            risk = self._assess_assumption_risk(assumption, constraints or [])
            scored.append({
                "id": f"asm-{i:03d}",
                "description": assumption,
                "risk": risk["risk"],
                "confidence": risk["confidence"],
                "mitigatable": risk["mitigatable"],
            })

        return scored

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _extract_assumptions(
        self,
        subject: str,
        evidence: dict[str, Any] | None,
        context: str | None,
        constraints: list[str] | None,
    ) -> list[str]:
        """Extract assumptions using LLM and heuristics."""
        from backend.app.core.config import settings
        from backend.app.core.model_router import model_router

        ev_str = json.dumps(evidence or {})[:500] if evidence else ""
        constraints_str = ", ".join(constraints or [])

        prompt = (
            f"Identify hidden assumptions in the following plan/strategy:\n\n"
            f"Subject: {subject}\n\n"
            f"Evidence: {ev_str}\n\n"
            f"Context: {context or 'N/A'}\n\n"
            f"Constraints: {constraints_str or 'None'}\n\n"
            "List each assumption as a separate line. Focus on assumptions that,"
            " if violated, would cause the plan to fail. Be creative and aggressive"
            " — think like a Devil's Advocate.\n"
            "Format: one assumption per line, starting with '-'"
        )

        try:
            if os.environ.get("TESTING", "").lower() in ("true", "1", "yes"):
                raise RuntimeError("Skipping LLM calls in test mode")
            from backend.app.core.config import settings
            from backend.app.core.model_router import model_router

            response = model_router.complete(
                [{"role": "user", "content": prompt}],
                model=settings.DEFAULT_REASONING_MODEL,
                temperature=0.7,
                max_tokens=1024,
            )
            lines = response.choices[0].message.content.strip().split("\n")
            assumptions = [line.lstrip("- ").strip() for line in lines if line.strip().startswith("-")]  # noqa: E501

            if assumptions:
                return assumptions[:20]  # Cap at 20
        except Exception as e:
            logger.warning(f"LLM assumption extraction failed: {e}")

        return self._heuristic_assumptions(subject)

    def _heuristic_assumptions(self, subject: str) -> list[str]:
        """Generate common assumptions heuristically."""
        return [
            "All stated inputs are accurate and complete",
            "No external shocks or disruptions occur during execution",
            "Dependencies (teams, services, vendors) behave as expected",
            "Resource allocation remains stable throughout implementation",
            "Market conditions do not change significantly",
            "Regulatory environment remains constant",
            "Stakeholder alignment persists throughout the project",
            "Technical debt does not accumulate beyond acceptable levels",
            "No critical security incidents occur",
            "User adoption follows predicted patterns",
        ]

    def _assess_assumption_risk(
        self, assumption: str, constraints: list[str]
    ) -> dict[str, Any]:
        """Assess the risk level of an assumption."""
        # Check if the assumption is already mitigated by a constraint
        for constraint in constraints:
            constraint_lower = constraint.lower()
            if any(word in constraint_lower for word in assumption.lower().split()[:5]):
                return {"risk": "medium", "confidence": 0.8, "mitigatable": True}

        # Heuristic risk assessment based on assumption keywords
        high_risk_keywords = ["accuracy", "no external", "dependencies behave", "stable",
                              "do not change", "remain constant", "no critical", "do not accumulate"]  # noqa: E501
        medium_risk_keywords = ["alignment", "follow predicted", "complete"]

        assumption_lower = assumption.lower()
        for keyword in high_risk_keywords:
            if keyword in assumption_lower:
                return {"risk": "high", "confidence": 0.9, "mitigatable": True}

        for keyword in medium_risk_keywords:
            if keyword in assumption_lower:
                return {"risk": "medium", "confidence": 0.8, "mitigatable": True}

        return {"risk": "low", "confidence": 0.6, "mitigatable": False}
