"""
Vendor Registry
===============

Registry for vendor adapters with auto-detection.
"""

import logging
from typing import Any

from apps.network_engineer.vendor.base import VendorAdapter
from apps.network_engineer.vendor.models import NetworkAST

logger = logging.getLogger(__name__)


class VendorRegistry:
    """Registry for vendor adapters."""

    def __init__(self):
        self._adapters: list[VendorAdapter] = []

    def register(self, adapter: VendorAdapter):
        """Register a vendor adapter."""
        self._adapters.append(adapter)
        logger.info(f"Registered vendor adapter: {adapter.vendor_name}")

    def detect_vendor(self, config_text: str) -> VendorAdapter | None:
        """Auto-detect vendor from config text."""
        for adapter in self._adapters:
            if adapter.detect(config_text):
                logger.info(f"Detected vendor: {adapter.vendor_name}")
                return adapter
        logger.warning("No vendor adapter matched the config")
        return None

    def parse(self, config_text: str, vendor: str | None = None) -> NetworkAST:
        """Parse config using specified or auto-detected vendor."""
        adapter = None
        if vendor:
            adapter = next((a for a in self._adapters if a.vendor_name == vendor), None)
        else:
            adapter = self.detect_vendor(config_text)

        if not adapter:
            raise ValueError(f"No vendor adapter found for config (vendor={vendor})")

        return adapter.parse(config_text)

    def list_vendors(self) -> list[dict[str, Any]]:
        """List all registered vendors."""
        return [a.get_vendor_info() for a in self._adapters]


vendor_registry = VendorRegistry()
