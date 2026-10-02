"""
DevSecOps Engine.
"""

from __future__ import annotations

import logging

from apps.devsecops.schemas import (
    DevSecOpsConfig,
    DevSecOpsReport,
    DevSecOpsRequest,
)
from apps.devsecops.security_engine import SecurityScanningEngine

logger = logging.getLogger(__name__)


class DevSecOpsEngine:
    """
    Orchestrates the DevSecOps security pipeline:
        1. Security Gate Scanning
        2. Vulnerability Collection
        3. Compliance Verification
        4. Security Scoring & Recommendations
    """

    def __init__(self) -> None:
        self.engine = SecurityScanningEngine()

    def execute(self, request: DevSecOpsRequest) -> DevSecOpsReport:
        config: DevSecOpsConfig = request.inputs

        gate_results = self.engine.scan_gates(config)
        all_vulnerabilities = self.engine.collect_vulnerabilities(config)
        compliance_results = self.engine.verify_compliance(config)
        recommendations = self.engine.generate_recommendations(
            gate_results, all_vulnerabilities
        )

        security_score, overall_status = self.engine.compute_security_score(
            gate_results, all_vulnerabilities
        )

        critical_count = sum(1 for v in all_vulnerabilities if v.severity.value == "critical")

        return DevSecOpsReport(
            request_id=request.request_id,
            pipeline_name=config.pipeline.name,
            gate_results=gate_results,
            all_vulnerabilities=all_vulnerabilities,
            compliance_results=compliance_results,
            overall_status=overall_status,
            security_score=security_score,
            total_vulnerabilities=len(all_vulnerabilities),
            critical_vulnerabilities=critical_count,
            recommendations=recommendations,
        )


__all__ = ["DevSecOpsEngine"]
