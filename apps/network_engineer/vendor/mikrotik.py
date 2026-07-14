"""
MikroTik Vendor Adapter
========================

Converts RouterOS configs to/from Universal AST.
"""

import logging
from typing import Any

from apps.network_engineer.vendor.base import VendorAdapter
from apps.network_engineer.vendor.models import (
    NetworkAST,
    UniversalInterface,
    UniversalIPAddress,
    UniversalFirewallRule,
    UniversalNATRule,
    UniversalRoute,
    UniversalDHCPServer,
    UniversalHotspot,
    UniversalDNS,
    UniversalBridge,
    UniversalQueue,
    UniversalSystem,
    InterfaceType,
    RuleAction,
)
from apps.network_engineer.mikrotik.routeros_parser import RouterOSParser, RouterOSConfig

logger = logging.getLogger(__name__)


class MikroTikAdapter(VendorAdapter):
    """MikroTik RouterOS adapter."""

    vendor_name = "mikrotik"
    vendor_versions = ["v6", "v7"]

    def detect(self, config_text: str) -> bool:
        """Detect RouterOS config."""
        indicators = [
            "/interface ",
            "/ip address",
            "/ip firewall",
            "/ip dhcp-server",
            "/system identity",
            "/ip pool",
        ]
        return any(indicator in config_text for indicator in indicators)

    def parse(self, config_text: str) -> NetworkAST:
        """Parse RouterOS config into Universal AST."""
        parser = RouterOSParser()
        config = parser.parse(config_text)

        ast = NetworkAST(
            vendor="mikrotik",
            device_id=config.system_identity.name if config.system_identity else "router",
        )

        # System
        if config.system_identity:
            ast.system = UniversalSystem(
                hostname=config.system_identity.name,
                backup_configured=config.metadata.get("backup_configured", False),
            )

        # Interfaces
        for iface in config.interfaces:
            ast.interfaces.append(UniversalInterface(
                name=iface.name,
                type=InterfaceType.ETHERNET,
                mac_address=iface.mac_address,
                comment=iface.comment,
                vendor_specific={"disabled": iface.disabled},
            ))

        # IP Addresses
        for ip in config.ip_addresses:
            ast.ip_addresses.append(UniversalIPAddress(
                address=ip.address,
                network=ip.network,
                interface=ip.interface,
                comment=ip.comment,
            ))

        # Routes
        for route in config.routes:
            ast.routes.append(UniversalRoute(
                destination=route.dst_address,
                gateway=route.gateway,
                distance=int(route.distance) if route.distance else 1,
                comment=route.comment,
            ))

        # Firewall Rules
        for rule in config.firewall_rules:
            action = RuleAction.DROP
            if rule.action.lower() == "accept":
                action = RuleAction.ACCEPT
            elif rule.action.lower() == "masquerade":
                action = RuleAction.MASQUERADE
            elif rule.action.lower() == "fasttrack-connection":
                action = RuleAction.FASTTRACK
            elif rule.action.lower() == "log":
                action = RuleAction.LOG
            elif rule.action.lower() == "return":
                action = RuleAction.RETURN
            elif rule.action.lower() == "jump":
                action = RuleAction.JUMP
            elif rule.action.lower() in ("snat", "srcnat"):
                action = RuleAction.SNAT
            elif rule.action.lower() == "dnat":
                action = RuleAction.DNAT

            ast.firewall_rules.append(UniversalFirewallRule(
                id=f"fw-{len(ast.firewall_rules)}",
                chain=rule.chain,
                action=action,
                src_address=rule.src_address,
                dst_address=rule.dst_address,
                protocol=rule.protocol,
                port=rule.port,
                in_interface=rule.in_interface,
                out_interface=rule.out_interface,
                comment=rule.comment,
            ))

        # NAT Rules
        for rule in config.nat_rules:
            action = RuleAction.MASQUERADE
            if rule.action.lower() == "accept":
                action = RuleAction.ACCEPT
            elif rule.action.lower() == "drop":
                action = RuleAction.DROP
            elif rule.action.lower() == "snat":
                action = RuleAction.SNAT
            elif rule.action.lower() == "dnat":
                action = RuleAction.DNAT

            ast.nat_rules.append(UniversalNATRule(
                id=f"nat-{len(ast.nat_rules)}",
                chain=rule.chain,
                action=action,
                src_address=rule.src_address,
                dst_address=rule.dst_address,
                in_interface=rule.in_interface,
                out_interface=rule.out_interface,
                comment=rule.comment,
            ))

        # DHCP Servers
        for dhcp in config.dhcp_servers:
            ast.dhcp_servers.append(UniversalDHCPServer(
                name=dhcp.name,
                interface=dhcp.interface,
                address_pool=dhcp.address_pool,
                lease_time=dhcp.lease_time,
                comment=dhcp.comment,
            ))

        # Hotspots
        for hs in config.hotspot_configs:
            ast.hotspots.append(UniversalHotspot(
                name=hs.name,
                interface=hs.interface,
                profile=hs.profile,
                comment=hs.comment,
            ))

        # DNS
        if config.dns_config:
            ast.dns = UniversalDNS(
                servers=config.dns_config.servers,
                allow_remote=config.dns_config.allow_remote_requests,
                cache_size=int(config.dns_config.cache_size) if config.dns_config.cache_size else 2048,
            )

        # Bridges
        for bridge in config.bridge_configs:
            ast.bridges.append(UniversalBridge(
                name=bridge.name,
                ports=bridge.ports,
                protocol_mode=bridge.protocol_mode,
                comment=bridge.comment,
            ))

        # Queues
        for queue in config.queue_configs:
            ast.queues.append(UniversalQueue(
                name=queue.name,
                target=queue.target,
                max_limit=queue.max_limit,
                comment=queue.comment,
            ))

        # BGP
        if any("/routing bgp" in line for line in config.raw_lines):
            ast.bgp = UniversalBGP()
            for line in config.raw_lines:
                if line.startswith("/routing bgp"):
                    ast.bgp.enabled = True
                if "router-id=" in line:
                    ast.bgp.router_id = line.split("router-id=")[1].split()[0]
                if "as=" in line:
                    try:
                        ast.bgp.local_as = int(line.split("as=")[1].split()[0])
                    except (ValueError, IndexError):
                        pass

        # MPLS
        if any("/mpls" in line for line in config.raw_lines):
            ast.mpls = UniversalMPLS()
            ast.mpls.enabled = True
            if any("/mpls ldp" in line and "enabled=yes" in line for line in config.raw_lines):
                ast.mpls.ldp_enabled = True
            for line in config.raw_lines:
                if "interface=" in line and "/mpls" in line:
                    ast.mpls.interfaces.append(line.split("interface=")[1].split()[0])

        # CAPsMAN
        if any("/capsman" in line.lower() for line in config.raw_lines):
            ast.capsman = UniversalCAPsMAN()
            ast.capsman.enabled = True
            for line in config.raw_lines:
                if "master-interface=" in line:
                    ast.capsman.interfaces.append(line.split("master-interface=")[1].split()[0])

        # WireGuard
        for line in config.raw_lines:
            if line.startswith("/interface wireguard"):
                if "add" in line:
                    parts = dict(p.split("=", 1) for p in line.split("add ")[1].split() if "=" in p)
                    ast.wireguard.append(UniversalWireGuard(
                        name=parts.get("name", ""),
                        listen_port=int(parts.get("listen-port", "0")),
                        enabled=True,
                    ))

        return ast

    def generate(self, ast: NetworkAST) -> str:
        """Generate RouterOS config from Universal AST."""
        lines = []
        lines.append("# Generated RouterOS Configuration")
        lines.append("")

        # System
        if ast.system.hostname:
            lines.append("/system identity")
            lines.append(f"set name={ast.system.hostname}")
            lines.append("")

        # Interfaces
        if ast.interfaces:
            lines.append("/interface ethernet")
            for iface in ast.interfaces:
                disabled = "yes" if iface.vendor_specific.get("disabled") else "no"
                lines.append(f"set [ find default-name={iface.name} ] name={iface.name} disabled={disabled}")
            lines.append("")

        # Bridges
        for bridge in ast.bridges:
            lines.append("/interface bridge")
            lines.append(f"add name={bridge.name}")
            lines.append("")

        # IP Addresses
        if ast.ip_addresses:
            lines.append("/ip address")
            for ip in ast.ip_addresses:
                lines.append(f"add address={ip.address} interface={ip.interface} network={ip.network}")
            lines.append("")

        # DHCP Servers
        if ast.dhcp_servers:
            lines.append("/ip pool")
            for dhcp in ast.dhcp_servers:
                if dhcp.address_pool:
                    lines.append(f"add name={dhcp.name}_pool ranges={dhcp.address_pool}")
            lines.append("")

            lines.append("/ip dhcp-server")
            for dhcp in ast.dhcp_servers:
                lines.append(f"add name={dhcp.name} interface={dhcp.interface} address-pool={dhcp.name}_pool")
            lines.append("")

        # Firewall Rules
        if ast.firewall_rules:
            lines.append("/ip firewall filter")
            for rule in ast.firewall_rules:
                line = f"add action={rule.action.value} chain={rule.chain}"
                if rule.src_address:
                    line += f" src-address={rule.src_address}"
                if rule.dst_address:
                    line += f" dst-address={rule.dst_address}"
                if rule.protocol:
                    line += f" protocol={rule.protocol}"
                if rule.port:
                    line += f" port={rule.port}"
                if rule.in_interface:
                    line += f" in-interface={rule.in_interface}"
                if rule.out_interface:
                    line += f" out-interface={rule.out_interface}"
                if rule.comment:
                    line += f" comment=\"{rule.comment}\""
                lines.append(line)
            lines.append("")

        # NAT Rules
        if ast.nat_rules:
            lines.append("/ip firewall nat")
            for rule in ast.nat_rules:
                line = f"add action={rule.action.value} chain={rule.chain}"
                if rule.out_interface:
                    line += f" out-interface={rule.out_interface}"
                if rule.comment:
                    line += f" comment=\"{rule.comment}\""
                lines.append(line)
            lines.append("")

        return "\n".join(lines)


mikrotik_adapter = MikroTikAdapter()
