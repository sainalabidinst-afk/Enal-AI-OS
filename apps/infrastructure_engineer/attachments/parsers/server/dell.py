from __future__ import annotations

import zipfile
from io import BytesIO

from apps.infrastructure_engineer.attachments.models import (
    AttachmentMeta,
    InfrastructureAST,
    InfrastructureFinding,
    Severity,
    VendorFamily,
)
from apps.infrastructure_engineer.attachments.parsers.base import BaseParser


def _read_zip_texts(content: bytes) -> list[str]:
    texts: list[str] = []
    try:
        with zipfile.ZipFile(BytesIO(content)) as archive:
            for name in archive.namelist()[:50]:
                try:
                    texts.append(archive.read(name).decode("utf-8", errors="ignore"))
                except Exception:
                    continue
    except Exception:
        pass
    return texts


class DellIDRACParser(BaseParser):
    def can_parse(self, meta: AttachmentMeta) -> bool:
        return meta.vendor == VendorFamily.dell or meta.filename.lower().startswith(("idrac", "dell", "openmanage"))

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        ast = InfrastructureAST(vendor=VendorFamily.dell, format="idrac_openmanage", device_role=meta.device_role)
        lowered = content.lower()
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if any(key in lowered for key in ["raid", "controller", "physical drive", "virtual drive"]):
                ast.storage.append({"raw": stripped[:200]})
                if "failed" in lowered or "degraded" in lowered:
                    evidence = [line.strip() for line in lines if "failed" in line.lower() or "degraded" in line.lower()][:5]
                    ast.findings.append(InfrastructureFinding(Severity.high, "storage", "Dell RAID degraded/failed drive detected", "Review RAID controller and replace failed drive", confidence=0.9, evidence=evidence))
            if any(key in lowered for key in ["fan ", "temperature", "power supply", "psu", "thermal"]):
                ast.system.setdefault("hardware_health", []).append({"raw": stripped[:200]})
                if "critical" in lowered or "failed" in lowered:
                    evidence = [line.strip() for line in lines if "critical" in line.lower() or "failed" in line.lower()][:5]
                    ast.findings.append(InfrastructureFinding(Severity.high, "hardware", "Dell hardware alert detected", "Review fan, PSU, and thermal status", confidence=0.9, evidence=evidence))
            if any(key in lowered for key in ["firmware", "bios", "version"]):
                ast.system.setdefault("firmware", []).append({"raw": stripped[:200]})
                if "mismatch" in lowered or "outofdate" in lowered:
                    evidence = [line.strip() for line in lines if "mismatch" in line.lower() or "outofdate" in line.lower()][:5]
                    ast.findings.append(InfrastructureFinding(Severity.medium, "hardware", "Dell firmware mismatch detected", "Update firmware to latest supported version", confidence=0.8, evidence=evidence))
            if any(key in lowered for key in ["memory", "dimm", "ecc"]):
                ast.system.setdefault("memory", []).append({"raw": stripped[:200]})
                if "ecc error" in lowered or "memory error" in lowered:
                    evidence = [line.strip() for line in lines if "ecc" in line.lower() or "memory error" in line.lower()][:5]
                    ast.findings.append(InfrastructureFinding(Severity.high, "hardware", "Dell memory ECC error detected", "Replace affected DIMM and check memory policy", confidence=0.9, evidence=evidence))
        return ast
