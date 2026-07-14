"""
Network Documentation Generator
==================================

Generates comprehensive network documentation from configurations and analysis.
"""

import logging
from typing import Any
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class NetworkDocumentation:
    title: str
    topology: str = ""
    ip_plan: str = ""
    firewall_rules: str = ""
    nat_rules: str = ""
    routing: str = ""
    vlan_config: str = ""
    dhcp_config: str = ""
    dns_config: str = ""
    hotspot_config: str = ""
    queue_config: str = ""
    backup: str = ""
    maintenance_guide: str = ""
    executive_summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class NetworkDocGenerator:
    """Generates network documentation."""

    def generate(self, config: Any, analysis: Any | None = None, topology: Any | None = None) -> NetworkDocumentation:
        doc = NetworkDocumentation(
            title=f"Network Configuration Documentation - {config.system_identity.name if config.system_identity else 'Router'}",
            metadata={"generated_at": datetime.utcnow().isoformat()},
        )

        doc.executive_summary = self._generate_executive_summary(config, analysis)
        doc.topology = self._generate_topology_section(topology, config)
        doc.ip_plan = self._generate_ip_plan(config)
        doc.firewall_rules = self._generate_firewall_section(config)
        doc.nat_rules = self._generate_nat_section(config)
        doc.routing = self._generate_routing_section(config)
        doc.dns_config = self._generate_dns_section(config)
        doc.dhcp_config = self._generate_dhcp_section(config)
        doc.hotspot_config = self._generate_hotspot_section(config)
        doc.queue_config = self._generate_queue_section(config)
        doc.backup = self._generate_backup_section()
        doc.maintenance_guide = self._generate_maintenance_guide()

        if analysis:
            doc.metadata["issues_critical"] = analysis.summary.get("critical", 0)
            doc.metadata["issues_warnings"] = analysis.summary.get("warnings", 0)
            doc.metadata["issues_info"] = analysis.summary.get("info", 0)

        return doc

    def _generate_executive_summary(self, config: Any, analysis: Any | None) -> str:
        device_name = config.system_identity.name if config.system_identity else "Router"
        lines = [f"## Executive Summary\n\nDevice: {device_name}\n"]
        if analysis:
            lines.append(f"Total Issues: {analysis.summary.get('total_issues', 0)}\n")
            lines.append(f"- Critical: {analysis.summary.get('critical', 0)}\n")
            lines.append(f"- Warnings: {analysis.summary.get('warnings', 0)}\n")
            lines.append(f"- Info: {analysis.summary.get('info', 0)}\n")
        return "\n".join(lines)

    def _generate_topology_section(self, topology: Any | None, config: Any) -> str:
        lines = ["## Network Topology\n"]
        lines.append(f"- Device: {config.system_identity.name if config.system_identity else 'Router'}\n")
        lines.append(f"- Interfaces: {len(config.interfaces)}\n")
        lines.append(f"- Bridges: {len(config.bridge_configs)}\n")
        if topology:
            lines.append(f"- Connections: {len(topology.connections)}\n")
        lines.append(f"- IP Addresses: {len(config.ip_addresses)}\n")
        lines.append(f"- Routes: {len(config.routes)}\n")
        return "\n".join(lines) + "\n"

    def _generate_ip_plan(self, config: Any) -> str:
        if not config.ip_addresses:
            return "## IP Address Plan\n\nNo IP addresses configured.\n"
        lines = ["## IP Address Plan\n\n| Interface | Address | Network | Comment |\n|-----------|---------|---------|---------|"]
        for ip in config.ip_addresses:
            lines.append(f"| {ip.interface} | {ip.address} | {ip.network} | {ip.comment} |")
        return "\n".join(lines) + "\n"

    def _generate_firewall_section(self, config: Any) -> str:
        if not config.firewall_rules:
            return "## Firewall Rules\n\nNo firewall rules configured.\n"
        lines = ["## Firewall Rules\n\n| Chain | Action | Source | Destination | Protocol | Port | In Interface | Out Interface | Comment |\n|-------|--------|--------|-------------|----------|------|-------------|--------------|---------|"]
        for rule in config.firewall_rules:
            lines.append(f"| {rule.chain} | {rule.action} | {rule.src_address} | {rule.dst_address} | {rule.protocol} | {rule.port} | {rule.in_interface} | {rule.out_interface} | {rule.comment} |")
        return "\n".join(lines) + "\n"

    def _generate_nat_section(self, config: Any) -> str:
        if not config.nat_rules:
            return "## NAT Rules\n\nNo NAT rules configured.\n"
        lines = ["## NAT Rules\n\n| Chain | Action | Source | Destination | Out Interface | Comment |\n|-------|--------|--------|-------------|--------------|---------|"]
        for rule in config.nat_rules:
            lines.append(f"| {rule.chain} | {rule.action} | {rule.src_address} | {rule.dst_address} | {rule.out_interface} | {rule.comment} |")
        return "\n".join(lines) + "\n"

    def _generate_routing_section(self, config: Any) -> str:
        if not config.routes:
            return "## Routing\n\nNo static routes configured.\n"
        lines = ["## Static Routes\n\n| Destination | Gateway | Distance | Comment |\n|-------------|---------|----------|---------|"]
        for route in config.routes:
            lines.append(f"| {route.dst_address} | {route.gateway} | {route.distance} | {route.comment} |")
        return "\n".join(lines) + "\n"

    def _generate_dns_section(self, config: Any) -> str:
        if not config.dns_config:
            return "## DNS Configuration\n\nNo DNS configuration found.\n"
        lines = ["## DNS Configuration\n\n| Setting | Value |\n|---------|-------|"]
        lines.append(f"| Servers | {', '.join(config.dns_config.servers) if config.dns_config.servers else 'None'} |")
        lines.append(f"| Allow Remote Requests | {'Yes' if config.dns_config.allow_remote_requests else 'No'} |")
        lines.append(f"| Cache Size | {config.dns_config.cache_size or 'Default'} |")
        return "\n".join(lines) + "\n"

    def _generate_dhcp_section(self, config: Any) -> str:
        if not config.dhcp_servers:
            return "## DHCP Configuration\n\nNo DHCP servers configured.\n"
        lines = ["## DHCP Configuration\n\n| Name | Interface | Pool | Lease Time | Comment |\n|------|-----------|------|------------|---------|"]
        for dhcp in config.dhcp_servers:
            lines.append(f"| {dhcp.name} | {dhcp.interface} | {dhcp.address_pool} | {dhcp.lease_time} | {dhcp.comment} |")
        return "\n".join(lines) + "\n"

    def _generate_hotspot_section(self, config: Any) -> str:
        if not config.hotspot_configs:
            return "## Hotspot Configuration\n\nNo hotspot configurations found.\n"
        lines = ["## Hotspot Configuration\n\n| Name | Interface | Profile | Comment |\n|------|-----------|---------|---------|"]
        for hs in config.hotspot_configs:
            lines.append(f"| {hs.name} | {hs.interface} | {hs.profile} | {hs.comment} |")
        return "\n".join(lines) + "\n"

    def _generate_queue_section(self, config: Any) -> str:
        if not config.queue_configs:
            return "## Queue Configuration\n\nNo queue configurations found.\n"
        lines = ["## Queue Configuration\n\n| Name | Target | Max Limit | Comment |\n|------|--------|-----------|---------|"]
        for queue in config.queue_configs:
            lines.append(f"| {queue.name} | {queue.target} | {queue.max_limit} | {queue.comment} |")
        return "\n".join(lines) + "\n"

    def _generate_backup_section(self) -> str:
        return """## Backup

### Backup Schedule
- Automatic backups: Daily at 02:00
- Retention: 30 days
- Location: Remote FTP/SFTP

### Restore Procedure
1. Upload backup file to router
2. Run: `/system backup load name=backup.backup`
3. Reboot if necessary
"""

    def _generate_maintenance_guide(self) -> str:
        return """## Maintenance Guide

### Daily Tasks
- Monitor system resources
- Check logs for errors
- Verify backup completion

### Weekly Tasks
- Review firewall logs
- Check for firmware updates
- Verify connectivity

### Monthly Tasks
- Full security audit
- Performance review
- Documentation update
"""

    def to_markdown(self, doc: NetworkDocumentation) -> str:
        sections = [
            f"# {doc.title}\n",
            doc.executive_summary,
            doc.topology,
            doc.ip_plan,
            doc.firewall_rules,
            doc.nat_rules,
            doc.routing,
            doc.dns_config,
            doc.dhcp_config,
            doc.hotspot_config,
            doc.queue_config,
            doc.backup,
            doc.maintenance_guide,
        ]
        return "\n".join(sections)


network_doc_generator = NetworkDocGenerator()
