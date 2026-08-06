from __future__ import annotations

from apps.infrastructure_engineer.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    InfrastructureFinding,
    Severity,
    VendorFamily,
)
from apps.infrastructure_engineer.attachments.parsers.base import BaseParser


class HuaweiParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.huawei

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.huawei, format="vrp", device_role=meta.device_role)
        for idx, line in enumerate(content.splitlines()):
            stripped = line.strip()
            if stripped.startswith("interface "):
                ast.interfaces.append({"raw": stripped[:200]})
                if "trunk" in stripped.lower() or "port trunk" in stripped.lower():
                    evidence = [stripped]
                    ast.findings.append(InfrastructureFinding(Severity.low, "switch", "Trunk detected", "Validate allowed VLANs and native VLAN", confidence=0.7, evidence=evidence))
                if "poe" in stripped.lower():
                    evidence = [stripped]
                    ast.findings.append(InfrastructureFinding(Severity.low, "switch", "PoE detected", "Review PoE allocation", confidence=0.6, evidence=evidence))
            if "vlan" in stripped.lower():
                ast.vlans.append({"raw": stripped[:200]})
            if any(key in stripped.lower() for key in ["acl", "firewall", "policy"]):
                ast.firewall.append({"raw": stripped[:200]})
            if any(key in stripped.lower() for key in ["ospf", "bgp", "rip", "isis"]):
                ast.routing.append({"raw": stripped[:200]})
            if "stp" in stripped.lower() or "spanning-tree" in stripped.lower():
                evidence = [stripped]
                ast.findings.append(InfrastructureFinding(Severity.low, "switch", "STP detected", "Verify spanning-tree protection", confidence=0.7, evidence=evidence))
        return ast
