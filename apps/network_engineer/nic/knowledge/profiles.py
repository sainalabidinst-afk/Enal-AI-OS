"""
Compliance Profiles
====================

Cross-vendor compliance profiles (CIS, NIST, PCI DSS, ISP Best Practice, SMB Best Practice).
All profiles operate on Universal AST, making them vendor-agnostic.
"""

import logging
from dataclasses import dataclass, field
from typing import Any

from apps.network_engineer.nic.knowledge.ontology import UniversalConcept, ConceptDefinition
from apps.network_engineer.vendor.models import NetworkAST

logger = logging.getLogger(__name__)


@dataclass
class ComplianceRule:
    id: str
    name: str
    description: str
    severity: str = "warning"
    vendor: str = "all"
    concept: UniversalConcept | None = None
    references: list[str] = field(default_factory=list)


@dataclass
class ComplianceCheck:
    rule_id: str
    rule_name: str
    status: str
    detail: str = ""
    evidence: str = ""
    concept: str | None = None
    references: list[str] = field(default_factory=list)


@dataclass
class ComplianceReport:
    device_id: str
    vendor: str
    profile: str
    checks: list[ComplianceCheck] = field(default_factory=list)
    score: float = 0.0
    passed: int = 0
    failed: int = 0
    warnings: int = 0
    skipped: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "device_id": self.device_id,
            "vendor": self.vendor,
            "profile": self.profile,
            "score": round(self.score, 2),
            "passed": self.passed,
            "failed": self.failed,
            "warnings": self.warnings,
            "skipped": self.skipped,
            "checks": [
                {
                    "rule_id": c.rule_id,
                    "rule_name": c.rule_name,
                    "status": c.status,
                    "detail": c.detail,
                    "evidence": c.evidence,
                    "concept": c.concept,
                    "references": c.references,
                }
                for c in self.checks
            ],
        }


class ComplianceProfile:
    """Base class for compliance profiles."""

    name: str = "base"
    description: str = "Base compliance profile"

    def get_rules(self) -> list[ComplianceRule]:
        raise NotImplementedError


class CISProfile(ComplianceProfile):
    name = "CIS"
    description = "CIS Benchmarks for network devices"

    def get_rules(self) -> list[ComplianceRule]:
        return [
            ComplianceRule(
                id="CIS-1.1",
                name="SSH Restricted",
                description="SSH must not be open to 0.0.0.0/0",
                severity="critical",
                concept=UniversalConcept.TRAFFIC_FILTERING,
                references=["CIS Benchmark 1.1"],
            ),
            ComplianceRule(
                id="CIS-1.2",
                name="Telnet Disabled",
                description="Telnet must not be enabled",
                severity="critical",
                concept=UniversalConcept.TRAFFIC_FILTERING,
                references=["CIS Benchmark 1.2"],
            ),
            ComplianceRule(
                id="CIS-1.3",
                name="Admin Password Set",
                description="Admin password must be set and strong",
                severity="critical",
                concept=UniversalConcept.AUTHENTICATION,
                references=["CIS Benchmark 1.3"],
            ),
            ComplianceRule(
                id="CIS-2.1",
                name="NTP Enabled",
                description="NTP must be enabled for accurate timekeeping",
                severity="warning",
                concept=UniversalConcept.TIME_SYNCHRONIZATION,
                references=["CIS Benchmark 2.1"],
            ),
            ComplianceRule(
                id="CIS-2.2",
                name="Logging Enabled",
                description="Logging must be enabled for audit trail",
                severity="warning",
                concept=UniversalConcept.LOGGING,
                references=["CIS Benchmark 2.2"],
            ),
            ComplianceRule(
                id="CIS-2.3",
                name="Backup Configured",
                description="Backup must be configured and tested",
                severity="warning",
                concept=UniversalConcept.BACKUP,
                references=["CIS Benchmark 2.3"],
            ),
            ComplianceRule(
                id="CIS-3.1",
                name="Unused Interfaces Disabled",
                description="Unused interfaces should be disabled",
                severity="info",
                concept=UniversalConcept.IP_MANAGEMENT,
                references=["CIS Benchmark 3.1"],
            ),
            ComplianceRule(
                id="CIS-3.2",
                name="HA or Redundancy Configured",
                description="Critical devices should have HA/redundancy",
                severity="warning",
                concept=UniversalConcept.HIGH_AVAILABILITY,
                references=["CIS Benchmark 3.3"],
            ),
            ComplianceRule(
                id="CIS-4.1",
                name="Firewall Rules Exist",
                description="Firewall/filter rules must be configured",
                severity="critical",
                concept=UniversalConcept.TRAFFIC_FILTERING,
                references=["CIS Benchmark 4.1"],
            ),
            ComplianceRule(
                id="CIS-4.2",
                name="NAT or Private Addressing",
                description="Internal addresses should use RFC 1918 private space",
                severity="warning",
                concept=UniversalConcept.ADDRESS_TRANSLATION,
                references=["CIS Benchmark 4.2"],
            ),
        ]


