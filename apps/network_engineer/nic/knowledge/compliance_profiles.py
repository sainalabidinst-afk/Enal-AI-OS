"""
Compliance Profiles
====================

Cross-vendor compliance profiles (CIS, NIST, PCI DSS, ISP Best Practice, SMB Best Practice).
All profiles operate on Universal AST, making them vendor-agnostic.
"""

import logging

from apps.network_engineer.nic.knowledge.compliance_models import (
    ComplianceProfile,
    ComplianceRule,
)
from apps.network_engineer.nic.knowledge.ontology import UniversalConcept

logger = logging.getLogger(__name__)


class CISProfile(ComplianceProfile):
    name = "CIS"
    description = "CIS Benchmarks for network devices"

    def get_rules(self) -> list[ComplianceRule]:
        return [
            ComplianceRule(
                id="CIS-1.1",
                name="SSH Restricted",
                description="SSH must not be open to 0.0.0.0/0",
                severity="critical",
                concept=UniversalConcept.TRAFFIC_FILTERING,
                references=["CIS Benchmark 1.1"],
            ),
            ComplianceRule(
                id="CIS-1.2",
                name="Telnet Disabled",
                description="Telnet must not be enabled",
                severity="critical",
                concept=UniversalConcept.TRAFFIC_FILTERING,
                references=["CIS Benchmark 1.2"],
            ),
            ComplianceRule(
                id="CIS-1.3",
                name="Admin Password Set",
                description="Admin password must be set and strong",
                severity="critical",
                concept=UniversalConcept.AUTHENTICATION,
                references=["CIS Benchmark 1.3"],
            ),
            ComplianceRule(
                id="CIS-2.1",
                name="NTP Enabled",
                description="NTP must be enabled for accurate timekeeping",
                severity="warning",
                concept=UniversalConcept.TIME_SYNCHRONIZATION,
                references=["CIS Benchmark 2.1"],
            ),
            ComplianceRule(
                id="CIS-2.2",
                name="Logging Enabled",
                description="Logging must be enabled for audit trail",
                severity="warning",
                concept=UniversalConcept.LOGGING,
                references=["CIS Benchmark 2.2"],
            ),
            ComplianceRule(
                id="CIS-2.3",
                name="Backup Configured",
                description="Backup must be configured and tested",
                severity="warning",
                concept=UniversalConcept.BACKUP,
                references=["CIS Benchmark 2.3"],
            ),
            ComplianceRule(
                id="CIS-3.1",
                name="Unused Interfaces Disabled",
                description="Unused interfaces should be disabled",
                severity="info",
                concept=UniversalConcept.IP_MANAGEMENT,
                references=["CIS Benchmark 3.1"],
            ),
            ComplianceRule(
                id="CIS-3.2",
                name="HA or Redundancy Configured",
                description="Critical devices should have HA/redundancy",
                severity="warning",
                concept=UniversalConcept.HIGH_AVAILABILITY,
                references=["CIS Benchmark 3.3"],
            ),
            ComplianceRule(
                id="CIS-4.1",
                name="Firewall Rules Exist",
                description="Firewall/filter rules must be configured",
                severity="critical",
                concept=UniversalConcept.TRAFFIC_FILTERING,
                references=["CIS Benchmark 4.1"],
            ),
            ComplianceRule(
                id="CIS-4.2",
                name="NAT or Private Addressing",
                description="Internal addresses should use RFC 1918 private space",
                severity="warning",
                concept=UniversalConcept.ADDRESS_TRANSLATION,
                references=["CIS Benchmark 4.2"],
            ),
        ]


class NISTProfile(ComplianceProfile):
    name = "NIST"
    description = "NIST SP 800-53 Security Controls"

    def get_rules(self) -> list[ComplianceRule]:
        return [
            ComplianceRule(
                id="NIST-AC-2",
                name="Account Management",
                description="Account management policies must be enforced",
                severity="warning",
                concept=UniversalConcept.AUTHENTICATION,
                references=["NIST SP 800-53 AC-2"],
            ),
            ComplianceRule(
                id="NIST-AC-3",
                name="Access Enforcement",
                description="Access enforcement mechanisms must be in place",
                severity="warning",
                concept=UniversalConcept.TRAFFIC_FILTERING,
                references=["NIST SP 800-53 AC-3"],
            ),
            ComplianceRule(
                id="NIST-SI-4",
                name="System Monitoring",
                description="System monitoring must be enabled",
                severity="warning",
                concept=UniversalConcept.MONITORING,
                references=["NIST SP 800-53 SI-4"],
            ),
            ComplianceRule(
                id="NIST-CP-2",
                name="Contingency Plan",
                description="Contingency and backup plans must exist",
                severity="warning",
                concept=UniversalConcept.BACKUP,
                references=["NIST SP 800-53 CP-2"],
            ),
        ]


