"""
Security Engineer — Compliance Mapper.

Maps security findings to compliance frameworks (SOC 2, ISO 27001,
HIPAA, PCI-DSS, NIST-CSF) and identifies compliance gaps.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.security_engineer.schemas import (
    ComplianceStandard,
    ComplianceReport,
    Finding,
)

logger = logging.getLogger(__name__)


# Mapping from OWASP/Security categories to compliance controls.
_COMPLIANCE_MAPPINGS: dict[str, dict[str, list[str]]] = {
    "SOC2": {
        "A01:2021-Broken Access Control": ["CC5.2", "CC6.1", "CC6.2", "CC6.3", "CC6.6", "CC7.1"],
        "A02:2021-Cryptographic Failures": ["CC5.3", "CC6.1", "CC6.8", "CC7.2"],
        "A03:2021-Injection": ["CC6.3", "CC7.3", "CC8.1"],
        "A04:2021-Insecure Design": ["CC1.3", "CC2.1", "CC3.2"],
        "A05:2021-Security Misconfiguration": ["CC7.1", "CC7.2", "CC7.3", "CC1.4"],
        "A06:2021-Vulnerable Components": ["CC7.1", "CC7.2", "CC8.1"],
        "A07:2021-Auth Failures": ["CC6.1", "CC6.2", "CC6.3", "CC6.6", "CC7.2", "CC8.1"],
        "A08:2021-Data Integrity Failures": ["CC5.3", "CC6.7", "CC7.1"],
        "A09:2021-Logging Failures": ["CC7.2", "CC8.1"],
        "A10:2021-SSRF": ["CC6.1", "CC7.3", "CC8.1"],
        "configuration_hardening": ["CC7.1", "CC1.4"],
        "vulnerability_detection": ["CC7.2", "CC7.3"],
        "secret_exposure": ["CC6.2", "CC7.2"],
        "dependency_vulnerability": ["CC7.2", "CC8.1"],
    },
    "ISO27001": {
        "A01:2021-Broken Access Control": ["A.9.2.3", "A.9.4.2", "A.9.4.3", "A.9.4.4"],
        "A02:2021-Cryptographic Failures": ["A.10.1.1", "A.10.1.2", "A.10.1.3"],
        "A03:2021-Injection": ["A.14.2.5", "A.14.2.6"],
        "A04:2021-Insecure Design": ["A.14.2.1", "A.14.2.2"],
        "A05:2021-Security Misconfiguration": ["A.12.1.1", "A.12.1.2", "A.12.1.3", "A.12.1.4"],
        "A06:2021-Vulnerable Components": ["A.12.6.1", "A.18.1.4"],
        "A07:2021-Auth Failures": ["A.9.2.1", "A.9.2.3", "A.9.2.4", "A.9.2.6"],
        "A08:2021-Data Integrity Failures": ["A.10.1.1", "A.13.1.3", "A.14.2.5"],
        "A09:2021-Logging Failures": ["A.12.4.1", "A.12.4.3"],
        "A10:2021-SSRF": ["A.13.1.3", "A.14.1.2", "A.14.2.5"],
        "configuration_hardening": ["A.12.1.1", "A.12.1.2"],
        "vulnerability_detection": ["A.12.6.1", "A.18.1.4"],
        "secret_exposure": ["A.9.2.1", "A.9.2.6"],
        "dependency_vulnerability": ["A.12.6.1", "A.18.1.4"],
    },
    "HIPAA": {
        "A01:2021-Broken Access Control": ["164.308(a)(4)", "164.308(a)(5)(ii)(B)"],
        "A02:2021-Cryptographic Failures": ["164.312(a)(2)(iv)", "164.312(e)(2)(i)"],
        "A03:2021-Injection": ["164.308(a)(8)", "164.312(c)(1)"],
        "A05:2021-Security Misconfiguration": ["164.308(a)(1)", "164.308(a)(2)"],
        "A07:2021-Auth Failures": ["164.308(a)(5)", "164.312(d)"],
        "A09:2021-Logging Failures": ["164.308(a)(1)(ii)(D)", "164.312(b)"],
        "secret_exposure": ["164.312(d)", "164.312(a)(2)(iv)"],
    },
    "PCI_DSS": {
        "A01:2021-Broken Access Control": ["3.1", "7.1", "8.7"],
        "A02:2021-Cryptographic Failures": ["3.4", "3.5", "4.1"],
        "A03:2021-Injection": ["6.5.1", "8.7"],
        "A05:2021-Security Misconfiguration": ["2.2", "2.6"],
        "A06:2021-Vulnerable Components": ["6.2", "6.5.5"],
        "A07:2021-Auth Failures": ["8.1", "8.2", "8.3"],
        "A09:2021-Logging Failures": ["10.1", "10.2", "10.3"],
        "secret_exposure": ["3.1", "3.5", "8.2"],
    },
    "NIST_CSF": {
        "A01:2021-Broken Access Control": ["PR.AC", "PR.AC-1", "PR.AC-6"],
        "A02:2021-Cryptographic Failures": ["PR.DS", "PR.DS-1", "PR.DS-2"],
        "A03:2021-Injection": ["PR.IP", "PR.IP-6", "PR.DS-5"],
        "A04:2021-Insecure Design": ["PR.IP", "PR.IP-1", "PR.DS-1"],
        "A05:2021-Security Misconfiguration": ["PR.IP", "PR.IP-7"],
        "A06:2021-Vulnerable Components": ["ID.RA", "ID.RA-1"],
        "A07:2021-Auth Failures": ["PR.AC", "PR.AC-1", "PR.AC-4"],
        "A08:2021-Data Integrity Failures": ["PR.DS", "PR.DS-3", "PR.DS-7"],
        "A09:2021-Logging Failures": ["DE.CM", "DE.CM-1"],
        "A10:2021-SSRF": ["PR.DS", "PR.DS-5"],
        "configuration_hardening": ["PR.IP-1", "PR.IP-7"],
        "vulnerability_detection": ["ID.RA-1", "PR.IP-12"],
        "secret_exposure": ["PR.AC-1", "PR.DS-1"],
        "dependency_vulnerability": ["ID.RA-1", "PR.IP-12"],
    },
}


class ComplianceMapper:
    """
    Maps security findings to compliance framework controls.

    Usage::

        mapper = ComplianceMapper()
        report = mapper.map(findings, standards=["SOC2", "ISO27001"])
    """

    def map(
        self,
        findings: list[Finding],
        standards: list[str] | None = None,
    ) -> ComplianceReport:
        """
        Map findings to compliance standards.

        Args:
            findings: List of security findings.
            standards: List of standards to map to (SOC2, ISO27001, HIPAA, PCI_DSS, NIST_CSF).

        Returns:
            ComplianceReport with mapped findings, compliance percentages, and gaps.
        """
        if not standards:
            standards = ["SOC2", "ISO27001", "NIST_CSF"]

        mapped_findings = 0
        compliance_per_standard: dict[str, float] = {}
        all_controls: dict[str, set[str]] = {}
        all_mapped_controls: dict[str, set[str]] = {}

        for std_name in standards:
            std_key = self._normalize_standard(std_name)
            std_mappings = _COMPLIANCE_MAPPINGS.get(std_key, {})
            mapped_controls: set[str] = set()
            total_relevant = 0

            all_controls[std_key] = set()
            for finding in findings:
                category = finding.category or ""
                controls = std_mappings.get(category, [])
                if controls:
                    total_relevant += len(controls)
                    mapped_findings += 1
                    for c in controls:
                        mapped_controls.add(c)

            # Check if finding has explicit compliance_mapping
            for finding in findings:
                for c in (finding.compliance_mapping or []):
                    if self._normalize_standard(c) == std_key:
                        mapped_findings += 1
                    mapped_controls.add(c)

            all_mapped_controls[std_key] = mapped_controls

            # Compliance percentage = mapped controls / expected controls.
            expected_count = total_relevant if total_relevant > 0 else len(std_mappings)
            if expected_count > 0:
                compliance_per_standard[std_key] = round(
                    min(1.0, len(mapped_controls) / max(expected_count, len(mapped_controls))),
                    4,
                )
            else:
                compliance_per_standard[std_key] = 1.0 if not findings else 0.0

        # Identify gaps.
        gaps = self._identify_gaps(standards, all_mappings=True)

        return ComplianceReport(
            standards=standards,
            mapped_findings=mapped_findings,
            compliance_percentage=compliance_per_standard,
            gaps=gaps,
        )

    def _identify_gaps(self, standards: list[str], all_mappings: bool = True) -> list[str]:
        """Identify compliance gaps."""
        gaps: list[str] = []
        for std in standards:
            std_key = self._normalize_standard(std)
            if std_key not in _COMPLIANCE_MAPPINGS:
                gaps.append(f"Standard '{std}' not in compliance mapping database")
            elif not _COMPLIANCE_MAPPINGS[std_key]:
                gaps.append(f"No control mappings defined for '{std}'")
        return gaps

    def _normalize_standard(self, std: str) -> str:
        """Normalize a standard name for lookup."""
        mapping = {
            "soc2": "SOC2",
            "iso27001": "ISO27001",
            "hipaa": "HIPAA",
            "pci_dss": "PCI_DSS",
            "pci": "PCI_DSS",
            "nist_csf": "NIST_CSF",
            "nist": "NIST_CSF",
            "cis": "CIS",
        }
        return mapping.get(std.lower().replace("-", "").replace(" ", ""), std)
