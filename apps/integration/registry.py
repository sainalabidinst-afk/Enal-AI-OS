"""
Capability Registry
====================

Provides metadata-driven discovery of capabilities so the orchestrator
no longer hardcodes capability relationships.

Each registered capability declares:
- id, domain, version
- inputs, outputs
- requires, provides
- optional tags/labels
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class CapabilityDescriptor:
    capability_id: str
    domain: str
    version: str = "1.0.0"
    description: str = ""
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    requires: list[str] = field(default_factory=list)
    provides: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "domain": self.domain,
            "version": self.version,
            "description": self.description,
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
            "requires": list(self.requires),
            "provides": list(self.provides),
            "tags": list(self.tags),
            "metadata": dict(self.metadata),
        }


class CapabilityRegistry:
    """
    Registry of all known capabilities and their contracts.

    The orchestrator uses this to resolve which capabilities are needed
    for a workflow without hardcoding capability-specific logic.
    """

    def __init__(self) -> None:
        self._descriptors: dict[str, CapabilityDescriptor] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        defaults = [
            CapabilityDescriptor(
                capability_id="trading-analysis",
                domain="trading",
                description="Analyze market conditions and produce structured evidence",
                inputs=["symbol", "timeframes", "exchange"],
                outputs=["market_evidence", "bias", "confidence", "risk_level"],
                requires=["market_data_provider"],
                provides=["market_evidence", "trading_context"],
                tags=["trading", "analysis"],
            ),
            CapabilityDescriptor(
                capability_id="knowledge-query",
                domain="knowledge",
                description="Query the knowledge base for entities and evidence",
                inputs=["query", "domain", "limit"],
                outputs=["knowledge_entities", "knowledge_evidence"],
                requires=["knowledge_store"],
                provides=["knowledge_context"],
                tags=["knowledge", "retrieval"],
            ),
            CapabilityDescriptor(
                capability_id="evidence-aggregation",
                domain="integration",
                description="Normalize and aggregate evidence from multiple capabilities",
                inputs=["evidences"],
                outputs=["aggregated_evidence"],
                requires=[],
                provides=["unified_evidence"],
                tags=["integration", "evidence"],
            ),
            CapabilityDescriptor(
                capability_id="reasoning",
                domain="cognition",
                description="Apply reasoning over facts and evidence",
                inputs=["facts", "goal"],
                outputs=["conclusions", "decisions"],
                requires=[],
                provides=["reasoning_output"],
                tags=["cognition", "reasoning"],
            ),
            CapabilityDescriptor(
                capability_id="network-design-review",
                domain="network",
                description="Review network topology and configuration against best practices",
                inputs=["topology", "requirements"],
                outputs=["design_issues", "grades", "recommendations"],
                requires=["network_knowledge"],
                provides=["design_review_report"],
                tags=["network", "design", "review"],
            ),
            CapabilityDescriptor(
                capability_id="summary-generation",
                domain="integration",
                description="Generate human-readable summary from analysis results",
                inputs=["analysis_result", "evidence"],
                outputs=["summary", "counter_scenario", "strategy"],
                requires=[],
                provides=["summary"],
                tags=["integration", "summary"],
            ),
        ]
        for descriptor in defaults:
            self.register(descriptor)

    def register(self, descriptor: CapabilityDescriptor) -> None:
        self._descriptors[descriptor.capability_id] = descriptor
        logger.debug("Registered capability: %s", descriptor.capability_id)

    def resolve(self, capability_id: str) -> CapabilityDescriptor | None:
        return self._descriptors.get(capability_id)

    def resolve_by_domain(self, domain: str) -> list[CapabilityDescriptor]:
        return [d for d in self._descriptors.values() if d.domain == domain]

    def resolve_by_tag(self, tag: str) -> list[CapabilityDescriptor]:
        return [d for d in self._descriptors.values() if tag in d.tags]

    def requires(self, capability_id: str) -> list[str]:
        descriptor = self._descriptors.get(capability_id)
        return list(descriptor.requires) if descriptor else []

    def provides(self, capability_id: str) -> list[str]:
        descriptor = self._descriptors.get(capability_id)
        return list(descriptor.provides) if descriptor else []

    def all(self) -> list[CapabilityDescriptor]:
        return list(self._descriptors.values())

    def to_dict(self) -> dict[str, dict[str, Any]]:
        return {cid: d.to_dict() for cid, d in self._descriptors.items()}


capability_registry = CapabilityRegistry()
