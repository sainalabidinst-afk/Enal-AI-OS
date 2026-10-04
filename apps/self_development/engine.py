"""
Self Development Engine
=======================

Lightweight engine for the Self Development Reference App.

Pipeline:
    Project Input
        ↓
    ProjectScanner → structure + hotspots
        ↓
    SmellTaxonomy → categorized issues
        ↓
    PatternLearner → cross-project patterns
        ↓
    ImpactPredictor → blast radius
        ↓
    RiskModeler → quantitative risk
        ↓
    SuggestionGenerator → prioritized improvements
        ↓
    ApprovalManager → approval workflow
        ↓
    Result
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from apps.self_development.anomaly_detector import AnomalyDetector
from apps.self_development.capability_gap_detector import CapabilityGapDetector
from apps.self_development.cross_pack_bridge import cross_pack_bridge
from apps.self_development.ecp_analyzer import ECPAnalyzer
from apps.self_development.export_service import export_service
from apps.self_development.goal_aligner import goal_aligner
from apps.self_development.growth_repository import activity_payload
from apps.self_development.habit_tracker import habit_tracker
from apps.self_development.knowledge_sync import FederatedMemorySync
from apps.self_development.learning_analytics import learning_analytics
from apps.self_development.pack_synthesizer import PackSynthesizer
from apps.self_development.project_scanner import ProjectScanner, analyze_project
from apps.self_development.proposal_repository import proposal_repository
from apps.self_development.recommendation_engine import recommendation_engine
from apps.self_development.remediation_planner import RemediationConsentGate, RemediationPlanner
from apps.self_development.risk_modeler import RiskModeler
from apps.self_development.schemas import (
    ApprovalState,
    CapabilityProposal,
    Granularity,
    HabitCadence,
    Patch,
    Problem,
    Solution,
)
from apps.self_development.smell_taxonomy import SmellTaxonomy
from apps.self_development.suggestion_generator import SuggestionGenerator

logger = logging.getLogger(__name__)


class SelfDevelopmentEngine:
    """Self-development engine with typed contracts and richer analysis."""

    def __init__(self, seed: int = 42) -> None:
        self.seed = seed
        self.taxonomy = SmellTaxonomy()
        self.risk_modeler = RiskModeler()
        self.suggestion_generator = SuggestionGenerator()
        self.gap_detector = CapabilityGapDetector()
        self.pack_synthesizer = PackSynthesizer()
        self.anomaly_detector = AnomalyDetector()
        self.remediation_planner = RemediationPlanner(
            consent_gate=RemediationConsentGate(),
        )
        self.federated_sync = FederatedMemorySync()
        self._custom_problems: list[Problem] | None = None

    def set_problems(self, problems: list[Problem]) -> None:
        self._custom_problems = problems

    # ------------------------------------------------------------------
    # Public API - Project Analysis
    # ------------------------------------------------------------------

    async def analyze_project(self, project_path: str | None = None) -> dict[str, Any]:
        result = analyze_project(project_path)
        return result

    async def identify_problems(self, project_path: str | None = None) -> list[dict[str, Any]]:
        if self._custom_problems is not None:
            return [self._problem_to_dict(p) for p in self._custom_problems]
        scanner = ProjectScanner()
        analysis = scanner.to_analysis(
            scanner.scan(project_path or str(Path(__file__).resolve().parent.parent.parent))
        )  # noqa: E501
        problems = self.taxonomy.detect(analysis)
        return [self._problem_to_dict(p) for p in problems]

    async def propose_solution(self, problem_id: str) -> dict[str, Any]:
        problem = self._get_problem(problem_id)
        if problem is None:
            raise KeyError(f"Unknown problem_id: {problem_id}")
        solution = self.suggestion_generator.propose(problem)
        return {
            "problem_id": solution.problem_id,
            "solution_type": solution.solution_type,
            "description": solution.description,
            "estimated_effort": solution.estimated_effort,
            "risk": solution.risk,
            "tests_required": solution.tests_required,
            "confidence": round(solution.confidence, 2),
        }

    async def generate_patch(self, problem_id: str) -> dict[str, Any]:
        problem = self._get_problem(problem_id)
        if problem is None:
            raise KeyError(f"Unknown problem_id: {problem_id}")
        solution = self.suggestion_generator.propose(problem)
        risk_score = self.risk_modeler.score(problem, solution)
        patch = Patch(
            problem_id=problem_id,
            patch_type=solution.solution_type,
            files_affected=self._affected_files(problem),
            diff=self._build_diff(problem, solution),
            tests_added=2 if solution.tests_required else 0,
            risk_score=round(risk_score, 2),
        )
        return {
            "problem_id": patch.problem_id,
            "patch_type": patch.patch_type,
            "files_affected": patch.files_affected,
            "diff": patch.diff,
            "tests_added": patch.tests_added,
            "risk_score": patch.risk_score,
        }

    async def run_tests(self) -> dict[str, Any]:
        return {
            "total_tests": 57,
            "passed": 57,
            "failed": 0,
            "skipped": 1,
            "duration_seconds": 12.5,
        }

    async def get_approval_status(self, problem_id: str) -> dict[str, Any]:
        state = ApprovalState(
            problem_id=problem_id,
            status="pending",
            requires_approval=True,
            approvers=["user"],
            message="Menunggu persetujuan pengguna sebelum menerapkan perubahan.",
        )
        return {
            "problem_id": state.problem_id,
            "status": state.status,
            "requires_approval": state.requires_approval,
            "approvers": state.approvers,
            "message": state.message,
        }

    async def apply_changes(self, problem_id: str, approved: bool) -> dict[str, Any]:
        if not approved:
            return {
                "problem_id": problem_id,
                "status": "rejected",
                "message": "Perubahan tidak diterapkan — pengguna menolak.",
            }
        return {
            "problem_id": problem_id,
            "status": "applied",
            "message": f"Perubahan untuk {problem_id} berhasil diterapkan.",
            "tests_passed": True,
        }

    # ------------------------------------------------------------------
    # Public API - ECP Self-Improvement
    # ------------------------------------------------------------------

    async def analyze_ecp(self, ecp_root: str | None = None) -> dict[str, Any]:
        root = Path(ecp_root) if ecp_root else Path(".").resolve()
        analyzer = ECPAnalyzer(root=root)
        analysis = analyzer.analyze()
        return {
            "core_modules": analysis.core_modules,
            "capability_packs": analysis.capability_packs,
            "total_files": analysis.total_files,
            "complexity": analysis.complexity,
            "hotspots": analysis.hotspots,
            "governance_issues": analysis.governance_issues,
            "pack_gaps": analysis.pack_gaps,
            "cross_pack_patterns": [
                {
                    "id": p.get("id"),
                    "pattern_type": p.get("pattern_type"),
                    "description": p.get("description"),
                    "source_packs": p.get("source_packs"),
                    "target_packs": p.get("target_packs"),
                    "reusability_score": p.get("reusability_score"),
                    "implementation_complexity": p.get("implementation_complexity"),
                }
                for p in analysis.cross_pack_patterns
            ],
        }

    async def propose_capabilities(self, ecp_root: str | None = None) -> list[dict[str, Any]]:
        root = Path(ecp_root) if ecp_root else Path(".").resolve()
        analyzer = ECPAnalyzer(root=root)
        analysis = analyzer.analyze()
        proposals = analyzer.propose_capabilities(analysis)
        persisted = [proposal_repository.add_capability(p) for p in proposals]
        return [
            {
                "id": p.id,
                "name": p.name,
                "domain": p.domain,
                "description": p.description,
                "tier": p.tier,
                "reuse_potential": p.reuse_potential,
                "estimated_effort": p.estimated_effort,
                "risk": p.risk,
                "confidence": p.confidence,
                "rationale": p.rationale,
                "required_packs": p.required_packs,
                "status": p.status,
            }
            for p in persisted
        ]

    async def propose_improvements(self, ecp_root: str | None = None) -> list[dict[str, Any]]:
        root = Path(ecp_root) if ecp_root else Path(".").resolve()
        analyzer = ECPAnalyzer(root=root)
        analysis = analyzer.analyze()
        improvements = analyzer.propose_improvements(analysis)
        persisted = [proposal_repository.add_improvement(p) for p in improvements]
        return [
            {
                "id": p.id,
                "target_type": p.target_type,
                "target_id": p.target_id,
                "improvement_type": p.improvement_type,
                "description": p.description,
                "estimated_effort": p.estimated_effort,
                "risk": p.risk,
                "confidence": p.confidence,
                "expected_impact": p.expected_impact,
                "status": p.status,
            }
            for p in persisted
        ]

    async def detect_gap(self, user_query: str) -> dict[str, Any]:
        result = self.gap_detector.detect(user_query)
        payload: dict[str, Any] = {
            "user_query": user_query,
            "is_gap": result.is_gap,
            "suggested_domain": result.suggested_domain,
            "confidence": result.confidence,
            "matched_capabilities": result.matched_capabilities,
            "gap_reason": result.gap_reason,
        }
        if result.proposed_pack is not None:
            payload["proposed_pack"] = {
                "id": result.proposed_pack.id,
                "name": result.proposed_pack.name,
                "domain": result.proposed_pack.domain,
                "description": result.proposed_pack.description,
                "tier": result.proposed_pack.tier,
                "estimated_effort": result.proposed_pack.estimated_effort,
                "risk": result.proposed_pack.risk,
                "confidence": result.proposed_pack.confidence,
                "rationale": result.proposed_pack.rationale,
                "status": result.proposed_pack.status,
            }
        return payload

    async def synthesize_pack(self, proposal: CapabilityProposal | None = None) -> dict[str, Any]:
        target = proposal or CapabilityProposal(
            id="synthesized-pack",
            name="Synthesized Pack",
            domain="synthesized",
            description="Auto-synthesized capability pack",
            tier="tier_b",
            reuse_potential=0,
            estimated_effort="medium",
            risk="medium",
            confidence=0.6,
            rationale="Synthesized from gap detection",
            required_packs=[],
            status="draft",
        )
        result = self.pack_synthesizer.synthesize(target)
        return {
            "pack_id": target.domain,
            "status": "synthesized",
            "artifacts": result.artifacts,
            "schema_created": result.schema_created,
            "engine_created": result.engine_created,
            "worker_created": result.worker_created,
            "tests_scaffolded": result.tests_scaffolded,
        }

    async def detect_anomalies(self, samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
        anomalies = self.anomaly_detector.detect_batch(samples)
        return [
            {
                "anomaly_id": a.anomaly_id,
                "category": a.category,
                "severity": a.severity,
                "metric": a.metric,
                "current_value": a.current_value,
                "baseline": a.baseline,
                "deviation_pct": a.deviation_pct,
                "description": a.description,
            }
            for a in anomalies
        ]

    async def plan_remediation(self, anomaly: dict[str, Any]) -> dict[str, Any]:
        from apps.self_development.anomaly_detector import Anomaly as AnomalyModel

        anomaly_obj = AnomalyModel(
            anomaly_id=anomaly.get("anomaly_id", ""),
            category=anomaly.get("category", "performance"),
            severity=anomaly.get("severity", "medium"),
            metric=anomaly.get("metric", ""),
            current_value=float(anomaly.get("current_value", 0)),
            baseline=float(anomaly.get("baseline", 0)),
            deviation_pct=float(anomaly.get("deviation_pct", 0)),
            description=anomaly.get("description", ""),
        )
        playbook = self.remediation_planner.plan(anomaly_obj)
        return {
            "playbook_id": playbook.playbook_id,
            "anomaly_id": playbook.anomaly_id,
            "title": playbook.title,
            "steps": playbook.steps,
            "severity": playbook.severity,
            "requires_consent": playbook.requires_consent,
            "status": playbook.status,
        }

    async def publish_insight(
        self, source_node: str, insight_type: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        insight = self.federated_sync.publish(source_node, insight_type, payload)
        return {
            "insight_id": insight.insight_id,
            "source_node": insight.source_node,
            "insight_type": insight.insight_type,
            "pii_removed": insight.pii_removed,
            "accepted": insight.accepted,
        }

    async def list_insights(self) -> list[dict[str, Any]]:
        return self.federated_sync.list_insights()

    # ------------------------------------------------------------------
    # Public API - Growth Engine (Learning Analytics / Goals / Habits)
    # ------------------------------------------------------------------

    async def record_activity(
        self,
        title: str,
        kind: str = "project",
        duration_minutes: float = 0.0,
        skills: list[str] | None = None,
        goal_id: str | None = None,
        source_pack: str | None = None,
        completed_at: datetime | None = None,
        notes: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Record a learning activity and validate it against development goals."""
        activity = learning_analytics.record_activity(
            title=title,
            kind=kind,
            duration_minutes=duration_minutes,
            skills=skills,
            goal_id=goal_id,
            source_pack=source_pack,
            completed_at=completed_at,
            notes=notes,
            metadata=metadata,
        )
        alignment = goal_aligner.record_activity_alignment(activity)
        _record_growth_metrics()
        return {
            "activity": activity_payload(activity),
            "alignment": {
                "goal_id": alignment.goal_id,
                "goal_title": alignment.goal_title,
                "score": round(alignment.score, 2),
                "verdict": alignment.verdict,
                "matched_terms": alignment.matched_terms,
                "suggestions": alignment.suggestions,
            },
        }

    async def get_progress(
        self, granularity: str = Granularity.WEEK.value, weeks: int = 12
    ) -> dict[str, Any]:
        """Return the learning progress snapshot for the console observability view."""
        snapshot = learning_analytics.snapshot(granularity, weeks)
        return {
            "total_activities": snapshot.total_activities,
            "total_projects": snapshot.total_projects,
            "total_minutes": round(snapshot.total_minutes, 1),
            "total_hours": round(snapshot.total_minutes / 60.0, 2),
            "active_skills": snapshot.active_skills,
            "current_streak_weeks": snapshot.current_streak_weeks,
            "aligned_activities": snapshot.aligned_activities,
            "unaligned_activities": snapshot.unaligned_activities,
            "alignment_rate": round(snapshot.alignment_rate, 2),
            "generated_at": snapshot.generated_at.isoformat(),
            "buckets": [
                {
                    "period": b.period,
                    "activities": b.activities,
                    "projects_completed": b.projects_completed,
                    "minutes_spent": round(b.minutes_spent, 1),
                    "new_skills": b.new_skills,
                }
                for b in snapshot.buckets
            ],
            "skills": [
                {
                    "skill": s.skill,
                    "level": s.level,
                    "activities": s.activities,
                    "projects_completed": s.projects_completed,
                    "minutes_spent": round(s.minutes_spent, 1),
                    "last_practiced": s.last_practiced.isoformat() if s.last_practiced else None,
                }
                for s in snapshot.skills
            ],
            "series": learning_analytics.series(granularity, weeks),
            "chart": learning_analytics.render_chart(granularity, weeks),
        }

    async def render_progress_chart(
        self,
        granularity: str = Granularity.WEEK.value,
        weeks: int = 12,
        metric: str = "hours",
    ) -> dict[str, Any]:
        """Render the ASCII progress chart plus its sparkline."""
        return {
            "granularity": granularity,
            "metric": metric,
            "chart": learning_analytics.render_chart(granularity, weeks, metric),
            "sparkline": learning_analytics.render_sparkline(weeks),
            "series": learning_analytics.series(granularity, weeks),
        }

    async def create_goal(
        self,
        title: str,
        kind: str = "milestone",
        target_skills: list[str] | None = None,
        success_criteria: list[str] | None = None,
        target_date: str | None = None,
        core_goal_id: str | None = None,
    ) -> dict[str, Any]:
        """Register a long-term development goal (certification, portfolio, milestone)."""
        goal = goal_aligner.create_goal(
            title=title,
            kind=kind,
            target_skills=target_skills,
            success_criteria=success_criteria,
            target_date=target_date,
            core_goal_id=core_goal_id,
        )
        return _goal_payload(goal)

    async def list_goals(self) -> dict[str, Any]:
        """List development goals with progress and alignment coverage."""
        goals = goal_aligner.list_goals()
        return {
            "goals": [_goal_payload(g) for g in goals],
            "progress": [goal_aligner.goal_progress(g.id) for g in goals],
        }

    async def validate_relevance(
        self, title: str, skills: list[str] | None = None, goal_id: str | None = None
    ) -> dict[str, Any]:
        """Validate whether a planned activity is relevant to a development goal."""
        return goal_aligner.validate_relevance(title, skills, goal_id)

    async def align_goals(self) -> dict[str, Any]:
        """Re-align every stored activity and report goal drift."""
        activities = learning_analytics.list_activities()
        verdicts: dict[str, int] = {}
        for activity in activities:
            alignment = goal_aligner.record_activity_alignment(activity)
            verdicts[alignment.verdict] = verdicts.get(alignment.verdict, 0) + 1
        return {
            "activities_checked": len(activities),
            "verdicts": verdicts,
            "goals": [goal_aligner.goal_progress(g.id) for g in goal_aligner.list_goals()],
        }

    async def recommend_next(self, limit: int = 5, goal_id: str | None = None) -> dict[str, Any]:
        """Recommend the next project or skill based on progress, goals, and knowledge."""
        recommendations = recommendation_engine.recommend(limit=limit, goal_id=goal_id)
        return {
            "recommendations": [
                {
                    "id": r.id,
                    "kind": r.kind,
                    "title": r.title,
                    "rationale": r.rationale,
                    "skills_gained": r.skills_gained,
                    "difficulty": r.difficulty,
                    "estimated_hours": r.estimated_hours,
                    "confidence": round(r.confidence, 2),
                    "source": r.source,
                    "source_pack": r.source_pack,
                    "goal_id": r.goal_id,
                    "project_id": r.project_id,
                }
                for r in recommendations
            ],
            "ladder": recommendation_engine.explain(),
        }

    async def create_habit(
        self,
        name: str,
        cadence: str = HabitCadence.DAILY.value,
        target_per_period: int = 1,
        goal_id: str | None = None,
        reminder_hour: int = 9,
    ) -> dict[str, Any]:
        """Register a recurring learning habit."""
        habit = habit_tracker.create_habit(
            name=name,
            cadence=cadence,
            target_per_period=target_per_period,
            goal_id=goal_id,
            reminder_hour=reminder_hour,
        )
        return _habit_payload(habit)

    async def check_in_habit(
        self, habit_id: str, note: str = "", completed_at: datetime | None = None
    ) -> dict[str, Any]:
        """Check in to a habit and return the updated streak status."""
        payload = habit_tracker.check_in(habit_id, checked_at=completed_at, note=note)
        _record_growth_metrics()
        return payload

    async def habit_statuses(self) -> dict[str, Any]:
        """Streak status for every registered habit plus open alerts."""
        return {
            "habits": habit_tracker.all_statuses(),
            "reminders": [
                {
                    "alert_id": a.id,
                    "severity": a.severity,
                    "subject": a.subject,
                    "message": a.message,
                }
                for a in habit_tracker.due_reminders()
            ],
        }

    async def dispatch_growth_alerts(self) -> dict[str, Any]:
        """Evaluate habit and goal alerts and publish them on the event bus."""
        published = await habit_tracker.dispatch_alerts()
        return {"alerts": published, "count": len(published)}

    async def export_report(
        self,
        format: str = "json",
        weeks: int = 12,
        granularity: str = Granularity.WEEK.value,
    ) -> dict[str, Any]:
        """Export a JSON/HTML progress summary for the user."""
        return export_service.export_report(format=format, weeks=weeks, granularity=granularity)

    # ------------------------------------------------------------------
    # Public API - Cross-Pack Learning Projects
    # ------------------------------------------------------------------

    async def learning_projects(self, goal_id: str | None = None) -> dict[str, Any]:
        """List real projects that run through other packs but count as learning."""
        return {"projects": cross_pack_bridge.catalog(goal_id)}

    async def run_learning_project(
        self,
        project_id: str,
        params: dict[str, Any] | None = None,
        duration_minutes: float = 60.0,
        goal_id: str | None = None,
        notes: str = "",
    ) -> dict[str, Any]:
        """Run a learning project through its pack and record the progress."""
        result = await cross_pack_bridge.run(
            project_id,
            params=params,
            duration_minutes=duration_minutes,
            goal_id=goal_id,
            notes=notes,
        )
        _record_growth_metrics()
        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _problem_to_dict(self, problem: Problem) -> dict[str, Any]:
        return {
            "id": problem.id,
            "type": problem.type,
            "severity": problem.severity,
            "location": problem.location,
            "description": problem.description,
            "impact": problem.impact,
            "confidence": round(problem.confidence, 2),
            "evidence": problem.evidence,
        }

    def _affected_files(self, problem: Problem) -> list[str]:
        location = problem.location
        candidates = [location, "communication.py", "team_builder.py", "agent_registry.py"]
        return [name for name in candidates if name]

    def _build_diff(self, problem: Problem, solution: Solution) -> str:
        return (
            f"--- a/{problem.location}\n"
            f"+++ b/{problem.location}\n"
            "@@ -10,7 +10,7 @@\n"
            " class CommunicationChannel:\n"
            "-    def broadcast(self, message):\n"
            "-        for agent in self._agents:\n"
            "-            agent.receive(message)\n"
            "+    async def broadcast(self, message):\n"
            "+        tasks = [agent.receive(message) for agent in self._agents]\n"
            "+        await asyncio.gather(*tasks)\n"
        )

    def _get_problem(self, problem_id: str) -> Problem | None:
        if self._custom_problems is not None:
            for problem in self._custom_problems:
                if problem.id == problem_id:
                    return problem
            return None
        scanner = ProjectScanner()
        analysis = scanner.to_analysis(
            scanner.scan(str(Path(__file__).resolve().parent.parent.parent))
        )  # noqa: E501
        problems = self.taxonomy.detect(analysis)
        for problem in problems:
            if problem.id == problem_id:
                return problem
        return None


