"""
Smoke tests for Network Engineer capability.
"""

from apps.network_engineer.advisor import *  # noqa: F403
from apps.network_engineer.analyzer import *  # noqa: F403
from apps.network_engineer.analyzer_ip_routing import *  # noqa: F403
from apps.network_engineer.analyzer_network import *  # noqa: F403
from apps.network_engineer.analyzer_security import *  # noqa: F403


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.network_engineer")
    assert mod is not None
