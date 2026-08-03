"""
Research Assistant Worker — thin adapter (per ADR-003).

Routes task requests to the Research Assistant Domain Engine.
Does not own business logic; delegates to ResearchEngine.
"""

from __future__ import annotations

from typing import Any

from apps.research_assistant.engine import ResearchEngine
from apps.research_assistant.schemas import (
    CitationStyle,
    ResearchOperation,
    ResearchRequest,
)


class ResearchAssistantWorker:
    """
    Thin Worker adapter for the Research Assistant Capability Pack.

    Responsibilities:
        - Parse incoming task into ResearchRequest
        - Delegate to ResearchEngine.analyze()
        - Return ResearchReport as dict

    Usage::

        worker = ResearchAssistantWorker()
        report = await worker.execute(task)
    """

    def __init__(self, engine: ResearchEngine | None = None) -> None:
        self._engine = engine or ResearchEngine()

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a research task.

        Expected task format::

            {
                "query": "What is the effect of AI on software development productivity?",
                "operation": "literature_review",
                "sources": [...],
                "citation_style": "apa",
                "max_sources": 20,
                "include_contradictions": true
            }

        Returns:
            ResearchReport as a JSON-serializable dict.
        """
        query = task.get("query", "")
        if not query:
            return {"error": "Missing required field: query"}

        op_value = task.get("operation", "literature_review")
        try:
            operation = ResearchOperation(op_value)
        except ValueError:
            operation = ResearchOperation.literature_review

        style_value = task.get("citation_style", "apa")
        try:
            citation_style = CitationStyle(style_value)
        except ValueError:
            citation_style = CitationStyle.apa

        request = ResearchRequest(
            query=query,
            operation=operation,
            citation_style=citation_style,
            max_sources=task.get("max_sources", 20),
            min_confidence=task.get("min_confidence", 0.5),
            include_contradictions=task.get("include_contradictions", True),
            include_citations=task.get("include_citations", True),
            context=task.get("context", {}),
            metadata=task.get("metadata", {}),
        )

        report = await self._engine.analyze(request)
        return report.to_dict()
