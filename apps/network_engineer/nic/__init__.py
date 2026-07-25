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

from apps.network_engineer.nic.inference import (
    Evidence,
    Hypothesis,
    InferenceEngine,
    ReasoningChain,
    inference_engine,
)
from apps.network_engineer.nic.knowledge.enricher import (
    ConceptTag,
    KnowledgeEnricher,
    knowledge_enricher,
)
from apps.network_engineer.nic.knowledge.ontology import (
    CONCEPT_DEFINITIONS,
    ConceptDefinition,
    ConceptMapper,
    UniversalConcept,
    concept_mapper,
)
from apps.network_engineer.nic.knowledge.profiles import (
    PROFILES,
    CISProfile,
    ComplianceCheck,
    ComplianceEngine,
    ComplianceProfile,
    ComplianceReport,
    ComplianceRule,
    ISPBestPracticeProfile,
    NISTProfile,
    PCIDSSProfile,
    SMBBestPracticeProfile,
    get_compliance_engine,
)

__all__ = [
    "CONCEPT_DEFINITIONS",
    "PROFILES",
    "CISProfile",
    "ComplianceCheck",
    "ComplianceEngine",
    "ComplianceProfile",
    "ComplianceReport",
    "ComplianceRule",
    "ConceptDefinition",
    "ConceptMapper",
    "ConceptTag",
    "Evidence",
    "Hypothesis",
    "ISPBestPracticeProfile",
    "InferenceEngine",
    "KnowledgeEnricher",
    "NISTProfile",
    "PCIDSSProfile",
    "ReasoningChain",
    "SMBBestPracticeProfile",
    "UniversalConcept",
    "concept_mapper",
    "get_compliance_engine",
    "inference_engine",
    "knowledge_enricher",
]
