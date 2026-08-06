from __future__ import annotations

import re

from apps.infrastructure_engineer.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    InfrastructureFinding,
    Severity,
    VendorFamily,
)
from apps.infrastructure_engineer.attachments.parsers.base import BaseParser


class MikroTikParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.mikrotik or meta.filename.lower().endswith((".rsc", ".backup", ".export"))

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.mikrotik, format="routeros", device_role=meta.device_role)
        lowered = content.lower()

        def section(marker: str) -> list[str]:
            parts: list[str] = []
            idx = content.find(marker)
            while idx != -1:
                end = content.find("\n/", idx + 1)
                if end == -1:
                    end = len(content)
                parts.append(content[idx:end])
                idx = content.find(marker, end + 1)
            return parts

        for part in section("/interface"):
            if "address=" in part:
                match = re.search(r"address=([\d./]+)", part)
                if match:
                    ast.interfaces.append({"address": match.group(1), "raw": part[:200]})
            if "vlan=" in part.lower():
                match = re.search(r"vlan=([^,\s]+)", part)
                if match:
                    ast.vlans.append({"id": match.group(1), "raw": part[:200]})
            if "master-port=" in part.lower() or "slave=" in part.lower():
                evidence = [line.strip() for line in part.splitlines()[:3] if line.strip()]
                ast.findings.append(InfrastructureFinding(Severity.low, "switch", "Bridge bonding/LACP detected", "Verify bridge port roles and redundancy", confidence=0.7, evidence=evidence))
            if "poe=" in part.lower() or "poe-out" in part.lower():
                evidence = [line.strip() for line in part.splitlines()[:3] if line.strip()]
                ast.findings.append(InfrastructureFinding(Severity.low, "switch", "PoE detected", "Review PoE contract vs device load", confidence=0.7, evidence=evidence))

        for part in section("/ip firewall"):
            ast.firewall.append({"raw": part[:200]})
            if "input" in part and "accept" not in part:
                evidence = [line.strip() for line in part.splitlines()[:5] if line.strip()]
                ast.findings.append(InfrastructureFinding(Severity.high, "firewall", "Restrictive input chain", "Review firewall input chain policy", confidence=0.7, evidence=evidence))

        for part in section("/routing ospf"):
            ast.routing.append({"protocol": "ospf", "raw": part[:200]})
        for part in section("/routing bgp"):
            ast.routing.append({"protocol": "bgp", "raw": part[:200]})
        for part in section("/routing mpls"):
            ast.routing.append({"protocol": "mpls", "raw": part[:200]})

        if "/interface bridge" in lowered:
            evidence = [line.strip() for line in content.splitlines() if "/interface bridge" in line][:3]
            ast.findings.append(InfrastructureFinding(Severity.low, "bridge", "Bridge configuration detected", "Verify bridge security, port security, and STP settings", confidence=0.8, evidence=evidence))
            if "stp" in lowered or "spanning-tree" in lowered:
                evidence = [line.strip() for line in content.splitlines() if "stp" in line.lower() or "spanning-tree" in line.lower()][:3]
                ast.findings.append(InfrastructureFinding(Severity.low, "switch", "STP/bridge security detected", "Verify STP mode and port roles", confidence=0.7, evidence=evidence))

        if "/queue" in lowered:
            ast.services.append({"type": "queue", "raw": "/queue detected"})
        if "/ip hotspot" in lowered:
            ast.services.append({"type": "hotspot", "raw": "/ip hotspot detected"})
        if "/capsman" in lowered or "capsman" in lowered:
            ast.wireless.append({"type": "capsman", "raw": "CAPsMAN configuration detected"})
            evidence = [line.strip() for line in content.splitlines() if "capsman" in line.lower()][:3]
            ast.findings.append(InfrastructureFinding(Severity.medium, "wireless", "CAPsMAN detected", "Verify WPA mode, SSID isolation, and management access", confidence=0.6, evidence=evidence))
        if "/interface wireless" in lowered or "wireless" in lowered:
            ast.wireless.append({"type": "wireless", "raw": "Wireless interface configuration detected"})
        if "/ip neighbor discovery" in lowered or "lldp" in lowered:
            evidence = [line.strip() for line in content.splitlines() if "lldp" in line.lower() or "neighbor discovery" in line.lower()][:3]
            ast.findings.append(InfrastructureFinding(Severity.low, "discovery", "LLDP/neighbor discovery detected", "Review neighbor policy for sensitive environment", confidence=0.5, evidence=evidence))
        return ast
