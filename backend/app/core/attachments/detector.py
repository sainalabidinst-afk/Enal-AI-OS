from __future__ import annotations

import zipfile
import tarfile
from pathlib import Path
from typing import Any

from backend.app.core.attachments.models import (
    AttachmentMeta,
    AttachmentType,
    DeviceRole,
    VendorFamily,
)


EXTENSION_MAP: dict[str, tuple[AttachmentType, VendorFamily | None, DeviceRole | None]] = {
    ".rsc": (AttachmentType.config, VendorFamily.mikrotik, DeviceRole.router),
    ".backup": (AttachmentType.backup, VendorFamily.mikrotik, DeviceRole.router),
    ".export": (AttachmentType.config, VendorFamily.mikrotik, DeviceRole.router),
    ".cfg": (AttachmentType.config, None, None),
    ".conf": (AttachmentType.config, None, None),
    ".txt": (AttachmentType.config, None, None),
    ".cli": (AttachmentType.config, None, None),
    ".xml": (AttachmentType.config, None, None),
    ".json": (AttachmentType.config, None, None),
    ".yaml": (AttachmentType.config, VendorFamily.docker, DeviceRole.container),
    ".yml": (AttachmentType.config, VendorFamily.docker, DeviceRole.container),
    ".tf": (AttachmentType.config, VendorFamily.aws, DeviceRole.cloud),
    ".ps1": (AttachmentType.config, VendorFamily.windows, DeviceRole.server),
    ".sh": (AttachmentType.config, VendorFamily.linux, DeviceRole.server),
    ".log": (AttachmentType.log, None, None),
    ".pdf": (AttachmentType.document, None, None),
    ".docx": (AttachmentType.document, None, None),
    ".xlsx": (AttachmentType.document, None, None),
    ".csv": (AttachmentType.document, None, None),
    ".pptx": (AttachmentType.document, None, None),
    ".drawio": (AttachmentType.diagram, None, None),
    ".vsdx": (AttachmentType.diagram, None, None),
    ".svg": (AttachmentType.diagram, None, None),
    ".png": (AttachmentType.image, None, None),
    ".jpg": (AttachmentType.image, None, None),
    ".jpeg": (AttachmentType.image, None, None),
    ".webp": (AttachmentType.image, None, None),
    ".bmp": (AttachmentType.image, None, None),
    ".zip": (AttachmentType.archive, None, None),
    ".tar.gz": (AttachmentType.archive, None, None),
    ".gz": (AttachmentType.archive, None, None),
}

VENDOR_SIGNATURES: dict[str, tuple[VendorFamily, DeviceRole | None]] = {
    "routeros": (VendorFamily.mikrotik, DeviceRole.router),
    "mikrotik": (VendorFamily.mikrotik, DeviceRole.router),
    "routeros 7": (VendorFamily.mikrotik, DeviceRole.router),
    "cisco ios": (VendorFamily.cisco, DeviceRole.router),
    "cisco ios-xe": (VendorFamily.cisco, DeviceRole.router),
    "cisco ios xr": (VendorFamily.cisco, DeviceRole.router),
    "cisco nx-os": (VendorFamily.cisco, DeviceRole.switch),
    "fortios": (VendorFamily.fortinet, DeviceRole.firewall),
    "fortigate": (VendorFamily.fortinet, DeviceRole.firewall),
    "junos": (VendorFamily.juniper, DeviceRole.router),
    "arubaos": (VendorFamily.aruba, DeviceRole.switch),
    "aruba aos": (VendorFamily.aruba, DeviceRole.switch),
    "instant os": (VendorFamily.aruba, DeviceRole.wireless_controller),
    "ruijie": (VendorFamily.ruijie, DeviceRole.switch),
    "huawei": (VendorFamily.huawei, DeviceRole.router),
    "vrp": (VendorFamily.huawei, DeviceRole.router),
    "comware": (VendorFamily.huawei, DeviceRole.switch),
    "dell networking": (VendorFamily.dell, DeviceRole.switch),
    "smart fabric": (VendorFamily.dell, DeviceRole.switch),
    "hp procurve": (VendorFamily.hp, DeviceRole.switch),
    "procurve": (VendorFamily.hp, DeviceRole.switch),
    "extremexos": (VendorFamily.extreme, DeviceRole.switch),
    "h3c": (VendorFamily.h3c, DeviceRole.switch),
    "comware v5": (VendorFamily.h3c, DeviceRole.switch),
    "unifi": (VendorFamily.ubiquiti, DeviceRole.wireless_controller),
    "ubiquiti": (VendorFamily.ubiquiti, DeviceRole.wireless_controller),
    "meraki": (VendorFamily.ubiquiti, DeviceRole.wireless_controller),
    "vyatta": (VendorFamily.vyos, DeviceRole.router),
    "vyos": (VendorFamily.vyos, DeviceRole.router),
    "pfsense": (VendorFamily.pfsense, DeviceRole.firewall),
    "opnsense": (VendorFamily.opnsense, DeviceRole.firewall),
    "esxi": (VendorFamily.vmware, DeviceRole.hypervisor),
    "vmware": (VendorFamily.vmware, DeviceRole.hypervisor),
    "proxmox": (VendorFamily.proxmox, DeviceRole.hypervisor),
    "hyper-v": (VendorFamily.hyperv, DeviceRole.hypervisor),
    "windows server": (VendorFamily.windows, DeviceRole.server),
    "ubuntu": (VendorFamily.linux, DeviceRole.server),
    "debian": (VendorFamily.linux, DeviceRole.server),
    "rocky": (VendorFamily.linux, DeviceRole.server),
    "almalinux": (VendorFamily.linux, DeviceRole.server),
    "rhel": (VendorFamily.linux, DeviceRole.server),
    "centos": (VendorFamily.linux, DeviceRole.server),
    "oracle linux": (VendorFamily.linux, DeviceRole.server),
    "suse": (VendorFamily.linux, DeviceRole.server),
}


