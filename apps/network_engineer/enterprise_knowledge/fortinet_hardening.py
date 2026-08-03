"""
Fortinet Hardening
===================

FortiOS security, policy optimization, VPN design, threat protection,
and logging best practices.

Reference: Fortinet Security Best Practices, FortiOS Hardening Guide
"""

import logging
from typing import Any

from apps.network_engineer.enterprise_knowledge.base import EnterpriseKnowledgeFinding

logger = logging.getLogger(__name__)


class FortinetHardeningAnalyzer:
    """
    Fortinet FortiOS security hardening analysis:
    - FortiOS security best practices
    - Policy optimization
    - VPN design (IPsec, SSL)
    - Threat protection integration
    - Logging and analytics
    """

    def analyze(self, config: object) -> list[EnterpriseKnowledgeFinding]:
        findings: list[EnterpriseKnowledgeFinding] = []
        raw = "\n".join(getattr(config, "raw_lines", [])).lower()

        vendor = getattr(config, "vendor", "") or ""
        if vendor != "fortinet":
            return findings

        findings.extend(self._check_fortios_security(raw, config))
        findings.extend(self._check_policy_optimization(raw, config))
        findings.extend(self._check_vpn_design(raw, config))
        findings.extend(self._check_threat_protection(raw, config))
        findings.extend(self._check_logging_analytics(raw, config))

        return findings

    def _check_fortios_security(self, raw: str, config: object) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_admin_hardening = any(kw in raw for kw in [
            "admin-hardening", "admin-ssh", "admin-https", "admin-lockout",
        ])
        has_strong_admin = any(kw in raw for kw in [
            "admin-strong-password", "password-policy", "min-len",
        ])
        has_trusted_hosts = "trusted-host" in raw or "trusthost" in raw
        has_auto_update = "auto-update" in raw or "fortiguard" in raw

        if not has_admin_hardening:
            findings.append(EnterpriseKnowledgeFinding(
                domain="fortinet_hardening", category="admin_access", severity="warning",
                description="FortiOS admin hardening not configured",
                recommendation=(
                    "Enable admin-hardening: set admin-ssh, admin-https, admin-lockout-threshold, "
                    "admin-lockout-duration. Use 'config system admin' for granular control."
                ),
                confidence=0.85, vendor="fortinet",
                references=["FortiOS Hardening Guide", "CIS Fortinet Benchmark"],
            ))
        if not has_strong_admin:
            findings.append(EnterpriseKnowledgeFinding(
                domain="fortinet_hardening", category="admin_access", severity="warning",
                description="Admin password policy not configured",
                recommendation=(
                    "Configure password policy: set min-len, require special characters, "
                    "enable admin-strong-password. Use 'config system password-policy'."
                ),
                confidence=0.8, vendor="fortinet",
                references=["FortiOS Password Policy Guide"],
            ))
        if not has_trusted_hosts:
            findings.append(EnterpriseKnowledgeFinding(
                domain="fortinet_hardening", category="admin_access", severity="warning",
                description="No trusted hosts configured for admin access",
                recommendation=(
                    "Restrict admin access to specific IP addresses using trusted-host. "
                    "Use 'config system admin edit admin set trusthost1 10.0.0.0/24'."
                ),
                confidence=0.9, vendor="fortinet",
                references=["FortiOS Admin Access Restriction"],
            ))
        if not has_auto_update:
            findings.append(EnterpriseKnowledgeFinding(
                domain="fortinet_hardening", category="system_security", severity="suggestion",
                description="FortiGuard auto-update not configured",
                recommendation=(
                    "Enable FortiGuard automatic updates for AV, IPS, application control, "
                    "and web filtering signatures."
                ),
                confidence=0.7, vendor="fortinet",
                references=["FortiGuard Update Guide"],
            ))
        return findings

    def _check_policy_optimization(self, raw: str, config: object) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_firewall_policy = "config firewall policy" in raw
        has_application_control = "application-control" in raw or "app-control" in raw
        has_ssl_inspection = "ssl-inspection" in raw or "deep-inspection" in raw
        has_identity = "identity-based" in raw or "user-group" in raw or "fsso" in raw

        if has_firewall_policy:
            policy_count = raw.count("edit ")
            if policy_count > 50:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="fortinet_hardening", category="policy_optimization", severity="suggestion",
                    description=f"Large number of firewall policies ({policy_count}) — review for consolidation",
                    recommendation=(
                        "Consolidate firewall policies using policy objects (address groups, "
                        "service groups). Remove unused policies."
                    ),
                    confidence=0.65, vendor="fortinet",
                    references=["Fortinet Policy Optimization Guide"],
                ))
            if not has_application_control:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="fortinet_hardening", category="policy_optimization", severity="warning",
                    description="Application control not enabled on firewall policies",
                    recommendation=(
                        "Enable application control to identify and control applications "
                        "regardless of port/protocol."
                    ),
                    confidence=0.8, vendor="fortinet",
                    references=["Fortinet Application Control Guide"],
                ))
            if not has_ssl_inspection:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="fortinet_hardening", category="policy_optimization", severity="warning",
                    description="SSL inspection not configured — encrypted traffic blind spot",
                    recommendation=(
                        "Enable SSL/SSH inspection to detect threats in encrypted traffic. "
                        "Use 'config firewall ssl-ssh-profile' with deep-inspection."
                    ),
                    confidence=0.85, vendor="fortinet",
                    references=["FortiGate SSL Inspection Guide"],
                ))
            if not has_identity:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="fortinet_hardening", category="policy_optimization", severity="suggestion",
                    description="Identity-based policies not configured",
                    recommendation=(
                        "Use identity-based policies with FSSO or LDAP integration "
                        "for user-aware firewall rules."
                    ),
                    confidence=0.7, vendor="fortinet",
                    references=["Fortinet Identity-Based Policy Guide"],
                ))
        return findings

    def _check_vpn_design(self, raw: str, config: object) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_ipsec = "vpn ipsec" in raw or "ipsec phase1" in raw or "ipsec phase2" in raw
        has_ssl_vpn = "vpn ssl" in raw or "ssl-vpn" in raw or "web-portal" in raw
        has_ikev2 = "ikev2" in raw or "ike-version 2" in raw
        has_dpd = "dpd" in raw or "dead-peer-detection" in raw
        has_nat_traversal = "nat-traversal" in raw or "nat-traversal-mode" in raw

        if has_ipsec:
            findings.append(EnterpriseKnowledgeFinding(
                domain="fortinet_hardening", category="vpn_design", severity="info",
                description="IPsec VPN configured",
                recommendation=(
                    "Use IKEv2 with strong encryption (AES-256-GCM, SHA-256, DH-14/21). "
                    "Enable DPD and NAT traversal for reliability."
                ),
                confidence=0.85, vendor="fortinet",
                references=["Fortinet IPsec VPN Guide", "RFC 7296"],
            ))
            if not has_ikev2:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="fortinet_hardening", category="vpn_design", severity="warning",
                    description="IPsec using IKEv1 — upgrade to IKEv2 recommended",
                    recommendation=(
                        "IKEv2 provides built-in NAT traversal, MOBIKE, and improved security. "
                        "Use 'set ike-version 2' in phase1-interface."
                    ),
                    confidence=0.8, vendor="fortinet",
                    references=["Fortinet IKEv2 Migration Guide"],
                ))
            if not has_dpd:
                findings.append(EnterpriseKnowledgeFinding(
                    domain="fortinet_hardening", category="vpn_design", severity="warning",
                    description="IPsec without DPD (Dead Peer Detection)",
                    recommendation=(
                        "Enable DPD to detect peer failures and trigger failover. "
                        "Use 'set dpd on-idle' in phase1-interface."
                    ),
                    confidence=0.85, vendor="fortinet",
                    references=["Fortinet IPsec DPD Guide"],
                ))
        if has_ssl_vpn:
            findings.append(EnterpriseKnowledgeFinding(
                domain="fortinet_hardening", category="vpn_design", severity="info",
                description="SSL VPN configured",
                recommendation=(
                    "Use FortiClient for SSL VPN with two-factor authentication. "
                    "Enable host-check and endpoint compliance."
                ),
                confidence=0.85, vendor="fortinet",
                references=["Fortinet SSL VPN Best Practices"],
            ))
        return findings

    def _check_threat_protection(self, raw: str, config: object) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_ips = "ips" in raw or "ips-sensor" in raw or "intrusion-prevention" in raw
        has_av = "antivirus" in raw or "av-profile" in raw
        has_waf = "waf" in raw or "web-application-firewall" in raw
        has_fortisandbox = "fortisandbox" in raw or "sandbox" in raw

        if not has_ips:
            findings.append(EnterpriseKnowledgeFinding(
                domain="fortinet_hardening", category="threat_protection", severity="warning",
                description="IPS (Intrusion Prevention System) not configured",
                recommendation=(
                    "Enable IPS on all internet-facing policies. "
                    "Use 'config ips sensor' with protect-client profile."
                ),
                confidence=0.9, vendor="fortinet",
                references=["Fortinet IPS Guide"],
            ))
        if not has_av:
            findings.append(EnterpriseKnowledgeFinding(
                domain="fortinet_hardening", category="threat_protection", severity="warning",
                description="Antivirus scanning not configured",
                recommendation=(
                    "Enable antivirus scanning on all relevant policies. "
                    "Use 'config antivirus profile' with flow-based and proxy-based scanning."
                ),
                confidence=0.85, vendor="fortinet",
                references=["Fortinet Antivirus Guide"],
            ))
        if not has_fortisandbox:
            findings.append(EnterpriseKnowledgeFinding(
                domain="fortinet_hardening", category="threat_protection", severity="suggestion",
                description="FortiSandbox not integrated — advanced threat detection missing",
                recommendation=(
                    "Integrate FortiSandbox for advanced threat detection. "
                    "Configure 'config system fortisandbox' for automated file submission."
                ),
                confidence=0.7, vendor="fortinet",
                references=["Fortinet FortiSandbox Integration"],
            ))
        return findings

    def _check_logging_analytics(self, raw: str, config: object) -> list[EnterpriseKnowledgeFinding]:
        findings = []
        has_logging = "log" in raw or "logdisk" in raw or "syslog" in raw
        has_fortianalyzer = "fortianalyzer" in raw or "analytics" in raw
        has_log_forward = "log-forward" in raw or "syslog" in raw
        has_audit = "audit" in raw or "event-log" in raw

        if not has_logging:
            findings.append(EnterpriseKnowledgeFinding(
                domain="fortinet_hardening", category="logging", severity="warning",
                description="Logging not configured on FortiGate",
                recommendation=(
                    "Configure logging: enable local logging, set log-rotation, "
                    "and forward logs to FortiAnalyzer or syslog server."
                ),
                confidence=0.9, vendor="fortinet",
                references=["Fortinet Logging Guide"],
            ))
        if not has_fortianalyzer:
            findings.append(EnterpriseKnowledgeFinding(
                domain="fortinet_hardening", category="logging", severity="suggestion",
                description="FortiAnalyzer not configured for centralized logging",
                recommendation=(
                    "Deploy FortiAnalyzer for centralized log collection, "
                    "reporting, and event correlation across all FortiGates."
                ),
                confidence=0.7, vendor="fortinet",
                references=["Fortinet FortiAnalyzer Guide"],
            ))
        if not has_log_forward:
            findings.append(EnterpriseKnowledgeFinding(
                domain="fortinet_hardening", category="logging", severity="suggestion",
                description="External logging not configured — no SIEM integration",
                recommendation=(
                    "Forward logs to SIEM or syslog server for centralized monitoring. "
                    "Use 'config log syslogd' for syslog forwarding."
                ),
                confidence=0.75, vendor="fortinet",
                references=["Fortinet Syslog Integration"],
            ))
        return findings


fortinet_hardening_analyzer = FortinetHardeningAnalyzer()
