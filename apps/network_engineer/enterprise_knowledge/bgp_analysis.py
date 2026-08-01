"""
BGP Analysis
=============

BGP path selection, route filtering, communities, monitoring,
and troubleshooting analysis.

Reference: RFC 4271, RFC 1997, RFC 7454, Cisco BGP Best Practices
"""

import logging
from typing import Any

from apps.network_engineer.enterprise_knowledge.base import EnterpriseKnowledgeFinding

logger = logging.getLogger(__name__)


class BGPAnalyzer:
    """
    BGP configuration analysis:
    - BGP path selection
    - Route filtering and manipulation
    - BGP communities
    - RR/CE design patterns
    - BGP monitoring and troubleshooting
    """

    def analyze(self, config: object) -> list[EnterpriseKnowledgeFinding]:
        findings: list[EnterpriseKnowledgeFinding] = []
        raw = "\n".join(getattr(config, "raw_lines", [])).lower()
        vendor = getattr(config, "vendor", "") or ""
        has_bgp = any(kw in raw for kw in ["router bgp", "routing bgp", "bgp"])

        if not has_bgp:
            return findings

        findings.extend(self._check_path_selection(raw, config, vendor))
        findings.extend(self._check_route_filtering(raw, config, vendor))
        findings.extend(self._check_communities(raw, config, vendor))
        findings.extend(self._check_route_reflector(raw, config, vendor))
        findings.extend(self._check_monitoring(raw, config, vendor))

        return findings

    def _check_path_selection(self, raw: str, config: object, vendor: str) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_weight = "weight" in raw or "set-weight" in raw or "local-preference" in raw
        has_local_pref = "local-preference" in raw or "set local-preference" in raw
        has_as_path = "as-path" in raw or "prepend" in raw or "as-path-prepend" in raw
        has_med = "med" in raw or "metric-out" in raw or "multi-exit-disc" in raw

        if not has_weight and not has_local_pref:
            findings.append(EnterpriseKnowledgeFinding(
                domain="bgp_analysis", category="path_selection", severity="warning",
                description="No BGP path selection attributes configured — using default best-path selection",
                recommendation=(
                    "Configure local-preference for outbound path selection (higher is preferred). "
                    "Use weight for fine-grained control on single router."
                ),
                confidence=0.8, vendor=vendor,
                references=["RFC 4271 Section 9.1", "BGP Best Path Selection Algorithm"],
            ))
        if not has_med:
            findings.append(EnterpriseKnowledgeFinding(
                domain="bgp_analysis", category="path_selection", severity="suggestion",
                description="MED (Multi-Exit Discriminator) not configured for inbound path selection",
                recommendation=(
                    "Use MED (lower is preferred) to influence inbound traffic from AS peers. "
                    "Set MED in route-maps for granular control."
                ),
                confidence=0.7, vendor=vendor,
                references=["RFC 4451", "BGP MED Best Practices"],
            ))
        if not has_as_path:
            findings.append(EnterpriseKnowledgeFinding(
                domain="bgp_analysis", category="path_selection", severity="suggestion",
                description="AS-path prepending not configured for backup path selection",
                recommendation=(
                    "Use AS-path prepending to make a path less preferred for backup routing. "
                    "Add 'set as-path prepend' in route-map for outbound policies."
                ),
                confidence=0.65, vendor=vendor,
                references=["BGP AS-Path Prepending Guide"],
            ))
        return findings

    def _check_route_filtering(self, raw: str, config: object, vendor: str) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_prefix_list = any(kw in raw for kw in ["prefix-list", "prefix-list", "ip prefix-list"])
        has_filter_list = "filter-list" in raw or "as-path-filter" in raw
        has_distribute = "distribute-list" in raw or "route-map" in raw
        has_max_prefix = "maximum-prefix" in raw or "max-prefix" in raw

        if not has_prefix_list:
            findings.append(EnterpriseKnowledgeFinding(
                domain="bgp_analysis", category="route_filtering", severity="warning",
                description="No BGP prefix-list filtering — accepting all routes from peers",
                recommendation=(
                    "Configure prefix-lists to filter BGP prefixes from peers. "
                    "Use 'ip prefix-list' to allow only required prefixes per peer."
                ),
                confidence=0.9, vendor=vendor,
                references=["RFC 7454 Section 3", "BGP Route Filtering Best Practices"],
            ))
        if not has_max_prefix:
            findings.append(EnterpriseKnowledgeFinding(
                domain="bgp_analysis", category="route_filtering", severity="warning",
                description="Maximum-prefix limit not configured — risk of memory exhaustion",
                recommendation=(
                    "Set maximum-prefix limit per BGP peer to prevent route table overflow. "
                    "Use 'neighbor maximum-prefix 1000 restart 60'."
                ),
                confidence=0.85, vendor=vendor,
                references=["RFC 7454 Section 4", "BGP Prefix Limit Best Practices"],
            ))
        if not has_distribute:
            findings.append(EnterpriseKnowledgeFinding(
                domain="bgp_analysis", category="route_filtering", severity="info",
                description="Basic route filtering configured",
                recommendation=(
                    "Enhance filtering with route-maps for policy-based control. "
                    "Use match conditions on AS-path, community, and prefix-list."
                ),
                confidence=0.7, vendor=vendor,
                references=["BGP Route-Map Configuration Guide"],
            ))
        return findings

    def _check_communities(self, raw: str, config: object, vendor: str) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_community = "community" in raw or "set community" in raw
        has_comm_list = "community-list" in raw or "ip community-list" in raw
        has_comm_action = any(kw in raw for kw in ["no-export", "no-advertise", "local-as"])

        if has_community:
            findings.append(EnterpriseKnowledgeFinding(
                domain="bgp_analysis", category="communities", severity="info",
                description="BGP communities configured for route tagging",
                recommendation=(
                    "Use well-known communities (no-export, no-advertise, local-as) "
                    "for route scope control. Define custom communities for path selection."
                ),
                confidence=0.8, vendor=vendor,
                references=["RFC 1997", "RFC 8092"],
            ))
            if not has_comm_list:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="bgp_analysis", category="communities", severity="suggestion",
                    description="BGP community filtering not configured",
                    recommendation=(
                        "Configure community-list for route filtering based on community tags. "
                        "Use 'ip community-list standard' for matching."
                    ),
                    confidence=0.7, vendor=vendor,
                    references=["BGP Community Filtering Guide"],
                ))
        else:
            findings.append(EnterpriseKnowledgeFinding(
                domain="bgp_analysis", category="communities", severity="suggestion",
                description="BGP communities not configured — limited route tagging",
                recommendation=(
                    "Use BGP communities for route tagging and policy-based control. "
                    "Define community values for different route types."
                ),
                confidence=0.6, vendor=vendor,
                references=["RFC 1997", "BGP Community Design Guide"],
            ))
        return findings

    def _check_route_reflector(self, raw: str, config: object, vendor: str) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        is_rr_client = "route-reflector-client" in raw or "rr-client" in raw or "cluster-id" in raw
        has_cluster = "cluster-id" in raw or "bgp cluster-id" in raw
        has_client_to_client = "client-to-client" in raw or "rr-client-to-client" in raw

        if is_rr_client:
            findings.append(EnterpriseKnowledgeFinding(
                domain="bgp_analysis", category="route_reflector", severity="info",
                description="BGP Route Reflector configuration detected",
                recommendation=(
                    "Ensure cluster-id is unique per RR to prevent routing loops. "
                    "For redundancy, deploy multiple RRs with same cluster-id."
                ),
                confidence=0.85, vendor=vendor,
                references=["RFC 4456", "BGP Route Reflector Design"],
            ))
            if not has_cluster:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="bgp_analysis", category="route_reflector", severity="warning",
                    description="BGP RR without cluster-id — potential routing loop risk",
                    recommendation=(
                        "Configure cluster-id on route reflector: "
                        "'bgp cluster-id <id>' to prevent loop detection issues."
                    ),
                    confidence=0.85, vendor=vendor,
                    references=["RFC 4456 Section 4", "BGP RR Cluster-ID Design"],
                ))
        return findings

    def _check_monitoring(self, raw: str, config: object, vendor: str) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_keepalive = "timers" in raw or "keepalive" in raw or "hold-time" in raw
        has_log_neighbor = any(kw in raw for kw in ["log-neighbor-changes", "log-updates", "bgp log"])
        has_bfd = "bfd" in raw

        if not has_keepalive:
            findings.append(EnterpriseKnowledgeFinding(
                domain="bgp_analysis", category="monitoring", severity="suggestion",
                description="BGP timers not configured — using defaults",
                recommendation=(
                    "Configure BGP timers for faster convergence: "
                    "keepalive 30, hold 90 (or keepalive 10, hold 30 for critical peers)."
                ),
                confidence=0.7, vendor=vendor,
                references=["BGP Timer Tuning Guide"],
            ))
        if not has_log_neighbor:
            findings.append(EnterpriseKnowledgeFinding(
                domain="bgp_analysis", category="monitoring", severity="warning",
                description="BGP neighbor logging not configured",
                recommendation=(
                    "Enable 'bgp log-neighbor-changes' to track neighbor state changes "
                    "for troubleshooting and audit."
                ),
                confidence=0.85, vendor=vendor,
                references=["BGP Neighbor Logging Best Practices"],
            ))
        if not has_bfd:
            findings.append(EnterpriseKnowledgeFinding(
                domain="bgp_analysis", category="monitoring", severity="suggestion",
                description="BFD not configured for BGP — slow failure detection",
                recommendation=(
                    "Enable BFD on BGP sessions for sub-second failure detection. "
                    "BFD provides < 50ms convergence vs 30s+ default hold timer."
                ),
                confidence=0.75, vendor=vendor,
                references=["RFC 5880", "BGP BFD Integration Guide"],
            ))
        return findings


bgp_analyzer = BGPAnalyzer()
