"""
MPLS Analysis
==============

MPLS forwarding, LDP, VRF, traffic engineering, and service provider edge patterns.

Reference: RFC 3031, RFC 5036, RFC 4364, MPLS Best Practices
"""

import logging
from typing import Any

from apps.network_engineer.enterprise_knowledge.base import EnterpriseKnowledgeFinding

logger = logging.getLogger(__name__)


class MPLSAnalyzer:
    """
    MPLS configuration analysis:
    - MPLS forwarding and labels
    - LDP configuration
    - VRF and route leaking
    - MPLS traffic engineering
    - Service provider edge patterns
    """

    def analyze(self, config: object) -> list[EnterpriseKnowledgeFinding]:
        findings: list[EnterpriseKnowledgeFinding] = []
        raw = "\n".join(getattr(config, "raw_lines", [])).lower()
        vendor = getattr(config, "vendor", "") or ""
        has_mpls = any(kw in raw for kw in ["mpls", "ldp", "label", "vrf"])

        if not has_mpls:
            return findings

        findings.extend(self._check_mpls_forwarding(raw, config, vendor))
        findings.extend(self._check_ldp_config(raw, config, vendor))
        findings.extend(self._check_vrf_config(raw, config, vendor))
        findings.extend(self._check_traffic_engineering(raw, config, vendor))
        findings.extend(self._check_sp_edge(raw, config, vendor))

        return findings

    def _check_mpls_forwarding(self, raw: str, config: object, vendor: str) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_mpls_ip = "mpls ip" in raw or "mpls label" in raw
        has_mtu = "mtu" in raw and "mpls" in raw
        has_ttl = "ttl" in raw and "mpls" in raw

        if has_mpls_ip:
            findings.append(EnterpriseKnowledgeFinding(
                domain="mpls_analysis", category="forwarding", severity="info",
                description="MPLS forwarding enabled",
                recommendation=(
                    "Ensure MPLS MTU is configured (typically 1508-1520 bytes for L2 header). "
                    "Set 'mpls mtu 1508' on all MPLS-enabled interfaces."
                ),
                confidence=0.8, vendor=vendor,
                references=["RFC 3031", "RFC 3032", "MPLS MTU Planning Guide"],
            ))
            if not has_mtu:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="mpls_analysis", category="forwarding", severity="warning",
                    description="MPLS MTU not configured — packet fragmentation risk",
                    recommendation=(
                        "Configure MPLS MTU on all interfaces. "
                        "Set 'mpls mtu 1508' for MPLS-enabled interfaces."
                    ),
                    confidence=0.8, vendor=vendor,
                    references=["MPLS MTU Best Practices"],
                ))
        return findings

    def _check_ldp_config(self, raw: str, config: object, vendor: str) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_ldp = "mpls ldp" in raw or "ldp" in raw
        has_ldp_auth = "ldp password" in raw or "ldp md5" in raw or "ldp auth" in raw
        has_ldp_transport = "transport-address" in raw or "ldp router-id" in raw
        has_ldp_session = "session protection" in raw or "ldp session" in raw

        if has_ldp:
            findings.append(EnterpriseKnowledgeFinding(
                domain="mpls_analysis", category="ldp", severity="info",
                description="LDP configured for label distribution",
                recommendation=(
                    "Use transport-address interface for LDP discovery. "
                    "Enable session protection for LDP session resilience."
                ),
                confidence=0.85, vendor=vendor,
                references=["RFC 5036", "LDP Configuration Guide"],
            ))
            if not has_ldp_auth:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="mpls_analysis", category="ldp", severity="warning",
                    description="LDP without authentication — spoofing risk",
                    recommendation=(
                        "Enable LDP MD5 authentication for neighbor session security. "
                        "Use 'mpls ldp neighbor <ip> password <key>'."
                    ),
                    confidence=0.85, vendor=vendor,
                    references=["RFC 5036 Section 2.7", "LDP Security Best Practices"],
                ))
            if not has_ldp_transport:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="mpls_analysis", category="ldp", severity="suggestion",
                    description="LDP transport-address not configured",
                    recommendation=(
                        "Set LDP transport address to loopback interface for stability. "
                        "Use 'mpls ldp transport-address interface loopback0'."
                    ),
                    confidence=0.75, vendor=vendor,
                    references=["LDP Transport Address Best Practices"],
                ))
        return findings

    def _check_vrf_config(self, raw: str, config: object, vendor: str) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_vrf = "vrf definition" in raw or "ip vrf" in raw or "vrf" in raw
        has_rd = "rd " in raw or "route-distinguisher" in raw
        has_rt = "route-target" in raw or "rt " in raw
        has_vrf_leaking = "import" in raw and "export" in raw and "vrf" in raw

        if has_vrf:
            findings.append(EnterpriseKnowledgeFinding(
                domain="mpls_analysis", category="vrf", severity="info",
                description="VRF (VPN Routing and Forwarding) configured",
                recommendation=(
                    "Ensure RD (Route Distinguisher) is unique per VRF. "
                    "Use RT (Route Target) for import/export policy control."
                ),
                confidence=0.85, vendor=vendor,
                references=["RFC 4364", "RFC 4659", "MPLS L3VPN Design Guide"],
            ))
            if not has_rd:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="mpls_analysis", category="vrf", severity="warning",
                    description="VRF without Route Distinguisher (RD) — incomplete MPLS VPN config",
                    recommendation=(
                        "Configure RD for each VRF to make routes globally unique. "
                        "Format: 'rd <ASN>:<nn>' or 'rd <IP>:<nn>'."
                    ),
                    confidence=0.9, vendor=vendor,
                    references=["RFC 4364 Section 4.2"],
                ))
            if not has_rt:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="mpls_analysis", category="vrf", severity="warning",
                    description="VRF without Route Target (RT) — no VPN route propagation",
                    recommendation=(
                        "Configure RT (route-target) for import/export of VPN routes. "
                        "Use 'route-target both <value>' for symmetrical routing."
                    ),
                    confidence=0.9, vendor=vendor,
                    references=["RFC 4364 Section 4.3"],
                ))
        return findings

    def _check_traffic_engineering(self, raw: str, config: object, vendor: str) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_te = "mpls traffic-eng" in raw or "traffic-engineering" in raw or "mpls te" in raw
        has_rsvp = "rsvp" in raw or "rsvp-te" in raw
        has_tunnel = "tunnel" in raw and "mpls" in raw

        if has_te:
            findings.append(EnterpriseKnowledgeFinding(
                domain="mpls_analysis", category="traffic_engineering", severity="info",
                description="MPLS Traffic Engineering configured",
                recommendation=(
                    "Use RSVP-TE for bandwidth reservation. "
                    "Configure tunnel interfaces with explicit paths for traffic steering."
                ),
                confidence=0.85, vendor=vendor,
                references=["RFC 3209", "MPLS TE Design Guide"],
            ))
            if not has_rsvp:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="mpls_analysis", category="traffic_engineering", severity="warning",
                    description="MPLS TE without RSVP — no bandwidth reservation",
                    recommendation=(
                        "Enable RSVP-TE as the signaling protocol for MPLS TE. "
                        "Use 'mpls traffic-eng tunnels' and 'ip rsvp bandwidth'."
                    ),
                    confidence=0.8, vendor=vendor,
                    references=["RFC 3209", "RSVP-TE Configuration Guide"],
                ))
        return findings

    def _check_sp_edge(self, raw: str, config: object, vendor: str) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_pe = "pe" in raw or "provider-edge" in raw
        has_ce = "ce" in raw or "customer-edge" in raw or "vrf" in raw
        has_bgp_l3vpn = "bgp" in raw and ("vpnv4" in raw or "vpnv6" in raw or "l3vpn" in raw)

        if has_bgp_l3vpn:
            findings.append(EnterpriseKnowledgeFinding(
                domain="mpls_analysis", category="sp_edge", severity="info",
                description="BGP L3VPN (MPLS VPN) detected — service provider edge pattern",
                recommendation=(
                    "Verify MP-BGP address-family vpnv4/vpnv6 configuration. "
                    "Ensure route-target filtering matches customer requirements."
                ),
                confidence=0.85, vendor=vendor,
                references=["RFC 4364", "MPLS L3VPN Service Provider Guide"],
            ))
        if has_pe and has_ce:
            findings.append(EnterpriseKnowledgeFinding(
                domain="mpls_analysis", category="sp_edge", severity="info",
                description="PE-CE routing pattern detected",
                recommendation=(
                    "Use PE-CE routing (static, RIP, OSPF, BGP, EIGRP) for customer edge. "
                    "Use VRF-lite for smaller deployments."
                ),
                confidence=0.75, vendor=vendor,
                references=["MPLS L3VPN PE-CE Routing Guide"],
            ))
        return findings


mpls_analyzer = MPLSAnalyzer()
