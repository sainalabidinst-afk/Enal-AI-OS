"""
Cisco IOS Vendor Adapter
=========================

Full Cisco IOS/IOS-XE/NX-OS parser.
"""

import logging

from apps.network_engineer.vendor.base import VendorAdapter
from apps.network_engineer.vendor.models import (
    InterfaceType,
    NetworkAST,
    RuleAction,
    UniversalBGP,
    UniversalDHCPServer,
    UniversalFirewallRule,
    UniversalInterface,
    UniversalIPAddress,
    UniversalNATRule,
    UniversalRoute,
    UniversalUser,
    UniversalVLAN,
)
from apps.network_engineer.vendor.cisco_ios_parsers import (
    parse_aaa,
    parse_acls,
    parse_bgp,
    parse_dhcp,
    parse_dns,
    parse_enable,
    parse_hsrp,
    parse_interfaces,
    parse_ip_addresses,
    parse_logging,
    parse_ntp,
    parse_ospf,
    parse_routes,
    parse_snmp,
    parse_spanning_tree,
    parse_system,
    parse_users,
    parse_vlans,
    parse_ssh_telnet,
)

logger = logging.getLogger(__name__)


class CiscoIOSAdapter(VendorAdapter):
    """Full Cisco IOS/IOS-XE/NX-OS adapter."""

    vendor_name = "cisco"
    vendor_versions = ["ios", "ios-xe", "nx-os"]

    def detect(self, config_text: str) -> bool:
        """Detect Cisco IOS config."""
        fortios_markers = [
            "config system global",
            "config firewall policy",
            "config system interface",
            "config vpn ipsec",
            "set hostname ",
        ]
        if any(marker in config_text for marker in fortios_markers):
            return False

        indicators = [
            "interface GigabitEthernet",
            "interface FastEthernet",
            "interface TenGigabitEthernet",
            "interface Dot11Radio",
            "interface BVI",
            "ip access-list ",
            "ip nat inside source",
            "line vty",
            "enable password",
            "router bgp ",
            "ip route ",
            "dot11 ssid",
            "router ospf",
            "snmp-server",
            "hostname ",
        ]
        return any(indicator in config_text for indicator in indicators)

    def _detect_subversion(self, config_text: str) -> str:
        """Detect Cisco sub-version."""
        if "vdc " in config_text.lower() or "vpc-domain" in config_text.lower():
            return "nx-os"
        if "interface GigabitEthernet" in config_text or "interface TenGigabitEthernet" in config_text:
            return "ios-xe"
        return "ios"

    def parse(self, config_text: str) -> NetworkAST:
        """Parse Cisco IOS config into Universal AST."""
        subversion = self._detect_subversion(config_text)
        ast = NetworkAST(vendor="cisco", vendor_version=subversion)
        lines = config_text.splitlines()

        parse_system(ast, lines)
        parse_interfaces(ast, lines)
        parse_vlans(ast, lines)
        parse_ip_addresses(ast, lines)
        parse_routes(ast, lines)
        parse_acls(ast, lines)
        parse_nat(ast, lines)
        parse_dhcp(ast, lines)
        parse_hsrp(ast, lines)
        parse_ospf(ast, lines)
        parse_bgp(ast, lines)
        parse_aaa(ast, lines)
        parse_snmp(ast, lines)
        parse_ntp(ast, lines)
        parse_logging(ast, lines)
        parse_ssh_telnet(ast, lines)
        parse_users(ast, lines)
        parse_enable(ast, lines)
        parse_dns(ast, lines)
        parse_spanning_tree(ast, lines)
        ast.raw_lines = [line for line in lines if line.strip() and not line.strip().startswith("!")]
        return ast

    @staticmethod
    def _mask_to_prefix(mask: str) -> str:
        binary = sum(int(o).bit_count() for o in mask.split("."))
        return str(binary)

    def generate(self, ast: NetworkAST) -> str:
        """Generate Cisco IOS config from Universal AST."""
        lines = []
        if ast.system.hostname:
            lines.append(f"hostname {ast.system.hostname}")
            lines.append("")

        for iface in ast.interfaces:
            lines.append(f"interface {iface.name}")
            for ip in ast.ip_addresses:
                if ip.interface == iface.name:
                    parts = ip.address.split("/")
                    if len(parts) == 2:
                        lines.append(f" ip address {parts[0]} {parts[1]}")
            lines.append(" no shutdown")
            lines.append("!")

        for route in ast.routes:
            parts = route.destination.split("/")
            if len(parts) == 2:
                lines.append(f"ip route {parts[0]} {parts[1]} {route.gateway}")

        lines.append("end")
        return "\n".join(lines)


cisco_ios_adapter = CiscoIOSAdapter()
