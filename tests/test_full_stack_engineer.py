"""
Smoke tests for Full Stack Engineer capability.
"""

from apps.full_stack_engineer.architecture_review import *
from apps.full_stack_engineer.architecture_review_engine import *
from apps.full_stack_engineer.architecture_review_models import *
from apps.full_stack_engineer.code_review import *
from apps.full_stack_engineer.engine import *


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.full_stack_engineer")
    assert mod is not None
