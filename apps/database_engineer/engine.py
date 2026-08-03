"""
Database Engineer — Domain Engine orchestrator.

Orchestrates the full database engineering pipeline:
    1. Schema Design (data types, normalization, constraints)
    2. Query Optimization (slow query detection, execution plan analysis)
    3. Migration Management (forward/rollback scripts, conflict resolution)
    4. Index Recommendation (based on query patterns)
    5. Replication Planning (HA topologies, failover)
    6. Backup and Recovery (RTO/RPO planning)
    7. Performance Analysis (slow queries, deadlocks, contention)

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
import time
from typing import Any

from apps.database_engineer.schemas import (
    DatabaseRequest,
    DatabaseReport,
    DatabaseAnalysisRecord,
    Finding,
    FindingCategory,
    SchemaRecommendation,
    IndexRecommendation,
    MigrationPlan,
    ReplicationDesign,
    BackupPlan,
    PerformanceStats,
    Severity,
)
from apps.database_engineer.schema_designer import SchemaDesigner
from apps.database_engineer.query_optimizer import QueryOptimizer
from apps.database_engineer.migration_manager import MigrationManager
from apps.database_engineer.index_advisor import IndexAdvisor
from apps.database_engineer.replication_planner import ReplicationPlanner
from apps.database_engineer.backup_planner import BackupPlanner
from apps.database_engineer.performance_analyzer import PerformanceAnalyzer

logger = logging.getLogger(__name__)


class DatabaseEngineerEngine:
    """
    Orchestrates the full database engineering pipeline.

    Public API::

        engine = DatabaseEngineerEngine()
        report = engine.analyze(request)
    """

    def __init__(self) -> None:
        self.schema_designer = SchemaDesigner()
        self.query_optimizer = QueryOptimizer()
        self.migration_manager = MigrationManager()
        self.index_advisor = IndexAdvisor()
        self.replication_planner = ReplicationPlanner()
        self.backup_planner = BackupPlanner()
        self.performance_analyzer = PerformanceAnalyzer()

    def analyze(self, request: DatabaseRequest) -> DatabaseReport:
        """
        Run the database engineering pipeline based on operation.

        Args:
            request: DatabaseRequest with operation, database type, schema, queries.

        Returns:
            DatabaseReport with findings, recommendations, and plans.
        """
        started = time.monotonic()
        all_findings: list[Finding] = []
        schema_recs: list[SchemaRecommendation] = []
        index_recs: list[IndexRecommendation] = []
        migration_plan: MigrationPlan | None = None
        replication_design: ReplicationDesign | None = None
        backup_plan: BackupPlan | None = None
        perf_stats = PerformanceStats()
        explanation_parts: list[str] = []

        op = request.operation.value if hasattr(request.operation, 'value') else str(request.operation)

        if op == "schema_design":
            schema_recs = self.schema_designer.design(request.database_schema, request.database_type)
            all_findings.extend(self._schema_to_findings(schema_recs))
            explanation_parts.append(f"Schema design analysis: {len(schema_recs)} recommendations")

        elif op == "query_optimization":
            opt_results = self.query_optimizer.optimize(request.queries, request.database_type)
            all_findings.extend(opt_results.get("findings", []))
            explanation_parts.append(f"Query optimization: {len(all_findings)} improvements identified")

        elif op == "migration":
            migration_plan = self.migration_manager.plan(
                request.current_schema_version,
                request.target_schema_version,
                request.database_schema,
            )
            explanation_parts.append(
                f"Migration plan: {len(migration_plan.steps)} steps from "
                f"{request.current_schema_version} to {request.target_schema_version}"
            )

        elif op == "index_recommendation":
            index_recs = self.index_advisor.recommend(
                request.queries, request.database_schema, request.workload_profile
            )
            all_findings.extend(self._index_to_findings(index_recs))
            explanation_parts.append(f"Index recommendations: {len(index_recs)} indexes suggested")

        elif op == "replication_plan":
            replication_design = self.replication_planner.design(
                request.workload_profile, request.database_type
            )
            explanation_parts.append(f"Replication design: {replication_design.strategy} topology")

        elif op == "backup_plan":
            backup_plan = self.backup_planner.plan(
                request.database_type, request.rto_hours, request.rpo_minutes
            )
            explanation_parts.append(f"Backup plan: {backup_plan.schedule} with RTO {request.rto_hours}h")

        elif op == "performance_analysis":
            perf_result = self.performance_analyzer.analyze(
                request.queries, request.database_schema, request.workload_profile
            )
            all_findings.extend(perf_result.get("findings", []))
            perf_stats = perf_result.get("stats", PerformanceStats())
            explanation_parts.append(f"Performance analysis: {perf_stats.slow_queries} slow queries detected")

        # Build summary.
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for f in all_findings:
            severity_counts[f.severity.value] = severity_counts.get(f.severity.value, 0) + 1

        overall_risk = self._compute_overall_risk(severity_counts)

        report = DatabaseReport(
            request_id=request.request_id,
            operation=op,
            findings=all_findings,
            schema_recommendations=schema_recs,
            index_recommendations=index_recs,
            migration_plan=migration_plan,
            replication_design=replication_design,
            backup_plan=backup_plan,
            performance_stats=perf_stats,
            explanation=". ".join(explanation_parts) if explanation_parts else f"Analyzed {op} for {request.database_type.value}",
            raw={
                "latency_ms": round((time.monotonic() - started) * 1000.0, 2),
                "overall_risk": overall_risk.value,
                "findings_count": len(all_findings),
                "severity_counts": severity_counts,
            },
        )

        # Record to Experience Memory.
        record = DatabaseAnalysisRecord(
            request_id=request.request_id,
            operation=op,
            database_type=request.database_type.value,
            findings_count=len(all_findings),
            critical_count=severity_counts.get("critical", 0),
            high_count=severity_counts.get("high", 0),
            migration_planned=migration_plan is not None,
            backup_configured=backup_plan is not None,
            outcome="success" if not all_findings else "partial",
        )
        self._record(record)

        return report

    def _schema_to_findings(self, recs: list[SchemaRecommendation]) -> list[Finding]:
        """Convert schema recommendations to findings."""
        findings: list[Finding] = []
        for rec in recs:
            findings.append(Finding(
                category=FindingCategory.schema,
                severity=rec.priority,
                title=f"Schema: {rec.action} on {rec.table}",
                description=rec.rationale,
                recommendation=rec.details.get("sql", ""),
                confidence=0.8,
            ))
        return findings

    def _index_to_findings(self, recs: list[IndexRecommendation]) -> list[Finding]:
        """Convert index recommendations to findings."""
        findings: list[Finding] = []
        for rec in recs:
            findings.append(Finding(
                category=FindingCategory.index,
                severity=rec.priority,
                title=f"Index recommended on {rec.table}({', '.join(rec.columns)})",
                description=f"Add {rec.index_type} index for query performance",
                recommendation=f"CREATE INDEX idx_{rec.table}_{'_'.join(rec.columns)} ON {rec.table} ({', '.join(rec.columns)})",
                estimated_improvement=rec.estimated_impact,
                confidence=0.85,
            ))
        return findings

    def _compute_overall_risk(self, severity_counts: dict[str, int]) -> Severity:
        """Compute overall risk level."""
        critical = severity_counts.get("critical", 0)
        high = severity_counts.get("high", 0)
        if critical > 0:
            return Severity.critical
        if high > 0:
            return Severity.high
        if severity_counts.get("medium", 0) > 2:
            return Severity.medium
        return Severity.low

    def _record(self, record: DatabaseAnalysisRecord) -> str:
        """Record to in-memory store (Experience Memory interface)."""
        try:
            import json
            from pathlib import Path
            base = Path("artifacts/database_history")
            base.mkdir(parents=True, exist_ok=True)
            path = base / f"{record.record_id}.json"
            path.write_text(
                json.dumps(record.model_dump(), indent=2, default=str),
                encoding="utf-8",
            )
        except OSError:
            logger.warning("Failed to persist database record %s", record.record_id)
        return record.record_id
