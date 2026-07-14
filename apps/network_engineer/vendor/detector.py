"""
Vendor Auto-Detection
=====================

Auto-detects vendor from config content.
"""

import logging
from typing import Any

from apps.network_engineer.vendor.registry import vendor_registry

logger = logging.getLogger(__name__)


def detect_vendor(config_text: str) -> str | None:
    """Detect vendor from config text."""
    adapter = vendor_registry.detect_vendor(config_text)
    return adapter.vendor_name if adapter else None


def parse_config(config_text: str, vendor: str | None = None) -> Any:
    """Parse config using specified or auto-detected vendor."""
    return vendor_registry.parse(config_text, vendor)
