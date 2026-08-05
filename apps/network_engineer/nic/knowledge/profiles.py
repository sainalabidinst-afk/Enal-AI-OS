"""
Compliance Profiles
====================

Cross-vendor compliance profiles (CIS, NIST, PCI DSS, ISP Best Practice, SMB Best Practice).
All profiles operate on Universal AST, making them vendor-agnostic.
"""

import logging

from apps.network_engineer.nic.knowledge.compliance_models import (
    ComplianceCheck,
    ComplianceProfile,
    ComplianceReport,
    ComplianceRule,
)
from apps.network_engineer.nic.knowledge.compliance_checks import CHECK_REGISTRY
from apps.network_engineer.nic.knowledge.compliance_profiles import (
    CISProfile,
    ISPBestPracticeProfile,
    NISTProfile,
    PCIDSSProfile,
    PROFILES,
    SMBBestPracticeProfile,
)
from apps.network_engineer.vendor.models import NetworkAST

logger = logging.getLogger(__name__)

AST_RULE_IDS = {
    "CIS-1.3",
    "CIS-2.1",
    "CIS-2.3",
    "CIS-3.1",
    "CIS-3.2",
    "CIS-4.1",
    "CIS-4.2",
    "NIST-AC-2",
    "NIST-AC-3",
    "NIST-SI-4",
    "NIST-CP-2",
    "PCI-6.1",
    "PCI-10.6",
    "ISP-1.1",
    "ISP-1.2",
    "ISP-2.1",
    "ISP-3.1",
    "ISP-4.1",
    "SMB-1.1",
    "SMB-3.1",
}


class ComplianceEngine:
    """Checks configurations against compliance profiles."""

    def __init__(self, profile_name: str = "CIS"):
        profile = PROFILES.get(profile_name)
        if not profile:
            raise ValueError(f"Unknown compliance profile: {profile_name}")
        self._profile = profile
        self._rules = profile.get_rules()

    @property
    def profile_name(self) -> str:
        return self._profile.name

    def check(self, ast: NetworkAST) -> ComplianceReport:
        """Check AST against compliance rules."""
        report = ComplianceReport(
            device_id=ast.device_id,
            vendor=ast.vendor,
            profile=self._profile.name,
        )
        raw = "\n".join(ast.raw_lines).lower()

        for rule in self._rules:
            check_fn = CHECK_REGISTRY.get(rule.id)
            if check_fn:
                if rule.id in AST_RULE_IDS:
                    check = check_fn(rule, ast)
                else:
                    check = check_fn(rule, raw)
            else:
                check = ComplianceCheck(rule_id=rule.id, rule_name=rule.name, status="skip", detail="Rule not implemented")
            report.checks.append(check)

            if check.status == "pass":
                report.passed += 1
            elif check.status == "fail":
                report.failed += 1
            elif check.status == "warning":
                report.warnings += 1
            else:
                report.skipped += 1

        total = len(self._rules)
        report.score = (report.passed / total * 100) if total > 0 else 0.0
        return report


def get_compliance_engine(profile_name: str = "CIS") -> ComplianceEngine:
    return ComplianceEngine(profile_name)
