"""
RouterOS Configuration Parser
===============================

Parses RouterOS configuration files (.rsc) into structured data.
"""

import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class ConfigSection(str, Enum):
    INTERFACE = "interface"
    IP_ADDRESS = "ip address"
    IP_FIREWALL = "ip firewall"
    IP_ROUTE = "ip route"
    IP_DHCP_SERVER = "ip dhcp-server"
    IP_HOTSPOT = "ip hotspot"
    IP_DNS = "ip dns"
    SYSTEM = "system"
    TOOL = "tool"
    ROUTING = "routing"
    CERTIFICATE = "certificate"
    USER = "user"
    PPP = "ppp"
    BRIDGE = "bridge"
    VLAN = "vlan"
    QUEUE = "queue"
    NTP = "system ntp"
    LOG = "system log"
    IP_SERVICE = "ip service"


@dataclass
class InterfaceConfig:
    name: str = ""
    type: str = ""
    mac_address: str = ""
    comment: str = ""
    disabled: bool = False


@dataclass
class IPAddressConfig:
    address: str = ""
    network: str = ""
    interface: str = ""
    comment: str = ""


@dataclass
class RouteConfig:
    dst_address: str = ""
    gateway: str = ""
    distance: str = ""
    comment: str = ""


@dataclass
class FirewallFilterRule:
    chain: str = ""
    action: str = ""
    src_address: str = ""
    dst_address: str = ""
    protocol: str = ""
    port: str = ""
    in_interface: str = ""
    out_interface: str = ""
    comment: str = ""


@dataclass
class NATRule:
    chain: str = ""
    action: str = ""
    src_address: str = ""
    dst_address: str = ""
    in_interface: str = ""
    out_interface: str = ""
    comment: str = ""


@dataclass
class DHCPConfig:
    name: str = ""
    interface: str = ""
    address_pool: str = ""
    lease_time: str = ""
    comment: str = ""


@dataclass
class HotspotConfig:
    name: str = ""
    interface: str = ""
    profile: str = ""
    comment: str = ""


@dataclass
class DNSConfig:
    servers: list[str] = field(default_factory=list)
    allow_remote_requests: bool = False
    cache_size: str = ""


@dataclass
class BridgeConfig:
    name: str = ""
    ports: list[str] = field(default_factory=list)
    protocol_mode: str = ""
    comment: str = ""


@dataclass
class QueueConfig:
    name: str = ""
    target: str = ""
    max_limit: str = ""
    comment: str = ""


@dataclass
class SystemIdentity:
    name: str = ""


@dataclass
class RouterOSConfig:
    interfaces: list[InterfaceConfig] = field(default_factory=list)
    ip_addresses: list[IPAddressConfig] = field(default_factory=list)
    routes: list[RouteConfig] = field(default_factory=list)
    firewall_rules: list[FirewallFilterRule] = field(default_factory=list)
    nat_rules: list[NATRule] = field(default_factory=list)
    dhcp_servers: list[DHCPConfig] = field(default_factory=list)
    hotspot_configs: list[HotspotConfig] = field(default_factory=list)
    dns_config: DNSConfig | None = None
    bridge_configs: list[BridgeConfig] = field(default_factory=list)
    queue_configs: list[QueueConfig] = field(default_factory=list)
    system_identity: SystemIdentity | None = None
    raw_lines: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    vendor: str = "mikrotik"


