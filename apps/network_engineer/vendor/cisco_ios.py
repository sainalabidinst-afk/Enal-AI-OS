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

logger = logging.getLogger(__name__)


class CiscoIOSAdapter(VendorAdapter):
    """Full Cisco IOS/IOS-XE/NX-OS adapter."""

    vendor_name = "cisco"
    vendor_versions = ["ios", "ios-xe", "nx-os"]

    def detect(self, config_text: str) -> bool:
        """Detect Cisco IOS config."""
        indicators = [
            "interface GigabitEthernet",
            "interface FastEthernet",
            "interface TenGigabitEthernet",
            "interface Dot11Radio",
            "interface BVI",
            "access-list ",
            "ip nat inside source",
            "line vty",
            "enable password",
            "router bgp ",
            "ip route ",
            "dot11 ssid",
            "ssid ",
            "switchport mode",
            "vlan ",
            "policy-map",
            "class-map",
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

        self._parse_system(ast, lines)
        self._parse_interfaces(ast, lines)
        self._parse_vlans(ast, lines)
        self._parse_ip_addresses(ast, lines)
        self._parse_routes(ast, lines)
        self._parse_acls(ast, lines)
        self._parse_nat(ast, lines)
        self._parse_dhcp(ast, lines)
        self._parse_hsrp(ast, lines)
        self._parse_ospf(ast, lines)
        self._parse_bgp(ast, lines)
        self._parse_aaa(ast, lines)
        self._parse_snmp(ast, lines)
        self._parse_ntp(ast, lines)
        self._parse_logging(ast, lines)
        self._parse_ssh_telnet(ast, lines)
        self._parse_users(ast, lines)
        self._parse_enable(ast, lines)
        self._parse_dns(ast, lines)
        self._parse_spanning_tree(ast, lines)
        ast.raw_lines = [line for line in lines if line.strip() and not line.strip().startswith("!")]
        return ast

    def _parse_system(self, ast: NetworkAST, lines: list[str]):
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("hostname "):
                ast.system.hostname = stripped.split(" ", 1)[1]
            elif stripped.startswith("ip domain-name "):
                pass

    def _parse_interfaces(self, ast: NetworkAST, lines: list[str]):
        current_iface = None
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("interface "):
                iface_name = stripped.split(" ", 1)[1]
                iface = UniversalInterface(
                    name=iface_name,
                    type=InterfaceType.ETHERNET,
                )
                ast.interfaces.append(iface)
                current_iface = iface
            elif current_iface is not None:
                if stripped.startswith("description "):
                    current_iface.comment = stripped.split(" ", 1)[1]
                elif stripped.startswith("mtu "):
                    try:
                        current_iface.mtu = int(stripped.split(" ", 1)[1])
                    except (ValueError, IndexError):
                        pass
                elif stripped == "shutdown":
                    current_iface.status = "disabled"
                elif stripped == "no shutdown":
                    current_iface.status = "enabled"
                elif stripped.startswith(("speed ", "duplex ")):
                    pass
                elif stripped.startswith("mac-address "):
                    current_iface.mac_address = stripped.split(" ", 1)[1]
                elif stripped.startswith("switchport mode "):
                    current_iface.vendor_specific["switchport_mode"] = stripped.split(" ", 2)[2]
                elif stripped.startswith("switchport access vlan "):
                    try:
                        vlan_id = int(stripped.split(" ", 4)[4])
                        current_iface.vendor_specific["access_vlan"] = vlan_id
                    except (ValueError, IndexError):
                        pass

    def _parse_vlans(self, ast: NetworkAST, lines: list[str]):
        in_vlan = False
        current_vlan = None
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("vlan "):
                in_vlan = True
                vlan_id_str = stripped.split(" ", 1)[1]
                try:
                    vlan_id = int(vlan_id_str)
                    current_vlan = UniversalVLAN(id=vlan_id)
                    ast.vlans.append(current_vlan)
                except ValueError:
                    current_vlan = None
            elif in_vlan and current_vlan is not None:
                if stripped.startswith("name "):
                    current_vlan.name = stripped.split(" ", 1)[1]
                elif stripped.startswith("!"):
                    in_vlan = False
                    current_vlan = None

    def _parse_ip_addresses(self, ast: NetworkAST, lines: list[str]):
        current_iface = None
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("interface "):
                current_iface = stripped.split(" ", 1)[1]
            elif stripped.startswith("ip address ") and current_iface:
                parts = stripped.split()
                if len(parts) >= 4:
                    ip = parts[2]
                    mask = parts[3]
                    ast.ip_addresses.append(UniversalIPAddress(
                        address=f"{ip}/{mask}",
                        interface=current_iface,
                    ))

    def _parse_routes(self, ast: NetworkAST, lines: list[str]):
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("ip route "):
                parts = stripped.split()
                if len(parts) >= 5:
                    dst = parts[2]
                    mask = parts[3]
                    gateway = parts[4]
                    distance = 1
                    if len(parts) >= 6:
                        try:
                            distance = int(parts[5])
                        except ValueError:
                            pass
                    prefix = self._mask_to_prefix(mask)
                    ast.routes.append(UniversalRoute(
                        destination=f"{dst}/{prefix}",
                        gateway=gateway,
                        distance=distance,
                    ))

    @staticmethod
    def _mask_to_prefix(mask: str) -> str:
        binary = sum(int(o).bit_count() for o in mask.split("."))
        return str(binary)

    def _parse_acls(self, ast: NetworkAST, lines: list[str]):
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(("access-list ", "ip access-list ")):
                parts = stripped.split()
                if len(parts) >= 4:
                    action = RuleAction.ACCEPT if parts[2].lower() == "permit" else RuleAction.DROP
                    chain = "INPUT"
                    if "input" in stripped.lower():
                        chain = "INPUT"
                    elif "output" in stripped.lower():
                        chain = "OUTPUT"
                    else:
                        chain = "FORWARD"
                    ast.firewall_rules.append(UniversalFirewallRule(
                        id=parts[1],
                        chain=chain,
                        action=action,
                        protocol=parts[3] if len(parts) > 3 else "",
                    ))

    def _parse_nat(self, ast: NetworkAST, lines: list[str]):
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("ip nat inside source "):
                if "static" in stripped:
                    parts = stripped.split()
                    to_addr = ""
                    for i, p in enumerate(parts):
                        if p == "address" and i + 1 < len(parts):
                            to_addr = parts[i + 1]
                    ast.nat_rules.append(UniversalNATRule(
                        chain="srcnat",
                        action=RuleAction.SNAT,
                        to_address=to_addr,
                    ))
                elif "list" in stripped:
                    parts = stripped.split()
                    out_interface = ""
                    for i, p in enumerate(parts):
                        if p == "interface" and i + 1 < len(parts):
                            out_interface = parts[i + 1]
                            break
                    ast.nat_rules.append(UniversalNATRule(
                        chain="srcnat",
                        action=RuleAction.MASQUERADE,
                        out_interface=out_interface,
                    ))

    def _parse_dhcp(self, ast: NetworkAST, lines: list[str]):
        in_dhcp = False
        current_pool = None
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("ip dhcp pool "):
                in_dhcp = True
                pool_name = stripped.split(" ", 3)[3]
                current_pool = UniversalDHCPServer(name=pool_name)
                ast.dhcp_servers.append(current_pool)
            elif in_dhcp and current_pool is not None:
                if stripped.startswith("network "):
                    parts = stripped.split()
                    if len(parts) >= 3:
                        current_pool.address_pool = f"{parts[1]}/{parts[2]}"
                elif stripped.startswith("default-router "):
                    current_pool.vendor_specific["default_router"] = stripped.split(" ", 1)[1]
                elif stripped.startswith("dns-server "):
                    current_pool.vendor_specific["dns_server"] = stripped.split(" ", 1)[1]
                elif stripped.startswith("lease "):
                    current_pool.lease_time = stripped.split(" ", 1)[1]
                elif stripped.startswith("!"):
                    in_dhcp = False
                    current_pool = None

    def _parse_hsrp(self, ast: NetworkAST, lines: list[str]):
        current_iface = None
        current_group = None
        in_hsrp = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("interface "):
                current_iface = stripped.split(" ", 1)[1]
                in_hsrp = False
            elif current_iface and stripped.startswith("standby "):
                parts = stripped.split()
                if len(parts) >= 2 and parts[1].isdigit():
                    current_group = parts[1]
                    in_hsrp = True
                if len(parts) >= 4 and parts[2] == "ip":
                    ast.vendor_specific.setdefault("hsrp", {})[
                        f"{current_iface}_{current_group}"
                    ] = parts[3]
                elif len(parts) >= 4 and parts[2] == "priority":
                    ast.vendor_specific.setdefault("hsrp_priority", {})[
                        f"{current_iface}_{current_group}"
                    ] = parts[3]
            elif in_hsrp and current_group:
                if stripped.startswith("ip ") and "address" in stripped:
                    ast.vendor_specific.setdefault("hsrp", {})[
                        f"{current_iface}_{current_group}"
                    ] = stripped.split(" ", 3)[3] if len(stripped.split()) >= 4 else ""
                elif stripped.startswith("priority "):
                    ast.vendor_specific.setdefault("hsrp_priority", {})[
                        f"{current_iface}_{current_group}"
                    ] = stripped.split(" ", 1)[1]
                elif stripped == "!" or stripped.startswith("username "):
                    in_hsrp = False
                    current_group = None
        in_hsrp = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("interface "):
                current_iface = stripped.split(" ", 1)[1]
                in_hsrp = False
            elif current_iface and stripped.startswith("standby "):
                in_hsrp = True
                parts = stripped.split()
                if len(parts) >= 2 and parts[1].isdigit():
                    current_group = parts[1]
            elif in_hsrp and current_group:
                if stripped.startswith("ip "):
                    if "address" in stripped:
                        ast.vendor_specific.setdefault("hsrp", {})[
                            f"{current_iface}_{current_group}"
                        ] = stripped.split(" ", 2)[2]
                elif stripped.startswith("priority "):
                    ast.vendor_specific.setdefault("hsrp_priority", {})[
                        f"{current_iface}_{current_group}"
                    ] = stripped.split(" ", 1)[1]
                elif stripped.startswith("!"):
                    in_hsrp = False
                    current_group = None

    def _parse_ospf(self, ast: NetworkAST, lines: list[str]):
        in_ospf = False
        ospf_process = ""
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("router ospf "):
                in_ospf = True
                ospf_process = stripped.split(" ", 2)[2]
            elif in_ospf:
                if stripped.startswith("network "):
                    parts = stripped.split()
                    if len(parts) >= 4:
                        ast.vendor_specific.setdefault("ospf", {}).setdefault("networks", []).append({
                            "process": ospf_process,
                            "network": parts[1],
                            "wildcard": parts[2],
                            "area": parts[3],
                        })
                elif stripped.startswith("area "):
                    pass
                elif stripped and not stripped.startswith(" ") and not stripped.startswith("router"):
                    in_ospf = False

    def _parse_bgp(self, ast: NetworkAST, lines: list[str]):
        bgp_section = False
        bgp_as = 0
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("router bgp "):
                bgp_section = True
                try:
                    bgp_as = int(stripped.split(" ", 2)[2])
                except (ValueError, IndexError):
                    pass
            elif bgp_section and stripped.startswith("neighbor "):
                parts = stripped.split()
                if len(parts) >= 4:
                    if ast.bgp is None:
                        ast.bgp = UniversalBGP(
                            local_as=bgp_as,
                            enabled=True,
                        )
                    ast.bgp.neighbors.append({
                        "address": parts[1],
                        "remote_as": parts[3],
                    })
            elif bgp_section and stripped.startswith("network "):
                if ast.bgp is None:
                    ast.bgp = UniversalBGP(local_as=bgp_as, enabled=True)
                ast.bgp.networks.append(stripped.split(" ", 1)[1])
            elif stripped and not stripped.startswith(" ") and not stripped.startswith("router"):
                bgp_section = False

    def _parse_aaa(self, ast: NetworkAST, lines: list[str]):
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("aaa new-model"):
                ast.vendor_specific["aaa_new_model"] = True
            elif stripped.startswith("aaa authentication "):
                parts = stripped.split()
                if len(parts) >= 4:
                    ast.vendor_specific.setdefault("aaa_authentication", []).append({
                        "type": parts[2],
                        "method": parts[3],
                    })

    def _parse_snmp(self, ast: NetworkAST, lines: list[str]):
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("snmp-server community "):
                parts = stripped.split()
                if len(parts) >= 3:
                    ast.vendor_specific["snmp_community"] = parts[2]

    def _parse_ntp(self, ast: NetworkAST, lines: list[str]):
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("ntp server "):
                ast.system.ntp_enabled = True
                server = stripped.split(" ", 2)[2]
                ast.system.ntp_servers.append(server)

    def _parse_logging(self, ast: NetworkAST, lines: list[str]):
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("logging "):
                ast.system.logging_enabled = True
                parts = stripped.split()
                if len(parts) >= 2 and parts[1] != "on" and parts[1] != "console" and parts[1] != "monitor":
                    ast.vendor_specific["logging_host"] = parts[1]
                break

    def _parse_ssh_telnet(self, ast: NetworkAST, lines: list[str]):
        in_line_vty = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("line vty "):
                in_line_vty = True
            elif in_line_vty:
                if stripped == "transport input ssh":
                    ast.vendor_specific["vty_ssh"] = True
                elif stripped == "transport input telnet":
                    ast.vendor_specific["vty_telnet"] = True
                elif stripped == "login local":
                    ast.vendor_specific["vty_login_local"] = True
                elif stripped == "exec-timeout ":
                    pass
                elif stripped == "!" or stripped.startswith("line "):
                    in_line_vty = False

    def _parse_users(self, ast: NetworkAST, lines: list[str]):
        in_username = False
        current_user = None
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("username "):
                in_username = True
                parts = stripped.split()
                if len(parts) >= 2:
                    current_user = UniversalUser(name=parts[1])
                    ast.users.append(current_user)
            elif in_username and current_user is not None:
                if stripped.startswith("privilege "):
                    try:
                        current_user.vendor_specific["privilege"] = int(stripped.split(" ", 1)[1])
                    except (ValueError, IndexError):
                        pass
                elif stripped.startswith("secret "):
                    current_user.vendor_specific["secret_type"] = stripped.split(" ", 1)[1].split(" ")[0] if " " in stripped else ""
                elif stripped == "!" or stripped.startswith("username "):
                    in_username = False
                    current_user = None

    def _parse_enable(self, ast: NetworkAST, lines: list[str]):
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("enable password "):
                parts = stripped.split(" ", 2)
                if len(parts) >= 3:
                    ast.vendor_specific["enable_password"] = parts[2]
            elif stripped.startswith("enable secret "):
                parts = stripped.split(" ", 2)
                if len(parts) >= 3:
                    ast.vendor_specific["enable_secret"] = parts[2]

    def _parse_dns(self, ast: NetworkAST, lines: list[str]):
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("ip name-server "):
                servers = stripped.split(" ", 2)[2].split()
                if ast.dns is None:
                    from apps.network_engineer.vendor.models import UniversalDNS
                    ast.dns = UniversalDNS()
                ast.dns.servers.extend(servers)
                ast.dns.allow_remote = True

    def _parse_spanning_tree(self, ast: NetworkAST, lines: list[str]):
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("spanning-tree mode "):
                ast.vendor_specific["stp_mode"] = stripped.split(" ", 2)[2]
            elif stripped.startswith("spanning-tree vlan "):
                parts = stripped.split()
                if len(parts) >= 4 and parts[2] == "priority":
                    ast.vendor_specific.setdefault("stp_vlan_priority", []).append({
                        "vlan": parts[1],
                        "priority": parts[3],
                    })

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
