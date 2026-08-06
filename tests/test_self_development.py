"""
Smoke tests for Self Development capability.
"""

from apps.self_development.engine import *
from apps.self_development.project_scanner import *
from apps.self_development.risk_modeler import *
from apps.self_development.schemas import *
from apps.self_development.smell_taxonomy import *


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.self_development")
    assert mod is not None
