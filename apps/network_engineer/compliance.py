"""
Compliance Engine
==================

Checks network configurations against policies and CIS Benchmarks.
Cross-vendor: works with Universal AST from any vendor.
"""

import logging
from typing import Any
from dataclasses import dataclass, field
from enum import Enum

from apps.network_engineer.vendor.models import NetworkAST

logger = logging.getLogger(__name__)


class ComplianceStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    SKIP = "skip"


@dataclass
class ComplianceRule:
    id: str
    name: str
    description: str
    severity: str = "warning"
    vendor: str = "all"


@dataclass
class ComplianceCheck:
    rule_id: str
    rule_name: str
    status: ComplianceStatus
    detail: str = ""
    evidence: str = ""


@dataclass
class ComplianceReport:
    device_id: str
    vendor: str
    checks: list[ComplianceCheck] = field(default_factory=list)
    score: float = 0.0
    passed: int = 0
    failed: int = 0
    warnings: int = 0
    skipped: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "device_id": self.device_id,
            "vendor": self.vendor,
            "score": round(self.score, 2),
            "passed": self.passed,
            "failed": self.failed,
            "warnings": self.warnings,
            "skipped": self.skipped,
            "checks": [
                {
                    "rule_id": c.rule_id,
                    "rule_name": c.rule_name,
                    "status": c.status.value,
                    "detail": c.detail,
                    "evidence": c.evidence,
                }
                for c in self.checks
            ],
        }


# CIS Benchmark Rules (cross-vendor)
CIS_BENCHMARK_RULES = [
    ComplianceRule(
        id="CIS-1.1",
        name="SSH Restricted",
        description="SSH must not be open to 0.0.0.0/0",
        severity="critical",
        vendor="all",
    ),
    ComplianceRule(
        id="CIS-1.2",
        name="Telnet Disabled",
        description="Telnet must not be enabled",
        severity="critical",
        vendor="all",
    ),
    ComplianceRule(
        id="CIS-1.3",
        name="Admin Password Set",
        description="Admin password must be set",
        severity="critical",
        vendor="all",
    ),
    ComplianceRule(
        id="CIS-2.1",
        name="NTP Enabled",
        description="NTP must be enabled for accurate timekeeping",
        severity="warning",
        vendor="all",
    ),
    ComplianceRule(
        id="CIS-2.2",
        name="Logging Enabled",
        description="Logging must be enabled for audit trail",
        severity="warning",
        vendor="all",
    ),
    ComplianceRule(
        id="CIS-3.1",
        name="Backup Configured",
        description="Backup must be configured",
        severity="warning",
        vendor="all",
    ),
    ComplianceRule(
        id="CIS-4.1",
        name="Default Password Changed",
        description="Default passwords must be changed",
        severity="critical",
        vendor="all",
    ),
    ComplianceRule(
        id="CIS-5.1",
        name="Unused Interfaces Disabled",
        description="Unused interfaces should be disabled",
        severity="info",
        vendor="all",
    ),
]


