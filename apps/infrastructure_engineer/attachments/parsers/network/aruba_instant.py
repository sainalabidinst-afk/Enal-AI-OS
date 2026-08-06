from __future__ import annotations

from apps.infrastructure_engineer.attachments.models import (
    AttachmentMeta,
    DeviceRole,
    InfrastructureAST,
    InfrastructureFinding,
    Severity,
    VendorFamily,
)
from apps.infrastructure_engineer.attachments.parsers.base import BaseParser


class ArubaInstantParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.aruba and "instant" in meta.text_preview.lower() or "aruba instant" in meta.text_preview.lower()

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.aruba, format="aruba_instant", device_role=DeviceRole.wireless_controller)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if "ssid" in stripped.lower() or "essid" in stripped.lower():
                ast.wireless.append({"raw": stripped[:200]})
                if "wpa" not in stripped.lower() and "aes" not in stripped.lower():
                    evidence = [stripped]
                    ast.findings.append(InfrastructureFinding(Severity.high, "wireless", "SSID without strong encryption detected", "Enable WPA3 or WPA2-AES", confidence=0.8, evidence=evidence))
            if "channel" in stripped.lower():
                ast.wireless.append({"type": "channel", "raw": stripped[:200]})
            if "dfs" in stripped.lower():
                ast.wireless.append({"type": "dfs", "raw": stripped[:200]})
            if "tx-power" in stripped.lower() or "txpower" in stripped.lower():
                ast.wireless.append({"type": "tx_power", "raw": stripped[:200]})
            if "band" in stripped.lower() or "5ghz" in stripped.lower() or "2.4ghz" in stripped.lower():
                ast.wireless.append({"type": "band", "raw": stripped[:200]})
            if "roaming" in stripped.lower():
                ast.wireless.append({"type": "roaming", "raw": stripped[:200]})
            if "mesh" in stripped.lower():
                ast.wireless.append({"type": "mesh", "raw": stripped[:200]})
        return ast
