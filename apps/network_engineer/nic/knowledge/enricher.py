"""
Knowledge Enricher
===================

Enriches Universal AST with conceptual knowledge tags,
explanations, and cross-vendor mappings.
"""

import logging
from dataclasses import dataclass, field
from typing import Any

from apps.network_engineer.nic.knowledge.ontology import (
    ConceptDefinition,
    ConceptMapper,
    UniversalConcept,
)

logger = logging.getLogger(__name__)


@dataclass
class ConceptTag:
    concept: UniversalConcept
    confidence: float
    evidence: list[dict[str, Any]]
    explanation: str = ""
    references: list[str] = field(default_factory=list)


class KnowledgeEnricher:
    """Enriches Universal AST with network knowledge."""

    def __init__(self):
        self._concept_mapper = ConceptMapper()

    def enrich(self, ast: Any) -> list[ConceptTag]:
        """Analyze AST and return conceptual tags with explanations."""
        tags = []
        detected = self._concept_mapper.detect_concepts(ast)

        for concept, evidence in detected.items():
            definition = self._concept_mapper.get_concept_definition(concept)
            if not definition:
                continue

            confidence = min(1.0, 0.5 + 0.1 * len(evidence))
            explanation = self._build_explanation(concept, definition, ast)
            references = list(definition.references)

            tags.append(ConceptTag(
                concept=concept,
                confidence=confidence,
                evidence=evidence,
                explanation=explanation,
                references=references,
            ))

        logger.info("Enriched AST with %d concept tags", len(tags))
        return tags

    def explain_finding(self, finding_category: str, ast: Any) -> str | None:
        """Explain a finding using knowledge base."""
        concept_map = {
            "Security": UniversalConcept.TRAFFIC_FILTERING,
            "Firewall": UniversalConcept.TRAFFIC_FILTERING,
            "NAT": UniversalConcept.ADDRESS_TRANSLATION,
            "Performance": UniversalConcept.QOS,
            "Backup": UniversalConcept.BACKUP,
            "DNS": UniversalConcept.DNS_RESOLUTION,
            "Routing": UniversalConcept.ROUTING,
            "OSPF": UniversalConcept.OSPF,
            "BGP": UniversalConcept.BGP,
            "IS-IS": UniversalConcept.IS_IS,
            "VXLAN": UniversalConcept.VXLAN,
            "EVPN": UniversalConcept.EVPN,
            "SD-WAN": UniversalConcept.SD_WAN,
            "System": UniversalConcept.TIME_SYNCHRONIZATION,
            "IP": UniversalConcept.IP_MANAGEMENT,
            "VLAN": UniversalConcept.VLAN,
            "Wireless": UniversalConcept.WIRELESS,
            "WiFi": UniversalConcept.WIRELESS,
            "PPP": UniversalConcept.VPN,
            "DHCP": UniversalConcept.DHCP,
            "Multicast": UniversalConcept.MULTICAST,
            "Switching": UniversalConcept.SWITCHING,
            "IPv6": UniversalConcept.IPV6,
            "Zero Trust": UniversalConcept.ZERO_TRUST,
        }

        concept = concept_map.get(finding_category)
        if not concept:
            return None

        definition = self._concept_mapper.get_concept_definition(concept)
        if definition:
            return definition.description
        return None

    def get_cross_vendor_mapping(self, vendor_concept: str, source_vendor: str, target_vendor: str) -> str | None:
        """Get the equivalent concept name in another vendor."""
        concept_map: dict[str, dict[str, str]] = {
            "hsrp": {"cisco": "hsrp", "fortinet": "ha", "mikrotik": "vrrp"},
            "vrrp": {"cisco": "hsrp", "fortinet": "ha", "mikrotik": "vrrp"},
            "ha": {"cisco": "hsrp", "fortinet": "ha", "mikrotik": "vrrp"},
            "acl": {"cisco": "access-list", "fortinet": "firewall policy", "mikrotik": "firewall filter"},
            "firewall_policy": {"cisco": "access-list", "fortinet": "firewall policy", "mikrotik": "firewall filter"},
            "firewall_filter": {"cisco": "access-list", "fortinet": "firewall policy", "mikrotik": "firewall filter"},
            "nat": {"cisco": "ip nat", "fortinet": "nat", "mikrotik": "nat"},
        }

        normalized = vendor_concept.lower().replace("-", " ").strip()
        mapping = concept_map.get(normalized)
        if mapping:
            return mapping.get(target_vendor)
        return None

    def _build_explanation(self, concept: UniversalConcept, definition: ConceptDefinition, ast: Any) -> str:
        explanations = {
            UniversalConcept.HIGH_AVAILABILITY: (
                "High Availability (HA) ensures network services remain available during failures. "
                "Protocols like HSRP, VRRP, and Fortinet HA provide automatic failover between devices."
            ),
            UniversalConcept.TRAFFIC_FILTERING: (
                "Traffic filtering controls which packets are allowed or denied based on "
                "source, destination, protocol, and port. Proper filtering is critical for network security."
            ),
            UniversalConcept.ADDRESS_TRANSLATION: (
                "Address Translation (NAT) maps private IP addresses to public IP addresses. "
                "This enables internal devices to access external networks while hiding internal addressing."
            ),
            UniversalConcept.IP_MANAGEMENT: (
                "IP Management includes interface configuration, DHCP services, and IP address planning. "
                "Proper IP management ensures connectivity and prevents address conflicts."
            ),
            UniversalConcept.ROUTING: (
                "Routing determines the path packets take through the network. "
                "Static routes provide fixed paths, while dynamic protocols adapt to topology changes."
            ),
            UniversalConcept.AUTHENTICATION: (
                "Authentication verifies user identity before granting access. "
                "Strong authentication prevents unauthorized access to network devices."
            ),
            UniversalConcept.MONITORING: (
                "Monitoring provides visibility into network health and performance. "
                "SNMP and logging enable proactive issue detection."
            ),
            UniversalConcept.BACKUP: (
                "Configuration backup ensures recovery from failures or misconfigurations. "
                "Regular backups reduce downtime during incidents."
            ),
            UniversalConcept.DNS_RESOLUTION: (
                "DNS resolution maps domain names to IP addresses. "
                "Reliable DNS is essential for network services and user experience."
            ),
            UniversalConcept.TIME_SYNCHRONIZATION: (
                "Time synchronization ensures consistent timestamps across devices. "
                "NTP provides accurate time for logging, certificates, and protocols."
            ),
            UniversalConcept.VPN: (
                "VPN creates encrypted tunnels over untrusted networks. "
                "IPsec and SSL VPNs provide secure remote access and site-to-site connectivity."
            ),
            UniversalConcept.QOS: (
                "Quality of Service prioritizes critical traffic over less important traffic. "
                "QoS ensures voice, video, and business applications perform well."
            ),
            UniversalConcept.LOGGING: (
                "Logging records events for troubleshooting, auditing, and security. "
                "Centralized logging enables correlation and compliance reporting."
            ),
            UniversalConcept.VLAN: (
                "VLANs segment broadcast domains for security and performance. "
                "Proper VLAN design limits traffic scope and improves network efficiency."
            ),
            UniversalConcept.SWITCHING: (
                "Switching forwards frames based on MAC addresses within a broadcast domain. "
                "Proper switch configuration prevents loops and optimizes traffic flow."
            ),
            UniversalConcept.OSPF: (
                "OSPF is an interior gateway protocol that calculates shortest paths using link-state databases. "
                "Proper area design and authentication improve scalability and security."
            ),
            UniversalConcept.IS_IS: (
                "IS-IS is a link-state routing protocol used for large service provider networks. "
                "It provides fast convergence and supports both IPv4 and IPv6."
            ),
            UniversalConcept.VXLAN: (
                "VXLAN tunnels Layer 2 traffic over Layer 3 networks using UDP encapsulation. "
                "It enables scalable network segmentation across data centers."
            ),
            UniversalConcept.EVPN: (
                "EVPN provides control plane for VXLAN and other overlay networks. "
                "It enables multi-tenancy and efficient MAC learning across sites."
            ),
            UniversalConcept.SD_WAN: (
                "SD-WAN orchestrates WAN connectivity with application-aware routing. "
                "It improves performance, reduces costs, and simplifies management."
            ),
            UniversalConcept.IPV6: (
                "IPv6 provides larger address space and improved header efficiency. "
                "Proper dual-stack or native IPv6 deployment ensures future readiness."
            ),
            UniversalConcept.MULTICAST: (
                "Multicast delivers traffic to multiple receivers efficiently. "
                "PIM and IGMP control multicast distribution without flooding all hosts."
            ),
            UniversalConcept.ZERO_TRUST: (
                "Zero Trust assumes no implicit trust and verifies every access request. "
                "Identity, device health, and least-privilege access reduce breach impact."
            ),
            UniversalConcept.DHCP: (
                "DHCP automatically assigns IP addresses and network parameters to devices. "
                "Proper DHCP sizing and relay configuration prevent address exhaustion."
            ),
        }

        return explanations.get(concept, definition.description)


knowledge_enricher = KnowledgeEnricher()
