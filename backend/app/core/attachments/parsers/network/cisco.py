from __future__ import annotations

import re

from backend.app.core.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    InfrastructureFinding,
    Severity,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class CiscoIOSParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.cisco

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.cisco, format="cisco_ios", device_role=meta.device_role)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("interface "):
                ast.interfaces.append({"raw": stripped[:200]})
                if idx + 1 < len(lines):
                    next_line = lines[idx + 1].strip().lower()
                    if "switchport mode trunk" in next_line:
                        evidence = [stripped, lines[idx + 1].strip()]
                        ast.findings.append(InfrastructureFinding(Severity.medium, "switch", f"Trunk detected on {stripped}", "Validate allowed VLAN list and pruning", confidence=0.8, evidence=evidence))
                    elif "switchport mode access" in next_line:
                        evidence = [stripped, lines[idx + 1].strip()]
                        ast.findings.append(InfrastructureFinding(Severity.low, "switch", f"Access port detected on {stripped}", "Verify access VLAN and port security", confidence=0.8, evidence=evidence))
                    if "spanning-tree" in next_line or "stp" in next_line:
                        evidence = [stripped, lines[idx + 1].strip()]
                        ast.findings.append(InfrastructureFinding(Severity.low, "switch", "STP configuration detected", f"Review STP mode on {stripped}", confidence=0.7, evidence=evidence))
                    if "channel-group" in next_line:
                        evidence = [stripped, lines[idx + 1].strip()]
                        ast.findings.append(InfrastructureFinding(Severity.low, "switch", "LACP/bundle detected", f"Verify LACP configuration on {stripped}", confidence=0.7, evidence=evidence))
                    if "power inline" in next_line:
                        evidence = [stripped, lines[idx + 1].strip()]
                        ast.findings.append(InfrastructureFinding(Severity.low, "switch", "PoE detected", f"Verify PoE allocation on {stripped}", confidence=0.7, evidence=evidence))
                    if "switchport voice vlan" in next_line:
                        evidence = [stripped, lines[idx + 1].strip()]
                        ast.findings.append(InfrastructureFinding(Severity.low, "switch", "Voice VLAN detected", f"Verify voice VLAN on {stripped}", confidence=0.7, evidence=evidence))
            if "access-list" in stripped or "ip access-list" in stripped:
                ast.firewall.append({"raw": stripped[:200]})
            if stripped.startswith("router ospf") or stripped.startswith("router bgp"):
                ast.routing.append({"raw": stripped[:200]})
            if "vlan" in stripped.lower() and stripped:
                if re.search(r"vlan\s+\d+", stripped, re.IGNORECASE):
                    ast.vlans.append({"raw": stripped[:200]})
        return ast
