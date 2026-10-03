"""
DNS Service — internal DNS resolution for Enal AI OS.

Provides DNS-based service discovery for internal services,
zone management, and query resolution.

ADR-003: Thin adapter over DNS library (dnspython).
ADR-004: Service registration and health tracking logic
         resides here; zone file generation is infrastructure.
"""

from __future__ import annotations

import logging
import socket
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class DNSService:
    """Represents a service registered in internal DNS."""

    name: str
    host: str
    port: int
    protocol: str = "tcp"
    ttl: int = 30
    metadata: dict[str, Any] = field(default_factory=dict)


class DNSError(Exception):
    """Raised when DNS operations fail."""


class DNSServiceDiscovery:
    """
    Internal DNS service discovery.

    Manages registration of services in the enal.ai zone
    and provides lookup capabilities.

    Usage::

        dns = DNSServiceDiscovery()
        dns.register("api", "backend", 8000)
        host = dns.lookup("api.enal.ai")
    """

    def __init__(self, zone: str = "enal.ai", dns_server: str = "localhost") -> None:
        self.zone = zone
        self.dns_server = dns_server
        self._services: dict[str, DNSService] = {}

    def register(
        self, name: str, host: str, port: int, protocol: str = "tcp", ttl: int = 30
    ) -> None:  # noqa: E501
        """Register a service in internal DNS."""
        self._services[name] = DNSService(
            name=name,
            host=host,
            port=port,
            protocol=protocol,
            ttl=ttl,
        )
        logger.info(f"Registered DNS service: {name}.{self.zone} -> {host}:{port}")

    def unregister(self, name: str) -> None:
        """Remove a service from internal DNS."""
        self._services.pop(name, None)

    def lookup(self, name: str) -> DNSService | None:
        """Look up a service by name (supports FQDN and short names)."""
        clean_name = name.replace(f".{self.zone}", "").replace(".", "")
        return self._services.get(clean_name)

    def lookup_host(self, name: str) -> str | None:
        """Resolve a service name to its host address."""
        svc = self.lookup(name)
        return svc.host if svc else None

    def list_services(self) -> list[DNSService]:
        """Return all registered services."""
        return list(self._services.values())

    def resolve(self, hostname: str) -> str:
        """
        Resolve a hostname via DNS.

        Uses system DNS first (for external lookups), then
        falls back to internal service registry.
        """
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            svc = self.lookup(hostname)
            if svc:
                return svc.host
            raise DNSError(f"Cannot resolve hostname: {hostname}")

    def generate_zone_file(self) -> str:
        """Generate a BIND-format zone file for all registered services."""
        lines = [
            f"$ORIGIN {self.zone}.",
            "$TTL    30",
            f"@       IN  SOA ns1.{self.zone}. admin.{self.zone}. (",
            "                        2024010101  ; serial",
            "                        7200        ; refresh",
            "                        3600        ; retry",
            "                        1209600     ; expire",
            "                        300 )       ; minimum",
            "",
            f"        IN  NS  ns1.{self.zone}.",
            "",
        ]
        for name, svc in self._services.items():
            if svc.protocol == "tcp":
                lines.append(f"{name}  IN  A    {svc.host}")
            else:
                lines.append(f"{name}  IN  A    {svc.host}")
            lines.append(f"{name}  IN  SRV  0 5 {svc.port} {name}.{self.zone}.")
        lines.append("")
        return "\n".join(lines)

    def ensure_default_services(self) -> None:
        """Register the default Enal AI OS services."""
        defaults = [
            ("backend", "backend", 8000),
            ("frontend", "frontend", 3000),
            ("api", "backend", 8000),
            ("postgres", "postgres", 5432),
            ("redis", "redis", 6379),
            ("qdrant", "qdrant", 6333),
            ("ollama", "ollama", 11434),
            ("minio", "minio", 9000),
            ("kafka", "kafka", 9092),
            ("zookeeper", "zookeeper", 22181),
            ("lb", "nginx", 80),
            ("gateway", "nginx", 80),
            ("coredns", "coredns", 53),
        ]
        for name, host, port in defaults:
            self.register(name, host, port)


dns_service = DNSServiceDiscovery()
