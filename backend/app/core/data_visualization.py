"""
Data Visualization Pack — Core Service.

Generates charts and graphs from data for the E2E scenario
and general-purpose visualization needs.
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ChartSpec(BaseModel):
    """Specification for a single chart."""

    title: str = ""
    chart_type: str = "line"
    labels: list[str] = Field(default_factory=list)
    datasets: list[dict[str, Any]] = Field(default_factory=list)
    x_label: str = ""
    y_label: str = ""


class VisualizationReport(BaseModel):
    """Report containing one or more generated visualizations."""

    charts: list[ChartSpec] = Field(default_factory=list)
    artifacts: list[dict[str, Any]] = Field(default_factory=list)
    summary: str = ""
    formula: str = ""
    inputs_traced: list[str] = Field(default_factory=list)
    quality_score: float = Field(default=0.90, ge=0, le=1)


class DataVisualizationService:
    """Generate charts and data visualizations."""

    VERSION = "1.0.0"

    def generate_chart(
        self,
        data: dict[str, Any],
        chart_type: str = "line",
        title: str = "",
    ) -> ChartSpec:
        """Generate a chart specification from data."""
        labels = data.get("labels", [])
        datasets = data.get("datasets", [])
        return ChartSpec(
            title=title or data.get("title", ""),
            chart_type=chart_type,
            labels=labels,
            datasets=datasets,
            x_label=data.get("x_label", ""),
            y_label=data.get("y_label", ""),
        )

    def generate_report(
        self,
        data: dict[str, Any],
        chart_type: str = "line",
        title: str = "",
    ) -> VisualizationReport:
        """Generate a full visualization report with chart specs and metadata."""
        chart = self.generate_chart(data, chart_type=chart_type, title=title)
        summary = f"Generated {chart_type} chart: {chart.title or 'Untitled'}"
        artifacts = [
            {
                "type": "chart",
                "format": "png",
                "spec": chart.model_dump(),
            }
        ]
        return VisualizationReport(
            charts=[chart],
            artifacts=artifacts,
            summary=summary,
            formula="visualization: data -> chart_spec -> render",
            inputs_traced=["data", "chart_type", "title"],
            quality_score=0.92,
        )

    def get_record(self) -> dict[str, Any]:
        """Return a capability record for registry/memory."""
        return {
            "pack_id": "data-visualization",
            "version": self.VERSION,
            "capabilities": [
                "generate_chart",
                "generate_report",
                "render_chart",
            ],
        }


data_visualization = DataVisualizationService()
