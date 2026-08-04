"""
Documentation Engineer — Public Contracts (Pydantic schemas).

Defines the input (DocumentationRequest) and output (DocumentationReport)
contracts for the Documentation Engineer Capability Pack, plus all supporting types.

These schemas follow the RFC-0016 contract definitions exactly.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class OperationType(str, Enum):
    openapi_generation = "openapi_generation"
    sdk_documentation = "sdk_documentation"
    architecture_documentation = "architecture_documentation"
    documentation_validation = "documentation_validation"
    release_notes_generation = "release_notes_generation"


class GenerationStatus(str, Enum):
    generated = "generated"
    validated = "validated"
    skipped = "skipped"
    failed = "failed"


class IssueSeverity(str, Enum):
    error = "error"
    warning = "warning"
    info = "info"


class DocumentationTarget(BaseModel):
    app_name: str = Field(default="", description="Target application name")
    version: str = Field(default="", description="Target version")
    output_path: str = Field(default="docs/", description="Output directory path")


class GenerationOptions(BaseModel):
    include_examples: bool = Field(default=True)
    validate_links: bool = Field(default=True)
    generate_diagrams: bool = Field(default=True)
    include_deprecated: bool = Field(default=False)


class DocumentationInput(BaseModel):
    source_code_path: str = Field(default="")
    existing_docs_path: str = Field(default="")
    commit_range: str = Field(default="")
    architecture_artifacts: list[str] = Field(default_factory=list)


class GeneratedFile(BaseModel):
    path: str = Field(default="")
    type: str = Field(default="")
    size_bytes: int = Field(default=0)
    status: GenerationStatus = Field(default=GenerationStatus.generated)
    issues: list[dict[str, Any]] = Field(default_factory=list)


class DocumentationSummary(BaseModel):
    total_files: int = Field(default=0)
    generated: int = Field(default=0)
    validated: int = Field(default=0)
    errors: int = Field(default=0)
    warnings: int = Field(default=0)


class QualityMetrics(BaseModel):
    completeness: float = Field(default=0.0, ge=0.0, le=1.0)
    accuracy: float = Field(default=0.0, ge=0.0, le=1.0)
    consistency: float = Field(default=0.0, ge=0.0, le=1.0)
    freshness: float = Field(default=0.0, ge=0.0, le=1.0)


class DocumentationRequest(BaseModel):
    """Input contract for a documentation request."""

    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: OperationType = Field(..., description="Type of documentation operation")
    target: DocumentationTarget = Field(default_factory=DocumentationTarget)
    options: GenerationOptions = Field(default_factory=GenerationOptions)
    inputs: DocumentationInput = Field(default_factory=DocumentationInput)


class DocumentationReport(BaseModel):
    """Output contract for a documentation report."""

    request_id: str = Field(..., description="Reference to the original request")
    operation: str = Field(..., description="The operation performed")
    generated_files: list[GeneratedFile] = Field(default_factory=list)
    summary: DocumentationSummary = Field(default_factory=DocumentationSummary)
    quality_metrics: QualityMetrics = Field(default_factory=QualityMetrics)
    explanation: str = Field(default="")
    raw: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()


class DocumentationRecord(BaseModel):
    """Persistent record for Experience Memory."""

    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str = Field(..., description="Reference to DocumentationRequest")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    operation: str = Field(default="")
    app_name: str = Field(default="")
    files_generated: int = Field(default=0)
    files_validated: int = Field(default=0)
    issues_found: int = Field(default=0)
    outcome: str = Field(default="pending", description="success|partial|failed|revised")
