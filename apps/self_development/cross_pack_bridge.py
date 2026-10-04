"""
Cross-Pack Bridge
=================

Runs real projects through other capability packs while counting them as
self-development progress.

The bridge never reimplements pack logic: each learning project declares the
target pack and operation, and the bridge delegates to that pack's engine via a
lazy import so the pack stays decoupled and import-safe.
"""

from __future__ import annotations

import inspect
import logging
import time
from collections.abc import Awaitable, Callable
from typing import Any

from apps.self_development.goal_aligner import GoalAligner, goal_aligner
from apps.self_development.learning_analytics import LearningAnalytics, learning_analytics
from apps.self_development.schemas import ActivityKind, LearningProject

logger = logging.getLogger(__name__)

LEARNING_CATALOG: tuple[LearningProject, ...] = (
    LearningProject(
        id="trading-backtest",
        title="Bangun mini backtest engine",
        pack="trading-analyst",
        operation="backtest_strategy",
        skills_gained=("python", "statistics", "quantitative-finance", "backtesting"),
        difficulty="hard",
        estimated_hours=10.0,
        description=(
            "Jalankan strategi lewat Trading Analyst BacktestEngine pada data OHLCV, "
            "lalu dokumentasikan win rate, profit factor, dan drawdown."
        ),
        goal_hints=("sertification", "trading", "quant", "portfolio"),
    ),
    LearningProject(
        id="architecture-review",
        title="Architecture review pada satu capability pack",
        pack="system-architect",
        operation="full_review",
        skills_gained=("clean-architecture", "ddd", "architecture-review"),
        difficulty="medium",
        estimated_hours=8.0,
        description=(
            "Jalankan System Architect full review pada repo atau pack pilihan, "
            "lalu portingkan temuan violation menjadi backlog refactor."
        ),
        goal_hints=("arsitektur", "architecture", "portfolio", "refactor"),
    ),
    LearningProject(
        id="knowledge-graph",
        title="Rancang knowledge graph untuk domain belajar",
        pack="knowledge-engineer",
        operation="knowledge_graph",
        skills_gained=("knowledge-graph", "ontology", "data-modeling"),
        difficulty="medium",
        estimated_hours=6.0,
        description=(
            "Bangun ontology + knowledge graph untuk materi belajar sendiri, "
            "sehingga rekomendasi berikutnya punya konteks yang lebih kaya."
        ),
        goal_hints=("knowledge", "ontology", "sistem"),
    ),
    LearningProject(
        id="research-digest",
        title="Literature review untuk skill baru",
        pack="research-assistant",
        operation="literature_review",
        skills_gained=("research", "evidence-evaluation", "technical-writing"),
        difficulty="easy",
        estimated_hours=3.0,
        description=(
            "Kumpulkan dan sintesis sumber terbaik untuk skill yang sedang dipelajari, "
            "lalu ubah hasilnya menjadi checklist hands-on."
        ),
        goal_hints=("sertifikasi", "research", "evidence"),
    ),
    LearningProject(
        id="data-pipeline-etl",
        title="Pipeline ETL dengan data quality gate",
        pack="data-engineer",
        operation="etl",
        skills_gained=("data-engineering", "etl", "data-quality"),
        difficulty="medium",
        estimated_hours=8.0,
        description=(
            "Jalankan job ETL pada dataset nyata dengan transformasi, quality rules, "
            "dan target schema untuk menutup gap data engineering."
        ),
        goal_hints=("data", "engineering", "sertifikasi", "portfolio"),
    ),
)


