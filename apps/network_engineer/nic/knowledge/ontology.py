"""
Network Ontology
=================

Maps vendor-specific network features to universal concepts.
This is the foundation for concept-level analysis, compliance, and cross-vendor translation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class UniversalConcept(str, Enum):
    HIGH_AVAILABILITY = "high_availability"
    TRAFFIC_FILTERING = "traffic_filtering"
    ADDRESS_TRANSLATION = "address_translation"
    IP_MANAGEMENT = "ip_management"
    ROUTING = "routing"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    MONITORING = "monitoring"
    BACKUP = "backup"
    DNS_RESOLUTION = "dns_resolution"
    TIME_SYNCHRONIZATION = "time_synchronization"
    WIRELESS = "wireless"
    VLAN = "vlan"
    VPN = "vpn"
    QOS = "qos"
    LOGGING = "logging"
    SYSTEM_IDENTITY = "system_identity"
    CERTIFICATE = "certificate"


@dataclass
class ConceptDefinition:
    concept: UniversalConcept
    description: str
    vendor_names: dict[str, list[str]]
    references: list[str] = field(default_factory=list)
    severity_default: str = "warning"


CONCEPT_DEFINITIONS: dict[UniversalConcept, ConceptDefinition] = {
    UniversalConcept.HIGH_AVAILABILITY: ConceptDefinition(
        concept=UniversalConcept.HIGH_AVAILABILITY,
        description="Protocols providing redundant gateway or device failover",
        vendor_names={
            "cisco": ["hsrp", "vrrp", "glbp", "redundancy"],
            "fortinet": ["ha", "cluster", "redundancy"],
            "mikrotik": ["vrrp", "redundancy"],
        },
        references=["RFC 3768", "RFC 2281", "CIS Benchmark 3.3"],
    ),
    UniversalConcept.TRAFFIC_FILTERING: ConceptDefinition(
        concept=UniversalConcept.TRAFFIC_FILTERING,
        description="Rules controlling traffic flow based on source, destination, protocol, and port",
        vendor_names={
            "cisco": ["acl", "access-list", "ip access-list"],
            "fortinet": ["firewall policy", "firewall address", "firewall service"],
            "mikrotik": ["firewall filter", "firewall nat"],
        },
        references=["RFC 791", "CIS Benchmark 4.1", "NIST SP 800-41"],
    ),
    UniversalConcept.ADDRESS_TRANSLATION: ConceptDefinition(
        concept=UniversalConcept.ADDRESS_TRANSLATION,
        description="Translation of private IP addresses to public IP addresses for internet access",
        vendor_names={
            "cisco": ["nat", "ip nat"],
            "fortinet": ["nat", "firewall nat"],
            "mikrotik": ["nat", "masquerade", "srcnat"],
        },
        references=["RFC 3022", "CIS Benchmark 4.2"],
    ),
    UniversalConcept.IP_MANAGEMENT: ConceptDefinition(
        concept=UniversalConcept.IP_MANAGEMENT,
        description="IP address assignment, DHCP, and interface configuration",
        vendor_names={
            "cisco": ["ip address", "dhcp", "interface"],
            "fortinet": ["interface", "dhcp server"],
            "mikrotik": ["ip address", "dhcp-server", "interface"],
        },
        references=["RFC 1918", "RFC 2131"],
    ),
    UniversalConcept.ROUTING: ConceptDefinition(
        concept=UniversalConcept.ROUTING,
        description="Static and dynamic routing protocols",
        vendor_names={
            "cisco": ["ip route", "router ospf", "router bgp", "router eigrp"],
            "fortinet": ["router static", "router ospf", "router bgp"],
            "mikrotik": ["ip route", "routing ospf", "routing bgp"],
        },
        references=["RFC 2328", "RFC 4271"],
    ),
    UniversalConcept.AUTHENTICATION: ConceptDefinition(
        concept=UniversalConcept.AUTHENTICATION,
        description="User authentication and login control",
        vendor_names={
            "cisco": ["username", "login local", "aaa authentication", "enable secret"],
            "fortinet": ["system local", "passwd", "ldap", "radius"],
            "mikrotik": ["user", "password", "aaa"],
        },
        references=["RFC 2865", "CIS Benchmark 5.1"],
    ),
    UniversalConcept.MONITORING: ConceptDefinition(
        concept=UniversalConcept.MONITORING,
        description="SNMP, logging, and network monitoring",
        vendor_names={
            "cisco": ["snmp-server", "logging", "debug"],
            "fortinet": ["log", "snmp", "monitor"],
            "mikrotik": ["snmp", "log", "monitor"],
        },
        references=["RFC 1157", "RFC 5424"],
    ),
    UniversalConcept.BACKUP: ConceptDefinition(
        concept=UniversalConcept.BACKUP,
        description="Configuration backup and restore",
        vendor_names={
            "cisco": ["archive", "backup", "copy"],
            "fortinet": ["backup", "restore", "config"],
            "mikrotik": ["backup", "export", "import"],
        },
        references=["CIS Benchmark 2.3"],
    ),
    UniversalConcept.DNS_RESOLUTION: ConceptDefinition(
        concept=UniversalConcept.DNS_RESOLUTION,
        description="DNS server configuration and caching",
        vendor_names={
            "cisco": ["ip name-server", "ip dns"],
            "fortinet": ["system dns"],
            "mikrotik": ["ip dns", "dns"],
        },
        references=["RFC 1034", "RFC 1035"],
    ),
    UniversalConcept.TIME_SYNCHRONIZATION: ConceptDefinition(
        concept=UniversalConcept.TIME_SYNCHRONIZATION,
        description="NTP and time configuration",
        vendor_names={
            "cisco": ["ntp server", "ntp source"],
            "fortinet": ["system ntp"],
            "mikrotik": ["system ntp", "ntp"],
        },
        references=["RFC 5905"],
    ),
    UniversalConcept.VPN: ConceptDefinition(
        concept=UniversalConcept.VPN,
        description="VPN tunnels and encryption",
        vendor_names={
            "cisco": ["crypto map", "tunnel", "ipsec"],
            "fortinet": ["vpn ipsec", "ssl vpn"],
            "mikrotik": ["interface", "vpn", "ipsec", "wireguard"],
        },
        references=["RFC 4301", "RFC 7296"],
    ),
    UniversalConcept.QOS: ConceptDefinition(
        concept=UniversalConcept.QOS,
        description="Quality of Service and traffic shaping",
        vendor_names={
            "cisco": ["qos", "policy-map", "class-map"],
            "fortinet": ["shaper", "traffic-shaper"],
            "mikrotik": ["queue", "queue-tree", "queue-type"],
        },
        references=["RFC 2474"],
    ),
    UniversalConcept.LOGGING: ConceptDefinition(
        concept=UniversalConcept.LOGGING,
        description="System logging and audit trails",
        vendor_names={
            "cisco": ["logging", "log"],
            "fortinet": ["log", "syslog"],
            "mikrotik": ["log", "system log"],
        },
        references=["RFC 5424"],
    ),
}


class ConceptMapper:
    """Maps vendor-specific AST features to universal concepts."""

    def __init__(self):
        self._concepts = CONCEPT_DEFINITIONS

    def detect_concepts(self, ast: Any) -> dict[UniversalConcept, list[dict[str, Any]]]:
        """Detect which universal concepts are present in the AST."""
        detected: dict[UniversalConcept, list[dict[str, Any]]] = {}
        vendor = getattr(ast, "vendor", "") or ""
        vendor_specific = getattr(ast, "vendor_specific", {}) or {}
        raw = "\n".join(getattr(ast, "raw_lines", [])).lower()

        for concept, definition in self._concepts.items():
            vendor_keywords = definition.vendor_names.get(vendor, [])
            evidence = []
            confidence = 0.0

            for keyword in vendor_keywords:
                if keyword in raw:
                    evidence.append({"keyword": keyword, "source": "raw_config", "vendor": vendor})

            if vendor in ["cisco", "fortinet"]:
                for key in vendor_specific:
                    if any(kw in key.lower() for kw in vendor_keywords):
                        evidence.append({"keyword": key, "source": "vendor_specific", "vendor": vendor})

            if evidence:
                detected[concept] = evidence
                confidence = min(1.0, 0.5 + 0.1 * len(evidence))

        return detected

    def get_concept_definition(self, concept: UniversalConcept) -> ConceptDefinition | None:
        return self._concepts.get(concept)

    def get_all_concepts(self) -> list[UniversalConcept]:
        return list(self._concepts.keys())


concept_mapper = ConceptMapper()
