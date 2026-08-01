"""
Cisco Design Guide
===================

Enterprise campus, data center, SD-WAN, and high availability design patterns.
Detects design issues and provides recommendations based on Cisco best practices.

Reference: Cisco Validated Designs, Cisco Enterprise Architecture
"""

import logging
from typing import Any

from apps.network_engineer.enterprise_knowledge.base import EnterpriseKnowledgeFinding

logger = logging.getLogger(__name__)


class CiscoDesignAnalyzer:
    """
    Analyzes Cisco configurations for enterprise design best practices:
    - Campus design (hierarchy, distribution, access layers)
    - Data center fabric (VXLAN/EVPN readiness)
    - SD-WAN design principles
    - High availability patterns (HSRP, stateful switchover)
    - Borderless network architecture
    """

    CAMPUS_DESIGN_PATTERNS = {
        "three_tier": ["distribution", "access", "core"],
        "collapsed_core": ["distribution", "core"],
        "spine_leaf": ["spine", "leaf"],
    }

    def analyze(self, config: object) -> list[EnterpriseKnowledgeFinding]:
        """Analyze Cisco config for enterprise design patterns."""
        findings: list[EnterpriseKnowledgeFinding] = []
        raw = "\n".join(getattr(config, "raw_lines", [])).lower()

        vendor = getattr(config, "vendor", "") or ""
        if vendor != "cisco" and vendor and vendor != "all":
            return findings

        findings.extend(self._check_campus_design(raw, config))
        findings.extend(self._check_data_center_fabric(raw, config))
        findings.extend(self._check_sdwan_patterns(raw, config))
        findings.extend(self._check_ha_patterns(raw, config))
        findings.extend(self._check_security_posture(raw, config))

        return findings

    def _check_campus_design(self, raw: str, config: object) -> list[EnterpriseKnowledgeFinding]:
        """Check campus design hierarchy patterns."""
        findings = []

        # Check for distribution layer (VLAN, inter-VLAN routing)
        has_distribution = any(kw in raw for kw in ["vlan", "ip routing", "interface vlan"])
        # Check for access layer (switchport, port-security)
        has_access = any(kw in raw for kw in ["switchport", "port-security", "spanning-tree portfast"])
        # Check for core layer (high-speed interfaces, routing)
        has_core = any(kw in raw for kw in ["router ospf", "router eigrp", "ip route 0.0.0.0"])

        if has_distribution and has_access and has_core:
            findings.append(EnterpriseKnowledgeFinding(
                domain="cisco_design",
                category="campus_architecture",
                severity="info",
                description="Three-tier campus hierarchy detected (core, distribution, access)",
                recommendation=(
                    "Ensure proper Layer 2/Layer 3 boundaries: access layer for user connectivity, "
                    "distribution for policy enforcement, core for high-speed transport."
                ),
                confidence=0.7,
                vendor="cisco",
                references=["Cisco Campus Design Guide", "CVD Enterprise Campus 3.0"],
            ))
        elif has_distribution and has_access and not has_core:
            findings.append(EnterpriseKnowledgeFinding(
                domain="cisco_design",
                category="campus_architecture",
                severity="info",
                description="Collapsed core design detected (distribution + core combined)",
                recommendation=(
                    "For networks under 500 devices, collapsed core is acceptable. "
                    "Ensure the distribution layer has sufficient forwarding capacity."
                ),
                confidence=0.65,
                vendor="cisco",
                references=["Cisco Collapsed Core Architecture"],
            ))

        # Check for VLAN design issues
        interfaces = getattr(config, "interfaces", [])
        vlan_count = sum(1 for i in interfaces if hasattr(i, "vlan") and i.vlan)
        if vlan_count > 50:
            findings.append(EnterpriseKnowledgeFinding(
                domain="cisco_design",
                category="campus_scalability",
                severity="warning",
                description=f"Large number of VLANs ({vlan_count}) detected — may cause STP convergence issues",
                recommendation=(
                    "Consider using VXLAN/EVPN for large-scale segmentation. "
                    "Alternatively, implement MSTP with multiple instances."
                ),
                confidence=0.7,
                vendor="cisco",
                references=["Cisco STP Best Practices", "RFC 7432 EVPN"],
            ))

        # Check for spanning-tree portfast
        if "spanning-tree portfast" not in raw and "spanning-tree" in raw:
            findings.append(EnterpriseKnowledgeFinding(
                domain="cisco_design",
                category="campus_optimization",
                severity="suggestion",
                description="PortFast not configured on access ports",
                recommendation=(
                    "Enable spanning-tree portfast on all access ports to reduce convergence time. "
                    "Use BPDUguard for port security."
                ),
                confidence=0.8,
                vendor="cisco",
                references=["Cisco STP PortFast Best Practice"],
            ))

        return findings

    def _check_data_center_fabric(self, raw: str, config: object) -> list[EnterpriseKnowledgeFinding]:
        """Check data center fabric patterns (VXLAN, EVPN, etc.)."""
        findings = []

        has_vxlan = any(kw in raw for kw in ["vxlan", "nve", "vni", "segment"])
        has_evpn = any(kw in raw for kw in ["evpn", "l2vpn", "evpn instance"])
        has_spine_leaf = any(kw in raw for kw in ["spine", "leaf", "border leaf"])

        if has_vxlan and has_evpn:
            findings.append(EnterpriseKnowledgeFinding(
                domain="cisco_design",
                category="data_center",
                severity="info",
                description="VXLAN/EVPN fabric detected — modern data center design",
                recommendation=(
                    "Verify anycast gateway configuration, VNI mapping, and "
                    "BGP EVPN address-family parameters for optimal operation."
                ),
                confidence=0.85,
                vendor="cisco",
                references=["Cisco ACI Design Guide", "RFC 7432", "RFC 8365"],
            ))
        elif has_vxlan and not has_evpn:
            findings.append(EnterpriseKnowledgeFinding(
                domain="cisco_design",
                category="data_center",
                severity="warning",
                description="VXLAN without EVPN control plane — manual flooding required",
                recommendation=(
                    "Add BGP EVPN as the control plane for VXLAN to enable "
                    "efficient MAC learning, ARP suppression, and multi-tenancy."
                ),
                confidence=0.8,
                vendor="cisco",
                references=["Cisco VXLAN/EVPN Design Guide"],
            ))

        if has_spine_leaf:
            findings.append(EnterpriseKnowledgeFinding(
                domain="cisco_design",
                category="data_center",
                severity="info",
                description="Spine-leaf topology detected",
                recommendation=(
                    "Ensure equal-cost multipath (ECMP) is configured across all spine links. "
                    "All leaf switches should connect to all spine switches for optimal load balancing."
                ),
                confidence=0.8,
                vendor="cisco",
                references=["Cisco Data Center Spine-Leaf Architecture"],
            ))

        return findings

    def _check_sdwan_patterns(self, raw: str, config: object) -> list[EnterpriseKnowledgeFinding]:
        """Check SD-WAN design patterns."""
        findings = []

        has_sdwan = any(kw in raw for kw in ["sd-wan", "vsmart", "vmanage", "vedge", "cedge"])
        has_tloc = "tloc" in raw
        has_bgp_wan = "bgp" in raw and any(kw in raw for kw in ["wan", "internet", "mpls"])

        if has_sdwan:
            findings.append(EnterpriseKnowledgeFinding(
                domain="cisco_design",
                category="sd_wan",
                severity="info",
                description="Cisco SD-WAN design detected",
                recommendation=(
                    "Verify vSmart/vManage/vBond controller placement, TLOC color mapping, "
                    "and application-aware routing policies for optimal SD-WAN operation."
                ),
                confidence=0.85,
                vendor="cisco",
                references=["Cisco SD-WAN Design Guide", "Cisco SD-WAN Validated Designs"],
            ))

            if has_tloc:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="cisco_design",
                    category="sd_wan",
                    severity="info",
                    description="TLOC (Transport Location) configurations detected",
                    recommendation=(
                        "Ensure TLOC colors are consistent across all WAN edges. "
                        "Verify that the transport network supports the configured TLOC colors."
                    ),
                    confidence=0.75,
                    vendor="cisco",
                    references=["Cisco SD-WAN TLOC Design"],
                ))

        return findings

    def _check_ha_patterns(self, raw: str, config: object) -> list[EnterpriseKnowledgeFinding]:
        """Check high availability design patterns."""
        findings = []

        has_hsrp = any(kw in raw for kw in ["standby", "hsrp", "vrrp", "glbp"])
        has_ssso = "redundancy" in raw or "stateful switchover" in raw
        has_nsf = "nsf" in raw or "non-stop forwarding" in raw

        if has_hsrp:
            standby_count = raw.count("standby")
            if standby_count > 1:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="cisco_design",
                    category="high_availability",
                    severity="info",
                    description=f"First Hop Redundancy Protocol detected ({standby_count} standby groups)",
                    recommendation=(
                        "Verify HSRP/VRRP authentication, preemption delay, and "
                        "object tracking for WAN link failure detection."
                    ),
                    confidence=0.85,
                    vendor="cisco",
                    references=["Cisco HSRP Best Practices", "RFC 2281"],
                ))

        if has_ssso or has_nsf:
            findings.append(EnterpriseKnowledgeFinding(
                domain="cisco_design",
                category="high_availability",
                severity="info",
                description="Stateful Switchover (SSO) or NSF detected",
                recommendation=(
                    "SSO/NSF provides hitless failover for routing protocols. "
                    "Verify that all peers support graceful restart."
                ),
                confidence=0.8,
                vendor="cisco",
                references=["Cisco SSO/NSF Design Guide"],
            ))

        if not has_hsrp and not has_ssso:
            findings.append(EnterpriseKnowledgeFinding(
                domain="cisco_design",
                category="high_availability",
                severity="suggestion",
                description="No high availability mechanism detected",
                recommendation=(
                    "Consider implementing HSRP/VRRP for gateway redundancy, "
                    "and SSO/NSF for control plane high availability."
                ),
                confidence=0.7,
                vendor="cisco",
                references=["Cisco HA Design Guide"],
            ))

        return findings

    def _check_security_posture(self, raw: str, config: object) -> list[EnterpriseKnowledgeFinding]:
        """Check security posture for Cisco devices."""
        findings = []

        # Check for AAA
        has_aaa = any(kw in raw for kw in ["aaa new-model", "aaa authentication", "aaa authorization"])
        if not has_aaa:
            findings.append(EnterpriseKnowledgeFinding(
                domain="cisco_design",
                category="security",
                severity="warning",
                description="AAA not configured for Cisco device",
                recommendation=(
                    "Enable AAA (aaa new-model) for centralized authentication, "
                    "authorization, and accounting. Use TACACS+ for device administration."
                ),
                confidence=0.9,
                vendor="cisco",
                references=["CIS Cisco Benchmark 5.1", "Cisco AAA Design Guide"],
            ))

        # Check for management plane protection
        if "control-plane" not in raw:
            findings.append(EnterpriseKnowledgeFinding(
                domain="cisco_design",
                category="security",
                severity="warning",
                description="Control Plane Policing (CoPP) not configured",
                recommendation=(
                    "Configure control-plane policing to protect the route processor "
                    "from excessive traffic and DoS attacks."
                ),
                confidence=0.7,
                vendor="cisco",
                references=["Cisco CoPP Best Practices"],
            ))

        # Check for NTP authentication
        if "ntp" in raw and "ntp authenticate" not in raw:
            findings.append(EnterpriseKnowledgeFinding(
                domain="cisco_design",
                category="security",
                severity="suggestion",
                description="NTP configured without authentication",
                recommendation=(
                    "Enable NTP authentication to prevent time spoofing attacks. "
                    "Use 'ntp authenticate' and 'ntp authentication-key' commands."
                ),
                confidence=0.8,
                vendor="cisco",
                references=["NIST SP 800-53 AU-8", "CIS Cisco Benchmark 2.2"],
            ))

        return findings


cisco_design_analyzer = CiscoDesignAnalyzer()
