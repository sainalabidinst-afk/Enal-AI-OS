"""
Business Analyst — Process Optimizer.

Identifies inefficiencies in business processes and
recommends improvements based on process models.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.business_analyst.schemas import (
    ProcessModel,
    ProcessActivity,
    ProcessOptimization,
)

logger = logging.getLogger(__name__)


# Inefficiency patterns and their remedies.
_INEFFICIENCY_PATTERNS: list[tuple[str, str, str, str]] = [
    ("manual", "Manual data entry", "Automate data capture with forms and integrations", "70%"),
    ("approval", "Sequential approval chain", "Implement parallel approvals with SLA tracking", "60%"),
    ("rework", "Error correction loop", "Add validation at source; reduce rework cycles", "50%"),
    ("wait", "Waiting for external input", "Implement SLAs and escalation paths", "40%"),
    ("duplicate", "Duplicate data entry", "Single source of truth; eliminate redundant entries", "80%"),
    ("batch", "Batch processing delay", "Move to event-driven or near-real-time processing", "65%"),
]


class ProcessOptimizer:
    """
    Identifies process inefficiencies and recommends improvements.

    Usage::

        optimizer = ProcessOptimizer()
        recs = optimizer.optimize(process_model)
    """

    def optimize(self, process_model: ProcessModel | None) -> list[ProcessOptimization]:
        """
        Analyze a process model and identify optimization opportunities.

        Args:
            process_model: ProcessModel to analyze.

        Returns:
            List of ProcessOptimization recommendations.
        """
        if not process_model or not process_model.activities:
            return []

        optimizations: list[ProcessOptimization] = []
        activities = process_model.activities

        # Analyze for inefficiency patterns.
        for activity in activities:
            opt = self._check_activity(activity, activities)
            if opt:
                optimizations.append(opt)

        # Analyze overall process structure.
        structure_opts = self._check_structure(activities)
        optimizations.extend(structure_opts)

        return optimizations

    def _check_activity(
        self, activity: ProcessActivity, all_activities: list[ProcessActivity]
    ) -> ProcessOptimization | None:
        """Check a single activity for inefficiencies."""
        desc_lower = activity.description.lower()
        name_lower = activity.name.lower()

        for keyword, inefficiency, recommendation, savings in _INEFFICIENCY_PATTERNS:
            if keyword in desc_lower or keyword in name_lower:
                return ProcessOptimization(
                    process_name=activity.name,
                    inefficiency=inefficiency,
                    current_time=self._estimate_time(activity),
                    optimized_time=self._estimate_optimized_time(activity, savings),
                    recommendation=recommendation,
                    estimated_savings=savings,
                )

        return None

    def _check_structure(self, activities: list[ProcessActivity]) -> list[ProcessOptimization]:
        """Check overall process structure for inefficiencies."""
        optimizations: list[ProcessOptimization] = []

        # Check for too many sequential steps.
        decision_count = sum(1 for a in activities if a.type.value == "decision")
        if decision_count > 3:
            optimizations.append(ProcessOptimization(
                process_name="Overall Process",
                inefficiency="Too many sequential decision points",
                current_time=f"{len(activities)} sequential steps",
                optimized_time=f"~{len(activities) // 2} parallel steps",
                recommendation="Parallelize independent decisions; reduce approval chains",
                estimated_savings="40%",
            ))

        # Check for redundant activities.
        activity_names = [a.name.lower() for a in activities]
        duplicates = [name for name in activity_names if activity_names.count(name) > 1]
        if duplicates:
            optimizations.append(ProcessOptimization(
                process_name="Overall Process",
                inefficiency="Duplicate activities detected",
                current_time=f"{len(duplicates)} redundant steps",
                optimized_time="0 redundant steps",
                recommendation="Consolidate duplicate activities into single step",
                estimated_savings="100%",
            ))

        return optimizations

    def _estimate_time(self, activity: ProcessActivity) -> str:
        """Estimate current time for an activity."""
        desc_lower = activity.description.lower()
        if "manual" in desc_lower:
            return "2-4 hours"
        if "approval" in desc_lower:
            return "1-3 days"
        if "batch" in desc_lower:
            return "4-24 hours"
        return "15-30 minutes"

    def _estimate_optimized_time(self, activity: ProcessActivity, savings: str) -> str:
        """Estimate optimized time based on savings percentage."""
        pct = int(savings.replace("%", "")) / 100
        current = self._estimate_time(activity)
        # Simple heuristic: reduce time proportionally.
        if "hour" in current:
            hours = float(current.split("-")[0])
            new_hours = max(0.1, hours * (1 - pct))
            return f"{new_hours:.1f} hours"
        if "day" in current:
            days = float(current.split("-")[0])
            new_days = max(0.1, days * (1 - pct))
            return f"{new_days:.1f} days"
        return "< 5 minutes"
