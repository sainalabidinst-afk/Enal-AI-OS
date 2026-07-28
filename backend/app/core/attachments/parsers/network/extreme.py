from __future__ import annotations

from backend.app.core.attachments.models import (
    AttachmentMeta,
    DeviceRole,
    InfrastructureAST,
    InfrastructureFinding,
    Severity,
    VendorFamily,
)
from backend.app.core.attachments.parsers.base import BaseParser


class ExtremeNetworksParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.extreme or "extreme" in meta.text_preview.lower() or "extremexos" in meta.text_preview.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.extreme, format="extremexos", device_role=DeviceRole.switch)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("create vlan "):
                ast.vlans.append({"raw": stripped[:200]})
            if stripped.startswith("configure ports "):
                ast.interfaces.append({"raw": stripped[:200]})
            if "stp" in stripped.lower():
                ast.findings.append(InfrastructureFinding(Severity.low, "switch", "STP detected", "Verify spanning-tree protection", confidence=0.7, evidence=[stripped]))
        return ast
