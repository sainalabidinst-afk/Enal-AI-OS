"""
Vendor Adapter Base
====================

Abstract base class for all vendor adapters.
Each vendor (MikroTik, Cisco, Fortinet) implements this contract.
"""

from abc import ABC, abstractmethod
from typing import Any

from apps.network_engineer.vendor.models import NetworkAST


class VendorAdapter(ABC):
    """Base class for vendor adapters."""

    vendor_name: str = "unknown"
    vendor_versions: list[str] = []

    @abstractmethod
    def detect(self, config_text: str) -> bool:
        """Return True if this adapter can parse the given config text."""
        raise NotImplementedError

    @abstractmethod
    def parse(self, config_text: str) -> NetworkAST:
        """Parse config text into Universal AST."""
        raise NotImplementedError

    @abstractmethod
    def generate(self, ast: NetworkAST) -> str:
        """Generate vendor-specific config from Universal AST."""
        raise NotImplementedError

    def get_vendor_info(self) -> dict[str, Any]:
        """Return vendor metadata."""
        return {
            "vendor": self.vendor_name,
            "versions": self.vendor_versions,
        }