class NISTProfile(ComplianceProfile):
    name = "NIST"
    description = "NIST SP 800-53 Security Controls"

    def get_rules(self) -> list[ComplianceRule]:
        return [
            ComplianceRule(
                id="NIST-AC-2",
                name="Account Management",
                description="Account management policies must be enforced",
                severity="warning",
                concept=UniversalConcept.AUTHENTICATION,
                references=["NIST SP 800-53 AC-2"],
            ),
            ComplianceRule(
                id="NIST-AC-3",
                name="Access Enforcement",
                description="Access enforcement mechanisms must be in place",
                severity="warning",
                concept=UniversalConcept.TRAFFIC_FILTERING,
                references=["NIST SP 800-53 AC-3"],
            ),
            ComplianceRule(
                id="NIST-SI-4",
                name="System Monitoring",
                description="System monitoring must be enabled",
                severity="warning",
                concept=UniversalConcept.MONITORING,
                references=["NIST SP 800-53 SI-4"],
            ),
            ComplianceRule(
                id="NIST-CP-2",
                name="Contingency Plan",
                description="Contingency and backup plans must exist",
                severity="warning",
                concept=UniversalConcept.BACKUP,
                references=["NIST SP 800-53 CP-2"],
            ),
        ]


class PCIDSSProfile(ComplianceProfile):
    name = "PCI-DSS"
    description = "PCI DSS v4.0 for payment card networks"

    def get_rules(self) -> list[ComplianceRule]:
        return [
            ComplianceRule(
                id="PCI-6.1",
                name="Firewall Rules",
                description="Firewall rules must restrict inbound/outbound traffic",
                severity="critical",
                concept=UniversalConcept.TRAFFIC_FILTERING,
                references=["PCI DSS 6.1"],
            ),
            ComplianceRule(
                id="PCI-6.2",
                name="Secure Network Protocols",
                description="Only secure protocols should be used",
                severity="critical",
                concept=UniversalConcept.TRAFFIC_FILTERING,
                references=["PCI DSS 6.2"],
            ),
            ComplianceRule(
                id="PCI-10.1",
                name="Audit Trail",
                description="Audit trail must be enabled and retained",
                severity="warning",
                concept=UniversalConcept.LOGGING,
                references=["PCI DSS 10.1"],
            ),
            ComplianceRule(
                id="PCI-10.6",
                name="Review Logs",
                description="Security logs must be reviewed regularly",
                severity="warning",
                concept=UniversalConcept.MONITORING,
                references=["PCI DSS 10.6"],
            ),
        ]


