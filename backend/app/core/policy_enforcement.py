"""
Policy Enforcement — Core Service.

Enforces GDPR/ISO compliance policies for the E2E scenario
and general-purpose governance checks.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class PolicyCheckResult(BaseModel):
    """Result of a single policy check."""

    policy_id: str = ""
    policy_name: str = ""
    status: str = "pass"
    severity: str = "low"
    details: str = ""
    remediation: str = ""


class ComplianceReport(BaseModel):
    """Full compliance report for an action or data payload."""

    checks: list[PolicyCheckResult] = Field(default_factory=list)
    overall_status: str = "pass"
    risk_score: float = Field(default=0.0, ge=0.0, le=1.0)
    framework: str = ""
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    formula: str = ""
    inputs_traced: list[str] = Field(default_factory=list)
    quality_score: float = Field(default=0.90, ge=0, le=1)


class PolicyEnforcementService:
    """Enforce GDPR/ISO compliance policies."""

    VERSION = "1.0.0"

    POLICIES: dict[str, dict[str, Any]] = {
        "gdpr_data_minimization": {
            "name": "GDPR Data Minimization",
            "framework": "GDPR",
            "severity": "high",
            "check": lambda payload: _count_fields(payload) <= 10,
        },
        "gdpr_consent": {
            "name": "GDPR Consent Required",
            "framework": "GDPR",
            "severity": "high",
            "check": lambda payload: payload.get("consent_given", False),
        },
        "gdpr_right_to_erasure": {
            "name": "GDPR Right to Erasure",
            "framework": "GDPR",
            "severity": "medium",
            "check": lambda payload: not payload.get("include_pii", False),
        },
        "iso27001_access_control": {
            "name": "ISO 27001 Access Control",
            "framework": "ISO 27001",
            "severity": "high",
            "check": lambda payload: payload.get("authenticated", False),
        },
        "iso27001_audit_logging": {
            "name": "ISO 27001 Audit Logging",
            "framework": "ISO 27001",
            "severity": "medium",
            "check": lambda payload: payload.get("audit_trail", False),
        },
        "pii_detection": {
            "name": "PII Detection",
            "framework": "GDPR",
            "severity": "high",
            "check": lambda payload: not _detect_pii(payload),
        },
    }

    def check_action(self, action: str, payload: dict[str, Any]) -> ComplianceReport:
        """Run all applicable policy checks for an action and payload."""
        checks: list[PolicyCheckResult] = []
        applicable_policies = self._applicable_policies(action, payload)
        inputs_traced = ["action", "payload"]

        for policy_id, policy in applicable_policies.items():
            passed = bool(policy["check"](payload))
            severity = policy.get("severity", "low")
            status = "pass" if passed else "fail"
            remediation = ""
            if not passed:
                if policy_id == "gdpr_data_minimization":
                    remediation = "Reduce the number of data fields included in the payload"
                elif policy_id == "gdpr_consent":
                    remediation = "Obtain explicit user consent before processing"
                elif policy_id == "gdpr_right_to_erasure":
                    remediation = "Remove PII fields or anonymize the data"
                elif policy_id == "iso27001_access_control":
                    remediation = "Ensure the user is authenticated before proceeding"
                elif policy_id == "iso27001_audit_logging":
                    remediation = "Enable audit trail logging for this action"
                elif policy_id == "pii_detection":
                    remediation = "Remove or mask detected PII before processing"

            checks.append(
                PolicyCheckResult(
                    policy_id=policy_id,
                    policy_name=policy["name"],
                    status=status,
                    severity=severity,
                    details=f"Policy {policy_id} {status}ed for action={action}",
                    remediation=remediation,
                )
            )
            inputs_traced.append(policy_id)

        failures = [c for c in checks if c.status == "fail"]
        overall = "fail" if failures else "pass"
        risk_score = min(len(failures) / max(len(checks), 1), 1.0)

        return ComplianceReport(
            checks=checks,
            overall_status=overall,
            risk_score=risk_score,
            framework="GDPR/ISO 27001",
            formula="policy: check(action, payload) -> compliance_report",
            inputs_traced=inputs_traced,
            quality_score=0.95 if overall == "pass" else 0.70,
        )

    def _applicable_policies(
        self, action: str, payload: dict[str, Any]
    ) -> dict[str, dict[str, Any]]:
        """Return policies applicable to this action."""
        applicable: dict[str, dict[str, Any]] = {}
        for policy_id, policy in self.POLICIES.items():
            if action in ("send_email", "process_document", "store_data", "share_data"):
                applicable[policy_id] = policy
        return applicable

    def get_supported_policies(self) -> list[str]:
        """Return list of supported policy IDs."""
        return list(self.POLICIES.keys())

    def get_record(self) -> dict[str, Any]:
        """Return a capability record for registry/memory."""
        return {
            "pack_id": "policy-enforcement",
            "version": self.VERSION,
            "capabilities": ["check_action", "list_policies", "generate_report"],
        }


policy_enforcement = PolicyEnforcementService()


def _count_fields(payload: dict[str, Any]) -> int:
    """Count the number of top-level fields in a payload."""
    return len(payload)


def _detect_pii(payload: dict[str, Any]) -> bool:
    """Detect whether payload contains PII indicators."""
    pii_fields = {"email", "ssn", "phone", "address", "name", "id_number", "passport"}
    return any(key in pii_fields for key in payload.keys())
