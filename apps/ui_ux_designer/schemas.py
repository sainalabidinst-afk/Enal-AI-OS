"""
UI/UX Designer Schemas — Public Contracts (Pydantic schemas).

Defines the input (UIUXDesignerRequest) and output (UIUXDesignerReport)
contracts for the UI/UX Designer Capability Pack, plus all supporting types.

These schemas follow the RFC-0018 contract definitions exactly.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class OperationType(str, Enum):
    ux_research = "ux_research"
    design_system = "design_system"
    prototyping = "prototyping"
    accessibility_audit = "accessibility_audit"
    full_design = "full_design"


class Priority(str, Enum):
    must_have = "must_have"
    should_have = "should_have"
    could_have = "could_have"
    wont_have = "wont_have"


class OutputFormat(str, Enum):
    json = "json"
    markdown = "markdown"
    figma = "figma"
    html = "html"
    css = "css"
    json_schema = "json_schema"


class BusinessContext(BaseModel):
    domain: str = Field(default="", description="Business domain (e-commerce, fintech, etc.)")
    project_name: str = Field(default="", description="Project name")
    description: str = Field(default="", description="Project overview")


class StakeholderInput(BaseModel):
    user_research_data: list[str] = Field(default_factory=list, description="Raw UX research data")
    product_requirements: list[str] = Field(default_factory=list, description="Product requirement statements")
    current_design: str = Field(default="", description="Current design documentation")
    technical_constraints: list[str] = Field(default_factory=list)
    business_goals: list[str] = Field(default_factory=list)


class Persona(BaseModel):
    name: str = Field(default="")
    role: str = Field(default="")
    goals: list[str] = Field(default_factory=list)
    pain_points: list[str] = Field(default_factory=list)
    technical_proficiency: str = Field(default="medium", description="low|medium|high")


class QualityAttributes(BaseModel):
    accessibility_target: str = Field(default="WCAG 2.1 AA", description="WCAG level target")
    performance_target: str = Field(default="< 100ms interaction", description="UI performance target")
    consistency_target: str = Field(default="100% design system compliance", description="Design consistency target")


class UXResearchResult(BaseModel):
    user_personas: list[Persona] = Field(default_factory=list)
    user_journeys: list[dict[str, Any]] = Field(default_factory=list)
    key_findings: list[str] = Field(default_factory=list)
    pain_points: list[str] = Field(default_factory=list)
    opportunities: list[str] = Field(default_factory=list)
    usability_issues: list[str] = Field(default_factory=list)
    research_confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class DesignToken(BaseModel):
    name: str = Field(default="")
    type: str = Field(default="color", description="color|typography|spacing|shadow|border|motion")
    value: str = Field(default="", description="#hex, px, ms, etc.")
    description: str = Field(default="")
    usage: str = Field(default="")


class ComponentSpec(BaseModel):
    id: str = Field(default_factory=lambda: f"COMP-{uuid.uuid4().hex[:8]}")
    name: str = Field(default="")
    description: str = Field(default="")
    component_type: str = Field(default="button", description="button|input|card|modal|nav|form|etc")
    props_schema: dict[str, Any] = Field(default_factory=dict, description="JSON Schema for component props")
    accessibility_requirements: list[str] = Field(default_factory=list)
    variants: list[str] = Field(default_factory=list)
    responsive_behavior: str = Field(default="")


class DesignSystem(BaseModel):
    id: str = Field(default_factory=lambda: f"DS-{uuid.uuid4().hex[:8]}")
    name: str = Field(default="")
    description: str = Field(default="")
    tokens: list[DesignToken] = Field(default_factory=list)
    components: list[ComponentSpec] = Field(default_factory=list)
    color_palette: dict[str, str] = Field(default_factory=dict)
    typography_scale: dict[str, Any] = Field(default_factory=dict)
    spacing_scale: list[str] = Field(default_factory=list)
    motion_principles: list[str] = Field(default_factory=list)
    accessibility_standards: list[str] = Field(default_factory=list, description=["WCAG 2.1 AA"])
    version: str = Field(default="1.0.0")


class PrototypeScreen(BaseModel):
    id: str = Field(default_factory=lambda: f"SCR-{uuid.uuid4().hex[:8]}")
    name: str = Field(default="")
    description: str = Field(default="")
    layout: dict[str, Any] = Field(default_factory=dict, description="Layout specification")
    components: list[dict[str, Any]] = Field(default_factory=list, description="Component placements")
    interactions: list[dict[str, Any]] = Field(default_factory=list, description="Interaction definitions")
    states: list[str] = Field(default_factory=list, description="default|hover|focus|disabled|error")
    responsive_breakpoints: list[str] = Field(default_factory=list)


class Prototype(BaseModel):
    id: str = Field(default_factory=lambda: f"PROTO-{uuid.uuid4().hex[:8]}")
    name: str = Field(default="")
    description: str = Field(default="")
    fidelity: str = Field(default="medium", description="low|medium|high")
    screens: list[PrototypeScreen] = Field(default_factory=list)
    user_flows: list[dict[str, Any]] = Field(default_factory=list)
    interaction_map: dict[str, Any] = Field(default_factory=dict)
    notes: list[str] = Field(default_factory=list)
    estimated_effort: str = Field(default="")


class AccessibilityViolation(BaseModel):
    id: str = Field(default_factory=lambda: f"A11Y-{uuid.uuid4().hex[:6]}")
    wcag_criterion: str = Field(default="", description="WCAG 2.1 criterion (e.g., 1.1.1, 2.4.1)")
    severity: str = Field(default="medium", description="low|medium|high|critical")
    description: str = Field(default="")
    element_selector: str = Field(default="", description="CSS selector or component ID")
    recommendation: str = Field(default="")
    impact: str = Field(default="")


class AccessibilityReport(BaseModel):
    total_checks: int = Field(default=0)
    violations_found: int = Field(default=0)
    compliance_score: float = Field(default=0.0, ge=0.0, le=1.0)
    violations: list[AccessibilityViolation] = Field(default_factory=list)
    passed_checks: list[str] = Field(default_factory=list)
    remediation_priority: list[str] = Field(default_factory=list)
    wcag_level: str = Field(default="AA", description="Target WCAG level")


class UIUXDesignerRequest(BaseModel):
    """Input contract for a UI/UX design request."""

    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: OperationType = Field(..., description="Type of UI/UX design operation")
    business_context: BusinessContext = Field(default_factory=BusinessContext)
    inputs: StakeholderInput = Field(default_factory=StakeholderInput)
    personas: list[Persona] = Field(default_factory=list)
    quality_attributes: QualityAttributes = Field(default_factory=QualityAttributes)
    output_format: OutputFormat = Field(default=OutputFormat.json)
    target_platforms: list[str] = Field(default_factory=list, description="web|mobile|desktop|tablet")


class UIUXDesignerReport(BaseModel):
    """Output contract for a UI/UX design report."""

    request_id: str = Field(..., description="Reference to the original request")
    operation: str = Field(..., description="The operation performed")
    ux_research: UXResearchResult | None = Field(default=None)
    design_system: DesignSystem | None = Field(default=None)
    prototype: Prototype | None = Field(default=None)
    accessibility_report: AccessibilityReport | None = Field(default=None)
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)
    explanation: str = Field(default="")
    raw: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()


class UXDesignRecord(BaseModel):
    """Persistent record for Experience Memory."""

    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str = Field(..., description="Reference to UIUXDesignerRequest")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    operation: str = Field(default="")
    project_name: str = Field(default="")
    personas_count: int = Field(default=0)
    screens_designed: int = Field(default=0)
    accessibility_score: float = Field(default=0.0)
    outcome: str = Field(default="pending", description="accepted|revised|rejected")
