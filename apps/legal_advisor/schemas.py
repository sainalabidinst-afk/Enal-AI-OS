"""
Legal Advisor Schemas
=====================

Typed contracts for the Legal Advisor capability pack.
Defines input (LegalAdvisorRequest) and output (LegalAdvisorReport)
contracts for legal document analysis, clause comparison, and obligation tracking.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class LegalOperation(StrEnum):
    document_extract = "document_extract"
    clause_compare = "clause_compare"
    obligation_register = "obligation_register"
    source_summary = "source_summary"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=5, ge=1)


class LegalInputs(BaseModel):
    operation: LegalOperation
    document_id: str | None = None
    text: str | None = None
    page: int | None = None
    playbook_id: str | None = None
    playbook_rule: str | None = None
    clause: str | None = None
    clauses: list[dict[str, Any]] = Field(default_factory=list)
    source_id: str | None = None
    jurisdiction: str | None = None
    effective_date: str | None = None
    approved_sources: list[str] = Field(default_factory=list)
    document_format: str | None = None
    content: Any = None
    question: str | None = None


class LegalAdvisorRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "document_extract"
    business_context: BusinessContext
    inputs: LegalInputs
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class ClauseExtraction(BaseModel):
    clause_type: str
    source_document: str
    page: int | None
    quoted_text: str
    confidence: float = Field(default=1.0, ge=0, le=1)


class ClauseDeviation(BaseModel):
    deviation_flagged: bool
    playbook_id: str
    legal_conclusion_claimed: bool = False


class ObligationRecord(BaseModel):
    responsible_party: str
    action: str
    deadline_trigger_present: bool
    source_id: str


class SourceSummary(BaseModel):
    jurisdiction_preserved: bool
    effective_date_preserved: bool
    source_id_preserved: bool


class LegalAdvisorReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operation: LegalOperation
    clause_extraction: list[ClauseExtraction] = Field(default_factory=list)
    clause_deviation: ClauseDeviation | None = None
    obligation: ObligationRecord | None = None
    source_summary: SourceSummary | None = None
    conflict_flagged: bool = False
    both_sources_preserved: bool = False
    definitive_interpretation: bool = False
    legal_conclusion_provided: bool = False
    evidence_gap_reported: bool = False
    source_fabricated: bool = False
    extraction_succeeded: bool = True
    validation_error_reported: bool = False
    silent_fallback: bool = False
    source_used: bool = True
    approval_error_reported: bool = False
    unsupported_claims: bool = False
    contract_approved: bool = False
    legal_advice_claimed: bool = False
    qualified_human_review_required: bool = True
    emergency_procedure_escalation: bool = False
    qualified_personnel_escalation: bool = False
    model_only_resolution: bool = False
    control_command_issued: bool = False
    authorization_required: bool = False
    safety_case_required: bool = False
    recommendations: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    quality_score: float = Field(default=0.90, ge=0, le=1)
    model_version: str = "1.0.0"


class LegalAdvisorRecord(BaseModel):
    pack_id: str = "legal-advisor"
    version: str = "1.0.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "document_extract",
        "clause_compare",
        "obligation_register",
        "source_summary",
    ])


__all__ = [
    "BusinessContext",
    "ClauseDeviation",
    "ClauseExtraction",
    "LegalAdvisorRecord",
    "LegalAdvisorReport",
    "LegalAdvisorRequest",
    "LegalInputs",
    "LegalOperation",
    "ObligationRecord",
    "SourceSummary",
]
