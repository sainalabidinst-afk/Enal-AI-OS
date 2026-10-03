"""
Smoke tests for Product Manager capability.
"""

from apps.product_manager.backlog_manager import *  # noqa: F403
from apps.product_manager.engine import *  # noqa: F403
from apps.product_manager.okr_tracker import *  # noqa: F403
from apps.product_manager.prioritizer import *  # noqa: F403
from apps.product_manager.roadmap_manager import *  # noqa: F403


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.product_manager")
    assert mod is not None
