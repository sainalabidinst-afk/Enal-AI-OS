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
    UniversalVLAN,
    UniversalVPN,
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

        self._parse_system(ast, lines)
        self._parse_interfaces(ast, lines)
        self._parse_vlans(ast, lines)
        self._parse_routes(ast, lines)
        self._parse_dhcp(ast, lines)
        self._parse_dns(ast, lines)
        self._parse_ntp(ast, lines)
        self._parse_syslog(ast, lines)
        self._parse_firewall_policies(ast, lines)
        self._parse_vpn(ast, lines)
        self._parse_users(ast, lines)
        self._parse_ha(ast, lines)
        self._parse_nat(ast, lines)
        ast.raw_lines = [line for line in lines if line.strip() and not line.strip().startswith("#")]
        return ast

    def _parse_system(self, ast: NetworkAST, lines: list[str]):
        in_system = False
        for line in lines:
            stripped = line.strip()
            if stripped == "config system global":
                in_system = True
            elif in_system and stripped == "end":
                in_system = False
            elif in_system and stripped.startswith("set hostname "):
                ast.system.hostname = stripped.split(" ", 2)[2].strip()
            elif in_system and stripped.startswith("set timezone "):
                ast.system.timezone = stripped.split(" ", 2)[2].strip()
            elif in_system and stripped.startswith("set admin-sport "):
                pass

    def _parse_interfaces(self, ast: NetworkAST, lines: list[str]):
        in_interface = False
        current_interface = None
        for line in lines:
            stripped = line.strip()
            if stripped == "config system interface":
                in_interface = True
            elif in_interface and stripped == "end":
                in_interface = False
            elif in_interface and stripped.startswith("edit "):
                iface_name = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 1)[1]
                current_interface = UniversalInterface(
                    name=iface_name,
                    type=InterfaceType.ETHERNET,
                )
                ast.interfaces.append(current_interface)
            elif in_interface and current_interface is not None:
                if stripped.startswith("set ip "):
                    parts = stripped.split()
                    if len(parts) >= 4:
                        ip = parts[2]
                        mask = parts[3]
                        ast.ip_addresses.append(UniversalIPAddress(
                            address=f"{ip}/{mask}",
                            interface=current_interface.name,
                        ))
                elif stripped.startswith("set type "):
                    iface_type = stripped.split(" ", 2)[2].strip()
                    if "vlan" in iface_type.lower():
                        current_interface.type = InterfaceType.VLAN
                    elif "tunnel" in iface_type.lower():
                        current_interface.type = InterfaceType.TUNNEL
                    elif "loopback" in iface_type.lower():
                        current_interface.type = InterfaceType.LOOPBACK
                elif stripped.startswith("set alias "):
                    current_interface.comment = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]
                elif stripped.startswith("set mtu "):
                    try:
                        current_interface.mtu = int(stripped.split(" ", 2)[2])
                    except (ValueError, IndexError):
                        pass
                elif stripped.startswith("set status "):
                    status = stripped.split(" ", 2)[2].strip()
                    current_interface.status = "enabled" if status == "up" else "disabled"

    def _parse_vlans(self, ast: NetworkAST, lines: list[str]):
        in_vlan = False
        current_vlan = None
        for line in lines:
            stripped = line.strip()
            if stripped == "config system vlan":
                in_vlan = True
            elif in_vlan and stripped == "end":
                in_vlan = False
            elif in_vlan and stripped.startswith("edit "):
                vlan_id_str = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 1)[1]
                try:
                    vlan_id = int(vlan_id_str)
                    current_vlan = UniversalVLAN(id=vlan_id)
                    ast.vlans.append(current_vlan)
                except ValueError:
                    current_vlan = None
            elif in_vlan and current_vlan is not None:
                if stripped.startswith("set ip "):
                    parts = stripped.split()
                    if len(parts) >= 4:
                        ast.ip_addresses.append(UniversalIPAddress(
                            address=f"{parts[2]}/{parts[3]}",
                            interface=f"vlan{current_vlan.id}",
                            vlan_id=current_vlan.id,
                        ))
                elif stripped.startswith("set interface "):
                    current_vlan.interface = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]

    def _parse_routes(self, ast: NetworkAST, lines: list[str]):
        in_route = False
        for line in lines:
            stripped = line.strip()
            if stripped == "config router static":
                in_route = True
            elif in_route and stripped == "end":
                in_route = False
            elif in_route and stripped.startswith("edit "):
                pass
            elif in_route and stripped.startswith("set gateway "):
                gateway = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]
                ast.routes.append(UniversalRoute(
                    destination="0.0.0.0/0",
                    gateway=gateway,
                ))
            elif in_route and stripped.startswith("set dst "):
                dst = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]
                ast.vendor_specific.setdefault("pending_routes", []).append({"dst": dst})

    def _parse_dhcp(self, ast: NetworkAST, lines: list[str]):
        in_dhcp = False
        current_server = None
        for line in lines:
            stripped = line.strip()
            if stripped == "config system dhcp server":
                in_dhcp = True
            elif in_dhcp and stripped == "end":
                in_dhcp = False
            elif in_dhcp and stripped.startswith("edit "):
                server_id = stripped.split(" ", 1)[1]
                current_server = UniversalDHCPServer(name=f"dhcp-{server_id}")
                ast.dhcp_servers.append(current_server)
            elif in_dhcp and current_server is not None:
                if stripped.startswith("set default-gateway "):
                    current_server.vendor_specific["default_gateway"] = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]
                elif stripped.startswith("set dns-service "):
                    pass
                elif stripped.startswith("set lease-time "):
                    current_server.lease_time = stripped.split(" ", 2)[2]

    def _parse_dns(self, ast: NetworkAST, lines: list[str]):
        in_dns = False
        for line in lines:
            stripped = line.strip()
            if stripped == "config system dns":
                in_dns = True
            elif in_dns and stripped == "end":
                in_dns = False
            elif in_dns and stripped.startswith("set primary ") or in_dns and stripped.startswith("set secondary "):
                server = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]
                if ast.dns is None:
                    ast.dns = UniversalDNS()
                ast.dns.servers.append(server)

    def _parse_ntp(self, ast: NetworkAST, lines: list[str]):
        in_ntp = False
        for line in lines:
            stripped = line.strip()
            if stripped == "config system ntp":
                in_ntp = True
            elif in_ntp and stripped == "end":
                in_ntp = False
            elif in_ntp and stripped.startswith("set ntpsync "):
                ast.system.ntp_enabled = stripped.split(" ", 2)[2].strip().lower() == "enable"
            elif in_ntp and stripped.startswith("set server "):
                parts = stripped.split('"')
                if len(parts) >= 2:
                    ast.system.ntp_servers.append(parts[1])

    def _parse_syslog(self, ast: NetworkAST, lines: list[str]):
        in_syslog = False
        for line in lines:
            stripped = line.strip()
            if stripped == "config log syslogd setting":
                in_syslog = True
            elif in_syslog and stripped == "end":
                in_syslog = False
            elif in_syslog and stripped.startswith("set status "):
                ast.system.logging_enabled = stripped.split(" ", 2)[2].strip().lower() == "enable"
            elif in_syslog and stripped.startswith("set server "):
                server = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]
                ast.vendor_specific.setdefault("syslog_servers", []).append(server)

    def _parse_firewall_policies(self, ast: NetworkAST, lines: list[str]):
        in_policy = False
        policy_id = None
        current_rule = None
        for line in lines:
            stripped = line.strip()
            if stripped == "config firewall policy":
                in_policy = True
            elif in_policy and stripped == "end":
                in_policy = False
            elif in_policy and stripped.startswith("edit "):
                policy_id = stripped.split(" ", 1)[1]
                current_rule = UniversalFirewallRule(
                    id=policy_id,
                    chain="INPUT",
                )
                ast.firewall_rules.append(current_rule)
            elif in_policy and current_rule is not None:
                if stripped.startswith("set srcintf "):
                    current_rule.in_interface = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]
                elif stripped.startswith("set dstintf "):
                    current_rule.out_interface = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]
                elif stripped.startswith("set srcaddr "):
                    current_rule.src_address = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]
                elif stripped.startswith("set dstaddr "):
                    current_rule.dst_address = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]
                elif stripped.startswith("set action "):
                    action_str = stripped.split(" ", 2)[2].strip()
                    current_rule.action = RuleAction.ACCEPT if action_str == "accept" else RuleAction.DROP
                elif stripped.startswith("set service "):
                    current_rule.protocol = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]
                elif stripped.startswith("set schedule "):
                    current_rule.vendor_specific["schedule"] = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]
                elif stripped.startswith("set logtraffic "):
                    current_rule.vendor_specific["logtraffic"] = stripped.split(" ", 2)[2]

    def _parse_vpn(self, ast: NetworkAST, lines: list[str]):
        in_phase1 = False
        in_phase2 = False
        current_vpn = None
        for line in lines:
            stripped = line.strip()
            if stripped == "config vpn ipsec phase1-interface":
                in_phase1 = True
                in_phase2 = False
            elif in_phase1 and stripped == "end":
                in_phase1 = False
            elif stripped == "config vpn ipsec phase2-interface":
                in_phase2 = True
                in_phase1 = False
            elif in_phase2 and stripped == "end":
                in_phase2 = False
            elif (in_phase1 or in_phase2) and stripped.startswith("edit "):
                vpn_name = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 1)[1]
                current_vpn = UniversalVPN(
                    name=vpn_name,
                    type="ipsec",
                    enabled=True,
                )
                ast.vpns.append(current_vpn)
            elif in_phase1 and current_vpn is not None:
                if stripped.startswith("set remote-gw "):
                    current_vpn.peer = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]
                elif stripped.startswith("set psksecret "):
                    current_vpn.pre_shared_key = stripped.split('"')[1] if '"' in stripped else ""
            elif in_phase2 and current_vpn is not None:
                if stripped.startswith("set dst-addr "):
                    current_vpn.remote_address = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]

    def _parse_users(self, ast: NetworkAST, lines: list[str]):
        in_users = False
        current_user = None
        for line in lines:
            stripped = line.strip()
            if stripped == "config system local":
                in_users = True
            elif in_users and stripped == "end":
                in_users = False
            elif in_users and stripped.startswith("edit "):
                user_name = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 1)[1]
                current_user = UniversalUser(name=user_name)
                ast.users.append(current_user)
            elif in_users and current_user is not None:
                if stripped.startswith("set type "):
                    current_user.vendor_specific["type"] = stripped.split(" ", 2)[2]
                elif stripped.startswith("set passwd "):
                    current_user.vendor_specific["has_password"] = True

    def _parse_ha(self, ast: NetworkAST, lines: list[str]):
        in_ha = False
        for line in lines:
            stripped = line.strip()
            if stripped == "config system ha":
                in_ha = True
            elif in_ha and stripped == "end":
                in_ha = False
            elif in_ha and stripped.startswith("set mode "):
                ast.vendor_specific["ha_mode"] = stripped.split(" ", 2)[2]
            elif in_ha and stripped.startswith("set group-name "):
                ast.vendor_specific["ha_group"] = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]
            elif in_ha and stripped.startswith("set priority "):
                try:
                    ast.vendor_specific["ha_priority"] = int(stripped.split(" ", 2)[2])
                except (ValueError, IndexError):
                    pass

    def _parse_nat(self, ast: NetworkAST, lines: list[str]):
        for line in lines:
            stripped = line.strip()
            if "nat" in stripped.lower() and "enable" in stripped.lower():
                ast.nat_rules.append(UniversalNATRule(
                    chain="srcnat",
                    action=RuleAction.MASQUERADE,
                ))

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
            lines.append(f"    edit \"{iface.name}\"")
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
