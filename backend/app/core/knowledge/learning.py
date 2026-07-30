from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from backend.app.core.knowledge.schema import (
    KnowledgeCategory,
    KnowledgeDomain,
    KnowledgeEntity,
    KnowledgeStatus,
    KnowledgeType,
)


@dataclass
class SuccessPattern:
    pattern_id: str
    domain: str
    context: dict[str, Any]
    action_taken: str
    outcome: str
    confidence: float = 0.0
    occurrences: int = 1
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FailurePattern:
    pattern_id: str
    domain: str
    context: dict[str, Any]
    action_taken: str
    failure_reason: str
    severity: str = "medium"
    occurrences: int = 1
    confidence: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Recommendation:
    recommendation_id: str
    domain: str
    context: dict[str, Any]
    suggestion: str
    rationale: str
    confidence: float = 0.0
    based_on_patterns: list[str] = field(default_factory=list)
    based_on_lessons: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)


class LearningEngine:
    def __init__(self) -> None:
        self._success_patterns: dict[str, SuccessPattern] = {}
        self._failure_patterns: dict[str, FailurePattern] = {}
        self._recommendations: dict[str, Recommendation] = {}

    def record_success(self, domain: str, context: dict[str, Any], action_taken: str, outcome: str, confidence: float = 0.0, metadata: dict[str, Any] | None = None) -> SuccessPattern:
        pattern_id = f"success-{domain}-{datetime.now(timezone.utc).timestamp()}"
        pattern = SuccessPattern(
            pattern_id=pattern_id,
            domain=domain,
            context=context,
            action_taken=action_taken,
            outcome=outcome,
            confidence=confidence,
            metadata=metadata or {},
        )
        self._success_patterns[pattern_id] = pattern
        return pattern

    def record_failure(self, domain: str, context: dict[str, Any], action_taken: str, failure_reason: str, severity: str = "medium", confidence: float = 0.0, metadata: dict[str, Any] | None = None) -> FailurePattern:
        pattern_id = f"failure-{domain}-{datetime.now(timezone.utc).timestamp()}"
        pattern = FailurePattern(
            pattern_id=pattern_id,
            domain=domain,
            context=context,
            action_taken=action_taken,
            failure_reason=failure_reason,
            severity=severity,
            confidence=confidence,
            metadata=metadata or {},
        )
        self._failure_patterns[pattern_id] = pattern
        return pattern

    def recommend(self, domain: str, context: dict[str, Any]) -> Recommendation | None:
        relevant_successes = [p for p in self._success_patterns.values() if p.domain == domain]
        relevant_failures = [p for p in self._failure_patterns.values() if p.domain == domain]
        if not relevant_successes and not relevant_failures:
            return None
        suggestion_parts = []
        rationale_parts = []
        based_on_patterns: list[str] = []
        based_on_lessons: list[str] = []
        if relevant_successes:
            best = max(relevant_successes, key=lambda p: p.confidence)
            suggestion_parts.append(f"Consider: {best.action_taken}")
            rationale_parts.append(f"Matched success pattern with confidence {best.confidence:.2f}")
            based_on_patterns.append(best.pattern_id)
        if relevant_failures:
            worst = max(relevant_failures, key=lambda p: p.confidence)
            suggestion_parts.append(f"Avoid: {worst.action_taken}")
            rationale_parts.append(f"Matched failure pattern ({worst.severity})")
            based_on_patterns.append(worst.pattern_id)
        if not suggestion_parts:
            return None
        recommendation_id = f"recommendation-{domain}-{datetime.now(timezone.utc).timestamp()}"
        recommendation = Recommendation(
            recommendation_id=recommendation_id,
            domain=domain,
            context=context,
            suggestion=" | ".join(suggestion_parts),
            rationale=" | ".join(rationale_parts),
            confidence=sum(p.confidence for p in relevant_successes if p.domain == domain) / max(len(relevant_successes), 1),
            based_on_patterns=based_on_patterns,
            based_on_lessons=based_on_lessons,
        )
        self._recommendations[recommendation_id] = recommendation
        return recommendation

    def success_patterns(self, domain: str | None = None) -> list[SuccessPattern]:
        patterns = list(self._success_patterns.values())
        if domain:
            patterns = [p for p in patterns if p.domain == domain]
        return patterns

    def failure_patterns(self, domain: str | None = None) -> list[FailurePattern]:
        patterns = list(self._failure_patterns.values())
        if domain:
            patterns = [p for p in patterns if p.domain == domain]
        return patterns

    def recommendations(self, domain: str | None = None) -> list[Recommendation]:
        recs = list(self._recommendations.values())
        if domain:
            recs = [r for r in recs if r.domain == domain]
        return recs

    def to_knowledge_entities(self) -> list[KnowledgeEntity]:
        entities: list[KnowledgeEntity] = []
        for pattern in self._success_patterns.values():
            entities.append(KnowledgeEntity(
                id=pattern.pattern_id,
                domain=KnowledgeDomain[pattern.domain.upper()] if pattern.domain.upper() in KnowledgeDomain.__members__ else KnowledgeDomain.EXPERIENCE,
                category=KnowledgeCategory.EXPERIENCE,
                type=KnowledgeType.PATTERN,
                name=f"Success: {pattern.action_taken}",
                description=pattern.outcome,
                status=KnowledgeStatus.VALIDATED,
                confidence=pattern.confidence,
                tags=["success-pattern", pattern.domain],
                metadata=pattern.metadata,
            ))
        for failure in self._failure_patterns.values():
            entities.append(KnowledgeEntity(
                id=failure.pattern_id,
                domain=KnowledgeDomain[failure.domain.upper()] if failure.domain.upper() in KnowledgeDomain.__members__ else KnowledgeDomain.EXPERIENCE,
                category=KnowledgeCategory.EXPERIENCE,
                type=KnowledgeType.PATTERN,
                name=f"Failure: {failure.action_taken}",
                description=failure.failure_reason,
                status=KnowledgeStatus.VALIDATED,
                confidence=failure.confidence,
                tags=["failure-pattern", failure.domain, failure.severity],
                metadata=failure.metadata,
            ))
        return entities
