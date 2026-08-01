"""
Enterprise Knowledge Module
=============================

Implements RFC-0004 Network Knowledge Expansion:
- Cisco Design Guide: campus, data center, SD-WAN, HA
- MikroTik Best Practice: ISP edge, hotspot, IPv6, FastTrack, admin security
- Fortinet Hardening: FortiOS, policy, VPN, threat protection
- BGP: path selection, filtering, communities, monitoring
- MPLS: forwarding, LDP, VRF, traffic engineering
- IPv6: dual-stack, SLAAC, DHCPv6, transition mechanisms
- Zero Trust: principles, micro-segmentation, ZTNA

All knowledge is integrated into the existing NIC (Network Intelligence Core)
via the EnterpriseKnowledgeEngine. No Core changes required.
"""

from apps.network_engineer.enterprise_knowledge.base import EnterpriseKnowledgeFinding
from apps.network_engineer.enterprise_knowledge.cisco_design_guide import CiscoDesignAnalyzer, cisco_design_analyzer
from apps.network_engineer.enterprise_knowledge.mikrotik_best_practice import MikroTikBestPracticeAnalyzer, mikrotik_bp_analyzer
from apps.network_engineer.enterprise_knowledge.fortinet_hardening import FortinetHardeningAnalyzer, fortinet_hardening_analyzer
from apps.network_engineer.enterprise_knowledge.bgp_analysis import BGPAnalyzer, bgp_analyzer
from apps.network_engineer.enterprise_knowledge.mpls_analysis import MPLSAnalyzer, mpls_analyzer
from apps.network_engineer.enterprise_knowledge.ipv6_analysis import IPv6Analyzer, ipv6_analyzer
from apps.network_engineer.enterprise_knowledge.zero_trust import ZeroTrustAnalyzer, zero_trust_analyzer

__all__ = [
    "EnterpriseKnowledgeFinding",
    "CiscoDesignAnalyzer",
    "MikroTikBestPracticeAnalyzer",
    "FortinetHardeningAnalyzer",
    "BGPAnalyzer",
    "MPLSAnalyzer",
    "IPv6Analyzer",
    "ZeroTrustAnalyzer",
    "cisco_design_analyzer",
    "mikrotik_bp_analyzer",
    "fortinet_hardening_analyzer",
    "bgp_analyzer",
    "mpls_analyzer",
    "ipv6_analyzer",
    "zero_trust_analyzer",
    "EnterpriseKnowledgeEngine",
    "enterprise_knowledge_engine",
]


class EnterpriseKnowledgeEngine:
    """
    Master analyzer that runs all enterprise knowledge modules
    and consolidates findings.
    """

    def __init__(self):
        self._analyzers = [
            cisco_design_analyzer,
            mikrotik_bp_analyzer,
            fortinet_hardening_analyzer,
            bgp_analyzer,
            mpls_analyzer,
            ipv6_analyzer,
            zero_trust_analyzer,
        ]

    def analyze(self, config: object) -> list[EnterpriseKnowledgeFinding]:
        """Run all enterprise knowledge analyzers on a config."""
        all_findings = []
        for analyzer in self._analyzers:
            try:
                findings = analyzer.analyze(config)
                all_findings.extend(findings)
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(
                    "Enterprise knowledge analyzer %s failed: %s",
                    type(analyzer).__name__, e
                )
        return all_findings

    def find_by_domain(self, findings: list[EnterpriseKnowledgeFinding], domain: str) -> list[EnterpriseKnowledgeFinding]:
        """Filter findings by domain."""
        return [f for f in findings if f.domain == domain]

    def find_by_vendor(self, findings: list[EnterpriseKnowledgeFinding], vendor: str) -> list[EnterpriseKnowledgeFinding]:
        """Filter findings by vendor."""
        return [f for f in findings if f.vendor == vendor]


enterprise_knowledge_engine = EnterpriseKnowledgeEngine()
