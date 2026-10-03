"""
Smoke tests for Devops Assistant capability.
"""

from apps.devops_assistant.deployment_planner import *  # noqa: F403
from apps.devops_assistant.engine import *  # noqa: F403
from apps.devops_assistant.infrastructure_designer import *  # noqa: F403
from apps.devops_assistant.monitoring_configurator import *  # noqa: F403
from apps.devops_assistant.pipeline_generator import *  # noqa: F403


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.devops_assistant")
    assert mod is not None