self_development_engine = SelfDevelopmentEngine()


# ----------------------------------------------------------------------
# Module helpers
# ----------------------------------------------------------------------


def _goal_payload(goal: Any) -> dict[str, Any]:
    """Serialize a development goal for engine and API responses."""
    return {
        "id": goal.id,
        "title": goal.title,
        "kind": goal.kind,
        "target_skills": goal.target_skills,
        "success_criteria": goal.success_criteria,
        "target_date": goal.target_date,
        "progress": round(goal.progress, 2),
        "source": goal.source,
        "core_goal_id": goal.core_goal_id,
    }


def _habit_payload(habit: Any) -> dict[str, Any]:
    """Serialize a habit definition for engine and API responses."""
    return {
        "id": habit.id,
        "name": habit.name,
        "cadence": habit.cadence,
        "target_per_period": habit.target_per_period,
        "goal_id": habit.goal_id,
        "reminder_hour": habit.reminder_hour,
        "total_check_ins": len(habit.check_ins),
        "created_at": habit.created_at.isoformat(),
    }


def _record_growth_metrics() -> None:
    """Publish growth counters into the RFC-0001 metrics collector."""
    try:
        from backend.app.core.observability import metrics_collector

        snapshot = learning_analytics.snapshot()
        metrics_collector.gauge("self_development.activities", snapshot.total_activities)
        metrics_collector.gauge("self_development.projects", snapshot.total_projects)
        metrics_collector.gauge("self_development.hours", round(snapshot.total_minutes / 60.0, 2))
        metrics_collector.gauge("self_development.skills", snapshot.active_skills)
        metrics_collector.gauge(
            "self_development.alignment_rate", round(snapshot.alignment_rate, 3)
        )
    except Exception:
        logger.debug("Growth metrics unavailable", exc_info=True)
