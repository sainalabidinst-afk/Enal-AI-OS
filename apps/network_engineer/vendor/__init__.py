"""
Vendor Abstraction Layer
=========================

All vendor adapters for Network Engineer.
"""

from apps.network_engineer.vendor.cisco_deploy import cisco_deploy_adapter
from apps.network_engineer.vendor.cisco_ios import cisco_ios_adapter
from apps.network_engineer.vendor.detector import detect_vendor, parse_config
from apps.network_engineer.vendor.fortinet import fortinet_adapter
from apps.network_engineer.vendor.fortinet_deploy import fortinet_deploy_adapter
from apps.network_engineer.vendor.mikrotik import mikrotik_adapter
from apps.network_engineer.vendor.mikrotik_deploy import mikrotik_deploy_adapter
from apps.network_engineer.vendor.registry import vendor_registry

# Register all adapters
vendor_registry.register(mikrotik_adapter)
vendor_registry.register(cisco_ios_adapter)
vendor_registry.register(fortinet_adapter)

__all__ = [
    "cisco_deploy_adapter",
    "cisco_ios_adapter",
    "detect_vendor",
    "fortinet_adapter",
    "fortinet_deploy_adapter",
    "mikrotik_adapter",
    "mikrotik_deploy_adapter",
    "parse_config",
    "vendor_registry",
]
