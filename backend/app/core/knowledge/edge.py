from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class RelationType(str):
    RELATES_TO = "relates_to"
    DEPENDS_ON = "depends_on"
    IMPLEMENTS = "implements"
    CONTAINS = "contains"
    SUPERSET_OF = "superset_of"
    SUBSET_OF = "subset_of"
    PREREQUISITE_OF = "prerequisite_of"
    EVIDENCE_FOR = "evidence_for"
    CONTRADICTS = "contradicts"
    SUPERSEDES = "supersedes"
    MAPPED_TO = "mapped_to"
    INSTANCE_OF = "instance_of"


@dataclass
class KnowledgeEdge:
    id: str
    source_id: str
    target_id: str
    relation: str
    weight: float = 1.0
    confidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
