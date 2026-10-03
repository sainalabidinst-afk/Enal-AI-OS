"""
Cybersecurity Analyst Engine.
"""

from __future__ import annotations

import logging

from apps.cybersecurity_analyst.cybersecurity_engine import CybersecurityAnalysisEngine
from apps.cybersecurity_analyst.schemas import (
    BusinessContext,
    ComplianceMapping,
    CybersecurityInputs,
    CybersecurityOperation,
    CybersecurityReport,
    CybersecurityRequest,
    IncidentDetectionReport,
    ThreatModel,
    VulnerabilityAssessment,
)

logger = logging.getLogger(__name__)


class CybersecurityAnalystEngine:
    """
    Orchestrates the cybersecurity analysis pipeline:
        1. Threat Modeling (STRIDE)
        2. Vulnerability Assessment (CVSS-based classification)
        3. Incident Detection (baseline deviation + alert analysis)
        4. Compliance Mapping (requirement-coverage analysis)
    """

    def __init__(self) -> None:
        self.engine = CybersecurityAnalysisEngine()

    def execute(self, request: CybersecurityRequest) -> CybersecurityReport:
        inputs: CybersecurityInputs = request.inputs
        ctx: BusinessContext = request.business_context
        validation = self.engine.check_input_validation(inputs)

        limitations = [
            "Cybersecurity outputs are advisory and do not certify a system secure",
            "Threat models are based on supplied descriptions, not live penetration testing",
            "Incident detection reflects observed signals, not root-cause diagnosis",
            "Compliance mappings require jurisdiction- and date-specific evidence review",
        ]
        recommendations = [
            "Validate threat model assumptions with architecture and security teams",
            "Patch or accept risk on all findings before production deployment",
            "Correlate multiple signal sources before opening a security incident",
            "Maintain evidence provenance and review compliance gaps with domain owners",
        ]
        assumptions = []

        threat_model: ThreatModel | None = None
        vulnerability_assessment: VulnerabilityAssessment | None = None
        incident_report: IncidentDetectionReport | None = None
        compliance: ComplianceMapping | None = None
        findings: list[dict] = []
        source_reference_preserved = inputs.source_id is not None

        if not validation["valid"]:
            limitations.append(f"Input validation failed: {validation['validation_errors']}")
            if inputs.operation == CybersecurityOperation.threat_model:
                if not inputs.system_description:
                    limitations.append("system_description is required for threat modeling")
            if inputs.operation == CybersecurityOperation.vulnerability_assess:
                if not inputs.vulnerabilities:
                    limitations.append(
                        "vulnerabilities list is required for vulnerability assessment"
                    )
            if inputs.operation == CybersecurityOperation.incident_detect:
                if inputs.current_event_count is None and not inputs.alerts:
                    limitations.append(
                        "current_event_count or alerts are required for incident detection"
                    )
            if inputs.operation == CybersecurityOperation.compliance_map:
                if not inputs.framework:
                    limitations.append("framework is required for compliance mapping")
                if not inputs.requirements:
                    limitations.append("requirements list is required for compliance mapping")

        if inputs.operation == CybersecurityOperation.threat_model:
            threat_model = self.engine.threat_model(inputs)
            findings = self.engine.build_findings(inputs, threat_model)
            assumptions.extend(
                [
                    f"STRIDE analysis for {ctx.project_name}",
                    f"trust boundaries: {len(inputs.trust_boundaries)}",
                ]
            )

        if inputs.operation == CybersecurityOperation.vulnerability_assess:
            vulnerability_assessment = self.engine.vulnerability_assess(inputs)
            findings = self.engine.build_findings(inputs, vulnerability_assessment)
            assumptions.append(f"CVSS-based severity for {ctx.project_name}")

        if inputs.operation == CybersecurityOperation.incident_detect:
            incident_report = self.engine.incident_detect(inputs)
            findings = self.engine.build_findings(inputs, incident_report)
            assumptions.append(
                f"baseline of {len(inputs.baseline_events)} events for {ctx.project_name}"
            )

        if inputs.operation == CybersecurityOperation.compliance_map:
            compliance = self.engine.compliance_map(inputs)
            findings = self.engine.build_findings(inputs, compliance)
            assumptions.append(f"framework={inputs.framework} for {ctx.project_name}")

        quality_score = 0.93 if validation["valid"] else 0.80

        return CybersecurityReport(
            request_id=request.request_id,
            operation=inputs.operation,
            threat_model=threat_model,
            vulnerability_assessment=vulnerability_assessment,
            incident_report=incident_report,
            compliance=compliance,
            findings=findings,
            assumptions=assumptions,
            limitations=limitations,
            recommendations=recommendations,
            source_reference_preserved=source_reference_preserved,
            incident_detection_claim=False,
            root_cause_attribution=False,
            compliance_certification_claim=False,
            model_version="2.4.0",
            quality_score=quality_score,
        )


__all__ = ["CybersecurityAnalystEngine"]
