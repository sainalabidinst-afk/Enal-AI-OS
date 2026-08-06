from __future__ import annotations

from apps.infrastructure_engineer.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    InfrastructureFinding,
    Severity,
    VendorFamily,
)
from apps.infrastructure_engineer.attachments.parsers.base import BaseParser


class ArubaParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor in {VendorFamily.aruba, VendorFamily.ubiquiti}

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=meta.vendor, format="aruba_aos", device_role=meta.device_role)
        lowered = content.lower()
        for idx, line in enumerate(content.splitlines()):
            stripped = line.strip()
            if any(key in lowered for key in ["interface", "vlan", "ssid", "wlan"]):
                if "vlan" in stripped.lower():
                    ast.vlans.append({"raw": stripped[:200]})
                elif "ssid" in stripped.lower() or "wlan" in stripped.lower():
                    ast.wireless.append({"raw": stripped[:200]})
                else:
                    ast.interfaces.append({"raw": stripped[:200]})
                if "trunk" in stripped.lower():
                    evidence = [stripped]
                    ast.findings.append(InfrastructureFinding(Severity.low, "switch", "Trunk detected", "Validate allowed VLANs and native VLAN", confidence=0.7, evidence=evidence))
                if "poe" in stripped.lower():
                    evidence = [stripped]
                    ast.findings.append(InfrastructureFinding(Severity.low, "switch", "PoE detected", "Review PoE allocation and redundancy", confidence=0.6, evidence=evidence))
            if any(key in stripped.lower() for key in ["firewall", "policy", "acl"]):
                ast.firewall.append({"raw": stripped[:200]})
            if any(key in stripped.lower() for key in ["router ", "ospf", "bgp", "static-route"]):
                ast.routing.append({"raw": stripped[:200]})
        if not ast.wireless and meta.device_role.value == "wireless_controller":
            ast.findings.append(InfrastructureFinding(Severity.low, "wireless", "No wireless profiles detected", "Verify WLAN/SSID export coverage", confidence=0.5))
        return ast
