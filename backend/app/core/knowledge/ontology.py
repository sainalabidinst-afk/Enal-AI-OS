from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class OntologyEntityType(str, Enum):
    CONCEPT = "concept"
    RELATION = "relation"
    RULE = "rule"
    PROCEDURE = "procedure"
    PATTERN = "pattern"
    EVIDENCE = "evidence"
    LESSON = "lesson"
    REFERENCE = "reference"
    CAPABILITY = "capability"
    OUTCOME = "outcome"


@dataclass
class OntologyEntity:
    entity_id: str
    entity_type: OntologyEntityType
    name: str
    description: str = ""
    parent_id: str | None = None
    properties: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class OntologyRelation:
    relation_id: str
    source_id: str
    target_id: str
    relation_type: str
    weight: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)


class Ontology:
    def __init__(self) -> None:
        self._entities: dict[str, OntologyEntity] = {}
        self._relations: dict[str, OntologyRelation] = {}
        self._by_type: dict[OntologyEntityType, list[str]] = {}

    def add_entity(self, entity: OntologyEntity) -> OntologyEntity:
        self._entities[entity.entity_id] = entity
        self._by_type.setdefault(entity.entity_type, []).append(entity.entity_id)
        return entity

    def add_relation(self, relation: OntologyRelation) -> OntologyRelation:
        self._relations[relation.relation_id] = relation
        return relation

    def get_entity(self, entity_id: str) -> OntologyEntity | None:
        return self._entities.get(entity_id)

    def get_relations(self, source_id: str | None = None, target_id: str | None = None, relation_type: str | None = None) -> list[OntologyRelation]:
        results = list(self._relations.values())
        if source_id is not None:
            results = [r for r in results if r.source_id == source_id]
        if target_id is not None:
            results = [r for r in results if r.target_id == target_id]
        if relation_type is not None:
            results = [r for r in results if r.relation_type == relation_type]
        return results

    def get_children(self, parent_id: str) -> list[OntologyEntity]:
        return [e for e in self._entities.values() if e.parent_id == parent_id]

    def get_parent(self, entity_id: str) -> OntologyEntity | None:
        entity = self._entities.get(entity_id)
        if entity and entity.parent_id:
            return self._entities.get(entity.parent_id)
        return None

    def get_by_type(self, entity_type: OntologyEntityType) -> list[OntologyEntity]:
        ids = self._by_type.get(entity_type, [])
        return [self._entities[eid] for eid in ids if eid in self._entities]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entities": [
                {
                    "entity_id": e.entity_id,
                    "entity_type": e.entity_type.value,
                    "name": e.name,
                    "description": e.description,
                    "parent_id": e.parent_id,
                    "properties": e.properties,
                    "metadata": e.metadata,
                }
                for e in self._entities.values()
            ],
            "relations": [
                {
                    "relation_id": r.relation_id,
                    "source_id": r.source_id,
                    "target_id": r.target_id,
                    "relation_type": r.relation_type,
                    "weight": r.weight,
                    "metadata": r.metadata,
                }
                for r in self._relations.values()
            ],
        }
