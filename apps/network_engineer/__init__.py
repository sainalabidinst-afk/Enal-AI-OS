"""
Network Engineer Reference App
===============================

Demonstrates ECP capabilities for network configuration and management.
Uses: SDK, Runtime, Marketplace, Studio, Contracts

Workflow:
 1. Natural Language Input
 2. Topology Understanding
 3. Requirement Extraction
 4. Network Planning
 5. Configuration Generation
 6. Simulation
 7. Verification
 8. Security Audit
 9. Documentation
10. Deployment (future)
11. Post Validation (future)

Network Engineer 2.0 capabilities:
 - Configuration parsing & validation
 - Security compliance auditing
 - Risk analysis & recommendations
 - Configuration generation & simulation
 - Design review (SPOF, bottleneck, security gap, scalability)
 - Troubleshooting engine (evidence → hypothesis → root cause)
 - Migration planner (cross-vendor with risk & rollback)
 - Network advisor (high-level design questions)
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.network_engineer.advisor import network_advisor
from apps.network_engineer.analyzer import NetworkAnalysisReport, network_analyzer
from apps.network_engineer.design_review import design_review_engine
from apps.network_engineer.docs_generator import network_doc_generator
from apps.network_engineer.generator import routeros_generator
from apps.network_engineer.graph_builder import network_graph_builder
from apps.network_engineer.mikrotik.routeros_parser import RouterOSParser, parse_routeros_config
from apps.network_engineer.migration_planner import migration_planner
from apps.network_engineer.nic import (
    ConceptTag,
    ReasoningChain,
    get_compliance_engine,
    inference_engine,
    knowledge_enricher,
)
from apps.network_engineer.recommendation_engine import recommendation_engine
from apps.network_engineer.simulator import network_simulator
from apps.network_engineer.topology import NetworkConnection, NetworkDevice, NetworkInterface, NetworkSegment
from apps.network_engineer.troubleshooting import troubleshooting_engine


class NetworkEngineerApp(BaseReferenceApp):
    name = "network-engineer"
    version = "2.0.0"
    description = "Vendor-agnostic network intelligence platform: configuration analysis, design review, troubleshooting, migration planning, and advisory."
    category = "networking"
    pipeline = ["perception", "memory", "reasoning", "decision", "action"]

    def __init__(self):
        self.parser = RouterOSParser()
        self.analyzer = network_analyzer
        self.graph_builder = network_graph_builder
        self.recommendation_engine = recommendation_engine
        self.generator = routeros_generator
        self.simulator = network_simulator
        self.doc_generator = network_doc_generator

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Run the Network Engineer app."""
        from backend.app.core.adaptive_runtime import adaptive_runtime
        context = context or {}
        project_id = context.get("project_id", "network-engineer-default")

        result = await adaptive_runtime.execute(
            user_input,
            project_id=project_id,
            force_pipeline=self.pipeline,
        )

        return {
            "app": self.name,
            "version": self.version,
            "input": user_input,
            "pipeline": self.pipeline,
            "result": result,
            "metadata": {
                "category": self.category,
                "capabilities_used": [
                    "networking",
                    "configuration",
                    "validation",
                    "simulation",
                    "documentation",
                    "knowledge",
                    "compliance",
                    "reasoning",
                    "design_review",
                    "troubleshooting",
                    "migration_planning",
                    "advisory",
                ],
            },
        }

    def _parse_config(self, config_content: str) -> Any:
        """Parse config with vendor auto-detection."""
        from apps.network_engineer.vendor.detector import detect_vendor, parse_config

        vendor = detect_vendor(config_content)
        if vendor == "cisco":
            return parse_config(config_content, vendor="cisco")
        elif vendor == "fortinet":
            return parse_config(config_content, vendor="fortinet")
        return self.parser.parse(config_content)

    def _detect_vendor(self, config_content: str) -> str | None:
        from apps.network_engineer.vendor.detector import detect_vendor
        return detect_vendor(config_content)

    async def analyze_config(self, config_content: str) -> dict[str, Any]:
        """Analyze a network configuration using NIC (Network Intelligence Core)."""
        config = self._parse_config(config_content)
        vendor = getattr(config, "vendor", None) or self._detect_vendor(config_content) or "unknown"

        concept_tags = knowledge_enricher.enrich(config)
        evidence = self._build_evidence(concept_tags)
        reasoning_chains = inference_engine.reason(evidence)

        topology = self.graph_builder.build(config)
        report: NetworkAnalysisReport = await self.analyzer.analyze(config, topology)
        recommendations = await self.recommendation_engine.generate(report.issues)

        return {
            "device": report.device_name,
            "vendor": vendor,
            "summary": report.summary,
            "concepts": [
                {
                    "concept": tag.concept.value,
                    "confidence": tag.confidence,
                    "explanation": tag.explanation,
                    "references": tag.references,
                }
                for tag in concept_tags
            ],
            "reasoning": [
                {
                    "hypothesis_id": chain.hypothesis_id,
                    "confidence": chain.confidence,
                    "conclusion": chain.conclusion,
                    "recommendation": chain.recommendation,
                    "evidence": [e.concept.value for e in chain.evidence_found],
                }
                for chain in reasoning_chains
            ],
            "issues": [
                {
                    "severity": issue.severity.value,
                    "category": issue.category,
                    "description": issue.description,
                    "recommendation": issue.recommendation,
                    "line": issue.line_number,
                    "confidence": issue.confidence,
                }
                for issue in report.issues
            ],
            "recommendations": [
                {
                    "priority": rec.priority.value,
                    "problem": rec.problem,
                    "why": rec.why,
                    "impact": rec.impact,
                    "recommendation": rec.recommendation,
                    "confidence": rec.confidence,
                    "references": rec.references,
                }
                for rec in recommendations
            ],
        }

    async def check_compliance(self, config_content: str, profile: str = "CIS") -> dict[str, Any]:
        """Check configuration against a compliance profile."""
        config = self._parse_config(config_content)
        engine = get_compliance_engine(profile)
        report = engine.check(config)
        return report.to_dict()

    async def explain_finding(self, config_content: str, category: str) -> str | None:
        """Explain a finding using NIC knowledge base."""
        config = self._parse_config(config_content)
        return knowledge_enricher.explain_finding(category, config)

    async def translate_config(self, config_content: str, target_vendor: str) -> dict[str, Any]:
        """Translate configuration between vendors (placeholder for future implementation)."""
        config = self._parse_config(config_content)
        concept_tags = knowledge_enricher.enrich(config)
        source_vendor = getattr(config, "vendor", None) or self._detect_vendor(config_content) or "unknown"

        translation = {
            "source_vendor": source_vendor,
            "target_vendor": target_vendor,
            "concepts_detected": len(concept_tags),
            "status": "not_implemented",
            "message": "Cross-vendor translation engine is planned for future release.",
            "concepts": [tag.concept.value for tag in concept_tags],
        }

        if source_vendor == "mikrotik" and target_vendor == "cisco":
            translation["mappings"] = [
                {"concept": "firewall_filter", "mikrotik": "/ip firewall filter", "cisco": "access-list"},
                {"concept": "vrrp", "mikrotik": "/interface vrrp", "cisco": "standby"},
            ]
        elif source_vendor == "cisco" and target_vendor == "fortinet":
            translation["mappings"] = [
                {"concept": "acl", "cisco": "access-list", "fortinet": "config firewall policy"},
                {"concept": "hsrp", "cisco": "standby", "fortinet": "config system ha"},
            ]
        elif source_vendor == "fortinet" and target_vendor == "mikrotik":
            translation["mappings"] = [
                {"concept": "firewall_policy", "fortinet": "config firewall policy", "mikrotik": "/ip firewall filter"},
                {"concept": "ha", "fortinet": "config system ha", "mikrotik": "/interface vrrp"},
            ]

        return translation

    async def generate_config(self, requirements: dict[str, Any]) -> dict[str, Any]:
        """Generate RouterOS configuration from requirements."""
        config = await self.generator.generate(requirements)
        return {
            "config": config,
            "type": requirements.get("type", "general"),
            "requirements": requirements,
        }

    async def simulate_config(self, config_content: str) -> dict[str, Any]:
        """Simulate a RouterOS configuration."""
        result = await self.simulator.simulate(config_content)
        return {
            "simulation_id": result.id,
            "status": result.status.value,
            "steps": [
                {
                    "id": step.id,
                    "description": step.description,
                    "passed": step.passed,
                    "actual_result": step.actual_result,
                }
                for step in result.steps
            ],
            "issues": result.issues,
            "improvements": result.improvements,
        }

    async def generate_documentation(self, config_content: str) -> str:
        """Generate documentation from network configuration (vendor-agnostic, NIC-powered)."""
        config = self._parse_config(config_content)
        topology = self.graph_builder.build(config)
        report: NetworkAnalysisReport = await self.analyzer.analyze(config, topology)
        concept_tags = knowledge_enricher.enrich(config)
        evidence = self._build_evidence(concept_tags)
        reasoning_chains = inference_engine.reason(evidence)
        doc = self.doc_generator.generate(config, analysis=report, topology=topology)
        markdown = self.doc_generator.to_markdown(doc)

        if concept_tags:
            markdown += "\n\n## Detected Concepts (NIC)\n\n"
            for tag in concept_tags:
                markdown += f"### {tag.concept.value.replace('_', ' ').title()}\n\n"
                markdown += f"{tag.explanation}\n\n"
                if tag.references:
                    markdown += f"**References:** {', '.join(tag.references)}\n\n"

        if reasoning_chains:
            markdown += "\n## Reasoning (NIC Inference Engine)\n\n"
            for chain in reasoning_chains:
                markdown += f"### {chain.conclusion}\n\n"
                markdown += f"**Confidence:** {chain.confidence:.0%}\n\n"
                markdown += f"**Evidence:** {', '.join(e.concept.value for e in chain.evidence_found)}\n\n"
                markdown += f"**Recommendation:** {chain.recommendation}\n\n"

        return markdown

    async def review_design(self, topology_json: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Perform design review on a network topology."""
        from apps.network_engineer.topology import NetworkTopology

        topology = NetworkTopology()
        for device_id, device_data in topology_json.get("devices", {}).items():
            from apps.network_engineer.topology import DeviceType, InterfaceType, RedundancyRole
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

        report = await design_review_engine.review(topology, context)
        return report.to_dict()

    async def troubleshoot(self, symptom: str, evidence: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        """Start or continue a troubleshooting session."""
        session = troubleshooting_engine.create_session(symptom)
        if evidence:
            for item in evidence:
                troubleshooting_engine.add_evidence(
                    session,
                    source=item.get("source", "user"),
                    content=item.get("content", ""),
                    confidence=item.get("confidence", 1.0),
                )
        hypotheses = troubleshooting_engine.generate_hypotheses(session)
        return session.to_dict()

    async def plan_migration(self, source_vendor: str, target_vendor: str, source_config: str = "") -> dict[str, Any]:
        """Generate a cross-vendor migration plan."""
        plan = await migration_planner.plan(source_config, source_vendor, target_vendor)
        return plan.to_dict()

    async def advise(self, query: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Provide high-level network design advice."""
        return await network_advisor.advise(query, context)

    def _build_evidence(self, concept_tags: list[ConceptTag]) -> list[Any]:
        from apps.network_engineer.nic.inference import Evidence
        return [
            Evidence(
                concept=tag.concept,
                present=True,
                details=tag.explanation,
                confidence=tag.confidence,
            )
            for tag in concept_tags
        ]


def get_app() -> NetworkEngineerApp:
    """Get the Network Engineer app instance."""
    return NetworkEngineerApp()
