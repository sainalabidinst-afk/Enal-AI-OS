"""
AI Ethics & Governance Engine.
"""

from __future__ import annotations

import logging

from apps.ai_ethics_pack.ai_ethics_engine import AIEthicsGovernanceEngine
from apps.ai_ethics_pack.schemas import (
    AIEthicsGovernanceReport,
    AIEthicsGovernanceRequest,
    AIEthicsInputs,
    AIEthicsOperation,
    BiasFinding,
    ComplianceMapping,
    EthicsAssessment,
    FairnessMetric,
)

logger = logging.getLogger(__name__)


class AIEthicsEngine:
    """
    Orchestrates AI ethics and governance analysis pipeline:
        1. Input Validation
        2. Fairness Audit / Bias Detection / Explainability / Compliance
        3. Ethics Assessment
        4. Compliance Mapping
        5. Recommendation Generation
    """

    def __init__(self) -> None:
        self.engine = AIEthicsGovernanceEngine()

    def analyze(self, request: AIEthicsGovernanceRequest) -> AIEthicsGovernanceReport:
        inputs: AIEthicsInputs = request.inputs
        validation = self.engine.check_input_validation(inputs)

        if not validation["valid"]:
            logger.warning("AI Ethics validation failed: %s", validation["errors"])
            return AIEthicsGovernanceReport(
                request_id=request.request_id,
                fairness_metrics=[],
                bias_findings=[],
                ethics_assessments=[],
                compliance_mappings=[],
                recommendations=validation["errors"],
                quality_score=0.0,
            )

        fairness_metrics: list[FairnessMetric] = []
        bias_findings: list[BiasFinding] = []
        assessments: list[EthicsAssessment] = []
        mappings: list[ComplianceMapping] = []
        recommendations: list[str] = []

        if inputs.operation == AIEthicsOperation.fairness_audit:
            fairness_metrics = self.engine.audit_fairness(inputs)
        elif inputs.operation == AIEthicsOperation.bias_detection:
            bias_findings = self.engine.detect_bias(inputs)
        elif inputs.operation == AIEthicsOperation.explainability:
            assessments = self.engine.assess_explainability(inputs)
        elif inputs.operation == AIEthicsOperation.compliance_check:
            mappings = self.engine.check_compliance(inputs)

        # Always run safety boundary check
        recommendations.extend(self.engine.safety_boundary_check(inputs))

        quality_score = self.engine.compute_quality_score(
            fairness_metrics, bias_findings, assessments, mappings
        )

        return AIEthicsGovernanceReport(
            request_id=request.request_id,
            fairness_metrics=fairness_metrics,
            bias_findings=bias_findings,
            ethics_assessments=assessments,
            compliance_mappings=mappings,
            recommendations=recommendations,
            quality_score=quality_score,
        )
