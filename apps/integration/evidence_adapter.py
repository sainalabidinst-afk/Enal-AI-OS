"""
Unified Evidence Adapter
========================

Bridges the gap between three separate Evidence implementations:
1. Trading Evidence (apps/trading_analyst/market_intelligence/evidence.py)
2. Knowledge Evidence (backend/app/core/knowledge/evidence.py)
3. Reasoning Evidence (apps/organization/reasoning_engine.py)

This adapter normalizes all evidence into a single standard format
that can be consumed by any capability.
"""

from __future__ import annotations

import logging
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


class EvidenceType(str, Enum):
    FACT = "fact"
    OBSERVATION = "observation"
    HYPOTHESIS = "hypothesis"
    DERIVED = "derived"
    CONTRADICTION = "contradiction"
    SUPPORT = "support"
    RULE = "rule"
    CONSTRAINT = "constraint"


@dataclass
class UnifiedEvidence:
    """Standard evidence format across all capabilities."""

    id: str
    source: EvidenceSource
    type: EvidenceType
    content: str
    confidence: float = 0.0
    strength: float = 0.0
    direction: str | None = None
    category: str | None = None
    claim_id: str | None = None
    contradicting_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    raw: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source.value,
            "type": self.type.value,
            "content": self.content,
            "confidence": self.confidence,
            "strength": self.strength,
            "direction": self.direction,
            "category": self.category,
            "claim_id": self.claim_id,
            "contradicting_ids": self.contradicting_ids,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }


class EvidenceAdapter:
    """
    Converts capability-specific evidence to UnifiedEvidence format
    and vice versa.
    """

    def from_trading_evidence(self, trading_evidence: Any) -> UnifiedEvidence:
        """Convert Trading market intelligence evidence to unified format."""
        return UnifiedEvidence(
            id=trading_evidence.id,
            source=EvidenceSource.TRADING,
            type=EvidenceType.OBSERVATION,
            content=trading_evidence.description,
            confidence=trading_evidence.confidence,
            strength=trading_evidence.strength,
            direction=trading_evidence.direction,
            category=getattr(trading_evidence, "category", trading_evidence.type),
            metadata={
                "timeframe": trading_evidence.timeframe,
                "indicator": trading_evidence.source,
                "symbol": getattr(trading_evidence, "symbol", None),
                "type": trading_evidence.type,
            },
            raw={
                "strength": trading_evidence.strength,
                "direction": trading_evidence.direction,
                "timeframe": trading_evidence.timeframe,
                "type": trading_evidence.type,
            },
        )

    def from_knowledge_evidence(self, knowledge_evidence: Any) -> UnifiedEvidence:
        """Convert Knowledge system evidence to unified format."""
        return UnifiedEvidence(
            id=getattr(knowledge_evidence, "id", knowledge_evidence.claim_id),
            source=EvidenceSource.KNOWLEDGE,
            type=EvidenceType.FACT,
            content=knowledge_evidence.content,
            confidence=knowledge_evidence.confidence,
            strength=knowledge_evidence.confidence,
            claim_id=knowledge_evidence.claim_id,
            contradicting_ids=list(knowledge_evidence.contradicting_ids),
            metadata={
                "source": knowledge_evidence.source,
                "source_type": knowledge_evidence.source_type,
                "capability": knowledge_evidence.capability,
                "citations": list(knowledge_evidence.citations),
            },
            raw={
                "claim_id": knowledge_evidence.claim_id,
                "source": knowledge_evidence.source,
                "source_type": knowledge_evidence.source_type,
                "contradicting_ids": list(knowledge_evidence.contradicting_ids),
            },
        )

    def from_reasoning_evidence(self, reasoning_evidence: Any) -> UnifiedEvidence:
        """Convert Reasoning engine evidence to unified format."""
        return UnifiedEvidence(
            id=reasoning_evidence.id,
            source=EvidenceSource.REASONING,
            type=EvidenceType(reasoning_evidence.type.value),
            content=reasoning_evidence.description,
            confidence=reasoning_evidence.confidence,
            strength=reasoning_evidence.confidence,
            category=reasoning_evidence.metadata.get("category"),
            metadata={
                "value": reasoning_evidence.value,
                "source": reasoning_evidence.source,
                "timestamp": reasoning_evidence.timestamp.isoformat() if hasattr(reasoning_evidence.timestamp, "isoformat") else str(reasoning_evidence.timestamp),
            },
            raw={
                "type": reasoning_evidence.type.value,
                "value": reasoning_evidence.value,
            },
        )

    def to_knowledge_evidence(self, unified: UnifiedEvidence) -> Any:
        """Convert unified evidence back to Knowledge system format."""
        from backend.app.core.knowledge.evidence import Evidence
        return Evidence(
            claim_id=unified.claim_id or unified.id,
            content=unified.content,
            source=unified.metadata.get("source_doc", unified.source.value),
            source_type="unified",
            confidence=unified.confidence,
            contradicting_ids=list(unified.contradicting_ids),
            metadata={
                "strength": unified.strength,
                "direction": unified.direction,
                "category": unified.category,
            },
        )

    def aggregate(self, evidences: list[UnifiedEvidence]) -> UnifiedEvidence:
        """Aggregate multiple evidences into a single composite evidence."""
        if not evidences:
            raise ValueError("Cannot aggregate empty evidence list")

        avg_confidence = sum(e.confidence for e in evidences) / len(evidences)
        avg_strength = sum(e.strength for e in evidences) / len(evidences)
        sources = list(set(e.source.value for e in evidences))
        types = list(set(e.type.value for e in evidences))

        combined_content = "; ".join(e.content for e in evidences[:5])
        if len(evidences) > 5:
            combined_content += f" ... (+{len(evidences) - 5} more)"

        return UnifiedEvidence(
            id=f"aggregated_{evidences[0].id[:8]}",
            source=EvidenceSource(sources[0]) if len(sources) == 1 else EvidenceSource.KNOWLEDGE,
            type=EvidenceType.DERIVED,
            content=combined_content,
            confidence=min(avg_confidence, 1.0),
            strength=min(avg_strength, 1.0),
            category=evidences[0].category,
            metadata={
                "aggregated_from": [e.id for e in evidences],
                "source_count": len(evidences),
                "sources": sources,
                "types": types,
            },
            raw={
                "evidence_count": len(evidences),
                "avg_confidence": avg_confidence,
                "avg_strength": avg_strength,
            },
        )
