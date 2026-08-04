"""
Prioritizer
============

Applies consistent prioritization frameworks to backlog items.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.product_manager.schemas import BacklogInput

logger = logging.getLogger(__name__)


class Prioritizer:
    """Applies consistent prioritization frameworks."""

    def prioritize(self, backlog_input: BacklogInput, framework: str) -> dict[str, Any]:
        """
        Prioritize backlog items using the given framework.

        Args:
            backlog_input: Backlog items.
            framework: Prioritization framework to apply.

        Returns:
            Prioritized backlog as a dict.
        """
        ranked = []
        for idx, item in enumerate(backlog_input.items):
            score = self._compute_score(item, framework)
            ranked.append({
                "id": item.id,
                "rank": idx + 1,
                "score": round(score, 2),
                "rationale": f"Scored using {framework} framework.",
            })
        ranked.sort(key=lambda x: float(x["score"]), reverse=True)
        logger.info("Prioritized %d items using %s framework", len(ranked), framework)
        return {
            "framework": framework,
            "ranked_items": ranked,
            "top_5": [i["id"] for i in ranked[:5]],
        }

    def _compute_score(self, item: Any, framework: str) -> float:
        if framework == "rice":
            reach = 3.0
            impact = 2.0
            confidence = 0.8
            effort = 1.0
            return (reach * impact * confidence) / max(effort, 0.1)
        if framework == "moscow":
            if item.value == "high":
                return 4.0
            if item.value == "medium":
                return 2.0
            return 1.0
        if framework == "value_effort":
            value_map = {"high": 3.0, "medium": 2.0, "low": 1.0}
            effort_map = {"low": 3.0, "medium": 2.0, "high": 1.0}
            return value_map.get(item.value, 1.0) * effort_map.get(item.effort, 1.0)
        return 1.0
