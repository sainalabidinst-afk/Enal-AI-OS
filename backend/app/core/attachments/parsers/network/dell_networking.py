from __future__ import annotations

import re

from backend.app.core.attachments.models import (
    AttachmentMeta,
    DeviceRole,
    InfrastructureAST,
    InfrastructureFinding,
    Severity,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class DellNetworkingParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.dell or "dell networking" in meta.text_preview.lower() or "smart fabric" in meta.text_preview.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.dell, format="dell_os", device_role=DeviceRole.switch)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if re.match(r"^interface .+", stripped):
                ast.interfaces.append({"raw": stripped[:200]})
                next_line = lines[idx + 1].strip() if idx + 1 < len(lines) else ""
                if "switchport mode trunk" in next_line.lower():
                    evidence = [stripped, next_line]
                    ast.findings.append(InfrastructureFinding(Severity.low, "switch", "Trunk detected", "Validate allowed VLANs and native VLAN", confidence=0.7, evidence=evidence))
                if "poe" in next_line.lower():
                    evidence = [stripped, next_line]
                    ast.findings.append(InfrastructureFinding(Severity.low, "switch", "PoE detected", "Review PoE allocation", confidence=0.6, evidence=evidence))
            if "vlan" in stripped.lower():
                ast.vlans.append({"raw": stripped[:200]})
            if "acl" in stripped.lower() or "firewall" in stripped.lower():
                ast.firewall.append({"raw": stripped[:200]})
            if "stp" in stripped.lower() or "spanning-tree" in stripped.lower():
                evidence = [stripped]
                ast.findings.append(InfrastructureFinding(Severity.low, "switch", "STP detected", "Verify spanning-tree protection", confidence=0.7, evidence=evidence))
        return ast