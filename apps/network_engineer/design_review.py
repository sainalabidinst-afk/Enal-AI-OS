"""
Design Review Engine
=====================

Analyzes network topology to identify design-level issues beyond configuration analysis.
Produces a scored review with categories: Availability, Security, Scalability, Performance.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from apps.network_engineer.topology import (
    DeviceType,
    InterfaceType,
    NetworkConnection,
    NetworkDevice,
    NetworkInterface,
    NetworkSegment,
    NetworkTopology,
    RedundancyRole,
)

logger = logging.getLogger(__name__)


class Grade(str, Enum):
    A = "A"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B = "B"
    B_MINUS = "B-"
    C_PLUS = "C+"
    C = "C"
    C_MINUS = "C-"
    D = "D"
    F = "F"


@dataclass
class DesignIssue:
    category: str
    severity: str
    title: str
    description: str
    recommendation: str
    affected_devices: list[str] = field(default_factory=list)
    affected_segments: list[str] = field(default_factory=list)
    confidence: float = 0.9


@dataclass
class DesignReviewReport:
    network_score: float = 0.0
    availability_grade: Grade = Grade.C
    security_grade: Grade = Grade.C
    scalability_grade: Grade = Grade.C
    performance_grade: Grade = Grade.C
    issues: list[DesignIssue] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "network_score": round(self.network_score, 1),
            "availability_grade": self.availability_grade.value,
            "security_grade": self.security_grade.value,
            "scalability_grade": self.scalability_grade.value,
            "performance_grade": self.performance_grade.value,
            "issues": [
                {
                    "category": i.category,
                    "severity": i.severity,
                    "title": i.title,
                    "description": i.description,
                    "recommendation": i.recommendation,
                    "affected_devices": i.affected_devices,
                    "affected_segments": i.affected_segments,
                    "confidence": i.confidence,
                }
                for i in self.issues
            ],
            "summary": self.summary,
        }


class DesignReviewEngine:
    """Analyzes network topology for design-level issues."""

    async def review(self, topology: NetworkTopology, context: dict[str, Any] | None = None) -> DesignReviewReport:
        context = context or {}
        report = DesignReviewReport()
        self._check_spof(topology, report)
        self._check_bottleneck(topology, report)
        self._check_security_gaps(topology, report)
        self._check_scalability(topology, report)
        self._check_performance(topology, report)
        self._check_vlan_leaks(topology, report)
        self._compute_grades(report, topology, context)
        return report

    def _check_spof(self, topology: NetworkTopology, report: DesignReviewReport):
        routers = [d for d in topology.devices.values() if d.device_type.value in ("router", "firewall")]
        for device in routers:
            conns = topology.get_connections(device.id)
            wan_conns = [c for c in conns if c.connection_type in ("ethernet", "fiber", "wan")]
            has_redundant_wan = len(wan_conns) >= 2
            has_ha = any(
                any("vrrp" in i.comment.lower() or "hsrp" in i.comment.lower() or "ha" in i.comment.lower()
                    for i in device.interfaces)
                or any(i.redundancy_role != RedundancyRole.NONE for i in device.interfaces)
                for device in [device]
            )
            if not has_redundant_wan or not has_ha:
                report.issues.append(DesignIssue(
                    category="Availability",
                    severity="critical",
                    title="Single Point of Failure",
                    description=f"Device {device.name} ({device.id}) lacks redundant WAN or HA configuration.",
                    recommendation="Add secondary WAN link, configure VRRP/HSRP/HA, and ensure redundant paths.",
                    affected_devices=[device.id],
                    confidence=0.9 if not has_redundant_wan else 0.7,
                ))

    def _check_bottleneck(self, topology: NetworkTopology, report: DesignReviewReport):
        for device in topology.devices.values():
            conns = topology.get_connections(device.id)
            if len(conns) > 4:
                low_bw = [c for c in conns if c.bandwidth in ("100Mbps", "10Mbps")]
                if low_bw:
                    report.issues.append(DesignIssue(
                        category="Performance",
                        severity="warning",
                        title="Potential Bottleneck",
                        description=f"Device {device.name} has {len(low_bw)} low-bandwidth links among {len(conns)} total connections.",
                        recommendation="Upgrade links to higher bandwidth or implement link aggregation.",
                        affected_devices=[device.id],
                        confidence=0.8,
                    ))

    def _check_security_gaps(self, topology: NetworkTopology, report: DesignReviewReport):
        for device in topology.devices.values():
            mgmt_ifaces = [i for i in device.interfaces if i.interface_type == InterfaceType.MANAGEMENT or "mgmt" in i.name.lower()]
            if mgmt_ifaces:
                for iface in mgmt_ifaces:
                    if not iface.ip_address:
                        continue
                    parts = iface.ip_address.split("/")
                    if len(parts) > 1 and parts[1] in ("0", "1", "8", "16", "24"):
                        report.issues.append(DesignIssue(
                            category="Security",
                            severity="warning",
                            title="Management Interface Exposure",
                            description=f"Management interface {iface.name} on {device.name} may be exposed to untrusted networks.",
                            recommendation="Restrict management access to dedicated out-of-band or management VLAN.",
                            affected_devices=[device.id],
                            confidence=0.85,
                        ))

    def _check_scalability(self, topology: NetworkTopology, report: DesignReviewReport):
        flat_segments = [s for s in topology.segments.values() if s.security_level == "standard" and len(s.devices) > 5]
        for segment in flat_segments:
            report.issues.append(DesignIssue(
                category="Scalability",
                severity="info",
                title="Flat Segment",
                description=f"Segment {segment.name} has {len(segment.devices)} devices without clear segmentation.",
                recommendation="Split segment into smaller VLANs or subnets to limit broadcast domains.",
                affected_segments=[segment.id],
                confidence=0.7,
            ))

    def _check_performance(self, topology: NetworkTopology, report: DesignReviewReport):
        for device in topology.devices.values():
            if device.device_type in (DeviceType.ROUTER, DeviceType.FIREWALL):
                conns = topology.get_connections(device.id)
                high_latency = [c for c in conns if c.latency and c.latency.endswith("ms") and int(c.latency[:-2]) > 50]
                if high_latency:
                    report.issues.append(DesignIssue(
                        category="Performance",
                        severity="info",
                        title="High Latency Link",
                        description=f"Device {device.name} has {len(high_latency)} high-latency links.",
                        recommendation="Review WAN links and consider SD-WAN or direct peering.",
                        affected_devices=[device.id],
                        confidence=0.8,
                    ))

    def _check_vlan_leaks(self, topology: NetworkTopology, report: DesignReviewReport):
        vlan_devices: dict[int, list[str]] = {}
        for device in topology.devices.values():
            for iface in device.interfaces:
                if iface.vlan_id is not None:
                    vlan_devices.setdefault(iface.vlan_id, []).append(device.id)
        for vlan_id, device_ids in vlan_devices.items():
            if len(device_ids) > 3:
                report.issues.append(DesignIssue(
                    category="Security",
                    severity="info",
                    title="VLAN Spanning Multiple Devices",
                    description=f"VLAN {vlan_id} spans {len(device_ids)} devices, increasing broadcast scope.",
                    recommendation="Verify VLAN assignment is intentional and review trunk links.",
                    affected_devices=device_ids,
                    confidence=0.6,
                ))

    def _compute_grades(self, report: DesignReviewReport, topology: NetworkTopology, context: dict[str, Any]):
        severity_weights = {"critical": 3, "warning": 2, "info": 1}
        category_scores = {
            "Availability": 0,
            "Security": 0,
            "Scalability": 0,
            "Performance": 0,
        }
        category_max = dict(category_scores)
        for issue in report.issues:
            cat = issue.category
            if cat in category_scores:
                category_max[cat] += 3
                category_scores[cat] += severity_weights.get(issue.severity, 1)

        def to_grade(score: float, max_score: float) -> Grade:
            if max_score == 0:
                return Grade.A
            ratio = 1.0 - (score / max_score)
            if ratio >= 0.95:
                return Grade.A
            if ratio >= 0.9:
                return Grade.A_MINUS
            if ratio >= 0.85:
                return Grade.B_PLUS
            if ratio >= 0.8:
                return Grade.B
            if ratio >= 0.75:
                return Grade.B_MINUS
            if ratio >= 0.7:
                return Grade.C_PLUS
            if ratio >= 0.65:
                return Grade.C
            if ratio >= 0.6:
                return Grade.C_MINUS
            if ratio >= 0.5:
                return Grade.D
            return Grade.F

        report.availability_grade = to_grade(category_scores["Availability"], category_max["Availability"])
        report.security_grade = to_grade(category_scores["Security"], category_max["Security"])
        report.scalability_grade = to_grade(category_scores["Scalability"], category_max["Scalability"])
        report.performance_grade = to_grade(category_scores["Performance"], category_max["Performance"])

        all_scores = [report.availability_grade, report.security_grade, report.scalability_grade, report.performance_grade]
        grade_values = {
            Grade.A: 4.0, Grade.A_MINUS: 3.7, Grade.B_PLUS: 3.3, Grade.B: 3.0,
            Grade.B_MINUS: 2.7, Grade.C_PLUS: 2.3, Grade.C: 2.0, Grade.C_MINUS: 1.7,
            Grade.D: 1.0, Grade.F: 0.0,
        }
        avg = sum(grade_values.get(g, 0.0) for g in all_scores) / len(all_scores) if all_scores else 0.0
        report.network_score = round(avg * 25, 1)

        report.summary = {
            "total_devices": len(topology.devices),
            "total_connections": len(topology.connections),
            "total_segments": len(topology.segments),
            "total_issues": len(report.issues),
            "critical_issues": sum(1 for i in report.issues if i.severity == "critical"),
            "warning_issues": sum(1 for i in report.issues if i.severity == "warning"),
            "info_issues": sum(1 for i in report.issues if i.severity == "info"),
        }


design_review_engine = DesignReviewEngine()