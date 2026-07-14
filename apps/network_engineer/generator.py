"""
RouterOS Configuration Generator
===================================

Generates RouterOS configurations from natural language or structured requirements.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class RouterOSGenerator:
    """Generates RouterOS configurations."""

    def __init__(self):
        self._templates = {
            "hotspot": self._generate_hotspot_template,
            "vlan": self._generate_vlan_template,
            "firewall": self._generate_firewall_template,
            "dhcp": self._generate_dhcp_template,
            "qos": self._generate_qos_template,
        }

    async def generate(self, requirements: dict[str, Any]) -> str:
        """Generate RouterOS configuration from requirements."""
        config_type = requirements.get("type", "general")
        generator = self._templates.get(config_type, self._generate_general_template)
        return await generator(requirements)

    async def _generate_general_template(self, requirements: dict[str, Any]) -> str:
        """Generate general RouterOS configuration."""
        return """# Generated RouterOS Configuration
/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan1

/ip address
add address=192.168.1.1/24 interface=lan1 network=192.168.1.0

/ip pool
add name=dhcp-pool ranges=192.168.1.100-192.168.1.200

/ip dhcp-server
add name=dhcp1 interface=lan1 address-pool=dhcp-pool lease-time=12h

/ip dhcp-server network
add address=192.168.1.0/24 gateway=192.168.1.1 dns-nameserver=8.8.8.8,1.1.1.1

/ip firewall nat
add chain=srcnat out-interface=wan action=masquerade

/ip firewall filter
add action=accept chain=input protocol=icmp comment="Allow ICMP"
add action=accept chain=input connection-state=established,related comment="Allow established"
add action=drop chain=input comment="Drop everything else"

/system identity
set name=Generated-Router
"""

    async def _generate_hotspot_template(self, requirements: dict[str, Any]) -> str:
        """Generate hotspot configuration."""
        interface = requirements.get("interface", "ether1")
        network = requirements.get("network", "192.168.88.0/24")
        pool = requirements.get("pool", "192.168.88.10-192.168.88.254")

        config = f"""# Hotspot Configuration
/ip hotspot
add name=hotspot1 interface={interface} address-pool=pool1 profile=default

/ip pool
add name=pool1 ranges={pool}

/ip dhcp-server
add name=dhcp1 interface={interface} address-pool=pool1 lease-time=12h

/ip hotspot profile
add name=default dns-name=hotspot.local hotspot-address={network}

/ip firewall nat
add chain=srcnat src-address={network} out-interface=ether0 action=masquerade
"""
        return config

    async def _generate_vlan_template(self, requirements: dict[str, Any]) -> str:
        """Generate VLAN configuration."""
        vlans = requirements.get("vlans", [])
        config = "# VLAN Configuration\n"

        for vlan in vlans:
            vlan_id = vlan.get("id", 10)
            name = vlan.get("name", f"vlan{vlan_id}")
            interface = vlan.get("interface", "bridge")
            config += f"/interface bridge vlan\nadd bridge={interface} tagged={interface} vlan-ids={vlan_id} comment={name}\n"

        return config

    async def _generate_firewall_template(self, requirements: dict[str, Any]) -> str:
        """Generate firewall configuration."""
        config = "# Firewall Configuration\n"

        config += "/ip firewall filter\n"
        config += "add chain=input action=accept protocol=icmp comment=\"Allow ICMP\"\n"
        config += "add chain=input action=accept connection-state=established,related comment=\"Allow established\"\n"
        config += "add chain=input action=drop comment=\"Drop everything else\"\n"

        return config

    async def _generate_dhcp_template(self, requirements: dict[str, Any]) -> str:
        """Generate DHCP configuration."""
        interface = requirements.get("interface", "bridge")
        pool = requirements.get("pool", "192.168.88.10-192.168.88.254")
        gateway = requirements.get("gateway", "192.168.88.1")

        config = f"""# DHCP Configuration
/ip pool
add name=dhcp-pool ranges={pool}

/ip dhcp-server
add name=dhcp1 interface={interface} address-pool=dhcp-pool lease-time=12h

/ip dhcp-server network
add address={gateway}/24 gateway={gateway} dns-nameserver=8.8.8.8,8.8.4.4
"""
        return config

    async def _generate_qos_template(self, requirements: dict[str, Any]) -> str:
        """Generate QoS configuration."""
        return "# QoS Configuration\n/queue tree\nadd name=default parent=global priority=8"


routeros_generator = RouterOSGenerator()
