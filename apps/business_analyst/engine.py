"""
Business Analyst — Domain Engine orchestrator.

Orchestrates the full business analysis pipeline:
    1. Requirement Gathering (structure, validate, score)
    2. Business Process Modeling (BPMN-like workflows)
    3. User Story Generation (INVEST-compliant stories)
    4. Use Case Modeling (actors, scenarios, exceptions)
    5. BRD Generation (Business Requirement Documents)
    6. Functional Specification (executable specs)
    7. Gap Analysis (business needs vs. capabilities)
    8. ROI Analysis (NPV, payback period)
    9. Process Optimization (inefficiency detection)

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
import time
from typing import Any

from apps.business_analyst.schemas import (
    BusinessAnalysisRequest,
    BusinessAnalysisReport,
    BusinessAnalysisRecord,
    Requirement,
    UserStory,
    UseCase,
    ProcessModel,
    GapItem,
    ROIResult,
    ProcessOptimization,
    OperationType,
    Priority,
    RequirementType,
    StoryPoint,
)
from apps.business_analyst.requirement_gatherer import RequirementGatherer
from apps.business_analyst.process_modeler import ProcessModeler
from apps.business_analyst.story_generator import StoryGenerator
from apps.business_analyst.use_case_modeler import UseCaseModeler
from apps.business_analyst.brd_generator import BRDGenerator
from apps.business_analyst.spec_generator import SpecGenerator
from apps.business_analyst.gap_analyzer import GapAnalyzer
from apps.business_analyst.roi_calculator import ROICalculator
from apps.business_analyst.optimizer import ProcessOptimizer

logger = logging.getLogger(__name__)


class BusinessAnalystEngine:
    """
    Orchestrates the full business analysis pipeline.

    Public API::

        engine = BusinessAnalystEngine()
        report = engine.analyze(request)
    """

    def __init__(self) -> None:
        self.req_gatherer = RequirementGatherer()
        self.process_modeler = ProcessModeler()
        self.story_gen = StoryGenerator()
        self.use_case_modeler = UseCaseModeler()
        self.brd_gen = BRDGenerator()
        self.spec_gen = SpecGenerator()
        self.gap_analyzer = GapAnalyzer()
        self.roi_calc = ROICalculator()
        self.optimizer = ProcessOptimizer()

    def analyze(self, request: BusinessAnalysisRequest) -> BusinessAnalysisReport:
        """
        Run the business analysis pipeline based on operation.

        Args:
            request: BusinessAnalysisRequest with context, inputs, options.

        Returns:
            BusinessAnalysisReport with requirements, stories, use cases, etc.
        """
        started = time.monotonic()
        op = request.operation.value if hasattr(request.operation, 'value') else str(request.operation)

        requirements: list[Requirement] = []
        user_stories: list[UserStory] = []
        use_cases: list[UseCase] = []
        process_model: ProcessModel | None = None
        gaps: list[GapItem] = []
        roi_result: ROIResult | None = None
        optimizations: list[ProcessOptimization] = []

        if op == "requirement_gathering":
            requirements = self.req_gatherer.gather(request.inputs, request.business_context)
            user_stories = self.story_gen.generate_from_requirements(requirements, request.personas)

        elif op == "process_modeling":
            process_model = self.process_modeler.model(request.inputs.current_state_documentation)

        elif op == "user_story":
            requirements = self.req_gatherer.gather(request.inputs, request.business_context)
            user_stories = self.story_gen.generate_from_requirements(requirements, request.personas)

        elif op == "use_case":
            requirements = self.req_gatherer.gather(request.inputs, request.business_context)
            use_cases = self.use_case_modeler.model(requirements, request.personas)

        elif op == "brd_generation":
            requirements = self.req_gatherer.gather(request.inputs, request.business_context)
            user_stories = self.story_gen.generate_from_requirements(requirements, request.personas)

        elif op == "functional_spec":
            requirements = self.req_gatherer.gather(request.inputs, request.business_context)
            user_stories = self.story_gen.generate_from_requirements(requirements, request.personas)

        elif op == "gap_analysis":
            gaps = self.gap_analyzer.analyze(request.inputs, request.inputs.technical_constraints)

        elif op == "roi_analysis":
            roi_result = self.roi_calc.calculate(request.inputs, request.business_context)

        elif op == "process_optimization":
            process_model = self.process_modeler.model(request.inputs.current_state_documentation)
            optimizations = self.optimizer.optimize(process_model)

        # Compute quality score.
        quality_score = self._compute_quality_score(requirements, user_stories, gaps, roi_result)

        explanation = self._build_explanation(op, requirements, user_stories, gaps, roi_result)

        report = BusinessAnalysisReport(
            request_id=request.request_id,
            operation=op,
            requirements=requirements,
            user_stories=user_stories,
            use_cases=use_cases,
            process_model=process_model,
            gaps=gaps,
            roi_result=roi_result,
            optimizations=optimizations,
            quality_score=quality_score,
            explanation=explanation,
            raw={
                "latency_ms": round((time.monotonic() - started) * 1000.0, 2),
                "requirements_count": len(requirements),
                "user_stories_count": len(user_stories),
                "gaps_identified": len(gaps),
                "roi_analyzed": roi_result is not None,
            },
        )

        # Record to Experience Memory.
        record = BusinessAnalysisRecord(
            request_id=request.request_id,
            operation=op,
            domain=request.business_context.domain,
            requirements_count=len(requirements),
            user_stories_count=len(user_stories),
            gaps_identified=len(gaps),
            roi_analyzed=roi_result is not None,
            outcome="success" if quality_score >= 0.5 else "partial",
        )
        self._record(record)

        return report

    def _compute_quality_score(
        self,
        requirements: list[Requirement],
        user_stories: list[UserStory],
        gaps: list[GapItem],
        roi: ROIResult | None,
    ) -> float:
        """Compute overall quality score."""
        score = 0.5  # baseline

        if requirements:
            avg_clarity = sum(r.clarity_score for r in requirements) / len(requirements)
            score += avg_clarity * 0.3

        if user_stories:
            complete_stories = sum(1 for s in user_stories if s.acceptance_criteria)
            story_completeness = complete_stories / len(user_stories)
            score += story_completeness * 0.2

        if gaps:
            score += 0.1

        if roi:
            score += 0.1

        return max(0.0, min(1.0, round(score, 4)))

    def _build_explanation(
        self,
        op: str,
        requirements: list[Requirement],
        user_stories: list[UserStory],
        gaps: list[GapItem],
        roi: ROIResult | None,
    ) -> str:
        """Build human-readable explanation."""
        parts = [f"Performed {op} analysis."]
        if requirements:
            parts.append(f"Generated {len(requirements)} requirements.")
        if user_stories:
            parts.append(f"Created {len(user_stories)} user stories.")
        if gaps:
            parts.append(f"Identified {len(gaps)} capability gaps.")
        if roi:
            parts.append(f"ROI analysis: NPV ${roi.npv:,.2f}, {roi.payback_period_months} months payback.")
        return " ".join(parts)

    def _record(self, record: BusinessAnalysisRecord) -> str:
        """Record to in-memory store (Experience Memory interface)."""
        try:
            import json
            from pathlib import Path
            base = Path("artifacts/business_analysis_history")
            base.mkdir(parents=True, exist_ok=True)
            path = base / f"{record.record_id}.json"
            path.write_text(
                json.dumps(record.model_dump(), indent=2, default=str),
                encoding="utf-8",
            )
        except OSError:
            logger.warning("Failed to persist business analysis record %s", record.record_id)
        return record.record_id
