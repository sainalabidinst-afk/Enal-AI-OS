"""
Data Engineer — Public Contracts (Pydantic schemas).

Defines the input (DataEngineeringRequest) and output (DataEngineeringReport)
contracts for the Data Engineer Capability Pack, plus all supporting types.

These schemas follow the RFC-0009 contract definitions exactly.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class JobType(str, Enum):
    etl = "etl"
    elt = "elt"
    clean = "clean"
    validate = "validate"
    schema_evolve = "schema_evolve"
    feature_engineer = "feature_engineer"
    time_series = "time_series"


class SourceType(str, Enum):
    csv = "csv"
    json = "json"
    api = "api"
    database = "database"
    file = "file"


class Operation(str, Enum):
    drop_duplicates = "drop_duplicates"
    fill_missing = "fill_missing"
    remove_outliers = "remove_outliers"
    normalize = "normalize"
    encode = "encode"
    aggregate = "aggregate"
    interpolate = "interpolate"


class QualityRule(str, Enum):
    completeness = "completeness"
    uniqueness = "uniqueness"
    validity = "validity"
    freshness = "freshness"
    consistency = "consistency"


class IssueType(str, Enum):
    missing_values = "missing_values"
    duplicate_rows = "duplicate_rows"
    schema_drift = "schema_drift"
    outlier = "outlier"
    invalid_format = "invalid_format"


class IssueSeverity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class JobStatus(str, Enum):
    success = "success"
    partial = "partial"
    failed = "failed"


class FeatureType(str, Enum):
    categorical = "categorical"
    numerical = "numerical"
    datetime = "datetime"


class ChangeType(str, Enum):
    added = "added"
    removed = "removed"
    type_changed = "type_changed"
    renamed = "renamed"


class DataSource(BaseModel):
    type: SourceType = Field(..., description="Type of data source")
    location: str = Field(..., description="File path, URL, or connection string")
    schema_definition: dict[str, Any] | None = Field(default=None, description="Expected schema definition")


class TransformOperation(BaseModel):
    operation: Operation = Field(..., description="Type of transformation")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Operation parameters")


class QualityRuleSpec(BaseModel):
    rule: QualityRule = Field(..., description="Quality dimension to check")
    thresholds: dict[str, float] = Field(default_factory=dict, description="Min/max thresholds")


class QualityIssue(BaseModel):
    type: IssueType = Field(..., description="Type of data quality issue")
    column: str = Field(default="", description="Affected column")
    severity: IssueSeverity = Field(default=IssueSeverity.medium)
    count: int = Field(default=0, description="Number of occurrences")
    remediation: str = Field(default="", description="How to fix")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class QualityReport(BaseModel):
    completeness: float = Field(default=0.0, ge=0.0, le=1.0)
    uniqueness: float = Field(default=0.0, ge=0.0, le=1.0)
    validity: float = Field(default=0.0, ge=0.0, le=1.0)
    freshness: float = Field(default=0.0, ge=0.0, le=1.0)
    consistency: float = Field(default=0.0, ge=0.0, le=1.0)
    overall_score: float = Field(default=0.0, ge=0.0, le=1.0)
    issues: list[QualityIssue] = Field(default_factory=list)


class SchemaChange(BaseModel):
    column: str = Field(..., description="Column name changed")
    change_type: ChangeType = Field(..., description="Type of schema change")
    old_type: str = Field(default="", description="Previous type")
    new_type: str = Field(default="", description="New type")


class SchemaDriftReport(BaseModel):
    detected: bool = Field(default=False)
    changes: list[SchemaChange] = Field(default_factory=list)
    migration_required: bool = Field(default=False)


class FeatureSpec(BaseModel):
    name: str = Field(..., description="Feature name")
    type: FeatureType = Field(default=FeatureType.numerical)
    description: str = Field(default="")
    expression: str = Field(default="", description="Transformation expression")
    dependencies: list[str] = Field(default_factory=list)


class TimeSeriesReport(BaseModel):
    frequency: str = Field(default="1h")
    missing_count: int = Field(default=0)
    interpolated_count: int = Field(default=0)
    alignment_complete: bool = Field(default=False)


class DatasetSummary(BaseModel):
    row_count: int = Field(default=0)
    column_count: int = Field(default=0)
    schema_definition: dict[str, Any] = Field(default_factory=dict)
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)


class DataLineage(BaseModel):
    source: str = Field(default="")
    transforms: list[str] = Field(default_factory=list)
    target: str = Field(default="")


class DataEngineeringRequest(BaseModel):
    """Input contract for a data engineering request."""

    job_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    job_type: JobType = Field(..., description="Type of data engineering job")
    source: DataSource = Field(..., description="Data source specification")
    operations: list[TransformOperation] = Field(default_factory=list)
    quality_rules: list[QualityRuleSpec] = Field(default_factory=list)
    target_schema: dict[str, Any] | None = Field(default=None)
    time_series_config: dict[str, Any] | None = Field(default=None)
    feature_definitions: list[FeatureSpec] = Field(default_factory=list)


class DataEngineeringReport(BaseModel):
    """Output contract for a data engineering report."""

    job_id: str = Field(..., description="Reference to the original request")
    job_type: str = Field(..., description="The job type performed")
    status: JobStatus = Field(default=JobStatus.success)
    dataset: DatasetSummary = Field(default_factory=DatasetSummary)
    quality_report: QualityReport = Field(default_factory=QualityReport)
    schema_drift: SchemaDriftReport = Field(default_factory=SchemaDriftReport)
    features: list[FeatureSpec] = Field(default_factory=list)
    time_series: TimeSeriesReport = Field(default_factory=TimeSeriesReport)
    lineage: DataLineage = Field(default_factory=DataLineage)
    execution_time_ms: int = Field(default=0)
    explanation: str = Field(default="")
    raw: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()


class DataQualityRecord(BaseModel):
    """Persistent record for Experience Memory."""

    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    job_id: str = Field(..., description="Reference to DataEngineeringRequest")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    job_type: str = Field(default="")
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)
    issues_found: int = Field(default=0)
    issues_resolved: int = Field(default=0)
    schema_drift_detected: bool = Field(default=False)
    features_created: int = Field(default=0)
    time_series_gaps_filled: int = Field(default=0)
    outcome: str = Field(default="pending", description="success|partial|failed|revised")
