"""
Cross-Domain Knowledge Graph — Public Contracts (Pydantic schemas).

Defines the input (GraphQueryRequest) and output (GraphQueryResult) contracts
for the Cross-Domain Knowledge Graph Capability Pack.
"""

from __future__ import annotations  # noqa: I001

import uuid
from dataclasses import dataclass, field
from enum import StrEnum, Enum  # noqa: F401
from typing import Any

from pydantic import BaseModel, Field


class MemoryLayer(StrEnum):
    """ECP memory layers that can be scanned for entities."""

    WORKING = "working"
    CONVERSATION = "conversation"
    KNOWLEDGE = "knowledge"
    LONGTERM = "longterm"
    EPISODIC = "episodic"
    SESSION = "session"
    PROJECT = "project"


class RelationType(StrEnum):
    """Types of relationships between entities."""

    RELATED_TO = "related_to"
    DEPENDS_ON = "depends_on"
    CORRELATES_WITH = "correlates_with"
    CONTRADICTS = "contradicts"
    SUPERSEDES = "supersedes"
    CAUSES = "causes"
    REFERENCES = "references"
    SAME_AS = "same_as"
    PART_OF = "part_of"
    IMPLEMENTED_IN = "implemented_in"


class NodeType(StrEnum):
    """Types of nodes in the cross-domain graph."""

    CONCEPT = "concept"
    PROJECT = "project"
    REQUIREMENT = "requirement"
    COMPONENT = "component"
    DECISION = "decision"
    EVIDENCE = "evidence"
    RECOMMENDATION = "recommendation"
    ISSUE = "issue"
    SOLUTION = "solution"
    ENTITY = "entity"


# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class GraphQueryRequest(BaseModel):
    """Input contract for a cross-domain graph query."""

    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique request identifier")  # noqa: E501
    query: str = Field(..., description="Natural language cross-domain question")
    source_domains: list[str] = Field(default_factory=list, description="Domains to search (e.g. trading, network, code)")  # noqa: E501
    target_memory_layers: list[str] = Field(
        default_factory=lambda: [
            MemoryLayer.KNOWLEDGE.value,
            MemoryLayer.EPISODIC.value,
            MemoryLayer.PROJECT.value,
            MemoryLayer.LONGTERM.value,
        ],
        description="Memory layers to scan",
    )
    max_depth: int = Field(default=3, ge=1, le=10, description="Maximum traversal depth")
    include_explanations: bool = Field(default=True, description="Include reasoning chain in output")  # noqa: E501
    confidence_threshold: float = Field(default=0.5, ge=0.0, le=1.0, description="Minimum confidence for relationships")  # noqa: E501


# ---------------------------------------------------------------------------
# Graph structures
# ---------------------------------------------------------------------------


@dataclass
class GraphNode:
    """A node in the cross-domain knowledge graph."""

    id: str
    name: str
    node_type: NodeType
    domain: str
    layer: str
    description: str = ""
    properties: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    embedding: list[float] | None = None


@dataclass
class GraphEdge:
    """An edge connecting two nodes in the graph."""

    id: str
    source_id: str
    target_id: str
    relation: RelationType
    weight: float = 1.0
    confidence: float = 0.0
    evidence: list[str] = field(default_factory=list)
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class ResolvedEntity:
    """An entity resolved across domains (potential duplicate of same entity)."""

    canonical_id: str
    name: str
    domain: str
    layer: str
    aliases: list[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class InferenceResult:
    """Result of inferring an answer from the graph."""

    answer: str
    evidence_chain: list[str]
    source_entities: list[str]
    confidence: float


# ---------------------------------------------------------------------------
# Output model
# ---------------------------------------------------------------------------


@dataclass
class GraphQueryResult:
    """Output contract for a cross-domain graph query result."""

    request_id: str
    query: str
    answer: str
    entities_discovered: list[dict[str, Any]]
    relationships: list[dict[str, Any]]
    relationship_paths: list[list[str]]
    inference: InferenceResult | None
    confidence: float
    graph_snapshot: dict[str, Any]
    explanation: dict[str, Any]
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "query": self.query,
            "answer": self.answer,
            "entities_discovered": self.entities_discovered,
            "relationships": self.relationships,
            "relationship_paths": self.relationship_paths,
            "inference": (
                {
                    "answer": self.inference.answer,
                    "evidence_chain": self.inference.evidence_chain,
                    "source_entities": self.inference.source_entities,
                    "confidence": self.inference.confidence,
                }
                if self.inference
                else None
            ),
            "confidence": self.confidence,
            "graph_snapshot": self.graph_snapshot,
            "explanation": self.explanation,
            "raw": self.raw,
        }
