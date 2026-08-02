"""
Security Engineer Worker — thin adapter (per ADR-003).

Routes task requests to the Security Engineer Domain Engine.
Does not own business logic; delegates to SecurityEngineerEngine.
"""

from __future__ import annotations

from typing import Any

from apps.security_engineer.engine import SecurityEngineerEngine
from apps.security_engineer.schemas import (
    SecurityAssessmentRequest,
    AssessmentType,
)


class SecurityEngineerWorker:
    """
    Thin Worker adapter for the Security Engineer Capability Pack.

    Responsibilities:
        - Parse incoming task into SecurityAssessmentRequest
        - Delegate to SecurityEngineerEngine.review()
        - Return SecurityAssessmentReport as dict

    Usage::

        worker = SecurityEngineerWorker()
        report = await worker.execute(task)
    """

    def __init__(self, engine: SecurityEngineerEngine | None = None) -> None:
        self._engine = engine or SecurityEngineerEngine()

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a security assessment task.

        Expected task format::

            {
                "target_type": "code",
                "target": {"source_code": "..."},
                "standards": ["owasp_top10", "cis"],
                "check_secrets": true,
                "check_dependencies": true,
                "include_compliance_mapping": true
            }

        Returns:
            SecurityAssessmentReport as a JSON-serializable dict.
        """
        target_type = task.get("target_type", "full_review")
        try:
            assessment_type = AssessmentType(target_type)
        except ValueError:
            assessment_type = AssessmentType.full_review

        request = SecurityAssessmentRequest(
            target_type=assessment_type,
            target=task.get("target", {}),
            standards=task.get("standards", ["owasp_top10", "cis"]),
            include_remediation=task.get("include_remediation", True),
            include_compliance_mapping=task.get("include_compliance_mapping", True),
            check_secrets=task.get("check_secrets", True),
            check_dependencies=task.get("check_dependencies", True),
            scan_depth=task.get("scan_depth", "thorough"),
        )

        report = self._engine.review(request)
        return report.to_dict()
