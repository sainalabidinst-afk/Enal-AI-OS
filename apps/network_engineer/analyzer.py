"""
Network Configuration Analyzer
===============================

Analyzes RouterOS configurations for security, performance, and best practices.
Rule checks are organized into mixin classes for maintainability.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from apps.network_engineer.analyzer_security import _SecurityRuleMixin
from apps.network_engineer.analyzer_network import _NetworkConfigRuleMixin
from apps.network_engineer.analyzer_ip_routing import _IPRoutingRuleMixin
from apps.network_engineer.analyzer_vendor import _VendorRuleMixin

logger = logging.getLogger(__name__)


class Severity(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    SUGGESTION = "suggestion"


@dataclass
class AnalysisIssue:
    severity: Severity
    category: str
    description: str
    recommendation: str
    line_number: int | None = None
    confidence: float = 1.0
    references: list[str] = field(default_factory=list)


@dataclass
class NetworkAnalysisReport:
    device_name: str
    issues: list[AnalysisIssue] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_issue(
        self,
        severity: Severity,
        category: str,
        description: str,
        recommendation: str,
        line_number: int | None = None,
        confidence: float = 1.0,
        references: list[str] | None = None,
    ):
        self.issues.append(AnalysisIssue(
            severity=severity,
            category=category,
            description=description,
            recommendation=recommendation,
            line_number=line_number,
            confidence=confidence,
            references=references or [],
        ))

    def get_summary(self) -> dict[str, Any]:
        return {
            "total_issues": len(self.issues),
            "critical": sum(1 for i in self.issues if i.severity == Severity.CRITICAL),
            "warnings": sum(1 for i in self.issues if i.severity == Severity.WARNING),
            "info": sum(1 for i in self.issues if i.severity == Severity.INFO),
            "suggestions": sum(1 for i in self.issues if i.severity == Severity.SUGGESTION),
        }


class NetworkAnalyzer(_SecurityRuleMixin, _NetworkConfigRuleMixin, _IPRoutingRuleMixin, _VendorRuleMixin):
    """Analyzes network configurations for issues and best practices."""

    def __init__(self):
        self._rules = [
            self._check_default_password,
            self._check_unrestricted_winbox,
            self._check_unrestricted_ssh,
            self._check_unrestricted_www,
            self._check_unrestricted_api,
            self._check_missing_fasttrack,
            self._check_missing_backup,
            self._check_open_dns,
            self._check_missing_firewall_input,
            self._check_missing_firewall_forward,
            self._check_missing_icmp_accept,
            self._check_missing_masquerade,
            self._check_unused_interfaces,
            self._check_duplicate_nat,
            self._check_duplicate_ip_addresses,
            self._check_overlapping_networks,
            self._check_dhcp_without_static,
            self._check_hotspot_without_profile,
            self._check_bridge_without_stp,
            self._check_queue_without_limit,
            self._check_route_without_gateway,
            self._check_missing_ntp,
            self._check_missing_logging,
            self._check_interface_mtu_mismatch,
            self._check_vlan_without_parent,
            self._check_user_without_password,
            self._check_service_without_restriction,
            self._check_dns_without_upstream,
            self._check_dhcp_pool_exhaustion,
            self._check_firewall_without_stateful,
            self._check_bridge_loop_risk,
            self._check_missing_loopback,
            self._check_mgmt_from_untrusted,
            self._check_weak_password_in_comment,
            self._check_unencrypted_protocols,
            self._check_missing_connection_tracking,
            self._check_high_risk_ports_open,
            self._check_default_route_missing,
            self._check_dns_servers_public_only,
            self._check_hotspot_dns_unsafe,
            self._check_ip_address_on_wrong_interface,
            self._check_firewall_rule_order,
            self._check_masquerade_on_lan,
            self._check_ppp_without_encryption,
            self._check_certificate_expired,
            self._check_radius_without_backup,
            self._check_wireless_open_security,
            self._check_queue_simple_duplicate,
            self._check_telnet_enabled_cisco,
            self._check_ipsec_configured_cisco,
            self._check_hsrp_configured_cisco,
            self._check_wpa2_enterprise_wireless,
            self._check_fortinet_firewall_policy,
            self._check_fortinet_vpn_ipsec,
            self._check_fortinet_ha_configured,
            self._check_cisco_ospf_configured,
            self._check_cisco_snmp_enabled,
            self._check_cisco_wireless_dot11,
            self._check_cisco_vlan_trunking,
            self._check_cisco_policy_map_qos,
            self._check_bgp_security,
            self._check_mpls_ldp,
            self._check_capsman_security,
            self._check_wireguard_peers,
            self._check_isis_configured,
            self._check_eigrp_stubs,
        ]

    async def analyze(self, config: Any, topology: Any | None = None) -> NetworkAnalysisReport:
        device_name = config.system_identity.name if config.system_identity else "Router"
        report = NetworkAnalysisReport(device_name=device_name)
        vendor = getattr(config, "vendor", "") or ""
        for rule in self._rules:
            try:
                rule(config, report, vendor)
            except Exception as e:
                logger.error(f"Analysis rule failed: {e}")
        try:
            from apps.network_engineer.enterprise_knowledge import enterprise_knowledge_engine
            findings = enterprise_knowledge_engine.analyze(config)
            for finding in findings:
                severity = Severity(finding.severity) if finding.severity in Severity._value2member_map_ else Severity.INFO
                report.add_issue(
                    severity=severity,
                    category=f"{finding.domain}.{finding.category}",
                    description=finding.description,
                    recommendation=finding.recommendation,
                    confidence=finding.confidence,
                    references=finding.references,
                )
        except Exception as e:
            logger.error(f"Enterprise knowledge analysis failed: {e}")
        report.summary = report.get_summary()
        parser_errors = getattr(config, "errors", [])
        report.metadata["total_rules"] = len(self._rules)
        report.metadata["parser_errors"] = len(parser_errors) if isinstance(parser_errors, list) else 0
        return report


network_analyzer = NetworkAnalyzer()
