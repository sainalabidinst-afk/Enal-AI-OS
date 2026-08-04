"""
Fortinet FortiOS Vendor Adapter
=================================

Converts FortiOS configs to/from Universal AST.
"""

import logging

from apps.network_engineer.vendor.base import VendorAdapter
from apps.network_engineer.vendor.models import (
    InterfaceType,
    NetworkAST,
    RuleAction,
    UniversalDHCPServer,
    UniversalDNS,
    UniversalFirewallRule,
    UniversalInterface,
    UniversalIPAddress,
    UniversalNATRule,
    UniversalRoute,
    UniversalUser,
    UniversalVPN,
)
from apps.network_engineer.vendor.fortinet_parsers import (
    parse_dns,
    parse_dhcp,
    parse_firewall_policies,
    parse_ha,
    parse_interfaces,
    parse_nat,
    parse_ntp,
    parse_routes,
    parse_syslog,
    parse_system,
    parse_users,
    parse_vlans,
    parse_vpn,
)

logger = logging.getLogger(__name__)


class FortiOSAdapter(VendorAdapter):
    """Fortinet FortiOS adapter."""

    vendor_name = "fortinet"
    vendor_versions = ["fortios-6", "fortios-7"]

    def detect(self, config_text: str) -> bool:
        """Detect FortiOS config."""
        indicators = [
            "config system interface",
            "config firewall policy",
            "config system global",
            "config vpn ipsec phase1-interface",
            'edit "',
            "next",
            "end",
            "set hostname ",
            "set ip ",
            "set action ",
        ]
        return any(indicator in config_text for indicator in indicators)

    def parse(self, config_text: str) -> NetworkAST:
        """Parse FortiOS config into Universal AST."""
        ast = NetworkAST(vendor="fortinet")
        lines = config_text.splitlines()

        parse_system(ast, lines)
        parse_interfaces(ast, lines)
        parse_vlans(ast, lines)
        parse_routes(ast, lines)
        parse_dhcp(ast, lines)
        parse_dns(ast, lines)
        parse_ntp(ast, lines)
        parse_syslog(ast, lines)
        parse_firewall_policies(ast, lines)
        parse_vpn(ast, lines)
        parse_users(ast, lines)
        parse_ha(ast, lines)
        parse_nat(ast, lines)
        ast.raw_lines = [line for line in lines if line.strip() and not line.strip().startswith("#")]
        return ast

    def generate(self, ast: NetworkAST) -> str:
        """Generate FortiOS config from Universal AST."""
        lines = []
        lines.append("config system global")
        if ast.system.hostname:
            lines.append(f"    set hostname {ast.system.hostname}")
        lines.append("end")
        lines.append("")

        lines.append("config system interface")
        for iface in ast.interfaces:
            lines.append(f'    edit "{iface.name}"')
            for ip in ast.ip_addresses:
                if ip.interface == iface.name:
                    parts = ip.address.split("/")
                    if len(parts) == 2:
                        lines.append(f"        set ip {parts[0]} {parts[1]}")
            lines.append("    next")
        lines.append("end")
        lines.append("")

        lines.append("config firewall policy")
        for rule in ast.firewall_rules:
            lines.append(f"    edit {rule.id}")
            lines.append(f"        set action {rule.action.value}")
            lines.append("    next")
        lines.append("end")

        return "\n".join(lines)


fortinet_adapter = FortiOSAdapter()
