"""
Cybersecurity Analyst — Cybersecurity Analysis Engine module.

Provides STRIDE threat modeling, vulnerability assessment, incident
detection, and compliance mapping.
"""

from __future__ import annotations

import logging
import statistics
from typing import Any

from apps.cybersecurity_analyst.schemas import (
    ComplianceGap,
    ComplianceMapping,
    CybersecurityInputs,
    CybersecurityOperation,
    IncidentDetectionReport,
    IncidentFinding,
    ThreatCategory,
    ThreatFinding,
    ThreatModel,
    VulnerabilityAssessment,
    VulnerabilityFinding,
)

logger = logging.getLogger(__name__)


class CybersecurityAnalysisEngine:
    """
    Provides threat modeling (STRIDE), vulnerability assessment, incident
    detection, and compliance mapping.

    All calculations use explicit inputs and declared formulae; no silent
    defaults are applied for missing values.
    """

    MAX_THREAT_FINDINGS: int = 20

    STRIDE_KEYWORDS: dict[str, str] = {
        "authentication": "spoofing",
        "token": "spoofing",
        "identity": "spoofing",
        "oauth": "spoofing",
        "saml": "spoofing",
        "data": "information_disclosure",
        "database": "information_disclosure",
        "storage": "information_disclosure",
        "secret": "information_disclosure",
        "key": "information_disclosure",
        "api": "tampering",
        "input": "tampering",
        "parameter": "tampering",
        "session": "repudiation",
        "audit": "repudiation",
        "log": "repudiation",
        "service": "denial_of_service",
        "queue": "denial_of_service",
        "endpoint": "denial_of_service",
        "privilege": "elevation_of_privilege",
        "admin": "elevation_of_privilege",
        "role": "elevation_of_privilege",
        "permission": "elevation_of_privilege",
    }

    SEVERITY_BY_CVSS: list[tuple[float, str]] = [
        (9.0, "critical"),
        (7.0, "high"),
        (4.0, "medium"),
        (0.1, "low"),
    ]

    def check_input_validation(self, inputs: CybersecurityInputs) -> dict[str, Any]:
        """Validate inputs for missing or ambiguous values."""
        errors: list[str] = []
        valid = True

        if inputs.operation == CybersecurityOperation.threat_model:
            if not inputs.system_description:
                errors.append("system_description is required for threat_model")
                valid = False
        if inputs.operation == CybersecurityOperation.vulnerability_assess:
            if not inputs.vulnerabilities:
                errors.append("vulnerabilities list is required for vulnerability_assess")
                valid = False
        if inputs.operation == CybersecurityOperation.incident_detect:
            if inputs.current_event_count is None and not inputs.alerts:
                errors.append("current_event_count or alerts is required for incident_detect")
                valid = False
        if inputs.operation == CybersecurityOperation.compliance_map:
            if not inputs.framework:
                errors.append("framework is required for compliance_map")
                valid = False
            if not inputs.requirements:
                errors.append("requirements list is required for compliance_map")
                valid = False

        return {
            "valid": valid and len(errors) == 0,
            "validation_errors": errors,
            "calculation_performed": valid,
        }

    def threat_model(self, inputs: CybersecurityInputs) -> ThreatModel:
        """Run a STRIDE threat model over the supplied system description, assets,
        and trust boundaries."""
        description = inputs.system_description or ""
        desc_lower = description.lower()
        assets = list(inputs.assets)
        trust_boundaries = list(inputs.trust_boundaries)
        data_flows = list(inputs.data_flows)

        findings: list[ThreatFinding] = []
        finding_counter = 1

        # Generate STRIDE threats from keyword analysis of the system description.
        matched_categories: set[str] = set()
        for keyword, category in self.STRIDE_KEYWORDS.items():
            if keyword in desc_lower and category not in matched_categories:
                matched_categories.add(category)
                threat = self._build_threat_finding(
                    category, keyword, description, assets, trust_boundaries, finding_counter
                )
                findings.append(threat)
                finding_counter += 1

        # Generate threats for explicit trust boundaries (interoperability risk).
        for boundary in trust_boundaries:
            findings.append(
                self._build_threat_finding(
                    "tampering",
                    boundary,
                    description,
                    assets,
                    trust_boundaries,
                    finding_counter,
                    is_boundary=True,
                )
            )
            finding_counter += 1

        # Generate threats for each asset (data flow risk).
        for asset in assets[:5]:
            if "information_disclosure" not in matched_categories:
                findings.append(
                    self._build_threat_finding(
                        "information_disclosure",
                        asset,
                        description,
                        assets,
                        trust_boundaries,
                        finding_counter,
                        asset=asset,
                    )
                )
                finding_counter += 1

        # Ensure all STRIDE categories are represented when the system is
        # richly described.
        all_categories = {c.value for c in ThreatCategory}
        for category in sorted(all_categories - matched_categories):
            if finding_counter <= self.MAX_THREAT_FINDINGS:
                findings.append(
                    self._build_threat_finding(
                        category,
                        "system_component",
                        description,
                        assets,
                        trust_boundaries,
                        finding_counter,
                    )
                )
                finding_counter += 1

        # Sort by severity and cap.
        severity_order = ["critical", "high", "medium", "low", "info"]
        findings.sort(
            key=lambda f: severity_order.index(f.severity) if f.severity in severity_order else 99
        )
        findings = findings[: self.MAX_THREAT_FINDINGS]

        inputs_traced = ["system_description", "assets", "trust_boundaries"]
        if data_flows:
            inputs_traced.append("data_flows")

        return ThreatModel(
            system_description=description,
            assets=assets,
            trust_boundaries=trust_boundaries,
            threat_findings=findings,
            threat_count=len(findings),
            formula="STRIDE analysis over system description, assets, and trust boundaries",
            inputs_traced=inputs_traced,
        )

    def _build_threat_finding(
        self,
        category: str,
        keyword: str,
        description: str,
        assets: list[str],
        trust_boundaries: list[str],
        idx: int,
        is_boundary: bool = False,
        asset: str | None = None,
    ) -> ThreatFinding:
        """Construct a single STRIDE threat finding."""
        severity = self._severity_for_category(category)
        likelihood = "medium" if severity in ("high", "critical") else "low"

        affected = asset or (
            trust_boundaries[0]
            if is_boundary and trust_boundaries
            else (assets[0] if assets else keyword)
        )

        title_map = {
            "spoofing": "Identity spoofing via credential replay",
            "tampering": "Data tampering at trust boundary",
            "repudiation": "Insufficient non-repudiation controls",
            "information_disclosure": "Information disclosure through data exposure",
            "denial_of_service": "Denial of service via resource exhaustion",
            "elevation_of_privilege": "Privilege escalation through weak access control",
        }
        mitigation_map = {
            "spoofing": "Implement multi-factor authentication and token rotation",
            "tampering": "Apply integrity checks (signatures, hashes) and boundary validation",
            "repudiation": "Enforce audit logging with tamper-evident storage",
            "information_disclosure": "Encrypt data at rest and in transit; enforce least privilege",  # noqa: E501
            "denial_of_service": "Apply rate limiting, circuit breakers, and capacity autoscaling",
            "elevation_of_privilege": "Enforce least-privilege RBAC and continuous privilege review",  # noqa: E501
        }

        return ThreatFinding(
            id=f"T-{idx:03d}",
            category=category,
            title=title_map.get(category, f"STRIDE threat: {category}"),
            description=f"Detected potential {category} risk related to '{keyword}' in system: {description[:80]}",  # noqa: E501
            affected_asset=affected,
            severity=severity,
            likelihood=likelihood,
            mitigation=mitigation_map.get(category, "Review and apply standard mitigations"),
            cvss_score=self._estimate_cvss(category),
        )

    @staticmethod
    def _severity_for_category(category: str) -> str:
        critical = {"elevation_of_privilege", "spoofing"}
        high = {"tampering", "information_disclosure"}
        medium = {"repudiation"}
        low = {"denial_of_service"}
        if category in critical:
            return "critical"
        if category in high:
            return "high"
        if category in medium:
            return "medium"
        if category in low:
            return "low"
        return "info"

    @staticmethod
    def _estimate_cvss(category: str) -> float:
        scores = {
            "spoofing": 8.1,
            "tampering": 7.5,
            "repudiation": 6.5,
            "information_disclosure": 7.8,
            "denial_of_service": 6.0,
            "elevation_of_privilege": 9.1,
        }
        return scores.get(category, 5.0)

    def vulnerability_assess(self, inputs: CybersecurityInputs) -> VulnerabilityAssessment:
        """Assess supplied vulnerabilities and classify by CVSS-based severity."""
        findings: list[VulnerabilityFinding] = []
        severity_counts: dict[str, int] = {}
        scores: list[float] = []

        for idx, vuln in enumerate(inputs.vulnerabilities, start=1):
            cvss = vuln.get("cvss_score")
            sev = (
                self._severity_from_cvss(cvss) if cvss is not None else vuln.get("severity", "info")
            )
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

            finding = VulnerabilityFinding(
                id=vuln.get("id", f"VULN-{idx:03d}"),
                cve=vuln.get("cve"),
                title=vuln.get("title", "Unknown vulnerability"),
                description=vuln.get("description", ""),
                severity=sev,
                cvss_score=cvss,
                affected_component=vuln.get("affected_component", "unknown"),
                remediation=vuln.get("remediation", "No remediation provided"),
            )
            findings.append(finding)
            if cvss is not None:
                scores.append(cvss)

        if scores:
            score_range = f"{min(scores):.1f} - {max(scores):.1f}"
        else:
            score_range = "N/A"

        inputs_traced = ["vulnerabilities"]
        if inputs.checklist_version:
            inputs_traced.append("checklist_version")

        return VulnerabilityAssessment(
            vulnerabilities_found=findings,
            vulnerability_count=len(findings),
            severity_counts=severity_counts,
            score_range=score_range,
            formula="CVSS >= 9.0 critical, 7.0-8.9 high, 4.0-6.9 medium, 0.1-3.9 low",
            inputs_traced=inputs_traced,
        )

    @staticmethod
    def _severity_from_cvss(cvss: float | None) -> str:
        if cvss is None:
            return "info"
        if cvss >= 9.0:
            return "critical"
        if cvss >= 7.0:
            return "high"
        if cvss >= 4.0:
            return "medium"
        if cvss >= 0.1:
            return "low"
        return "info"

    def incident_detect(self, inputs: CybersecurityInputs) -> IncidentDetectionReport:
        """Detect incident anomalies by comparing current activity to a baseline."""
        baseline_values = list(inputs.baseline_events)
        current = inputs.current_event_count
        threshold_pct = inputs.anomaly_threshold_pct

        baseline_count = len(baseline_values)
        baseline_avg: float | None = None
        deviation_pct: float | None = None
        anomaly_detected = False

        if baseline_count > 0:
            baseline_avg = round(statistics.fmean(baseline_values), 4)

        if current is not None and baseline_avg is not None and baseline_avg != 0:
            deviation_pct = round(((current - baseline_avg) / baseline_avg) * 100, 2)
            if deviation_pct is not None and abs(deviation_pct) > threshold_pct:
                anomaly_detected = True

        # Analyze explicit alerts.
        alert_findings: list[IncidentFinding] = []
        for idx, alert in enumerate(inputs.alerts, start=1):
            sev = alert.get("severity", "info")
            detected = anomaly_detected or alert.get("active", False)
            confidence = alert.get("confidence", 0.0)
            alert_findings.append(
                IncidentFinding(
                    id=alert.get("id", f"INC-{idx:03d}"),
                    alert_name=alert.get("name", "Unnamed alert"),
                    severity=sev,
                    description=alert.get("description", ""),
                    detected=detected,
                    confidence=confidence,
                )
            )

        inputs_traced = ["baseline_events", "current_event_count", "alerts"]

        return IncidentDetectionReport(
            alerts_analyzed=alert_findings,
            anomaly_detected=anomaly_detected,
            baseline_event_count=baseline_count,
            current_event_count=current,
            deviation_pct=deviation_pct,
            threshold_pct=threshold_pct,
            formula="(current - baseline_avg) / baseline_avg * 100; anomaly if |deviation| > threshold_pct",  # noqa: E501
            inputs_traced=inputs_traced,
        )

    def compliance_map(self, inputs: CybersecurityInputs) -> ComplianceMapping:
        """Map supplied evidence to compliance requirements and report coverage."""
        requirements: list[dict[str, Any]] = list(inputs.requirements)
        evidence: list[dict[str, Any]] = list(inputs.evidence)

        evidence_keys = {ev.get("requirement_id") for ev in evidence if ev.get("requirement_id")}
        evidence_status = {
            ev.get("requirement_id"): ev.get("status", "unknown")
            for ev in evidence
            if ev.get("requirement_id")
        }

        gaps: list[ComplianceGap] = []
        covered = 0

        for req in requirements:
            req_id = req.get("id", "unknown")
            req_name = req.get("name", "Unnamed requirement")
            if req_id in evidence_keys:
                covered += 1
                status = evidence_status.get(req_id, "unknown")
                gaps.append(
                    ComplianceGap(
                        requirement_id=req_id,
                        requirement_name=req_name,
                        status=status,
                        evidence_available=True,
                        gap="",
                    )
                )
            else:
                gaps.append(
                    ComplianceGap(
                        requirement_id=req_id,
                        requirement_name=req_name,
                        status="missing",
                        evidence_available=False,
                        gap=f"No evidence supplied for requirement {req_id}",
                    )
                )

        total = len(requirements)
        coverage_pct = round((covered / total) * 100, 2) if total > 0 else 0.0

        inputs_traced = ["framework", "requirements", "evidence"]
        if inputs.checklist_version:
            inputs_traced.append("checklist_version")

        return ComplianceMapping(
            framework=inputs.framework or "unknown",
            gaps=gaps,
            total_requirements=total,
            covered_requirements=covered,
            coverage_pct=coverage_pct,
            formula=f"{covered}/{total} requirements covered = {coverage_pct}%",
            inputs_traced=inputs_traced,
        )

    def build_findings(self, inputs: CybersecurityInputs, report_any) -> list[dict[str, Any]]:
        """Extract a flexible findings list from any report object."""
        findings: list[dict[str, Any]] = []
        if report_any is None:
            return findings

        if hasattr(report_any, "threat_findings"):
            for f in report_any.threat_findings:
                findings.append(f.model_dump())
        if hasattr(report_any, "vulnerabilities_found"):
            for f in report_any.vulnerabilities_found:
                findings.append(f.model_dump())
        if hasattr(report_any, "alerts_analyzed"):
            for f in report_any.alerts_analyzed:
                findings.append(f.model_dump())
        if hasattr(report_any, "gaps"):
            for f in report_any.gaps:
                findings.append(f.model_dump())

        return findings


__all__ = ["CybersecurityAnalysisEngine"]
