"""
Security Engineer — Domain Engine orchestrator.

Orchestrates the full security pipeline:
    1. OWASP Analysis (SQLi, XSS, command injection, SSRF, CSRF)
    2. Secret Detection (hardcoded credentials, tokens, keys)
    3. Dependency Audit (CVE correlation, license risk)
    4. Threat Modeling (STRIDE analysis)
    5. Vulnerability Scanning (deserialization, XXE, open redirect)
    6. Configuration Hardening (Docker, K8s, Terraform, SSH)
    7. Compliance Mapping (SOC 2, ISO 27001, HIPAA, PCI-DSS, NIST-CSF)

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
import time
from typing import Any

from apps.security_engineer.schemas import (
    SecurityAssessmentRequest,
    SecurityAssessmentReport,
    SecuritySummary,
    SecurityAnalysisRecord,
    AssessmentOutcome,
    Finding,
    Severity,
)
from apps.security_engineer.owasp_analyzer import OWASPAnalyzer
from apps.security_engineer.secret_detector import SecretDetector
from apps.security_engineer.dependency_auditor import DependencyAuditor
from apps.security_engineer.threat_modeler import ThreatModeler
from apps.security_engineer.vulnerability_scanner import VulnerabilityScanner
from apps.security_engineer.hardening_reviewer import HardeningReviewer
from apps.security_engineer.compliance_mapper import ComplianceMapper

logger = logging.getLogger(__name__)


class SecurityEngineerEngine:
    """
    Orchestrates the full security assessment pipeline.

    Public API::

        engine = SecurityEngineerEngine()
        report = engine.review(request)
    """

    def __init__(self) -> None:
        self.owasp = OWASPAnalyzer()
        self.secret_detector = SecretDetector()
        self.dependency_auditor = DependencyAuditor()
        self.threat_modeler = ThreatModeler()
        self.vuln_scanner = VulnerabilityScanner()
        self.hardening = HardeningReviewer()
        self.compliance_mapper = ComplianceMapper()

    def review(self, request: SecurityAssessmentRequest) -> SecurityAssessmentReport:
        """
        Run the full security assessment pipeline.

        Args:
            request: SecurityAssessmentRequest with target, standards, options.

        Returns:
            SecurityAssessmentReport with findings, secrets, deps, threat model, compliance.
        """
        started = time.monotonic()
        target = request.target or {}
        source_code = target.get("source_code", "")
        language = target.get("language", "python")
        file_path = target.get("file_path", "<unknown>")

        all_findings: list[Finding] = []
        all_secrets: list[Any] = []
        dep_findings: list[Any] = []

        # 1. OWASP Analysis (code).
        if request.target_type in ("code", "full_review") and source_code:
            owasp_findings = self.owasp.analyze(source_code, language, file_path)
            all_findings.extend(owasp_findings)

        # 2. Secret Detection.
        if request.check_secrets and source_code:
            secrets = self.secret_detector.scan(source_code, file_path)
            all_secrets.extend(secrets)

        # 3. Dependency Audit.
        if request.check_dependencies:
            manifest_content = target.get("manifest_content", "")
            manifest_type = target.get("manifest_type", "requirements.txt")
            if manifest_content:
                dep_findings = self.dependency_auditor.audit(manifest_content, manifest_type)

        # 4. Threat Modeling.
        threat_model = self.threat_modeler.model(
            architecture_description=target.get("architecture_description", ""),
            source_code=source_code,
            components=target.get("components", []),
            data_flows=target.get("data_flows", []),
        )

        # 5. Vulnerability Scanning (beyond OWASP).
        if source_code:
            vuln_findings = self.vuln_scanner.scan(source_code, language, file_path)
            all_findings.extend(vuln_findings)

        # 6. Configuration Hardening.
        config_content = target.get("config_content", "")
        config_type = target.get("config_type", "auto")
        if config_content:
            harden_findings = self.hardening.review(config_content, config_type)
            all_findings.extend(harden_findings)

        # 7. Compliance Mapping.
        compliance = self.compliance_mapper.map(
            findings=all_findings,
            standards=request.standards,
        )

        # Build summary.
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for f in all_findings:
            severity_counts[f.severity.value] = severity_counts.get(f.severity.value, 0) + 1

        # Secrets contribute to critical findings.
        for s in all_secrets:
            severity_counts[s.severity.value] = severity_counts.get(s.severity.value, 0) + 1

        overall_risk = self._compute_overall_risk(
            len(all_findings), len(all_secrets), len(dep_findings),
            severity_counts, threat_model.risk_rating,
            source_code,
        )
        compliance_score = self._compute_compliance_score(
            severity_counts, compliance, threat_model,
        )

        recommendations = self._generate_recommendations(
            severity_counts, all_findings, all_secrets, dep_findings
        )

        report = SecurityAssessmentReport(
            assessment_id=request.assessment_id,
            target_type=request.target_type.value,
            findings=all_findings,
            secrets=all_secrets,
            dependency_findings=dep_findings,
            threat_model=threat_model,
            summary=SecuritySummary(
                total_findings=len(all_findings),
                critical_count=severity_counts["critical"],
                high_count=severity_counts["high"],
                medium_count=severity_counts["medium"],
                low_count=severity_counts["low"],
                overall_risk=overall_risk,
                compliance_score=compliance_score,
                recommendations_count=len(recommendations),
            ),
            compliance_report=compliance,
            raw={
                "latency_ms": round((time.monotonic() - started) * 1000.0, 2),
                "findings_count": len(all_findings),
                "secrets_count": len(all_secrets),
                "dependency_findings_count": len(dep_findings),
                "threats_count": len(threat_model.threats),
                "overall_risk": overall_risk.value,
                "compliance_score": compliance_score,
            },
        )

        # Record to Experience Memory.
        record = SecurityAnalysisRecord(
            assessment_id=request.assessment_id,
            target_type=request.target_type.value,
            total_findings=len(all_findings),
            critical_count=severity_counts["critical"],
            high_count=severity_counts["high"],
            fp_rate=0.0,
            detection_rate=1.0,
            outcome=AssessmentOutcome.pending,
        )
        self._record(record)

        return report

    def _compute_overall_risk(
        self,
        findings_count: int,
        secrets_count: int,
        dep_count: int,
        severity_counts: dict[str, int],
        threat_rating: Severity,
        source_code: str,
    ) -> Severity:
        """Compute overall risk level."""
        critical = severity_counts.get("critical", 0)
        high = severity_counts.get("high", 0)

        if critical > 0 or secrets_count > 0:
            return Severity.critical
        if high > 0 or severity_counts.get("medium", 0) > 5:
            return Severity.high
        if threat_rating in (Severity.critical, Severity.high):
            return Severity.high if threat_rating == Severity.high else Severity.critical
        if findings_count > 0 or dep_count > 0:
            return Severity.medium
        return Severity.low

    def _compute_compliance_score(
        self,
        severity_counts: dict[str, int],
        compliance: Any,
        threat_model: Any,
    ) -> float:
        """Compute a compliance score from 0-1."""
        penalties = 0.0
        penalties += severity_counts.get("critical", 0) * 0.25
        penalties += severity_counts.get("high", 0) * 0.15
        penalties += severity_counts.get("medium", 0) * 0.08
        penalties += severity_counts.get("low", 0) * 0.03
        penalties += len(threat_model.threats) * 0.02

        # Average compliance percentage across standards.
        comp_pct = compliance.compliance_percentage
        if comp_pct:
            avg_comp = sum(comp_pct.values()) / len(comp_pct)
        else:
            avg_comp = 0.5

        score = max(0.0, min(1.0, avg_comp - penalties))
        return round(score, 4)

    def _generate_recommendations(
        self,
        severity_counts: dict[str, int],
        findings: list[Finding],
        secrets: list[Any],
        dep_findings: list[Any],
    ) -> list[str]:
        """Generate prioritized recommendations."""
        recs: list[str] = []

        if severity_counts.get("critical", 0) > 0:
            recs.append(f"Address {severity_counts['critical']} critical security finding(s) immediately")
        if secrets:
            recs.append(f"Rotate and remove {len(secrets)} hardcoded secret(s) — store in a secrets manager")
        if dep_findings:
            recs.append(f"Upgrade {len(dep_findings)} vulnerable dependency package(s)")
        if severity_counts.get("high", 0) > 0:
            recs.append(f"Remediate {severity_counts['high']} high-severity issue(s)")
        if not recs:
            recs.append("No critical security issues found. Continue regular security assessments.")

        return recs

    def _record(self, record: SecurityAnalysisRecord) -> str:
        """Record to in-memory store (Experience Memory interface)."""
        try:
            import json
            from pathlib import Path
            base = Path("artifacts/security_history")
            base.mkdir(parents=True, exist_ok=True)
            path = base / f"{record.record_id}.json"
            path.write_text(
                json.dumps(record.model_dump(), indent=2, default=str),
                encoding="utf-8",
            )
        except OSError:
            logger.warning("Failed to persist security record %s", record.record_id)
        return record.record_id
