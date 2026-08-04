import logging
from typing import Any

logger = logging.getLogger(__name__)


class _VendorRuleMixin:
    def _check_fortinet_firewall_policy(self, config: Any, report: Any, vendor: str = ""):
        has_fortinet_fw = any("config firewall policy" in line.lower() or "firewall policy" in line.lower() for line in config.raw_lines)
        if has_fortinet_fw:
            for line in config.raw_lines:
                if "telnet" in line.lower() and "deny" not in line.lower():
                    report.add_issue("critical", "Security", "Fortinet firewall may allow Telnet", "Block Telnet in firewall policy", confidence=0.9)

    def _check_fortinet_vpn_ipsec(self, config: Any, report: Any, vendor: str = ""):
        for line in config.raw_lines:
            if "config vpn ipsec" in line.lower() or "vpn ipsec phase1" in line.lower():
                report.add_issue("info", "VPN", "Fortinet IPSec VPN configured", "Verify VPN phase1/phase2 settings", confidence=0.9)

    def _check_fortinet_ha_configured(self, config: Any, report: Any, vendor: str = ""):
        has_ha = any("config system ha" in line.lower() or ("mode a-a" in line.lower() or "mode a-p" in line.lower()) for line in config.raw_lines)
        if has_ha:
            report.add_issue("info", "High Availability", "Fortinet HA configured", "Verify HA cluster settings", confidence=0.9)

    def _check_ipsec_configured_cisco(self, config: Any, report: Any, vendor: str = ""):
        has_ipsec = any("crypto isakmp" in line.lower() or "crypto map" in line.lower() for line in config.raw_lines)
        if has_ipsec:
            report.add_issue("info", "VPN", "IPSec VPN configured", "Verify IPSec configuration for security compliance", confidence=0.9)

    def _check_hsrp_configured_cisco(self, config: Any, report: Any, vendor: str = ""):
        for line in config.raw_lines:
            if "standby" in line.lower() and "ip" in line.lower():
                report.add_issue("info", "High Availability", "HSRP configured", "Verify HSRP authentication and preemption", confidence=0.9)
