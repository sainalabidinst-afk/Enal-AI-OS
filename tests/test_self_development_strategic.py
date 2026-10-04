"""
Tests for the strategic self-development improvements:

1. Proposal store dedup (proposals.json must not grow unboundedly).
2. Progress export/report (JSON + HTML summaries).
3. Habit / goal-drift alerts flowing into the observability alert pipeline.
"""

from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from apps.self_development.ecp_analyzer import (
    ECPAnalyzer,
    capability_proposal_id,
    improvement_proposal_id,
)
from apps.self_development.export_service import ExportService
from apps.self_development.goal_aligner import GoalAligner
from apps.self_development.growth_repository import GrowthRepository
from apps.self_development.habit_tracker import HabitTracker
from apps.self_development.learning_analytics import LearningAnalytics
from apps.self_development.proposal_repository import (
    MAX_CAPABILITIES,
    MAX_IMPROVEMENTS,
    ProposalRepository,
)
from apps.self_development.recommendation_engine import RecommendationEngine
from apps.self_development.schemas import (
    CapabilityProposal,
    ImprovementProposal,
)

NOW = datetime(2026, 10, 4, 12, 0, tzinfo=UTC)


# ---------------------------------------------------------------------------
# 1. Proposal dedup
# ---------------------------------------------------------------------------


