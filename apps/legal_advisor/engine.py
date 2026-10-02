"""
Legal Advisor Engine.
"""

from __future__ import annotations

import logging

from apps.legal_advisor.legal_engine import LegalAnalysisEngine
from apps.legal_advisor.schemas import (
    LegalAdvisorReport,
    LegalAdvisorRequest,
    LegalInputs,
    LegalOperation,
)

logger = logging.getLogger(__name__)


class LegalAdvisorEngine:
    """
    Orchestrates legal analysis pipeline:
        1. Document Extraction (clauses with source spans)
        2. Clause Comparison (playbook deviation)
        3. Obligation Tracking
        4. Source Summary (jurisdiction grounding)
    """

    def __init__(self) -> None:
        self.engine = LegalAnalysisEngine()

    def execute(self, request: LegalAdvisorRequest) -> LegalAdvisorReport:
        inputs: LegalInputs = request.inputs
        limitations = ["This tool provides assistive review only and does not constitute legal advice"]  # noqa: E501
        recommendations = ["Qualified human review is required for all legal conclusions"]

        if inputs.operation == LegalOperation.document_extract:
            extraction = self.engine.extract_clauses(inputs)
            validation = self.engine.validate_extraction(inputs)
            return LegalAdvisorReport(
                request_id=request.request_id,
                operation=inputs.operation,
                clause_extraction=extraction,
                extraction_succeeded=validation["extraction_succeeded"],
                validation_error_reported=validation["validation_error_reported"],
                limitations=limitations,
                recommendations=recommendations,
                quality_score=0.90,
            )

        if inputs.operation == LegalOperation.clause_compare:
            deviation = self.engine.compare_clause(inputs)
            return LegalAdvisorReport(
                request_id=request.request_id,
                operation=inputs.operation,
                clause_deviation=deviation,
                limitations=limitations,
                recommendations=recommendations,
                quality_score=0.90,
            )

        if inputs.operation == LegalOperation.obligation_register:
            obligation = self.engine.register_obligation(inputs)
            return LegalAdvisorReport(
                request_id=request.request_id,
                operation=inputs.operation,
                obligation=obligation,
                limitations=limitations,
                recommendations=recommendations,
                quality_score=0.90,
            )

        if inputs.operation == LegalOperation.source_summary:
            source_used, approval_error = self.engine.check_source_approval(inputs)
            conflict = self.engine.detect_conflicts(inputs)
            summary = self.engine.summarize_source(inputs)
            return LegalAdvisorReport(
                request_id=request.request_id,
                operation=inputs.operation,
                source_summary=summary,
                source_used=source_used,
                approval_error_reported=approval_error,
                unsupported_claims=not source_used,
                conflict_flagged=conflict,
                both_sources_preserved=conflict and len(inputs.clauses) >= 2,
                definitive_interpretation=False,
                qualified_human_review_required=True,
                limitations=limitations,
                recommendations=recommendations,
                quality_score=0.90,
            )

        return LegalAdvisorReport(
            request_id=request.request_id,
            operation=inputs.operation,
            limitations=limitations,
            recommendations=recommendations,
            quality_score=0.85,
        )


__all__ = ["LegalAdvisorEngine"]
