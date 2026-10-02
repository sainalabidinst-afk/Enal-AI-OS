"""
DevSecOps Pack
==============

Demonstrates ECP capabilities for CI/CD security gate enforcement.

Workflow:
    User Request
        ↓
    Intent Router
        ↓
    Capability Graph → devsecops-*
        ↓
    Task Planner
        ↓
    Subtasks:
    - Security Gate Scanning (SAST, DAST, SCA, Container, Secrets)
    - Vulnerability Collection
    - Compliance Verification
    - Security Scoring & Recommendations
        ↓
    Execution Planner
        ↓
    Execution Runtime
        ↓
    DevSecOps Worker
        ↓
    Security Scanning Engine (full security pipeline)
        ↓
    Result
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.devsecops.engine import DevSecOpsEngine
from apps.devsecops.schemas import (
    BusinessContext,
    ComplianceResult,
    DependencyType,
    DevSecOpsConfig,
    DevSecOpsPackRecord,
    DevSecOpsReport,
    DevSecOpsRequest,
    GateResult,
    GateStatus,
    PipelineConfig,
    PipelineStage,
    SecurityGate,
    Vulnerability,
    VulnerabilitySeverity,
)
from apps.devsecops.worker import DevSecOpsWorker


class DevSecOpsApp(BaseReferenceApp):
    name = "devsecops"
    version = "1.0.0"
    description = "CI/CD security gates: SAST, DAST, SCA, container scanning, secrets detection, policy enforcement and compliance checks"  # noqa: E501
    category = "devsecops"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = DevSecOpsWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> DevSecOpsApp:
    return DevSecOpsApp()


__all__ = [
    "DevSecOpsApp",
    "DevSecOpsEngine",
    "DevSecOpsWorker",
    "SecurityGate",
    "VulnerabilitySeverity",
    "GateStatus",
    "DependencyType",
    "BusinessContext",
    "PipelineStage",
    "PipelineConfig",
    "DevSecOpsConfig",
    "DevSecOpsRequest",
    "Vulnerability",
    "GateResult",
    "ComplianceResult",
    "DevSecOpsReport",
    "DevSecOpsPackRecord",
]
