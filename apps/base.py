"""
Base Reference Application
============================

All reference applications inherit from this base class.
This ensures consistency and makes it easy to add new apps.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseApp(ABC):
    """Base class for all ECP Capability Pack applications (canonical name)."""

    name: str = "base"
    version: str = "1.0.0"
    description = "Base reference application"
    category: str = "general"
    pipeline: list[str] = []

    @abstractmethod
    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Run the application with user input."""
        raise NotImplementedError

    async def _execute_pipeline(self, user_input: str, project_id: str | None = None) -> dict[str, Any]:
        """Execute the application's cognitive pipeline."""
        from backend.app.core.adaptive_runtime import adaptive_runtime
        return await adaptive_runtime.execute(
            user_input,
            project_id,
            force_pipeline=self.pipeline if self.pipeline else None,
        )

    def to_dict(self) -> dict[str, Any]:
        """Return app metadata."""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "category": self.category,
            "pipeline": self.pipeline,
        }


# Backward-compatible alias (docs historically referenced BaseReferenceApp).
BaseReferenceApp = BaseApp
