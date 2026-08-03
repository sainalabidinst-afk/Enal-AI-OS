"""
Research Assistant Reference App
====================================

Demonstrates ECP capabilities for AI-powered research.
Uses: SDK, Runtime, Marketplace, Studio, Contracts

Workflow:
1. Natural Language Input
2. Intent Understanding
3. Capability Selection
4. Task Decomposition
5. Evidence Gathering
6. Analysis
7. Report Generation
8. Citation
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.research_assistant.engine import research_engine
from apps.research_assistant.schemas import ResearchOperation, ResearchRequest
from apps.research_assistant.worker import ResearchAssistantWorker


class ResearchAssistantApp(BaseReferenceApp):
    name = "research-assistant"
    version = "1.0.0"
    description = "AI-powered research assistant with evidence gathering and citations"
    category = "research"
    pipeline = ["perception", "memory", "reasoning", "decision", "action"]

    def __init__(self):
        self.engine = research_engine
        self.worker = ResearchAssistantWorker()

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        project_id = context.get("project_id", "research-assistant-default")

        request = ResearchRequest(
            query=user_input,
            operation=ResearchOperation.literature_review,
            max_sources=20,
            min_confidence=0.5,
            include_contradictions=True,
            include_citations=True,
            context=context,
        )
        report = await self.engine.analyze(request)

        return {
            "app": self.name,
            "version": self.version,
            "input": user_input,
            "pipeline": self.pipeline,
            "result": report.to_dict() if hasattr(report, "to_dict") else report,
            "metadata": {
                "category": self.category,
                "capabilities_used": [
                    "research",
                    "literature-review",
                    "data-analysis",
                    "report-writing",
                ],
            },
        }


def get_app() -> ResearchAssistantApp:
    """Get the Research Assistant app instance."""
    return ResearchAssistantApp()
