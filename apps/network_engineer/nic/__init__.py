"""
Network Intelligence Core (NIC)
=================================

The brain of ECP's network intelligence.

Architecture:
Layer 1: Syntax (vendor configs)
Layer 2: Universal AST (vendor-agnostic representation)
Layer 3: Ontology (concepts, mappings, knowledge)
Layer 4: Reasoning (inference, hypothesis, decision)

All network applications use NIC as their shared core.
"""

from apps.network_engineer.nic.knowledge.ontology import (
    ConceptMapper,
    ConceptDefinition,
    UniversalConcept,
    concept_mapper,
    CONCEPT_DEFINITIONS,
)
from apps.network_engineer.nic.knowledge.enricher import (
    KnowledgeEnricher,
    ConceptTag,
    knowledge_enricher,
)
from apps.network_engineer.nic.knowledge.profiles import (
    ComplianceProfile,
    ComplianceRule,
    ComplianceCheck,
    ComplianceReport,
    ComplianceEngine,
    CISProfile,
    NISTProfile,
    PCIDSSProfile,
    ISPBestPracticeProfile,
    SMBBestPracticeProfile,
    PROFILES,
    get_compliance_engine,
)
from apps.network_engineer.nic.inference import (
    InferenceEngine,
    Evidence,
    Hypothesis,
    ReasoningChain,
    inference_engine,
)

__all__ = [
    "ConceptMapper",
    "ConceptDefinition",
    "UniversalConcept",
    "concept_mapper",
    "CONCEPT_DEFINITIONS",
    "KnowledgeEnricher",
    "ConceptTag",
    "knowledge_enricher",
    "ComplianceProfile",
    "ComplianceRule",
    "ComplianceCheck",
    "ComplianceReport",
    "ComplianceEngine",
    "CISProfile",
    "NISTProfile",
    "PCIDSSProfile",
    "ISPBestPracticeProfile",
    "SMBBestPracticeProfile",
    "PROFILES",
    "get_compliance_engine",
    "InferenceEngine",
    "Evidence",
    "Hypothesis",
    "ReasoningChain",
    "inference_engine",
]