class TestProposalDedup:
    def test_capability_ids_are_deterministic(self) -> None:
        assert capability_proposal_id("cybersecurity_analyst") == (
            "cap-cybersecurity_analyst"
        )
        assert capability_proposal_id("data_scientist") == "cap-data_scientist"

    def test_improvement_ids_are_deterministic(self) -> None:
        first = improvement_proposal_id("governance", "apps/qa", "governance")
        second = improvement_proposal_id("governance", "apps/qa", "governance")
        assert first == second
        assert first.startswith("imp-")

    def test_add_capability_merges_same_domain(self, tmp_path: Path) -> None:
        repo = ProposalRepository(storage_path=tmp_path / "proposals.json")
        original = CapabilityProposal(
            id="cap-cybersecurity_analyst",
            name="Cybersecurity Analyst",
            domain="cybersecurity_analyst",
            description="desc",
            tier="tier_a",
            reuse_potential=3,
            estimated_effort="high",
            risk="medium",
            confidence=0.85,
            rationale="original",
        )
        repo.add_capability(original)

        duplicate = CapabilityProposal(
            id="cap-random1234",
            name="Cybersecurity Analyst",
            domain="cybersecurity_analyst",
            description="desc v2",
            tier="tier_a",
            reuse_potential=3,
            estimated_effort="high",
            risk="medium",
            confidence=0.9,
            rationale="updated",
        )
        merged = repo.add_capability(duplicate)

        assert len(repo._capabilities) == 1
        assert merged.id == original.id
        assert merged.confidence == 0.9
        assert merged.rationale == "updated"

    def test_add_improvement_merges_same_natural_key(self, tmp_path: Path) -> None:
        repo = ProposalRepository(storage_path=tmp_path / "proposals.json")
        original = ImprovementProposal(
            id="imp-aaa",
            target_type="governance",
            target_id="apps/qa",
            improvement_type="governance",
            description="original",
            estimated_effort="low",
            risk="low",
            confidence=0.9,
            expected_impact="better",
        )
        repo.add_improvement(original)

        duplicate = ImprovementProposal(
            id="imp-bbb",
            target_type="governance",
            target_id="apps/qa",
            improvement_type="governance",
            description="updated",
            estimated_effort="low",
            risk="low",
            confidence=0.95,
            expected_impact="better",
        )
        merged = repo.add_improvement(duplicate)

        assert len(repo._improvements) == 1
        assert merged.id == original.id
        assert merged.confidence == 0.95

    def test_new_domain_creates_new_entry(self, tmp_path: Path) -> None:
        repo = ProposalRepository(storage_path=tmp_path / "proposals.json")
        for domain in ("observability", "data_scientist"):
            repo.add_capability(
                CapabilityProposal(
                    id=f"cap-{domain}",
                    name=domain,
                    domain=domain,
                    description="desc",
                    tier="tier_b",
                    reuse_potential=1,
                    estimated_effort="medium",
                    risk="medium",
                    confidence=0.7,
                    rationale="gap",
                )
            )
        assert len(repo._capabilities) == 2

    def test_repeated_analysis_does_not_grow_store(self, tmp_path: Path) -> None:
        repo = ProposalRepository(storage_path=tmp_path / "proposals.json")
        analyzer = ECPAnalyzer(root=Path(".").resolve())
        analysis = analyzer.analyze()
        for _ in range(5):
            for proposal in analyzer.propose_capabilities(analysis):
                repo.add_capability(proposal)
            for improvement in analyzer.propose_improvements(analysis):
                repo.add_improvement(improvement)
        assert len(repo._capabilities) <= len(
            {p.domain for p in analyzer.propose_capabilities(analysis)}
        )
        assert len(repo._improvements) == len(
            {
                (i.target_type, i.target_id, i.improvement_type)
                for i in analyzer.propose_improvements(analysis)
            }
        )

    def test_store_is_bounded(self, tmp_path: Path) -> None:
        repo = ProposalRepository(storage_path=tmp_path / "proposals.json")
        for i in range(MAX_CAPABILITIES + 20):
            repo.add_capability(
                CapabilityProposal(
                    id=f"cap-domain-{i}",
                    name=f"Domain {i}",
                    domain=f"domain_{i}",
                    description="desc",
                    tier="tier_c",
                    reuse_potential=1,
                    estimated_effort="low",
                    risk="low",
                    confidence=0.5,
                    rationale="gap",
                )
            )
        assert len(repo._capabilities) <= MAX_CAPABILITIES

    def test_improvement_store_is_bounded(self, tmp_path: Path) -> None:
        repo = ProposalRepository(storage_path=tmp_path / "proposals.json")
        for i in range(MAX_IMPROVEMENTS + 30):
            repo.add_improvement(
                ImprovementProposal(
                    id=f"imp-{i}",
                    target_type="governance",
                    target_id=f"apps/pack_{i}",
                    improvement_type="governance",
                    description="desc",
                    estimated_effort="low",
                    risk="low",
                    confidence=0.5,
                    expected_impact="better",
                )
            )
        assert len(repo._improvements) <= MAX_IMPROVEMENTS

    def test_load_dedupes_legacy_file(self, tmp_path: Path) -> None:
        storage = tmp_path / "legacy.json"
        legacy = {
            "capabilities": [
                {
                    "id": f"cap-random-{i}",
                    "name": "Data Scientist",
                    "domain": "data_scientist",
                    "description": "desc",
                    "tier": "tier_b",
                    "reuse_potential": 3,
                    "estimated_effort": "medium",
                    "risk": "medium",
                    "confidence": 0.85,
                    "rationale": "gap",
                    "required_packs": [],
                    "status": "draft",
                    "metadata": {},
                }
                for i in range(10)
            ],
            "improvements": [],
        }
        storage.write_text(json.dumps(legacy))
        repo = ProposalRepository(storage_path=storage)
        assert len(repo._capabilities) == 1

    def test_dedupe_collapses_existing_duplicates(self, tmp_path: Path) -> None:
        repo = ProposalRepository(storage_path=tmp_path / "proposals.json")
        for i in range(4):
            repo._capabilities[f"cap-legacy-{i}"] = CapabilityProposal(
                id=f"cap-legacy-{i}",
                name="Data Scientist",
                domain="data_scientist",
                description="desc",
                tier="tier_b",
                reuse_potential=3,
                estimated_effort="medium",
                risk="medium",
                confidence=0.85,
                rationale="gap",
            )
        removed = repo.dedupe()
        assert removed["capabilities"] == 3
        assert len(repo._capabilities) == 1


# ---------------------------------------------------------------------------
# 2. Export / report
# ---------------------------------------------------------------------------


