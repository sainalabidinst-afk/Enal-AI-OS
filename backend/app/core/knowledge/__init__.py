from backend.app.core.knowledge.edge import KnowledgeEdge, RelationType
from backend.app.core.knowledge.evidence import (
    ConfidencePropagator,
    ConflictDetector,
    Evidence,
    EvidenceBuilder,
    EvidenceStore,
)
from backend.app.core.knowledge.graph import KnowledgeGraph
from backend.app.core.knowledge.integration import CapabilityKnowledgeBridge
from backend.app.core.knowledge.learning import (
    FailurePattern,
    LearningEngine,
    Recommendation,
    SuccessPattern,
)
from backend.app.core.knowledge.node import KnowledgeNode
from backend.app.core.knowledge.ontology import (
    Ontology,
    OntologyEntity,
    OntologyEntityType,
    OntologyRelation,
)
from backend.app.core.knowledge.reference import Reference, ReferenceStore
from backend.app.core.knowledge.registry import KnowledgeRegistry
from backend.app.core.knowledge.retrieval import KnowledgeRetrieval
from backend.app.core.knowledge.schema import (
    KNOWLEDGE_SCHEMA_VERSION,
    KnowledgeCategory,
    KnowledgeDomain,
    KnowledgeEntity,
    KnowledgeStatus,
    KnowledgeType,
)
from backend.app.core.knowledge.versioning import KnowledgeVersion, KnowledgeVersionStore

__all__ = [
    "KNOWLEDGE_SCHEMA_VERSION",
    "CapabilityKnowledgeBridge",
    "ConfidencePropagator",
    "ConflictDetector",
    "Evidence",
    "EvidenceBuilder",
    "EvidenceStore",
    "FailurePattern",
    "KnowledgeCategory",
    "KnowledgeDomain",
    "KnowledgeEdge",
    "KnowledgeEntity",
    "KnowledgeGraph",
    "KnowledgeNode",
    "KnowledgeRegistry",
    "KnowledgeRetrieval",
    "KnowledgeStatus",
    "KnowledgeType",
    "KnowledgeVersion",
    "KnowledgeVersionStore",
    "LearningEngine",
    "Ontology",
    "OntologyEntity",
    "OntologyEntityType",
    "OntologyRelation",
    "Reference",
    "ReferenceStore",
    "Recommendation",
    "RelationType",
    "SuccessPattern",
]
