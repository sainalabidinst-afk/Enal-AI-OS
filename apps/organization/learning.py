"""
Organizational Learning
========================

Post-project learning system.
Captures lessons learned, best practices, reusable assets, and mistakes.
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class LessonLearned:
    id: str
    project_id: str
    category: str
    description: str
    impact: str
    recommendation: str
    confidence: float = 1.0
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class BestPractice:
    id: str
    name: str
    description: str
    context: str
    evidence: str
    applicability: list[str] = field(default_factory=list)
    confidence: float = 1.0


@dataclass
class ReusableAsset:
    id: str
    name: str
    asset_type: str
    content: Any
    description: str
    tags: list[str] = field(default_factory=list)
    usage_count: int = 0
    success_rate: float = 0.0


@dataclass
class MistakeRecord:
    id: str
    project_id: str
    severity: str
    description: str
    root_cause: str
    impact: str
    remediation: str
    tags: list[str] = field(default_factory=list)


class OrganizationalLearning:
    """Captures and retrieves organizational knowledge."""

    def __init__(self):
        self._lessons: dict[str, LessonLearned] = {}
        self._best_practices: dict[str, BestPractice] = {}
        self._reusable_assets: dict[str, ReusableAsset] = {}
        self._mistakes: dict[str, MistakeRecord] = {}
        self._project_learnings: dict[str, list[str]] = {}

    def record_lesson(self, project_id: str, category: str, description: str, impact: str, recommendation: str, confidence: float = 1.0, tags: list[str] | None = None) -> LessonLearned:
        lesson_id = f"lesson-{uuid.uuid4().hex[:8]}"
        lesson = LessonLearned(
            id=lesson_id,
            project_id=project_id,
            category=category,
            description=description,
            impact=impact,
            recommendation=recommendation,
            confidence=confidence,
            tags=tags or [],
        )
        self._lessons[lesson_id] = lesson
        self._project_learnings.setdefault(project_id, []).append(lesson_id)
        logger.info("Lesson recorded: %s for project %s", category, project_id)
        return lesson

    def record_best_practice(self, name: str, description: str, context: str, evidence: str, applicability: list[str] | None = None) -> BestPractice:
        practice_id = f"practice-{uuid.uuid4().hex[:8]}"
        practice = BestPractice(
            id=practice_id,
            name=name,
            description=description,
            context=context,
            evidence=evidence,
            applicability=applicability or [],
        )
        self._best_practices[practice_id] = practice
        logger.info("Best practice recorded: %s", name)
        return practice

    def record_reusable_asset(self, name: str, asset_type: str, content: Any, description: str, tags: list[str] | None = None) -> ReusableAsset:
        asset_id = f"asset-{uuid.uuid4().hex[:8]}"
        asset = ReusableAsset(
            id=asset_id,
            name=name,
            asset_type=asset_type,
            content=content,
            description=description,
            tags=tags or [],
        )
        self._reusable_assets[asset_id] = asset
        logger.info("Reusable asset recorded: %s (%s)", name, asset_type)
        return asset

    def record_mistake(self, project_id: str, severity: str, description: str, root_cause: str, impact: str, remediation: str, tags: list[str] | None = None) -> MistakeRecord:
        mistake_id = f"mistake-{uuid.uuid4().hex[:8]}"
        mistake = MistakeRecord(
            id=mistake_id,
            project_id=project_id,
            severity=severity,
            description=description,
            root_cause=root_cause,
            impact=impact,
            remediation=remediation,
            tags=tags or [],
        )
        self._mistakes[mistake_id] = mistake
        logger.warning("Mistake recorded: %s (severity: %s)", description, severity)
        return mistake

    def get_project_lessons(self, project_id: str) -> list[LessonLearned]:
        lesson_ids = self._project_learnings.get(project_id, [])
        return [self._lessons[lid] for lid in lesson_ids if lid in self._lessons]

    def get_best_practices(self, context: str | None = None) -> list[BestPractice]:
        practices = list(self._best_practices.values())
        if context:
            practices = [p for p in practices if context in p.applicability or context in p.context]
        return practices

    def get_reusable_assets(self, asset_type: str | None = None, tags: list[str] | None = None) -> list[ReusableAsset]:
        assets = list(self._reusable_assets.values())
        if asset_type:
            assets = [a for a in assets if a.asset_type == asset_type]
        if tags:
            assets = [a for a in assets if any(tag in a.tags for tag in tags)]
        return assets

    def get_mistakes(self, severity: str | None = None) -> list[MistakeRecord]:
        mistakes = list(self._mistakes.values())
        if severity:
            mistakes = [m for m in mistakes if m.severity == severity]
        return mistakes

    def get_learning_summary(self, project_id: str) -> dict[str, Any]:
        lessons = self.get_project_lessons(project_id)
        project_mistakes = [m for m in self._mistakes.values() if m.project_id == project_id]
        return {
            "project_id": project_id,
            "lessons_learned": len(lessons),
            "mistakes": len(project_mistakes),
            "lessons": [
                {
                    "category": l.category,
                    "description": l.description,
                    "impact": l.impact,
                    "recommendation": l.recommendation,
                }
                for l in lessons
            ],
            "mistakes_detail": [
                {
                    "severity": m.severity,
                    "description": m.description,
                    "root_cause": m.root_cause,
                    "remediation": m.remediation,
                }
                for m in project_mistakes
            ],
        }


organizational_learning = OrganizationalLearning()
