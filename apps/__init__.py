"""
ECP Reference Applications
============================

These 5 reference applications demonstrate ECP's capabilities
and serve as golden tests for the platform.

Apps:
1. Trading Analyst - Market analysis and trading insights
2. Network Engineer - Network configuration and management
3. DevOps Assistant - CI/CD and infrastructure automation
4. Code Engineer - Full-stack application generation
5. Research Assistant - AI-powered research with RAG

Each app uses:
- SDK for agent/tool/workflow definitions
- Runtime for execution
- Contracts for stable interfaces
- Marketplace for plugin access
- Studio for observability
"""

from importlib import import_module
from typing import Any


def _load_app(name: str) -> Any | None:
    try:
        module = import_module(f"apps.{name}")
        return module.get_app()
    except Exception:
        return None


APPS = {
    "trading-analyst": _load_app("trading_analyst"),
    "network-engineer": _load_app("network_engineer"),
    "devops-assistant": _load_app("devops_assistant"),
    "code-engineer": _load_app("code_engineer"),
    "research-assistant": _load_app("research_assistant"),
    "full-stack-engineer": _load_app("full_stack_engineer"),
}


def get_app(name: str) -> Any | None:
    """Get a reference application by name."""
    return APPS.get(name)


def list_apps() -> list[dict[str, str]]:
    """List all available reference applications."""
    return [
        {
            "name": app.name,
            "version": app.version,
            "description": app.description,
            "category": app.category,
        }
        for app in APPS.values()
        if app is not None
    ]


__all__ = ["APPS", "get_app", "list_apps"]