class PCIDSSProfile(ComplianceProfile):
    name = "PCI-DSS"
    description = "PCI DSS v4.0 for payment card networks"

    def get_rules(self) -> list[ComplianceRule]:
        return [
            ComplianceRule(
                id="PCI-6.1",
                name="Firewall Rules",
                description="Firewall rules must restrict inbound/outbound traffic",
                severity="critical",
                concept=UniversalConcept.TRAFFIC_FILTERING,
                references=["PCI DSS 6.1"],
            ),
            ComplianceRule(
                id="PCI-6.2",
                name="Secure Network Protocols",
                description="Only secure protocols should be used",
                severity="critical",
                concept=UniversalConcept.TRAFFIC_FILTERING,
                references=["PCI DSS 6.2"],
            ),
            ComplianceRule(
                id="PCI-10.1",
                name="Audit Trail",
                description="Audit trail must be enabled and retained",
                severity="warning",
                concept=UniversalConcept.LOGGING,
                references=["PCI DSS 10.1"],
            ),
            ComplianceRule(
                id="PCI-10.6",
                name="Review Logs",
                description="Security logs must be reviewed regularly",
                severity="warning",
                concept=UniversalConcept.MONITORING,
                references=["PCI DSS 10.6"],
            ),
        ]


class ISPBestPracticeProfile(ComplianceProfile):
    name = "ISP-Best-Practice"
    description = "Best practices for ISP and enterprise networks"

    def get_rules(self) -> list[ComplianceRule]:
        return [
            ComplianceRule(
                id="ISP-1.1",
                name="High Availability",
                description="Critical routers should have VRRP/HSRP/HA configured",
                severity="warning",
                concept=UniversalConcept.HIGH_AVAILABILITY,
            ),
            ComplianceRule(
                id="ISP-1.2",
                name="QoS Configured",
                description="QoS should be configured for traffic prioritization",
                severity="warning",
                concept=UniversalConcept.QOS,
            ),
            ComplianceRule(
                id="ISP-2.1",
                name="BGP or OSPF",
                description="Dynamic routing should be used for resilience",
                severity="info",
                concept=UniversalConcept.ROUTING,
            ),
            ComplianceRule(
                id="ISP-3.1",
                name="Monitoring Enabled",
                description="SNMP and logging should be enabled",
                severity="warning",
                concept=UniversalConcept.MONITORING,
            ),
            ComplianceRule(
                id="ISP-4.1",
                name="Backup Configured",
                description="Automated backups should be configured",
                severity="warning",
                concept=UniversalConcept.BACKUP,
            ),
        ]


class SMBBestPracticeProfile(ComplianceProfile):
    name = "SMB-Best-Practice"
    description = "Best practices for small and medium business networks"

    def get_rules(self) -> list[ComplianceRule]:
        return [
            ComplianceRule(
                id="SMB-1.1",
                name="Firewall Enabled",
                description="Firewall must be enabled and configured",
                severity="critical",
                concept=UniversalConcept.TRAFFIC_FILTERING,
            ),
            ComplianceRule(
                id="SMB-1.2",
                name="Strong Passwords",
                description="Admin passwords must be strong",
                severity="critical",
                concept=UniversalConcept.AUTHENTICATION,
            ),
            ComplianceRule(
                id="SMB-2.1",
                name="Firmware Updated",
                description="Device firmware should be up to date",
                severity="warning",
                concept=UniversalConcept.SYSTEM_IDENTITY,
            ),
            ComplianceRule(
                id="SMB-3.1",
                name="VLAN Segmented",
                description="Network should be segmented with VLANs",
                severity="info",
                concept=UniversalConcept.VLAN,
            ),
        ]


PROFILES: dict[str, ComplianceProfile] = {
    "CIS": CISProfile(),
    "NIST": NISTProfile(),
    "PCI-DSS": PCIDSSProfile(),
    "ISP-Best-Practice": ISPBestPracticeProfile(),
    "SMB-Best-Practice": SMBBestPracticeProfile(),
}
