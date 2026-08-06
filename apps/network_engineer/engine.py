"""
Network Engineer Engine
=======================

Domain engine orchestrator for the Network Engineer Capability Pack.

Orchestrates:
    1. Configuration parsing and validation
    2. Security analysis
    3. Topology inference
    4. Design review
    5. Troubleshooting
    6. Migration planning
    7. Advisory

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
from typing import Any

from apps.network_engineer.analyzer import NetworkAnalyzer
from apps.network_engineer.analyzer_security import SecurityAnalyzer
from apps.network_engineer.topology import TopologyAnalyzer
from apps.network_engineer.design_review import DesignReviewEngine
from apps.network_engineer.troubleshooting import TroubleshootingEngine
from apps.network_engineer.migration_planner import MigrationPlanner
from apps.network_engineer.advisor import NetworkAdvisor
from apps.network_engineer.risk_scorer import RiskScorer

logger = logging.getLogger(__name__)


class NetworkEngineerEngine:
    """
    Orchestrates the full network engineering pipeline.

    Public API::

        engine = NetworkEngineerEngine()
        result = engine.audit(config_text, vendor="mikrotik")
        result = engine.review_design(topology_json)
    """

    def __init__(self) -> None:
        self.analyzer = NetworkAnalyzer()
        self.security_analyzer = SecurityAnalyzer()
        self.topology_analyzer = TopologyAnalyzer()
        self.design_review = DesignReviewEngine()
        self.troubleshooting = TroubleshootingEngine()
        self.migration_planner = MigrationPlanner()
        self.advisor = NetworkAdvisor()
        self.risk_scorer = RiskScorer()

    def audit(self, config: str, vendor: str = "auto-detect") -> dict[str, Any]:
        """Run full security and best-practice audit on a network config."""
        parsed = self.analyzer.parse(config, vendor=vendor)
        security_findings = self.security_analyzer.analyze(parsed)
        best_practice_findings = self.analyzer.analyze_best_practices(parsed)
        risk_score = self.risk_scorer.calculate(
            security_findings + best_practice_findings
        )
        return {
            "vendor": vendor,
            "parsed": parsed,
            "issues": security_findings + best_practice_findings,
            "risk_score": risk_score,
            "summary": self._build_summary(security_findings + best_practice_findings),
        }

    def analyze_topology(self, config: str, vendor: str = "auto-detect") -> dict[str, Any]:
        """Infer network topology from configuration."""
        parsed = self.analyzer.parse(config, vendor=vendor)
        return self.topology_analyzer.infer(parsed)

    def review_design(self, topology_json: dict[str, Any]) -> dict[str, Any]:
        """Run design review on a network topology."""
        return self.design_review.review(topology_json)

    def troubleshoot(self, symptom: str, evidence: list[str] | None = None) -> dict[str, Any]:
        """Run structured troubleshooting workflow."""
        return self.troubleshooting.analyze(symptom, evidence or [])

    def plan_migration(
        self,
        source_vendor: str,
        target_vendor: str,
        requirements: dict[str, Any],
    ) -> dict[str, Any]:
        """Plan cross-vendor migration with risk assessment."""
        return self.migration_planner.plan(
            source_vendor=source_vendor,
            target_vendor=target_vendor,
            requirements=requirements,
        )

    def advise(self, query: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Provide network design advisory."""
        return self.advisor.propose(query, context or {})

    def _build_summary(self, findings: list[dict[str, Any]]) -> dict[str, Any]:
        """Build summary statistics from findings."""
        severity_counts: dict[str, int] = {}
        for finding in findings:
            sev = finding.get("severity", "info")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
        return {
            "total_findings": len(findings),
            "severity_breakdown": severity_counts,
        }
