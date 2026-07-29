from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Evidence:
    claim_id: str
    content: str
    source: str
    source_type: str = "manual"
    confidence: float = 0.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    capability: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


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