class CrossPackBridge:
    """Executes learning projects by delegating to other capability packs."""

    def __init__(
        self,
        analytics: LearningAnalytics | None = None,
        aligner: GoalAligner | None = None,
        catalog: tuple[LearningProject, ...] = LEARNING_CATALOG,
    ) -> None:
        self._analytics = analytics or learning_analytics
        self._aligner = aligner or goal_aligner
        self._catalog = {project.id: project for project in catalog}
        self._handlers: dict[str, Callable[..., Awaitable[dict[str, Any]]]] = {
            "backtest_strategy": self._run_backtest,
            "full_review": self._run_architecture_review,
            "knowledge_graph": self._run_knowledge_graph,
            "literature_review": self._run_research_review,
            "etl": self._run_etl,
        }

    # ------------------------------------------------------------------
    # Catalog
    # ------------------------------------------------------------------

    def catalog(self, goal_id: str | None = None) -> list[dict[str, Any]]:
        """List learning projects, optionally filtered by goal relevance."""
        out = []
        for project in self._catalog.values():
            payload = _project_payload(project)
            if goal_id:
                alignment = self._aligner.align(
                    title=project.title,
                    skills=list(project.skills_gained),
                    goal_id=goal_id,
                )
                payload["goal_alignment"] = round(alignment.score, 2)
                payload["goal_verdict"] = alignment.verdict
            out.append(payload)
        return out

    def get_project(self, project_id: str) -> LearningProject | None:
        return self._catalog.get(project_id)

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    async def run(
        self,
        project_id: str,
        params: dict[str, Any] | None = None,
        duration_minutes: float = 60.0,
        goal_id: str | None = None,
        notes: str = "",
    ) -> dict[str, Any]:
        """Run a learning project through its pack and record the progress."""
        project = self._catalog.get(project_id)
        if project is None:
            raise KeyError(f"Unknown learning project: {project_id}")
        params = params or {}
        started = time.perf_counter()
        handler = self._handlers.get(project.operation)
        if handler is None:
            raise ValueError(f"No handler for operation: {project.operation}")

        error: str | None = None
        result: dict[str, Any] = {}
        try:
            result = await handler(params)
        except Exception as exc:
            logger.warning("Learning project %s failed: %s", project_id, exc)
            error = f"{type(exc).__name__}: {exc}"

        elapsed_minutes = duration_minutes or round((time.perf_counter() - started) / 60.0, 3)
        alignment = self._aligner.align(
            title=project.title,
            skills=list(project.skills_gained),
            goal_id=goal_id,
            duration_minutes=elapsed_minutes,
        )
        activity = self._analytics.record_activity(
            title=project.title,
            kind=ActivityKind.CROSS_PACK.value,
            duration_minutes=elapsed_minutes,
            skills=list(project.skills_gained),
            goal_id=alignment.goal_id,
            goal_alignment=alignment.score,
            goal_verdict=alignment.verdict,
            source_pack=project.pack,
            notes=notes,
            metadata={
                "learning_project_id": project.id,
                "operation": project.operation,
                "params": params,
                "succeeded": error is None,
            },
        )
        return {
            "project": _project_payload(project),
            "activity_id": activity.id,
            "goal_alignment": round(alignment.score, 2),
            "goal_verdict": alignment.verdict,
            "duration_minutes": elapsed_minutes,
            "status": "completed" if error is None else "failed",
            "error": error,
            "result": result,
        }

    # ------------------------------------------------------------------
    # Pack handlers
    # ------------------------------------------------------------------

    async def _run_backtest(self, params: dict[str, Any]) -> dict[str, Any]:
        from apps.trading_analyst.backtest_engine import BacktestEngine

        candles = params.get("ohlcv_data") or []
        strategy = params.get("strategy")
        if not candles or strategy is None:
            return {
                "status": "skipped",
                "reason": "ohlcv_data dan strategy wajib diisi untuk backtest",
                "hint": "Gunakan /api/v1/trading/analyze lebih dulu untuk mendapat data pasar.",
            }
        engine = BacktestEngine()
        backtest = engine.run_backtest(
            ohlcv_data=candles,
            strategy=strategy,
            initial_capital=float(params.get("initial_capital", 10000.0)),
            position_size_percent=float(params.get("position_size_percent", 0.02)),
        )
        return {
            "status": "executed",
            "total_trades": backtest.total_trades,
            "win_rate": round(backtest.win_rate, 4),
            "profit_factor": round(backtest.profit_factor, 4),
            "total_pnl": round(backtest.total_pnl, 4),
            "final_capital": round(float(backtest.metadata.get("final_capital", 0.0)), 2),
        }

    async def _run_architecture_review(self, params: dict[str, Any]) -> dict[str, Any]:
        from apps.system_architect.worker import SystemArchitectWorker

        workspace_path = params.get("workspace_path")
        if not workspace_path:
            return {"status": "skipped", "reason": "workspace_path wajib diisi untuk review"}
        report = await SystemArchitectWorker().execute(
            {
                "workspace_path": workspace_path,
                "review_type": params.get("review_type", "full_review"),
                "focus_areas": params.get("focus_areas", []),
            }
        )
        if "error" in report:
            return {"status": "failed", "reason": report["error"]}
        return {
            "status": "executed",
            "review_type": report.get("review_type"),
            "findings": len(report.get("findings", []) or []),
            "recommendations": len(report.get("recommendations", []) or []),
            "metrics": report.get("architecture_metrics", {}),
        }

    async def _run_knowledge_graph(self, params: dict[str, Any]) -> dict[str, Any]:
        from apps.knowledge_engineer.worker import KnowledgeEngineerWorker

        domain = params.get("domain", "personal-learning")
        project_name = params.get("project_name", "Personal Learning Knowledge Graph")
        entities = list(params.get("entities", []) or [domain, "skill", "project", "milestone"])
        report = await _maybe_await(
            KnowledgeEngineerWorker().execute(
                {
                    "operation": "knowledge_graph",
                    "business_context": {
                        "project_name": project_name,
                        "domain": domain,
                        "team_size": 1,
                    },
                    "inputs": {
                        "operation": "knowledge_graph",
                        "domain": domain,
                        "store_type": "graph",
                        "entities": entities,
                        "relationships": params.get("relationships", []),
                    },
                }
            )
        )
        return {
            "status": "executed",
            "ontology_classes": len(report.get("ontology_classes", [])),
            "relationship_types": len(report.get("relationship_types", [])),
            "quality_score": report.get("quality_score"),
            "recommendations": report.get("recommendations", []),
        }

    async def _run_research_review(self, params: dict[str, Any]) -> dict[str, Any]:
        from apps.research_assistant.worker import ResearchAssistantWorker

        query = params.get("query")
        if not query:
            return {"status": "skipped", "reason": "query wajib diisi untuk literature review"}
        report = await _maybe_await(ResearchAssistantWorker().execute({"query": query}))
        return {
            "status": "executed",
            "sources": len(report.get("sources", []) or []),
            "confidence": report.get("confidence"),
            "summary": report.get("summary"),
        }

    async def _run_etl(self, params: dict[str, Any]) -> dict[str, Any]:
        from apps.data_engineer.worker import DataEngineerWorker

        source_location = params.get("source_location")
        if not source_location:
            return {
                "status": "skipped",
                "reason": "source_location wajib diisi untuk menjalankan job ETL",
            }
        report = await _maybe_await(
            DataEngineerWorker().execute(
                {
                    "job_type": params.get("job_type", "etl"),
                    "source": {
                        "type": params.get("source_type", "csv"),
                        "location": source_location,
                        "schema": params.get("schema"),
                    },
                    "operations": params.get("operations", []),
                    "quality_rules": params.get("quality_rules", []),
                    "feature_definitions": params.get("feature_definitions", []),
                }
            )
        )
        return {
            "status": "executed",
            "job_id": report.get("job_id"),
            "job_type": report.get("job_type"),
            "rows_processed": report.get("rows_processed"),
            "quality_report": report.get("quality_report"),
        }


async def _maybe_await(value: Any) -> Any:
    """Await ``value`` when the target pack exposes a coroutine, else pass through."""
    if inspect.isawaitable(value):
        return await value
    return value


def _project_payload(project: LearningProject) -> dict[str, Any]:
    return {
        "id": project.id,
        "title": project.title,
        "pack": project.pack,
        "operation": project.operation,
        "skills_gained": list(project.skills_gained),
        "difficulty": project.difficulty,
        "estimated_hours": project.estimated_hours,
        "description": project.description,
    }


cross_pack_bridge = CrossPackBridge()
