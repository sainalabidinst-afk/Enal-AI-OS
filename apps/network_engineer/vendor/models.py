"""
Universal Network AST
=====================

Vendor-agnostic data model for network configurations.
All vendor parsers convert their config into this model.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class InterfaceType(str, Enum):
    ETHERNET = "ethernet"
    WIRELESS = "wireless"
    VLAN = "vlan"
    BRIDGE = "bridge"
    PPP = "ppp"
    TUNNEL = "tunnel"
    LOOPBACK = "loopback"
    VPN = "vpn"


class RuleAction(str, Enum):
    ACCEPT = "accept"
    DROP = "drop"
    REJECT = "reject"
    MASQUERADE = "masquerade"
    FASTTRACK = "fasttrack"
    LOG = "log"
    RETURN = "return"
    JUMP = "jump"
    SNAT = "snat"
    DNAT = "dnat"


@dataclass
class UniversalInterface:
    name: str
    type: InterfaceType = InterfaceType.ETHERNET
    mac_address: str = ""
    mtu: int = 1500
    status: str = "enabled"
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalIPAddress:
    address: str = ""
    network: str = ""
    interface: str = ""
    vlan_id: int | None = None
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalFirewallRule:
    id: str = ""
    chain: str = ""
    action: RuleAction = RuleAction.DROP
    src_address: str = ""
    dst_address: str = ""
    protocol: str = ""
    port: str = ""
    in_interface: str = ""
    out_interface: str = ""
    stateful: bool = True
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalNATRule:
    id: str = ""
    chain: str = "srcnat"
    action: RuleAction = RuleAction.MASQUERADE
    src_address: str = ""
    dst_address: str = ""
    in_interface: str = ""
    out_interface: str = ""
    to_address: str = ""
    to_port: str = ""
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalRoute:
    destination: str = ""
    gateway: str = ""
    distance: int = 1
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)

    @property
    def dst_address(self) -> str:
        return self.destination


@dataclass
class UniversalDHCPServer:
    name: str = ""
    interface: str = ""
    address_pool: str = ""
    lease_time: str = "12h"
    enabled: bool = True
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalHotspot:
    name: str = ""
    interface: str = ""
    profile: str = ""
    address_pool: str = ""
    enabled: bool = True
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalDNS:
    servers: list[str] = field(default_factory=list)
    allow_remote: bool = False
    cache_size: int = 2048
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalVPN:
    name: str = ""
    type: str = ""
    peer: str = ""
    local_address: str = ""
    remote_address: str = ""
    pre_shared_key: str = ""
    enabled: bool = True
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalBGP:
    local_as: int = 0
    router_id: str = ""
    neighbors: list[dict[str, str]] = field(default_factory=list)
    networks: list[str] = field(default_factory=list)
    enabled: bool = False
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalMPLS:
    enabled: bool = False
    ldp_enabled: bool = False
    interfaces: list[str] = field(default_factory=list)
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalCAPsMAN:
    enabled: bool = False
    interfaces: list[str] = field(default_factory=list)
    security_profiles: list[dict[str, Any]] = field(default_factory=list)
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalWireGuard:
    name: str = ""
    listen_port: int = 0
    peers: list[dict[str, str]] = field(default_factory=list)
    enabled: bool = False
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalVLAN:
    id: int = 0
    name: str = ""
    interface: str = ""
    tagged_ports: list[str] = field(default_factory=list)
    untagged_ports: list[str] = field(default_factory=list)
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalBridge:
    name: str = ""
    ports: list[str] = field(default_factory=list)
    protocol_mode: str = ""
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalQueue:
    name: str = ""
    target: str = ""
    max_limit: str = ""
    parent: str = ""
    priority: int = 8
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalUser:
    name: str = ""
    group: str = ""
    disabled: bool = False
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalCertificate:
    name: str = ""
    subject: str = ""
    issuer: str = ""
    valid_until: str = ""
    enabled: bool = True
    comment: str = ""
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class UniversalSystem:
    hostname: str = ""
    timezone: str = ""
    ntp_enabled: bool = False
    ntp_servers: list[str] = field(default_factory=list)
    logging_enabled: bool = False
    backup_configured: bool = False
    vendor_specific: dict[str, Any] = field(default_factory=dict)


@dataclass
class NetworkAST:
    """Universal Abstract Syntax Tree for network configurations."""
    vendor: str = ""
    vendor_version: str = ""
    device_id: str = ""
    system: UniversalSystem = field(default_factory=UniversalSystem)
    interfaces: list[UniversalInterface] = field(default_factory=list)
    ip_addresses: list[UniversalIPAddress] = field(default_factory=list)
    routes: list[UniversalRoute] = field(default_factory=list)
    firewall_rules: list[UniversalFirewallRule] = field(default_factory=list)
    nat_rules: list[UniversalNATRule] = field(default_factory=list)
    dhcp_servers: list[UniversalDHCPServer] = field(default_factory=list)
    hotspots: list[UniversalHotspot] = field(default_factory=list)
    dns: UniversalDNS | None = None
    vpns: list[UniversalVPN] = field(default_factory=list)
    vlans: list[UniversalVLAN] = field(default_factory=list)
    bridges: list[UniversalBridge] = field(default_factory=list)
    queues: list[UniversalQueue] = field(default_factory=list)
    users: list[UniversalUser] = field(default_factory=list)
    certificates: list[UniversalCertificate] = field(default_factory=list)
    bgp: UniversalBGP | None = None
    mpls: UniversalMPLS | None = None
    capsman: UniversalCAPsMAN | None = None
    wireguard: list[UniversalWireGuard] = field(default_factory=list)
    raw_lines: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    vendor_specific: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "vendor": self.vendor,
            "vendor_version": self.vendor_version,
            "device_id": self.device_id,
            "system": {
                "hostname": self.system.hostname,
                "timezone": self.system.timezone,
                "ntp_enabled": self.system.ntp_enabled,
                "logging_enabled": self.system.logging_enabled,
                "backup_configured": self.system.backup_configured,
            },
            "interfaces": [
                {
                    "name": i.name,
                    "type": i.type.value,
                    "mac_address": i.mac_address,
                    "mtu": i.mtu,
                    "status": i.status,
                    "comment": i.comment,
                }
                for i in self.interfaces
            ],
            "ip_addresses": [
                {
                    "address": ip.address,
                    "network": ip.network,
                    "interface": ip.interface,
                    "vlan_id": ip.vlan_id,
                    "comment": ip.comment,
                }
                for ip in self.ip_addresses
            ],
            "routes": [
                {
                    "destination": r.destination,
                    "gateway": r.gateway,
                    "interface": "",
                    "distance": r.distance,
                    "comment": r.comment,
                }
                for r in self.routes
            ],
            "firewall_rules": [
                {
                    "id": f.id,
                    "chain": f.chain,
                    "action": f.action.value,
                    "src_address": f.src_address,
                    "dst_address": f.dst_address,
                    "protocol": f.protocol,
                    "port": f.port,
                    "in_interface": f.in_interface,
                    "out_interface": f.out_interface,
                    "stateful": f.stateful,
                    "comment": f.comment,
                }
                for f in self.firewall_rules
            ],
            "nat_rules": [
                {
                    "id": n.id,
                    "chain": n.chain,
                    "action": n.action.value,
                    "src_address": n.src_address,
                    "dst_address": n.dst_address,
                    "in_interface": n.in_interface,
                    "out_interface": n.out_interface,
                    "to_address": n.to_address,
                    "to_port": n.to_port,
                    "comment": n.comment,
                }
                for n in self.nat_rules
            ],
            "dhcp_servers": [
                {
                    "name": d.name,
                    "interface": d.interface,
                    "address_pool": d.address_pool,
                    "lease_time": d.lease_time,
                    "enabled": d.enabled,
                    "comment": d.comment,
                }
                for d in self.dhcp_servers
            ],
            "hotspots": [
                {
                    "name": h.name,
                    "interface": h.interface,
                    "profile": h.profile,
                    "address_pool": h.address_pool,
                    "enabled": h.enabled,
                    "comment": h.comment,
                }
                for h in self.hotspots
            ],
            "dns": {
                "servers": self.dns.servers if self.dns else [],
                "allow_remote": self.dns.allow_remote if self.dns else False,
                "cache_size": self.dns.cache_size if self.dns else 0,
            } if self.dns else None,
            "vpns": [
                {
                    "name": v.name,
                    "type": v.type,
                    "peer": v.peer,
                    "local_address": v.local_address,
                    "remote_address": v.remote_address,
                    "enabled": v.enabled,
                    "comment": v.comment,
                }
                for v in self.vpns
            ],
            "vlans": [
                {
                    "id": v.id,
                    "name": v.name,
                    "interface": v.interface,
                    "tagged_ports": v.tagged_ports,
                    "untagged_ports": v.untagged_ports,
                    "comment": v.comment,
                }
                for v in self.vlans
            ],
            "bridges": [
                {
                    "name": b.name,
                    "ports": b.ports,
                    "protocol_mode": b.protocol_mode,
                    "comment": b.comment,
                }
                for b in self.bridges
            ],
            "queues": [
                {
                    "name": q.name,
                    "target": q.target,
                    "max_limit": q.max_limit,
                    "parent": q.parent,
                    "priority": q.priority,
                    "comment": q.comment,
                }
                for q in self.queues
            ],
            "users": [
                {
                    "name": u.name,
                    "group": u.group,
                    "disabled": u.disabled,
                    "comment": u.comment,
                }
                for u in self.users
            ],
            "certificates": [
                {
                    "name": c.name,
                    "subject": c.subject,
                    "issuer": c.issuer,
                    "valid_until": c.valid_until,
                    "enabled": c.enabled,
                    "comment": c.comment,
                }
                for c in self.certificates
            ],
            "bgp": {
                "local_as": self.bgp.local_as,
                "router_id": self.bgp.router_id,
                "neighbors": self.bgp.neighbors,
                "networks": self.bgp.networks,
                "enabled": self.bgp.enabled,
            } if self.bgp else None,
            "mpls": {
                "enabled": self.mpls.enabled,
                "ldp_enabled": self.mpls.ldp_enabled,
                "interfaces": self.mpls.interfaces,
            } if self.mpls else None,
            "capsman": {
                "enabled": self.capsman.enabled,
                "interfaces": self.capsman.interfaces,
                "security_profiles": self.capsman.security_profiles,
            } if self.capsman else None,
            "wireguard": [
                {
                    "name": w.name,
                    "listen_port": w.listen_port,
                    "peers": w.peers,
                    "enabled": w.enabled,
                    "comment": w.comment,
                }
                for w in self.wireguard
            ],
        }

    # Backward-compatible properties for existing analyzer code
    @property
    def system_identity(self):
        class _Identity:
            def __init__(self, hostname):
                self.name = hostname
        return _Identity(self.system.hostname) if self.system.hostname else None

    @property
    def hotspot_configs(self):
        return self.hotspots

    @property
    def bridge_configs(self):
        return self.bridges

    @property
    def dns_config(self):
        if not self.dns:
            return None
        class _DNSConfig:
            def __init__(self, dns):
                self.servers = dns.servers
                self.allow_remote_requests = dns.allow_remote
                self.cache_size = str(dns.cache_size)
        return _DNSConfig(self.dns)

    @property
    def queue_configs(self):
        return self.queues

    @property
    def errors(self):
        return self.metadata.get("parser_errors", [])
