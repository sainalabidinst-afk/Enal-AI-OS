"""
Capability Integration Module
===============================

Provides integration between ECP capabilities:
- Trading Intelligence + Knowledge System + Reasoning
- Network Engineer + Knowledge Graph + Reasoning
- Self-Improvement + Execution History + Knowledge Update

Architecture:
    CapabilityIntegrationEngine (orchestrator)
        ├── EvidenceAdapter (unified evidence)
        ├── TradingKnowledgeIntegration
        ├── NetworkKnowledgeIntegration
        └── SelfImprovementIntegration
"""

from apps.integration.evidence_adapter import EvidenceAdapter
from apps.integration.orchestrator import IntegrationEngine

__all__ = [
    "EvidenceAdapter",
    "IntegrationEngine",
]
