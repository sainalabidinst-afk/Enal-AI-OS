from __future__ import annotations

import re

from apps.infrastructure_engineer.attachments.models import (
    AttachmentMeta,
    DeviceRole,
    InfrastructureAST,
    InfrastructureFinding,
    Severity,
    VendorFamily,
)
from apps.infrastructure_engineer.attachments.parsers.base import BaseParser


class HPEProCurveParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.hp or "procurve" in meta.text_preview.lower() or "hp" in meta.text_preview.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.hp, format="procurve", device_role=DeviceRole.switch)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if re.match(r"^interface .+", stripped):
                ast.interfaces.append({"raw": stripped[:200]})
                next_line = lines[idx + 1].strip() if idx + 1 < len(lines) else ""
                if "trunk" in next_line.lower():
                    evidence = [stripped, next_line]
                    ast.findings.append(InfrastructureFinding(Severity.low, "switch", "Trunk detected", "Validate allowed VLANs", confidence=0.7, evidence=evidence))
            if "vlan" in stripped.lower():
                ast.vlans.append({"raw": stripped[:200]})
            if stripped.startswith("spanning-tree"):
                evidence = [stripped]
                ast.findings.append(InfrastructureFinding(Severity.low, "switch", "STP detected", "Verify spanning-tree protection", confidence=0.7, evidence=evidence))
        return ast
