"""Quick test for Research Assistant engine."""
import asyncio
from apps.research_assistant.engine import research_engine
from apps.research_assistant.schemas import ResearchRequest


async def main():
    request = ResearchRequest(
        query="AI software engineering productivity",
        operation="literature_review",
        max_sources=10,
        min_confidence=0.5,
        include_contradictions=True,
        include_citations=True,
    )
    report = await research_engine.analyze(request)
    print("Evidence:", len(report.evidence))
    print("Findings:", len(report.findings))
    print("Citations:", len(report.citations))
    print("Contradictions:", len(report.contradictions))
    print("Confidence:", report.confidence)
    print("Report length:", len(report.report_markdown))


if __name__ == "__main__":
    asyncio.run(main())
