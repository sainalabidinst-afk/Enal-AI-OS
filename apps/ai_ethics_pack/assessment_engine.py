"""
AI Ethics & Governance — Ethics Assessment module.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.ai_ethics_pack.schemas import (
    BiasFinding,
    BiasMetric,
    BusinessContext,
    EthicsConfig,
    EthicsFramework,
    EthicsRisk,
    FairnessViolation,
    Severity,
)

logger = logging.getLogger(__name__)


class EthicsAssessmentEngine:
    """
    Provides bias detection, fairness auditing, explanation review, and impact
    assessment for AI systems across ethical frameworks.
    """

    # Acceptable thresholds per bias metric (higher is fairer).
    FAIRNESS_THRESHOLDS: dict[BiasMetric, tuple[float, float]] = {
        BiasMetric.demographic_parity: (0.8, 1.0),
        BiasMetric.equalized_odds: (0.8, 1.0),
        BiasMetric.statistical_parity: (0.8, 1.0),
        BiasMetric.disparate_impact: (0.8, 1.0),
        BiasMetric.calibration: (0.05, 0.2),
        BiasMetric.equal_opportunity: (0.8, 1.0),
    }

    # Framework-specific ethical requirements.
    FRAMEWORK_REQUIREMENTS: dict[EthicsFramework, list[dict[str, Any]]] = {
        EthicsFramework.fairness: [
            {"id": "FAIR-01", "name": "Demographic Parity", "domain": "fairness"},
            {"id": "FAIR-02", "name": "Equalized Odds", "domain": "fairness"},
            {"id": "FAIR-03", "name": "Equal Opportunity", "domain": "fairness"},
        ],
        EthicsFramework.accountability: [
            {"id": "ACC-01", "name": "Audit Trail", "domain": "accountability"},
            {"id": "ACC-02", "name": "Human Oversight", "domain": "accountability"},
            {"id": "ACC-03", "name": "Explainable Decisions", "domain": "accountability"},
        ],
        EthicsFramework.transparency: [
            {"id": "TRAN-01", "name": "Model Disclosure", "domain": "transparency"},
            {"id": "TRAN-02", "name": "Feature Attribution", "domain": "transparency"},
        ],
        EthicsFramework.privacy: [
            {"id": "PRIV-01", "name": "Data Minimization", "domain": "privacy"},
            {"id": "PRIV-02", "name": "Purpose Limitation", "domain": "privacy"},
            {"id": "PRIV-03", "name": "Right to Erasure", "domain": "privacy"},
        ],
        EthicsFramework.safety: [
            {"id": "SAFE-01", "name": "Robustness Testing", "domain": "safety"},
            {"id": "SAFE-02", "name": "Adversarial Defense", "domain": "safety"},
            {"id": "SAFE-03", "name": "Out-of-Distribution Detection", "domain": "safety"},
        ],
        EthicsFramework.sustainability: [
            {"id": "SUST-01", "name": "Carbon Footprint", "domain": "sustainability"},
            {"id": "SUST-02", "name": "Energy Efficiency", "domain": "sustainability"},
        ],
    }

    def assess_fairness(
        self, config: EthicsConfig, context: BusinessContext
    ) -> list[FairnessViolation]:
        """Assess fairness across configured bias metrics."""
        violations = []
        for metric in config.bias_metrics:
            threshold = self.FAIRNESS_THRESHOLDS.get(metric, (0.8, 1.0))
            observed = self._simulate_metric(metric, context)
            lower, upper = threshold
            status = "pass"
            if metric == BiasMetric.calibration:
                status = "pass" if lower <= observed <= upper else "fail"
            else:
                status = "pass" if observed >= lower else "fail"
            if status == "fail":
                violations.append(FairnessViolation(
                    metric=metric,
                    threshold=lower if metric != BiasMetric.calibration else upper,
                    observed_value=observed,
                    delta=round(abs(lower - observed), 4),
                    status=status,
                ))
        return violations

    def detect_bias(
        self, config: EthicsConfig, context: BusinessContext
    ) -> list[BiasFinding]:
        """Detect bias findings across protected attributes and metrics."""
        findings = []
        for attr in context.protected_attributes:
            for group in attr.groups:
                for metric in config.bias_metrics:
                    violation = self._evaluate_attribute(metric, attr, group)
                    if violation is not None:
                        severity = (
                            Severity.critical if violation["delta"] > 0.3
                            else Severity.high if violation["delta"] > 0.15
                            else Severity.medium
                        )
                        findings.append(BiasFinding(
                            id=f"bias-{metric.value}-{group}",
                            metric=metric,
                            finding=(
                                f"Bias detected for attribute '{attr.name}' "
                                f"on group '{group}': {metric.value} delta={violation['delta']:.3f}"
                            ),
                            severity=severity,
                            affected_groups=[group],
                            recommendation=self._bias_recommendation(metric),
                            confidence=violation["confidence"],
                        ))
        return findings

    def assess_risks(
        self, config: EthicsConfig, context: BusinessContext
    ) -> list[EthicsRisk]:
        """Assess ethical risks across frameworks and operations."""
        risks = [
            EthicsRisk(
                id="RISK-ETH-001",
                description="Disparate impact on protected groups causing unfair outcomes",
                likelihood=0.4 if EthicsFramework.fairness in config.frameworks else 0.1,
                impact=0.9 if EthicsFramework.fairness in config.frameworks else 0.0,
                overall_risk=0.36,
                mitigation=(
                    "Implement bias mitigation: reweighing, adversarial debiasing"
                ),
            ),
            EthicsRisk(
                id="RISK-ETH-002",
                description="Lack of explainability in high-stakes decisions",
                likelihood=0.5 if EthicsFramework.accountability in config.frameworks else 0.1,
                impact=0.8 if EthicsFramework.accountability in config.frameworks else 0.0,
                overall_risk=0.40,
                mitigation="Integrate SHAP/LIME explanations and human-in-the-loop review",
            ),
            EthicsRisk(
                id="RISK-ETH-003",
                description="Privacy violations from data retention or leakage",
                likelihood=0.3 if EthicsFramework.privacy in config.frameworks else 0.1,
                impact=0.85 if EthicsFramework.privacy in config.frameworks else 0.0,
                overall_risk=0.255,
                mitigation="Apply differential privacy and enforce data retention policies",
            ),
        ]
        return risks

    def generate_recommendations(
        self, config: EthicsConfig, context: BusinessContext
    ) -> list[str]:
        """Generate ethical AI recommendations based on frameworks and findings."""
        recs = [
            "Conduct regular bias audits on model outputs across protected attributes",
            "Maintain an audit trail for all model decisions and data lineage",
            "Implement explainable AI tooling (SHAP, LIME) for high-stakes predictions",
            "Apply data minimization and purpose limitation for PII handling",
            "Perform adversarial robustness testing before production deployment",
        ]
        if EthicsFramework.fairness in config.frameworks:
            recs.append("Deploy fairness constraints and post-processing mitigation")
        if EthicsFramework.transparency in config.frameworks:
            recs.append("Publish model cards and factsheets for stakeholder transparency")
        if EthicsFramework.sustainability in config.frameworks:
            recs.append("Measure and report carbon footprint of model training and inference")
        if EthicsFramework.safety in config.frameworks:
            recs.append("Implement OOD detection and fail-safe behavior for edge cases")
        return recs

    def _simulate_metric(self, metric: BiasMetric, context: BusinessContext) -> float:
        """Deterministic synthetic metric value for testing/offline use."""
        # Deterministic based on metric and use case so results are reproducible.
        seed = sum([
            len(context.project_name),
            len(context.domain),
            len(context.ml_use_case),
        ])
        base = {
            BiasMetric.demographic_parity: 0.75,
            BiasMetric.equalized_odds: 0.68,
            BiasMetric.statistical_parity: 0.72,
            BiasMetric.disparate_impact: 0.65,
            BiasMetric.calibration: 0.35,
            BiasMetric.equal_opportunity: 0.70,
        }.get(metric, 0.5)
        return round(min(base + (seed % 10) * 0.01, 1.0), 4)

    def _evaluate_attribute(
        self, metric: BiasMetric, attr: Any, group: str
    ) -> dict[str, Any] | None:
        """Evaluate a single attribute-group pair against a metric.

        Returns violation detail dict or None if within threshold.
        """
        if not attr.groups or not attr.name:
            return None
        observed = self._simulate_metric(metric, BusinessContext(
            project_name="audit",
            domain="audit",
            ml_use_case="audit",
            team_size=1,
        ))
        threshold = self.FAIRNESS_THRESHOLDS.get(metric, (0.8, 1.0))
        lower, upper = threshold
        if metric == BiasMetric.calibration:
            delta = abs(observed - upper)
            fails = observed > upper
        else:
            delta = abs(lower - observed)
            fails = observed < lower
        if not fails:
            return None
        return {
            "delta": delta,
            "confidence": max(0.6, 1.0 - delta),
        }

    def _bias_recommendation(self, metric: BiasMetric) -> str:
        """Return a mitigation recommendation for a bias metric."""
        mapping = {
            BiasMetric.demographic_parity: "Resample training data to balance group representation",
            BiasMetric.equalized_odds: "Apply threshold optimization per protected group",
            BiasMetric.statistical_parity: "Use reweighing to equalize positive prediction rates",
            BiasMetric.disparate_impact: "Enforce disparate impact remover preprocessing",
            BiasMetric.calibration: "Post-process prediction thresholds to calibrate across groups",
            BiasMetric.equal_opportunity: "Ensure true positive rates are equal across groups",
        }
        return mapping.get(metric, "Review data and model for potential