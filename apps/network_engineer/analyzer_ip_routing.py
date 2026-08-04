import logging
from typing import Any

logger = logging.getLogger(__name__)


class _IPRoutingRuleMixin:
    def _get_interfaces_with_ips(self, config: Any) -> set[str]:
        return {ip.interface for ip in config.ip_addresses if ip.interface}

    def _check_unused_interfaces(self, config: Any, report: Any, vendor: str = ""):
        interfaces_with_ips = self._get_interfaces_with_ips(config)
        for iface in config.interfaces:
            has_ip = iface.name in interfaces_with_ips
            is_bridge_member = any(iface.name in bridge.ports for bridge in config.bridge_configs)
            disabled = getattr(iface, "disabled", None)
            if disabled is None:
                disabled = getattr(iface, "status", "enabled") == "disabled"
            if not has_ip and not is_bridge_member and not disabled:
                report.add_issue("info", "Interfaces", f"Interface {iface.name or '<unnamed>'} has no IP and is enabled", "Consider disabling unused interfaces", confidence=0.8)

    def _check_duplicate_ip_addresses(self, config: Any, report: Any, vendor: str = ""):
        seen = {}
        for ip in config.ip_addresses:
            if ip.address in seen:
                report.add_issue("critical", "IP", f"Duplicate IP address {ip.address}", "Remove duplicate IP addresses", confidence=1.0)
            seen[ip.address] = True

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

    def _check_overlapping_networks(self, config: Any, report: Any, vendor: str = ""):
        networks = [ip.network for ip in config.ip_addresses if ip.network]
        for i, net1 in enumerate(networks):
            for net2 in networks[i+1:]:
                if self._networks_overlap(net1, net2):
                    report.add_issue("warning", "IP", f"Overlapping networks {net1} and {net2}", "Fix network addressing", confidence=0.9)

    def _check_ip_address_on_wrong_interface(self, config: Any, report: Any, vendor: str = ""):
        valid_interfaces = {iface.name for iface in config.interfaces}
        valid_interfaces.update(f"vlan{v.id}" for v in getattr(config, "vlans", []))
        for ip in config.ip_addresses:
            if ip.interface and ip.interface not in valid_interfaces:
                report.add_issue("warning", "IP", f"IP {ip.address} on non-existent interface {ip.interface}", "Fix interface assignment", confidence=1.0)

    def _check_route_without_gateway(self, config: Any, report: Any, vendor: str = ""):
        for route in config.routes:
            if route.dst_address and not route.gateway:
                report.add_issue("warning", "Routing", f"Route {route.dst_address} has no gateway", "Add gateway for static route", confidence=0.9)

    def _check_default_route_missing(self, config: Any, report: Any, vendor: str = ""):
        if not any(route.dst_address == "0.0.0.0/0" for route in config.routes):
            report.add_issue("warning", "Routing", "No default route configured", "Add default route for internet access", confidence=0.9)

    def _check_bgp_security(self, config: Any, report: Any, vendor: str = ""):
        has_bgp = any("bgp" in line.lower() or "router bgp" in line.lower() for line in config.raw_lines)
        if has_bgp:
            has_auth = any("neighbor" in line.lower() and ("password" in line.lower() or "ttl-security" in line.lower()) for line in config.raw_lines)
            if not has_auth:
                report.add_issue("warning", "BGP", "BGP without neighbor authentication", "Add MD5 authentication or TTL security to BGP peers", confidence=0.9)
            if "no synchronization" not in str(config.raw_lines).lower():
                report.add_issue("info", "BGP", "BGP synchronization check", "Consider enabling synchronization for full-mesh iBGP", confidence=0.7)

    def _check_mpls_ldp(self, config: Any, report: Any, vendor: str = ""):
        has_mpls = any("mpls" in line.lower() or "ldp" in line.lower() for line in config.raw_lines)
        if has_mpls:
            report.add_issue("info", "MPLS", "MPLS LDP configured", "Verify LDP parameters and transport address", confidence=0.8)
            if not any("label mode" in line.lower() for line in config.raw_lines):
                report.add_issue("warning", "MPLS", "MPLS label conservation not configured", "Enable label mode for LDP label conservation", confidence=0.7)

    def _check_capsman_security(self, config: Any, report: Any, vendor: str = ""):
        has_capsman = any("capsman" in line.lower() or "managed by capsman" in line.lower() for line in config.raw_lines)
        if has_capsman:
            has_security = any("security" in line.lower() and "wpa2" in line.lower() for line in config.raw_lines)
            if not has_security:
                report.add_issue("warning", "CAPsMAN", "CAPsMAN without WPA2 security", "Configure WPA2 security for managed APs", confidence=0.9)

    def _check_isis_configured(self, config: Any, report: Any, vendor: str = ""):
        has_isis = any("isis" in line.lower() or "router isis" in line.lower() for line in config.raw_lines)
        if has_isis:
            report.add_issue("info", "Routing", "IS-IS routing configured", "Verify IS-IS NET address and area configuration", confidence=0.8)
            net_present = any("net " in line.lower() for line in config.raw_lines)
            if not net_present:
                report.add_issue("warning", "Routing", "IS-IS without NET address", "Configure NET address for IS-IS", confidence=0.9)

    def _check_eigrp_stubs(self, config: Any, report: Any, vendor: str = ""):
        has_eigrp = any("eigrp" in line.lower() or "router eigrp" in line.lower() for line in config.raw_lines)
        if has_eigrp:
            report.add_issue("info", "Routing", "EIGRP routing configured", "Verify EIGRP autonomous system number and networks", confidence=0.8)
            if not any("passive-interface" in line.lower() for line in config.raw_lines):
                report.add_issue("suggestion", "Routing", "EIGRP without passive interfaces", "Configure passive-interface for LAN segments", confidence=0.7)

    def _check_cisco_ospf_configured(self, config: Any, report: Any, vendor: str = ""):
        for line in config.raw_lines:
            if "router ospf" in line.lower():
                has_auth = any("message-digest" in l.lower() or "area" in l.lower() for l in config.raw_lines)
                if not has_auth:
                    report.add_issue("warning", "Routing", "OSPF configured without authentication", "Add OSPF authentication for security", confidence=0.8)
                else:
                    report.add_issue("info", "Routing", "OSPF routing configured", "Verify OSPF configuration and areas", confidence=0.9)
                break

    def _check_cisco_snmp_enabled(self, config: Any, report: Any, vendor: str = ""):
        if vendor != "cisco":
            return
        if any("snmp-server" in line.lower() for line in config.raw_lines):
            has_acl = any("snmp-server" in line.lower() and "acl" in line.lower() for line in config.raw_lines)
            if not has_acl:
                report.add_issue("warning", "Services", "SNMP enabled without ACL restriction", "Restrict SNMP access with ACL", confidence=0.8)

    def _check_cisco_wireless_dot11(self, config: Any, report: Any, vendor: str = ""):
        if vendor != "cisco":
            return
        if any("dot11" in line.lower() or "ssid" in line.lower() for line in config.raw_lines):
            has_wpa = any("wpa" in line.lower() for line in config.raw_lines)
            if not has_wpa:
                report.add_issue("critical", "Wireless", "Wireless SSID without WPA encryption", "Enable WPA2/WPA3 for wireless security", confidence=0.9)

    def _check_cisco_vlan_trunking(self, config: Any, report: Any, vendor: str = ""):
        if vendor != "cisco":
            return
        if any("vlan" in line.lower() and "switchport" in line.lower() for line in config.raw_lines):
            report.add_issue("info", "Switching", "VLAN trunking configured", "Verify trunking and allowed VLANs", confidence=0.8)
        if any("vlan" in line.lower() and "switchport mode trunk" in line.lower() for line in config.raw_lines):
            report.add_issue("info", "Switching", "Switchport trunk mode enabled", "Confirm trunk encapsulation", confidence=0.9)

    def _check_cisco_policy_map_qos(self, config: Any, report: Any, vendor: str = ""):
        if vendor != "cisco":
            return
        if any("policy-map" in line.lower() or "class-map" in line.lower() for line in config.raw_lines):
            report.add_issue("info", "QoS", "QoS policy-map configured", "Review bandwidth allocation and priority", confidence=0.8)

    def _check_wpa2_enterprise_wireless(self, config: Any, report: Any, vendor: str = ""):
        for line in config.raw_lines:
            if "wpa" in line.lower() and "wpa2" not in line.lower() and "wpa3" not in line.lower():
                if "enterprise" in line.lower() or "wpa" in line.lower():
                    report.add_issue("warning", "Wireless", "Wireless using WPA (not WPA2/3)", "Upgrade to WPA2-Enterprise or WPA3", confidence=0.8)
            if "wep" in line.lower():
                report.add_issue("critical", "Wireless", "WEP encryption enabled", "Replace with WPA2/WPA3 immediately", confidence=1.0)
