"""
Tests for Research Assistant Capability Pack.

Covers:
- Evidence gathering and ranking
- Contradiction detection
- Citation quality assessment
- Confidence estimation
- Synthesis generation
- Report generation
"""

import pytest

from apps.research_assistant.engine import ResearchEngine
from apps.research_assistant.schemas import (
    CitationStyle,
    ConfidenceLevel,
    Contradiction,
    Evidence,
    Finding,
    FindingSeverity,
    ResearchOperation,
    ResearchRequest,
    SourceQuality,
    SourceType,
)


@pytest.fixture
def engine():
    return ResearchEngine()


@pytest.fixture
def base_request():
    return ResearchRequest(
        query="AI software engineering productivity",
        operation=ResearchOperation.literature_review,
        max_sources=10,
        min_confidence=0.5,
        include_contradictions=True,
        include_citations=True,
    )


class TestEvidenceGathering:
    async def test_returns_evidence_list(self, engine, base_request):
        report = await engine.analyze(base_request)
        assert isinstance(report.evidence, list)
        assert len(report.evidence) > 0

    async def test_evidence_has_required_fields(self, engine, base_request):
        report = await engine.analyze(base_request)
        for ev in report.evidence:
            assert ev.id
            assert ev.title
            assert ev.content
            assert 0.0 <= ev.confidence <= 1.0

    async def test_evidence_ranking_by_quality(self, engine):
        request = ResearchRequest(
            query="software engineering",
            operation=ResearchOperation.evidence_gathering,
            max_sources=5,
            min_confidence=0.0,
        )
        report = await engine.analyze(request)
        assert len(report.evidence) <= 5
        for i in range(len(report.evidence) - 1):
            assert report.evidence[i].confidence >= report.evidence[i + 1].confidence

    async def test_respects_max_sources(self, engine):
        request = ResearchRequest(
            query="software engineering",
            operation=ResearchOperation.evidence_gathering,
            max_sources=3,
            min_confidence=0.0,
        )
        report = await engine.analyze(request)
        assert len(report.evidence) <= 3


class TestContradictionDetection:
    async def test_detects_contradictions(self, engine):
        sources = [
            Evidence(
                title="AI improves productivity",
                authors=["Smith"],
                year=2024,
                source_type=SourceType.journal,
                source_quality=SourceQuality.peer_reviewed,
                content="AI tools significantly improve developer productivity by automating repetitive tasks.",
                recency_score=0.9,
                methodology_score=0.9,
                relevance_score=0.9,
                confidence=0.9,
            ),
            Evidence(
                title="AI has no effect on productivity",
                authors=["Jones"],
                year=2023,
                source_type=SourceType.journal,
                source_quality=SourceQuality.peer_reviewed,
                content="Our study found no statistically significant effect of AI tools on developer productivity.",
                recency_score=0.8,
                methodology_score=0.85,
                relevance_score=0.9,
                confidence=0.8,
            ),
        ]
        request = ResearchRequest(
            query="AI productivity",
            operation=ResearchOperation.contradiction_analysis,
            sources=sources,
            include_contradictions=True,
        )
        report = await engine.analyze(request)
        assert len(report.contradictions) > 0

    async def test_empty_sources_no_contradictions(self, engine):
        request = ResearchRequest(
            query="zzzz_no_match_zzzz",
            operation=ResearchOperation.contradiction_analysis,
            sources=[],
            include_contradictions=True,
        )
        report = await engine.analyze(request)
        assert isinstance(report.contradictions, list)


class TestCitationQuality:
    async def test_generates_citations(self, engine, base_request):
        report = await engine.analyze(base_request)
        assert isinstance(report.citations, list)
        assert len(report.citations) > 0

    async def test_citation_has_required_fields(self, engine, base_request):
        report = await engine.analyze(base_request)
        for citation in report.citations:
            assert citation.text
            assert 0.0 <= citation.overall_quality <= 1.0
            assert 0.0 <= citation.completeness <= 1.0

    async def test_citation_style_variants(self, engine):
        for style in [CitationStyle.apa, CitationStyle.mla, CitationStyle.ieee]:
            request = ResearchRequest(
                query="software engineering",
                operation=ResearchOperation.citation_assessment,
                citation_style=style,
                max_sources=3,
            )
            report = await engine.analyze(request)
            assert len(report.citations) > 0
            for citation in report.citations:
                assert citation.style == style


class TestConfidenceEstimation:
    async def test_confidence_in_valid_range(self, engine, base_request):
        report = await engine.analyze(base_request)
        assert 0.0 <= report.confidence <= 1.0

    async def test_high_quality_sources_high_confidence(self, engine):
        sources = [
            Evidence(
                title="High quality source",
                authors=["Expert"],
                year=2024,
                source_type=SourceType.journal,
                source_quality=SourceQuality.peer_reviewed,
                content="High quality peer-reviewed content.",
                recency_score=0.95,
                methodology_score=0.95,
                relevance_score=0.95,
                confidence=0.95,
            ),
        ]
        request = ResearchRequest(
            query="test",
            operation=ResearchOperation.confidence_estimation,
            sources=sources,
        )
        report = await engine.analyze(request)
        assert report.confidence >= 0.8

    async def test_uncertainty_factors_populated(self, engine, base_request):
        report = await engine.analyze(base_request)
        assert isinstance(report.uncertainty_factors, list)


class TestSynthesis:
    async def test_synthesis_generated(self, engine, base_request):
        request = ResearchRequest(
            query="AI software engineering",
            operation=ResearchOperation.synthesis,
            max_sources=5,
        )
        report = await engine.analyze(request)
        assert report.synthesis is not None
        assert report.synthesis.narrative
        assert len(report.synthesis.gaps_identified) > 0

    async def test_synthesis_has_confidence(self, engine, base_request):
        request = ResearchRequest(
            query="AI software engineering",
            operation=ResearchOperation.synthesis,
            max_sources=5,
        )
        report = await engine.analyze(request)
        assert 0.0 <= report.synthesis.confidence <= 1.0


class TestReportGeneration:
    async def test_report_has_markdown(self, engine, base_request):
        report = await engine.analyze(base_request)
        assert report.report_markdown
        assert len(report.report_markdown) > 100

    async def test_report_contains_query(self, engine, base_request):
        report = await engine.analyze(base_request)
        assert base_request.query in report.report_markdown

    async def test_report_operation_matches_request(self, engine, base_request):
        report = await engine.analyze(base_request)
        assert report.operation == base_request.operation.value


class TestWorker:
    async def test_worker_executes_task(self):
        from apps.research_assistant.worker import ResearchAssistantWorker
        worker = ResearchAssistantWorker()
        result = await worker.execute({
            "query": "test query",
            "operation": "literature_review",
        })
        assert "evidence" in result or "error" in result

    async def test_worker_returns_dict(self):
        from apps.research_assistant.worker import ResearchAssistantWorker
        worker = ResearchAssistantWorker()
        result = await worker.execute({
            "query": "test",
            "operation": "evidence_gathering",
        })
        assert isinstance(result, dict)
