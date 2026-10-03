"""
Attack Vector Generator — generates adversarial attack scenarios.

Generates diverse, creative attack scenarios that challenge the
robustness of a plan, recommendation, or strategy. Each attack
represents a worst-case assumption or external shock.
"""

from __future__ import annotations

import logging
import os
import uuid
from typing import Any

from apps.adversarial_testing.schemas import (
    AttackCategory,
    AttackVector,
    Severity,
)

logger = logging.getLogger(__name__)


_ATTACK_TEMPLATES: dict[AttackCategory, list[dict[str, Any]]] = {
    AttackCategory.EXTERNAL_SHOCK: [
        {
            "template": "Market crash: A sudden market downturn eliminates 30% of projected revenue",  # noqa: E501
            "severity": Severity.HIGH,
            "assumptions": [
                "Market moves faster than expected",
                "No early warning indicators",
                "Liquidity dries up",
            ],  # noqa: E501
        },
        {
            "template": "Geopolitical crisis: War, sanctions, or political upheaval disrupts supply chains",  # noqa: E501
            "severity": Severity.CRITICAL,
            "assumptions": ["No fallback suppliers", "No contingency plan", "Regulatory freeze"],
        },
        {
            "template": "Natural disaster: Localized event (fire, flood, earthquake) halts operations",  # noqa: E501
            "severity": Severity.HIGH,
            "assumptions": [
                "Single-region deployment",
                "No disaster recovery",
                "Critical dependency on location",
            ],  # noqa: E501
        },
    ],
    AttackCategory.DEPENDENCY_FAILURE: [
        {
            "template": "Third-party API outage: A critical external service goes down for 24 hours",  # noqa: E501
            "severity": Severity.HIGH,
            "assumptions": ["No circuit breaker", "No caching layer", "Single provider"],
        },
        {
            "template": "Database corruption: Data integrity is compromised, requiring full restore",  # noqa: E501
            "severity": Severity.CRITICAL,
            "assumptions": ["No recent backup", "No data validation", "Single database instance"],
        },
        {
            "template": "Network partition: Services lose connectivity to each other",
            "severity": Severity.HIGH,
            "assumptions": ["No multi-zone deployment", "No retry logic", "Stateful coupling"],
        },
    ],
    AttackCategory.RESOURCE_EXHAUSTION: [
        {
            "template": "Budget overrun: Project costs exceed budget by 200%",
            "severity": Severity.HIGH,
            "assumptions": [
                "No budget monitoring",
                "Fixed-cost commitments",
                "No cost optimization",
            ],  # noqa: E501
        },
        {
            "template": "Team turnover: 80% of key personnel leave mid-project",
            "severity": Severity.HIGH,
            "assumptions": [
                "No documentation",
                "No knowledge transfer",
                "Single-person dependencies",
            ],  # noqa: E501
        },
        {
            "template": "Compute exhaustion: Cloud costs or resource limits are exceeded",
            "severity": Severity.MEDIUM,
            "assumptions": ["No auto-scaling", "No load shedding", "Unbounded resource usage"],
        },
    ],
    AttackCategory.COMPETITIVE_RESPONSE: [
        {
            "template": "Competitor price war: A major competitor launches aggressive discounting",
            "severity": Severity.HIGH,
            "assumptions": ["No pricing flexibility", "No differentiation", "No customer loyalty"],
        },
        {
            "template": "Competitor innovation leap: A competitor releases a superior product",
            "severity": Severity.HIGH,
            "assumptions": ["No R&D buffer", "No fast-follow capability", "Static roadmap"],
        },
        {
            "template": "New entrant disruption: A startup with innovative technology enters the market",  # noqa: E501
            "severity": Severity.MEDIUM,
            "assumptions": [
                "No market monitoring",
                "No response plan",
                "High entry barriers assumed",
            ],  # noqa: E501
        },
    ],
    AttackCategory.REGULATORY_CHANGE: [
        {
            "template": "New compliance requirement: Sudden regulatory change requires architecture redesign",  # noqa: E501
            "severity": Severity.HIGH,
            "assumptions": [
                "No compliance monitoring",
                "Hard-coded compliance",
                "No modular design",
            ],  # noqa: E501
        },
        {
            "template": "Data privacy crackdown: Stricter GDPR/CCPA enforcement blocks current practices",  # noqa: E501
            "severity": Severity.CRITICAL,
            "assumptions": [
                "No data governance",
                "No regional compliance",
                "No consent management",
            ],  # noqa: E501
        },
    ],
    AttackCategory.DATA_CORRUPTION: [
        {
            "template": "Data poisoning: Malicious actor injects corrupt data into the system",
            "severity": Severity.CRITICAL,
            "assumptions": ["No input validation", "No anomaly detection", "Trusted data sources"],
        },
        {
            "template": "Model drift: LLM output quality degrades due to prompt injection or drift",
            "severity": Severity.HIGH,
            "assumptions": [
                "No output validation",
                "No model monitoring",
                "No fallback to deterministic logic",
            ],  # noqa: E501
        },
    ],
    AttackCategory.INFORMATION_WARFARE: [
        {
            "template": "Misinformation campaign: Fake evidence or reports mislead the analysis",
            "severity": Severity.MEDIUM,
            "assumptions": ["No source verification", "No cross-check", "Single-source dependency"],
        },
    ],
    AttackCategory.OPERATIONAL_DISRUPTION: [
        {
            "template": "Security breach: Unauthorized access compromises system integrity",
            "severity": Severity.CRITICAL,
            "assumptions": ["No defense in depth", "No incident response", "No access reviews"],
        },
        {
            "template": "Release rollback failure: Critical bug in production, rollback fails",
            "severity": Severity.CRITICAL,
            "assumptions": ["No canary deployment", "No rollback testing", "Stateful migrations"],
        },
    ],
}


