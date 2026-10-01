"""
Adversarial Testing Engine — domain engine orchestrator.

Orchestrates the full adversarial testing pipeline:
    1. Attack Vector Generator (generate diverse attack scenarios)
    2. Assumption Auditor (identify hidden assumptions)
    3. Vulnerability Scanner (score vulnerabilities)
    4. Hardening Advisor (recommend mitigations)
    5. Adversarial Gate (pass/fail decision)
    6. Explanation Generator (full reasoning chain)

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
import time
from typing import Any

from apps.adversarial_testing.adversarial_gate import AdversarialGate
from apps.adversarial_testing.assumption_auditor import AssumptionAuditor
from apps.adversarial_testing.attack_vector_generator import AttackVectorGenerator
from apps.adversarial_testing.explanation_generator import ExplanationGenerator
from apps.adversarial_testing.hardening_advisor import HardeningAdvisor
from apps.adversarial_testing.schemas import (
    AdversarialTestResult,
    GateResult,
    SubjectType,
)
from apps.adversarial_testing.vulnerability_scanner import VulnerabilityScanner

logger = logging.getLogger(__name__)


class AdversarialTestingEngine:
    """
    Orchestrates the full adversarial testing pipeline.

    Public API::

        engine = AdversarialTestingEngine()
        request = AdversarialTestRequest(subject="...", subject_type="plan", ...)
        result = engine.test(subject, subject_type, ...)
    """

    def __init__(self) -> None:
        self.generator = AttackVectorGenerator()
        self.auditor = AssumptionAuditor()
        self.scanner = VulnerabilityScanner()
        self.advisor = HardeningAdvisor()
        self.gate = AdversarialGate()
        self.explainer = ExplanationGenerator()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def test(
        self,
        subject: str,
        subject_type: str = "plan",
        context: str | None = None,
        evidence: dict[str, Any] | None = None,
        constraints: list[str] | None = None,
        attack_categories: list[str] | None = None,
        attack_budget: int = 10,
        existing_hardening: list[str] | None = None,
    ) -> AdversarialTestResult:
        """
        Run the full adversarial testing pipeline.

        Args:
            subject: The plan/strategy/recommendation to attack.
            subject_type: Type of subject (plan, recommendation, etc.).
            context: Additional context.
            evidence: Supporting evidence.
            constraints: Hard constraints.
            attack_categories: Categories of attacks to generate.
            attack_budget: Number of attacks to generate.
            existing_hardening: Already-applied mitigations.

        Returns:
            AdversarialTestResult with attacks, vulnerabilities, and gate result.
        """
        started = time.monotonic()
        existing = existing_hardening or []

        # Step 1: Generate attack vectors
        vectors = self.generator.generate(
            subject=subject,
            subject_type=subject_type,
            categories=attack_categories or [c.value for c in self.generator._templates.keys()],
            budget=attack_budget,
            context=context,
            constraints=constraints or [],
            existing_hardening=existing,
        )
        logger.info(f"Generated {len(vectors)} attack vectors")

        # Step 2: Audit assumptions
        assumptions = self.auditor.audit(subject, evidence, context, constraints or [])

        # Step 3: Scan for vulnerabilities
        vulnerabilities = self.scanner.scan(subject, vectors, evidence, constraints or [])
        logger.info(f"Found {len(vulnerabilities)} vulnerabilities")

        # Step 4: Generate hardening recommendations
        hardening_actions = self.advisor.recommend(
            vulnerabilities, vectors, constraints or [], existing
        )

        # Step 5: Evaluate gate
        gate_result = self.gate.evaluate(
            vulnerabilities, hardening_actions, attack_budget, existing
        )

        # Step 6: Generate explanation
        explanation = self.explainer.generate(
            subject, subject_type, vectors, vulnerabilities,
            hardening_actions, gate_result, assumptions,
        )

        # Build result
        result = AdversarialTestResult(
            request_id="",
            subject=subject,
            subject_type=SubjectType(subject_type) if isinstance(subject_type, str) else subject_type,  # noqa: E501
            attack_vectors=[
                {
                    "id": v.id,
                    "category": v.category.value,
                    "description": v.description,
                    "severity": v.severity.value,
                    "assumptions": v.assumptions,
                    "worst_case_impact": v.worst_case_impact,
                }
                for v in vectors
            ],
            vulnerabilities_found=[
                {
                    "id": v.id,
                    "attack_id": v.attack_id,
                    "vulnerability": v.vulnerability,
                    "impact": v.impact,
                    "severity": v.severity.value,
                    "exploit_path": v.exploit_path,
                    "exploitable": v.exploitable,
                    "confidence": v.confidence,
                }
                for v in vulnerabilities
            ],
            hardening_recommendations=[
                {
                    "id": a.id,
                    "attack_id": a.attack_id,
                    "recommendation": a.recommendation,
                    "priority": a.priority.value,
                    "estimated_effort": a.estimated_effort,
                }
                for a in hardening_actions
            ],
            gate_result=GateResult(gate_result["gate_result"]),
            pass_score=gate_result["pass_score"],
            confidence=gate_result["confidence"],
            explanation_chain=explanation,
            raw={
                "latency_ms": round((time.monotonic() - started) * 1000, 2),
                "attack_count": len(vectors),
                "vulnerability_count": len(vulnerabilities),
                "hardening_count": len(hardening_actions),
                "assumptions_audited": len(assumptions),
                "vulnerability_summary": gate_result["vulnerability_summary"],
                "hardening_required": gate_result["hardening_required"],
                "hardening_applied": gate_result["hardening_applied"],
                "hardening_completion": gate_result["hardening_completion"],
            },
        )

        return result
