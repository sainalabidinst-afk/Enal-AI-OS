"""
F6 — Release Engineer
=======================

Checks release readiness:
- changelog
- semantic version
- migration
- rollback plan
- deployment checklist
- post-deployment verification
"""

import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class ReleaseCheck:
    name: str
    status: str
    detail: str = ""
    severity: str = Severity.INFO


@dataclass
class ReleaseReport:
    ready: bool = False
    checks: list[ReleaseCheck] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ready": self.ready,
            "checks": [{"name": c.name, "status": c.status, "detail": c.detail, "severity": c.severity} for c in self.checks],
            "summary": self.summary,
        }


class ReleaseEngineer:
    """Validates release readiness."""

    async def review(self, changes: list[dict[str, Any]], context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        report = ReleaseReport()
        self._check_changelog(changes, context, report)
        self._check_semver(changes, context, report)
        self._check_migration(changes, context, report)
        self._check_rollback(changes, context, report)
        self._check_deployment_checklist(changes, context, report)
        self._check_post_deployment(changes, context, report)
        self._compute_readiness(report)
        return report.to_dict()

    def _check_changelog(self, changes: list[dict[str, Any]], context: dict[str, Any], report: ReleaseReport):
        changelog = context.get("changelog", "")
        if not changelog:
            report.checks.append(ReleaseCheck(
                name="Changelog",
                status="missing",
                detail="No changelog provided.",
                severity=Severity.HIGH,
            ))
        elif len(changelog) < 50:
            report.checks.append(ReleaseCheck(
                name="Changelog",
                status="insufficient",
                detail="Changelog is too short to be useful.",
                severity=Severity.MEDIUM,
            ))
        else:
            report.checks.append(ReleaseCheck(
                name="Changelog",
                status="present",
                detail="Changelog found.",
                severity=Severity.INFO,
            ))

    def _check_semver(self, changes: list[dict[str, Any]], context: dict[str, Any], report: ReleaseReport):
        version = context.get("version", "")
        if not version:
            report.checks.append(ReleaseCheck(
                name="Semantic Version",
                status="missing",
                detail="No version specified.",
                severity=Severity.HIGH,
            ))
        elif not re.match(r"^\d+\.\d+\.\d+", version):
            report.checks.append(ReleaseCheck(
                name="Semantic Version",
                status="invalid",
                detail=f"Version '{version}' does not follow semver.",
                severity=Severity.MEDIUM,
            ))
        else:
            report.checks.append(ReleaseCheck(
                name="Semantic Version",
                status="valid",
                detail=f"Version {version} is valid semver.",
                severity=Severity.INFO,
            ))

    def _check_migration(self, changes: list[dict[str, Any]], context: dict[str, Any], report: ReleaseReport):
        has_migration = any("migration" in str(c).lower() or "schema" in str(c).lower() for c in changes)
        if has_migration:
            report.checks.append(ReleaseCheck(
                name="Migration",
                status="present",
                detail="Database/schema migration changes detected.",
                severity=Severity.INFO,
            ))
        else:
            report.checks.append(ReleaseCheck(
                name="Migration",
                status="not_required",
                detail="No migration changes detected.",
                severity=Severity.INFO,
            ))

    def _check_rollback(self, changes: list[dict[str, Any]], context: dict[str, Any], report: ReleaseReport):
        rollback = context.get("rollback_plan", "")
        if not rollback:
            report.checks.append(ReleaseCheck(
                name="Rollback Plan",
                status="missing",
                detail="No rollback plan provided.",
                severity=Severity.HIGH,
            ))
        else:
            report.checks.append(ReleaseCheck(
                name="Rollback Plan",
                status="present",
                detail="Rollback plan documented.",
                severity=Severity.INFO,
            ))

    def _check_deployment_checklist(self, changes: list[dict[str, Any]], context: dict[str, Any], report: ReleaseReport):
        checklist = context.get("deployment_checklist", [])
        if not checklist:
            report.checks.append(ReleaseCheck(
                name="Deployment Checklist",
                status="missing",
                detail="No deployment checklist provided.",
                severity=Severity.MEDIUM,
            ))
        else:
            report.checks.append(ReleaseCheck(
                name="Deployment Checklist",
                status="present",
                detail=f"{len(checklist)} checklist items found.",
                severity=Severity.INFO,
            ))

    def _check_post_deployment(self, changes: list[dict[str, Any]], context: dict[str, Any], report: ReleaseReport):
        verification = context.get("post_deployment_verification", [])
        if not verification:
            report.checks.append(ReleaseCheck(
                name="Post-Deployment Verification",
                status="missing",
                detail="No post-deployment verification steps.",
                severity=Severity.MEDIUM,
            ))
        else:
            report.checks.append(ReleaseCheck(
                name="Post-Deployment Verification",
                status="present",
                detail=f"{len(verification)} verification steps found.",
                severity=Severity.INFO,
            ))

    def _compute_readiness(self, report: ReleaseReport):
        critical = [c for c in report.checks if c.severity == Severity.CRITICAL]
        high = [c for c in report.checks if c.severity == Severity.HIGH]
        medium = [c for c in report.checks if c.severity == Severity.MEDIUM]

        report.ready = len(critical) == 0 and len(high) == 0

        report.summary = {
            "total_checks": len(report.checks),
            "critical_issues": len(critical),
            "high_issues": len(high),
            "medium_issues": len(medium),
            "ready": report.ready,
        }


release_engineer = ReleaseEngineer()
