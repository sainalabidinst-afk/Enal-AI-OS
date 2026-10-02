"""
DevSecOps Capability Schemas
=============================

Typed contracts for the DevSecOps capability pack.
Defines input (DevSecOpsRequest) and output (DevSecOpsReport) contracts for
CI/CD security gate evaluation, vulnerability scanning, dependency checks,
and pipeline security analysis.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class SecurityGate(StrEnum):
    sast = "sast"
    dast = "dast"
    sca = "sca"
    container_scan = "container_scan"
    infrastructure_scan = "infrastructure_scan"
    secrets_detection = "secrets_detection"
    policy_enforcement = "policy_enforcement"
    compliance_check = "compliance_check"


class VulnerabilitySeverity(StrEnum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"


class GateStatus(StrEnum):
    pass_gate = "pass"
    fail_gate = "fail"
    warn = "warn"
    skip = "skip"


class DependencyType(StrEnum):
    direct = "direct"
    transitive = "transitive"
    dev = "dev"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=8, ge=1)


class PipelineStage(BaseModel):
    name: str
    order: int
    gates: list[SecurityGate] = Field(default_factory=list)


class PipelineConfig(BaseModel):
    name: str
    stages: list[PipelineStage] = Field(default_factory=list)
    repository_url: str = ""
    branch: str = "main"
    environment: str = "production"
    compliance_standards: list[str] = Field(default_factory=list)
    policy_thresholds: dict[str, Any] = Field(default_factory=dict)


class Vulnerability(BaseModel):
    id: str
    cve: str
    title: str
    severity: VulnerabilitySeverity
    cvss_score: float = Field(default=0.0, ge=0.0, le=10.0)
    package: str
    version: str
    description: str
    remediation: str
    dependency_type: DependencyType = DependencyType.direct
    fix_version: str = ""


class GateResult(BaseModel):
    gate: SecurityGate
    status: GateStatus
    vulnerabilities_found: int = 0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    execution_time_seconds: float = 0.0
    details: list[str] = Field(default_factory=list)


class ComplianceResult(BaseModel):
    standard: str
    checks_total: int = 0
    checks_passed: int = 0
    checks_failed: int = 0
    compliance_score: float = Field(default=0.0, ge=0.0, le=1.0)
    violations: list[str] = Field(default_factory=list)


class DevSecOpsConfig(BaseModel):
    operation: str = "pipeline_security_audit"
    pipeline: PipelineConfig
    stages: list[PipelineStage] = Field(default_factory=list)
    policy_thresholds: dict[str, Any] = Field(default_factory=dict)
    constraints: dict[str, Any] = Field(default_factory=dict)


class DevSecOpsRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "pipeline_security_audit"
    business_context: BusinessContext
    inputs: DevSecOpsConfig
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class DevSecOpsReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    pipeline_name: str
    gate_results: list[GateResult] = Field(default_factory=list)
    all_vulnerabilities: list[Vulnerability] = Field(default_factory=list)
    compliance_results: list[ComplianceResult] = Field(default_factory=list)
    overall_status: GateStatus = GateStatus.pass_gate
    security_score: float = Field(default=0.0, ge=0.0, le=1.0)
    total_vulnerabilities: int = 0
    critical_vulnerabilities: int = 0
    recommendations: list[str] = Field(default_factory=list)
    model_version: str = "1.0.0"


class DevSecOpsPackRecord(BaseModel):
    pack_id: str = "devsecops"
    version: str = "1.0.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "sast_scanning",
        "dast_scanning",
        "sca_dependency_check",
        "container_security_scan",
        "secrets_detection",
        "policy_enforcement",
    ])


__all__ = [
    "BusinessContext",
    "ComplianceResult",
    "DependencyType",
    "DevSecOpsConfig",
    "DevSecOpsPackRecord",
    "DevSecOpsReport",
    "DevSecOpsRequest",
    "GateResult",
    "GateStatus",
    "PipelineConfig",
    "PipelineStage",
    "SecurityGate",
    "Vulnerability",
    "VulnerabilitySeverity",
]
