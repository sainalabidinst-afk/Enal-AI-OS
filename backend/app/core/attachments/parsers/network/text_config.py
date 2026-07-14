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


class TextConfigParser(BaseParser):
    """Shared text-based parsing helpers for network configs."""

    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.attachment_type in {meta.attachment_type.config, meta.attachment_type.backup, meta.attachment_type.log}

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(format="text", version="")
        lowered = content.lower()
        if any(key in lowered for key in ["routeros", "/interface", "/ip firewall", "/routing ospf", "/routing bgp"]):
            ast.vendor = VendorFamily.mikrotik
            ast.format = "routeros"
            self._parse_routeros(ast, content)
        elif any(key in lowered for key in ["building configuration", "version ", "hostname", "access-list", "ip route", "interface "]):
            ast.vendor = VendorFamily.cisco
            ast.format = "cisco_ios"
            self._parse_cisco(ast, content)
        elif any(key in lowered for key in ["config system global", "config system interface", "config firewall policy", "fortios"]):
            ast.vendor = VendorFamily.fortinet
            ast.format = "fortios"
            self._parse_fortinet(ast, content)
        elif any(key in lowered for key in ["set ", "hierarchical", "activate ", "commit "]):
            ast.vendor = VendorFamily.juniper
            ast.format = "junos"
            self._parse_juniper(ast, content)
        else:
            self._parse_generic(ast, content)
        return ast

    def _section(self, content: str, marker: str) -> list[str]:
        parts: list[str] = []
        idx = content.find(marker)
        while idx != -1:
            end = content.find("\n/", idx + 1)
            if end == -1:
                end = len(content)
            parts.append(content[idx:end])
            idx = content.find(marker, end + 1)
        return parts

    def _parse_routeros(self, ast: InfrastructureAST, content: str) -> None:
        for section in self._section(content, "/interface"):
            if "address=" in section:
                match = re.search(r"address=([\d./]+)", section)
                if match:
                    ast.interfaces.append({"address": match.group(1), "raw": section[:200]})
            if "vlan=" in section.lower():
                match = re.search(r"vlan=([^,\s]+)", section)
                if match:
                    ast.vlans.append({"id": match.group(1), "raw": section[:200]})
        for section in self._section(content, "/ip firewall"):
            ast.firewall.append({"raw": section[:200]})
            if "input" in section and "accept" not in section:
                ast.findings.append(InfrastructureFinding(Severity.high, "firewall", "Restrictive input chain", "Review firewall input chain policy", confidence=0.7))
        for section in self._section(content, "/routing ospf"):
            ast.routing.append({"protocol": "ospf", "raw": section[:200]})
        for section in self._section(content, "/interface bridge"):
            ast.findings.append(InfrastructureFinding(Severity.low, "bridge", "Bridge configuration detected", "Verify bridge security and port security", confidence=0.8))

    def _parse_cisco(self, ast: InfrastructureAST, content: str) -> None:
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("interface "):
                ast.interfaces.append({"raw": stripped[:200]})
            if "access-list" in stripped or "ip access-list" in stripped:
                ast.firewall.append({"raw": stripped[:200]})
            if stripped.startswith("router ospf") or stripped.startswith("router bgp"):
                ast.routing.append({"raw": stripped[:200]})
            if "vlan" in stripped.lower() and stripped:
                ast.vlans.append({"raw": stripped[:200]})

    def _parse_fortinet(self, ast: InfrastructureAST, content: str) -> None:
        for line in content.splitlines():
            stripped = line.strip()
            if "config system interface" in stripped or stripped.startswith("edit "):
                ast.interfaces.append({"raw": stripped[:200]})
            if "config firewall policy" in stripped:
                ast.firewall.append({"raw": stripped[:200]})
            if stripped.startswith("config router ") or stripped.startswith("edit "):
                ast.routing.append({"raw": stripped[:200]})

    def _parse_juniper(self, ast: InfrastructureAST, content: str) -> None:
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("set interfaces "):
                ast.interfaces.append({"raw": stripped[:200]})
            if stripped.startswith("set security "):
                ast.firewall.append({"raw": stripped[:200]})
            if stripped.startswith("set routing-instances ") or stripped.startswith("set protocols ospf") or stripped.startswith("set protocols bgp"):
                ast.routing.append({"raw": stripped[:200]})

    def _parse_generic(self, ast: InfrastructureAST, content: str) -> None:
        for line in content.splitlines()[:300]:
            lowered = line.lower()
            if any(key in lowered for key in ["interface", "ip addr", "ip address"]):
                ast.interfaces.append({"raw": line.strip()[:200]})
            if any(key in lowered for key in ["firewall", "filter", "acl"]):
                ast.firewall.append({"raw": line.strip()[:200]})
            if "vlan" in lowered:
                ast.vlans.append({"raw": line.strip()[:200]})
            if any(key in lowered for key in ["route", "ospf", "bgp"]):
                ast.routing.append({"raw": line.strip()[:200]})


text_config_parser = TextConfigParser()