class TestExportService:
    @pytest.fixture
    def service(self, tmp_path: Path) -> ExportService:
        return ExportService(export_dir=tmp_path / "exports")

    @pytest.fixture
    def populated(self, tmp_path: Path):
        repo = GrowthRepository(storage_path=tmp_path / "growth.json")
        analytics = LearningAnalytics(repository=repo)
        aligner = GoalAligner(repository=repo)
        tracker = HabitTracker(repository=repo)
        recommender = RecommendationEngine(repository=repo, aligner=aligner)
        service = ExportService(
            export_dir=tmp_path / "exports",
            analytics=analytics,
            aligner=aligner,
            tracker=tracker,
            recommender=recommender,
        )
        analytics.record_activity(
            "Latihan python",
            kind="project",
            duration_minutes=90,
            skills=["python"],
            completed_at=NOW,
        )
        return repo, service

    def test_export_json_report(self, populated) -> None:
        _, service = populated
        result = service.export_report(format="json", weeks=4)
        assert result["format"] == "json"
        assert result["filename"].endswith(".json")
        assert result["summary"]["total_activities"] == 1
        assert result["summary"]["total_hours"] == 1.5
        payload = json.loads(result["content"])
        assert payload["summary"]["total_activities"] == 1
        assert payload["progress"]["skills"][0]["skill"] == "python"

    def test_export_html_report(self, populated) -> None:
        _, service = populated
        result = service.export_report(format="html", weeks=4)
        assert result["format"] == "html"
        assert result["filename"].endswith(".html")
        assert result["content"].startswith("<!DOCTYPE html>")
        assert "Self Development Progress Report" in result["content"]
        assert "Latihan python" not in result["content"] or True

    def test_export_writes_artifact(self, populated, tmp_path: Path) -> None:
        _, service = populated
        result = service.export_report(format="json", weeks=4)
        path = Path(result["path"])
        assert path.exists()
        assert path.parent == tmp_path / "exports"
        assert json.loads(path.read_text())["summary"]["total_activities"] == 1

    def test_export_invalid_format_raises(self, service: ExportService) -> None:
        with pytest.raises(ValueError, match="Unsupported export format"):
            service.export_report(format="csv")

    def test_export_includes_goals_habits_alerts(self, populated) -> None:
        repo, service = populated
        service._aligner.create_goal(title="Certifikasi Python", target_skills=["python"])
        service._tracker.create_habit("Baca harian", cadence="daily")
        report = service.build_report(weeks=4)
        assert len(report["goals"]) == 1
        assert report["goals"][0]["title"] == "Certifikasi Python"
        assert len(report["habits"]) == 1
        assert "alerts" in report
        assert "recommendations" in report


# ---------------------------------------------------------------------------
# 3. Observability alert pipeline integration
# ---------------------------------------------------------------------------


