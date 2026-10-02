"""
DevSecOps Engine.
"""

from __future__ import annotations

import logging

from apps.devsecops.schemas import (
    DevSecOpsInputs,
    DevSecOpsOperation,
    DevSecOpsReport,
    DevSecOpsRequest,
    PipelineSecurityGate,
    SecurityFinding,
    VulnerableDependency,
)
from apps.devsecops.security_engine import DevSecOpsSecurityEngine

logger = logging.getLogger(__name__)


class DevSecOpsEngine:
    """
    Orchestrates DevSecOps pipeline:
        1. Input Validation
        2. Security Gate / Dependency Scan / Runtime Policy / Compliance
        3. Result Generation
    """

    def __init__(self) -> None:
        self.engine = DevSecOpsSecurityEngine()

    def analyze(self, request: DevSecOpsRequest) -> DevSecOpsReport:
        inputs: DevSecOpsInputs = request.inputs
        validation = self.engine.check_input_validation(inputs)

        if not validation["valid"]:
            logger.warning("DevSecOps validation failed: %s", validation["errors"])
            return DevSecOpsReport(
                request_id=request.request_id,
                security_gates=[],
                findings=[],
                vulnerable_dependencies=[],
                policy_violations=[],
                recommendations=validation["errors"],
                quality_score=0.0,
            )

        security_gates: list[PipelineSecurityGate] = []
        findings: list[SecurityFinding] = []
        vulnerable_dependencies: list[VulnerableDependency] = []
        policy_violations: list[str] = []
        recommendations: list[str] = []

        if inputs.operation == DevSecOpsOperation.security_gate:
            security_gates.append(self.engine.evaluate_security_gate(inputs))
        elif inputs.operation == DevSecOpsOperation.dependency_scan:
            vulnerable_dependencies = self.engine.scan_dependencies(inputs)
            findings = self.engine.detect_security_findings(inputs)
        elif inputs.operation == DevSecOpsOperation.runtime_policy:
            policy_violations = self.engine.evaluate_runtime_policy(inputs)
        elif inputs.operation == DevSecOpsOperation.compliance_as_code:
            policy_violations = self.engine.check_compliance(inputs)
            security_gates.append(self.engine.evaluate_security_gate(inputs))

        recommendations.extend(self.engine.safety_boundary_check())

        quality_score = self.engine.compute_quality_score(
            security_gates=security_gates,
            findings=findings,
            vulnerable_dependencies=vulnerable_dependencies,
        )

        return DevSecOpsReport(
            request_id=request.request_id,
            security_gates=security_gates,
            findings=findings,
            vulnerable_dependencies=vulnerable_dependencies,
            policy_violations=policy_violations,
            recommendations=recommendations,
            quality_score=quality_score,
        )
