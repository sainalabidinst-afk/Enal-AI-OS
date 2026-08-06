from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AttachmentType(str, Enum):
    config = "config"
    screenshot = "screenshot"
    document = "document"
    diagram = "diagram"
    archive = "archive"
    image = "image"
    log = "log"
    backup = "backup"
    unknown = "unknown"


class VendorFamily(str, Enum):
    mikrotik = "mikrotik"
    cisco = "cisco"
    fortinet = "fortinet"
    aruba = "aruba"
    ruijie = "ruijie"
    juniper = "juniper"
    ubiquiti = "ubiquiti"
    huawei = "huawei"
    dell = "dell"
    hp = "hp"
    extreme = "extreme"
    h3c = "h3c"
    palo_alto = "palo_alto"
    checkpoint = "checkpoint"
    sonicwall = "sonicwall"
    sophos = "sophos"
    vyos = "vyos"
    pfsense = "pfsense"
    opnsense = "opnsense"
    vmware = "vmware"
    proxmox = "proxmox"
    hyperv = "hyperv"
    docker = "docker"
    kubernetes = "kubernetes"
    linux = "linux"
    windows = "windows"
    synology = "synology"
    truenas = "truenas"
    qnap = "qnap"
    netapp = "netapp"
    aws = "aws"
    azure = "azure"
    gcp = "gcp"
    unknown = "unknown"


class DeviceRole(str, Enum):
    router = "router"
    firewall = "firewall"
    switch = "switch"
    wireless_controller = "wireless_controller"
    access_point = "access_point"
    gateway = "gateway"
    server = "server"
    storage = "storage"
    hypervisor = "hypervisor"
    cloud = "cloud"
    container = "container"
    monitoring = "monitoring"
    endpoint = "endpoint"
    unknown = "unknown"


class Severity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    informational = "informational"


@dataclass
class AttachmentMeta:
    filename: str
    content_type: str | None = None
    size_bytes: int = 0
    attachment_type: AttachmentType = AttachmentType.unknown
    vendor: VendorFamily = VendorFamily.unknown
    device_role: DeviceRole = DeviceRole.unknown
    detected_format: str = ""
    detected_version: str = ""
    confidence: float = 0.0
    text_preview: str = ""
    parser_used: str = ""
    parse_error: str | None = None


@dataclass
class InfrastructureFinding:
    severity: Severity
    category: str
    title: str
    description: str
    recommendation: str | None = None
    confidence: float = 1.0
    evidence: list[str] = field(default_factory=list)
    location: str | None = None


@dataclass
class InfrastructureAST:
    vendor: VendorFamily = VendorFamily.unknown
    device_role: DeviceRole = DeviceRole.unknown
    format: str = ""
    version: str = ""
    interfaces: list[dict[str, Any]] = field(default_factory=list)
    vlans: list[dict[str, Any]] = field(default_factory=list)
    routing: list[dict[str, Any]] = field(default_factory=list)
    firewall: list[dict[str, Any]] = field(default_factory=list)
    services: list[dict[str, Any]] = field(default_factory=list)
    security: list[dict[str, Any]] = field(default_factory=list)
    wireless: list[dict[str, Any]] = field(default_factory=list)
    ha: list[dict[str, Any]] = field(default_factory=list)
    storage: list[dict[str, Any]] = field(default_factory=list)
    system: dict[str, Any] = field(default_factory=dict)
    raw_sections: dict[str, Any] = field(default_factory=dict)
    findings: list[InfrastructureFinding] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "vendor": self.vendor.value,
            "device_role": self.device_role.value,
            "format": self.format,
            "version": self.version,
            "interfaces": self.interfaces,
            "vlans": self.vlans,
            "routing": self.routing,
            "firewall": self.firewall,
            "services": self.services,
            "security": self.security,
            "wireless": self.wireless,
            "ha": self.ha,
            "storage": self.storage,
            "system": self.system,
            "findings": [
                {
                    "severity": f.severity.value,
                    "category": f.category,
                    "title": f.title,
                    "description": f.description,
                    "recommendation": f.recommendation,
                    "confidence": f.confidence,
                    "evidence": f.evidence,
                    "location": f.location,
                }
                for f in self.findings
            ],
            "metadata": self.metadata,
        }


@dataclass
class AttachmentAnalysisResult:
    meta: AttachmentMeta
    ast: InfrastructureAST
    summary: str = ""
    risk_score: float = 0.0
    recommendations: list[str] = field(default_factory=list)
    analysis_error: str | None = None
