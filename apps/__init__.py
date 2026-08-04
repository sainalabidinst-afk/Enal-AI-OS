"""
ECP Reference Applications
============================

These 18 reference applications demonstrate ECP's capabilities
and serve as golden tests for the platform.

Apps:
  1. Trading Analyst - Market analysis and trading insights
  2. Network Engineer - Network configuration and management
  3. DevOps Assistant - CI/CD and infrastructure automation
  4. Code Engineer - Full-stack application generation
  5. Research Assistant - AI-powered research with RAG
  6. Full Stack Engineer - Full-stack development
  7. Self Development - Personal improvement and learning
  8. Decision Intelligence - Cross-domain reasoning layer
  9. System Architect - Architecture review and governance
 10. Security Engineer - Security analysis and hardening
 11. Data Engineer - Data lifecycle management
 12. Database Engineer - Database design and optimization
 13. QA Engineer - Quality assurance and testing
 14. Business Analyst - Business-to-technical translation
15. UI/UX Designer - User experience design and design systems
 15. Documentation Engineer - Automated technical documentation
 16. Product Manager - Product management and prioritization
 17. Infrastructure Engineer - Infrastructure design and HA planning
 18. AI Engineer - AI architecture, RAG, and LLMOps design

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
    "self-development": _load_app("self_development"),
    "decision-intelligence": _load_app("decision_intelligence"),
    "system-architect": _load_app("system_architect"),
    "security-engineer": _load_app("security_engineer"),
    "data-engineer": _load_app("data_engineer"),
    "database-engineer": _load_app("database_engineer"),
    "qa-engineer": _load_app("qa_engineer"),
    "business-analyst": _load_app("business_analyst"),
    "documentation-engineer": _load_app("documentation_engineer"),
    "product-manager": _load_app("product_manager"),
    "infrastructure-engineer": _load_app("infrastructure_engineer"),
    "ai-engineer": _load_app("ai_engineer"),
    "ui-ux-designer": _load_app("ui_ux_designer"),
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
