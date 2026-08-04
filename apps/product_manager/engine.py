"""
Product Manager — Domain Engine orchestrator.

Orchestrates the full product management pipeline:
    1. Roadmap Management
    2. Backlog Management
    3. Sprint Planning
    4. OKR/KPI Tracking
    5. Prioritization
    6. Release Coordination

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
import time
from typing import Any

from apps.product_manager.backlog_manager import BacklogManager
from apps.product_manager.okr_tracker import OKRTracker
from apps.product_manager.prioritizer import Prioritizer
from apps.product_manager.roadmap_manager import RoadmapManager
from apps.product_manager.schemas import (
    ProductManagementReport,
    ProductManagementRequest,
    ProductRecord,
)

logger = logging.getLogger(__name__)


class ProductManagerEngine:
    """
    Orchestrates the full product management pipeline.

    Public API::

        engine = ProductManagerEngine()
        report = engine.manage(request)
    """

    def __init__(self) -> None:
        self.roadmap_manager = RoadmapManager()
        self.backlog_manager = BacklogManager()
        self.okr_tracker = OKRTracker()
        self.prioritizer = Prioritizer()

    def manage(self, request: ProductManagementRequest) -> ProductManagementReport:
        started = time.monotonic()
        if hasattr(request.operation, "value"):
            op_value = request.operation.value
        else:
            op_value = str(request.operation)
        op = op_value

        roadmap: dict[str, Any] = {}
        backlog: dict[str, Any] = {"items": [], "summary": {}}
        sprint_plan: dict[str, Any] = {}
        okrs: dict[str, Any] = {}
        prioritization: dict[str, Any] = {}
        release_plan: dict[str, Any] = {}

        if op == "roadmap_management":
            roadmap = self.roadmap_manager.create_roadmap(
                request.product_context, request.inputs.roadmap
            )

        elif op == "backlog_management":
            backlog = self.backlog_manager.manage_backlog(
                request.inputs.backlog, request.options.prioritization_framework
            )

        elif op == "sprint_planning":
            sprint_plan = self.backlog_manager.plan_sprint(
                request.inputs.backlog, request.constraints.team_capacity
            )

        elif op == "okr_tracking":
            okrs = self.okr_tracker.track(request.inputs.okrs)

        elif op == "prioritization":
            prioritization = self.prioritizer.prioritize(
                request.inputs.backlog, request.options.prioritization_framework
            )

        elif op == "release_coordination":
            release_plan = self.roadmap_manager.coordinate_release(
                request.inputs.roadmap, request.inputs.backlog
            )

        quality_metrics = self._compute_quality_metrics(
            roadmap, backlog, okrs, prioritization, release_plan
        )
        explanation = self._build_explanation(
            op, roadmap, backlog, sprint_plan, okrs, prioritization, release_plan
        )

        report = ProductManagementReport(
            request_id=request.request_id,
            operation=op,
            roadmap=roadmap,
            backlog=backlog,
            sprint_plan=sprint_plan,
            okrs=okrs,
            prioritization=prioritization,
            release_plan=release_plan,
            quality_score=quality_metrics.get("overall", 0.0),
            explanation=explanation,
            raw={
                "latency_ms": round((time.monotonic() - started) * 1000.0, 2),
            },
        )

        record = ProductRecord(
            request_id=request.request_id,
            operation=op,
            product_name=request.product_context.product_name,
            backlog_items_managed=len(backlog.get("items", [])),
            okrs_tracked=len(okrs.get("objectives", [])),
            sprints_planned=1 if sprint_plan else 0,
            releases_coordinated=len(release_plan.get("releases", [])),
            outcome="success",
        )
        self._record(record)

        return report

    def _compute_quality_metrics(
        self,
        roadmap: dict[str, Any],
        backlog: dict[str, Any],
        okrs: dict[str, Any],
        prioritization: dict[str, Any],
        release_plan: dict[str, Any],
    ) -> dict[str, float]:
        score = 0.5
        if roadmap:
            score += 0.1
        if backlog.get("items"):
            score += 0.1
        if okrs.get("objectives"):
            score += 0.1
        if prioritization.get("ranked_items"):
            score += 0.1
        if release_plan.get("releases"):
            score += 0.1
        return {"overall": max(0.0, min(1.0, score))}

    def _build_explanation(
        self,
        op: str,
        roadmap: dict[str, Any],
        backlog: dict[str, Any],
        sprint_plan: dict[str, Any],
        okrs: dict[str, Any],
        prioritization: dict[str, Any],
        release_plan: dict[str, Any],
    ) -> str:
        parts = [f"Performed {op}."]
        if roadmap:
            parts.append(f"Roadmap with {len(roadmap.get('milestones', []))} milestones.")
        if backlog.get("items"):
            parts.append(f"Backlog with {len(backlog['items'])} items.")
        if sprint_plan:
            parts.append(
                f"Sprint plan with {len(sprint_plan.get('committed_items', []))} committed items."
            )
        if okrs.get("objectives"):
            parts.append(f"{len(okrs['objectives'])} OKR objectives tracked.")
        if prioritization.get("ranked_items"):
            parts.append(f"Prioritized {len(prioritization['ranked_items'])} items.")
        if release_plan.get("releases"):
            parts.append(f"{len(release_plan['releases'])} releases coordinated.")
        return " ".join(parts)

    def _record(self, record: ProductRecord) -> str:
        try:
            import json
            from pathlib import Path
            base = Path("artifacts/product_history")
            base.mkdir(parents=True, exist_ok=True)
            path = base / f"{record.record_id}.json"
            path.write_text(
                json.dumps(record.model_dump(), indent=2, default=str),
                encoding="utf-8",
            )
        except OSError:
            logger.warning("Failed to persist product record %s", record.record_id)
        return record.record_id


product_manager_engine = ProductManagerEngine()
