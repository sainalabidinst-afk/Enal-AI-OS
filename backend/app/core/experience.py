import json
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import TypedDict

logger = logging.getLogger(__name__)


def _empty_tags() -> list[str]:
    return []


class LessonData(TypedDict):
    id: str
    project_id: str
    category: str
    situation: str
    action_taken: str
    outcome: str
    quality_score: float
    timestamp: str
    tags: list[str]


@dataclass
class Lesson:
    id: str
    project_id: str
    category: str
    situation: str
    action_taken: str
    outcome: str
    quality_score: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    tags: list[str] = field(default_factory=_empty_tags)


class ExperienceLearning:
    def __init__(self, base_path: str = "./workspace/memory/experience"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._lessons: dict[str, Lesson] = {}

    def record(
        self,
        project_id: str,
        category: str,
        situation: str,
        action_taken: str,
        outcome: str,
        quality_score: float,
        tags: list[str] | None = None,
    ):
        lesson_id = f"lesson-{datetime.now(UTC).timestamp()}"
        lesson_tags = tags or []

        lesson = Lesson(
            id=lesson_id,
            project_id=project_id,
            category=category,
            situation=situation,
            action_taken=action_taken,
            outcome=outcome,
            quality_score=quality_score,
            tags=lesson_tags,
        )
        self._lessons[lesson_id] = lesson
        self._persist(lesson)
        logger.info(f"Lesson recorded: {lesson_id} ({category})")
        return lesson_id

    def search(
        self,
        query: str,
        category: str | None = None,
        limit: int = 5,
    ) -> list[Lesson]:
        results: list[Lesson] = list(self._lessons.values())
        if category:
            results = [lesson for lesson in results if lesson.category == category]

        scored: list[tuple[int, Lesson]] = []
        q = query.lower()
        for lesson in results:
            score: int = 0
            if q in lesson.situation.lower():
                score += 2
            if q in lesson.action_taken.lower():
                score += 1
            if q in lesson.outcome.lower():
                score += 1
            scored.append((score, lesson))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [lesson for _, lesson in scored[:limit]]

    def get_by_project(self, project_id: str) -> list[Lesson]:
        return [lesson for lesson in self._lessons.values() if lesson.project_id == project_id]

    def _persist(self, lesson: Lesson) -> None:
        path = self.base_path / f"{lesson.id}.json"
        data: LessonData = {
            "id": lesson.id,
            "project_id": lesson.project_id,
            "category": lesson.category,
            "situation": lesson.situation,
            "action_taken": lesson.action_taken,
            "outcome": lesson.outcome,
            "quality_score": lesson.quality_score,
            "timestamp": lesson.timestamp.isoformat(),
            "tags": lesson.tags,
        }
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load_all(self) -> None:
        for path in self.base_path.glob("*.json"):
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
                data: LessonData = raw

                tags_raw = data.get("tags") or []
                lesson_tags = [str(t) for t in tags_raw]

                lesson = Lesson(
                    id=data["id"],
                    project_id=data["project_id"],
                    category=data["category"],
                    situation=data["situation"],
                    action_taken=data["action_taken"],
                    outcome=data["outcome"],
                    quality_score=data["quality_score"],
                    timestamp=datetime.fromisoformat(data["timestamp"]),
                    tags=lesson_tags,
                )
                self._lessons[lesson.id] = lesson
            except Exception as e:
                logger.error(f"Failed to load lesson {path}: {e}")


experience_learning = ExperienceLearning()
