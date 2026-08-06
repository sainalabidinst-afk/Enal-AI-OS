"""
Smoke tests for Network Engineer capability.
"""

from apps.network_engineer.advisor import *
from apps.network_engineer.analyzer import *
from apps.network_engineer.analyzer_ip_routing import *
from apps.network_engineer.analyzer_network import *
from apps.network_engineer.analyzer_security import *


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.network_engineer")
    assert mod is not None
