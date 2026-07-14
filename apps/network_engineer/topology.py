"""
Network Topology Model
========================

Represents network topology as a graph of devices, interfaces, and connections.
"""

import logging
from dataclasses import dataclass, field
from typing import Any
from enum import Enum

logger = logging.getLogger(__name__)


class DeviceType(str, Enum):
    ROUTER = "router"
    SWITCH = "switch"
    FIREWALL = "firewall"
    ACCESS_POINT = "access_point"
    SERVER = "server"
    CLOUD = "cloud"
    END_DEVICE = "end_device"


class InterfaceType(str, Enum):
    ETHERNET = "ethernet"
    WIRELESS = "wireless"
    VLAN = "vlan"
    BRIDGE = "bridge"
    PPP = "ppp"
    TUNNEL = "tunnel"


@dataclass
class NetworkInterface:
    name: str
    interface_type: InterfaceType
    ip_address: str = ""
    mac_address: str = ""
    bandwidth: str = ""
    vlan_id: int | None = None
    comment: str = ""


@dataclass
class NetworkDevice:
    id: str
    name: str
    device_type: DeviceType
    model: str = ""
    firmware_version: str = ""
    interfaces: list[NetworkInterface] = field(default_factory=list)
    configuration: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class NetworkConnection:
    source_device: str
    source_interface: str
    target_device: str
    target_interface: str
    connection_type: str = "ethernet"
    bandwidth: str = "1Gbps"
    latency: str = "0ms"


@dataclass
class NetworkTopology:
    devices: dict[str, NetworkDevice] = field(default_factory=dict)
    connections: list[NetworkConnection] = field(default_factory=list)

    def add_device(self, device: NetworkDevice) -> str:
        self.devices[device.id] = device
        return device.id

    def add_connection(self, connection: NetworkConnection) -> str:
        self.connections.append(connection)
        return f"{connection.source_device}:{connection.source_interface} -> {connection.target_device}:{connection.target_interface}"

    def get_device(self, device_id: str) -> NetworkDevice | None:
        return self.devices.get(device_id)

    def get_connections(self, device_id: str) -> list[NetworkConnection]:
        return [c for c in self.connections if c.source_device == device_id or c.target_device == device_id]
