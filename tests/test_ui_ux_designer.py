"""
Smoke tests for Ui Ux Designer capability.
"""

from apps.ui_ux_designer.accessibility_checker import *  # noqa: F403
from apps.ui_ux_designer.design_system import *  # noqa: F403
from apps.ui_ux_designer.engine import *  # noqa: F403
from apps.ui_ux_designer.prototype_generator import *  # noqa: F403
from apps.ui_ux_designer.schemas import *  # noqa: F403


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.ui_ux_designer")
    assert mod is not None
