"""
Network Advisor
===============

High-level network design advisor that answers architectural questions
and produces explainable designs, not just configuration lists.
"""

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class DesignRequirement:
    category: str
    description: str
    priority: str = "medium"


@dataclass
class DesignProposal:
    title: str
    description: str
    architecture_summary: str
    components: list[str]
    recommendations: list[str]
    risks: list[str]
    estimated_cost: str = "medium"
    complexity: str = "medium"

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "architecture_summary": self.architecture_summary,
            "components": self.components,
            "recommendations": self.recommendations,
            "risks": self.risks,
            "estimated_cost": self.estimated_cost,
            "complexity": self.complexity,
        }


class NetworkAdvisor:
    """Provides high-level network design advice."""

    async def advise(self, query: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        query_lower = query.lower()
        proposals = []

        if "500 cabang" in query_lower or "500 branch" in query_lower or "branch" in query_lower:
            proposals.append(self._design_multi_branch(context))
        if "ha datacenter" in query_lower or "high availability datacenter" in query_lower or "datacenter" in query_lower:
            proposals.append(self._design_ha_datacenter(context))
        if "security" in query_lower and "zero trust" in query_lower:
            proposals.append(self._design_zero_trust(context))
        if "sd-wan" in query_lower:
            proposals.append(self._design_sd_wan(context))
        if "small office" in query_lower or "sme" in query_lower or "small business" in query_lower:
            proposals.append(self._design_smb(context))

        if not proposals:
            proposals.append(self._general_advice(query, context))

        return {
            "query": query,
            "proposals": [p.to_dict() for p in proposals],
            "meta": {
                "total_proposals": len(proposals),
                "advisor_version": "2.0.0",
            },
        }

    def _design_multi_branch(self, context: dict[str, Any]) -> DesignProposal:
        return DesignProposal(
            title="Multi-Branch Enterprise Network",
            description="Scalable design for 500+ branches with centralized control.",
            architecture_summary=(
                "Hub-and-spoke topology with a central datacenter hub, regional distribution hubs, "
                "and branch edge routers. SD-WAN orchestrates connectivity with application-aware routing. "
                "Zero Trust Network Access (ZTNA) secures branch-to-cloud traffic."
            ),
            components=[
                "Centralized SD-WAN controller",
                "Branch edge routers/firewalls",
                "Regional distribution hubs",
                "IPsec/VXLAN tunnels for site-to-site",
                "Centralized identity and policy management",
                "Cloud on-ramp for SaaS applications",
            ],
            recommendations=[
                "Use SD-WAN for branch connectivity to reduce MPLS costs.",
                "Implement centralized configuration management (GitOps or Ansible).",
                "Deploy branch firewalls with URL filtering and IPS.",
                "Use IPsec tunnels for internet breakouts and critical apps.",
                "Segment each branch into VLANs: corporate, guest, IoT, management.",
                "Implement redundant WAN links (dual ISP) at each branch.",
            ],
            risks=[
                "Controller failure can affect all branches.",
                "Insufficient bandwidth at regional hubs.",
                "Branch devices may lack resources for full security stack.",
            ],
            estimated_cost="high",
            complexity="high",
        )

    def _design_ha_datacenter(self, context: dict[str, Any]) -> DesignProposal:
        return DesignProposal(
            title="High Availability Datacenter Network",
            description="Resilient datacenter design with no single point of failure.",
            architecture_summary=(
                "Leaf-spine topology with dual-homed servers, MLAG/EVPN multi-chassis, "
                "and out-of-band management network. Border leaf routers provide north-south connectivity "
                "with redundant BGP peering. Power, cooling, and control plane are fully redundant."
            ),
            components=[
                "Spine switches (2+ devices)",
                "Leaf switches (2+ per rack)",
                "Border leaf routers with BGP Anycast",
                "EVPN-VXLAN for L2 extension",
                "Out-of-band management network",
                "Dual power supplies and PDUs",
            ],
            recommendations=[
                "Use EVPN-VXLAN for scalable L2/L3 fabric.",
                "Implement anycast gateways for first-hop redundancy.",
                "Deploy redundant border routers with BGP communities.",
                "Separate management, storage, and production networks.",
                "Implement DCI (Data Center Interconnect) for disaster recovery.",
                "Use automated provisioning and telemetry for fast failure detection.",
            ],
            risks=[
                "MLAG vendor lock-in if not using open standards.",
                "VXLAN control plane complexity.",
                "Under-provisioning of spine bandwidth as scale grows.",
            ],
            estimated_cost="very high",
            complexity="very high",
        )

    def _design_zero_trust(self, context: dict[str, Any]) -> DesignProposal:
        return DesignProposal(
            title="Zero Trust Network Architecture",
            description="Security model that verifies every request, regardless of origin.",
            architecture_summary=(
                "Identity-aware firewall and microsegmentation enforce least-privilege access. "
                "All traffic is inspected, and access is granted per application and user identity. "
                "Continuous verification replaces perimeter-based trust."
            ),
            components=[
                "Identity Provider (IdP) with MFA",
                "Zero Trust Network Access (ZTNA) gateway",
                "Microsegmentation policy engine",
                "Device posture assessment",
                "Encrypted DNS (DoH/DoT)",
                "Centralized policy and audit logging",
            ],
            recommendations=[
                "Deploy identity-aware firewalls at all enforcement points.",
                "Segment applications using microsegmentation, not just VLANs.",
                "Require MFA and device compliance for all access.",
                "Encrypt all traffic, including internal East-West traffic.",
                "Implement continuous monitoring and automated response.",
                "Use software-defined perimeters (SDP) for remote access.",
            ],
            risks=[
                "Increased complexity in policy management.",
                "Potential performance impact from deep packet inspection.",
                "User experience degradation if policies are too strict.",
            ],
            estimated_cost="high",
            complexity="high",
        )

    def _design_sd_wan(self, context: dict[str, Any]) -> DesignProposal:
        return DesignProposal(
            title="SD-WAN Architecture",
            description="Application-aware WAN with centralized orchestration.",
            architecture_summary=(
                "SD-WAN edge devices at each site connect to multiple transports (MPLS, broadband, LTE). "
                "Centralized controller defines policies for path selection based on application performance. "
                "Cloud on-ramp provides optimized access to SaaS applications."
            ),
            components=[
                "SD-WAN edge appliances",
                "Centralized orchestrator/controller",
                "Transport diversity (MPLS, broadband, 5G)",
                "Application performance monitoring",
                "Cloud on-ramp gateways",
                "Integrated security (FW, IPS, URL filtering)",
            ],
            recommendations=[
                "Start with a pilot site to validate application performance.",
                "Use application-aware routing to steer critical traffic over MPLS and less critical over broadband.",
                "Deploy integrated security at the edge to avoid backhauling.",
                "Implement centralized configuration and zero-touch provisioning.",
                "Monitor application performance with synthetic testing.",
            ],
            risks=[
                "Controller failure affects all sites.",
                "Underestimating broadband variability.",
                "Security gaps if edge appliances are not properly hardened.",
            ],
            estimated_cost="medium",
            complexity="medium",
        )

    def _design_smb(self, context: dict[str, Any]) -> DesignProposal:
        return DesignProposal(
            title="Small and Medium Business Network",
            description="Simplified, secure network for small offices with limited IT staff.",
            architecture_summary=(
                "Unified firewall, switch, and wireless in a single appliance or compact stack. "
                "Cloud-managed for easy administration. Guest and corporate networks segmented. "
                "Basic threat protection and content filtering included."
            ),
            components=[
                "Unified Threat Management (UTM) firewall",
                "Managed PoE switches",
                "Cloud-managed wireless access points",
                "Guest Wi-Fi with captive portal",
                "Basic VLAN segmentation",
                "Automated firmware updates",
            ],
            recommendations=[
                "Use a single vendor stack for simplified management.",
                "Segment guest, corporate, and POS/PCI networks.",
                "Enable automatic firmware updates.",
                "Deploy cloud-based logging and threat intelligence.",
                "Use strong passwords and MFA for admin access.",
                "Implement regular backups of device configurations.",
            ],
            risks=[
                "Single point of failure with unified appliance.",
                "Limited scalability as business grows.",
                "Cloud dependency for management.",
            ],
            estimated_cost="low",
            complexity="low",
        )

    def _general_advice(self, query: str, context: dict[str, Any]) -> DesignProposal:
        return DesignProposal(
            title="General Network Design Guidance",
            description=f"Advice based on query: '{query}'",
            architecture_summary=(
                "A well-designed network follows the principle of least privilege, defense in depth, "
                "and operational simplicity. Start with requirements gathering, then design the physical and logical topology, "
                "followed by detailed configuration and testing."
            ),
            components=[
                "Requirements analysis",
                "Logical and physical topology design",
                "Device selection and sizing",
                "Configuration standards",
                "Testing and validation plan",
            ],
            recommendations=[
                "Document requirements before designing.",
                "Follow vendor best practices and compliance frameworks.",
                "Implement redundancy for critical paths.",
                "Plan for monitoring and operations from day one.",
            ],
            risks=[],
            estimated_cost="medium",
            complexity="medium",
        )


network_advisor = NetworkAdvisor()