from __future__ import annotations

from backend.app.core.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    InfrastructureFinding,
    Severity,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class FortinetParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.fortinet

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.fortinet, format="fortios", device_role=meta.device_role)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if "config system interface" in stripped or stripped.startswith("edit "):
                ast.interfaces.append({"raw": stripped[:200]})
            if "config firewall policy" in stripped:
                ast.firewall.append({"raw": stripped[:200]})
            if stripped.startswith("config router "):
                ast.routing.append({"raw": stripped[:200]})
            if stripped.startswith("config system vpn"):
                ast.security.append({"raw": stripped[:200]})
            if stripped.startswith("config system ha"):
                ast.ha.append({"raw": stripped[:200]})
                evidence = [lines[i].strip() for i in range(idx, min(idx + 5, len(lines))) if lines[i].strip()][:5]
                ast.findings.append(InfrastructureFinding(Severity.low, "ha", "HA cluster detected", "Verify HA mode, priority, and heartbeat interfaces", confidence=0.7, evidence=evidence))
            if stripped.startswith("config switch"):
                if "vlan" in stripped.lower():
                    ast.vlans.append({"raw": stripped[:200]})
                evidence = [stripped]
                ast.findings.append(InfrastructureFinding(Severity.low, "switch", "Switch configuration detected", "Verify VLANs, trunk ports, and STP/RSTP", confidence=0.7, evidence=evidence))
            if "poe" in stripped.lower() and "status" in stripped.lower():
                evidence = [stripped]
                ast.findings.append(InfrastructureFinding(Severity.low, "switch", "PoE detected", "Review PoE budget and port allocation", confidence=0.6, evidence=evidence))
            if "wlan" in stripped.lower() or "ssid" in stripped.lower():
                ast.wireless.append({"raw": stripped[:200]})
        return ast
