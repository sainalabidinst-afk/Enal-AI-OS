"""
Research Engine
===============

Domain engine for the Research Assistant Capability Pack.

Orchestrates:
    1. Evidence gathering with quality ranking
    2. Contradiction detection
    3. Citation quality assessment
    4. Confidence estimation with uncertainty quantification
    5. Synthesis of multi-source findings
    6. Report generation with citations

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
import math
import random
import re
from datetime import datetime, timezone
from typing import Any

from apps.research_assistant.schemas import (
    Citation,
    CitationStyle,
    ConfidenceLevel,
    Contradiction,
    ContradictionType,
    Evidence,
    Finding,
    FindingSeverity,
    ResearchOperation,
    ResearchRequest,
    ResearchReport,
    ResearchQualityRecord,
    SourceQuality,
    SourceType,
    Synthesis,
)

logger = logging.getLogger(__name__)


class EvidenceRanker:
    """Ranks evidence by source quality, recency, and methodology."""

    def rank(self, evidence_list: list[Evidence], query_terms: list[str]) -> list[Evidence]:
        scored: list[tuple[float, Evidence]] = []
        current_year = datetime.now(timezone.utc).year

        for ev in evidence_list:
            recency = ev.recency_score
            if ev.year > 0:
                age = max(0, current_year - ev.year)
                recency = max(recency, 1.0 - (age / 50.0))

            methodology = ev.methodology_score
            quality_map = {
                SourceQuality.peer_reviewed: 1.0,
                SourceQuality.expert_review: 0.85,
                SourceQuality.editorial: 0.7,
                SourceQuality.unverified: 0.4,
            }
            source_quality = quality_map.get(ev.source_quality, 0.5)

            relevance = ev.relevance_score
            if query_terms:
                title_lower = ev.title.lower()
                content_lower = ev.content.lower()
                keyword_hits = sum(1 for term in query_terms if term in title_lower or term in content_lower)
                relevance = max(relevance, min(1.0, keyword_hits / max(1, len(query_terms))))

            composite = (source_quality * 0.4) + (recency * 0.25) + (methodology * 0.2) + (relevance * 0.15)
            scored.append((composite, ev))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        ranked: list[Evidence] = []
        for composite, ev in scored:
            data = ev.model_dump()
            data["confidence"] = round(composite, 4)
            updated = Evidence(**data)
            ranked.append(updated)
        return ranked


class ContradictionDetector:
    """Detects conflicting claims between evidence items."""

    def detect(self, evidence_list: list[Evidence]) -> list[Contradiction]:
        contradictions: list[Contradiction] = []
        seen: set[tuple[str, str]] = set()

        for i, a in enumerate(evidence_list):
            for b in evidence_list[i + 1:]:
                pair = (a.id, b.id)
                if pair in seen:
                    continue
                seen.add(pair)

                if self._are_contradictory(a, b):
                    contradictions.append(Contradiction(
                        type=self._classify_contradiction(a, b),
                        evidence_a=a.id,
                        evidence_b=b.id,
                        description=self._describe_contradiction(a, b),
                        severity=FindingSeverity.high,
                        confidence=0.8,
                        resolution_suggestion="Further investigation needed; compare methodologies and sample sizes.",
                    ))

        return contradictions

    def _are_contradictory(self, a: Evidence, b: Evidence) -> bool:
        a_text = a.content.lower()
        b_text = b.content.lower()

        opposition_patterns = [
            (r"\b(improve|increase|enhance|boost|positive)\b", r"\b(no\s+\w+.*effect|decrease|reduce|negative|ineffective|no\s+significant)\b"),
            (r"\b(significant|strong|effective)\b", r"\b(no\s+significant|weak|ineffective|no\s+effect)\b"),
        ]
        for positive_pattern, negative_pattern in opposition_patterns:
            a_has_positive = bool(re.search(positive_pattern, a_text))
            a_has_negative = bool(re.search(negative_pattern, a_text))
            b_has_positive = bool(re.search(positive_pattern, b_text))
            b_has_negative = bool(re.search(negative_pattern, b_text))
            if (a_has_positive and b_has_negative) or (a_has_negative and b_has_positive):
                return True
        return False

    def _classify_contradiction(self, a: Evidence, b: Evidence) -> ContradictionType:
        types = list(ContradictionType)
        return random.choice(types)

    def _describe_contradiction(self, a: Evidence, b: Evidence) -> str:
        return (
            f"Conflicting claims between '{a.title}' and '{b.title}'. "
            f"Further investigation is needed to reconcile differences in methodology, sample, or interpretation."
        )


class CitationQualityAssessor:
    """Assesses citation completeness, format accuracy, and provenance."""

    def assess(self, evidence_list: list[Evidence], style: CitationStyle) -> list[Citation]:
        citations: list[Citation] = []

        for ev in evidence_list:
            text = self._format_citation(ev, style)
            completeness = self._score_completeness(ev)
            format_accuracy = self._score_format(text, style)
            provenance = self._score_provenance(ev)

            overall = (completeness * 0.4) + (format_accuracy * 0.35) + (provenance * 0.25)
            issues: list[str] = []
            if completeness < 0.8:
                issues.append("Missing author or publication details")
            if format_accuracy < 0.8:
                issues.append("Citation format deviates from style guide")
            if provenance < 0.8:
                issues.append("Weak provenance traceability")

            citations.append(Citation(
                evidence_id=ev.id,
                style=style,
                text=text,
                completeness=completeness,
                format_accuracy=format_accuracy,
                provenance_traceability=provenance,
                overall_quality=overall,
                issues=issues,
            ))

        return citations

    def _format_citation(self, ev: Evidence, style: CitationStyle) -> str:
        authors = ", ".join(ev.authors) if ev.authors else "Unknown Author"
        year_str = str(ev.year) if ev.year else "n.d."
        if style == CitationStyle.apa:
            return f"{authors} ({year_str}). {ev.title}."
        if style == CitationStyle.mla:
            return f'{authors}. "{ev.title}." {year_str}.'
        if style == CitationStyle.ieee:
            return f'{authors}, "{ev.title}," {year_str}.'
        return f"{authors} ({year_str}). {ev.title}."

    def _score_completeness(self, ev: Evidence) -> float:
        score = 0.0
        if ev.authors:
            score += 0.4
        if ev.year > 0:
            score += 0.3
        if ev.url:
            score += 0.2
        if ev.source_type:
            score += 0.1
        return min(1.0, score)

    def _score_format(self, text: str, style: CitationStyle) -> float:
        if not text:
            return 0.0
        if style == CitationStyle.apa:
            return 1.0 if re.search(r"\(\d{4}\)", text) else 0.7
        if style == CitationStyle.ieee:
            return 1.0 if re.search(r'",\s*\d{4}', text) else 0.7
        return 0.85

    def _score_provenance(self, ev: Evidence) -> float:
        score = 0.0
        if ev.url:
            score += 0.5
        if ev.citation:
            score += 0.3
        if ev.metadata:
            score += 0.2
        return min(1.0, score)


class ConfidenceEstimator:
    """Estimates confidence with uncertainty quantification."""

    def estimate(self, evidence_list: list[Evidence], contradictions: list[Contradiction]) -> tuple[float, ConfidenceLevel, list[str]]:
        if not evidence_list:
            return 0.0, ConfidenceLevel.very_low, ["No evidence available"]

        evidence_conf = [ev.confidence for ev in evidence_list]
        avg_evidence_conf = sum(evidence_conf) / len(evidence_conf)

        source_quality_scores = {
            SourceQuality.peer_reviewed: 0.9,
            SourceQuality.expert_review: 0.75,
            SourceQuality.editorial: 0.6,
            SourceQuality.unverified: 0.4,
        }
        quality_scores = [source_quality_scores.get(ev.source_quality, 0.5) for ev in evidence_list]
        avg_quality = sum(quality_scores) / len(quality_scores)

        contradiction_penalty = min(0.3, len(contradictions) * 0.05)

        confidence = (avg_evidence_conf * 0.5) + (avg_quality * 0.35) + (0.15 * (1.0 - contradiction_penalty))
        confidence = max(0.0, min(1.0, confidence))

        if confidence >= 0.9:
            level = ConfidenceLevel.very_high
        elif confidence >= 0.75:
            level = ConfidenceLevel.high
        elif confidence >= 0.6:
            level = ConfidenceLevel.moderate
        elif confidence >= 0.4:
            level = ConfidenceLevel.low
        else:
            level = ConfidenceLevel.very_low

        uncertainty: list[str] = []
        if contradiction_penalty > 0:
            uncertainty.append(f"{len(contradictions)} contradictions detected")
        if avg_quality < 0.7:
            uncertainty.append("Source quality varies")
        if len(evidence_list) < 5:
            uncertainty.append("Limited evidence base")
        if any(ev.recency_score < 0.3 for ev in evidence_list):
            uncertainty.append("Some sources are outdated")

        return confidence, level, uncertainty


class SynthesisEngine:
    """Synthesizes multi-source findings into coherent narrative."""

    def synthesize(self, query: str, evidence_list: list[Evidence], findings: list[Finding], contradictions: list[Contradiction]) -> Synthesis:
        narrative_parts = [
            f"## Synthesis: {query}",
            "",
            "### Overview",
            f"This synthesis integrates {len(evidence_list)} sources and {len(findings)} findings to address the research query.",
            "",
            "### Key Findings",
        ]

        for finding in findings[:5]:
            narrative_parts.append(f"- **{finding.title}**: {finding.description} (confidence: {finding.confidence:.0%})")

        if contradictions:
            narrative_parts.extend([
                "",
                "### Contradictions and Uncertainties",
                f"{len(contradictions)} contradictions were identified:",
            ])
            for c in contradictions[:3]:
                narrative_parts.append(f"- {c.description}")

        narrative_parts.extend([
            "",
            "### Research Gaps",
            "- Further validation needed for conflicting results",
            "- Additional longitudinal studies recommended",
            "",
            "### Conclusion",
            "The evidence suggests moderate-to-high confidence in the primary findings, with noted uncertainties that warrant further investigation.",
        ])

        narrative = "\n".join(narrative_parts)

        return Synthesis(
            query=query,
            narrative=narrative,
            supporting_evidence=[ev.id for ev in evidence_list[:10]],
            contradicted_evidence=[],
            confidence=0.85,
            gaps_identified=["conflicting_results", "limited_longitudinal_data"],
            future_work=["Longitudinal validation", "Cross-cultural replication"],
        )


class ResearchEngine:
    """
    Orchestrates the full research pipeline.

    Public API::

        engine = ResearchEngine()
        report = await engine.analyze(request)
    """

    def __init__(self) -> None:
        self._ranker = EvidenceRanker()
        self._contradiction_detector = ContradictionDetector()
        self._citation_assessor = CitationQualityAssessor()
        self._confidence_estimator = ConfidenceEstimator()
        self._synthesis_engine = SynthesisEngine()
        self._sources: list[Evidence] = self._build_source_knowledge()

    def _build_source_knowledge(self) -> list[Evidence]:
        """Build simulated source knowledge base."""
        sources = [
            Evidence(
                title="Artificial Intelligence in Software Engineering: A Systematic Mapping Study",
                authors=["Smith, J.", "Doe, A.", "Lee, K."],
                year=2024,
                source_type=SourceType.journal,
                source_quality=SourceQuality.peer_reviewed,
                content="AI significantly improves software development productivity through automated code generation, testing, and deployment. The study found a 35% increase in developer productivity when using AI-assisted tools.",
                url="https://doi.org/10.1000/ai-se-2024",
                recency_score=0.95,
                methodology_score=0.9,
                relevance_score=0.9,
                confidence=0.92,
                keywords=["AI", "software engineering", "productivity", "systematic review"],
            ),
            Evidence(
                title="The Impact of Large Language Models on Code Quality",
                authors=["Johnson, M.", "Williams, R."],
                year=2023,
                source_type=SourceType.conference,
                source_quality=SourceQuality.peer_reviewed,
                content="LLMs improve code generation speed but may introduce subtle bugs. Human review remains essential for critical systems. The study analyzed 10,000+ AI-generated code samples.",
                url="https://doi.org/10.1000/llm-code-2023",
                recency_score=0.85,
                methodology_score=0.88,
                relevance_score=0.95,
                confidence=0.88,
                keywords=["LLM", "code quality", "bugs", "code generation"],
            ),
            Evidence(
                title="Machine Learning for Requirements Engineering: A Comprehensive Review",
                authors=["Chen, L.", "Patel, S.", "Garcia, M."],
                year=2022,
                source_type=SourceType.journal,
                source_quality=SourceQuality.peer_reviewed,
                content="ML techniques show promise in automating requirements elicitation and validation. NLP-based approaches achieve 78% accuracy in extracting requirements from natural language.",
                url="https://doi.org/10.1000/ml-re-2022",
                recency_score=0.75,
                methodology_score=0.85,
                relevance_score=0.8,
                confidence=0.82,
                keywords=["ML", "requirements engineering", "NLP", "automation"],
            ),
            Evidence(
                title="AI-Assisted Debugging: Challenges and Opportunities",
                authors=["Brown, T.", "Davis, P."],
                year=2024,
                source_type=SourceType.preprint,
                source_quality=SourceQuality.unverified,
                content="AI debugging tools can identify 60% of common bugs but struggle with complex logic errors. Integration with IDE workflows shows the most promise.",
                url="https://arxiv.org/abs/2024.ai-debug",
                recency_score=0.9,
                methodology_score=0.7,
                relevance_score=0.88,
                confidence=0.75,
                keywords=["debugging", "AI", "IDE", "bug detection"],
            ),
            Evidence(
                title="Statistical Methods in Software Engineering Research",
                authors=["Miller, D.", "Wilson, E."],
                year=2021,
                source_type=SourceType.book,
                source_quality=SourceQuality.expert_review,
                content="Proper statistical methods are crucial for valid software engineering research. The book covers experimental design, hypothesis testing, and effect size calculation.",
                url="https://books.example.com/stat-se",
                recency_score=0.6,
                methodology_score=0.95,
                relevance_score=0.7,
                confidence=0.9,
                keywords=["statistics", "research methods", "software engineering"],
            ),
            Evidence(
                title="Neural Code Generation: A Double-Edged Sword",
                authors=["Anderson, K.", "Taylor, J."],
                year=2023,
                source_type=SourceType.journal,
                source_quality=SourceQuality.peer_reviewed,
                content="Neural code generation can reduce development time by 40% but may perpetuate biases present in training data. Careful validation is required for production use.",
                url="https://doi.org/10.1000/neural-code-2023",
                recency_score=0.85,
                methodology_score=0.87,
                relevance_score=0.92,
                confidence=0.85,
                keywords=["neural code", "bias", "productivity", "validation"],
            ),
            Evidence(
                title="Automated Testing in the Age of AI: Opportunities and Risks",
                authors=["White, S.", "Harris, M."],
                year=2024,
                source_type=SourceType.conference,
                source_quality=SourceQuality.peer_reviewed,
                content="AI-generated tests achieve 85% coverage but may miss edge cases. Human-designed tests remain superior for complex business logic validation.",
                url="https://doi.org/10.1000/ai-test-2024",
                recency_score=0.95,
                methodology_score=0.82,
                relevance_score=0.9,
                confidence=0.83,
                keywords=["testing", "AI", "automation", "coverage"],
            ),
            Evidence(
                title="The Future of Software Development: Human-AI Collaboration",
                authors=["Roberts, A.", "Clark, N."],
                year=2024,
                source_type=SourceType.report,
                source_quality=SourceQuality.editorial,
                content="The future of software development lies in effective human-AI collaboration. Developers who leverage AI tools effectively show 2x productivity improvements.",
                url="https://reports.example.com/future-se-2024",
                recency_score=0.95,
                methodology_score=0.65,
                relevance_score=0.88,
                confidence=0.7,
                keywords=["collaboration", "AI", "productivity", "future"],
            ),
            Evidence(
                title="Reproducibility in AI-Powered Software Engineering",
                authors=["Liu, H.", "Zhang, Y."],
                year=2022,
                source_type=SourceType.journal,
                source_quality=SourceQuality.peer_reviewed,
                content="Reproducibility remains a challenge in AI-powered SE research. Only 30% of studies provide sufficient detail for replication.",
                url="https://doi.org/10.1000/repro-se-2022",
                recency_score=0.7,
                methodology_score=0.9,
                relevance_score=0.75,
                confidence=0.87,
                keywords=["reproducibility", "AI", "research", "replication"],
            ),
            Evidence(
                title="Ethical Considerations in AI-Assisted Software Development",
                authors=["Green, P.", "Adams, R."],
                year=2023,
                source_type=SourceType.book,
                source_quality=SourceQuality.expert_review,
                content="AI-assisted development raises ethical concerns around code ownership, licensing, and accountability. New frameworks are needed to address these challenges.",
                url="https://books.example.com/ethics-ai-se",
                recency_score=0.8,
                methodology_score=0.88,
                relevance_score=0.78,
                confidence=0.84,
                keywords=["ethics", "AI", "licensing", "accountability"],
            ),
        ]

        for i, source in enumerate(sources):
            source.id = f"ev-{i + 1:03d}"
            source.metadata = {
                "index": i + 1,
                "database": "simulated-research-db",
                "indexed_at": datetime.now(timezone.utc).isoformat(),
            }

        return sources

    async def analyze(self, request: ResearchRequest) -> ResearchReport:
        """
        Run the research analysis pipeline.

        Args:
            request: ResearchRequest with query, operation, and preferences.

        Returns:
            ResearchReport with evidence, findings, contradictions, citations, and synthesis.
        """
        started = datetime.now(timezone.utc)
        query_terms = [term.lower() for term in re.findall(r"[a-zA-Z]{3,}", request.query)]

        if request.operation == ResearchOperation.literature_review:
            return await self._literature_review(request, query_terms, started)
        if request.operation == ResearchOperation.evidence_gathering:
            return await self._evidence_gathering(request, query_terms, started)
        if request.operation == ResearchOperation.contradiction_analysis:
            return await self._contradiction_analysis(request, query_terms, started)
        if request.operation == ResearchOperation.citation_assessment:
            return await self._citation_assessment(request, query_terms, started)
        if request.operation == ResearchOperation.confidence_estimation:
            return await self._confidence_estimation(request, query_terms, started)
        if request.operation == ResearchOperation.synthesis:
            return await self._synthesis(request, query_terms, started)
        if request.operation == ResearchOperation.report_generation:
            return await self._report_generation(request, query_terms, started)

        return await self._literature_review(request, query_terms, started)

    async def _literature_review(self, request: ResearchRequest, query_terms: list[str], started: datetime) -> ResearchReport:
        evidence = self._gather_evidence(request, query_terms)
        findings = self._generate_findings(evidence, request.query)
        contradictions = self._contradiction_detector.detect(evidence) if request.include_contradictions else []
        citations = self._citation_assessor.assess(evidence, request.citation_style) if request.include_citations else []
        confidence, level, uncertainty = self._confidence_estimator.estimate(evidence, contradictions)
        synthesis = self._synthesis_engine.synthesize(request.query, evidence, findings, contradictions)

        report = self._build_report(
            request, evidence, findings, contradictions, citations, synthesis, confidence, uncertainty, started
        )
        self._record_quality(request, evidence, findings, contradictions, citations, confidence)
        return report

    async def _evidence_gathering(self, request: ResearchRequest, query_terms: list[str], started: datetime) -> ResearchReport:
        evidence = self._gather_evidence(request, query_terms)
        findings = self._generate_findings(evidence, request.query)
        contradictions = self._contradiction_detector.detect(evidence) if request.include_contradictions else []
        confidence, level, uncertainty = self._confidence_estimator.estimate(evidence, contradictions)

        report = ResearchReport(
            request_id=request.request_id,
            query=request.query,
            operation=ResearchOperation.evidence_gathering.value,
            evidence=evidence,
            findings=findings,
            contradictions=contradictions,
            confidence=confidence,
            uncertainty_factors=uncertainty,
            report_markdown=self._generate_evidence_report(request.query, evidence, findings, contradictions, confidence, uncertainty),
            raw={"evidence_count": len(evidence), "finding_count": len(findings), "contradiction_count": len(contradictions)},
        )
        self._record_quality(request, evidence, findings, contradictions, [], confidence)
        return report

    async def _contradiction_analysis(self, request: ResearchRequest, query_terms: list[str], started: datetime) -> ResearchReport:
        evidence = self._gather_evidence(request, query_terms)
        contradictions = self._contradiction_detector.detect(evidence)
        confidence, level, uncertainty = self._confidence_estimator.estimate(evidence, contradictions)

        report = ResearchReport(
            request_id=request.request_id,
            query=request.query,
            operation=ResearchOperation.contradiction_analysis.value,
            evidence=evidence,
            contradictions=contradictions,
            confidence=confidence,
            uncertainty_factors=uncertainty,
            report_markdown=self._generate_contradiction_report(request.query, evidence, contradictions, confidence, uncertainty),
            raw={"contradiction_count": len(contradictions)},
        )
        self._record_quality(request, evidence, [], contradictions, [], confidence)
        return report

    async def _citation_assessment(self, request: ResearchRequest, query_terms: list[str], started: datetime) -> ResearchReport:
        evidence = self._gather_evidence(request, query_terms)
        citations = self._citation_assessor.assess(evidence, request.citation_style)
        avg_quality = sum(c.overall_quality for c in citations) / max(1, len(citations))

        report = ResearchReport(
            request_id=request.request_id,
            query=request.query,
            operation=ResearchOperation.citation_assessment.value,
            evidence=evidence,
            citations=citations,
            confidence=avg_quality,
            uncertainty_factors=[],
            report_markdown=self._generate_citation_report(request.query, citations, avg_quality),
            raw={"citation_count": len(citations), "average_quality": avg_quality},
        )
        self._record_quality(request, evidence, [], [], citations, avg_quality)
        return report

    async def _confidence_estimation(self, request: ResearchRequest, query_terms: list[str], started: datetime) -> ResearchReport:
        evidence = self._gather_evidence(request, query_terms)
        findings = self._generate_findings(evidence, request.query)
        contradictions = self._contradiction_detector.detect(evidence) if request.include_contradictions else []
        confidence, level, uncertainty = self._confidence_estimator.estimate(evidence, contradictions)

        report = ResearchReport(
            request_id=request.request_id,
            query=request.query,
            operation=ResearchOperation.confidence_estimation.value,
            evidence=evidence,
            findings=findings,
            contradictions=contradictions,
            confidence=confidence,
            uncertainty_factors=uncertainty,
            report_markdown=self._generate_confidence_report(request.query, confidence, level, uncertainty, evidence, findings),
            raw={"confidence": confidence, "level": level.value, "uncertainty_count": len(uncertainty)},
        )
        self._record_quality(request, evidence, findings, contradictions, [], confidence)
        return report

    async def _synthesis(self, request: ResearchRequest, query_terms: list[str], started: datetime) -> ResearchReport:
        evidence = self._gather_evidence(request, query_terms)
        findings = self._generate_findings(evidence, request.query)
        contradictions = self._contradiction_detector.detect(evidence) if request.include_contradictions else []
        confidence, level, uncertainty = self._confidence_estimator.estimate(evidence, contradictions)
        synthesis = self._synthesis_engine.synthesize(request.query, evidence, findings, contradictions)

        report = ResearchReport(
            request_id=request.request_id,
            query=request.query,
            operation=ResearchOperation.synthesis.value,
            evidence=evidence,
            findings=findings,
            contradictions=contradictions,
            synthesis=synthesis,
            confidence=confidence,
            uncertainty_factors=uncertainty,
            report_markdown=synthesis.narrative,
            raw={"synthesis_id": synthesis.id},
        )
        self._record_quality(request, evidence, findings, contradictions, [], confidence)
        return report

    async def _report_generation(self, request: ResearchRequest, query_terms: list[str], started: datetime) -> ResearchReport:
        return await self._literature_review(request, query_terms, started)

    def _gather_evidence(self, request: ResearchRequest, query_terms: list[str]) -> list[Evidence]:
        pool = request.sources if request.sources else self._sources
        ranked = self._ranker.rank(pool, query_terms)
        max_sources = min(request.max_sources, len(ranked))
        min_conf = request.min_confidence
        filtered = [ev for ev in ranked[:max_sources] if ev.confidence >= min_conf]
        return filtered or ranked[:max(1, max_sources)]

    def _generate_findings(self, evidence_list: list[Evidence], query: str) -> list[Finding]:
        findings: list[Finding] = []
        if not evidence_list:
            return findings

        primary = evidence_list[0]
        findings.append(Finding(
            title=f"Primary Finding: {query}",
            description=primary.content[:280],
            evidence_ids=[primary.id],
            confidence=primary.confidence,
            severity=FindingSeverity.high,
            category="primary",
        ))

        if len(evidence_list) > 1:
            secondary = evidence_list[1]
            findings.append(Finding(
                title="Supporting Evidence",
                description=secondary.content[:220],
                evidence_ids=[secondary.id],
                confidence=secondary.confidence * 0.95,
                severity=FindingSeverity.medium,
                category="supporting",
            ))

        return findings

    def _build_report(
        self,
        request: ResearchRequest,
        evidence: list[Evidence],
        findings: list[Finding],
        contradictions: list[Contradiction],
        citations: list[Citation],
        synthesis: Synthesis | None,
        confidence: float,
        uncertainty: list[str],
        started: datetime,
    ) -> ResearchReport:
        latency_ms = (datetime.now(timezone.utc) - started).total_seconds() * 1000.0

        return ResearchReport(
            request_id=request.request_id,
            query=request.query,
            operation=request.operation.value,
            evidence=evidence,
            findings=findings,
            contradictions=contradictions,
            citations=citations,
            synthesis=synthesis,
            confidence=confidence,
            uncertainty_factors=uncertainty,
            report_markdown=self._generate_full_report(
                request.query, evidence, findings, contradictions, citations, synthesis, confidence, uncertainty
            ),
            raw={
                "latency_ms": round(latency_ms, 2),
                "evidence_count": len(evidence),
                "finding_count": len(findings),
                "contradiction_count": len(contradictions),
                "citation_count": len(citations),
                "confidence": confidence,
                "uncertainty_count": len(uncertainty),
            },
        )

    def _generate_full_report(
        self,
        query: str,
        evidence: list[Evidence],
        findings: list[Finding],
        contradictions: list[Contradiction],
        citations: list[Citation],
        synthesis: Synthesis | None,
        confidence: float,
        uncertainty: list[str],
    ) -> str:
        lines = [f"# Research Report: {query}", ""]

        if synthesis:
            lines.append(synthesis.narrative)
        else:
            lines.extend([
                "## Evidence",
                f"Retrieved {len(evidence)} sources.",
            ])
            for ev in evidence[:5]:
                lines.append(f"- **{ev.title}** ({ev.year}) — confidence: {ev.confidence:.0%}")

        if findings:
            lines.extend(["", "## Findings"])
            for finding in findings:
                lines.append(f"- **{finding.title}**: {finding.description}")

        if contradictions:
            lines.extend(["", "## Contradictions", f"Detected {len(contradictions)} contradictions."])
            for c in contradictions[:5]:
                lines.append(f"- {c.description}")

        if citations:
            lines.extend(["", "## Citations"])
            for citation in citations[:10]:
                lines.append(f"- {citation.text}")

        lines.extend([
            "",
            "## Confidence Assessment",
            f"- Overall confidence: {confidence:.0%}",
            f"- Uncertainty factors: {', '.join(uncertainty) if uncertainty else 'None identified'}",
        ])

        return "\n".join(lines)

    def _generate_evidence_report(self, query: str, evidence: list[Evidence], findings: list[Finding], contradictions: list[Contradiction], confidence: float, uncertainty: list[str]) -> str:
        return self._generate_full_report(query, evidence, findings, contradictions, [], None, confidence, uncertainty)

    def _generate_contradiction_report(self, query: str, evidence: list[Evidence], contradictions: list[Contradiction], confidence: float, uncertainty: list[str]) -> str:
        lines = [f"# Contradiction Analysis: {query}", "", f"## Summary", f"Analyzed {len(evidence)} sources and detected {len(contradictions)} contradictions.", ""]
        if contradictions:
            lines.extend(["## Contradictions"])
            for c in contradictions:
                lines.append(f"- **{c.type.value}**: {c.description} (severity: {c.severity.value})")
        lines.extend(["", f"## Confidence: {confidence:.0%}"])
        return "\n".join(lines)

    def _generate_citation_report(self, query: str, citations: list[Citation], avg_quality: float) -> str:
        lines = [f"# Citation Assessment: {query}", "", f"## Summary", f"Assessed {len(citations)} citations with average quality {avg_quality:.0%}.", ""]
        if citations:
            lines.extend(["## Citations"])
            for c in citations:
                lines.append(f"- {c.text}")
                if c.issues:
                    lines.append(f"  - Issues: {', '.join(c.issues)}")
        return "\n".join(lines)

    def _generate_confidence_report(self, query: str, confidence: float, level: ConfidenceLevel, uncertainty: list[str], evidence: list[Evidence], findings: list[Finding]) -> str:
        lines = [
            f"# Confidence Estimation: {query}",
            "",
            "## Summary",
            f"- Confidence: {confidence:.0%} ({level.value})",
            f"- Evidence count: {len(evidence)}",
            f"- Findings count: {len(findings)}",
            "",
            "## Uncertainty Factors",
        ]
        if uncertainty:
            for factor in uncertainty:
                lines.append(f"- {factor}")
        else:
            lines.append("- None identified")
        return "\n".join(lines)

    def _record_quality(
        self,
        request: ResearchRequest,
        evidence: list[Evidence],
        findings: list[Finding],
        contradictions: list[Contradiction],
        citations: list[Citation],
        confidence: float,
    ) -> None:
        avg_quality = sum(ev.confidence for ev in evidence) / max(1, len(evidence))
        citation_accuracy = sum(c.overall_quality for c in citations) / max(1, len(citations))

        record = ResearchQualityRecord(
            request_id=request.request_id,
            operation=request.operation.value,
            evidence_count=len(evidence),
            finding_count=len(findings),
            contradiction_count=len(contradictions),
            citation_accuracy=citation_accuracy,
            evidence_quality_score=avg_quality,
            confidence_score=confidence,
            completeness=min(1.0, (len(evidence) / max(1, request.max_sources))),
        )
        logger.debug("Research quality recorded: %s", record.id)


research_engine = ResearchEngine()
