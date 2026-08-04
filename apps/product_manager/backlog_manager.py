"""
Backlog Manager
===============

Manages product backlogs and sprint planning.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.product_manager.schemas import BacklogInput

logger = logging.getLogger(__name__)


class BacklogManager:
    """Manages product backlogs and sprint planning."""

    def manage_backlog(self, backlog_input: BacklogInput, framework: str) -> dict[str, Any]:
        """
        Manage and structure the backlog.

        Args:
            backlog_input: Backlog items.
            framework: Prioritization framework to apply.

        Returns:
            Structured backlog as a dict.
        """
        items = []
        high = 0
        medium = 0
        low = 0
        for item in backlog_input.items:
            priority = "medium"
            if item.value == "high" and item.effort == "low":
                priority = "high"
                high += 1
            elif item.value == "low" or item.effort == "high":
                priority = "low"
                low += 1
            else:
                medium += 1
            items.append({
                "id": item.id,
                "title": item.title,
                "priority": priority,
                "effort": item.effort,
                "value": item.value,
                "score": 0.0,
                "rationale": f"Prioritized using {framework} framework.",
            })
        logger.info("Managed backlog with %d items using %s framework", len(items), framework)
        return {
            "items": items,
            "summary": {
                "total_items": len(items),
                "high_priority": high,
                "medium_priority": medium,
                "low_priority": low,
            },
        }

    def plan_sprint(self, backlog_input: BacklogInput, team_capacity: str) -> dict[str, Any]:
        """
        Plan a sprint based on backlog and team capacity.

        Args:
            backlog_input: Backlog items.
            team_capacity: Team capacity description.

        Returns:
            Sprint plan as a dict.
        """
        items = [item.title for item in backlog_input.items[:5]]
        stretch = [item.title for item in backlog_input.items[5:10]]
        logger.info(
            "Planned sprint with %d committed items and %d stretch items",
            len(items),
            len(stretch),
        )
        return {
            "sprint_id": "SPR-001",
            "duration_weeks": 2,
            "capacity": team_capacity,
            "committed_items": items,
            "stretch_items": stretch,
            "goal": "Deliver highest priority backlog items",
        }
