"""
Smoke tests for Code Engineer capability.
"""

from apps.code_engineer.analyzer import *
from apps.code_engineer.architecture_models import *
from apps.code_engineer.architecture_patterns import *
from apps.code_engineer.architecture_reader import *
from apps.code_engineer.clean_architecture import *


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.code_engineer")
    assert mod is not None
