"""
HSE Specialist Engine.
"""

from __future__ import annotations

import logging

from apps.hse_specialist.hse_engine import HSERiskEngineer
from apps.hse_specialist.schemas import (
    HSEInputs,
    HSEOperation,
    HSESpecialistReport,
    HSESpecialistRequest,
)

logger = logging.getLogger(__name__)


class HSESpecialistEngine:
    """
    Orchestrates HSE engineering pipeline:
        1. Hazard Analysis
        2. Risk Register (risk scoring)
        3. Control Review (hierarchy of controls)
        4. Incident Analysis (timeline + factors)
        5. Compliance Gap Check
    """

    def __init__(self) -> None:
        self.engine = HSERiskEngineer()

    def execute(self, request: HSESpecialistRequest) -> HSESpecialistReport:
        inputs: HSEInputs = request.inputs
        limitations = [
            "HSE outputs are assistive and require qualified human verification",
            "The system does not autonomously operate equipment or issue control commands",
        ]
        recommendations = [
            "Engage qualified HSE personnel for final risk decisions",
            "Verify all hazard identifications against site-specific conditions",
        ]

        if inputs.operation == HSEOperation.hazard_analysis:
            hazard_finding = self.engine.identify_hazards(inputs)
            return HSESpecialistReport(
                request_id=request.request_id,
                operation=inputs.operation,
                hazard_finding=hazard_finding,
                limitations=limitations,
                recommendations=recommendations,
                quality_score=0.92,
            )

        if inputs.operation == HSEOperation.risk_register:
            risk_score = self.engine.calculate_risk(inputs)
            return HSESpecialistReport(
                request_id=request.request_id,
                operation=inputs.operation,
                risk_score=risk_score,
                limitations=limitations,
                recommendations=recommendations,
                quality_score=0.90,
            )

        if inputs.operation == HSEOperation.control_review:
            control_result = self.engine.review_controls(inputs)
            return HSESpecialistReport(
                request_id=request.request_id,
                operation=inputs.operation,
                control_review=control_result,
                limitations=limitations,
                recommendations=recommendations,
                quality_score=0.88,
            )

        if inputs.operation == HSEOperation.incident_analysis:
            incident = self.engine.analyze_incident(inputs)
            return HSESpecialistReport(
                request_id=request.request_id,
                operation=inputs.operation,
                incident_analysis=incident,
                limitations=limitations,
                recommendations=recommendations,
                quality_score=0.93,
            )

        if inputs.operation == HSEOperation.compliance_gap_check:
            compliance = self.engine.check_compliance_gaps(inputs)
            return HSESpecialistReport(
                request_id=request.request_id,
                operation=inputs.operation,
                evidence_id_preserved=compliance["evidence_id_preserved"],
                gap_reported=compliance["gap_reported"],
                certification_claim=compliance["certification_claim"],
                jurisdiction_preserved=compliance["jurisdiction_preserved"],
                as_of_preserved=compliance["as_of_preserved"],
                evidence_reference_preserved=compliance["evidence_reference_preserved"],
                limitations=limitations,
                recommendations=recommendations,
                quality_score=0.91,
            )

        return HSESpecialistReport(
            request_id=request.request_id,
            operation=inputs.operation,
            limitations=limitations,
            recommendations=recommendations,
            quality_score=0.85,
        )


__all__ = ["HSESpecialistEngine"]
