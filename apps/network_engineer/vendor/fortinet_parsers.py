"""
Fortinet FortiOS Parser Functions
====================================

Standalone parser functions for FortiOS configuration.
"""

from apps.network_engineer.vendor.models import (
    NetworkAST,
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


def parse_system(ast: NetworkAST, lines: list[str]):
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


def parse_interfaces(ast: NetworkAST, lines: list[str]):
    from apps.network_engineer.vendor.models import InterfaceType
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


def parse_vlans(ast: NetworkAST, lines: list[str]):
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


def parse_routes(ast: NetworkAST, lines: list[str]):
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


def parse_dhcp(ast: NetworkAST, lines: list[str]):
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


def parse_dns(ast: NetworkAST, lines: list[str]):
    in_dns = False
    for line in lines:
        stripped = line.strip()
        if stripped == "config system dns":
            in_dns = True
        elif in_dns and stripped == "end":
            in_dns = False
        elif in_dns and (stripped.startswith("set primary ") or stripped.startswith("set secondary ")):
            server = stripped.split('"')[1] if '"' in stripped else stripped.split(" ", 2)[2]
            if ast.dns is None:
                ast.dns = UniversalDNS()
            ast.dns.servers.append(server)


def parse_ntp(ast: NetworkAST, lines: list[str]):
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


def parse_syslog(ast: NetworkAST, lines: list[str]):
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


def parse_firewall_policies(ast: NetworkAST, lines: list[str]):
    from apps.network_engineer.vendor.models import RuleAction
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


def parse_vpn(ast: NetworkAST, lines: list[str]):
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


def parse_users(ast: NetworkAST, lines: list[str]):
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


def parse_ha(ast: NetworkAST, lines: list[str]):
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


def parse_nat(ast: NetworkAST, lines: list[str]):
    from apps.network_engineer.vendor.models import RuleAction
    for line in lines:
        stripped = line.strip()
        if "nat" in stripped.lower() and "enable" in stripped.lower():
            ast.nat_rules.append(UniversalNATRule(
                chain="srcnat",
                action=RuleAction.MASQUERADE,
            ))
