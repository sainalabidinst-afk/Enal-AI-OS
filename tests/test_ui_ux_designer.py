"""
Smoke tests for Ui Ux Designer capability.
"""

from apps.ui_ux_designer.accessibility_checker import *
from apps.ui_ux_designer.design_system import *
from apps.ui_ux_designer.engine import *
from apps.ui_ux_designer.prototype_generator import *
from apps.ui_ux_designer.schemas import *


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.ui_ux_designer")
    assert mod is not None
