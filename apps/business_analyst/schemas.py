"""
Business Analyst — Public Contracts (Pydantic schemas).

Defines the input (BusinessAnalysisRequest) and output (BusinessAnalysisReport)
contracts for the Business Analyst Capability Pack, plus all supporting types.

These schemas follow the RFC-0013 contract definitions exactly.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class OperationType(str, Enum):
    requirement_gathering = "requirement_gathering"
    process_modeling = "process_modeling"
    user_story = "user_story"
    use_case = "use_case"
    brd_generation = "brd_generation"
    functional_spec = "functional_spec"
    gap_analysis = "gap_analysis"
    roi_analysis = "roi_analysis"
    process_optimization = "process_optimization"


class RequirementType(str, Enum):
    functional = "functional"
    non_functional = "non_functional"


class Priority(str, Enum):
    must_have = "must_have"
    should_have = "should_have"
    could_have = "could_have"
    wont_have = "wont_have"


class StoryPoint(str, Enum):
    xs = "XS"
    s = "S"
    m = "M"
    l = "L"
    xl = "XL"


class ProcessActivityType(str, Enum):
    start = "start"
    end = "end"
    task = "task"
    decision = "decision"
    gateway = "gateway"
    subprocess = "subprocess"


class OutputFormat(str, Enum):
    json = "json"
    markdown = "markdown"
    bpmn = "bpmn"
    jira = "jira"
    confluence = "confluence"


class Severity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"


class FindingCategory(str, Enum):
    schema = "schema"
    requirement = "requirement"
    process = "process"
    roi = "roi"
    gap = "gap"


class Finding(BaseModel):
    """A single business analysis finding."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category: FindingCategory = Field(default=FindingCategory.schema)
    severity: Severity = Field(default=Severity.medium)
    title: str = Field(..., description="Short title")
    description: str = Field(..., description="Detailed description")
    evidence: dict[str, Any] = Field(default_factory=dict)
    recommendation: str = Field(default="", description="Remediation guidance")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class BusinessContext(BaseModel):
    domain: str = Field(default="", description="Business domain (e-commerce, fintech, etc.)")
    project_name: str = Field(default="", description="Project name")
    description: str = Field(default="", description="Project overview")


class StakeholderInput(BaseModel):
    natural_language_requirements: list[str] = Field(default_factory=list)
    stakeholder_notes: list[str] = Field(default_factory=list)
    interview_transcripts: list[str] = Field(default_factory=list)
    current_state_documentation: str = Field(default="")
    technical_constraints: list[str] = Field(default_factory=list)


class Persona(BaseModel):
    name: str = Field(default="")
    role: str = Field(default="")
    goals: list[str] = Field(default_factory=list)
    pain_points: list[str] = Field(default_factory=list)


class QualityAttributes(BaseModel):
    availability_target: str = Field(default="99.9%")
    performance_target: str = Field(default="< 200ms response time")
    security_target: str = Field(default="OWASP Top 10 compliance")


class Requirement(BaseModel):
    id: str = Field(default_factory=lambda: f"REQ-{uuid.uuid4().hex[:8]}")
    title: str = Field(default="")
    description: str = Field(default="")
    type: RequirementType = Field(default=RequirementType.functional)
    priority: Priority = Field(default=Priority.should_have)
    clarity_score: float = Field(default=0.0, ge=0.0, le=1.0)
    ambiguity_flags: list[str] = Field(default_factory=list)
    source: str = Field(default="")
    acceptance_criteria: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)


class UserStory(BaseModel):
    id: str = Field(default_factory=lambda: f"US-{uuid.uuid4().hex[:8]}")
    title: str = Field(..., description="As a <role> I want <goal> so that <benefit>")
    description: str = Field(default="")
    acceptance_criteria: list[str] = Field(default_factory=list)
    story_points: str = Field(default=StoryPoint.m.value)
    priority: Priority = Field(default=Priority.should_have)
    dependencies: list[str] = Field(default_factory=list)


class UseCase(BaseModel):
    id: str = Field(default_factory=lambda: f"UC-{uuid.uuid4().hex[:8]}")
    name: str = Field(default="")
    primary_actor: str = Field(default="")
    preconditions: list[str] = Field(default_factory=list)
    postconditions: list[str] = Field(default_factory=list)
    main_scenario: list[str] = Field(default_factory=list)
    alternative_scenarios: list[str] = Field(default_factory=list)
    exceptions: list[str] = Field(default_factory=list)


class ProcessActivity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: ProcessActivityType = Field(default=ProcessActivityType.task)
    name: str = Field(default="")
    description: str = Field(default="")
    actor: str = Field(default="")
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    decision_condition: str = Field(default="")
    next_activities: list[str] = Field(default_factory=list)


class ProcessModel(BaseModel):
    name: str = Field(default="")
    activities: list[ProcessActivity] = Field(default_factory=list)
    start_activity: str = Field(default="")
    end_activity: str = Field(default="")


class GapItem(BaseModel):
    id: str = Field(default_factory=lambda: f"GAP-{uuid.uuid4().hex[:6]}")
    business_need: str = Field(default="")
    current_capability: str = Field(default="")
    required_capability: str = Field(default="")
    gap_description: str = Field(default="")
    priority: Priority = Field(default=Priority.should_have)
    estimated_effort: str = Field(default="")
    impact_if_unaddressed: str = Field(default="")


class ROIResult(BaseModel):
    npv: float = Field(default=0.0, description="Net Present Value")
    payback_period_months: int = Field(default=0)
    roi_percentage: float = Field(default=0.0)
    cost_estimate: float = Field(default=0.0)
    benefit_estimate: float = Field(default=0.0)
    assumptions: list[str] = Field(default_factory=list)


class ProcessOptimization(BaseModel):
    process_name: str = Field(default="")
    inefficiency: str = Field(default="")
    current_time: str = Field(default="")
    optimized_time: str = Field(default="")
    recommendation: str = Field(default="")
    estimated_savings: str = Field(default="")


class BusinessAnalysisRequest(BaseModel):
    """Input contract for a business analysis request."""

    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: OperationType = Field(..., description="Type of business analysis")
    business_context: BusinessContext = Field(default_factory=BusinessContext)
    inputs: StakeholderInput = Field(default_factory=StakeholderInput)
    personas: list[Persona] = Field(default_factory=list)
    quality_attributes: QualityAttributes = Field(default_factory=QualityAttributes)
    output_format: OutputFormat = Field(default=OutputFormat.markdown)


class BusinessAnalysisReport(BaseModel):
    """Output contract for a business analysis report."""

    request_id: str = Field(..., description="Reference to the original request")
    operation: str = Field(..., description="The operation performed")
    requirements: list[Requirement] = Field(default_factory=list)
    user_stories: list[UserStory] = Field(default_factory=list)
    use_cases: list[UseCase] = Field(default_factory=list)
    process_model: ProcessModel | None = Field(default=None)
    gaps: list[GapItem] = Field(default_factory=list)
    roi_result: ROIResult | None = Field(default=None)
    optimizations: list[ProcessOptimization] = Field(default_factory=list)
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)
    explanation: str = Field(default="")
    raw: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()


class BusinessAnalysisRecord(BaseModel):
    """Persistent record for Experience Memory."""

    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str = Field(..., description="Reference to BusinessAnalysisRequest")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    operation: str = Field(default="")
    domain: str = Field(default="")
    requirements_count: int = Field(default=0)
    user_stories_count: int = Field(default=0)
    gaps_identified: int = Field(default=0)
    roi_analyzed: bool = Field(default=False)
    outcome: str = Field(default="pending", description="success|partial|failed|revised")
