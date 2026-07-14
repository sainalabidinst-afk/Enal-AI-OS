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


class UniFiWirelessParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.ubiquiti and "unifi" in meta.text_preview.lower() or meta.filename.lower().startswith("unifi")

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.ubiquiti, format="unifi", device_role=DeviceRole.wireless_controller)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if "ssid" in stripped.lower():
                ast.wireless.append({"raw": stripped[:200]})
                if "wpa" not in stripped.lower() and "encryption" not in stripped.lower():
                    evidence = [stripped]
                    ast.findings.append(InfrastructureFinding(Severity.high, "wireless", "SSID without WPA/WPA2/WPA3 detected", "Enable WPA3 or at minimum WPA2-PSK", confidence=0.8, evidence=evidence))
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
            if "captive" in stripped.lower() or "portal" in stripped.lower():
                ast.wireless.append({"type": "captive_portal", "raw": stripped[:200]})
        return ast