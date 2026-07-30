"""
Knowledge K3 — Evidence Intelligence
======================================

Enhances evidence with:
- Source tracking
- Version tracking
- Timestamp
- Confidence scoring with decay
- Conflict detection across capabilities
- Citation chain

Design:
    Capability A produces Evidence
         ↓
    Evidence Intelligence
         ↓
    ├── Version tracking
    ├── Conflict detection
    ├── Confidence propagation
    └── Citation chain
         ↓
    Reasoning Engine consumes enriched evidence
"""

from __future__ import annotations

import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class EvidenceSource(str, Enum):
    TRADING = "trading"
    NETWORK = "network"
    CODE = "code"
    SECURITY = "security"
    DEVOPS = "devops"
    RESEARCH = "research"
    KNOWLEDGE = "knowledge"
    REASONING = "reasoning"
    SELF_IMPROVEMENT = "self_improvement"
    USER = "user"
    SYSTEM = "system"


class EvidenceType(str, Enum):
    FACT = "fact"
    OBSERVATION = "observation"
    HYPOTHESIS = "hypothesis"
    DERIVED = "derived"
    CONTRADICTION = "contradiction"
    SUPPORT = "support"
    RULE = "rule"
    CONSTRAINT = "constraint"
    LESSON = "lesson"
    TELEMETRY = "telemetry"


@dataclass
class EvidenceVersion:
    version: int
    timestamp: datetime
    source: str
    content: str
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvidenceRecord:
    """Enhanced evidence with versioning, conflict detection, and citation."""
    id: str = field(default_factory=lambda: f"ev-{uuid.uuid4().hex[:12]}")
    claim_id: str = ""
    content: str = ""
    source: EvidenceSource = EvidenceSource.SYSTEM
    evidence_type: EvidenceType = EvidenceType.OBSERVATION
    confidence: float = 0.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    version: int = 1
    versions: list[EvidenceVersion] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)
    contradicting_ids: list[str] = field(default_factory=list)
    supporting_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    capability: str | None = None
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "claim_id": self.claim_id,
            "content": self.content,
            "source": self.source.value,
            "evidence_type": self.evidence_type.value,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
            "versions": [
                {
                    "version": v.version,
                    "timestamp": v.timestamp.isoformat(),
                    "source": v.source,
                    "content": v.content,
                    "confidence": v.confidence,
                    "metadata": v.metadata,
                }
                for v in self.versions
            ],
            "citations": self.citations,
            "contradicting_ids": self.contradicting_ids,
            "supporting_ids": self.supporting_ids,
            "metadata": self.metadata,
            "capability": self.capability,
            "tags": self.tags,
        }


class EvidenceConflict:
    """Represents a conflict between two pieces of evidence."""

    def __init__(self, evidence_a: EvidenceRecord, evidence_b: EvidenceRecord):
        self.evidence_a = evidence_a
        self.evidence_b = evidence_b
        self.confidence_a = evidence_a.confidence
        self.confidence_b = evidence_b.confidence
        self.detected_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_a_id": self.evidence_a.id,
            "evidence_b_id": self.evidence_b.id,
            "claim_a": self.evidence_a.claim_id,
            "claim_b": self.evidence_b.claim_id,
            "content_a": self.evidence_a.content,
            "content_b": self.evidence_b.content,
            "confidence_a": self.confidence_a,
            "confidence_b": self.confidence_b,
            "detected_at": self.detected_at.isoformat(),
            "resolution": "unresolved",
        }


