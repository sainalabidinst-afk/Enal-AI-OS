"""
Semantic Configuration Diff Engine
====================================

Produces semantic diffs between configurations, not text diffs.
Shows added/removed/modified rules grouped by category.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class DiffType(str, Enum):
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"
    UNCHANGED = "unchanged"


@dataclass
class DiffEntry:
    category: str
    diff_type: DiffType
    path: str
    before: Any = None
    after: Any = None
    description: str = ""


@dataclass
class SemanticDiff:
    entries: list[DiffEntry] = field(default_factory=list)
    summary: dict[str, int] = field(default_factory=dict)

    def added(self) -> list[DiffEntry]:
        return [e for e in self.entries if e.diff_type == DiffType.ADDED]

    def removed(self) -> list[DiffEntry]:
        return [e for e in self.entries if e.diff_type == DiffType.REMOVED]

    def modified(self) -> list[DiffEntry]:
        return [e for e in self.entries if e.diff_type == DiffType.MODIFIED]

    def to_markdown(self) -> str:
        lines = ["# Configuration Diff\n"]
        lines.append(f"- Added: {len(self.added())}")
        lines.append(f"- Removed: {len(self.removed())}")
        lines.append(f"- Modified: {len(self.modified())}\n")

        if self.added():
            lines.append("## Added\n")
            for e in self.added():
                lines.append(f"+ [{e.category}] {e.description}")
        if self.removed():
            lines.append("\n## Removed\n")
            for e in self.removed():
                lines.append(f"- [{e.category}] {e.description}")
        if self.modified():
            lines.append("\n## Modified\n")
            for e in self.modified():
                lines.append(f"~ [{e.category}] {e.description}")
                lines.append(f"  Before: {e.before}")
                lines.append(f"  After: {e.after}")

        return "\n".join(lines)


class SemanticDiffEngine:
    """Produces semantic diffs between two RouterOS configurations."""

    def diff(self, before: str, after: str) -> SemanticDiff:
        """Diff two RouterOS configuration strings semantically."""
        from apps.network_engineer.mikrotik.routeros_parser import parse_routeros_config

        before_cfg = parse_routeros_config(before)
        after_cfg = parse_routeros_config(after)

        entries: list[DiffEntry] = []

        entries.extend(self._diff_interfaces(before_cfg.interfaces, after_cfg.interfaces))
        entries.extend(self._diff_ip_addresses(before_cfg.ip_addresses, after_cfg.ip_addresses))
        entries.extend(self._diff_firewall(before_cfg.firewall_rules, after_cfg.firewall_rules))
        entries.extend(self._diff_nat(before_cfg.nat_rules, after_cfg.nat_rules))
        entries.extend(self._diff_routes(before_cfg.routes, after_cfg.routes))
        entries.extend(self._diff_dhcp(before_cfg.dhcp_servers, after_cfg.dhcp_servers))
        entries.extend(self._diff_hotspot(before_cfg.hotspot_configs, after_cfg.hotspot_configs))
        entries.extend(self._diff_dns(before_cfg.dns_config, after_cfg.dns_config))
        entries.extend(self._diff_queues(before_cfg.queue_configs, after_cfg.queue_configs))
        entries.extend(self._diff_bridges(before_cfg.bridge_configs, after_cfg.bridge_configs))

        summary = {
            "added": len([e for e in entries if e.diff_type == DiffType.ADDED]),
            "removed": len([e for e in entries if e.diff_type == DiffType.REMOVED]),
            "modified": len([e for e in entries if e.diff_type == DiffType.MODIFIED]),
        }

        return SemanticDiff(entries=entries, summary=summary)

    def _diff_interfaces(self, before, after) -> list[DiffEntry]:
        entries = []
        before_names = {i.name for i in before}
        after_names = {i.name for i in after}

        for iface in after:
            if iface.name not in before_names:
                entries.append(DiffEntry(
                    category="Interface",
                    diff_type=DiffType.ADDED,
                    path=f"interface/{iface.name}",
                    after=iface.name,
                    description=f"Interface {iface.name} added",
                ))

        for iface in before:
            if iface.name not in after_names:
                entries.append(DiffEntry(
                    category="Interface",
                    diff_type=DiffType.REMOVED,
                    path=f"interface/{iface.name}",
                    before=iface.name,
                    description=f"Interface {iface.name} removed",
                ))

        return entries

    def _diff_ip_addresses(self, before, after) -> list[DiffEntry]:
        entries = []
        before_map = {f"{ip.interface}:{ip.address}" for ip in before}
        after_map = {f"{ip.interface}:{ip.address}" for ip in after}

        for ip in after:
            key = f"{ip.interface}:{ip.address}"
            if key not in before_map:
                entries.append(DiffEntry(
                    category="IP Address",
                    diff_type=DiffType.ADDED,
                    path=f"ip/address/{ip.interface}",
                    after=ip.address,
                    description=f"IP {ip.address} added on {ip.interface}",
                ))

        for ip in before:
            key = f"{ip.interface}:{ip.address}"
            if key not in after_map:
                entries.append(DiffEntry(
                    category="IP Address",
                    diff_type=DiffType.REMOVED,
                    path=f"ip/address/{ip.interface}",
                    before=ip.address,
                    description=f"IP {ip.address} removed from {ip.interface}",
                ))

        return entries

    def _diff_firewall(self, before, after) -> list[DiffEntry]:
        entries = []
        before_set = {(r.chain, r.action, r.protocol, r.port, r.in_interface, r.out_interface) for r in before}
        after_set = {(r.chain, r.action, r.protocol, r.port, r.in_interface, r.out_interface) for r in after}

        for r in after:
            key = (r.chain, r.action, r.protocol, r.port, r.in_interface, r.out_interface)
            if key not in before_set:
                entries.append(DiffEntry(
                    category="Firewall",
                    diff_type=DiffType.ADDED,
                    path=f"firewall/filter/{r.chain}",
                    after=key,
                    description=f"Firewall rule added: {r.action} on {r.chain}",
                ))

        for r in before:
            key = (r.chain, r.action, r.protocol, r.port, r.in_interface, r.out_interface)
            if key not in after_set:
                entries.append(DiffEntry(
                    category="Firewall",
                    diff_type=DiffType.REMOVED,
                    path=f"firewall/filter/{r.chain}",
                    before=key,
                    description=f"Firewall rule removed: {r.action} on {r.chain}",
                ))

        return entries

    def _diff_nat(self, before, after) -> list[DiffEntry]:
        entries = []
        before_set = {(r.chain, r.action, r.out_interface) for r in before}
        after_set = {(r.chain, r.action, r.out_interface) for r in after}

        for r in after:
            key = (r.chain, r.action, r.out_interface)
            if key not in before_set:
                entries.append(DiffEntry(
                    category="NAT",
                    diff_type=DiffType.ADDED,
                    path=f"firewall/nat/{r.chain}",
                    after=key,
                    description=f"NAT rule added: {r.action} on {r.out_interface}",
                ))

        for r in before:
            key = (r.chain, r.action, r.out_interface)
            if key not in after_set:
                entries.append(DiffEntry(
                    category="NAT",
                    diff_type=DiffType.REMOVED,
                    path=f"firewall/nat/{r.chain}",
                    before=key,
                    description=f"NAT rule removed: {r.action} on {r.out_interface}",
                ))

        return entries

    def _diff_routes(self, before, after) -> list[DiffEntry]:
        entries = []
        before_set = {(r.dst_address, r.gateway) for r in before}
        after_set = {(r.dst_address, r.gateway) for r in after}

        for r in after:
            key = (r.dst_address, r.gateway)
            if key not in before_set:
                entries.append(DiffEntry(
                    category="Route",
                    diff_type=DiffType.ADDED,
                    path=f"ip/route/{r.dst_address}",
                    after=key,
                    description=f"Route added: {r.dst_address} via {r.gateway}",
                ))

        for r in before:
            key = (r.dst_address, r.gateway)
            if key not in after_set:
                entries.append(DiffEntry(
                    category="Route",
                    diff_type=DiffType.REMOVED,
                    path=f"ip/route/{r.dst_address}",
                    before=key,
                    description=f"Route removed: {r.dst_address} via {r.gateway}",
                ))

        return entries

    def _diff_dhcp(self, before, after) -> list[DiffEntry]:
        entries = []
        before_names = {d.name for d in before}
        after_names = {d.name for d in after}

        for d in after:
            if d.name not in before_names:
                entries.append(DiffEntry(
                    category="DHCP",
                    diff_type=DiffType.ADDED,
                    path=f"dhcp-server/{d.name}",
                    after=d.name,
                    description=f"DHCP server {d.name} added",
                ))

        for d in before:
            if d.name not in after_names:
                entries.append(DiffEntry(
                    category="DHCP",
                    diff_type=DiffType.REMOVED,
                    path=f"dhcp-server/{d.name}",
                    before=d.name,
                    description=f"DHCP server {d.name} removed",
                ))

        return entries

    def _diff_hotspot(self, before, after) -> list[DiffEntry]:
        entries = []
        before_names = {h.name for h in before}
        after_names = {h.name for h in after}

        for h in after:
            if h.name not in before_names:
                entries.append(DiffEntry(
                    category="Hotspot",
                    diff_type=DiffType.ADDED,
                    path=f"hotspot/{h.name}",
                    after=h.name,
                    description=f"Hotspot {h.name} added",
                ))

        for h in before:
            if h.name not in after_names:
                entries.append(DiffEntry(
                    category="Hotspot",
                    diff_type=DiffType.REMOVED,
                    path=f"hotspot/{h.name}",
                    before=h.name,
                    description=f"Hotspot {h.name} removed",
                ))

        return entries

    def _diff_dns(self, before, after) -> list[DiffEntry]:
        entries = []
        before_servers = set(before.servers) if before else set()
        after_servers = set(after.servers) if after else set()

        if before_servers != after_servers:
            entries.append(DiffEntry(
                category="DNS",
                diff_type=DiffType.MODIFIED,
                path="ip/dns/servers",
                before=sorted(before_servers),
                after=sorted(after_servers),
                description="DNS servers changed",
            ))

        before_remote = before.allow_remote_requests if before else False
        after_remote = after.allow_remote_requests if after else False
        if before_remote != after_remote:
            entries.append(DiffEntry(
                category="DNS",
                diff_type=DiffType.MODIFIED,
                path="ip/dns/allow-remote-requests",
                before=before_remote,
                after=after_remote,
                description=f"DNS allow-remote-requests changed: {before_remote} -> {after_remote}",
            ))

        return entries

    def _diff_queues(self, before, after) -> list[DiffEntry]:
        entries = []
        before_names = {q.name for q in before}
        after_names = {q.name for q in after}

        for q in after:
            if q.name not in before_names:
                entries.append(DiffEntry(
                    category="Queue",
                    diff_type=DiffType.ADDED,
                    path=f"queue/{q.name}",
                    after=q.name,
                    description=f"Queue {q.name} added",
                ))

        for q in before:
            if q.name not in after_names:
                entries.append(DiffEntry(
                    category="Queue",
                    diff_type=DiffType.REMOVED,
                    path=f"queue/{q.name}",
                    before=q.name,
                    description=f"Queue {q.name} removed",
                ))

        return entries

    def _diff_bridges(self, before, after) -> list[DiffEntry]:
        entries = []
        before_names = {b.name for b in before}
        after_names = {b.name for b in after}

        for b in after:
            if b.name not in before_names:
                entries.append(DiffEntry(
                    category="Bridge",
                    diff_type=DiffType.ADDED,
                    path=f"bridge/{b.name}",
                    after=b.name,
                    description=f"Bridge {b.name} added",
                ))

        for b in before:
            if b.name not in after_names:
                entries.append(DiffEntry(
                    category="Bridge",
                    diff_type=DiffType.REMOVED,
                    path=f"bridge/{b.name}",
                    before=b.name,
                    description=f"Bridge {b.name} removed",
                ))

        return entries


semantic_diff_engine = SemanticDiffEngine()
