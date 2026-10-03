"""
Knowledge Engineer Schemas
==========================

Typed contracts for the Knowledge Engineer capability pack.
Defines input (KnowledgeEngineerRequest) and output (KnowledgeEngineerReport)
contracts for ontology design, knowledge graphs, and semantic search.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class KnowledgeOperation(StrEnum):
    ontology_design = "ontology_design"
    knowledge_graph = "knowledge_graph"
    semantic_search = "semantic_search"
    entity_resolution = "entity_resolution"


class KnowledgeStoreType(StrEnum):
    vector = "vector"
    graph = "graph"
    relational = "relational"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=5, ge=1)


class KnowledgeConfig(BaseModel):
    operation: KnowledgeOperation
    domain: str = "general"
    store_type: KnowledgeStoreType = KnowledgeStoreType.vector
    entities: list[str] = Field(default_factory=list)
    relationships: list[str] = Field(default_factory=list)


class KnowledgeEngineerRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "ontology_design"
    business_context: BusinessContext
    inputs: KnowledgeConfig
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class OntologyClass(BaseModel):
    name: str
    description: str
    properties: list[str] = Field(default_factory=list)
    parent_class: str | None = None


class RelationshipType(BaseModel):
    name: str
    source_class: str
    target_class: str
    cardinality: str = "n:m"


class EntityMapping(BaseModel):
    entity_id: str
    name: str
    type: str
    confidence: float = Field(default=1.0, ge=0, le=1)
    aliases: list[str] = Field(default_factory=list)


class KnowledgeEngineerReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operation: KnowledgeOperation
    ontology_classes: list[OntologyClass] = Field(default_factory=list)
    relationship_types: list[RelationshipType] = Field(default_factory=list)
    entity_mappings: list[EntityMapping] = Field(default_factory=list)
    semantic_models: dict[str, Any] = Field(default_factory=dict)
    recommendations: list[str] = Field(default_factory=list)
    quality_score: float = Field(default=0.90, ge=0, le=1)
    model_version: str = "1.0.0"


class KnowledgeEngineerRecord(BaseModel):
    pack_id: str = "knowledge-engineer"
    version: str = "1.0.0"
    capabilities: list[str] = Field(
        default_factory=lambda: [
            "ontology_design",
            "knowledge_graph",
            "semantic_search",
            "entity_resolution",
        ]
    )


__all__ = [
    "BusinessContext",
    "EntityMapping",
    "KnowledgeConfig",
    "KnowledgeEngineerRecord",
    "KnowledgeEngineerReport",
    "KnowledgeEngineerRequest",
    "KnowledgeOperation",
    "KnowledgeStoreType",
    "OntologyClass",
    "RelationshipType",
]
