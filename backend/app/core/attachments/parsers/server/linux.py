from __future__ import annotations


from backend.app.core.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    InfrastructureFinding,
    Severity,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class LinuxParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.linux or meta.filename.lower().endswith(
            (".conf", ".cfg", ".log", ".sh", ".txt")
        )

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.linux, format="linux", device_role=meta.device_role)
        lowered = content.lower()
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if any(key in lowered for key in ["ip addr", "inet ", "interface"]):
                ast.interfaces.append({"raw": stripped[:200]})
            if any(key in stripped.lower() for key in ["iptables", "nft", "firewall"]):
                ast.firewall.append({"raw": stripped[:200]})
            if any(key in stripped.lower() for key in ["systemctl", "service ", "active ", "running"]):
                ast.services.append({"raw": stripped[:200]})
            if any(key in stripped.lower() for key in ["user ", "group ", "sudo", "password"]):
                ast.security.append({"raw": stripped[:200]})
            if "permit rootlogin" in lowered and "no" not in lowered:
                evidence = [line for line in lines if "permit rootlogin" in line.lower()][:3]
                ast.findings.append(InfrastructureFinding(Severity.high, "security", "SSH root login may be permitted", "Disable PermitRootLogin in sshd_config", confidence=0.8, evidence=evidence))
            if "password authentication" in lowered and "no" not in lowered:
                evidence = [line for line in lines if "passwordauthentication" in line.lower()][:3]
                ast.findings.append(InfrastructureFinding(Severity.high, "security", "SSH password authentication may be enabled", "Disable PasswordAuthentication in sshd_config", confidence=0.8, evidence=evidence))
        if "journalctl" in lowered or "syslog" in lowered:
            ast.system["log_source"] = "journalctl/syslog"
        return ast
