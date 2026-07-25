"""
Network Topology Builder
=========================

Builds a network graph from parsed RouterOS configuration.
"""

import logging

from apps.network_engineer.mikrotik.routeros_parser import RouterOSConfig
from apps.network_engineer.topology import (
    DeviceType,
    InterfaceType,
    NetworkConnection,
    NetworkDevice,
    NetworkInterface,
    NetworkTopology,
)

logger = logging.getLogger(__name__)


class NetworkGraphBuilder:
    """Builds network topology graph from RouterOS config."""

    def build(self, config: RouterOSConfig) -> NetworkTopology:
        topology = NetworkTopology()
        router = self._build_router(config)
        topology.add_device(router)
        self._link_interfaces(config, router, topology)
        self._link_bridges(config, router, topology)
        return topology

    def _build_router(self, config: RouterOSConfig) -> NetworkDevice:
        name = config.system_identity.name if config.system_identity else "router"
        return NetworkDevice(
            id="router-1",
            name=name,
            device_type=DeviceType.ROUTER,
            interfaces=[
                NetworkInterface(
                    name=iface.name,
                    interface_type=InterfaceType.ETHERNET,
                    comment=iface.comment,
                )
                for iface in config.interfaces
            ],
            configuration={
                "interfaces": len(config.interfaces),
                "ip_addresses": len(config.ip_addresses),
                "routes": len(config.routes),
                "firewall_rules": len(config.firewall_rules),
                "nat_rules": len(config.nat_rules),
                "dhcp_servers": len(config.dhcp_servers),
                "hotspots": len(config.hotspot_configs),
                "dns_servers": len(config.dns_config.servers) if config.dns_config else 0,
                "queues": len(config.queue_configs),
            },
        )

    def _link_interfaces(self, config: RouterOSConfig, router: NetworkDevice, topology: NetworkTopology):
        for ip_addr in config.ip_addresses:
            iface = next((i for i in router.interfaces if i.name == ip_addr.interface), None)
            if iface:
                iface.ip_address = ip_addr.address
                if ip_addr.network:
                    topology.add_connection(NetworkConnection(
                        source_device=router.id,
                        source_interface=iface.name,
                        target_device=f"network-{ip_addr.network}",
                        target_interface="",
                        connection_type="ip-network",
                    ))

    def _link_bridges(self, config: RouterOSConfig, router: NetworkDevice, topology: NetworkTopology):
        for bridge in config.bridge_configs:
            bridge_iface = NetworkInterface(
                name=bridge.name,
                interface_type=InterfaceType.BRIDGE,
                comment=f"Bridge with {len(bridge.ports)} ports",
            )
            router.interfaces.append(bridge_iface)
            for port in bridge.ports:
                topology.add_connection(NetworkConnection(
                    source_device=bridge.name,
                    source_interface="",
                    target_device=router.id,
                    target_interface=port,
                    connection_type="bridge-member",
                ))


network_graph_builder = NetworkGraphBuilder()
