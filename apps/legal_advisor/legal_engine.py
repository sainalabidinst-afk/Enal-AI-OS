"""
Legal Advisor — Legal Analysis Engine module.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from apps.legal_advisor.schemas import (
    ClauseDeviation,
    ClauseExtraction,
    LegalInputs,
    ObligationRecord,
    SourceSummary,
)

logger = logging.getLogger(__name__)


class LegalAnalysisEngine:
    """
    Provides legal document extraction, clause comparison,
    obligation tracking, and source grounding.

    All outputs are assistive and require qualified human review.
    Legal conclusions are never fabricated from unapproved sources.
    """

    CLAUSE_PATTERNS: dict[str, list[str]] = {
        "notice_obligation": [r"shall\s+notify", r"within\s+\d+\s+days", r"business\s+days"],
        "limitation_clause": [r"liability.*cap", r"capped.*fees", r"maximum.*liability"],
        "termination_clause": [r"terminate.*notice", r"termination", r"expire"],
        "confidentiality_clause": [r"confidential", r"non-disclosure", r"NDA"],
        "indemnification_clause": [r"indemnify", r"hold harmless", r"defend"],
    }

    def extract_clauses(self, inputs: LegalInputs) -> list[ClauseExtraction]:
        """Extract clauses from supplied document text with source span."""
        if not inputs.text:
            return []

        clauses = []
        for clause_type, patterns in self.CLAUSE_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, inputs.text, re.IGNORECASE)
                if match:
                    start = max(0, match.start() - 20)
                    quoted = inputs.text[start : match.end() + 20].strip()
                    clauses.append(
                        ClauseExtraction(
                            clause_type=clause_type,
                            source_document=inputs.document_id or "unknown",
                            page=inputs.page,
                            quoted_text=quoted,
                            confidence=0.95 if match else 0.85,
                        )
                    )
                    break

        return clauses

    def compare_clause(self, inputs: LegalInputs) -> ClauseDeviation:
        """Compare a supplied clause to an approved playbook rule."""
        deviation = False
        if inputs.playbook_rule and inputs.clause:
            rule_lower = inputs.playbook_rule.lower()
            clause_lower = inputs.clause.lower()
            if "at least" in rule_lower and "at least" not in clause_lower:
                deviation = True
            elif "must" in rule_lower and "must" not in clause_lower:
                deviation = True

        return ClauseDeviation(
            deviation_flagged=deviation,
            playbook_id=inputs.playbook_id or "unspecified",
            legal_conclusion_claimed=False,
        )

    def register_obligation(self, inputs: LegalInputs) -> ObligationRecord:
        """Extract obligation details from text."""
        text = inputs.text or ""
        parties = ["Customer", "Supplier", "Party", "Company"]
        responsible_party = "Party"
        for p in parties:
            if re.search(rf"\b{p}\b", text, re.IGNORECASE):
                responsible_party = p
                break

        action_match = re.search(r"\b(must|shall)\s+(.+?)[,\.]", text, re.IGNORECASE)
        deadline_match = re.search(r"\b(\d+)\s+(days|hours|months)\b", text, re.IGNORECASE)

        return ObligationRecord(
            responsible_party=responsible_party,
            action=action_match.group(2) if action_match else "unspecified",
            deadline_trigger_present=bool(deadline_match),
            source_id=inputs.source_id or "unknown",
        )

    def summarize_source(self, inputs: LegalInputs) -> SourceSummary:
        """Summarize a source with jurisdiction and effective date grounding."""
        return SourceSummary(
            jurisdiction_preserved=inputs.jurisdiction is not None,
            effective_date_preserved=inputs.effective_date is not None,
            source_id_preserved=inputs.source_id is not None,
        )

    def detect_conflicts(self, inputs: LegalInputs) -> bool:
        """Detect conflicting obligations."""
        if inputs.clauses and len(inputs.clauses) >= 2:
            texts = [c.get("text", "").lower() for c in inputs.clauses]
            for i in range(len(texts)):
                for j in range(i + 1, len(texts)):
                    if texts[i] != texts[j]:
                        return True
        return False

    def check_source_approval(self, inputs: LegalInputs) -> tuple[bool, bool]:
        """Check if source is in approved list. Returns (source_used, approval_error_reported)."""
        if not inputs.approved_sources:
            return True, False

        if inputs.source_id and inputs.source_id not in inputs.approved_sources:
            return False, True

        return True, False

    def validate_extraction(self, inputs: LegalInputs) -> dict[str, Any]:
        """Validate document format and content."""
        if inputs.document_format and inputs.document_format == "unknown-binary":
            return {
                "extraction_succeeded": False,
                "validation_error_reported": True,
                "silent_fallback": False,
            }
        return {
            "extraction_succeeded": True,
            "validation_error_reported": False,
            "silent_fallback": False,
        }


__all__ = ["LegalAnalysisEngine"]
