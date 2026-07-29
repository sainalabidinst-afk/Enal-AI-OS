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
    OSPF = "ospf"
    BGP = "bgp"
    IS_IS = "is_is"
    SWITCHING = "switching"
    VLAN = "vlan"
    VXLAN = "vxlan"
    EVPN = "evpn"
    MPLS = "mpls"
    SD_WAN = "sd_wan"
    QOS = "qos"
    MULTICAST = "multicast"
    WIRELESS = "wireless"
    WIRELESS_MANAGEMENT = "wireless_management"
    VPN = "vpn"
    IPV6 = "ipv6"
    DNS_RESOLUTION = "dns_resolution"
    DHCP = "dhcp"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    ZERO_TRUST = "zero_trust"
    MONITORING = "monitoring"
    BACKUP = "backup"
    TIME_SYNCHRONIZATION = "time_synchronization"
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
    UniversalConcept.DHCP: ConceptDefinition(
        concept=UniversalConcept.DHCP,
        description="DHCP server and relay configuration",
        vendor_names={
            "cisco": ["ip dhcp", "dhcp pool", "dhcp relay"],
            "fortinet": ["dhcp server", "dhcp relay"],
            "mikrotik": ["ip dhcp-server", "dhcp-server", "dhcp relay"],
        },
        references=["RFC 2131", "RFC 2132"],
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
     UniversalConcept.BGP: ConceptDefinition(
         concept=UniversalConcept.BGP,
         description="Border Gateway Protocol for external routing",
         vendor_names={
             "cisco": ["router bgp", "bgp", "neighbor", "as-path"],
             "fortinet": ["router bgp", "bgp", "neighbor"],
             "mikrotik": ["routing bgp", "bgp", "peer"],
         },
         references=["RFC 4271", "RFC 1997"],
     ),
     UniversalConcept.MPLS: ConceptDefinition(
         concept=UniversalConcept.MPLS,
         description="Multiprotocol Label Switching for traffic engineering",
         vendor_names={
             "cisco": ["mpls", "ldp", "label", "traffic-eng"],
             "fortinet": ["mpls"],
             "mikrotik": ["mpls", "ldp", "label"],
         },
         references=["RFC 3031", "RFC 5036"],
     ),
     UniversalConcept.WIRELESS_MANAGEMENT: ConceptDefinition(
         concept=UniversalConcept.WIRELESS_MANAGEMENT,
         description="Centralized wireless access point management",
         vendor_names={
             "cisco": ["wireless", "capwap", "flexconnect"],
             "fortinet": ["wireless", "wlan"],
             "mikrotik": ["capsman", "managed by capsman"],
         },
         references=["RFC 5415"],
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
    UniversalConcept.SWITCHING: ConceptDefinition(
        concept=UniversalConcept.SWITCHING,
        description="Layer 2 switching, port configuration, and MAC learning",
        vendor_names={
            "cisco": ["switchport", "mac address-table", "vlan", "spanning-tree"],
            "fortinet": ["switch interface", "spanning-tree"],
            "mikrotik": ["etherswitch", "bridge", "interface bridge"],
        },
        references=["IEEE 802.1D", "IEEE 802.1Q"],
    ),
    UniversalConcept.OSPF: ConceptDefinition(
        concept=UniversalConcept.OSPF,
        description="Open Shortest Path First interior routing protocol",
        vendor_names={
            "cisco": ["router ospf", "ospf", "area", "network"],
            "fortinet": ["router ospf", "ospf"],
            "mikrotik": ["routing ospf", "ospf", "area"],
        },
        references=["RFC 2328", "RFC 5340"],
    ),
    UniversalConcept.IS_IS: ConceptDefinition(
        concept=UniversalConcept.IS_IS,
        description="Intermediate System to Intermediate System routing protocol",
        vendor_names={
            "cisco": ["router isis", "is-type", "net"],
            "fortinet": ["router isis"],
            "mikrotik": ["routing isis", "isis"],
        },
        references=["ISO 10589", "RFC 1195"],
    ),
    UniversalConcept.VXLAN: ConceptDefinition(
        concept=UniversalConcept.VXLAN,
        description="Virtual Extensible LAN for overlay networks",
        vendor_names={
            "cisco": ["vxlan", "segment", "nve", "vni"],
            "fortinet": ["vxlan", "interface vxlan"],
            "mikrotik": ["vxlan", "vxlan1"],
        },
        references=["RFC 7348"],
    ),
    UniversalConcept.EVPN: ConceptDefinition(
        concept=UniversalConcept.EVPN,
        description="Ethernet VPN for L2VPN and L3VPN services",
        vendor_names={
            "cisco": ["evpn", "l2vpn", "evpn instance"],
            "fortinet": ["evpn", "bgp evpn"],
            "mikrotik": ["evpn", "bgp evpn"],
        },
        references=["RFC 7432", "RFC 8365"],
    ),
    UniversalConcept.SD_WAN: ConceptDefinition(
        concept=UniversalConcept.SD_WAN,
        description="Software-Defined Wide Area Network orchestration",
        vendor_names={
            "cisco": ["sd-wan", "vsmart", "vmanage", "cEdge"],
            "fortinet": ["sd-wan", "sdwan", "performance-sla"],
            "mikrotik": ["sd-wan", "zerotier", "vxlan"],
        },
        references=["IETF SD-WAN"],
    ),
    UniversalConcept.IPV6: ConceptDefinition(
        concept=UniversalConcept.IPV6,
        description="IPv6 addressing and routing",
        vendor_names={
            "cisco": ["ipv6", "ipv6 address", "ipv6 route"],
            "fortinet": ["ipv6", "config ipv6"],
            "mikrotik": ["ipv6", "ipv6 address"],
        },
        references=["RFC 8200"],
    ),
    UniversalConcept.MULTICAST: ConceptDefinition(
        concept=UniversalConcept.MULTICAST,
        description="Multicast routing and forwarding",
        vendor_names={
            "cisco": ["ip multicast-routing", "pim", "igmp"],
            "fortinet": ["multicast", "pim"],
            "mikrotik": ["routing pim", "multicast"],
        },
        references=["RFC 7761", "RFC 3376"],
    ),
    UniversalConcept.ZERO_TRUST: ConceptDefinition(
        concept=UniversalConcept.ZERO_TRUST,
        description="Zero Trust network access and segmentation",
        vendor_names={
            "cisco": ["zero-trust", "ztpa", "identity services engine"],
            "fortinet": ["zero-trust", "fortigate", "identity"],
            "mikrotik": ["zero-trust", "radius", "certificate"],
        },
        references=["NIST SP 800-207"],
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

            for keyword in vendor_keywords:
                if keyword in raw:
                    evidence.append({"keyword": keyword, "source": "raw_config", "vendor": vendor})

            if vendor in ["cisco", "fortinet"]:
                for key in vendor_specific:
                    if any(kw in key.lower() for kw in vendor_keywords):
                        evidence.append({"keyword": key, "source": "vendor_specific", "vendor": vendor})

            if evidence:
                detected[concept] = evidence
                min(1.0, 0.5 + 0.1 * len(evidence))

        return detected

    def get_concept_definition(self, concept: UniversalConcept) -> ConceptDefinition | None:
        return self._concepts.get(concept)

    def get_all_concepts(self) -> list[UniversalConcept]:
        return list(self._concepts.keys())


concept_mapper = ConceptMapper()
