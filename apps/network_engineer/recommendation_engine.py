"""
Network Recommendation Engine
================================

Generates prioritized recommendations from analysis findings.
"""

import logging
from typing import Any
from dataclasses import dataclass, field
from enum import Enum

from apps.network_engineer.analyzer import AnalysisIssue, Severity

logger = logging.getLogger(__name__)


class RecommendationPriority(str, Enum):
    P0_CRITICAL = "P0-CRITICAL"
    P1_HIGH = "P1-HIGH"
    P2_MEDIUM = "P2-MEDIUM"
    P3_LOW = "P3-LOW"


@dataclass
class Recommendation:
    problem: str
    why: str
    impact: str
    recommendation: str
    confidence: float
    priority: RecommendationPriority
    references: list[str] = field(default_factory=list)


class RecommendationEngine:
    """Generates prioritized recommendations from analysis findings."""

    async def generate(self, issues: list[AnalysisIssue]) -> list[Recommendation]:
        recommendations = []
        for issue in issues:
            priority = self._map_priority(issue.severity)
            recommendations.append(Recommendation(
                problem=issue.description,
                why=self._explain_why(issue),
                impact=self._assess_impact(issue),
                recommendation=issue.recommendation,
                confidence=issue.confidence,
                priority=priority,
                references=issue.references or [],
            ))
        recommendations.sort(key=lambda r: r.priority)
        return recommendations

    def _map_priority(self, severity: Severity) -> RecommendationPriority:
        mapping = {
            Severity.CRITICAL: RecommendationPriority.P0_CRITICAL,
            Severity.WARNING: RecommendationPriority.P1_HIGH,
            Severity.INFO: RecommendationPriority.P2_MEDIUM,
            Severity.SUGGESTION: RecommendationPriority.P3_LOW,
        }
        return mapping.get(severity, RecommendationPriority.P3_LOW)

    def _explain_why(self, issue: AnalysisIssue) -> str:
        explanations = {
            "Security": "This creates an attack surface that could be exploited by unauthorized users.",
            "Firewall": "Improper firewall rules can allow malicious traffic into the network.",
            "NAT": "NAT misconfigurations can break internet access or expose internal networks.",
            "Performance": "This configuration may limit throughput or increase latency.",
            "Backup": "Without backups, configuration changes cannot be rolled back.",
            "DNS": "DNS misconfigurations can break name resolution.",
            "Routing": "Missing routes can cause traffic blackholes.",
            "Interfaces": "Unused interfaces increase attack surface.",
            "DHCP": "DHCP issues can cause IP conflicts or exhaustion.",
            "Hotspot": "Hotspot misconfigurations can create security vulnerabilities.",
            "Bridge": "Bridge loops can cause network outages.",
            "QoS": "Missing QoS can lead to bandwidth abuse.",
            "System": "System misconfigurations can affect stability.",
            "IP": "IP address issues can cause connectivity problems.",
            "VLAN": "VLAN misconfigurations can cause traffic leakage.",
            "Wireless": "Wireless security issues can expose the network.",
            "PPP": "Unencrypted PPP can expose credentials.",
        }
        return explanations.get(issue.category, "This configuration may cause operational issues.")

    def _assess_impact(self, issue: AnalysisIssue) -> str:
        impacts = {
            "CRITICAL": "Immediate security risk. Network may be compromised.",
            "WARNING": "Potential operational impact. Should be addressed soon.",
            "INFO": "Minor impact. Consider addressing in next maintenance window.",
            "SUGGESTION": "Low impact. Optional optimization.",
        }
        return impacts.get(issue.severity.value.upper(), "Unknown impact.")


recommendation_engine = RecommendationEngine()
