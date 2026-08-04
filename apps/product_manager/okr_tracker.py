"""
OKR Tracker
===========

Tracks OKRs and KPIs with measurable progress.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.product_manager.schemas import OKRInput

logger = logging.getLogger(__name__)


class OKRTracker:
    """Tracks OKRs and KPIs."""

    def track(self, okr_input: OKRInput) -> dict[str, Any]:
        """
        Track OKRs based on the given input.

        Args:
            okr_input: OKR objectives and key results.

        Returns:
            OKR tracking report as a dict.
        """
        objectives: list[dict[str, Any]] = []
        for obj in okr_input.objectives:
            key_results: list[dict[str, Any]] = []
            for kr in obj.key_results:
                current_val = float(kr.current) if kr.current.replace('.', '', 1).isdigit() else 0.0
                target_val = float(kr.target) if kr.target.replace('.', '', 1).isdigit() else 100.0
                progress = min(current_val / target_val, 1.0) if target_val > 0 else 0.0
                key_results.append({
                    "description": kr.description,
                    "target": kr.target,
                    "current": kr.current,
                    "progress": round(progress, 2),
                })
            progress_values = [float(kr["progress"]) for kr in key_results]
            overall = (
                sum(progress_values) / len(key_results)
                if key_results
                else 0.0
            )
            objectives.append({
                "id": obj.id,
                "objective": obj.objective,
                "key_results": key_results,
                "overall_progress": round(overall, 2),
                "confidence": "on_track" if overall >= 0.5 else "at_risk",
            })
        logger.info("Tracked %d OKR objectives", len(objectives))
        return {"quarter": "Q3 2026", "objectives": objectives}
