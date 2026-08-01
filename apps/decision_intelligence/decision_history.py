"""
Decision History — record decisions to Experience Memory.

Persists a structured, queryable record of every decision for learning,
audit, and rollback support.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from apps.decision_intelligence.schemas import (
    DecisionOutcome,
    DecisionRecord,
)

logger = logging.getLogger(__name__)


class DecisionHistoryStore:
    """
    In-memory + optional file-backed store for decision records.

    The default storage location is `artifacts/decision_history/`.
    This store is intentionally lightweight and satisfies the RFC-0007
    interface. Experience Memory integration can swap in the platform
    memory service without changing the record schema.

    Usage::

        store = DecisionHistoryStore()
        ref = store.record(decision_record)
        records = store.list_recent(limit=10)
    """

    def __init__(self, base_dir: str | Path | None = None) -> None:
        self._records: list[DecisionRecord] = []
        self._by_id: dict[str, DecisionRecord] = {}
        if base_dir is None:
            base_dir = Path("artifacts") / "decision_history"
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def record(self, record: DecisionRecord) -> str:
        """Persist a decision record and return its record_id."""
        self._records.append(record)
        self._by_id[record.record_id] = record

        # Persist to disk as JSON for durability.
        try:
            path = self._path_for(record.record_id)
            path.write_text(
                json.dumps(record.model_dump(), indent=2, default=str),
                encoding="utf-8",
            )
        except OSError as exc:  # pragma: no cover - filesystem boundary
            logger.warning("Failed to persist decision record %s: %s", record.record_id, exc)

        return record.record_id

    def get(self, record_id: str) -> DecisionRecord | None:
        """Retrieve a record by ID."""
        return self._by_id.get(record_id)

    def list_recent(self, limit: int = 20) -> list[DecisionRecord]:
        """Return the most recent records (newest first)."""
        sorted_records = sorted(
            self._records,
            key=lambda r: r.timestamp,
            reverse=True,
        )
        return sorted_records[:limit]

    def update_outcome(
        self,
        record_id: str,
        outcome: DecisionOutcome,
        user_feedback: str | None = None,
    ) -> DecisionRecord | None:
        """Update the outcome of a decision record."""
        record = self._by_id.get(record_id)
        if record is None:
            return None
        record.outcome = outcome
        if user_feedback is not None:
            record.user_feedback = user_feedback
        record.revision_history.append(
            {
                "revision_id": f"rev-{len(record.revision_history) + 1}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "changes": f"outcome -> {outcome.value}",
            }
        )
        return record

    def count(self) -> int:
        """Total number of stored records."""
        return len(self._records)

    def export_recent(self, limit: int = 50) -> list[dict[str, Any]]:
        """Export recent records as plain dicts (JSON-serializable)."""
        return [r.model_dump() for r in self.list_recent(limit)]

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _path_for(self, record_id: str) -> Path:
        safe = "".join(c for c in record_id if c.isalnum() or c in "-_")
        return self.base_dir / f"{safe}.json"

