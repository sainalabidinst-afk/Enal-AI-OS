"""
ECP Reference Applications
============================

These 31 reference applications demonstrate ECP's capabilities and serve as
golden tests for the platform.

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
 16. Documentation Engineer - Automated technical documentation
 17. Product Manager - Product management and prioritization
 18. Infrastructure Engineer - Infrastructure design and HA planning
    18. AI Engineer - AI architecture, RAG, and LLMOps design
    19. Cloud Architect - Cloud architecture design (Phase 5)
    20. SRE Engineer - Site reliability engineering (Phase 5)
    21. Compliance Officer - Compliance assessment and audit (Phase 5)
    22. Knowledge Engineer - Ontology and knowledge graphs
    23. Finance Analyst - Financial analysis and risk modeling
    24. Legal Advisor - Legal document analysis and clause review
    25. HSE Specialist - Health safety environment hazard analysis (Phase 5)
    26. Observability - Metrics collection, tracing, log analysis, anomaly detection (Phase 6)
    27. Cybersecurity Analyst - Threat modeling, vulnerability assessment, incident detection, compliance mapping (Phase 6)
    27. AI Ethics & Governance - Bias detection, fairness auditing, explainability (Phase 6)
    28. Supply Chain Analyst - Logistics optimization, route planning, inventory (Phase 6)
    29. Data Scientist - Advanced ML pipelines, feature engineering, model training (Phase 6)
    30. Business Intelligence - Dashboarding, KPI tracking, metric analysis (Phase 6)
    31. Innovation Strategist - Trend analysis, technology foresight, scenario planning (Phase 6)
    32. DevSecOps - CI/CD security gates, vulnerability scanning, compliance (Phase 6)

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
    "cloud-architect": _load_app("cloud_architect"),
    "sre-engineer": _load_app("sre_engineer"),
    "compliance-officer": _load_app("compliance_officer"),
    "knowledge-engineer": _load_app("knowledge_engineer"),
    "finance-analyst": _load_app("finance_analyst"),
    "legal-advisor": _load_app("legal_advisor"),
    "hse-specialist": _load_app("hse_specialist"),
    "ai-ethics-governance": _load_app("ai_ethics_pack"),
    "supply-chain-analyst": _load_app("supply_chain_analyst"),
    "data-scientist": _load_app("data_scientist"),
    "business-intelligence": _load_app("business_intelligence"),
    "innovation-strategist": _load_app("innovation_strategist"),
    "devsecops": _load_app("devsecops"),
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