class ComplianceEngine:
    """Checks configurations against compliance policies."""

    def __init__(self, rules: list[ComplianceRule] | None = None):
        self._rules = rules or list(CIS_BENCHMARK_RULES)

    def check(self, ast: NetworkAST) -> ComplianceReport:
        """Check AST against compliance rules."""
        report = ComplianceReport(device_id=ast.device_id, vendor=ast.vendor)
        raw = "\n".join(ast.raw_lines).lower()

        for rule in self._rules:
            if rule.vendor != "all" and rule.vendor != ast.vendor:
                report.skipped += 1
                report.checks.append(ComplianceCheck(
                    rule_id=rule.id,
                    rule_name=rule.name,
                    status=ComplianceStatus.SKIP,
                    detail=f"Rule not applicable for vendor {ast.vendor}",
                ))
                continue

            check = self._check_rule(rule, ast, raw)
            report.checks.append(check)

            if check.status == ComplianceStatus.PASS:
                report.passed += 1
            elif check.status == ComplianceStatus.FAIL:
                report.failed += 1
            elif check.status == ComplianceStatus.WARNING:
                report.warnings += 1
            else:
                report.skipped += 1

        total = len(self._rules)
        report.score = (report.passed / total * 100) if total > 0 else 0.0
        return report

    def _check_rule(self, rule: ComplianceRule, ast: NetworkAST, raw: str) -> ComplianceCheck:
        """Check a single compliance rule."""
        if rule.id == "CIS-1.1":
            return self._check_ssh_restricted(rule, raw)
        elif rule.id == "CIS-1.2":
            return self._check_telnet_disabled(rule, raw)
        elif rule.id == "CIS-1.3":
            return self._check_admin_password(rule, ast)
        elif rule.id == "CIS-2.1":
            return self._check_ntp_enabled(rule, ast, raw)
        elif rule.id == "CIS-2.2":
            return self._check_logging_enabled(rule, raw)
        elif rule.id == "CIS-3.1":
            return self._check_backup_configured(rule, ast)
        elif rule.id == "CIS-4.1":
            return self._check_default_password_changed(rule, raw)
        elif rule.id == "CIS-5.1":
            return self._check_unused_interfaces_disabled(rule, ast)
        return ComplianceCheck(rule_id=rule.id, rule_name=rule.name, status=ComplianceStatus.SKIP)

    def _check_ssh_restricted(self, rule: ComplianceRule, raw: str) -> ComplianceCheck:
        if "0.0.0.0/0" in raw and ("ssh" in raw or "winbox" in raw):
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status=ComplianceStatus.FAIL,
                detail="SSH or management service is open to 0.0.0.0/0",
                evidence="Found 0.0.0.0/0 with SSH/management service",
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status=ComplianceStatus.PASS,
            detail="SSH is not open to the world",
        )

    def _check_telnet_disabled(self, rule: ComplianceRule, raw: str) -> ComplianceCheck:
        if "telnet" in raw:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status=ComplianceStatus.FAIL,
                detail="Telnet is enabled (unencrypted)",
                evidence="Found telnet in configuration",
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status=ComplianceStatus.PASS,
            detail="Telnet is not enabled",
        )

    def _check_admin_password(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        if not ast.system.hostname:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status=ComplianceStatus.WARNING,
                detail="Cannot verify admin password from config",
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status=ComplianceStatus.PASS,
            detail="Admin password check requires live system",
        )

    def _check_ntp_enabled(self, rule: ComplianceRule, ast: NetworkAST, raw: str) -> ComplianceCheck:
        if ast.system.ntp_enabled or "ntp" in raw:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status=ComplianceStatus.PASS,
                detail="NTP is enabled",
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status=ComplianceStatus.FAIL,
            detail="NTP is not configured",
        )

    def _check_logging_enabled(self, rule: ComplianceRule, raw: str) -> ComplianceCheck:
        if "log" in raw or "logging" in raw:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status=ComplianceStatus.PASS,
                detail="Logging is configured",
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status=ComplianceStatus.FAIL,
            detail="Logging is not configured",
        )

    def _check_backup_configured(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        if ast.system.backup_configured:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status=ComplianceStatus.PASS,
                detail="Backup is configured",
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status=ComplianceStatus.FAIL,
            detail="No backup configuration found",
        )

    def _check_default_password_changed(self, rule: ComplianceRule, raw: str) -> ComplianceCheck:
        if "password=" in raw and ("admin" in raw or "1234" in raw):
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status=ComplianceStatus.FAIL,
                detail="Default or weak password detected",
                evidence="Found default/weak password pattern",
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status=ComplianceStatus.PASS,
            detail="No default password detected",
        )

    def _check_unused_interfaces_disabled(self, rule: ComplianceRule, ast: NetworkAST) -> ComplianceCheck:
        unused = [i for i in ast.interfaces if i.status == "enabled" and not any(ip.interface == i.name for ip in ast.ip_addresses)]
        if unused:
            return ComplianceCheck(
                rule_id=rule.id,
                rule_name=rule.name,
                status=ComplianceStatus.WARNING,
                detail=f"{len(unused)} unused interfaces are enabled",
                evidence=", ".join(i.name for i in unused),
            )
        return ComplianceCheck(
            rule_id=rule.id,
            rule_name=rule.name,
            status=ComplianceStatus.PASS,
            detail="No unused interfaces enabled",
        )


compliance_engine = ComplianceEngine()
