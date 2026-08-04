import logging
from typing import Any

logger = logging.getLogger(__name__)


class _NetworkConfigRuleMixin:
    def _check_missing_fasttrack(self, config: Any, report: Any, vendor: str = ""):
        if vendor != "mikrotik":
            return
        has_fasttrack = any("fasttrack" in line.lower() for line in config.raw_lines)
        if not has_fasttrack and (config.nat_rules or config.firewall_rules):
            report.add_issue("suggestion", "Performance", "FastTrack is not enabled", "Enable FastTrack for improved NAT performance", confidence=0.8)

    def _check_missing_backup(self, config: Any, report: Any, vendor: str = ""):
        if not config.metadata.get("backup_configured"):
            report.add_issue("warning", "Backup", "No backup configuration found", "Configure automatic backups", confidence=0.9)

    def _check_open_dns(self, config: Any, report: Any, vendor: str = ""):
        if config.dns_config and config.dns_config.allow_remote_requests:
            report.add_issue("warning", "DNS", "DNS allows remote requests", "Disable remote DNS requests unless required", confidence=1.0)

    def _check_missing_firewall_input(self, config: Any, report: Any, vendor: str = ""):
        if vendor != "mikrotik":
            return
        has_input = any("chain=input" in line.lower() for line in config.raw_lines)
        if not has_input:
            report.add_issue("critical", "Firewall", "No input chain rules found", "Add input chain firewall rules", confidence=1.0)

    def _check_missing_firewall_forward(self, config: Any, report: Any, vendor: str = ""):
        if vendor != "mikrotik":
            return
        if config.nat_rules and not any("chain=forward" in line.lower() for line in config.raw_lines):
            report.add_issue("critical", "Firewall", "Forward chain missing with NAT configured", "Add forward chain rules when using NAT", confidence=1.0)

    def _check_missing_icmp_accept(self, config: Any, report: Any, vendor: str = ""):
        if vendor != "mikrotik":
            return
        if not any("icmp" in line.lower() and "accept" in line.lower() for line in config.raw_lines):
            report.add_issue("info", "Firewall", "ICMP not explicitly allowed", "Consider allowing ICMP for diagnostics", confidence=0.7)

    def _check_missing_masquerade(self, config: Any, report: Any, vendor: str = ""):
        if vendor != "mikrotik":
            return
        if not any("masquerade" in line.lower() for line in config.raw_lines) and config.ip_addresses:
            report.add_issue("warning", "NAT", "No masquerade rule found", "Add masquerade for internet access", confidence=0.9)

    def _check_masquerade_on_lan(self, config: Any, report: Any, vendor: str = ""):
        for nat in config.nat_rules:
            if nat.action == "masquerade" and nat.out_interface and nat.out_interface.startswith("lan"):
                report.add_issue("warning", "NAT", "Masquerade on LAN interface", "Use WAN interface for masquerade", confidence=0.9)

    def _check_duplicate_nat(self, config: Any, report: Any, vendor: str = ""):
        if len(config.nat_rules) > 1:
            report.add_issue("warning", "NAT", "Multiple NAT rules detected", "Review NAT rules for conflicts", confidence=0.9)

    def _check_firewall_without_stateful(self, config: Any, report: Any, vendor: str = ""):
        if config.firewall_rules and not any("connection-state" in line.lower() for line in config.raw_lines):
            report.add_issue("warning", "Firewall", "No stateful inspection rules", "Add connection-state rules for security", confidence=0.8)

    def _check_bridge_loop_risk(self, config: Any, report: Any, vendor: str = ""):
        for bridge in config.bridge_configs:
            if len(bridge.ports) > 2 and not bridge.protocol_mode:
                report.add_issue("warning", "Bridge", f"Bridge {bridge.name} with {len(bridge.ports)} ports and no STP", "Enable STP to prevent loops", confidence=0.9)

    def _check_bridge_without_stp(self, config: Any, report: Any, vendor: str = ""):
        for bridge in config.bridge_configs:
            if not bridge.protocol_mode:
                report.add_issue("suggestion", "Bridge", f"Bridge {bridge.name} has no protocol mode", "Configure STP or RSTP to prevent loops", confidence=0.8)

    def _check_missing_connection_tracking(self, config: Any, report: Any, vendor: str = ""):
        if vendor != "mikrotik":
            return
        if config.firewall_rules and not any("connection-state" in line.lower() for line in config.raw_lines):
            report.add_issue("warning", "Firewall", "No connection tracking rules", "Add connection-state rules", confidence=0.8)

    def _check_firewall_rule_order(self, config: Any, report: Any, vendor: str = ""):
        drop_rules = sum(1 for r in config.firewall_rules if r.action == "drop")
        accept_rules = sum(1 for r in config.firewall_rules if r.action == "accept")
        if drop_rules > 0 and accept_rules > 0 and drop_rules < accept_rules / 2:
            report.add_issue("info", "Firewall", "Firewall rule order may allow unwanted traffic", "Review rule order", confidence=0.6)

    def _check_service_without_restriction(self, config: Any, report: Any, vendor: str = ""):
        for svc in config.metadata.get("ip_services", []):
            if svc.get("address") == "0.0.0.0/0" and not svc.get("disabled", False):
                report.add_issue("warning", "Security", f"Service {svc.get('name')} open to all", "Restrict service to trusted networks", confidence=1.0)

    def _check_missing_ntp(self, config: Any, report: Any, vendor: str = ""):
        if not any("ntp" in line.lower() for line in config.raw_lines):
            report.add_issue("info", "System", "NTP not configured", "Configure NTP for accurate timekeeping", confidence=0.9)

    def _check_missing_logging(self, config: Any, report: Any, vendor: str = ""):
        if not any("log" in line.lower() for line in config.raw_lines):
            report.add_issue("info", "System", "Logging not configured", "Configure logging for audit trail", confidence=0.9)

    def _check_interface_mtu_mismatch(self, config: Any, report: Any, vendor: str = ""):
        if not any("mtu" in line.lower() for line in config.raw_lines):
            report.add_issue("suggestion", "Performance", "No MTU configuration found", "Consider setting MTU for optimal performance", confidence=0.6)

    def _check_missing_loopback(self, config: Any, report: Any, vendor: str = ""):
        if not any("/interface loopback" in line.lower() for line in config.raw_lines):
            report.add_issue("suggestion", "System", "No loopback interface", "Add loopback for stable router ID", confidence=0.6)

    def _check_dns_without_upstream(self, config: Any, report: Any, vendor: str = ""):
        if config.dns_config and not config.dns_config.servers:
            report.add_issue("warning", "DNS", "No DNS servers configured", "Configure upstream DNS servers", confidence=0.9)

    def _check_dns_servers_public_only(self, config: Any, report: Any, vendor: str = ""):
        if config.dns_config and config.dns_config.servers:
            for server in config.dns_config.servers:
                if server.startswith(("8.8.8.", "1.1.1.")):
                    report.add_issue("suggestion", "DNS", "Using public DNS only", "Consider internal DNS for privacy", confidence=0.5)

    def _check_hotspot_without_profile(self, config: Any, report: Any, vendor: str = ""):
        for hs in config.hotspot_configs:
            if not hs.profile:
                report.add_issue("warning", "Hotspot", f"Hotspot {hs.name} has no profile", "Assign a hotspot profile", confidence=0.9)

    def _check_hotspot_dns_unsafe(self, config: Any, report: Any, vendor: str = ""):
        for hs in config.hotspot_configs:
            if hs.profile and "default" in hs.profile.lower():
                report.add_issue("warning", "Hotspot", f"Hotspot {hs.name} using default profile", "Use custom hotspot profile", confidence=0.8)

    def _check_dhcp_without_static(self, config: Any, report: Any, vendor: str = ""):
        if config.dhcp_servers:
            report.add_issue("suggestion", "DHCP", "DHCP server without static mappings", "Add static DHCP mappings for known devices", confidence=0.7)

    def _check_dhcp_pool_exhaustion(self, config: Any, report: Any, vendor: str = ""):
        for dhcp in config.dhcp_servers:
            if not dhcp.address_pool:
                report.add_issue("warning", "DHCP", f"DHCP {dhcp.name} has no pool", "Configure address pool", confidence=0.9)

    def _check_queue_without_limit(self, config: Any, report: Any, vendor: str = ""):
        for queue in config.queue_configs:
            if not queue.max_limit:
                report.add_issue("warning", "QoS", f"Queue {queue.name} has no max limit", "Set max-limit for bandwidth control", confidence=0.9)

    def _check_queue_simple_duplicate(self, config: Any, report: Any, vendor: str = ""):
        targets = [q.target for q in config.queue_configs if q.target]
        if len(targets) != len(set(targets)):
            report.add_issue("warning", "QoS", "Duplicate queue targets", "Review queue configuration", confidence=0.9)

    def _check_vlan_without_parent(self, config: Any, report: Any, vendor: str = ""):
        if config.bridge_configs and not any("vlan" in line.lower() for line in config.raw_lines):
            report.add_issue("suggestion", "VLAN", "Bridges without VLAN filtering", "Enable VLAN filtering on bridges", confidence=0.7)