def _extension_for(filename: str) -> str:
    lower = filename.lower()
    if lower.endswith(".tar.gz"):
        return ".tar.gz"
    return Path(filename).suffix.lower()


def detect_from_filename(filename: str) -> AttachmentMeta:
    ext = _extension_for(filename)
    mapped = EXTENSION_MAP.get(ext)
    attachment_type: AttachmentType = AttachmentType.unknown
    vendor: VendorFamily | None = None
    device_role: DeviceRole | None = None
    if mapped:
        attachment_type, vendor, device_role = mapped
    return AttachmentMeta(
        filename=filename,
        attachment_type=attachment_type,
        vendor=vendor or VendorFamily.unknown,
        device_role=device_role or DeviceRole.unknown,
        detected_format=ext,
    )


def detect_from_content(filename: str, content: str, max_preview: int = 2000) -> AttachmentMeta:
    meta = detect_from_filename(filename)
    lowered = content.lower()
    preview = content[:max_preview]
    meta.text_preview = preview

    # Auto-detect vendor and role from content signatures
    best_confidence = 0.3
    for signature, (sig_vendor, sig_role) in VENDOR_SIGNATURES.items():
        if signature in lowered:
            weight = len(signature)
            if weight > best_confidence:
                meta.vendor = sig_vendor
                if sig_role is not None:
                    meta.device_role = sig_role
                best_confidence = weight

    if meta.vendor != VendorFamily.unknown:
        meta.confidence = min(1.0, 0.5 + best_confidence / 10.0)

    if meta.attachment_type == AttachmentType.unknown:
        if any(key in lowered for key in ["/interface", "/ip ", "routeros", "/routing", "/ip firewall"]):
            meta.attachment_type = AttachmentType.config
        elif any(key in lowered for key in ["building", "Building configuration", "version", "hostname"]):
            meta.attachment_type = AttachmentType.config
        elif "apiVersion:" in lowered and "kind:" in lowered:
            meta.attachment_type = AttachmentType.config
            meta.vendor = VendorFamily.kubernetes
            meta.device_role = DeviceRole.container
            meta.confidence = max(meta.confidence, 0.85)
        elif "docker-compose" in lowered or "services:" in lowered:
            meta.attachment_type = AttachmentType.config
            meta.vendor = VendorFamily.docker
            meta.device_role = DeviceRole.container
            meta.confidence = max(meta.confidence, 0.85)

    return meta


def classify_archive_member(name: str) -> AttachmentMeta:
    return detect_from_filename(name)


def summarize_archive(content: bytes, filename: str) -> dict[str, Any]:
    members: list[str] = []
    inferred: list[AttachmentMeta] = []
    try:
        if filename.endswith(".zip"):
            with zipfile.ZipFile(__import__("io").BytesIO(content)) as archive:
                members = archive.namelist()
        elif filename.endswith(".tar.gz") or filename.endswith(".gz"):
            with tarfile.open(fileobj=__import__("io").BytesIO(content), mode="r:gz") as archive:
                members = [m.name for m in archive.getmembers() if m.isfile()]
    except Exception as exc:
        return {"error": str(exc), "members": []}

    for member in members[:50]:
        inferred.append(classify_archive_member(member))

    return {
        "members": members,
        "member_count": len(members),
        "inferred_types": [m.attachment_type.value for m in inferred],
        "inferred_vendors": [m.vendor.value for m in inferred if m.vendor != VendorFamily.unknown],
    }
