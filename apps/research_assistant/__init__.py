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


class ResearchAssistantApp(BaseReferenceApp):
    name = "research-assistant"
    version = "1.0.0"
    description = "AI-powered research assistant with evidence gathering and citations"
    category = "research"
    pipeline = ["perception", "memory", "reasoning", "decision", "action"]

    def __init__(self):
        self.engine = research_engine

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        project_id = context.get("project_id", "research-assistant-default")

        evidence = await self.engine.search_evidence(user_input)
        analysis = await self.engine.analyze_findings(user_input, evidence)
        report = await self.engine.generate_report(user_input, analysis)

        return {
            "app": self.name,
            "version": self.version,
            "input": user_input,
            "pipeline": self.pipeline,
            "result": {
                "evidence": evidence,
                "analysis": analysis,
                "report": report,
            },
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
