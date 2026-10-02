"""
AI Ethics & Governance Engine.
"""

from __future__ import annotations

import logging

from apps.ai_ethics_pack.assessment_engine import EthicsAssessmentEngine
from apps.ai_ethics_pack.schemas import (
    EthicsConfig,
    EthicsReport,
    EthicsRequest,
)

logger = logging.getLogger(__name__)


class AIEthicsGovernanceEngine:
    """
    Orchestrates the AI ethics and governance pipeline:
        1. Fairness Assessment (bias metric evaluation)
        2. Bias Detection (protected attribute analysis)
        3. Risk Assessment (ethical risk identification)
        4. Recommendation Generation
    """

    def __init__(self) -> None:
        self.engine = EthicsAssessmentEngine()

    def execute(self, request: EthicsRequest) -> EthicsReport:
        config: EthicsConfig = request.inputs

        violations = self.engine.assess_fairness(config, request.business_context)
        findings = self.engine.detect_bias(config, request.business_context)
        risks = self.engine.assess_risks(config, request.business_context)
        recommendations = self.engine.generate_recommendations(config, request.business_context)

        all_findings = len(findings)
        all_violations = len(violations)
        if all_findings + all_violations == 0:
            fairness_score = 1.0
        else:
            weights = {"critical": 0.4, "high": 0.25, "medium": 0.15, "low": 0.05}
            penalty = 0.0
            for f in findings:
                penalty += weights.get(f.severity.value, 0.1) * f.confidence
            for v in violations:
                penalty += 0.1
            fairness_score = max(0.0, round(1.0 - penalty, 2))

        return EthicsReport(
            request_id=request.request_id,
            operation=config.operation,
            frameworks=config.frameworks,
            fairness_violations=violations,
            bias_findings=findings,
            risks=risks,
            recommendations=recommendations,
            fairness_score=fairness_score,
        )


__all__ = ["AIEthicsGovernanceEngine"]
