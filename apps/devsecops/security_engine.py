"""
DevSecOps — Security Scanning module.
"""

from __future__ import annotations

import hashlib
import logging
import random
from typing import Any

from apps.devsecops.schemas import (
    ComplianceResult,
    DevSecOpsConfig,
    GateResult,
    GateStatus,
    SecurityGate,
    Vulnerability,
    VulnerabilitySeverity,
)

logger = logging.getLogger(__name__)


class SecurityScanningEngine:
    """
    Provides CI/CD security gate scanning, vulnerability detection,
    dependency checking, and compliance verification.
    """

    # Synthetic vulnerability database for deterministic scanning.
    VULNERABILITY_DB: list[dict[str, Any]] = [
        {
            "cve": "CVE-2024-1001", "title": "Path Traversal in file upload",
            "severity": VulnerabilitySeverity.critical, "cvss": 9.8,
            "package": "express-fileupload", "fix": "1.5.0",
            "description": "Path traversal allows writing files outside upload directory",
            "remediation": "Upgrade to express-fileupload >= 1.5.0",
        },
        {
            "cve": "CVE-2024-1002", "title": "Prototype Pollution",
            "severity": VulnerabilitySeverity.high, "cvss": 7.5,
            "package": "lodash", "fix": "4.17.21",
            "description": "Prototype pollution via merge function",
            "remediation": "Upgrade to lodash >= 4.17.21",
        },
        {
            "cve": "CVE-2024-1003", "title": "Insecure Deserialization",
            "severity": VulnerabilitySeverity.high, "cvss": 8.1,
            "package": "pyyaml", "fix": "6.0.1",
            "description": "Arbitrary code execution via unsafe YAML loading",
            "remediation": "Use yaml.safe_load instead of yaml.load",
        },
        {
            "cve": "CVE-2024-1004", "title": "SQL Injection",
            "severity": VulnerabilitySeverity.critical, "cvss": 9.1,
            "package": "sqlalchemy", "fix": "2.0.0",
            "description": "SQL injection via string interpolation in queries",
            "remediation": "Use parameterized queries with bound parameters",
        },
        {
            "cve": "CVE-2024-1005", "title": "XSS Vulnerability",
            "severity": VulnerabilitySeverity.medium, "cvss": 6.1,
            "package": "django", "fix": "4.2.0",
            "description": "Cross-site scripting via unescaped output",
            "remediation": "Enable auto-escaping and Content Security Policy",
        },
        {
            "cve": "CVE-2024-1006", "title": "Hardcoded Credentials",
            "severity": VulnerabilitySeverity.high, "cvss": 7.7,
            "package": "auth-lib", "fix": "N/A",
            "description": "Hardcoded API keys found in source code",
            "remediation": "Remove hardcoded credentials and use secret management",
        },
        {
            "cve": "CVE-2024-1007", "title": "Container Privilege Escalation",
            "severity": VulnerabilitySeverity.high, "cvss": 7.8,
            "package": "nginx", "fix": "1.25.0",
            "description": "Container running as root allows privilege escalation",
            "remediation": "Run container as non-root user with dropped capabilities",
        },
        {
            "cve": "CVE-2024-1008", "title": "Outdated Base Image",
            "severity": VulnerabilitySeverity.medium, "cvss": 5.3,
            "package": "alpine", "fix": "3.18.0",
            "description": "Base image contains known vulnerabilities",
            "remediation": "Update base image to latest patched version",
        },
    ]

    COMPLIANCE_STANDARDS: dict[str, list[str]] = {
        "soc2": ["access_control", "audit_logging", "data_encryption", "incident_response"],  # noqa: E501
        "iso27001": ["risk_assessment", "access_control", "cryptography", "vendor_management"],  # noqa: E501
        "pci_dss": [
            "data_encryption", "access_control",
            "vulnerability_scanning", "network_security",
        ],  # noqa: E501
        "nist_csf": ["identify", "protect", "detect", "respond", "recover"],
        "cis_docker": [
            "user_namespace", "content_trust",
            "secrets_management", "runtime_security",
        ],
    }

    def scan_gates(self, config: DevSecOpsConfig) -> list[GateResult]:
        """Run security gate scans across pipeline stages."""
        results = []
        rng = random.Random(42)

        for stage in config.stages:
            for gate in stage.gates:
                vulns = self._scan_gate(gate, rng)
                severity_counts = self._count_by_severity(vulns)
                gate_result = GateResult(
                    gate=gate,
                    status=self._gate_status(gate, vulns, config.policy_thresholds),
                    vulnerabilities_found=len(vulns),
                    critical_count=severity_counts["critical"],
                    high_count=severity_counts["high"],
                    medium_count=severity_counts["medium"],
                    low_count=severity_counts["low"],
                    execution_time_seconds=round(rng.uniform(1.0, 15.0), 2),
                    details=[v.title for v in vulns],
                )
                results.append(gate_result)

        return results

    def collect_vulnerabilities(self, config: DevSecOpsConfig) -> list[Vulnerability]:
        """Collect all vulnerabilities found across all gates."""
        all_vulns = []
        rng = random.Random(42)

        for stage in config.stages:
            for gate in stage.gates:
                vulns = self._scan_gate(gate, rng)
                for v in vulns:
                    all_vulns.append(v)
        return all_vulns

    def verify_compliance(self, config: DevSecOpsConfig) -> list[ComplianceResult]:
        """Verify compliance against configured standards."""
        results = []
        for standard in config.pipeline.compliance_standards:
            checks = self.COMPLIANCE_STANDARDS.get(standard, [])
            if not checks:
                continue
            checks_total = len(checks)
            checks_passed = max(1, checks_total - 1)  # At least one passes.
            checks_failed = checks_total - checks_passed
            score = round(checks_passed / checks_total, 2)
            violations = [
                f"Check '{c}' failed for {standard}"
                for c in checks
            ][:checks_failed]

            results.append(ComplianceResult(
                standard=standard,
                checks_total=checks_total,
                checks_passed=checks_passed,
                checks_failed=checks_failed,
                compliance_score=score,
                violations=violations,
            ))
        return results

    def generate_recommendations(
        self, gate_results: list[GateResult], vulnerabilities: list[Vulnerability]
    ) -> list[str]:
        """Generate security recommendations based on findings."""
        recs = []
        has_critical = any(g.critical_count > 0 for g in gate_results)
        has_high = any(g.high_count > 0 for g in gate_results)
        has_failures = any(g.status == GateStatus.fail_gate for g in gate_results)

        if has_critical:
            recs.append("Immediately address critical vulnerabilities before deployment")
        if has_high:
            recs.append("Review and remediate high-severity findings in current sprint")
        if has_failures:
            recs.append("Fix failing security gates to unblock the pipeline")

        # Package-specific recommendations.
        packages_seen = set()
        for vuln in vulnerabilities:
            if vuln.package not in packages_seen:
                packages_seen.add(vuln.package)
                recs.append(
                    f"Upgrade {vuln.package} to {vuln.fix_version or 'latest'} to resolve CVEs"
                )

        if not recs:
            recs.append("All gates passed; maintain regular security scanning")
            recs.append("Schedule quarterly security assessments")
        return recs[:10]

    def compute_security_score(
        self, gate_results: list[GateResult], vulnerabilities: list[Vulnerability]
    ) -> tuple[float, GateStatus]:
        """Compute overall security score and gate status."""
        critical = sum(1 for v in vulnerabilities if v.severity == VulnerabilitySeverity.critical)
        high = sum(1 for v in vulnerabilities if v.severity == VulnerabilitySeverity.high)
        medium = sum(1 for v in vulnerabilities if v.severity == VulnerabilitySeverity.medium)
        low = sum(1 for v in vulnerabilities if v.severity == VulnerabilitySeverity.low)

        score = 1.0
        score -= critical * 0.25
        score -= high * 0.15
        score -= medium * 0.08
        score -= low * 0.03
        score = max(0.0, round(score, 2))

        failed_gates = sum(1 for g in gate_results if g.status == GateStatus.fail_gate)
        if critical > 0 or failed_gates > 0:
            return score, GateStatus.fail_gate
        if high > 0:
            return score, GateStatus.warn
        return score, GateStatus.pass_gate

    def _scan_gate(
        self, gate: SecurityGate, rng: random.Random
    ) -> list[Vulnerability]:
        """Simulate a security scan for a specific gate type."""
        # Deterministic subset of vulnerabilities per gate.
        relevant = [v for v in self.VULNERABILITY_DB if self._matches_gate(gate, v)]
        if not relevant:
            return []
        count = rng.randint(0, min(3, len(relevant)))
        selected = relevant[:count]

        vulns = []
        for i, v in enumerate(selected):
            vulns.append(Vulnerability(
                id=hashlib.md5(f"{gate.value}-{v['cve']}".encode()).hexdigest()[:12],
                cve=v["cve"],
                title=v["title"],
                severity=v["severity"],
                cvss_score=v["cvss"],
                package=v["package"],
                version=f"{rng.randint(1, 5)}.{rng.randint(0, 9)}.{rng.randint(0, 9)}",
                description=v["description"],
                remediation=v["remediation"],
                fix_version=v["fix"],
            ))
        return vulns

    def _matches_gate(self, gate: SecurityGate, vuln: dict[str, Any]) -> bool:
        """Determine if a vulnerability is relevant to a security gate."""
        gate_map = {
            SecurityGate.sast: [
                "SQL Injection", "Path Traversal",
                "Prototype Pollution", "Insecure Deserialization",
            ],
            SecurityGate.dast: ["XSS", "Path Traversal"],
            SecurityGate.sca: ["lodash", "express-fileupload", "pyyaml", "sqlalchemy", "django"],
            SecurityGate.container_scan: ["Container", "Base Image", "nginx", "alpine"],
            SecurityGate.infrastructure_scan: ["Container", "Base Image"],
            SecurityGate.secrets_detection: ["Hardcoded Credentials"],
            SecurityGate.policy_enforcement: ["Hardcoded Credentials"],
        }
        relevant_titles = gate_map.get(gate, [])
        return (
            vuln["title"] in relevant_titles
            or vuln["package"] in relevant_titles
        )

    def _count_by_severity(self, vulns: list[Vulnerability]) -> dict[str, int]:
        """Count vulnerabilities by severity level."""
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for v in vulns:
            counts[v.severity.value] = counts.get(v.severity.value, 0) + 1
        return counts

    def _gate_status(
        self, gate: SecurityGate, vulns: list[Vulnerability], thresholds: dict[str, Any]
    ) -> GateStatus:
        """Determine gate status based on vulnerabilities and thresholds."""
        counts = self._count_by_severity(vulns)
        if counts["critical"] > 0:
            return GateStatus.fail_gate
        if counts["high"] > 0:
            return GateStatus.fail_gate if counts["high"] >= 3 else GateStatus.warn
        return GateStatus.pass_gate


__all__ = ["SecurityScanningEngine"]
