"""
Network Engineer Engine
=======================

Domain engine orchestrator for the Network Engineer Capability Pack.

Orchestrates:
    1. Configuration parsing and validation
    2. Security analysis
    3. Topology inference
    4. Design review
    5. Troubleshooting
    6. Migration planning
    7. Advisory

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
from typing import Any

from apps.network_engineer.advisor import NetworkAdvisor
from apps.network_engineer.analyzer import NetworkAnalysisReport, NetworkAnalyzer
from apps.network_engineer.design_review import DesignReviewEngine
from apps.network_engineer.migration_planner import MigrationPlanner
from apps.network_engineer.risk_scorer import RiskScoringEngine
from apps.network_engineer.topology import NetworkTopology
from apps.network_engineer.vendor.detector import parse_config

logger = logging.getLogger(__name__)


class NetworkEngineerEngine:
    """
    Orchestrates the full network engineering pipeline.

    Public API::

        engine = NetworkEngineerEngine()
        result = engine.audit(config_text, vendor="mikrotik")
        result = engine.review_design(topology_json)
    """

    def __init__(self) -> None:
        self.analyzer = NetworkAnalyzer()
        self.design_review = DesignReviewEngine()
        self.migration_planner = MigrationPlanner()
        self.advisor = NetworkAdvisor()
        self.risk_scorer = RiskScoringEngine()

    async def audit(self, config: str, vendor: str = "auto-detect") -> dict[str, Any]:
        """Run full security and best-practice audit on a network config."""
        parsed = parse_config(config, vendor if vendor != "auto-detect" else None)
        report: NetworkAnalysisReport = await self.analyzer.analyze(parsed)
        findings = [
            {
                "severity": issue.severity.value,
                "category": issue.category,
                "description": issue.description,
                "recommendation": issue.recommendation,
            }
            for issue in report.issues
        ]
        risk_score = self.risk_scorer.score(
            diff_summary={},
            findings=findings,
        )
        return {
            "device": report.device_name,
            "summary": report.summary,
            "issues": findings,
            "risk_score": risk_score.to_dict(),
            "metadata": report.metadata,
        }

    async def analyze_topology(
        self, config: str, vendor: str = "auto-detect"
    ) -> dict[str, Any]:
        """Infer network topology from configuration."""
        parsed = parse_config(config, vendor if vendor != "auto-detect" else None)
        from apps.network_engineer.graph_builder import network_graph_builder

        topology: NetworkTopology = network_graph_builder.build(parsed)
        return topology.to_dict()

    async def review_design(
        self,
        topology_json: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Run design review on a network topology."""
        from apps.network_engineer.topology import (
            DeviceType,
            InterfaceType,
            NetworkConnection,
            NetworkDevice,
            NetworkInterface,
            NetworkSegment,
            RedundancyRole,
        )

        topology = NetworkTopology()
        for device_id, device_data in topology_json.get("devices", {}).items():
            interfaces = [
                NetworkInterface(
                    name=i.get("name", ""),
                    interface_type=InterfaceType(i.get("type", "ethernet")),
                    ip_address=i.get("ip_address", ""),
                    vlan_id=i.get("vlan_id"),
                    bandwidth=i.get("bandwidth", ""),
                    redundancy_role=RedundancyRole(i.get("redundancy_role", "none")),
                )
                for i in device_data.get("interfaces", [])
            ]
            device = NetworkDevice(
                id=device_data.get("id", device_id),
                name=device_data.get("name", device_id),
                device_type=DeviceType(device_data.get("type", "router")),
                vendor=device_data.get("vendor", ""),
                model=device_data.get("model", ""),
                interfaces=interfaces,
                zone=device_data.get("zone", ""),
            )
            topology.add_device(device)

        for conn in topology_json.get("connections", []):
            topology.add_connection(NetworkConnection(
                source_device=conn.get("source_device", ""),
                source_interface=conn.get("source_interface", ""),
                target_device=conn.get("target_device", ""),
                target_interface=conn.get("target_interface", ""),
                connection_type=conn.get("connection_type", "ethernet"),
                bandwidth=conn.get("bandwidth", "1Gbps"),
                latency=conn.get("latency", "0ms"),
                redundancy_path=conn.get("redundancy_path", False),
                protocol=conn.get("protocol", ""),
            ))

        for segment_id, segment_data in topology_json.get("segments", {}).items():
            topology.add_segment(NetworkSegment(
                id=segment_data.get("id", segment_id),
                name=segment_data.get("name", segment_id),
                cidr=segment_data.get("cidr", ""),
                vlan_id=segment_data.get("vlan_id"),
                devices=segment_data.get("devices", []),
                purpose=segment_data.get("purpose", ""),
                security_level=segment_data.get("security_level", "standard"),
            ))

        report = await self.design_review.review(topology, context)
        return report.to_dict()

    async def troubleshoot(
        self,
        symptom: str,
        evidence: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Run structured troubleshooting workflow."""
        from apps.network_engineer.troubleshooting import troubleshooting_engine

        session = troubleshooting_engine.create_session(symptom)
        if evidence:
            for item in evidence:
                troubleshooting_engine.add_evidence(
                    session,
                    source=item.get("source", "user"),
                    content=item.get("content", ""),
                    confidence=item.get("confidence", 1.0),
                )
        troubleshooting_engine.generate_hypotheses(session)
        return session.to_dict()

    async def plan_migration(
        self,
        source_config: str,
        source_vendor: str,
        target_vendor: str,
    ) -> dict[str, Any]:
        """Plan cross-vendor migration with risk assessment."""
        plan = await self.migration_planner.plan(
            source_config=source_config,
            source_vendor=source_vendor,
            target_vendor=target_vendor,
        )
        return plan.to_dict()

    async def advise(
        self, query: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Provide network design advisory."""
        return await self.advisor.advise(query, context or {})

    def _build_summary(self, findings: list[dict[str, Any]]) -> dict[str, Any]:
        """Build summary statistics from findings."""
        severity_counts: dict[str, int] = {}
        for finding in findings:
            sev = finding.get("severity", "info")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
        return {
            "total_findings": len(findings),
            "severity_breakdown": severity_counts,
        }
