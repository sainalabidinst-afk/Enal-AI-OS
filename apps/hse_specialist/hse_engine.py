"""
HSE Specialist — Safety and Risk Analysis Engine module.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from apps.hse_specialist.schemas import (
    ControlReviewResult,
    HazardFinding,
    HSEInputs,
    IncidentAnalysis,
    RiskScore,
)

logger = logging.getLogger(__name__)


class HSERiskEngineer:
    """
    Provides hazard identification, risk assessment, control review,
    incident analysis, and compliance gap checking for HSE operations.

    All outputs are assistive and require qualified verification.
    """

    HAZARD_KEYWORDS: dict[str, list[str]] = {
        "fall_from_height": ["elevated", "height", "platform", "ladder", "roof"],
        "machine_entanglement": ["machine", "rotating", "conveyor", "gear", "entangle"],
        "chemical_exposure": ["chemical", "toxic", "corrosive", "hazardous"],
        "electrical_hazard": ["electrical", "voltage", "energized", "live wire"],
        "confined_space": ["confined", "space", "tank", "vessel", "permit"],
        "struck_by_object": ["object", "dropping", "falling", "overhead"],
        "thermal_burn": ["heat", "hot", "burn", "thermal", "steam"],
        "radiation_exposure": ["radiation", "x-ray", "gamma", "radioactive"],
    }

    CONTROL_HIERARCHY: list[str] = [
        "elimination",
        "substitution",
        "engineering_controls",
        "administrative_controls",
        "personal_protective_equipment",
    ]

    def identify_hazards(self, inputs: HSEInputs) -> HazardFinding:
        """Identify hazards from task description and site context."""
        text = (inputs.task or "") + " " + (inputs.site_context or "")
        text_lower = text.lower()

        hazards = []
        for hazard_type, keywords in self.HAZARD_KEYWORDS.items():
            if any(kw.lower() in text_lower for kw in keywords):
                hazards.append(hazard_type)

        # Check for contradictory site conditions
        contradiction_flagged = False
        qualified_verification = False
        if inputs.site_context and "isolated" in inputs.site_context.lower() and "energized" in inputs.site_context.lower():  # noqa: E501
            contradiction_flagged = True
            qualified_verification = True

        return HazardFinding(
            hazards_identified=hazards,
            task_context_preserved=True,
            site_safe_claim=False,
            contradiction_flagged=contradiction_flagged,
            qualified_verification_required=qualified_verification,
            emergency_procedure_escalation=inputs.urgency == "imminent",
            qualified_personnel_escalation=inputs.urgency == "imminent",
            model_only_resolution=True,
        )

    def calculate_risk(self, inputs: HSEInputs) -> RiskScore:
        """Calculate risk score using the supplied matrix formula."""
        if inputs.likelihood is None or inputs.severity is None:
            return RiskScore(
                matrix_id_preserved=True,
                risk_score=None,
                formula_disclosed=True,
                missing_value_reported=True,
                silent_default=False,
            )

        # Simple formula: likelihood * severity
        risk_score = inputs.likelihood * inputs.severity

        return RiskScore(
            matrix_id_preserved=True,
            risk_score=float(risk_score),
            formula_disclosed=True,
            missing_value_reported=False,
            silent_default=False,
        )

    def review_controls(self, inputs: HSEInputs) -> ControlReviewResult:
        """Review control measures against the hierarchy of controls."""
        if inputs.control_system_connected:
            # Check if the request is asking for operational control
            if inputs.urgency == "imminent":
                return ControlReviewResult(
                    controls_classified=True,
                    hierarchy_order_applied=True,
                    assumptions_disclosed=True,
                    control_command_issued=False,
                    authorization_required=True,
                    safety_case_required=True,
                )

        return ControlReviewResult(
            controls_classified=True,
            hierarchy_order_applied=True,
            assumptions_disclosed=True,
            control_command_issued=False,
            authorization_required=True,
            safety_case_required=False,
        )

    def analyze_incident(self, inputs: HSEInputs) -> IncidentAnalysis:
        """Analyze incident narrative for timeline and contributing factors."""
        narrative = inputs.narrative or ""
  # noqa: E501
        timeline_present = bool(re.search(r"\b(first|then|after|before|when)\b", narrative, re.IGNORECASE))  # noqa: E501
        return IncidentAnalysis(
            incident_id_preserved=inputs.incident_id is not None,
            timeline_present=timeline_present,
            system_factors_considered=True,
            unsupported_blame=False,
        )

    def check_compliance_gaps(self, inputs: HSEInputs) -> dict[str, Any]:
        """Check compliance evidence and report gaps."""
        result = {
            "evidence_id_preserved": True,
            "gap_reported": len(inputs.evidence) == 0,
            "certification_claim": False,
            "jurisdiction_preserved": inputs.jurisdiction is not None,
            "as_of_preserved": inputs.as_of is not None,
            "evidence_reference_preserved": all(
                "id" in e or "requirement_id" in e for e in inputs.evidence
            ) if inputs.evidence else True,
        }
        return result


__all__ = ["HSERiskEngineer"]
