"""
Smoke tests for Business Analyst capability.
"""

from apps.business_analyst.brd_generator import *
from apps.business_analyst.domain_knowledge import *
from apps.business_analyst.engine import *
from apps.business_analyst.gap_analyzer import *
from apps.business_analyst.optimizer import *


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.business_analyst")
    assert mod is not None
