"""
Compliance Officer — Compliance Assessment module.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.compliance_officer.schemas import (
    AuditEvidence,
    ComplianceConfig,
    ComplianceFramework,
    ControlRequirement,
    RiskItem,
)

logger = logging.getLogger(__name__)


class ComplianceAssessmentEngine:
    """
    Provides compliance assessment, audit planning, risk assessment,
    and remediation planning for regulatory frameworks.
    """

    FRAMEWORK_REQUIREMENTS: dict[ComplianceFramework, list[dict[str, Any]]] = {
        ComplianceFramework.iso27001: [
            {"id": "A.5.1", "name": "Information Security Policy", "domain": "governance"},
            {"id": "A.6.1", "name": "Organization of Information Security", "domain": "governance"},
            {"id": "A.8.1", "name": "Information Classification", "domain": "data"},
            {"id": "A.9.1", "name": "Business Requirement of Access Control", "domain": "access"},
            {"id": "A.10.1", "name": "Cryptographic Controls", "domain": "security"},
            {"id": "A.12.1", "name": "Secure Development Lifecycle", "domain": "development"},
            {"id": "A.13.1", "name": "Network Security Management", "domain": "network"},
            {"id": "A.14.1", "name": "Security Requirements of Information Systems", "domain": "development"},  # noqa: E501
        ],
        ComplianceFramework.nist: [
            {"id": "ID.AM-1", "name": "Resource Inventory", "domain": "assets"},
            {"id": "PR.AC-1", "name": "Identity Management", "domain": "access"},
            {"id": "PR.DS-1", "name": "Data-at-rest", "domain": "data"},
            {"id": "PR.DS-2", "name": "Data-in-transit", "domain": "data"},
            {"id": "DE.CM-1", "name": "Baseline Selection", "domain": "security"},
            {"id": "RS.MI-3", "name": "Incident Response Plan Execution", "domain": "incident"},
        ],
        ComplianceFramework.pci_dss: [
            {"id": "1.1", "name": "Firewall Configuration", "domain": "network"},
            {"id": "2.1", "name": "Default Password Changes", "domain": "access"},
            {"id": "3.1", "name": "Cardholder Data Encryption", "domain": "data"},
            {"id": "4.1", "name": "Secure Network Transmission", "domain": "network"},
            {"id": "6.1", "name": "Secure Development", "domain": "development"},
            {"id": "7.1", "name": "Access Control", "domain": "access"},
        ],
        ComplianceFramework.gdpr: [
            {"id": "Art 5", "name": "Data Processing Principles", "domain": "privacy"},
            {"id": "Art 15", "name": "Right of Access", "domain": "privacy"},
            {"id": "Art 17", "name": "Right to Erasure", "domain": "privacy"},
            {"id": "Art 25", "name": "Data Protection by Design", "domain": "privacy"},
            {"id": "Art 30", "name": "Records of Processing Activities", "domain": "privacy"},
        ],
        ComplianceFramework.soc2: [
            {"id": "CC1.1", "name": "Control Environment", "domain": "governance"},
            {"id": "CC5.1", "name": "System Operations", "domain": "operations"},
            {"id": "CC6.1", "name": "Logical Access", "domain": "access"},
            {"id": "CC6.6", "name": "System Change Management", "domain": "development"},
            {"id": "CC7.1", "name": "Detection of Security Events", "domain": "security"},
        ],
    }

    EVIDENCE_REQUIREMENTS: dict[ComplianceFramework, list[str]] = {
        ComplianceFramework.iso27001: [
            "policy_document",
            "access_log",
            "incident_report",
            "training_record",
        ],
        ComplianceFramework.pci_dss: [
            "penetration_test_report",
            "vulnerability_scan",
            "attestation_of_compliance",
        ],
    }

    def assess_requirements(self, config: ComplianceConfig) -> list[ControlRequirement]:
        """Assess control requirements across frameworks."""
        requirements = []
        for framework in config.frameworks:
            framework_reqs = self.FRAMEWORK_REQUIREMENTS.get(framework, [])
            for req in framework_reqs:
                sev = "high" if req["domain"] in ("access", "data", "security") else "medium"
                evidence = self.EVIDENCE_REQUIREMENTS.get(framework, []) if sev == "high" else []
                requirements.append(ControlRequirement(
                    id=req["id"],
                    name=req["name"],
                    framework=framework,
                    description=f"{req['name']} for {framework.value}",
                    severity=sev,
                    status="pending",
                    evidence_needed=evidence,
                ))
        return requirements

    def collect_evidence(self, requirements: list[ControlRequirement]) -> list[AuditEvidence]:
        """Collect audit evidence for requirements."""
        evidence_items = []
        for req in requirements:
            for evidence_type in req.evidence_needed:
                evidence_items.append(AuditEvidence(
                    control_id=req.id,
                    evidence_type=evidence_type,
                    collected=False,
                    description=f"Evidence needed for {req.name}",
                ))
        return evidence_items

    def assess_risks(self, config: ComplianceConfig) -> list[RiskItem]:
        """Assess compliance risks."""
        risks = [
            RiskItem(
                id="RISK-001",
                description="Data breach due to inadequate encryption",
                likelihood=0.3,
                impact=0.9,
                overall_risk=0.27,
                mitigation="Implement encryption at rest and in transit",
            ),
            RiskItem(
                id="RISK-002",
                description="Unauthorized access to sensitive data",
                likelihood=0.4,
                impact=0.8,
                overall_risk=0.32,
                mitigation="Enforce RBAC and MFA for all accounts",
            ),
            RiskItem(
                id="RISK-003",
                description="Non-compliance audit failure",
                likelihood=0.2,
                impact=0.7,
                overall_risk=0.14,
                mitigation="Regular compliance testing and documentation",
            ),
        ]
        return risks

    def generate_recommendations(self, config: ComplianceConfig) -> list[str]:
        """Generate compliance recommendations."""
        base_recs = [
            "Conduct quarterly compliance assessments",
            "Maintain audit trail for all data processing activities",
            "Implement privacy by design principles",
            "Establish incident response procedures",
        ]
        if ComplianceFramework.gdpr in config.frameworks:
            base_recs.append("Appoint Data Protection Officer (DPO)")
            base_recs.append("Conduct Data Protection Impact Assessments (DPIA)")
        if ComplianceFramework.pci_dss in config.frameworks:
            base_recs.append("Implement tokenization for cardholder data")
            base_recs.append("Conduct quarterly penetration testing")
        return base_recs


__all__ = ["ComplianceAssessmentEngine"]
