"""
Compliance Checks
==================

Individual check implementations for the ComplianceEngine.
"""

import logging

from apps.network_engineer.nic.knowledge.compliance_models import (
    ComplianceCheck,
    ComplianceReport,
    ComplianceRule,
)
from apps.network_engineer.vendor.models import NetworkAST

logger = logging.getLogger(__name__)


def check_ssh_restricted(rule: ComplianceRule, raw: str) -> ComplianceCheck:
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


def check_telnet_disabled(rule: ComplianceRule, raw: str) -> ComplianceCheck:
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


def check_admin_password(rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
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


def check_ntp_enabled(rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
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


def check_logging_enabled(rule: ComplianceRule, raw: str) -> ComplianceCheck:
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


def check_backup_configured(rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
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


def check_unused_interfaces_disabled(rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
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


def check_ha_configured(rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
    vendor = getattr(ast, "vendor", "")
    vs = getattr(ast, "vendor_specific", {}) or {}

    has_ha = False
    if vendor == "cisco" and ("hsrp" in vs or "hsrp_priority" in vs) or vendor == "fortinet" and "ha_mode" in vs:
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


def check_firewall_rules(rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
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


def check_private_addressing(rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
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


def check_account_management(rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
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


def check_access_enforcement(rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
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


def check_monitoring(rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
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


def check_contingency(rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
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


def check_secure_protocols(rule: ComplianceRule, raw: str) -> ComplianceCheck:
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


def check_qos_configured(rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
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


def check_dynamic_routing(rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
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


def check_strong_passwords(rule: ComplianceRule, raw: str) -> ComplianceCheck:
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


def check_firmware(rule: ComplianceRule, raw: str) -> ComplianceCheck:
    return ComplianceCheck(
        rule_id=rule.id,
        rule_name=rule.name,
        status="warning",
        detail="Firmware version check requires live system",
        concept=rule.concept.value if rule.concept else None,
        references=rule.references,
    )


def check_vlans(rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
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


CHECK_REGISTRY = {
    "CIS-1.1": check_ssh_restricted,
    "CIS-1.2": check_telnet_disabled,
    "CIS-1.3": check_admin_password,
    "CIS-2.1": check_ntp_enabled,
    "CIS-2.2": check_logging_enabled,
    "CIS-2.3": check_backup_configured,
    "CIS-3.1": check_unused_interfaces_disabled,
    "CIS-3.2": check_ha_configured,
    "CIS-4.1": check_firewall_rules,
    "CIS-4.2": check_private_addressing,
    "NIST-AC-2": check_account_management,
    "NIST-AC-3": check_access_enforcement,
    "NIST-SI-4": check_monitoring,
    "NIST-CP-2": check_contingency,
    "PCI-6.1": check_firewall_rules,
    "PCI-6.2": check_secure_protocols,
    "PCI-10.1": check_logging_enabled,
    "PCI-10.6": check_monitoring,
    "ISP-1.1": check_ha_configured,
    "ISP-1.2": check_qos_configured,
    "ISP-2.1": check_dynamic_routing,
    "ISP-3.1": check_monitoring,
    "ISP-4.1": check_backup_configured,
    "SMB-1.1": check_firewall_rules,
    "SMB-1.2": check_strong_passwords,
    "SMB-2.1": check_firmware,
    "SMB-3.1": check_vlans,
}
