"""
Network Configuration Analyzer
===============================

Analyzes RouterOS configurations for security, performance, and best practices.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

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


class NetworkAnalyzer:
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

    def _get_interfaces_with_ips(self, config: Any) -> set[str]:
        return {ip.interface for ip in config.ip_addresses if ip.interface}

    def _check_default_password(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if any("password=" in line.lower() and ("admin" in line.lower() or "1234" in line or "password" in line.lower()) for line in config.raw_lines):
            report.add_issue(Severity.CRITICAL, "Security", "Default or weak password detected", "Change to a strong password immediately", confidence=0.9)

    def _check_unrestricted_winbox(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for line in config.raw_lines:
            if "winbox" in line.lower() and "0.0.0.0/0" in line:
                report.add_issue(Severity.CRITICAL, "Security", "Winbox is open to the world", "Restrict Winbox access to management IPs only", confidence=1.0)

    def _check_unrestricted_ssh(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for line in config.raw_lines:
            if "ssh" in line.lower() and "0.0.0.0/0" in line:
                report.add_issue(Severity.WARNING, "Security", "SSH is open to the world", "Restrict SSH access to management IPs", confidence=1.0)

    def _check_unrestricted_www(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for line in config.raw_lines:
            if "www" in line.lower() and "0.0.0.0/0" in line:
                report.add_issue(Severity.WARNING, "Security", "Web interface is open to the world", "Restrict web access to trusted networks", confidence=1.0)

    def _check_unrestricted_api(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for line in config.raw_lines:
            if "api" in line.lower() and "0.0.0.0/0" in line:
                report.add_issue(Severity.WARNING, "Security", "API is open to the world", "Restrict API access to trusted networks", confidence=1.0)

    def _check_missing_fasttrack(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if vendor != "mikrotik":
            return
        has_fasttrack = any("fasttrack" in line.lower() for line in config.raw_lines)
        if not has_fasttrack and (config.nat_rules or config.firewall_rules):
            report.add_issue(Severity.SUGGESTION, "Performance", "FastTrack is not enabled", "Enable FastTrack for improved NAT performance", confidence=0.8)

    def _check_missing_backup(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if not config.metadata.get("backup_configured"):
            report.add_issue(Severity.WARNING, "Backup", "No backup configuration found", "Configure automatic backups", confidence=0.9)

    def _check_open_dns(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if config.dns_config and config.dns_config.allow_remote_requests:
            report.add_issue(Severity.WARNING, "DNS", "DNS allows remote requests", "Disable remote DNS requests unless required", confidence=1.0)

    def _check_missing_firewall_input(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if vendor != "mikrotik":
            return
        has_input = any("chain=input" in line.lower() for line in config.raw_lines)
        if not has_input:
            report.add_issue(Severity.CRITICAL, "Firewall", "No input chain rules found", "Add input chain firewall rules", confidence=1.0)

    def _check_missing_firewall_forward(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if vendor != "mikrotik":
            return
        if config.nat_rules and not any("chain=forward" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.CRITICAL, "Firewall", "Forward chain missing with NAT configured", "Add forward chain rules when using NAT", confidence=1.0)

    def _check_missing_icmp_accept(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if vendor != "mikrotik":
            return
        if not any("icmp" in line.lower() and "accept" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.INFO, "Firewall", "ICMP not explicitly allowed", "Consider allowing ICMP for diagnostics", confidence=0.7)

    def _check_missing_masquerade(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if vendor != "mikrotik":
            return
        if not any("masquerade" in line.lower() for line in config.raw_lines) and config.ip_addresses:
            report.add_issue(Severity.WARNING, "NAT", "No masquerade rule found", "Add masquerade for internet access", confidence=0.9)

    def _check_unused_interfaces(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        interfaces_with_ips = self._get_interfaces_with_ips(config)
        for iface in config.interfaces:
            has_ip = iface.name in interfaces_with_ips
            is_bridge_member = any(iface.name in bridge.ports for bridge in config.bridge_configs)
            disabled = getattr(iface, "disabled", None)
            if disabled is None:
                disabled = getattr(iface, "status", "enabled") == "disabled"
            if not has_ip and not is_bridge_member and not disabled:
                report.add_issue(Severity.INFO, "Interfaces", f"Interface {iface.name or '<unnamed>'} has no IP and is enabled", "Consider disabling unused interfaces", confidence=0.8)

    def _check_duplicate_nat(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if len(config.nat_rules) > 1:
            report.add_issue(Severity.WARNING, "NAT", "Multiple NAT rules detected", "Review NAT rules for conflicts", confidence=0.9)

    def _check_duplicate_ip_addresses(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        seen = {}
        for ip in config.ip_addresses:
            if ip.address in seen:
                report.add_issue(Severity.CRITICAL, "IP", f"Duplicate IP address {ip.address}", "Remove duplicate IP addresses", confidence=1.0)
            seen[ip.address] = True

    def _check_overlapping_networks(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        networks = [ip.network for ip in config.ip_addresses if ip.network]
        for i, net1 in enumerate(networks):
            for net2 in networks[i+1:]:
                if self._networks_overlap(net1, net2):
                    report.add_issue(Severity.WARNING, "IP", f"Overlapping networks {net1} and {net2}", "Fix network addressing", confidence=0.9)

    def _check_dhcp_without_static(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if config.dhcp_servers:
            report.add_issue(Severity.SUGGESTION, "DHCP", "DHCP server without static mappings", "Add static DHCP mappings for known devices", confidence=0.7)

    def _check_hotspot_without_profile(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for hs in config.hotspot_configs:
            if not hs.profile:
                report.add_issue(Severity.WARNING, "Hotspot", f"Hotspot {hs.name} has no profile", "Assign a hotspot profile", confidence=0.9)

    def _check_bridge_without_stp(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for bridge in config.bridge_configs:
            if not bridge.protocol_mode:
                report.add_issue(Severity.SUGGESTION, "Bridge", f"Bridge {bridge.name} has no protocol mode", "Configure STP or RSTP to prevent loops", confidence=0.8)

    def _check_queue_without_limit(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for queue in config.queue_configs:
            if not queue.max_limit:
                report.add_issue(Severity.WARNING, "QoS", f"Queue {queue.name} has no max limit", "Set max-limit for bandwidth control", confidence=0.9)

    def _check_route_without_gateway(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for route in config.routes:
            if route.dst_address and not route.gateway:
                report.add_issue(Severity.WARNING, "Routing", f"Route {route.dst_address} has no gateway", "Add gateway for static route", confidence=0.9)

    def _check_missing_ntp(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if not any("ntp" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.INFO, "System", "NTP not configured", "Configure NTP for accurate timekeeping", confidence=0.9)

    def _check_missing_logging(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if not any("log" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.INFO, "System", "Logging not configured", "Configure logging for audit trail", confidence=0.9)

    def _check_interface_mtu_mismatch(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if not any("mtu" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.SUGGESTION, "Performance", "No MTU configuration found", "Consider setting MTU for optimal performance", confidence=0.6)

    def _check_vlan_without_parent(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if config.bridge_configs and not any("vlan" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.SUGGESTION, "VLAN", "Bridges without VLAN filtering", "Enable VLAN filtering on bridges", confidence=0.7)

    def _check_user_without_password(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if not any("/user" in line.lower() and "password=" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.CRITICAL, "Security", "No user password configured", "Set password for all users", confidence=0.9)

    def _check_service_without_restriction(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for svc in config.metadata.get("ip_services", []):
            if svc.get("address") == "0.0.0.0/0" and not svc.get("disabled", False):
                report.add_issue(Severity.WARNING, "Security", f"Service {svc.get('name')} open to all", "Restrict service to trusted networks", confidence=1.0)

    def _check_dns_without_upstream(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if config.dns_config and not config.dns_config.servers:
            report.add_issue(Severity.WARNING, "DNS", "No DNS servers configured", "Configure upstream DNS servers", confidence=0.9)

    def _check_dhcp_pool_exhaustion(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for dhcp in config.dhcp_servers:
            if not dhcp.address_pool:
                report.add_issue(Severity.WARNING, "DHCP", f"DHCP {dhcp.name} has no pool", "Configure address pool", confidence=0.9)

    def _check_firewall_without_stateful(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if config.firewall_rules and not any("connection-state" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.WARNING, "Firewall", "No stateful inspection rules", "Add connection-state rules for security", confidence=0.8)

    def _check_bridge_loop_risk(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for bridge in config.bridge_configs:
            if len(bridge.ports) > 2 and not bridge.protocol_mode:
                report.add_issue(Severity.WARNING, "Bridge", f"Bridge {bridge.name} with {len(bridge.ports)} ports and no STP", "Enable STP to prevent loops", confidence=0.9)

    def _check_missing_loopback(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if not any("/interface loopback" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.SUGGESTION, "System", "No loopback interface", "Add loopback for stable router ID", confidence=0.6)

    def _check_mgmt_from_untrusted(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if vendor != "mikrotik":
            return
        mgmt_services = ["winbox", "ssh", "www", "api"]
        for svc in config.metadata.get("ip_services", []):
            if svc.get("name") in mgmt_services and svc.get("address") == "0.0.0.0/0":
                report.add_issue(Severity.CRITICAL, "Security", f"Management service {svc.get('name')} accessible from anywhere", "Restrict to management subnet", confidence=1.0)

    def _check_weak_password_in_comment(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for line in config.raw_lines:
            if "password=" in line.lower():
                import re
                comment_match = re.search(r'comment="([^"]*)"', line, re.IGNORECASE)
                if comment_match and any(word in comment_match.group(1).lower() for word in ["password", "secret", "admin"]):
                    report.add_issue(Severity.WARNING, "Security", "Password exposed in comment", "Remove password from comments", confidence=0.8)

    def _check_unencrypted_protocols(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if vendor != "mikrotik":
            return
        if any("telnet" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.CRITICAL, "Security", "Telnet is enabled (unencrypted)", "Use SSH instead of Telnet", confidence=1.0)
        if any("http" in line.lower() and "www" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.WARNING, "Security", "HTTP management enabled", "Use HTTPS for web management", confidence=0.9)

    def _check_missing_connection_tracking(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if vendor != "mikrotik":
            return
        if config.firewall_rules and not any("connection-state" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.WARNING, "Firewall", "No connection tracking rules", "Add connection-state rules", confidence=0.8)

    def _check_high_risk_ports_open(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        high_risk_ports = ["23", "2323", "3306", "5432", "6379", "27017"]
        for line in config.raw_lines:
            for port in high_risk_ports:
                if f"port={port}" in line and "0.0.0.0/0" in line:
                    report.add_issue(Severity.CRITICAL, "Security", f"High-risk port {port} open to world", "Close or restrict port", confidence=1.0)

    def _check_default_route_missing(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if not any(route.dst_address == "0.0.0.0/0" for route in config.routes):
            report.add_issue(Severity.WARNING, "Routing", "No default route configured", "Add default route for internet access", confidence=0.9)

    def _check_dns_servers_public_only(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if config.dns_config and config.dns_config.servers:
            for server in config.dns_config.servers:
                if server.startswith(("8.8.8.", "1.1.1.")):
                    report.add_issue(Severity.SUGGESTION, "DNS", "Using public DNS only", "Consider internal DNS for privacy", confidence=0.5)

    def _check_hotspot_dns_unsafe(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for hs in config.hotspot_configs:
            if hs.profile and "default" in hs.profile.lower():
                report.add_issue(Severity.WARNING, "Hotspot", f"Hotspot {hs.name} using default profile", "Use custom hotspot profile", confidence=0.8)

    def _check_ip_address_on_wrong_interface(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        valid_interfaces = {iface.name for iface in config.interfaces}
        valid_interfaces.update(f"vlan{v.id}" for v in getattr(config, "vlans", []))
        for ip in config.ip_addresses:
            if ip.interface and ip.interface not in valid_interfaces:
                report.add_issue(Severity.WARNING, "IP", f"IP {ip.address} on non-existent interface {ip.interface}", "Fix interface assignment", confidence=1.0)

    def _check_firewall_rule_order(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        drop_rules = sum(1 for r in config.firewall_rules if r.action == "drop")
        accept_rules = sum(1 for r in config.firewall_rules if r.action == "accept")
        if drop_rules > 0 and accept_rules > 0 and drop_rules < accept_rules / 2:
            report.add_issue(Severity.INFO, "Firewall", "Firewall rule order may allow unwanted traffic", "Review rule order", confidence=0.6)

    def _check_masquerade_on_lan(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for nat in config.nat_rules:
            if nat.action == "masquerade" and nat.out_interface and nat.out_interface.startswith("lan"):
                report.add_issue(Severity.WARNING, "NAT", "Masquerade on LAN interface", "Use WAN interface for masquerade", confidence=0.9)

    def _check_ppp_without_encryption(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if any("ppp" in line.lower() and "encryption=no" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.CRITICAL, "PPP", "PPP without encryption", "Enable PPP encryption", confidence=1.0)

    def _check_certificate_expired(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if any("certificate" in line.lower() and "expired" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.CRITICAL, "Security", "Expired certificate detected", "Renew certificate immediately", confidence=1.0)

    def _check_radius_without_backup(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if any("radius" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.WARNING, "Security", "RADIUS without backup", "Add backup RADIUS server", confidence=0.8)

    def _check_wireless_open_security(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if any("wireless" in line.lower() and "security-profile=default" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.CRITICAL, "Wireless", "Wireless using default security", "Configure proper wireless security", confidence=1.0)

    def _check_queue_simple_duplicate(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        targets = [q.target for q in config.queue_configs if q.target]
        if len(targets) != len(set(targets)):
            report.add_issue(Severity.WARNING, "QoS", "Duplicate queue targets", "Review queue configuration", confidence=0.9)

    def _check_telnet_enabled_cisco(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for line in config.raw_lines:
            if "telnet" in line.lower() and "disabled" not in line.lower():
                report.add_issue(Severity.CRITICAL, "Security", "Telnet is enabled (unencrypted)", "Use SSH instead of Telnet", confidence=1.0)

    def _check_ipsec_configured_cisco(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        has_ipsec = any("crypto isakmp" in line.lower() or "crypto map" in line.lower() for line in config.raw_lines)
        if has_ipsec:
            report.add_issue(Severity.INFO, "VPN", "IPSec VPN configured", "Verify IPSec configuration for security compliance", confidence=0.9)

    def _check_hsrp_configured_cisco(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for line in config.raw_lines:
            if "standby" in line.lower() and "ip" in line.lower():
                report.add_issue(Severity.INFO, "High Availability", "HSRP configured", "Verify HSRP authentication and preemption", confidence=0.9)

    def _check_wpa2_enterprise_wireless(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for line in config.raw_lines:
            if "wpa" in line.lower() and "wpa2" not in line.lower() and "wpa3" not in line.lower():
                if "enterprise" in line.lower() or "wpa" in line.lower():
                    report.add_issue(Severity.WARNING, "Wireless", "Wireless using WPA (not WPA2/3)", "Upgrade to WPA2-Enterprise or WPA3", confidence=0.8)
            if "wep" in line.lower():
                report.add_issue(Severity.CRITICAL, "Wireless", "WEP encryption enabled", "Replace with WPA2/WPA3 immediately", confidence=1.0)

    def _check_fortinet_firewall_policy(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        has_fortinet_fw = any("config firewall policy" in line.lower() or "firewall policy" in line.lower() for line in config.raw_lines)
        if has_fortinet_fw:
            for line in config.raw_lines:
                if "telnet" in line.lower() and "deny" not in line.lower():
                    report.add_issue(Severity.CRITICAL, "Security", "Fortinet firewall may allow Telnet", "Block Telnet in firewall policy", confidence=0.9)

    def _check_fortinet_vpn_ipsec(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for line in config.raw_lines:
            if "config vpn ipsec" in line.lower() or "vpn ipsec phase1" in line.lower():
                report.add_issue(Severity.INFO, "VPN", "Fortinet IPSec VPN configured", "Verify VPN phase1/phase2 settings", confidence=0.9)

    def _check_fortinet_ha_configured(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        has_ha = any("config system ha" in line.lower() or ("mode a-a" in line.lower() or "mode a-p" in line.lower()) for line in config.raw_lines)
        if has_ha:
            report.add_issue(Severity.INFO, "High Availability", "Fortinet HA configured", "Verify HA cluster settings", confidence=0.9)

    def _check_cisco_ospf_configured(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        for line in config.raw_lines:
            if "router ospf" in line.lower():
                has_auth = any("message-digest" in l.lower() or "area" in l.lower() for l in config.raw_lines)
                if not has_auth:
                    report.add_issue(Severity.WARNING, "Routing", "OSPF configured without authentication", "Add OSPF authentication for security", confidence=0.8)
                else:
                    report.add_issue(Severity.INFO, "Routing", "OSPF routing configured", "Verify OSPF configuration and areas", confidence=0.9)
                break

    def _check_cisco_snmp_enabled(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if vendor != "cisco":
            return
        if any("snmp-server" in line.lower() for line in config.raw_lines):
            has_acl = any("snmp-server" in line.lower() and "acl" in line.lower() for line in config.raw_lines)
            if not has_acl:
                report.add_issue(Severity.WARNING, "Services", "SNMP enabled without ACL restriction", "Restrict SNMP access with ACL", confidence=0.8)

    def _check_cisco_wireless_dot11(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if vendor != "cisco":
            return
        if any("dot11" in line.lower() or "ssid" in line.lower() for line in config.raw_lines):
            has_wpa = any("wpa" in line.lower() for line in config.raw_lines)
            if not has_wpa:
                report.add_issue(Severity.CRITICAL, "Wireless", "Wireless SSID without WPA encryption", "Enable WPA2/WPA3 for wireless security", confidence=0.9)

    def _check_cisco_vlan_trunking(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if vendor != "cisco":
            return
        if any("vlan" in line.lower() and "switchport" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.INFO, "Switching", "VLAN trunking configured", "Verify trunking and allowed VLANs", confidence=0.8)
        if any("vlan" in line.lower() and "switchport mode trunk" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.INFO, "Switching", "Switchport trunk mode enabled", "Confirm trunk encapsulation", confidence=0.9)

    def _check_cisco_policy_map_qos(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        if vendor != "cisco":
            return
        if any("policy-map" in line.lower() or "class-map" in line.lower() for line in config.raw_lines):
            report.add_issue(Severity.INFO, "QoS", "QoS policy-map configured", "Review bandwidth allocation and priority", confidence=0.8)

    def _networks_overlap(self, net1: str, net2: str) -> bool:
        try:
            parts1 = net1.split("/")
            parts2 = net2.split("/")
            if len(parts1) != 2 or len(parts2) != 2:
                return False
            ip1, prefix1 = parts1
            ip2, prefix2 = parts2
            if ip1 == ip2:
                return True
            import ipaddress
            n1 = ipaddress.ip_network(f"{ip1}/{prefix1}", strict=False)
            n2 = ipaddress.ip_network(f"{ip2}/{prefix2}", strict=False)
            return n1.overlaps(n2)
        except Exception:
            return False

    def _check_bgp_security(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        has_bgp = any("bgp" in line.lower() or "router bgp" in line.lower() for line in config.raw_lines)
        if has_bgp:
            has_auth = any("neighbor" in line.lower() and ("password" in line.lower() or "ttl-security" in line.lower()) for line in config.raw_lines)
            if not has_auth:
                report.add_issue(Severity.WARNING, "BGP", "BGP without neighbor authentication", "Add MD5 authentication or TTL security to BGP peers", confidence=0.9)
            if "no synchronization" not in str(config.raw_lines).lower():
                report.add_issue(Severity.INFO, "BGP", "BGP synchronization check", "Consider enabling synchronization for full-mesh iBGP", confidence=0.7)

    def _check_mpls_ldp(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        has_mpls = any("mpls" in line.lower() or "ldp" in line.lower() for line in config.raw_lines)
        if has_mpls:
            report.add_issue(Severity.INFO, "MPLS", "MPLS LDP configured", "Verify LDP parameters and transport address", confidence=0.8)
            if not any("label mode" in line.lower() for line in config.raw_lines):
                report.add_issue(Severity.WARNING, "MPLS", "MPLS label conservation not configured", "Enable label mode for LDP label conservation", confidence=0.7)

    def _check_capsman_security(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        has_capsman = any("capsman" in line.lower() or "managed by capsman" in line.lower() for line in config.raw_lines)
        if has_capsman:
            has_security = any("security" in line.lower() and "wpa2" in line.lower() for line in config.raw_lines)
            if not has_security:
                report.add_issue(Severity.WARNING, "CAPsMAN", "CAPsMAN without WPA2 security", "Configure WPA2 security for managed APs", confidence=0.9)

    def _check_wireguard_peers(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        has_wg = any("wireguard" in line.lower() or "wg0" in line.lower() for line in config.raw_lines)
        if has_wg:
            if not any("allowed-address" in line.lower() for line in config.raw_lines):
                report.add_issue(Severity.WARNING, "WireGuard", "WireGuard peer without allowed-address", "Configure allowed-address for proper routing", confidence=0.9)
            if not any("persistent-keepalive" in line.lower() for line in config.raw_lines):
                report.add_issue(Severity.INFO, "WireGuard", "WireGuard without persistent-keepalive", "Add keepalive for NAT traversal", confidence=0.7)

    def _check_isis_configured(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        has_isis = any("isis" in line.lower() or "router isis" in line.lower() for line in config.raw_lines)
        if has_isis:
            report.add_issue(Severity.INFO, "Routing", "IS-IS routing configured", "Verify IS-IS NET address and area configuration", confidence=0.8)
            net_present = any("net " in line.lower() for line in config.raw_lines)
            if not net_present:
                report.add_issue(Severity.WARNING, "Routing", "IS-IS without NET address", "Configure NET address for IS-IS", confidence=0.9)

    def _check_eigrp_stubs(self, config: Any, report: NetworkAnalysisReport, vendor: str = ""):
        has_eigrp = any("eigrp" in line.lower() or "router eigrp" in line.lower() for line in config.raw_lines)
        if has_eigrp:
            report.add_issue(Severity.INFO, "Routing", "EIGRP routing configured", "Verify EIGRP autonomous system number and networks", confidence=0.8)
            if not any("passive-interface" in line.lower() for line in config.raw_lines):
                report.add_issue(Severity.SUGGESTION, "Routing", "EIGRP without passive interfaces", "Configure passive-interface for LAN segments", confidence=0.7)


network_analyzer = NetworkAnalyzer()
