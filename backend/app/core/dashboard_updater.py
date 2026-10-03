"""
Dashboard Updater — Core Service.

Updates the dashboard with execution artifacts and timeline
for the E2E scenario and general-purpose observability.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ArtifactPreview(BaseModel):
    """Preview of a dashboard artifact."""

    name: str = ""
    type: str = "file"
    url: str = ""
    size_bytes: int = 0
    status: str = "ready"


class TimelineEntry(BaseModel):
    """Single entry in the execution timeline."""

    step: str = ""
    status: str = "pending"
    started_at: str = ""
    completed_at: str = ""
    duration_ms: float = 0.0
    details: str = ""


class DashboardUpdate(BaseModel):
    """Dashboard state update payload."""

    execution_id: str = ""
    timeline: list[TimelineEntry] = Field(default_factory=list)
    artifacts: list[ArtifactPreview] = Field(default_factory=list)
    status: str = "running"
    current_step: str = ""
    summary: str = ""
    formula: str = ""
    inputs_traced: list[str] = Field(default_factory=list)
    quality_score: float = Field(default=0.90, ge=0, le=1)


class DashboardUpdaterService:
    """Update dashboard with execution artifacts and timeline."""

    VERSION = "1.0.0"

    def create_update(
        self,
        execution_id: str,
        steps: list[str],
        artifacts: list[dict[str, Any]] | None = None,
    ) -> DashboardUpdate:
        """Create a dashboard update from execution steps and artifacts."""
        now = datetime.now(UTC).isoformat()
        timeline: list[TimelineEntry] = []
        inputs_traced: list[str] = ["execution_id", "steps", "artifacts"]

        for idx, step in enumerate(steps):
            timeline.append(
                TimelineEntry(
                    step=step,
                    status="completed" if idx < len(steps) - 1 else "running",
                    started_at=now,
                    completed_at=now if idx < len(steps) - 1 else "",
                    duration_ms=0.0,
                    details=f"Step {idx + 1}/{len(steps)}",
                )
            )
            inputs_traced.append(step)

        artifact_previews: list[ArtifactPreview] = []
        if artifacts:
            for artifact in artifacts:
                artifact_previews.append(
                    ArtifactPreview(
                        name=artifact.get("name", ""),
                        type=artifact.get("type", "file"),
                        url=artifact.get("url", ""),
                        size_bytes=artifact.get("size_bytes", 0),
                        status=artifact.get("status", "ready"),
                    )
                )
                inputs_traced.append(artifact.get("name", "artifact"))

        status = "completed" if all(t.status == "completed" for t in timeline) else "running"
        current_step = timeline[-1].step if timeline else ""

        return DashboardUpdate(
            execution_id=execution_id,
            timeline=timeline,
            artifacts=artifact_previews,
            status=status,
            current_step=current_step,
            summary=f"Dashboard updated for execution {execution_id}",
            formula="dashboard: execution_id + steps + artifacts -> update",
            inputs_traced=inputs_traced,
            quality_score=0.93,
        )

    def append_artifact(
        self, update: DashboardUpdate, artifact: dict[str, Any]
    ) -> DashboardUpdate:
        """Append a new artifact to an existing dashboard update."""
        update.artifacts.append(
            ArtifactPreview(
                name=artifact.get("name", ""),
                type=artifact.get("type", "file"),
                url=artifact.get("url", ""),
                size_bytes=artifact.get("size_bytes", 0),
                status=artifact.get("status", "ready"),
            )
        )
        update.inputs_traced.append(artifact.get("name", "artifact"))
        return update

    def mark_step_complete(self, update: DashboardUpdate, step: str) -> DashboardUpdate:
        """Mark a timeline step as completed."""
        for entry in update.timeline:
            if entry.step == step:
                entry.status = "completed"
                entry.completed_at = datetime.now(UTC).isoformat()
                break
        update.status = (
            "completed"
            if all(t.status == "completed" for t in update.timeline)
            else "running"
        )
        return update

    def get_record(self) -> dict[str, Any]:
        """Return a capability record for registry/memory."""
        return {
            "pack_id": "dashboard-updater",
            "version": self.VERSION,
            "capabilities": [
                "create_update",
                "append_artifact",
                "mark_step_complete",
            ],
        }


dashboard_updater = DashboardUpdaterService()