class ISPBestPracticeProfile(ComplianceProfile):
    name = "ISP-Best-Practice"
    description = "Best practices for ISP and enterprise networks"

    def get_rules(self) -> list[ComplianceRule]:
        return [
            ComplianceRule(
                id="ISP-1.1",
                name="High Availability",
                description="Critical routers should have VRRP/HSRP/HA configured",
                severity="warning",
                concept=UniversalConcept.HIGH_AVAILABILITY,
            ),
            ComplianceRule(
                id="ISP-1.2",
                name="QoS Configured",
                description="QoS should be configured for traffic prioritization",
                severity="warning",
                concept=UniversalConcept.QOS,
            ),
            ComplianceRule(
                id="ISP-2.1",
                name="BGP or OSPF",
                description="Dynamic routing should be used for resilience",
                severity="info",
                concept=UniversalConcept.ROUTING,
            ),
            ComplianceRule(
                id="ISP-3.1",
                name="Monitoring Enabled",
                description="SNMP and logging should be enabled",
                severity="warning",
                concept=UniversalConcept.MONITORING,
            ),
            ComplianceRule(
                id="ISP-4.1",
                name="Backup Configured",
                description="Automated backups should be configured",
                severity="warning",
                concept=UniversalConcept.BACKUP,
            ),
        ]


class SMBBestPracticeProfile(ComplianceProfile):
    name = "SMB-Best-Practice"
    description = "Best practices for small and medium business networks"

    def get_rules(self) -> list[ComplianceRule]:
        return [
            ComplianceRule(
                id="SMB-1.1",
                name="Firewall Enabled",
                description="Firewall must be enabled and configured",
                severity="critical",
                concept=UniversalConcept.TRAFFIC_FILTERING,
            ),
            ComplianceRule(
                id="SMB-1.2",
                name="Strong Passwords",
                description="Admin passwords must be strong",
                severity="critical",
                concept=UniversalConcept.AUTHENTICATION,
            ),
            ComplianceRule(
                id="SMB-2.1",
                name="Firmware Updated",
                description="Device firmware should be up to date",
                severity="warning",
                concept=UniversalConcept.SYSTEM_IDENTITY,
            ),
            ComplianceRule(
                id="SMB-3.1",
                name="VLAN Segmented",
                description="Network should be segmented with VLANs",
                severity="info",
                concept=UniversalConcept.VLAN,
            ),
        ]


PROFILES: dict[str, ComplianceProfile] = {
    "CIS": CISProfile(),
    "NIST": NISTProfile(),
    "PCI-DSS": PCIDSSProfile(),
    "ISP-Best-Practice": ISPBestPracticeProfile(),
    "SMB-Best-Practice": SMBBestPracticeProfile(),
}


