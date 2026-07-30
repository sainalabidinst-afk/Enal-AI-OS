from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class Evidence:
    claim_id: str
    content: str
    source: str
    source_type: str = "manual"
    confidence: float = 0.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    capability: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    citations: list[str] = field(default_factory=list)
    contradicting_ids: list[str] = field(default_factory=list)


class EvidenceBuilder:
    def __init__(self, claim_id: str, capability: str | None = None) -> None:
        self.claim_id = claim_id
        self.capability = capability
        self._items: list[Evidence] = []

    def add(self, content: str, source: str, source_type: str = "manual", confidence: float = 0.0, metadata: dict[str, Any] | None = None) -> EvidenceBuilder:
        evidence = Evidence(
            claim_id=self.claim_id,
            content=content,
            source=source,
            source_type=source_type,
            confidence=confidence,
            capability=self.capability,
            metadata=metadata or {},
        )
        self._items.append(evidence)
        return self

    def build(self) -> list[Evidence]:
        return list(self._items)


class ConfidencePropagator:
    def __init__(self, evidence_store: EvidenceStore) -> None:
        self.evidence_store = evidence_store

    def propagate(self, claim_id: str, decay: float = 0.95) -> float:
        direct = self.evidence_store.confidence(claim_id)
        if direct > 0:
            return direct
        related_claims = [cid for cid in self.evidence_store.all().keys() if cid != claim_id]
        if not related_claims:
            return 0.0
        propagated = sum(self.evidence_store.confidence(cid) * (decay ** 1) for cid in related_claims) / len(related_claims)
        return propagated


class ConflictDetector:
    def __init__(self, evidence_store: EvidenceStore) -> None:
        self.evidence_store = evidence_store

    def detect(self, claim_id: str) -> list[tuple[str, str, float]]:
        conflicts: list[tuple[str, str, float]] = []
        for cid, entries in self.evidence_store.all().items():
            if cid == claim_id:
                continue
            for entry in entries:
                if claim_id in entry.contradicting_ids:
                    conflicts.append((cid, entry.content, entry.confidence))
        return conflicts

    def register_conflict(self, claim_id_a: str, claim_id_b: str) -> None:
        for cid in [claim_id_a, claim_id_b]:
            for entry in self.evidence_store.get(cid):
                if claim_id_b not in entry.contradicting_ids:
                    entry.contradicting_ids.append(claim_id_b)


@dataclass
class EvidenceStore:
    _evidence: dict[str, list[Evidence]] = field(default_factory=dict)

    def add(self, evidence: Evidence) -> None:
        self._evidence.setdefault(evidence.claim_id, []).append(evidence)

    def get(self, claim_id: str) -> list[Evidence]:
        return self._evidence.get(claim_id, [])

    def all(self) -> dict[str, list[Evidence]]:
        return dict(self._evidence)

    def confidence(self, claim_id: str) -> float:
        entries = self._evidence.get(claim_id, [])
        if not entries:
            return 0.0
        return sum(e.confidence for e in entries) / len(entries)

    def citations(self, claim_id: str) -> list[str]:
        citations: list[str] = []
        for entries in self._evidence.values():
            for entry in entries:
                if claim_id in entry.citations:
                    citations.append(entry.claim_id)
        return citations
