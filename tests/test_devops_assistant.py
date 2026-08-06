"""
Smoke tests for Devops Assistant capability.
"""

from apps.devops_assistant.deployment_planner import *
from apps.devops_assistant.engine import *
from apps.devops_assistant.infrastructure_designer import *
from apps.devops_assistant.monitoring_configurator import *
from apps.devops_assistant.pipeline_generator import *


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.devops_assistant")
    assert mod is not None