class ComplianceEngine:
    """Checks configurations against compliance profiles."""

    def __init__(self, profile_name: str = "CIS"):
        profile = PROFILES.get(profile_name)
        if not profile:
            raise ValueError(f"Unknown compliance profile: {profile_name}")
        self._profile = profile
        self._rules = profile.get_rules()

    @property
    def profile_name(self) -> str:
        return self._profile.name

    def check(self, ast: NetworkAST) -> ComplianceReport:
        """Check AST against compliance rules."""
        report = ComplianceReport(
            device_id=ast.device_id,
            vendor=ast.vendor,
            profile=self._profile.name,
        )
        raw = "\n".join(ast.raw_lines).lower()

        for rule in self._rules:
            check = self._check_rule(rule, ast, raw)
            report.checks.append(check)

            if check.status == "pass":
                report.passed += 1
            elif check.status == "fail":
                report.failed += 1
            elif check.status == "warning":
                report.warnings += 1
            else:
                report.skipped += 1

        total = len(self._rules)
        report.score = (report.passed / total * 100) if total > 0 else 0.0
        return report

    def _check_rule(self, rule: ComplianceRule, ast: NetworkAST, raw: str) -> ComplianceCheck:
        if rule.id == "CIS-1.1":
            return self._check_ssh_restricted(rule, raw)
        elif rule.id == "CIS-1.2":
            return self._check_telnet_disabled(rule, raw)
        elif rule.id == "CIS-1.3":
            return self._check_admin_password(rule, ast)
        elif rule.id == "CIS-2.1":
            return self._check_ntp_enabled(rule, ast)
        elif rule.id == "CIS-2.2":
            return self._check_logging_enabled(rule, raw)
        elif rule.id == "CIS-2.3":
            return self._check_backup_configured(rule, ast)
        elif rule.id == "CIS-3.1":
            return self._check_unused_interfaces_disabled(rule, ast)
        elif rule.id == "CIS-3.2":
            return self._check_ha_configured(rule, ast)
        elif rule.id == "CIS-4.1":
            return self._check_firewall_rules(rule, ast)
        elif rule.id == "CIS-4.2":
            return self._check_private_addressing(rule, ast)
        elif rule.id == "NIST-AC-2":
            return self._check_account_management(rule, ast)
        elif rule.id == "NIST-AC-3":
            return self._check_access_enforcement(rule, ast)
        elif rule.id == "NIST-SI-4":
            return self._check_monitoring(rule, ast)
        elif rule.id == "NIST-CP-2":
            return self._check_contingency(rule, ast)
        elif rule.id == "PCI-6.1":
            return self._check_firewall_rules(rule, ast)
        elif rule.id == "PCI-6.2":
            return self._check_secure_protocols(rule, raw)
        elif rule.id == "PCI-10.1":
            return self._check_logging_enabled(rule, raw)
        elif rule.id == "PCI-10.6":
            return self._check_monitoring(rule, ast)
        elif rule.id == "ISP-1.1":
            return self._check_ha_configured(rule, ast)
        elif rule.id == "ISP-1.2":
            return self._check_qos_configured(rule, ast)
        elif rule.id == "ISP-2.1":
            return self._check_dynamic_routing(rule, ast)
        elif rule.id == "ISP-3.1":
            return self._check_monitoring(rule, ast)
        elif rule.id == "ISP-4.1":
            return self._check_backup_configured(rule, ast)
        elif rule.id == "SMB-1.1":
            return self._check_firewall_rules(rule, ast)
        elif rule.id == "SMB-1.2":
            return self._check_strong_passwords(rule, raw)
        elif rule.id == "SMB-2.1":
            return self._check_firmware(rule, raw)
        elif rule.id == "SMB-3.1":
            return self._check_vlans(rule, ast)

        return ComplianceCheck(rule_id=rule.id, rule_name=rule.name, status="skip", detail="Rule not implemented")

    def _check_ssh_restricted(self, rule: ComplianceRule, raw: str) -> ComplianceCheck:
        if "0.0.0.0/0" in raw and ("ssh" in raw or "winbox" in raw):
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="fail",
                detail="SSH or management service is open to 0.0.0.0/0",
                evidence="Found 0.0.0.0/0 with SSH/management service",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="pass",
            detail="SSH is not open to the world",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_telnet_disabled(self, rule: ComplianceRule, raw: str) -> ComplianceCheck:
        if "telnet" in raw:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="fail",
                detail="Telnet is enabled (unencrypted)",
                evidence="Found telnet in configuration",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="pass",
            detail="Telnet is not enabled",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_admin_password(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        has_users = len(getattr(ast, "users", [])) > 0 or "username" in "\n".join(ast.raw_lines).lower()
        if not has_users:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="warning",
                detail="Cannot verify admin password from config",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="pass",
            detail="Admin accounts are configured",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_ntp_enabled(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        if getattr(ast.system, "ntp_enabled", False):
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="pass",
                detail="NTP is enabled",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="fail",
            detail="NTP is not configured",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_logging_enabled(self, rule: ComplianceRule, raw: str) -> ComplianceCheck:
        if "log" in raw or "logging" in raw:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="pass",
                detail="Logging is configured",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="fail",
            detail="Logging is not configured",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_backup_configured(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        if getattr(ast.system, "backup_configured", False):
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="pass",
                detail="Backup is configured",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="fail",
            detail="No backup configuration found",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_unused_interfaces_disabled(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        unused = [i for i in ast.interfaces if getattr(i, "status", "enabled") == "enabled" and not any(ip.interface == i.name for ip in ast.ip_addresses)]
        if unused:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="warning",
                detail=f"{len(unused)} unused interfaces are enabled",
                evidence=", ".join(i.name for i in unused),
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="pass",
            detail="No unused interfaces enabled",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_ha_configured(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        vendor = getattr(ast, "vendor", "")
        vs = getattr(ast, "vendor_specific", {}) or {}

        has_ha = False
        if vendor == "cisco" and ("hsrp" in vs or "hsrp_priority" in vs):
            has_ha = True
        elif vendor == "fortinet" and "ha_mode" in vs:
            has_ha = True
        elif vendor == "mikrotik":
            raw = "\n".join(ast.raw_lines).lower()
            if "vrrp" in raw:
                has_ha = True

        if has_ha:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="pass",
                detail="HA/redundancy is configured",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="warning",
            detail="No HA/redundancy configuration found",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_firewall_rules(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        if ast.firewall_rules:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="pass",
                detail=f"{len(ast.firewall_rules)} firewall rules configured",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="fail",
            detail="No firewall rules configured",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_private_addressing(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        private_prefixes = ["10.", "172.16.", "172.17.", "172.18.", "172.19.", "172.20.", "172.21.", "172.22.", "172.23.", "172.24.", "172.25.", "172.26.", "172.27.", "172.28.", "172.29.", "172.30.", "172.31.", "192.168."]
        has_private = any(
            any(ip.address.startswith(p) for p in private_prefixes)
            for ip in ast.ip_addresses
        )
        if has_private:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="pass",
                detail="Private addressing (RFC 1918) is in use",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="warning",
            detail="No RFC 1918 private addressing detected",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_account_management(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        raw = "\n".join(ast.raw_lines).lower()
        if "username" in raw or "system local" in raw:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="pass",
                detail="Account management is configured",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="warning",
            detail="Account management not detected",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_access_enforcement(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        if ast.firewall_rules:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="pass",
                detail="Access enforcement rules are configured",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="warning",
            detail="No access enforcement rules found",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_monitoring(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        raw = "\n".join(ast.raw_lines).lower()
        if "snmp" in raw or "log" in raw:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="pass",
                detail="Monitoring is configured",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="fail",
            detail="Monitoring is not configured",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_contingency(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        raw = "\n".join(ast.raw_lines).lower()
        if "backup" in raw or "export" in raw:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="pass",
                detail="Backup/contingency is configured",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="warning",
            detail="No contingency/backup configuration found",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_secure_protocols(self, rule: ComplianceRule, raw: str) -> ComplianceCheck:
        if "telnet" in raw:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="fail",
                detail="Insecure protocol telnet is enabled",
                evidence="Found telnet in configuration",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="pass",
            detail="No insecure protocols detected",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_qos_configured(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        raw = "\n".join(ast.raw_lines).lower()
        if "queue" in raw or "qos" in raw or "shaper" in raw:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="pass",
                detail="QoS is configured",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="warning",
            detail="No QoS configuration found",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_dynamic_routing(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        raw = "\n".join(ast.raw_lines).lower()
        if "router ospf" in raw or "router bgp" in raw or "routing ospf" in raw or "routing bgp" in raw:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="pass",
                detail="Dynamic routing is configured",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="info",
            detail="Only static routing detected",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_strong_passwords(self, rule: ComplianceRule, raw: str) -> ComplianceCheck:
        if "password=" in raw and ("admin" in raw or "1234" in raw):
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="fail",
                detail="Weak or default password detected",
                evidence="Found default/weak password pattern",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="pass",
            detail="No weak passwords detected",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_firmware(self, rule: ComplianceRule, raw: str) -> ComplianceCheck:
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="warning",
            detail="Firmware version check requires live system",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )

    def _check_vlans(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        if getattr(ast, "vlans", []):
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status="pass",
                detail=f"{len(ast.vlans)} VLANs configured",
                concept=rule.concept.value if rule.concept else None,
                references=rule.references,
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status="info",
            detail="No VLANs configured",
            concept=rule.concept.value if rule.concept else None,
            references=rule.references,
        )


def get_compliance_engine(profile_name: str = "CIS") -> ComplianceEngine:
    return ComplianceEngine(profile_name)
