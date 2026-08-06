"""
Smoke tests for Product Manager capability.
"""

from apps.product_manager.backlog_manager import *
from apps.product_manager.engine import *
from apps.product_manager.okr_tracker import *
from apps.product_manager.prioritizer import *
from apps.product_manager.roadmap_manager import *


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.product_manager")
    assert mod is not None
