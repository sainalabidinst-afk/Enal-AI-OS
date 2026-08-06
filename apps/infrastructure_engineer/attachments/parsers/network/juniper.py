from __future__ import annotations

from apps.infrastructure_engineer.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    InfrastructureFinding,
    Severity,
    VendorFamily,
)
from apps.infrastructure_engineer.attachments.parsers.base import BaseParser


class JuniperParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.juniper or meta.filename.lower().endswith((".conf", ".txt", ".set", ".xml"))

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.juniper, format="junos", device_role=meta.device_role)
        for idx, line in enumerate(content.splitlines()):
            stripped = line.strip()
            if stripped.startswith("set interfaces "):
                parts = stripped.split()
                if len(parts) >= 4:
                    ast.interfaces.append({"name": parts[2], "property": " ".join(parts[3:]), "raw": stripped[:200]})
                if "vlan" in stripped.lower():
                    ast.vlans.append({"raw": stripped[:200]})
                if "aggregated" in stripped.lower() or "ae" in stripped.lower():
                    evidence = [stripped]
                    ast.findings.append(InfrastructureFinding(Severity.low, "switch", "LACP/bond detected", "Verify LACP/ae interface configuration", confidence=0.7, evidence=evidence))
                if "poe" in stripped.lower():
                    evidence = [stripped]
                    ast.findings.append(InfrastructureFinding(Severity.low, "switch", "PoE detected", "Review PoE interface allocation", confidence=0.6, evidence=evidence))
            if stripped.startswith("set security "):
                ast.firewall.append({"raw": stripped[:200]})
            if stripped.startswith("set routing-instances ") or stripped.startswith("set protocols ospf") or stripped.startswith("set protocols bgp"):
                ast.routing.append({"raw": stripped[:200]})
            if stripped.startswith("set vlans "):
                ast.vlans.append({"raw": stripped[:200]})
            if stripped.startswith("set protocols "):
                if "rstp" in stripped.lower() or "stp" in stripped.lower():
                    evidence = [stripped]
                    ast.findings.append(InfrastructureFinding(Severity.low, "switch", "STP/RSTP detected", "Verify spanning-tree protection", confidence=0.7, evidence=evidence))
            if stripped.startswith("set system "):
                ast.system["hostname"] = stripped
        if not ast.interfaces and not ast.firewall:
            ast.findings.append(InfrastructureFinding(Severity.low, "coverage", "Limited Juniper-specific patterns matched", "Review full config export for complete analysis", confidence=0.4))
        return ast