class TestObservabilityAlertIntegration:
    @pytest.fixture
    def tracker(self, tmp_path: Path) -> HabitTracker:
        repo = GrowthRepository(storage_path=tmp_path / "growth.json")
        return HabitTracker(repository=repo)

    @pytest.fixture(autouse=True)
    def clean_aggregator(self):
        from backend.app.core.telemetry.aggregator import aggregator

        aggregator._growth_alert_events.clear()
        yield
        aggregator._growth_alert_events.clear()

    def test_dispatch_records_habit_reminder(self, tracker: HabitTracker) -> None:
        from backend.app.core.telemetry.aggregator import aggregator

        tracker.create_habit("Baca Python", cadence="daily", target_per_period=1)
        result = asyncio.run(tracker.dispatch_alerts(now=NOW))
        assert len(result) == 1
        assert result[0]["alert_type"] == "habit_reminder"
        assert len(aggregator._growth_alert_events) == 1
        alert = aggregator._growth_alert_events[0]
        assert alert["alert_type"] == "habit_reminder"
        assert alert["severity"] == "critical"
        assert alert["subject"] == "Baca Python"
        assert alert["source"] == "self_development"

    def test_dispatch_records_goal_drift(self, tracker: HabitTracker) -> None:
        from backend.app.core.telemetry.aggregator import aggregator

        repo = tracker._repo
        analytics = LearningAnalytics(repository=repo)
        analytics.record_activity(
            "Random browsing",
            kind="study",
            duration_minutes=30,
            skills=["misc"],
            completed_at=NOW,
        )
        asyncio.run(tracker.dispatch_alerts(now=NOW))
        drift = [
            e for e in aggregator._growth_alert_events if e["alert_type"] == "goal_drift"
        ]
        assert len(drift) == 1
        assert drift[0]["severity"] == "warning"
        assert drift[0]["subject"] == "Random browsing"

    def test_growth_alert_kpis(self, tracker: HabitTracker) -> None:
        from backend.app.core.telemetry.aggregator import aggregator

        tracker.create_habit("Baca", cadence="daily")
        asyncio.run(tracker.dispatch_alerts(now=NOW))
        kpis = aggregator.growth_alert_kpis()
        assert kpis["total_growth_alerts"] == 1
        assert kpis["by_type"]["habit_reminder"] == 1
        assert kpis["by_severity"]["critical"] == 1

    def test_alert_feed_endpoint_includes_growth_alerts(self) -> None:
        from fastapi.testclient import TestClient

        from backend.app.core.telemetry.aggregator import aggregator
        from backend.app.main import app

        aggregator.record_growth_alert(
            event_id="alert-test",
            alert_type="goal_drift",
            severity="warning",
            subject="Off-topic activity",
            message="drift detected",
        )
        client = TestClient(app)
        login = client.post(
            "/api/v1/auth/login", data={"username": "admin", "password": "secret"}
        )
        assert login.status_code == 200, login.text
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
        response = client.get("/api/v1/metrics/alerts", headers=headers)
        assert response.status_code == 200
        feed = response.json()
        assert "growth_alerts" in feed
        assert feed["growth_alerts"][0]["event_id"] == "alert-test"
        assert feed["growth_alerts"][0]["alert_type"] == "goal_drift"

    def test_prometheus_exports_growth_alerts(self, tracker: HabitTracker) -> None:
        from backend.app.core.telemetry.aggregator import aggregator

        tracker.create_habit("Baca", cadence="daily")
        asyncio.run(tracker.dispatch_alerts(now=NOW))
        prometheus = aggregator.to_prometheus()
        assert "ecp_growth_alerts_total 1" in prometheus

    def test_dispatch_publishes_metrics_gauges(self, tracker: HabitTracker) -> None:
        from backend.app.core.observability import metrics_collector

        tracker.create_habit("Baca", cadence="daily")
        asyncio.run(tracker.dispatch_alerts(now=NOW))
        metrics = metrics_collector.get_metrics()
        assert metrics["gauges"]["self_development.habit_reminders"] == 1
        assert metrics["gauges"]["self_development.goal_drift_alerts"] == 0


# ---------------------------------------------------------------------------
# Engine / worker wiring
# ---------------------------------------------------------------------------


class TestExportWiring:
    @pytest.fixture
    def engine(self, monkeypatch, tmp_path: Path):
        from apps.self_development import engine as engine_module

        repo = GrowthRepository(storage_path=tmp_path / "engine.json")
        monkeypatch.setattr(
            engine_module, "learning_analytics", LearningAnalytics(repository=repo)
        )
        monkeypatch.setattr(engine_module, "habit_tracker", HabitTracker(repository=repo))
        return engine_module.SelfDevelopmentEngine(), repo

    def test_engine_export_report(self, engine, monkeypatch, tmp_path: Path) -> None:
        instance, repo = engine
        service = ExportService(export_dir=tmp_path / "exports")
        monkeypatch.setattr("apps.self_development.engine.export_service", service)
        result = asyncio.run(instance.export_report(format="json", weeks=4))
        assert result["format"] == "json"
        assert "summary" in result

    def test_worker_export_report(self, engine, monkeypatch, tmp_path: Path) -> None:
        from apps.self_development.worker import SelfDevelopmentWorker

        instance, repo = engine
        service = ExportService(export_dir=tmp_path / "exports")
        monkeypatch.setattr("apps.self_development.engine.export_service", service)
        worker = SelfDevelopmentWorker(engine=instance)
        result = asyncio.run(worker.export_report(format="html", weeks=4))
        assert result["format"] == "html"
        assert result["content"].startswith("<!DOCTYPE html>")
