import json
from pathlib import Path

import pytest

from backend.app.core.experience import ExperienceLearning, Lesson


class TestEmptyTags:
    def test_returns_empty_list(self):
        from backend.app.core.experience import _empty_tags
        assert _empty_tags() == []


class TestLesson:
    def test_defaults(self):
        lesson = Lesson(
            id="l1",
            project_id="p1",
            category="test",
            situation="s",
            action_taken="a",
            outcome="o",
            quality_score=0.8,
        )
        assert lesson.tags == []
        assert lesson.timestamp is not None

    def test_custom_tags(self):
        lesson = Lesson(
            id="l1",
            project_id="p1",
            category="test",
            situation="s",
            action_taken="a",
            outcome="o",
            quality_score=0.8,
            tags=["tag1", "tag2"],
        )
        assert lesson.tags == ["tag1", "tag2"]


class TestExperienceLearning:
    @pytest.fixture
    def manager(self, tmp_path):
        return ExperienceLearning(base_path=str(tmp_path))

    def test_record_creates_lesson(self, manager):
        lesson_id = manager.record(
            project_id="p1",
            category="test",
            situation="situation",
            action_taken="action",
            outcome="outcome",
            quality_score=0.9,
        )
        assert lesson_id.startswith("lesson-")
        assert lesson_id in manager._lessons

    def test_record_with_tags(self, manager):
        lesson_id = manager.record(
            project_id="p1",
            category="test",
            situation="s",
            action_taken="a",
            outcome="o",
            quality_score=0.5,
            tags=["fast", "reliable"],
        )
        assert manager._lessons[lesson_id].tags == ["fast", "reliable"]

    def test_search_returns_matching_lessons(self, manager):
        from unittest.mock import patch
        import backend.app.core.experience as exp_module
        from datetime import datetime, UTC

        with patch.object(exp_module, "datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
            mock_dt.UTC = UTC
            manager.record("p1", "bug", "login fails", "fix auth", "works", 0.9)
            mock_dt.now.return_value = datetime(2024, 1, 1, 12, 0, 1, tzinfo=UTC)
            manager.record("p1", "bug", "api fails", "fix endpoint", "works", 0.7)
        results = manager.search("login")
        assert len(results) >= 1
        assert results[0].situation == "login fails"

    def test_search_filters_by_category(self, manager):
        from unittest.mock import patch
        import backend.app.core.experience as exp_module
        from datetime import datetime, UTC

        with patch.object(exp_module, "datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
            mock_dt.UTC = UTC
            manager.record("p1", "bug", "s1", "a1", "o1", 0.9)
            mock_dt.now.return_value = datetime(2024, 1, 1, 12, 0, 1, tzinfo=UTC)
            manager.record("p1", "feature", "s2", "a2", "o2", 0.8)
        results = manager.search("s", category="bug")
        assert len(results) == 1
        assert results[0].category == "bug"

    def test_search_scores_action_taken(self, manager):
        from unittest.mock import patch
        import backend.app.core.experience as exp_module
        from datetime import datetime, UTC

        with patch.object(exp_module, "datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
            mock_dt.UTC = UTC
            manager.record("p1", "test", "situation", "action taken here", "outcome", 0.9)
        results = manager.search("action")
        assert len(results) == 1
        assert results[0].action_taken == "action taken here"

    def test_search_scores_by_relevance(self, manager):
        from unittest.mock import patch
        import backend.app.core.experience as exp_module
        from datetime import datetime, UTC

        with patch.object(exp_module, "datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
            mock_dt.UTC = UTC
            id1 = manager.record("p1", "test", "fix login bug", "update auth", "resolved", 0.9)
            mock_dt.now.return_value = datetime(2024, 1, 1, 12, 0, 1, tzinfo=UTC)
            id2 = manager.record("p1", "test", "update docs", "write readme", "done", 0.5)
        assert id1 != id2
        results = manager.search("login")
        assert results[0].situation == "fix login bug"

    def test_search_respects_limit(self, manager):
        from unittest.mock import patch
        import backend.app.core.experience as exp_module
        from datetime import datetime, UTC

        with patch.object(exp_module, "datetime") as mock_dt:
            mock_dt.UTC = UTC
            for i in range(10):
                mock_dt.now.return_value = datetime(2024, 1, 1, 12, 0, i, tzinfo=UTC)
                manager.record("p1", "test", f"situation {i}", f"action {i}", f"outcome {i}", 0.5)
        results = manager.search("situation", limit=3)
        assert len(results) == 3

    def test_get_by_project_filters_by_project(self, manager):
        from unittest.mock import patch
        import backend.app.core.experience as exp_module
        from datetime import datetime, UTC

        with patch.object(exp_module, "datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
            mock_dt.UTC = UTC
            manager.record("p1", "test", "s1", "a1", "o1", 0.9)
            mock_dt.now.return_value = datetime(2024, 1, 1, 12, 0, 1, tzinfo=UTC)
            manager.record("p2", "test", "s2", "a2", "o2", 0.8)
        results = manager.get_by_project("p1")
        assert len(results) == 1
        assert results[0].project_id == "p1"

    def test_get_by_project_returns_empty_for_missing(self, manager):
        results = manager.get_by_project("missing")
        assert results == []

    def test_persist_writes_json(self, manager, tmp_path):
        lesson = Lesson(
            id="l1",
            project_id="p1",
            category="test",
            situation="s",
            action_taken="a",
            outcome="o",
            quality_score=0.9,
        )
        manager._persist(lesson)
        path = Path(tmp_path) / "l1.json"
        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["id"] == "l1"
        assert data["quality_score"] == 0.9

    def test_load_all_reads_persisted_lessons(self, manager):
        lesson_id = manager.record(
            project_id="p1",
            category="test",
            situation="s",
            action_taken="a",
            outcome="o",
            quality_score=0.9,
        )
        manager2 = ExperienceLearning(base_path=str(manager.base_path))
        manager2.load_all()
        assert lesson_id in manager2._lessons
        assert manager2._lessons[lesson_id].project_id == "p1"

    def test_load_all_handles_invalid_json(self, manager, tmp_path):
        bad_file = Path(tmp_path) / "bad.json"
        bad_file.write_text("not json", encoding="utf-8")
        manager.load_all()
        assert len(manager._lessons) == 0

    def test_load_all_handles_missing_fields(self, manager, tmp_path):
        bad_file = Path(tmp_path) / "bad2.json"
        bad_file.write_text(json.dumps({"id": "l1"}), encoding="utf-8")
        manager.load_all()
        assert len(manager._lessons) == 0
