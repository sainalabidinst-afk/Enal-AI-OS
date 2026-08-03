"""
Database Engineer — Public Contracts (Pydantic schemas).

Defines the input (DatabaseRequest) and output (DatabaseReport)
contracts for the Database Engineer Capability Pack, plus all supporting types.

These schemas follow the RFC-0010 contract definitions exactly.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DatabaseType(str, Enum):
    postgresql = "postgresql"
    mysql = "mysql"
    sqlite = "sqlite"
    mongodb = "mongodb"
    sqlserver = "sqlserver"


class OperationType(str, Enum):
    schema_design = "schema_design"
    query_optimization = "query_optimization"
    migration = "migration"
    index_recommendation = "index_recommendation"
    replication_plan = "replication_plan"
    backup_plan = "backup_plan"
    performance_analysis = "performance_analysis"


class Severity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class FindingCategory(str, Enum):
    schema = "schema"
    query_performance = "query_performance"
    index = "index"  # type: ignore[assignment]
    migration = "migration"
    replication = "replication"
    backup = "backup"
    deadlock = "deadlock"


class ColumnDefinition(BaseModel):
    name: str = Field(..., description="Column name")
    type: str = Field(..., description="SQL data type")
    constraints: list[str] = Field(default_factory=list, description="NOT NULL, UNIQUE, DEFAULT, etc.")


class ForeignKey(BaseModel):
    column: str = Field(..., description="Column in this table")
    references: str = Field(..., description="Referenced table name")
    references_column: str = Field(..., description="Referenced column name")


class TableDefinition(BaseModel):
    name: str = Field(..., description="Table name")
    columns: list[ColumnDefinition] = Field(default_factory=list)
    primary_key: list[str] = Field(default_factory=list)
    foreign_keys: list[ForeignKey] = Field(default_factory=list)


class SchemaDefinition(BaseModel):
    tables: list[TableDefinition] = Field(default_factory=list)


class WorkloadProfile(BaseModel):
    read_write_ratio: float = Field(default=0.5, ge=0.0, le=1.0)
    peak_qps: int = Field(default=100)
    data_volume_gb: float = Field(default=10.0)
    query_patterns: list[str] = Field(default_factory=list)


class Finding(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category: FindingCategory = Field(..., description="Category of finding")
    severity: Severity = Field(default=Severity.medium)
    title: str = Field(..., description="Short title")
    description: str = Field(..., description="Detailed description")
    evidence: dict[str, Any] = Field(default_factory=dict, description="Query, table, execution plan")
    recommendation: str = Field(default="", description="How to fix")
    estimated_improvement: str = Field(default="", description="Expected performance gain")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class SchemaRecommendation(BaseModel):
    table: str = Field(..., description="Table name")
    action: str = Field(..., description="add_column | modify_column | add_index | add_constraint")
    details: dict[str, Any] = Field(default_factory=dict)
    priority: Severity = Field(default=Severity.medium)
    rationale: str = Field(default="")


class IndexRecommendation(BaseModel):
    table: str = Field(..., description="Table name")
    columns: list[str] = Field(default_factory=list)
    index_type: str = Field(default="btree", description="btree | hash | gin | gist")
    estimated_impact: str = Field(default="", description="Expected query improvement")
    priority: Severity = Field(default=Severity.medium)


class MigrationStep(BaseModel):
    step_number: int = Field(default=1)
    action: str = Field(..., description="CREATE | ALTER | DROP | INSERT")
    sql: str = Field(..., description="SQL statement to execute")
    rollback_sql: str = Field(default="", description="SQL to reverse this step")
    description: str = Field(default="")


class MigrationPlan(BaseModel):
    from_version: str = Field(default="")
    to_version: str = Field(default="")
    steps: list[MigrationStep] = Field(default_factory=list)
    conflicts: list[str] = Field(default_factory=list)
    rollback_available: bool = Field(default=True)


class ReplicationDesign(BaseModel):
    strategy: str = Field(default="primary_replica", description="primary_replica | multi_primary | leaderless")
    topology: str = Field(default="", description="Description of replication topology")
    nodes: list[dict[str, Any]] = Field(default_factory=list)
    failover_strategy: str = Field(default="automatic")
    estimated_lag_ms: int = Field(default=0)


class BackupPlan(BaseModel):
    schedule: str = Field(default="daily", description="backup frequency")
    backup_type: str = Field(default="full", description="full | incremental | differential")
    retention_days: int = Field(default=30)
    rto_hours: float = Field(default=4.0)
    rpo_minutes: int = Field(default=60)
    storage_location: str = Field(default="local")
    encryption_required: bool = Field(default=True)
    steps: list[str] = Field(default_factory=list)


class PerformanceStats(BaseModel):
    slow_queries: int = Field(default=0)
    deadlocks_detected: int = Field(default=0)
    avg_query_time_ms: float = Field(default=0.0)
    peak_connections: int = Field(default=0)
    cache_hit_ratio: float = Field(default=0.0)


class DatabaseRequest(BaseModel):
    """Input contract for a database engineering request."""

    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: OperationType = Field(..., description="Type of database operation")
    database_type: DatabaseType = Field(..., description="Target database type")
    database_schema: SchemaDefinition | None = Field(default=None, description="Database schema")
    queries: list[str] = Field(default_factory=list, description="SQL queries to analyze")
    workload_profile: WorkloadProfile | None = Field(default=None)
    current_schema_version: str = Field(default="v1")
    target_schema_version: str = Field(default="v2")
    rto_hours: float = Field(default=4.0)
    rpo_minutes: int = Field(default=60)


class DatabaseReport(BaseModel):
    """Output contract for a database engineering report."""

    request_id: str = Field(..., description="Reference to the original request")
    operation: str = Field(..., description="The operation performed")
    findings: list[Finding] = Field(default_factory=list)
    schema_recommendations: list[SchemaRecommendation] = Field(default_factory=list)
    index_recommendations: list[IndexRecommendation] = Field(default_factory=list)
    migration_plan: MigrationPlan | None = Field(default=None)
    replication_design: ReplicationDesign | None = Field(default=None)
    backup_plan: BackupPlan | None = Field(default=None)
    performance_stats: PerformanceStats = Field(default_factory=PerformanceStats)
    explanation: str = Field(default="")
    raw: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()


class DatabaseAnalysisRecord(BaseModel):
    """Persistent record for Experience Memory."""

    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str = Field(..., description="Reference to DatabaseRequest")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    operation: str = Field(default="")
    database_type: str = Field(default="")
    findings_count: int = Field(default=0)
    critical_count: int = Field(default=0)
    high_count: int = Field(default=0)
    migration_planned: bool = Field(default=False)
    backup_configured: bool = Field(default=False)
    outcome: str = Field(default="pending", description="success|partial|failed|revised")
