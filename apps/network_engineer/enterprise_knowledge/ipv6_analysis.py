"""
IPv6 Analysis
==============

IPv6 addressing, dual-stack, SLAAC, DHCPv6, security, and transition mechanisms.

Reference: RFC 8200, RFC 4861, RFC 4862, RFC 8415, RFC 6144
"""

import logging
from typing import Any

from apps.network_engineer.enterprise_knowledge.base import EnterpriseKnowledgeFinding

logger = logging.getLogger(__name__)


class IPv6Analyzer:
    """
    IPv6 configuration analysis:
    - Dual-stack design
    - SLAAC vs DHCPv6
    - IPv6 security considerations
    - Transition mechanisms
    - ISP IPv6 deployment patterns
    """

    def analyze(self, config: object) -> list[EnterpriseKnowledgeFinding]:
        findings: list[EnterpriseKnowledgeFinding] = []
        raw = "\n".join(getattr(config, "raw_lines", [])).lower()
        vendor = getattr(config, "vendor", "") or ""
        has_ipv6 = any(kw in raw for kw in ["ipv6", "ipv6 address", "ipv6 route"])

        if not has_ipv6:
            return findings

        findings.extend(self._check_dual_stack(raw, config, vendor))
        findings.extend(self._check_addressing(raw, config, vendor))
        findings.extend(self._check_security(raw, config, vendor))
        findings.extend(self._check_transition(raw, config, vendor))
        findings.extend(self._check_isp_deployment(raw, config, vendor))

        return findings

    def _check_dual_stack(self, raw: str, config: object, vendor: str) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_ipv4 = any(kw in raw for kw in ["ip address", "ip route 0.0.0.0"])
        has_ipv6_route = "ipv6 route" in raw or "ipv6 address" in raw

        if has_ipv4 and has_ipv6_route:
            findings.append(EnterpriseKnowledgeFinding(
                domain="ipv6_analysis", category="dual_stack", severity="info",
                description="Dual-stack (IPv4 + IPv6) deployment detected",
                recommendation=(
                    "Ensure DNS resolution works for both families. "
                    "Verify that applications prefer IPv6 when available. "
                    "Monitor both stacks for connectivity and performance."
                ),
                confidence=0.85, vendor=vendor,
                references=["RFC 4213", "RFC 4038", "Dual-Stack Deployment Guide"],
            ))
        elif has_ipv6_route and not has_ipv4:
            findings.append(EnterpriseKnowledgeFinding(
                domain="ipv6_analysis", category="dual_stack", severity="info",
                description="IPv6-only deployment detected",
                recommendation=(
                    "Ensure IPv6-only applications are compatible. "
                    "Consider DNS64/NAT64 for legacy IPv4-only services."
                ),
                confidence=0.75, vendor=vendor,
                references=["RFC 6144", "IPv6-Only Network Design"],
            ))
        return findings

    def _check_addressing(self, raw: str, config: object, vendor: str) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_slaac = any(kw in raw for kw in ["slaac", "autoconfig", "ipv6 nd ra"])
        has_dhcpv6 = any(kw in raw for kw in ["dhcpv6", "dhcp6", "ipv6 dhcp"])
        has_dhcp_pd = "dhcpv6-pd" in raw or "prefix-delegation" in raw or "pd " in raw
        has_ula = "fc" in raw or "fd" in raw or "unique-local" in raw

        if has_slaac:
            findings.append(EnterpriseKnowledgeFinding(
                domain="ipv6_analysis", category="addressing", severity="info",
                description="SLAAC (Stateless Address Autoconfiguration) configured",
                recommendation=(
                    "SLAAC is suitable for end-user devices. "
                    "Configure RA (Router Advertisement) parameters: "
                    "set managed-config-flag, other-config-flag for DHCPv6 option."
                ),
                confidence=0.85, vendor=vendor,
                references=["RFC 4862", "RFC 4861", "IPv6 SLAAC Best Practices"],
            ))
        if has_dhcpv6:
            findings.append(EnterpriseKnowledgeFinding(
                domain="ipv6_analysis", category="addressing", severity="info",
                description="DHCPv6 configured for address assignment",
                recommendation=(
                    "DHCPv6 provides more control than SLAAC. "
                    "Use DHCPv6 for server infrastructure and SLAAC for clients. "
                    "Consider DHCPv6-PD for prefix delegation."
                ),
                confidence=0.8, vendor=vendor,
                references=["RFC 8415", "DHCPv6 Best Practices"],
            ))
        if has_dhcp_pd:
            findings.append(EnterpriseKnowledgeFinding(
                domain="ipv6_analysis", category="addressing", severity="info",
                description="DHCPv6 Prefix Delegation (PD) detected",
                recommendation=(
                    "DHCPv6-PD is ideal for ISP CPE and downstream routers. "
                    "Ensure the delegated prefix is properly advertised via RA."
                ),
                confidence=0.8, vendor=vendor,
                references=["RFC 3633", "DHCPv6-PD Design Guide"],
            ))
        if not has_ula:
            findings.append(EnterpriseKnowledgeFinding(
                domain="ipv6_analysis", category="addressing", severity="suggestion",
                description="ULA (Unique Local Address) not configured for internal routing",
                recommendation=(
                    "Consider using ULA (fc00::/7) for internal infrastructure addressing. "
                    "ULA addresses are not routable on the internet."
                ),
                confidence=0.6, vendor=vendor,
                references=["RFC 4193", "IPv6 ULA Best Practices"],
            ))
        return findings

    def _check_security(self, raw: str, config: object, vendor: str) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_ipv6_fw = any(kw in raw for kw in ["ipv6 firewall", "ipv6 access-list", "ipv6 filter"])
        has_ra_guard = any(kw in raw for kw in ["ra-guard", "router-advertisement-guard", "nd inspect"])
        has_dhcpv6_guard = "dhcpv6-guard" in raw or "dhcp-snooping v6" in raw
        has_privacy = "privacy-extensions" in raw or "ipv6 privacy" in raw

        if not has_ipv6_fw:
            findings.append(EnterpriseKnowledgeFinding(
                domain="ipv6_analysis", category="security", severity="warning",
                description="IPv6 firewall rules not configured",
                recommendation=(
                    "IPv6 firewall is separate from IPv4. "
                    "Configure IPv6 access-lists/firewall rules for all traffic. "
                    "Block ICMPv6 redirects and unauthorized RA messages."
                ),
                confidence=0.9, vendor=vendor,
                references=["RFC 4890", "IPv6 Firewall Best Practices"],
            ))
        if not has_ra_guard:
            findings.append(EnterpriseKnowledgeFinding(
                domain="ipv6_analysis", category="security", severity="warning",
                description="RA Guard not configured — rogue RA vulnerability",
                recommendation=(
                    "Enable RA Guard to prevent rogue Router Advertisement attacks. "
                    "Use 'ipv6 nd raguard' on access ports."
                ),
                confidence=0.85, vendor=vendor,
                references=["RFC 6105", "RA Guard Best Practices"],
            ))
        if not has_privacy:
            findings.append(EnterpriseKnowledgeFinding(
                domain="ipv6_analysis", category="security", severity="suggestion",
                description="IPv6 privacy extensions not configured",
                recommendation=(
                    "Enable privacy extensions for temporary IPv6 address generation. "
                    "Use 'ipv6 privacy-extensions' on client interfaces."
                ),
                confidence=0.6, vendor=vendor,
                references=["RFC 4941", "IPv6 Privacy Extensions"],
            ))
        return findings

    def _check_transition(self, raw: str, config: object, vendor: str) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_dns64 = "dns64" in raw or "nat64" in raw
        has_6to4 = "6to4" in raw or "ipv6 6to4" in raw
        has_6rd = "6rd" in raw or "ipv6 6rd" in raw
        has_tunnel = any(kw in raw for kw in ["tunnel", "ipv6ip", "gre tunnel"])

        if has_dns64:
            findings.append(EnterpriseKnowledgeFinding(
                domain="ipv6_analysis", category="transition", severity="info",
                description="DNS64/NAT64 transition mechanism detected",
                recommendation=(
                    "DNS64/NAT64 enables IPv6-only clients to access IPv4 services. "
                    "Verify DNS64 prefix mapping and NAT64 address pool."
                ),
                confidence=0.85, vendor=vendor,
                references=["RFC 6144", "RFC 6146", "NAT64 Design Guide"],
            ))
        if has_6to4 or has_6rd:
            findings.append(EnterpriseKnowledgeFinding(
                domain="ipv6_analysis", category="transition", severity="info",
                description="6to4/6rd transition mechanism detected",
                recommendation=(
                    "6to4 and 6rd are deprecated. Use native IPv6 or dual-stack. "
                    "If transition is needed, prefer NAT64/DNS64 or manual tunnels."
                ),
                confidence=0.8, vendor=vendor,
                references=["RFC 6343", "RFC 5569", "IPv6 Transition Best Practices"],
            ))
        return findings

    def _check_isp_deployment(self, raw: str, config: object, vendor: str) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_wan_ipv6 = any(kw in raw for kw in ["ipv6 address", "ipv6 dhcp client", "ipv6 pd"])
        has_bgp_ipv6 = "ipv6" in raw and "bgp" in raw
        has_ospf_ipv6 = "ipv6" in raw and "ospf" in raw

        if has_wan_ipv6:
            findings.append(EnterpriseKnowledgeFinding(
                domain="ipv6_analysis", category="isp_deployment", severity="info",
                description="ISP IPv6 WAN connectivity detected",
                recommendation=(
                    "Use DHCPv6-PD for prefix delegation from ISP. "
                    "Delegate /64 subnets to internal interfaces. "
                    "Advertise prefixes via RA for SLAAC clients."
                ),
                confidence=0.8, vendor=vendor,
                references=["ISP IPv6 Deployment Guide", "RFC 7084"],
            ))
        if has_bgp_ipv6:
            findings.append(EnterpriseKnowledgeFinding(
                domain="ipv6_analysis", category="isp_deployment", severity="info",
                description="BGP IPv6 peering detected",
                recommendation=(
                    "Configure BGP for IPv6 unicast address-family. "
                    "Use prefix-list and route-maps for IPv6 route filtering."
                ),
                confidence=0.85, vendor=vendor,
                references=["RFC 2545", "BGP IPv6 Peering Guide"],
            ))
        return findings


ipv6_analyzer = IPv6Analyzer()