# Severity ranking for sorting
_SEVERITY_RANK = {Severity.LOW: 0, Severity.MEDIUM: 1, Severity.HIGH: 2, Severity.CRITICAL: 3}


class AttackVectorGenerator:
    """
    Generates adversarial attack scenarios for a given subject.

    Usage::

        generator = AttackVectorGenerator()
        vectors = generator.generate(request)
    """

    def __init__(self) -> None:
        self._templates = _ATTACK_TEMPLATES

    def generate(
        self,
        subject: str,
        subject_type: str,
        categories: list[str] | None = None,
        budget: int = 10,
        context: str | None = None,
        constraints: list[str] | None = None,
        existing_hardening: list[str] | None = None,
    ) -> list[AttackVector]:
        """
        Generate attack vectors for the given subject.

        Args:
            subject: The plan/strategy/recommendation to attack.
            subject_type: Type of subject (plan, recommendation, etc.).
            categories: Attack categories to generate (default: all).
            budget: Number of attacks to generate.
            constraints: Hard constraints attacks must not violate.
            existing_hardening: Already-applied mitigations (to avoid reusing).

        Returns:
            List of AttackVector objects.
        """
        existing_hardening = existing_hardening or []
        if categories is None:
            categories = [c.value for c in self._templates.keys()]

        # Try LLM generation first for contextual attacks
        llm_vectors = self._generate_with_llm(
            subject,
            subject_type,
            categories,
            budget,
            context,
            constraints or [],
            existing_hardening,  # noqa: E501
        )

        # Supplement with template-based attacks
        if len(llm_vectors) < budget:
            template_vectors = self._generate_from_templates(
                subject, categories, budget - len(llm_vectors), existing_hardening
            )
            llm_vectors.extend(template_vectors)

        # Sort by severity (highest first) for prioritized testing
        llm_vectors.sort(key=lambda v: _SEVERITY_RANK.get(v.severity, 0), reverse=True)

        return llm_vectors[:budget]

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _generate_with_llm(
        self,
        subject: str,
        subject_type: str,
        categories: list[str],
        budget: int,
        context: str | None,
        constraints: list[str],
        existing_hardening: list[str],
    ) -> list[AttackVector]:
        """Generate attack vectors using LLM for creative, contextual attacks."""
        from backend.app.runtime import model_router, settings

        categories_str = ", ".join(categories) if categories else "all categories"

        hardening_note = ""
        if existing_hardening:
            hardening_note = (
                f"\n\nAlready applied mitigations (do NOT reuse): {', '.join(existing_hardening)}"  # noqa: E501
            )

        constraints_note = ""
        if constraints:
            constraints_note = (
                f"\n\nHard constraints (attacks must NOT violate these): {', '.join(constraints)}"  # noqa: E501
            )

        prompt = (
            f"You are a Devil's Advocate agent. Your job is to find weaknesses in plans and strategies.\n\n"  # noqa: E501
            f"Subject ({subject_type}): {subject}\n\n"
            f"Context: {context or 'No additional context'}\n\n"
            f"Generate {budget} diverse adversarial attack scenarios across categories: {categories_str}.{hardening_note}{constraints_note}\n\n"  # noqa: E501
            "For each attack, provide:\n"
            "- category (from the list above)\n"
            "- description (specific, creative attack scenario)\n"
            "- severity (low/medium/high/critical)\n"
            "- assumptions (worst-case assumptions the attack relies on)\n"
            "- worst_case_impact (what happens if the attack succeeds)\n\n"
            "Output JSON array of objects with these exact fields."
        )

        try:
            if os.environ.get("TESTING", "").lower() in ("true", "1", "yes"):
                raise RuntimeError("Skipping LLM calls in test mode")
            from backend.app.runtime import model_router, settings

            response = model_router.complete(
                [{"role": "user", "content": prompt}],
                model=settings.DEFAULT_REASONING_MODEL,
                temperature=0.8,
                max_tokens=2048,
            )
            import json

            data = json.loads(response.choices[0].message.content)

            vectors: list[AttackVector] = []
            for item in data:
                cat_str = item.get("category", "external_shock")
                try:
                    category = AttackCategory(cat_str)
                except ValueError:
                    category = AttackCategory.EXTERNAL_SHOCK

                try:
                    severity = Severity(item.get("severity", "medium"))
                except ValueError:
                    severity = Severity.MEDIUM

                vectors.append(
                    AttackVector(
                        id=f"atk-{uuid.uuid4().hex[:8]}",
                        category=category,
                        description=item.get("description", ""),
                        severity=severity,
                        assumptions=item.get("assumptions", []),
                        worst_case_impact=item.get("worst_case_impact", ""),
                    )
                )
            return vectors
        except Exception as e:
            logger.warning(f"LLM attack generation failed, falling back to templates: {e}")
            return self._generate_from_templates(subject, categories, budget, existing_hardening)

    def _generate_from_templates(
        self,
        subject: str,
        categories: list[str],
        count: int,
        existing_hardening: list[str],
    ) -> list[AttackVector]:
        """Generate attack vectors from predefined templates."""
        import random as _random

        available: list[tuple[AttackCategory, dict[str, Any]]] = []
        for cat in categories:
            try:
                cat_enum = AttackCategory(cat)
            except ValueError:
                continue
            for template in self._templates.get(cat_enum, []):
                if template["template"] in existing_hardening:
                    continue
                available.append((cat_enum, template))

        if not available:
            return []

        if len(available) > count:
            selected = _random.sample(available, count)
        else:
            selected = available

        vectors: list[AttackVector] = []
        for cat_enum, template in selected:
            try:
                severity = Severity(template["severity"])
            except (ValueError, TypeError):
                severity = Severity.MEDIUM

            vectors.append(
                AttackVector(
                    id=f"atk-{uuid.uuid4().hex[:8]}",
                    category=cat_enum,
                    description=f"{template['template']} (applied to: {subject[:80]})",
                    severity=severity,
                    assumptions=template.get("assumptions", []),
                    worst_case_impact=f"Subject may fail due to {template['template'].lower().split(':')[0]}",  # noqa: E501
                )
            )

        return vectors
