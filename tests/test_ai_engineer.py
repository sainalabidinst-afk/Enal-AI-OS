"""
Smoke tests for Ai Engineer capability.
"""

from apps.ai_engineer.agent_designer import *  # noqa: F403
from apps.ai_engineer.engine import *  # noqa: F403
from apps.ai_engineer.llmops_manager import *  # noqa: F403
from apps.ai_engineer.prompt_engineer import *  # noqa: F403
from apps.ai_engineer.rag_engine import *  # noqa: F403


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.ai_engineer")
    assert mod is not None