class EvidenceIntelligenceEngine:
    """Manages evidence lifecycle: creation, versioning, conflict detection, and citation."""

    def __init__(self):
        self._evidence: dict[str, EvidenceRecord] = {}
        self._conflicts: list[EvidenceConflict] = []
        self._claim_index: dict[str, list[str]] = {}

    def create(
        self,
        claim_id: str,
        content: str,
        source: EvidenceSource = EvidenceSource.SYSTEM,
        evidence_type: EvidenceType = EvidenceType.OBSERVATION,
        confidence: float = 0.0,
        capability: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> EvidenceRecord:
        evidence = EvidenceRecord(
            claim_id=claim_id,
            content=content,
            source=source,
            evidence_type=evidence_type,
            confidence=confidence,
            capability=capability,
            tags=tags or [],
            metadata=metadata or {},
        )
        self._evidence[evidence.id] = evidence
        self._claim_index.setdefault(claim_id, []).append(evidence.id)
        logger.debug("Evidence created: %s for claim %s", evidence.id, claim_id)
        return evidence

    def update(self, evidence_id: str, content: str, confidence: float, source: str = "system") -> EvidenceRecord | None:
        record = self._evidence.get(evidence_id)
        if not record:
            return None
        record.versions.append(EvidenceVersion(
            version=record.version,
            timestamp=record.timestamp,
            source=record.source.value,
            content=record.content,
            confidence=record.confidence,
            metadata=dict(record.metadata),
        ))
        record.version += 1
        record.content = content
        record.confidence = confidence
        record.timestamp = datetime.now(timezone.utc)
        record.metadata.setdefault("updated_by", source)
        logger.debug("Evidence updated: %s to version %d", evidence_id, record.version)
        return record

    def add_citation(self, evidence_id: str, cited_evidence_id: str) -> bool:
        record = self._evidence.get(evidence_id)
        if not record or cited_evidence_id not in self._evidence:
            return False
        if cited_evidence_id not in record.citations:
            record.citations.append(cited_evidence_id)
        cited = self._evidence[cited_evidence_id]
        if evidence_id not in cited.supporting_ids:
            cited.supporting_ids.append(evidence_id)
        logger.debug("Citation added: %s -> %s", evidence_id, cited_evidence_id)
        return True

    def register_conflict(self, evidence_a_id: str, evidence_b_id: str) -> EvidenceConflict | None:
        a = self._evidence.get(evidence_a_id)
        b = self._evidence.get(evidence_b_id)
        if not a or not b:
            return None
        a.contradicting_ids.append(evidence_b_id)
        b.contradicting_ids.append(evidence_a_id)
        conflict = EvidenceConflict(a, b)
        self._conflicts.append(conflict)
        logger.info("Conflict registered: %s vs %s", evidence_a_id, evidence_b_id)
        return conflict

    def detect_conflicts_for_claim(self, claim_id: str) -> list[EvidenceConflict]:
        claim_evidence_ids = self._claim_index.get(claim_id, [])
        if len(claim_evidence_ids) < 2:
            return []
        conflicts = []
        for i in range(len(claim_evidence_ids)):
            for j in range(i + 1, len(claim_evidence_ids)):
                a_id = claim_evidence_ids[i]
                b_id = claim_evidence_ids[j]
                a = self._evidence.get(a_id)
                b = self._evidence.get(b_id)
                if a and b and a.confidence > 0.3 and b.confidence > 0.3:
                    if abs(a.confidence - b.confidence) > 0.4 or (
                        a.content.lower() != b.content.lower() and not b.content.lower().startswith(a.content.lower())
                    ):
                        conflict = EvidenceConflict(a, b)
                        conflicts.append(conflict)
        return conflicts

    def get_evidence_for_claim(self, claim_id: str) -> list[EvidenceRecord]:
        return [self._evidence[eid] for eid in self._claim_index.get(claim_id, []) if eid in self._evidence]

    def get_confidence(self, claim_id: str, decay: float = 0.95) -> float:
        entries = self.get_evidence_for_claim(claim_id)
        if not entries:
            return 0.0
        direct = sum(e.confidence for e in entries) / len(entries)
        if direct > 0:
            return direct
        return 0.0

    def get_conflicts(self) -> list[EvidenceConflict]:
        return list(self._conflicts)

    def propagate_confidence(self, claim_id: str, decay: float = 0.95) -> float:
        direct = self.get_confidence(claim_id)
        if direct > 0:
            return direct
        related_claims = [cid for cid in self._claim_index if cid != claim_id]
        if not related_claims:
            return 0.0
        propagated = sum(self.get_confidence(cid) * (decay ** 1) for cid in related_claims) / len(related_claims)
        return propagated

    def enrich_for_reasoning(self, claim_id: str) -> dict[str, Any]:
        evidence = self.get_evidence_for_claim(claim_id)
        conflicts = [c for c in self._conflicts if c.evidence_a.claim_id == claim_id or c.evidence_b.claim_id == claim_id]
        supporting = [e for e in evidence if not e.contradicting_ids]
        contradicting = [e for e in evidence if e.contradicting_ids]
        return {
            "claim_id": claim_id,
            "confidence": self.get_confidence(claim_id),
            "evidence_count": len(evidence),
            "supporting_count": len(supporting),
            "contradicting_count": len(contradicting),
            "conflicts": [c.to_dict() for c in conflicts],
            "evidence": [e.to_dict() for e in sorted(evidence, key=lambda e: e.confidence, reverse=True)],
        }

    def all(self) -> dict[str, EvidenceRecord]:
        return dict(self._evidence)


evidence_intelligence_engine = EvidenceIntelligenceEngine()