"""
Hardening Advisor — recommends mitigations for discovered vulnerabilities.

Generates prioritized hardening recommendations that address
specific vulnerabilities, considering effort and impact.
"""

from __future__ import annotations

import logging

from apps.adversarial_testing.schemas import (
    AttackVector,
    HardeningAction,
    Priority,
    Severity,
    Vulnerability,
)

logger = logging.getLogger(__name__)


# Mitigation templates per attack category
_MITIGATION_TEMPLATES: dict[Severity, list[str]] = {
    Severity.CRITICAL: [
        "Implement multi-region redundancy with automatic failover",
        "Establish incident response plan with 24/7 escalation",
        "Deploy defense-in-depth with layered security controls",
        "Create backup and restore procedures with regular testing",
        "Implement circuit breakers and graceful degradation",
    ],
    Severity.HIGH: [
        "Add monitoring and alerting for early detection",
        "Implement rate limiting and request throttling",
        "Establish secondary suppliers or alternatives",
        "Add retry logic with exponential backoff",
        "Create runbooks for common failure scenarios",
    ],
    Severity.MEDIUM: [
        "Document assumptions and validate with stakeholders",
        "Add health checks and dependency status monitoring",
        "Implement cost budget alerts and caps",
        "Create simple fallback for non-critical features",
    ],
    Severity.LOW: [
        "Document as known limitation",
        "Add to periodic review checklist",
    ],
}

# Effort estimation
_EFFORT_BY_SEVERITY = {
    Severity.CRITICAL: "high",
    Severity.HIGH: "medium",
    Severity.MEDIUM: "medium",
    Severity.LOW: "low",
}


class HardeningAdvisor:
    """
    Generates hardening recommendations for vulnerabilities.

    Usage::

        advisor = HardeningAdvisor()
        actions = advisor.recommend(vulnerabilities, attack_vectors, constraints)
    """

    def recommend(
        self,
        vulnerabilities: list[Vulnerability],
        attack_vectors: list[AttackVector],
        constraints: list[str] | None = None,
        existing_hardening: list[str] | None = None,
    ) -> list[HardeningAction]:
        """
        Generate hardening recommendations for all vulnerabilities.

        Args:
            vulnerabilities: Discovered vulnerabilities.
            attack_vectors: The attack vectors that found them.
            constraints: Hard constraints (mitigations must not violate).
            existing_hardening: Already-applied mitigations.

        Returns:
            List of prioritized HardeningAction objects.
        """
        existing = existing_hardening or []
        constraints = constraints or []

        # Build a lookup from attack_id to vector
        vector_lookup = {v.id: v for v in attack_vectors}

        actions: list[HardeningAction] = []

        for vuln in vulnerabilities:
            vector = vector_lookup.get(vuln.attack_id)
            if vector is None:
                continue

            # Skip if this attack's template is already in existing hardening
            if vector.description in existing:
                continue

            # Generate mitigation
            mitigation = self._select_mitigation(vuln.severity, constraints)
            if not mitigation:
                continue

            priority = self._severity_to_priority(vuln.severity)

            actions.append(
                HardeningAction(
                    id=f"harden-{vuln.id}",
                    attack_id=vuln.attack_id,
                    recommendation=mitigation,
                    priority=priority,
                    estimated_effort=_EFFORT_BY_SEVERITY.get(vuln.severity, "medium"),
                    applies_to_constraint=self._find_constraint(mitigation, constraints),
                )
            )

        # Sort by priority (highest first)
        priority_rank = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        actions.sort(key=lambda a: priority_rank.get(a.priority.value, 0), reverse=True)

        return actions

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _select_mitigation(self, severity: Severity, constraints: list[str]) -> str | None:
        """Select an appropriate mitigation template for the severity."""
        templates = _MITIGATION_TEMPLATES.get(severity, [])
        if not templates:
            return "Add monitoring and alerting for early detection"

        # Filter out mitigations that might violate constraints
        for template in templates:
            violates = False
            for constraint in constraints:
                # Simple check: if constraint mentions a mitigation keyword
                if any(word in template.lower() for word in constraint.lower().split()):
                    if "no" in constraint.lower() or "disable" in constraint.lower():
                        violates = True
                        break
            if not violates:
                return template

        return templates[0]  # Return first if all filtered

    def _severity_to_priority(self, severity: Severity) -> Priority:
        """Map severity to priority."""
        mapping = {
            Severity.CRITICAL: Priority.CRITICAL,
            Severity.HIGH: Priority.HIGH,
            Severity.MEDIUM: Priority.MEDIUM,
            Severity.LOW: Priority.LOW,
        }
        return mapping.get(severity, Priority.MEDIUM)

    def _find_constraint(self, mitigation: str, constraints: list[str]) -> str | None:
        """Find a constraint that the mitigation applies to."""
        mitigation_lower = mitigation.lower()
        for constraint in constraints:
            constraint_keywords = set(constraint.lower().split())
            mitigation_keywords = set(mitigation_lower.split())
            if constraint_keywords & mitigation_keywords:
                return constraint
        return None
