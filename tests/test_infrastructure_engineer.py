"""
Smoke tests for Infrastructure Engineer capability.
"""

from apps.infrastructure_engineer.disaster_recovery import *
from apps.infrastructure_engineer.engine import *
from apps.infrastructure_engineer.ha_cluster_designer import *
from apps.infrastructure_engineer.kubernetes_designer import *
from apps.infrastructure_engineer.schemas import *


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.infrastructure_engineer")
    assert mod is not None
