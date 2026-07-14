from __future__ import annotations

from enum import Enum

from backend.app.core.attachments.models import InfrastructureAST, Severity


class ComplianceFramework(str, Enum):
    CIS = "cis"
    NIST_CSF = "nist_csf"
    ZERO_TRUST = "zero_trust"
    VENDOR_BEST_PRACTICE = "vendor_best_practice"
    CISCO = "cisco"
    FORTINET = "fortinet"
    MIKROTIK = "mikrotik"


class ComplianceCheck:
    def __init__(self, framework: ComplianceFramework, control_id: str, title: str, description: str) -> None:
        self.framework = framework
        self.control_id = control_id
        self.title = title
        self.description = description
        self.passed = False
        self.evidence: list[str] = []
        self.remediation: str | None = None
        self.severity = Severity.low


class ComplianceEngine:
    def evaluate(self, ast: InfrastructureAST, frameworks: list[ComplianceFramework] | None = None) -> list[ComplianceCheck]:
        frameworks = frameworks or [ComplianceFramework.CIS, ComplianceFramework.NIST_CSF, ComplianceFramework.ZERO_TRUST, ComplianceFramework.VENDOR_BEST_PRACTICE]
        checks: list[ComplianceCheck] = []
        for framework in frameworks:
            checks.extend(self._run_framework(ast, framework))
        return checks

    def _run_framework(self, ast: InfrastructureAST, framework: ComplianceFramework) -> list[ComplianceCheck]:
        if framework == ComplianceFramework.CIS:
            return self._cis_checks(ast)
        if framework == ComplianceFramework.NIST_CSF:
            return self._nist_checks(ast)
        if framework == ComplianceFramework.ZERO_TRUST:
            return self._zero_trust_checks(ast)
        if framework == ComplianceFramework.VENDOR_BEST_PRACTICE:
            return self._vendor_best_practice_checks(ast)
        return []

    def _cis_checks(self, ast: InfrastructureAST) -> list[ComplianceCheck]:
        checks: list[ComplianceCheck] = []
        check = ComplianceCheck(ComplianceFramework.CIS, "CIS-3.1.1", "Disable unnecessary network services", "Ensure management services like Telnet/FTP are disabled.")
        check.passed = not self._text_contains_any(ast, ["telnet enabled", "ftp enabled", "service telnet", "service ftp"])
        if not check.passed:
            check.evidence = self._find_evidence(ast, ["telnet enabled", "ftp enabled", "service telnet", "service ftp"])
            check.remediation = "Disable Telnet and FTP; use SSH/HTTPS for management."
            check.severity = Severity.high
        checks.append(check)

        check = ComplianceCheck(ComplianceFramework.CIS, "CIS-3.1.2", "Enable encrypted management protocols", "Ensure only encrypted management protocols are used.")
        check.passed = self._text_contains_any(ast, ["ssh", "https"])
        if not check.passed:
            check.evidence = self._find_evidence(ast, ["ssh", "https", "management"])
            check.remediation = "Enable SSH/HTTPS and disable plaintext management protocols."
            check.severity = Severity.high
        checks.append(check)

        check = ComplianceCheck(ComplianceFramework.CIS, "CIS-4.1", "Secure routing protocol authentication", "Use authentication for routing protocols when supported.")
        check.passed = self._text_contains_any(ast, ["ospf authentication", "bgp authentication", "md5"])
        if not check.passed:
            check.evidence = self._find_evidence(ast, ["ospf", "bgp", "rip"])
            check.remediation = "Enable routing protocol authentication if supported."
            check.severity = Severity.medium
        checks.append(check)

        check = ComplianceCheck(ComplianceFramework.CIS, "CIS-9.1", "Ensure firewall rules are defined", "Verify firewall rules exist for traffic filtering.")
        check.passed = bool(ast.firewall)
        if not check.passed:
            check.evidence = ["No firewall rules detected."]
            check.remediation = "Add explicit firewall rules."
            check.severity = Severity.high
        checks.append(check)

        return checks

    def _nist_checks(self, ast: InfrastructureAST) -> list[ComplianceCheck]:
        checks: list[ComplianceCheck] = []
        check = ComplianceCheck(ComplianceFramework.NIST_CSF, "NIST-PR.AC-1", "Manage access to assets", "Restrict management access and avoid default or broad configurations.")
        check.passed = self._text_contains_any(ast, ["vlan", "acl", "access-list", "policy"])
        if not check.passed:
            check.evidence = self._find_evidence(ast, ["vlan", "acl", "access-list", "policy"])
            check.remediation = "Add access control segmentation for management and user traffic."
            check.severity = Severity.medium
        checks.append(check)

        check = ComplianceCheck(ComplianceFramework.NIST_CSF, "NIST-PR.DS-1", "Protect data at rest and in transit", "Avoid plaintext protocols and unencrypted channels.")
        check.passed = not self._text_contains_any(ast, ["telnet", "ftp", "http"])
        if not check.passed:
            check.evidence = self._find_evidence(ast, ["telnet", "ftp", "http"])
            check.remediation = "Use encrypted protocols such as SSH, HTTPS, FTPS, or SFTP."
            check.severity = Severity.high
        checks.append(check)

        check = ComplianceCheck(ComplianceFramework.NIST_CSF, "NIST-DE.CM-1", "Configuration baseline and change management", "Maintain configuration integrity and track changes.")
        check.passed = bool(ast.system)
        if not check.passed:
            check.evidence = ["Limited system metadata detected."]
            check.remediation = "Document system metadata and baseline configuration."
            check.severity = Severity.low
        checks.append(check)
        return checks

    def _zero_trust_checks(self, ast: InfrastructureAST) -> list[ComplianceCheck]:
        checks: list[ComplianceCheck] = []
        check = ComplianceCheck(ComplianceFramework.ZERO_TRUST, "ZT-1", "Verify explicitly", "Enforce identity and posture checks before granting access.")
        check.passed = self._text_contains_any(ast, ["aaa", "authentication", "policy", "identity"])
        if not check.passed:
            check.evidence = self._find_evidence(ast, ["aaa", "authentication", "policy"])
            check.remediation = "Add explicit authentication and policy enforcement for all traffic segments."
            check.severity = Severity.high
        checks.append(check)

        check = ComplianceCheck(ComplianceFramework.ZERO_TRUST, "ZT-2", "Use least privilege access", "Restrict services, interfaces, and administrative access to the minimum required.")
        check.passed = not self._text_contains_any(ast, ["any", "0.0.0.0/0", "anywhere"])
        if not check.passed:
            check.evidence = self._find_evidence(ast, ["any", "0.0.0.0/0", "anywhere"])
            check.remediation = "Replace broad source/destination rules with least-privilege filters."
            check.severity = Severity.high
        checks.append(check)

        check = ComplianceCheck(ComplianceFramework.ZERO_TRUST, "ZT-3", "Assume breach and monitor continuously", "Enable logging, monitoring, and inspection for lateral movement.")
        check.passed = self._text_contains_any(ast, ["log", "monitor", "inspect", "telemetry"])
        if not check.passed:
            check.evidence = self._find_evidence(ast, ["log", "monitor", "inspect", "telemetry"])
            check.remediation = "Enable logging and monitoring for traffic, authentication, and configuration changes."
            check.severity = Severity.medium
        checks.append(check)
        return checks

    def _vendor_best_practice_checks(self, ast: InfrastructureAST) -> list[ComplianceCheck]:
        checks: list[ComplianceCheck] = []
        if ast.vendor.value == "mikrotik":
            checks.extend(self._mikrotik_best_practices(ast))
        elif ast.vendor.value == "cisco":
            checks.extend(self._cisco_best_practices(ast))
        elif ast.vendor.value == "fortinet":
            checks.extend(self._fortinet_best_practices(ast))
        return checks

    def _mikrotik_best_practices(self, ast: InfrastructureAST) -> list[ComplianceCheck]:
        checks: list[ComplianceCheck] = []
        check = ComplianceCheck(ComplianceFramework.VENDOR_BEST_PRACTICE, "MTK-1", "Disable unused services", "RouterOS enables several services by default.")
        check.passed = not self._text_contains_any(ast, ["telnet enabled", "ftp enabled", "api enabled"])
        if not check.passed:
            check.evidence = self._find_evidence(ast, ["telnet enabled", "ftp enabled", "api enabled"])
            check.remediation = "Disable unused services and restrict API/management access."
            check.severity = Severity.high
        checks.append(check)

        check = ComplianceCheck(ComplianceFramework.VENDOR_BEST_PRACTICE, "MTK-2", "Filter management plane", "Restrict management access to trusted IPs or VLANs.")
        check.passed = self._text_contains_any(ast, ["management_vlan", "management-access", "allowed_management"])
        if not check.passed:
            check.evidence = self._find_evidence(ast, ["management", "allowed_management"])
            check.remediation = "Create a dedicated management VLAN and restrict access by source address."
            check.severity = Severity.medium
        checks.append(check)
        return checks

    def _cisco_best_practices(self, ast: InfrastructureAST) -> list[ComplianceCheck]:
        checks: list[ComplianceCheck] = []
        check = ComplianceCheck(ComplianceFramework.VENDOR_BEST_PRACTICE, "CISCO-1", "Disable unused interfaces", "Disable unused switchports and router interfaces.")
        check.passed = self._text_contains_any(ast, ["shutdown", "no shutdown"])
        if not check.passed:
            check.evidence = self._find_evidence(ast, ["interface "])
            check.remediation = "Shutdown unused interfaces and apply port security where supported."
            check.severity = Severity.medium
        checks.append(check)
        return checks

    def _fortinet_best_practices(self, ast: InfrastructureAST) -> list[ComplianceCheck]:
        checks: list[ComplianceCheck] = []
        check = ComplianceCheck(ComplianceFramework.VENDOR_BEST_PRACTICE, "FORTI-1", "Enable strict firewall policy defaults", "Ensure default action is deny and implicit deny is enforced.")
        check.passed = self._text_contains_any(ast, ["deny", "drop", "implicit"])
        if not check.passed:
            check.evidence = self._find_evidence(ast, ["firewall", "policy"])
            check.remediation = "Ensure implicit deny and default-deny policies are enforced."
            check.severity = Severity.high
        checks.append(check)
        return checks

    def _text_contains_any(self, ast: InfrastructureAST, keywords: list[str]) -> bool:
        blob = " ".join(
            str(item.get("raw", ""))
            for item in (
                ast.interfaces + ast.vlans + ast.routing + ast.firewall + ast.services + ast.security + ast.wireless + ast.ha
            )
        ).lower()
        return any(keyword.lower() in blob for keyword in keywords)

    def _find_evidence(self, ast: InfrastructureAST, keywords: list[str]) -> list[str]:
        evidence: list[str] = []
        for item in (
            ast.interfaces + ast.vlans + ast.routing + ast.firewall + ast.services + ast.security + ast.wireless + ast.ha
        ):
            raw = str(item.get("raw", ""))
            lowered = raw.lower()
            if any(keyword.lower() in lowered for keyword in keywords):
                evidence.append(raw)
            if len(evidence) >= 5:
                break
        return evidence or ["No direct evidence found."]
