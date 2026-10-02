"""
DevSecOps Schemas
=================

Typed contracts for the DevSecOps capability pack.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class DevSecOpsOperation(StrEnum):
    security_gate = "security_gate"
    dependency_scan = "dependency_scan"
    runtime_policy = "runtime_policy"
    compliance_as_code = "compliance_as_code"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=5, ge=1)
    budget_monthly_usd: float = Field(default=10000, ge=0)


class DevSecOpsInputs(BaseModel):
    operation: DevSecOpsOperation
    pipeline_name: str = ""
    dependencies: list[str] = Field(default_factory=list)
    dependency_versions: dict[str, str] = Field(default_factory=dict)
    policies: list[str] = Field(default_factory=list)
    cve_database: str = "NVD"
    severity_threshold: str = "high"
    scan_depth: str = "full"
    environment: str = "production"


class PipelineSecurityGate(BaseModel):
    stage_name: str
    checks: list[str] = Field(default_factory=list)
    passed: bool = False
    blocking: bool = True
    failure_reasons: list[str] = Field(default_factory=list)


class SecurityFinding(BaseModel):
    finding_id: str
    severity: str
    category: str
    description: str
    file_path: str = ""
    line_number: int = 0
    cwe_id: str = ""
    remediation: str = ""


class VulnerableDependency(BaseModel):
    name: str
    current_version: str
    latest_version: str
    cve_count: int
    severity: str
    remediation: str = ""


class DevSecOpsReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    security_gates: list[PipelineSecurityGate] = Field(default_factory=list)
    findings: list[SecurityFinding] = Field(default_factory=list)
    vulnerable_dependencies: list[VulnerableDependency] = Field(default_factory=list)
    policy_violations: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    quality_score: float = Field(default=0.90, ge=0, le=1)
    model_version: str = "1.0.0"


class DevSecOpsRecord(BaseModel):
    pack_id: str = "devsecops"
    version: str = "3.0.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "security_gate",
        "dependency_scan",
        "runtime_policy",
        "compliance_as_code",
    ])


class DevSecOpsRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    business_context: BusinessContext
    inputs: DevSecOpsInputs
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


__all__ = [
    "DevSecOpsInputs",
    "DevSecOpsOperation",
    "DevSecOpsRequest",
    "DevSecOpsReport",
    "DevSecOpsRecord",
    "PipelineSecurityGate",
    "SecurityFinding",
    "VulnerableDependency",
    "BusinessContext",
]
