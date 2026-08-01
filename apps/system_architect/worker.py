"""
System Architect Worker — thin adapter (per ADR-003).

Routes task requests to the System Architect Domain Engine.
Does not own business logic; delegates to SystemArchitectEngine.
"""

from __future__ import annotations

from typing import Any

from apps.system_architect.engine import SystemArchitectEngine
from apps.system_architect.schemas import ArchitectureReviewRequest, ReviewType


class SystemArchitectWorker:
    """
    Thin Worker adapter for the System Architect Capability Pack.

    Responsibilities:
        - Parse incoming task into ArchitectureReviewRequest
        - Delegate to SystemArchitectEngine.review()
        - Return ArchitectureReviewReport as dict

    Usage::
        worker = SystemArchitectWorker()
        result = await worker.execute(task)
    """

    def __init__(self, engine: SystemArchitectEngine | None = None) -> None:
        self._engine = engine or SystemArchitectEngine()

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute an architecture review task.

        Expected task format::

            {
                "workspace_path": "...",
                "review_type": "full_review",
                "architecture_style": "clean_architecture",
                "existing_adrs": ["ADR-001"],
                "constraints": [],
                "focus_areas": [],
                "include_recommendations": true
            }

        Returns:
            ArchitectureReviewReport as a JSON-serializable dict.
        """
        # Validate workspace path
        workspace_path = task.get("workspace_path")
        if not workspace_path:
            return {"error": "workspace_path is required"}

        # Parse review type safely
        review_type_raw = task.get("review_type", "full_review")
        try:
            review_type = ReviewType(review_type_raw)
        except ValueError:
            review_type = ReviewType.full_review

        request = ArchitectureReviewRequest(
            review_id=task.get("review_id", ""),
            review_type=review_type,
            workspace_path=workspace_path,
            architecture_style=task.get("architecture_style", "clean_architecture"),
            existing_adrs=task.get("existing_adrs", []),
            constraints=task.get("constraints", []),
            focus_areas=task.get("focus_areas", []),
            include_recommendations=task.get("include_recommendations", True),
        )

        try:
            report = await self._engine.review(request)
            return report.to_dict()
        except FileNotFoundError as exc:
            return {"error": str(exc)}
        except Exception as exc:  # pragma: no cover
            return {"error": f"Architecture review failed: {exc}"}
