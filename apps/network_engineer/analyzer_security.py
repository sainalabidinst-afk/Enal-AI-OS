import logging
from typing import Any

logger = logging.getLogger(__name__)


class _SecurityRuleMixin:
    def _check_default_password(self, config: Any, report: Any, vendor: str = ""):
        if any("password=" in line.lower() and ("admin" in line.lower() or "1234" in line or "password" in line.lower()) for line in config.raw_lines):
            report.add_issue("critical", "Security", "Default or weak password detected", "Change to a strong password immediately", confidence=0.9)

    def _check_unrestricted_winbox(self, config: Any, report: Any, vendor: str = ""):
        for line in config.raw_lines:
            if "winbox" in line.lower() and "0.0.0.0/0" in line:
                report.add_issue("critical", "Security", "Winbox is open to the world", "Restrict Winbox access to management IPs only", confidence=1.0)

    def _check_unrestricted_ssh(self, config: Any, report: Any, vendor: str = ""):
        for line in config.raw_lines:
            if "ssh" in line.lower() and "0.0.0.0/0" in line:
                report.add_issue("warning", "Security", "SSH is open to the world", "Restrict SSH access to management IPs", confidence=1.0)

    def _check_unrestricted_www(self, config: Any, report: Any, vendor: str = ""):
        for line in config.raw_lines:
            if "www" in line.lower() and "0.0.0.0/0" in line:
                report.add_issue("warning", "Security", "Web interface is open to the world", "Restrict web access to trusted networks", confidence=1.0)

    def _check_unrestricted_api(self, config: Any, report: Any, vendor: str = ""):
        for line in config.raw_lines:
            if "api" in line.lower() and "0.0.0.0/0" in line:
                report.add_issue("warning", "Security", "API is open to the world", "Restrict API access to trusted networks", confidence=1.0)

    def _check_high_risk_ports_open(self, config: Any, report: Any, vendor: str = ""):
        high_risk_ports = ["23", "2323", "3306", "5432", "6379", "27017"]
        for line in config.raw_lines:
            for port in high_risk_ports:
                if f"port={port}" in line and "0.0.0.0/0" in line:
                    report.add_issue("critical", "Security", f"High-risk port {port} open to world", "Close or restrict port", confidence=1.0)

    def _check_unencrypted_protocols(self, config: Any, report: Any, vendor: str = ""):
        if vendor != "mikrotik":
            return
        if any("telnet" in line.lower() for line in config.raw_lines):
            report.add_issue("critical", "Security", "Telnet is enabled (unencrypted)", "Use SSH instead of Telnet", confidence=1.0)
        if any("http" in line.lower() and "www" in line.lower() for line in config.raw_lines):
            report.add_issue("warning", "Security", "HTTP management enabled", "Use HTTPS for web management", confidence=0.9)

    def _check_ppp_without_encryption(self, config: Any, report: Any, vendor: str = ""):
        if any("ppp" in line.lower() and "encryption=no" in line.lower() for line in config.raw_lines):
            report.add_issue("critical", "PPP", "PPP without encryption", "Enable PPP encryption", confidence=1.0)

    def _check_certificate_expired(self, config: Any, report: Any, vendor: str = ""):
        if any("certificate" in line.lower() and "expired" in line.lower() for line in config.raw_lines):
            report.add_issue("critical", "Security", "Expired certificate detected", "Renew certificate immediately", confidence=1.0)

    def _check_radius_without_backup(self, config: Any, report: Any, vendor: str = ""):
        if any("radius" in line.lower() for line in config.raw_lines):
            report.add_issue("warning", "Security", "RADIUS without backup", "Add backup RADIUS server", confidence=0.8)

    def _check_wireless_open_security(self, config: Any, report: Any, vendor: str = ""):
        if any("wireless" in line.lower() and "security-profile=default" in line.lower() for line in config.raw_lines):
            report.add_issue("critical", "Wireless", "Wireless using default security", "Configure proper wireless security", confidence=1.0)

    def _check_telnet_enabled_cisco(self, config: Any, report: Any, vendor: str = ""):
        for line in config.raw_lines:
            if "telnet" in line.lower() and "disabled" not in line.lower():
                report.add_issue("critical", "Security", "Telnet is enabled (unencrypted)", "Use SSH instead of Telnet", confidence=1.0)

    def _check_wireguard_peers(self, config: Any, report: Any, vendor: str = ""):
        has_wg = any("wireguard" in line.lower() or "wg0" in line.lower() for line in config.raw_lines)
        if has_wg:
            if not any("allowed-address" in line.lower() for line in config.raw_lines):
                report.add_issue("warning", "WireGuard", "WireGuard peer without allowed-address", "Configure allowed-address for proper routing", confidence=0.9)
            if not any("persistent-keepalive" in line.lower() for line in config.raw_lines):
                report.add_issue("info", "WireGuard", "WireGuard without persistent-keepalive", "Add keepalive for NAT traversal", confidence=0.7)

    def _check_user_without_password(self, config: Any, report: Any, vendor: str = ""):
        if not any("/user" in line.lower() and "password=" in line.lower() for line in config.raw_lines):
            report.add_issue("critical", "Security", "No user password configured", "Set password for all users", confidence=0.9)

    def _check_mgmt_from_untrusted(self, config: Any, report: Any, vendor: str = ""):
        if vendor != "mikrotik":
            return
        mgmt_services = ["winbox", "ssh", "www", "api"]
        for svc in config.metadata.get("ip_services", []):
            if svc.get("name") in mgmt_services and svc.get("address") == "0.0.0.0/0":
                report.add_issue("critical", "Security", f"Management service {svc.get('name')} accessible from anywhere", "Restrict to management subnet", confidence=1.0)

    def _check_weak_password_in_comment(self, config: Any, report: Any, vendor: str = ""):
        for line in config.raw_lines:
            if "password=" in line.lower():
                import re
                comment_match = re.search(r'comment="([^"]*)"', line, re.IGNORECASE)
                if comment_match and any(word in comment_match.group(1).lower() for word in ["password", "secret", "admin"]):
                    report.add_issue("warning", "Security", "Password exposed in comment", "Remove password from comments", confidence=0.8)