class RouterOSParser:
    """Parser for RouterOS configuration files."""

    def __init__(self):
        self._current_section: ConfigSection | None = None
        self._current_subsection: str | None = None

    def parse(self, content: str) -> RouterOSConfig:
        config = RouterOSConfig()
        lines = content.splitlines()
        config.raw_lines = [line for line in lines if line.strip() and not line.strip().startswith("#")]

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            section_match = re.match(r'^/(.+)$', line)
            if section_match:
                section_name = section_match.group(1).strip()
                parts = section_name.split(" ")
                self._current_section = None
                subsection = None
                for i in range(len(parts), 0, -1):
                    candidate = " ".join(parts[:i])
                    try:
                        self._current_section = ConfigSection(candidate)
                        if i < len(parts):
                            subsection = " ".join(parts[i:])
                        break
                    except ValueError:
                        continue
                self._current_subsection = subsection
                continue

            if self._current_section:
                self._parse_line(config, line)

        config.metadata["parser_version"] = "1.0.0"
        config.metadata["total_lines"] = len(lines)
        config.metadata["non_comment_lines"] = len(config.raw_lines)
        logger.info(
            "Parsed RouterOS config: interfaces=%d, ip_addresses=%d, routes=%d, firewall=%d, nat=%d, dhcp=%d",
            len(config.interfaces), len(config.ip_addresses), len(config.routes),
            len(config.firewall_rules), len(config.nat_rules), len(config.dhcp_servers),
        )
        return config

    def _parse_line(self, config: RouterOSConfig, line: str):
        if self._current_section == ConfigSection.INTERFACE:
            self._parse_interface(config, line)
        elif self._current_section == ConfigSection.IP_ADDRESS:
            self._parse_ip_address(config, line)
        elif self._current_section == ConfigSection.IP_FIREWALL:
            self._parse_firewall(config, line)
        elif self._current_section == ConfigSection.IP_ROUTE:
            self._parse_route(config, line)
        elif self._current_section == ConfigSection.IP_DHCP_SERVER:
            self._parse_dhcp(config, line)
        elif self._current_section == ConfigSection.IP_HOTSPOT:
            self._parse_hotspot(config, line)
        elif self._current_section == ConfigSection.IP_DNS:
            self._parse_dns(config, line)
        elif self._current_section == ConfigSection.BRIDGE:
            self._parse_bridge(config, line)
        elif self._current_section == ConfigSection.QUEUE:
            self._parse_queue(config, line)
        elif self._current_section == ConfigSection.SYSTEM:
            self._parse_system(config, line)
        elif self._current_section == ConfigSection.IP_SERVICE:
            self._parse_ip_service(config, line)

    def _parse_interface(self, config: RouterOSConfig, line: str):
        if line.startswith(("add ", "set ")):
            params = self._parse_params(line.split(" ", 1)[1] if " " in line else "")
            config.interfaces.append(InterfaceConfig(
                name=params.get("name", ""),
                type=params.get("type", ""),
                mac_address=params.get("mac-address", ""),
                comment=params.get("comment", ""),
                disabled=params.get("disabled", "no").lower() == "yes",
            ))

    def _parse_ip_address(self, config: RouterOSConfig, line: str):
        if line.startswith(("add ", "set ")):
            params = self._parse_params(line.split(" ", 1)[1] if " " in line else "")
            config.ip_addresses.append(IPAddressConfig(
                address=params.get("address", ""),
                network=params.get("network", ""),
                interface=params.get("interface", ""),
                comment=params.get("comment", ""),
            ))

    def _parse_route(self, config: RouterOSConfig, line: str):
        if line.startswith(("add ", "set ")):
            params = self._parse_params(line.split(" ", 1)[1] if " " in line else "")
            config.routes.append(RouteConfig(
                dst_address=params.get("dst-address", ""),
                gateway=params.get("gateway", ""),
                distance=params.get("distance", ""),
                comment=params.get("comment", ""),
            ))

    def _parse_firewall(self, config: RouterOSConfig, line: str):
        if line.startswith(("add ", "set ")):
            params = self._parse_params(line.split(" ", 1)[1] if " " in line else "")
            if self._current_subsection == "nat":
                config.nat_rules.append(NATRule(
                    chain=params.get("chain", ""),
                    action=params.get("action", ""),
                    src_address=params.get("src-address", ""),
                    dst_address=params.get("dst-address", ""),
                    out_interface=params.get("out-interface", ""),
                    comment=params.get("comment", ""),
                ))
            else:
                config.firewall_rules.append(FirewallFilterRule(
                    chain=params.get("chain", ""),
                    action=params.get("action", ""),
                    src_address=params.get("src-address", ""),
                    dst_address=params.get("dst-address", ""),
                    protocol=params.get("protocol", ""),
                    port=params.get("port", ""),
                    in_interface=params.get("in-interface", ""),
                    out_interface=params.get("out-interface", ""),
                    comment=params.get("comment", ""),
                ))

    def _parse_dhcp(self, config: RouterOSConfig, line: str):
        if line.startswith(("add ", "set ")):
            params = self._parse_params(line.split(" ", 1)[1] if " " in line else "")
            config.dhcp_servers.append(DHCPConfig(
                name=params.get("name", ""),
                interface=params.get("interface", ""),
                address_pool=params.get("address-pool", ""),
                lease_time=params.get("lease-time", ""),
                comment=params.get("comment", ""),
            ))

    def _parse_hotspot(self, config: RouterOSConfig, line: str):
        if line.startswith(("add ", "set ")):
            params = self._parse_params(line.split(" ", 1)[1] if " " in line else "")
            config.hotspot_configs.append(HotspotConfig(
                name=params.get("name", ""),
                interface=params.get("interface", ""),
                profile=params.get("profile", ""),
                comment=params.get("comment", ""),
            ))

    def _parse_dns(self, config: RouterOSConfig, line: str):
        if line.startswith(("set ", "add ")):
            params = self._parse_params(line.split(" ", 1)[1] if " " in line else "")
            if config.dns_config is None:
                config.dns_config = DNSConfig()
            config.dns_config.servers = [s.strip() for s in params.get("servers", "").split(",") if s.strip()]
            config.dns_config.allow_remote_requests = params.get("allow-remote-requests", "no").lower() == "yes"

    def _parse_bridge(self, config: RouterOSConfig, line: str):
        if line.startswith("add "):
            params = self._parse_params(line[4:])
            bridge = BridgeConfig(
                name=params.get("name", ""),
                ports=[p.strip() for p in params.get("ports", "").split(",") if p.strip()],
                protocol_mode=params.get("protocol-mode", ""),
            )
            config.bridge_configs.append(bridge)

    def _parse_queue(self, config: RouterOSConfig, line: str):
        if line.startswith(("add ", "set ")):
            params = self._parse_params(line.split(" ", 1)[1] if " " in line else "")
            config.queue_configs.append(QueueConfig(
                name=params.get("name", ""),
                target=params.get("target", ""),
                max_limit=params.get("max-limit", ""),
                comment=params.get("comment", ""),
            ))

    def _parse_system(self, config: RouterOSConfig, line: str):
        if line.startswith(("identity set ", "identity add ")):
            params = self._parse_params(line.split(" ", 2)[2] if line.count(" ") >= 2 else "")
            config.system_identity = SystemIdentity(name=params.get("name", ""))

    def _parse_ip_service(self, config: RouterOSConfig, line: str):
        if line.startswith(("set ", "add ")):
            params = self._parse_params(line.split(" ", 1)[1] if " " in line else "")
            config.metadata.setdefault("ip_services", []).append({
                "name": params.get("name", ""),
                "port": params.get("port", ""),
                "address": params.get("address", ""),
                "disabled": params.get("disabled", "no").lower() == "yes",
            })

    def _parse_params(self, line: str) -> dict[str, str]:
        """Parse RouterOS parameter line into dict."""
        params = {}
        pattern = r'(\S+?)=(["\'])([^"\']*)\2|(\S+?)=([^\s;]*)'
        matches = re.findall(pattern, line)
        for match in matches:
            if match[0]:
                params[match[0]] = match[2]
            elif match[3]:
                params[match[3]] = match[4]
        return params


def parse_routeros_config(content: str) -> RouterOSConfig:
    parser = RouterOSParser()
    return parser.parse(content)
