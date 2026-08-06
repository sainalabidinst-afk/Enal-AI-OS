"""
Smoke tests for Qa Engineer capability.
"""

from apps.qa_engineer.coverage_analyzer import *
from apps.qa_engineer.engine import *
from apps.qa_engineer.flaky_detector import *
from apps.qa_engineer.golden_test_gen import *
from apps.qa_engineer.mutation_tester import *


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.qa_engineer")
    assert mod is not None
