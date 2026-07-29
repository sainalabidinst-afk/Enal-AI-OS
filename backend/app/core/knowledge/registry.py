from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from backend.app.core.knowledge.schema import (
    KnowledgeCategory,
    KnowledgeDomain,
    KnowledgeEntity,
    KnowledgeStatus,
    KnowledgeType,
)
from backend.app.core.knowledge.versioning import KnowledgeVersion, KnowledgeVersionStore


class KnowledgeRegistry:
    def __init__(self) -> None:
        self._entities: dict[str, KnowledgeEntity] = {}
        self._by_domain: dict[KnowledgeDomain, list[str]] = {}
        self._by_category: dict[KnowledgeCategory, list[str]] = {}
        self._versions = KnowledgeVersionStore()

    def register(self, entity: KnowledgeEntity) -> KnowledgeEntity:
        self._entities[entity.id] = entity
        self._by_domain.setdefault(entity.domain, []).append(entity.id)
        self._by_category.setdefault(entity.category, []).append(entity.id)
        return entity

    def resolve(self, entity_id: str) -> KnowledgeEntity | None:
        return self._entities.get(entity_id)

    def find_by_domain(self, domain: KnowledgeDomain) -> list[KnowledgeEntity]:
        ids = self._by_domain.get(domain, [])
        return [self._entities[eid] for eid in ids if eid in self._entities]

    def find_by_category(self, category: KnowledgeCategory) -> list[KnowledgeEntity]:
        ids = self._by_category.get(category, [])
        return [self._entities[eid] for eid in ids if eid in self._entities]

    def find_by_status(self, status: KnowledgeStatus) -> list[KnowledgeEntity]:
        return [e for e in self._entities.values() if e.status == status]

    def find_by_type(self, entity_type: KnowledgeType) -> list[KnowledgeEntity]:
        return [e for e in self._entities.values() if e.type == entity_type]

    def find_by_tag(self, tag: str) -> list[KnowledgeEntity]:
        return [e for e in self._entities.values() if tag in e.tags]

    def find_by_name(self, query: str) -> list[KnowledgeEntity]:
        lowered = query.lower()
        return [e for e in self._entities.values() if lowered in e.name.lower()]

    def all(self) -> list[KnowledgeEntity]:
        return list(self._entities.values())

    def domains(self) -> list[KnowledgeDomain]:
        return list(self._by_domain.keys())

    def categories(self) -> list[KnowledgeCategory]:
        return list(self._by_category.keys())

    def version(self, entity: KnowledgeEntity, version: str, changed_by: str | None = None, change_summary: str = "") -> None:
        kv = KnowledgeVersion(
            entity_id=entity.id,
            version=version,
            changed_by=changed_by,
            change_summary=change_summary,
            snapshot=self._serialize(entity),
        )
        self._versions.record(kv)

    def history(self, entity_id: str) -> list[KnowledgeVersion]:
        return self._versions.history(entity_id)

    def _serialize(self, entity: KnowledgeEntity) -> dict[str, Any]:
        return {
            "id": entity.id,
            "domain": entity.domain.value,
            "category": entity.category.value,
            "type": entity.type.value,
            "name": entity.name,
            "description": entity.description,
            "status": entity.status.value,
            "confidence": entity.confidence,
            "knowledge_version": entity.knowledge_version,
            "updated_at": entity.updated_at.isoformat(),
            "tags": list(entity.tags),
            "metadata": dict(entity.metadata),
            "evidence": list(entity.evidence),
            "related_ids": list(entity.related_ids),
            "source": entity.source,
            "owner": entity.owner,
        }
