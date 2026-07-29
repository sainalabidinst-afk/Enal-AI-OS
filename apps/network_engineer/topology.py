"""
Network Topology Model
=======================

Represents network topology as a graph of devices, interfaces, and connections.
Supports multi-device topologies for design review and analysis.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class DeviceType(str, Enum):
    ROUTER = "router"
    SWITCH = "switch"
    FIREWALL = "firewall"
    ACCESS_POINT = "access_point"
    SERVER = "server"
    CLOUD = "cloud"
    END_DEVICE = "end_device"
    LOAD_BALANCER = "load_balancer"
    IDS_IPS = "ids_ips"


class InterfaceType(str, Enum):
    ETHERNET = "ethernet"
    WIRELESS = "wireless"
    VLAN = "vlan"
    BRIDGE = "bridge"
    PPP = "ppp"
    TUNNEL = "tunnel"
    LOOPBACK = "loopback"
    VXLAN = "vxlan"
    MANAGEMENT = "management"


class RedundancyRole(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    PASSIVE = "passive"
    NONE = "none"


@dataclass
class NetworkInterface:
    name: str
    interface_type: InterfaceType
    ip_address: str = ""
    mac_address: str = ""
    bandwidth: str = ""
    vlan_id: int | None = None
    comment: str = ""
    redundancy_role: RedundancyRole = RedundancyRole.NONE
    neighbors: list[str] = field(default_factory=list)
    state: str = "enabled"


@dataclass
class NetworkDevice:
    id: str
    name: str
    device_type: DeviceType
    model: str = ""
    firmware_version: str = ""
    vendor: str = ""
    interfaces: list[NetworkInterface] = field(default_factory=list)
    configuration: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    roles: list[str] = field(default_factory=list)
    zone: str = ""


@dataclass
class NetworkConnection:
    source_device: str
    source_interface: str
    target_device: str
    target_interface: str
    connection_type: str = "ethernet"
    bandwidth: str = "1Gbps"
    latency: str = "0ms"
    redundancy_path: bool = False
    protocol: str = ""
    cost: int = 1


@dataclass
class NetworkSegment:
    id: str
    name: str
    cidr: str = ""
    vlan_id: int | None = None
    devices: list[str] = field(default_factory=list)
    purpose: str = ""
    security_level: str = "standard"


@dataclass
class NetworkTopology:
    devices: dict[str, NetworkDevice] = field(default_factory=dict)
    connections: list[NetworkConnection] = field(default_factory=list)
    segments: dict[str, NetworkSegment] = field(default_factory=dict)

    def add_device(self, device: NetworkDevice) -> str:
        self.devices[device.id] = device
        return device.id

    def add_connection(self, connection: NetworkConnection) -> str:
        self.connections.append(connection)
        return f"{connection.source_device}:{connection.source_interface} -> {connection.target_device}:{connection.target_interface}"

    def add_segment(self, segment: NetworkSegment) -> str:
        self.segments[segment.id] = segment
        return segment.id

    def get_device(self, device_id: str) -> NetworkDevice | None:
        return self.devices.get(device_id)

    def get_connections(self, device_id: str) -> list[NetworkConnection]:
        return [c for c in self.connections if c.source_device == device_id or c.target_device == device_id]

    def get_segment(self, segment_id: str) -> NetworkSegment | None:
        return self.segments.get(segment_id)

    def get_device_connections(self, device_id: str) -> list[tuple[NetworkConnection, str]]:
        results = []
        for c in self.connections:
            if c.source_device == device_id:
                results.append((c, "source"))
            elif c.target_device == device_id:
                results.append((c, "target"))
        return results

    def get_redundant_paths(self, source_id: str, target_id: str) -> list[list[NetworkConnection]]:
        """Find all redundant paths between two devices using BFS."""
        if source_id not in self.devices or target_id not in self.devices:
            return []

        adj: dict[str, list[tuple[str, NetworkConnection]]] = {d: [] for d in self.devices}
        for c in self.connections:
            adj[c.source_device].append((c.target_device, c))
            adj[c.target_device].append((c.source_device, c))

        paths: list[list[NetworkConnection]] = []
        visited = set()
        path: list[NetworkConnection] = []

        def dfs(current: str):
            if current == target_id:
                paths.append(list(path))
                return
            visited.add(current)
            for neighbor, conn in adj[current]:
                if neighbor not in visited:
                    path.append(conn)
                    dfs(neighbor)
                    path.pop()
            visited.discard(current)

        dfs(source_id)
        return paths

    def to_dict(self) -> dict[str, Any]:
        return {
            "devices": {
                did: {
                    "id": d.id,
                    "name": d.name,
                    "type": d.device_type.value,
                    "vendor": d.vendor,
                    "model": d.model,
                    "zone": d.zone,
                    "interfaces": [
                        {
                            "name": i.name,
                            "type": i.interface_type.value,
                            "ip_address": i.ip_address,
                            "vlan_id": i.vlan_id,
                            "bandwidth": i.bandwidth,
                            "redundancy_role": i.redundancy_role.value,
                            "state": i.state,
                        }
                        for i in d.interfaces
                    ],
                }
                for did, d in self.devices.items()
            },
            "connections": [
                {
                    "source_device": c.source_device,
                    "source_interface": c.source_interface,
                    "target_device": c.target_device,
                    "target_interface": c.target_interface,
                    "connection_type": c.connection_type,
                    "bandwidth": c.bandwidth,
                    "redundancy_path": c.redundancy_path,
                    "protocol": c.protocol,
                    "cost": c.cost,
                }
                for c in self.connections
            ],
            "segments": {
                sid: {
                    "id": s.id,
                    "name": s.name,
                    "cidr": s.cidr,
                    "vlan_id": s.vlan_id,
                    "purpose": s.purpose,
                    "security_level": s.security_level,
                    "devices": s.devices,
                }
                for sid, s in self.segments.items()
            },
        }
