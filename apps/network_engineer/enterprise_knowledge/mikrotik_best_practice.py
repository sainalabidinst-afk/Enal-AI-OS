"""
MikroTik Best Practice
=======================

ISP edge, hotspot, FastTrack, IPv6 deployment, and secure administrative access
best practices for MikroTik RouterOS.

Reference: MikroTik Official Documentation, RouterOS Best Practices
"""

import logging
from typing import Any

from apps.network_engineer.enterprise_knowledge.base import EnterpriseKnowledgeFinding

logger = logging.getLogger(__name__)


class MikroTikBestPracticeAnalyzer:
    """
    Analyzes MikroTik RouterOS configurations for best practices:
    - ISP edge and PPPoE patterns
    - Hotspot and traffic shaping
    - FastTrack optimization
    - IPv6 deployment on RouterOS
    - Secure administrative access
    """

    def analyze(self, config: object) -> list[EnterpriseKnowledgeFinding]:
        """Analyze MikroTik config for best practices."""
        findings: list[EnterpriseKnowledgeFinding] = []
        raw = "\n".join(getattr(config, "raw_lines", [])).lower()

        vendor = getattr(config, "vendor", "") or ""
        if vendor not in ("mikrotik", "") and vendor != "all":
            return findings

        findings.extend(self._check_isp_edge(raw, config))
        findings.extend(self._check_hotspot_design(raw, config))
        findings.extend(self._check_fasttrack_optimization(raw, config))
        findings.extend(self._check_ipv6_deployment(raw, config))
        findings.extend(self._check_admin_security(raw, config))

        return findings

    def _check_isp_edge(self, raw: str, config: object) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_pppoe = any(kw in raw for kw in ["pppoe", "pppoe-server", "pppoe-client", "ppp profile"])
        has_ppp_encryption = "ppp encrypt" in raw or "encryption" in raw
        has_bgp_peering = any(kw in raw for kw in ["routing bgp", "bgp peer", "remote-as"])
        has_bfd = "bfd" in raw

        if has_pppoe:
            findings.append(EnterpriseKnowledgeFinding(
                domain="mikrotik_best_practice",
                category="isp_edge",
                severity="info",
                description="PPPoE configuration detected",
                recommendation=(
                    "For ISP edge: use PPPoE profile with 'use-encryption=yes', "
                    "set 'max-mtu=1492', and configure rate limiting via queue profiles."
                ),
                confidence=0.85, vendor="mikrotik",
                references=["MikroTik PPPoE Best Practice", "RFC 2516"],
            ))
            if not has_ppp_encryption:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="mikrotik_best_practice",
                    category="isp_edge",
                    severity="warning",
                    description="PPPoE without encryption — user credentials in cleartext",
                    recommendation="Enable PPP encryption (use-encryption=required) in PPP profile.",
                    confidence=0.9, vendor="mikrotik",
                    references=["MikroTik PPP Security Guide"],
                ))

        if has_bgp_peering:
            findings.append(EnterpriseKnowledgeFinding(
                domain="mikrotik_best_practice",
                category="isp_edge",
                severity="info",
                description="BGP peering detected — ISP edge routing",
                recommendation=(
                    "For ISP edge BGP: configure prefix lists for inbound filtering, "
                    "set appropriate local-preference, and use BGP communities for path control."
                ),
                confidence=0.8, vendor="mikrotik",
                references=["MikroTik BGP ISP Peering Guide", "RFC 7454"],
            ))
            if not has_bfd:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="mikrotik_best_practice",
                    category="isp_edge",
                    severity="suggestion",
                    description="BGP without BFD for fast failure detection",
                    recommendation="Enable BFD on BGP peers for sub-second failure detection (< 50ms).",
                    confidence=0.75, vendor="mikrotik",
                    references=["MikroTik BFD Guide", "RFC 5880"],
                ))

        return findings

    def _check_hotspot_design(self, raw: str, config: object) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_hotspot = any(kw in raw for kw in ["ip hotspot", "hotspot", "hotspot profile"])
        has_custom_profile = "hotspot profile" in raw and "default" not in raw
        has_https = "https" in raw or "ssl" in raw
        has_bandwidth = any(kw in raw for kw in ["queue", "limit", "bandwidth"])

        if has_hotspot:
            findings.append(EnterpriseKnowledgeFinding(
                domain="mikrotik_best_practice", category="hotspot", severity="info",
                description="Hotspot configuration detected",
                recommendation="Use custom hotspot profiles with HTTPS redirect and bandwidth management.",
                confidence=0.85, vendor="mikrotik",
                references=["MikroTik Hotspot Best Practice"],
            ))
            if not has_custom_profile:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="mikrotik_best_practice", category="hotspot", severity="warning",
                    description="Hotspot using default profile — limited customization",
                    recommendation="Create a custom hotspot profile with branded login page and bandwidth limits.",
                    confidence=0.8, vendor="mikrotik",
                    references=["MikroTik Custom Hotspot Guide"],
                ))
            if not has_https:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="mikrotik_best_practice", category="hotspot", severity="warning",
                    description="Hotspot without HTTPS — credentials in cleartext",
                    recommendation="Enable HTTPS on hotspot to encrypt login credentials.",
                    confidence=0.9, vendor="mikrotik",
                    references=["MikroTik Hotspot HTTPS Guide"],
                ))
            if not has_bandwidth:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="mikrotik_best_practice", category="hotspot", severity="suggestion",
                    description="Hotspot without per-user bandwidth management",
                    recommendation="Configure per-user bandwidth limits via queue profiles.",
                    confidence=0.7, vendor="mikrotik",
                    references=["MikroTik Bandwidth Management Guide"],
                ))

        return findings

    def _check_fasttrack_optimization(self, raw: str, config: object) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_fasttrack = "fasttrack" in raw
        has_fasttrack_connection = "fasttrack-connection" in raw
        has_firewall_rules = any(kw in raw for kw in ["firewall", "ip firewall", "chain="])

        if has_fasttrack:
            if not has_firewall_rules:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="mikrotik_best_practice", category="fasttrack", severity="warning",
                    description="FastTrack enabled without firewall rules — bypasses security",
                    recommendation=(
                        "FastTrack bypasses connection tracking. Only enable after establishing "
                        "proper firewall policies. Add FastTrack exceptions for sensitive traffic."
                    ),
                    confidence=0.85, vendor="mikrotik",
                    references=["MikroTik FastTrack Guide"],
                ))
            else:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="mikrotik_best_practice", category="fasttrack", severity="info",
                    description="FastTrack enabled with firewall rules",
                    recommendation=(
                        "Verify FastTrack is applied only to trusted traffic. "
                        "Use connection-mark selectors for selective acceleration."
                    ),
                    confidence=0.8, vendor="mikrotik",
                    references=["MikroTik FastTrack Optimization"],
                ))
        else:
            has_nat = any(kw in raw for kw in ["nat", "masquerade", "srcnat"])
            if has_nat:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="mikrotik_best_practice", category="fasttrack", severity="suggestion",
                    description="FastTrack not enabled — potential performance improvement",
                    recommendation="Enable FastTrack to improve NAT throughput by up to 5x.",
                    confidence=0.7, vendor="mikrotik",
                    references=["MikroTik FastTrack Performance Guide"],
                ))

        return findings

    def _check_ipv6_deployment(self, raw: str, config: object) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_ipv6 = any(kw in raw for kw in ["ipv6", "ipv6 address", "ipv6 route"])
        has_ipv6_firewall = "ipv6 firewall" in raw or ("ipv6" in raw and "firewall" in raw)
        has_ipv6_nd = "nd" in raw or "neighbor discovery" in raw

        if has_ipv6:
            findings.append(EnterpriseKnowledgeFinding(
                domain="mikrotik_best_practice", category="ipv6", severity="info",
                description="IPv6 configuration detected",
                recommendation=(
                    "For dual-stack: use SLAAC for end-user devices "
                    "and DHCPv6-PD for prefix delegation to downstream routers."
                ),
                confidence=0.85, vendor="mikrotik",
                references=["MikroTik IPv6 Guide", "RFC 8200", "RFC 8415"],
            ))
            if not has_ipv6_firewall:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="mikrotik_best_practice", category="ipv6", severity="warning",
                    description="IPv6 enabled without IPv6 firewall rules",
                    recommendation=(
                        "IPv6 firewall rules are separate from IPv4. "
                        "Configure '/ipv6 firewall filter' with input, forward, and output chains."
                    ),
                    confidence=0.9, vendor="mikrotik",
                    references=["MikroTik IPv6 Firewall Guide", "RFC 4890"],
                ))
            has_ipv4 = any(kw in raw for kw in ["ip address", "ip route 0.0.0.0"])
            if has_ipv4:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="mikrotik_best_practice", category="ipv6", severity="info",
                    description="Dual-stack (IPv4 + IPv6) deployment detected",
                    recommendation=(
                        "Ensure DNS resolution works for both address families. "
                        "Configure DNS64/NAT64 if some applications only support IPv4."
                    ),
                    confidence=0.75, vendor="mikrotik",
                    references=["RFC 6144", "RFC 6146"],
                ))

        return findings

    def _check_admin_security(self, raw: str, config: object) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_ssh_key = "ssh-key" in raw or "public-key" in raw or "user-keys" in raw
        has_mac_server = "mac-server" in raw or "mac-winbox" in raw
        has_management_acl = "ip services" in raw or "set address" in raw

        if not has_ssh_key:
            findings.append(EnterpriseKnowledgeFinding(
                domain="mikrotik_best_practice", category="admin_security", severity="warning",
                description="SSH key authentication not configured — password-only login",
                recommendation=(
                    "Configure SSH public key authentication for administrative access. "
                    "Use '/user ssh-keys import' to add public keys. "
                    "Disable password-based SSH after keys are deployed."
                ),
                confidence=0.8, vendor="mikrotik",
                references=["MikroTik SSH Key Management"],
            ))

        if has_mac_server:
            findings.append(EnterpriseKnowledgeFinding(
                domain="mikrotik_best_practice", category="admin_security", severity="warning",
                description="MAC server (Winbox over MAC) enabled — local network risk",
                recommendation=(
                    "Disable MAC server on WAN interfaces. "
                    "Use '/tool mac-server set allowed-interface-list=LAN' to restrict access."
                ),
                confidence=0.85, vendor="mikrotik",
                references=["MikroTik MAC Server Security"],
            ))

        if "neighbor discovery" in raw or "ip neighbor discovery" in raw:
            findings.append(EnterpriseKnowledgeFinding(
                domain="mikrotik_best_practice", category="admin_security", severity="suggestion",
                description="MikroTik Neighbor Discovery enabled",
                recommendation=(
                    "Disable Neighbor Discovery on WAN interfaces for security. "
                    "Use '/ip neighbor discovery-settings set discover-interface-list=LAN'."
                ),
                confidence=0.7, vendor="mikrotik",
                references=["MikroTik Neighbor Discovery Security"],
            ))

        if not has_management_acl:
            findings.append(EnterpriseKnowledgeFinding(
                domain="mikrotik_best_practice", category="admin_security", severity="warning",
                description="No IP service access restrictions — all services open",
                recommendation=(
                    "Restrict management services to specific IP addresses. "
                    "Use '/ip services set winbox address=10.0.0.0/24' and similar for SSH, API."
                ),
                confidence=0.85, vendor="mikrotik",
                references=["MikroTik Service Hardening Guide"],
            ))

        return findings


mikrotik_bp_analyzer = MikroTikBestPracticeAnalyzer()
