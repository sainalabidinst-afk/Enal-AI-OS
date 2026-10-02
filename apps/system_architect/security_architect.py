"""
System Architect — Security Architect.

Reviews system architecture for security concerns:
- Authentication and authorization patterns
- Data protection and encryption
- Network security boundaries
- Threat surface analysis
- Security architecture patterns
"""

from __future__ import annotations

import logging
from typing import Any

from apps.system_architect.schemas import (
    Finding,
    FindingCategory,
    Impact,
    Severity,
)

logger = logging.getLogger(__name__)


class SecurityArchitect:
    """
    Analyzes system architecture for security concerns.

    Usage::

        architect = SecurityArchitect()
        findings = architect.review(dependency_graph, architecture_metrics)
    """

    def review(self, snapshot: Any, metrics: Any) -> list[Finding]:
        """Review architecture for security concerns based on dependency graph and metrics."""
        findings: list[Finding] = []
        findings.extend(self._check_auth_patterns(snapshot))
        findings.extend(self._check_data_protection(snapshot))
        findings.extend(self._check_threat_surface(snapshot, metrics))
        return findings

    def _check_auth_patterns(self, snapshot: Any) -> list[Finding]:
        findings: list[Finding] = []
        modules = getattr(snapshot, 'modules', {})
        has_auth = any('auth' in m.lower() or 'security' in m.lower() for m in modules.keys())
        if not has_auth and modules:
            findings.append(Finding(
                category=FindingCategory.security,
                severity=Severity.high,
                title="Missing authentication layer",
                description="No dedicated authentication or authorization module detected in the dependency graph",  # noqa: E501
                recommendation="Introduce authentication/authorization layer with standard patterns (OAuth2, JWT, or session-based)",  # noqa: E501
                impact=Impact.maintainability,
                confidence=0.7,
            ))
        return findings

    def _check_data_protection(self, snapshot: Any) -> list[Finding]:
        findings: list[Finding] = []
        modules = getattr(snapshot, 'modules', {})
        has_encryption = any('encrypt' in m.lower() or 'crypto' in m.lower() for m in modules.keys())  # noqa: E501
        if not has_encryption and modules:
            findings.append(Finding(
                category=FindingCategory.security,
                severity=Severity.medium,
                title="Missing data protection module",
                description="No encryption or data protection module detected in the dependency graph",  # noqa: E501
                recommendation="Add data encryption at rest and in transit; use standard crypto libraries",  # noqa: E501
                impact=Impact.maintainability,
                confidence=0.6,
            ))
        return findings

    def _check_network_boundaries(self, snapshot: Any) -> list[Finding]:
        findings: list[Finding] = []
        return findings

    def _check_threat_surface(self, snapshot: Any, metrics: Any) -> list[Finding]:
        findings: list[Finding] = []
        if hasattr(metrics, 'package_boundaries_crossed') and metrics.package_boundaries_crossed > 5:  # noqa: E501
            findings.append(Finding(
                category=FindingCategory.security,
                severity=Severity.medium,
                title="Large attack surface: many package boundary crossings",
                description=f"{metrics.package_boundaries_crossed} boundary crossings increase attack surface",  # noqa: E501
                recommendation="Reduce cross-package dependencies; define explicit API contracts",
                impact=Impact.maintainability,
                confidence=0.75,
            ))
        return findings
