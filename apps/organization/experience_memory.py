"""
Knowledge K4 — Experience Memory
==================================

Connects execution history to knowledge and evidence.

Pipeline:
    Execution
        ↓
    Evidence
        ↓
    Result
        ↓
    User Feedback
        ↓
    Lessons Learned
        ↓
    Knowledge Update

This is the foundation for Self-Improvement.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ExecutionRecord:
    """Single execution event with inputs, outputs, and outcomes."""
    execution_id: str
    capability_id: str
    subtask_id: str
    status: str
    started_at: datetime
    finished_at: datetime | None = None
    duration_seconds: float = 0.0
    input_hash: str = ""
    output: dict[str, Any] | None = None
    error: str | None = None
    evidence_ids: list[str] = field(default_factory=list)
    user_feedback: str | None = None
    user_rating: float | None = None
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "capability_id": self.capability_id,
            "subtask_id": self.subtask_id,
            "status": self.status,
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "duration_seconds": self.duration_seconds,
            "input_hash": self.input_hash,
            "output": self.output,
            "error": self.error,
            "evidence_ids": self.evidence_ids,
            "user_feedback": self.user_feedback,
            "user_rating": self.user_rating,
            "tags": self.tags,
            "metadata": self.metadata,
        }


@dataclass
class LessonLearned:
    """Derived lesson from execution experience."""
    id: str
    execution_id: str
    capability_id: str
    category: str
    situation: str
    action_taken: str
    outcome: str
    quality_score: float
    root_cause: str | None = None
    recommendation: str | None = None
    evidence_ids: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "execution_id": self.execution_id,
            "capability_id": self.capability_id,
            "category": self.category,
            "situation": self.situation,
            "action_taken": self.action_taken,
            "outcome": self.outcome,
            "quality_score": self.quality_score,
            "root_cause": self.root_cause,
            "recommendation": self.recommendation,
            "evidence_ids": self.evidence_ids,
            "timestamp": self.timestamp.isoformat(),
            "tags": self.tags,
            "metadata": self.metadata,
        }


class ExperienceMemory:
    """Stores and retrieves execution experiences and derived lessons."""

    def __init__(self):
        self._executions: dict[str, ExecutionRecord] = {}
        self._lessons: dict[str, LessonLearned] = {}
        self._capability_index: dict[str, list[str]] = {}
        self._execution_index: dict[str, list[str]] = {}

    def record_execution(
        self,
        capability_id: str,
        subtask_id: str,
        status: str,
        started_at: datetime,
        finished_at: datetime | None = None,
        output: dict[str, Any] | None = None,
        error: str | None = None,
        evidence_ids: list[str] | None = None,
        user_feedback: str | None = None,
        user_rating: float | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ExecutionRecord:
        execution_id = f"exec-{uuid.uuid4().hex[:12]}"
        duration = 0.0
        if finished_at and started_at:
            duration = (finished_at - started_at).total_seconds()
        record = ExecutionRecord(
            execution_id=execution_id,
            capability_id=capability_id,
            subtask_id=subtask_id,
            status=status,
            started_at=started_at,
            finished_at=finished_at,
            duration_seconds=duration,
            output=output,
            error=error,
            evidence_ids=evidence_ids or [],
            user_feedback=user_feedback,
            user_rating=user_rating,
            tags=tags or [],
            metadata=metadata or {},
        )
        self._executions[execution_id] = record
        self._capability_index.setdefault(capability_id, []).append(execution_id)
        self._execution_index.setdefault(subtask_id, []).append(execution_id)
        logger.debug("Execution recorded: %s for capability %s", execution_id, capability_id)
        return record

    def record_lesson(
        self,
        execution_id: str,
        capability_id: str,
        category: str,
        situation: str,
        action_taken: str,
        outcome: str,
        quality_score: float,
        root_cause: str | None = None,
        recommendation: str | None = None,
        evidence_ids: list[str] | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> LessonLearned:
        lesson_id = f"lesson-{uuid.uuid4().hex[:8]}"
        lesson = LessonLearned(
            id=lesson_id,
            execution_id=execution_id,
            capability_id=capability_id,
            category=category,
            situation=situation,
            action_taken=action_taken,
            outcome=outcome,
            quality_score=quality_score,
            root_cause=root_cause,
            recommendation=recommendation,
            evidence_ids=evidence_ids or [],
            tags=tags or [],
            metadata=metadata or {},
        )
        self._lessons[lesson_id] = lesson
        logger.info("Lesson learned recorded: %s (%s)", lesson_id, category)
        return lesson

    def get_execution(self, execution_id: str) -> ExecutionRecord | None:
        return self._executions.get(execution_id)

    def get_lessons_for_capability(self, capability_id: str) -> list[LessonLearned]:
        return [lesson for lesson in self._lessons.values() if lesson.capability_id == capability_id]

    def get_lessons_for_execution(self, execution_id: str) -> list[LessonLearned]:
        return [lesson for lesson in self._lessons.values() if lesson.execution_id == execution_id]

    def get_recent_executions(self, capability_id: str | None = None, limit: int = 10) -> list[ExecutionRecord]:
        if capability_id:
            ids = self._capability_index.get(capability_id, [])
            records = [self._executions[eid] for eid in ids if eid in self._executions]
        else:
            records = list(self._executions.values())
        records.sort(key=lambda r: r.started_at, reverse=True)
        return records[:limit]

    def get_recent_lessons(self, capability_id: str | None = None, limit: int = 10) -> list[LessonLearned]:
        if capability_id:
            lessons = self.get_lessons_for_capability(capability_id)
        else:
            lessons = list(self._lessons.values())
        lessons.sort(key=lambda l: l.timestamp, reverse=True)
        return lessons[:limit]

    def get_quality_trend(self, capability_id: str) -> dict[str, Any]:
        lessons = self.get_lessons_for_capability(capability_id)
        if not lessons:
            return {"capability_id": capability_id, "average_quality": 0.0, "count": 0}
        scores = [l.quality_score for l in lessons]
        return {
            "capability_id": capability_id,
            "average_quality": round(sum(scores) / len(scores), 3),
            "count": len(scores),
            "min": round(min(scores), 3),
            "max": round(max(scores), 3),
        }

    def search(self, query: str, capability_id: str | None = None, limit: int = 5) -> list[dict[str, Any]]:
        q = query.lower()
        results: list[tuple[float, ExecutionRecord | LessonLearned]] = []
        candidates = list(self._executions.values()) + list(self._lessons.values())
        for item in candidates:
            if capability_id and hasattr(item, "capability_id") and item.capability_id != capability_id:
                continue
            text = str(item.to_dict()).lower()
            score = 0
            if q in text:
                score += 1
            if hasattr(item, "tags"):
                for tag in item.tags:
                    if q in tag.lower():
                        score += 2
            if score > 0:
                results.append((score, item))
        results.sort(key=lambda x: x[0], reverse=True)
        return [item.to_dict() for _, item in results[:limit]]

    def to_knowledge_update(self, capability_id: str | None = None) -> list[dict[str, Any]]:
        """Convert recent lessons into knowledge update proposals."""
        lessons = self.get_recent_lessons(capability_id=capability_id, limit=20)
        updates = []
        for lesson in lessons:
            if lesson.quality_score >= 0.7:
                updates.append({
                    "type": "lesson_learned",
                    "source": "experience_memory",
                    "capability_id": lesson.capability_id,
                    "category": lesson.category,
                    "content": lesson.outcome,
                    "recommendation": lesson.recommendation,
                    "confidence": lesson.quality_score,
                    "evidence_ids": lesson.evidence_ids,
                    "tags": lesson.tags,
                    "timestamp": lesson.timestamp.isoformat(),
                })
        return updates


experience_memory = ExperienceMemory()