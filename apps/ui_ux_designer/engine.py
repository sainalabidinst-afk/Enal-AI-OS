"""
UI/UX Designer — Domain Engine orchestrator.

Orchestrates the full UI/UX design pipeline:
    1. UX Research (personas, journeys, pain points, opportunities)
    2. Design System (tokens, palette, typography, components)
    3. Prototyping (screens, flows, interactions, responsive)
    4. Accessibility Audit (WCAG 2.1 AA compliance)

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
import time
from typing import Any

from apps.ui_ux_designer.schemas import (
    UIUXDesignerRequest,
    UIUXDesignerReport,
    UXDesignRecord,
    UXResearchResult,
    DesignSystem,
    Prototype,
    AccessibilityReport,
    OperationType,
)
from apps.ui_ux_designer.ux_researcher import UXResearcher
from apps.ui_ux_designer.design_system import DesignSystemBuilder
from apps.ui_ux_designer.prototype_generator import PrototypeGenerator
from apps.ui_ux_designer.accessibility_checker import AccessibilityChecker

logger = logging.getLogger(__name__)


class UIUXDesignerEngine:
    """
    Orchestrates the full UI/UX design pipeline.

    Public API::

        engine = UIUXDesignerEngine()
        report = engine.design(request)
    """

    def __init__(self) -> None:
        self.researcher = UXResearcher()
        self.design_system_builder = DesignSystemBuilder()
        self.prototype_generator = PrototypeGenerator()
        self.accessibility_checker = AccessibilityChecker()

    def design(self, request: UIUXDesignerRequest) -> UIUXDesignerReport:
        """
        Run the UI/UX design pipeline based on operation.

        Args:
            request: UIUXDesignerRequest with context, inputs, options.

        Returns:
            UIUXDesignerReport with research, design system, prototype, accessibility.
        """
        started = time.monotonic()
        op = request.operation.value if hasattr(request.operation, 'value') else str(request.operation)

        ux_research: UXResearchResult | None = None
        design_system: DesignSystem | None = None
        prototype: Prototype | None = None
        accessibility_report: AccessibilityReport | None = None

        if op in ("ux_research", "full_design"):
            ux_research = self.researcher.research(
                request.inputs,
                request.personas,
                request.business_context,
            )

        if op in ("design_system", "full_design"):
            design_system = self.design_system_builder.build(
                request.inputs,
                request.business_context,
                request.quality_attributes,
                request.target_platforms,
            )

        if op in ("prototyping", "full_design"):
            prototype = self.prototype_generator.generate(
                request.business_context,
                ux_research or UXResearchResult(),
                design_system,
                request.target_platforms,
                fidelity="medium",
            )

        if op in ("accessibility_audit", "full_design"):
            accessibility_report = self.accessibility_checker.audit(
                design_system,
                prototype,
                request.business_context,
            )

        quality_score = self._compute_quality_score(
            ux_research, design_system, prototype, accessibility_report
        )

        explanation = self._build_explanation(
            op, ux_research, design_system, prototype, accessibility_report
        )

        report = UIUXDesignerReport(
            request_id=request.request_id,
            operation=op,
            ux_research=ux_research,
            design_system=design_system,
            prototype=prototype,
            accessibility_report=accessibility_report,
            quality_score=quality_score,
            explanation=explanation,
            raw={
                "latency_ms": round((time.monotonic() - started) * 1000.0, 2),
                "personas_generated": len(ux_research.user_personas) if ux_research else 0,
                "screens_designed": len(prototype.screens) if prototype else 0,
                "accessibility_violations": accessibility_report.violations_found if accessibility_report else 0,
                "components_designed": len(design_system.components) if design_system else 0,
            },
        )

        record = UXDesignRecord(
            request_id=request.request_id,
            operation=op,
            project_name=request.business_context.project_name,
            personas_count=len(ux_research.user_personas) if ux_research else 0,
            screens_designed=len(prototype.screens) if prototype else 0,
            accessibility_score=accessibility_report.compliance_score if accessibility_report else 0.0,
            outcome="accepted" if quality_score >= 0.7 else "revised",
        )
        self._record(record)

        return report

    def _compute_quality_score(
        self,
        ux_research: UXResearchResult | None,
        design_system: DesignSystem | None,
        prototype: Prototype | None,
        accessibility: AccessibilityReport | None,
    ) -> float:
        """Compute overall quality score."""
        score = 0.5

        if ux_research:
            score += ux_research.research_confidence * 0.2

        if design_system:
            score += 0.1
            if design_system.components:
                score += 0.1

        if prototype:
            score += 0.1

        if accessibility:
            score += accessibility.compliance_score * 0.1

        return max(0.0, min(1.0, round(score, 4)))

    def _build_explanation(
        self,
        op: str,
        ux_research: UXResearchResult | None,
        design_system: DesignSystem | None,
        prototype: Prototype | None,
        accessibility: AccessibilityReport | None,
    ) -> str:
        """Build human-readable explanation."""
        parts = [f"Performed {op} UI/UX design."]
        if ux_research:
            parts.append(
                f"UX Research: {len(ux_research.user_personas)} personas, "
                f"{len(ux_research.pain_points)} pain points, "
                f"{len(ux_research.opportunities)} opportunities."
            )
        if design_system:
            parts.append(
                f"Design System: {len(design_system.tokens)} tokens, "
                f"{len(design_system.components)} components."
            )
        if prototype:
            parts.append(
                f"Prototype: {len(prototype.screens)} screens, "
                f"{len(prototype.user_flows)} user flows."
            )
        if accessibility:
            parts.append(
                f"Accessibility: {accessibility.compliance_score:.0%} compliant, "
                f"{accessibility.violations_found} violations found."
            )
        return " ".join(parts)

    def _record(self, record: UXDesignRecord) -> str:
        """Record to in-memory store (Experience Memory interface)."""
        try:
            import json
            from pathlib import Path
            base = Path("artifacts/ux_design_history")
            base.mkdir(parents=True, exist_ok=True)
            path = base / f"{record.record_id}.json"
            path.write_text(
                json.dumps(record.model_dump(), indent=2, default=str),
                encoding="utf-8",
            )
        except OSError:
            logger.warning("Failed to persist UX design record %s", record.record_id)
        return record.record_id
