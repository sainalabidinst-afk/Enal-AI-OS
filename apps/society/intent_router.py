"""
Intent Router
==============

Classifies user intent into capability domains.
Routes tasks to the appropriate team of micro-agents.

This is the main entry point for user commands.
User sees: simple conversation.
Behind the scenes: Intent → Domain → Team → Execution → Result
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class IntentDomain(str, Enum):
    NETWORK = "network"
    CODE = "code"
    RESEARCH = "research"
    DEVOPS = "devops"
    TRADING = "trading"
    SECURITY = "security"
    DATA = "data"
    SELF_DEVELOPMENT = "self-development"
    GENERAL = "general"


class IntentComplexity(str, Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


@dataclass
class Intent:
    raw_input: str
    domain: IntentDomain
    complexity: IntentComplexity
    confidence: float = 0.0
    entities: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CapabilityPack:
    domain: IntentDomain
    capabilities: list[str]
    workers: list[str]
    description: str = ""


class IntentRouter:
    """Routes user intent to appropriate capability domains and teams."""

    def __init__(self):
        self._capability_packs: dict[IntentDomain, CapabilityPack] = {}
        self._register_default_packs()

    def _register_default_packs(self):
        self._capability_packs = {
            IntentDomain.NETWORK: CapabilityPack(
                domain=IntentDomain.NETWORK,
                capabilities=["network-design", "config-analysis", "security-audit", "compliance-check", "troubleshooting"],
                workers=["network-engineer", "cisco-specialist", "mikrotik-specialist", "fortinet-specialist"],
                description="Network infrastructure: design, configuration, security, compliance",
            ),
            IntentDomain.CODE: CapabilityPack(
                domain=IntentDomain.CODE,
                capabilities=["code-generation", "code-review", "refactoring", "testing", "documentation"],
                workers=["backend-developer", "frontend-developer", "qa-engineer", "security-engineer"],
                description="Software engineering: development, review, testing, documentation",
            ),
            IntentDomain.RESEARCH: CapabilityPack(
                domain=IntentDomain.RESEARCH,
                capabilities=["literature-review", "data-analysis", "experiment-design", "report-writing"],
                workers=["researcher", "data-analyst", "writer"],
                description="Research: analysis, experimentation, reporting",
            ),
            IntentDomain.DEVOPS: CapabilityPack(
                domain=IntentDomain.DEVOPS,
                capabilities=["infrastructure-design", "ci-cd", "monitoring", "deployment", "automation"],
                workers=["devops-engineer", "cloud-architect", "sre"],
                description="DevOps: infrastructure, CI/CD, monitoring, automation",
            ),
            IntentDomain.TRADING: CapabilityPack(
                domain=IntentDomain.TRADING,
                capabilities=["market-analysis", "risk-assessment", "portfolio-optimization", "strategy-backtesting"],
                workers=["market-analyst", "risk-analyst", "portfolio-manager"],
                description="Trading: market analysis, risk, portfolio, strategy",
            ),
            IntentDomain.SELF_DEVELOPMENT: CapabilityPack(
                domain=IntentDomain.SELF_DEVELOPMENT,
                capabilities=["architecture-analysis", "code-review", "testing", "documentation", "approval-management"],
                workers=["self-developer", "code-analyzer", "test-runner"],
                description="Self-development: autonomous improvement with user approval",
            ),
            IntentDomain.SECURITY: CapabilityPack(
                domain=IntentDomain.SECURITY,
                capabilities=["vulnerability-scan", "penetration-test", "compliance-audit", "incident-response"],
                workers=["security-analyst", "penetration-tester", "compliance-auditor"],
                description="Security: vulnerability scanning, penetration testing, compliance",
            ),
            IntentDomain.DATA: CapabilityPack(
                domain=IntentDomain.DATA,
                capabilities=["data-modeling", "etl-design", "analytics", "visualization"],
                workers=["data-engineer", "data-analyst", "visualization-specialist"],
                description="Data: modeling, ETL, analytics, visualization",
            ),
            IntentDomain.GENERAL: CapabilityPack(
                domain=IntentDomain.GENERAL,
                capabilities=["general-assistance", "question-answering", "documentation"],
                workers=["general-assistant"],
                description="General purpose assistance",
            ),
        }

    def route(self, user_input: str, context: dict[str, Any] | None = None) -> Intent:
        context = context or {}
        lower_input = user_input.lower()

        domain_scores = {}
        for domain, pack in self._capability_packs.items():
            score = sum(1 for cap in pack.capabilities if cap.replace("-", " ") in lower_input or cap in lower_input)
            domain_scores[domain] = score

        entities = self._extract_entities(user_input)
        entity_domain_hints = {
            "cisco": IntentDomain.NETWORK,
            "mikrotik": IntentDomain.NETWORK,
            "fortinet": IntentDomain.NETWORK,
            "python": IntentDomain.CODE,
            "javascript": IntentDomain.CODE,
            "database": IntentDomain.DATA,
            "kubernetes": IntentDomain.DEVOPS,
            "docker": IntentDomain.DEVOPS,
            "aws": IntentDomain.DEVOPS,
            "azure": IntentDomain.DEVOPS,
            "gcp": IntentDomain.DEVOPS,
            "terraform": IntentDomain.DEVOPS,
            "ci": IntentDomain.DEVOPS,
            "cd": IntentDomain.DEVOPS,
            "pipeline": IntentDomain.DEVOPS,
            "research": IntentDomain.RESEARCH,
            "trading": IntentDomain.TRADING,
            "crypto": IntentDomain.TRADING,
            "stock": IntentDomain.TRADING,
            "self-development": IntentDomain.SELF_DEVELOPMENT,
        }
        for entity in entities:
            hinted_domain = entity_domain_hints.get(entity)
            if hinted_domain and hinted_domain in domain_scores:
                domain_scores[hinted_domain] += 2

        best_domain = max(domain_scores, key=domain_scores.get)
        if domain_scores[best_domain] == 0:
            best_domain = IntentDomain.GENERAL

        complexity = self._estimate_complexity(user_input)
        constraints = self._extract_constraints(user_input)

        intent = Intent(
            raw_input=user_input,
            domain=best_domain,
            complexity=complexity,
            confidence=min(1.0, 0.5 + 0.1 * domain_scores[best_domain]),
            entities=entities,
            constraints=constraints,
        )

        logger.info("Intent routed: domain=%s, complexity=%s, confidence=%.2f", best_domain.value, complexity.value, intent.confidence)
        return intent

    def get_capability_pack(self, domain: IntentDomain) -> CapabilityPack | None:
        return self._capability_packs.get(domain)

    def get_available_domains(self) -> list[IntentDomain]:
        return list(self._capability_packs.keys())

    def _estimate_complexity(self, user_input: str) -> IntentComplexity:
        lower_input = user_input.lower()
        complex_keywords = ["build", "create", "design", "architecture", "system", "platform", "migrate", "implement"]
        medium_keywords = ["analyze", "review", "optimize", "improve", "fix", "update"]

        if any(kw in lower_input for kw in complex_keywords):
            return IntentComplexity.COMPLEX
        if any(kw in lower_input for kw in medium_keywords):
            return IntentComplexity.MEDIUM
        return IntentComplexity.SIMPLE

    def _extract_entities(self, user_input: str) -> list[str]:
        entities = []
        lower_input = user_input.lower()
        entity_keywords = {
            "cisco": ["cisco", "ios", "ios-xe", "nx-os"],
            "mikrotik": ["mikrotik", "routeros"],
            "fortinet": ["fortinet", "fortios"],
            "python": ["python", "fastapi", "flask", "django"],
            "javascript": ["javascript", "js", "node", "react", "vue"],
            "database": ["database", "sql", "postgres", "mysql", "mongodb"],
            "api": ["api", "rest", "graphql"],
            "kubernetes": ["kubernetes", "k8s", "kubectl"],
            "docker": ["docker", "container", "image"],
            "aws": ["aws", "amazon", "ec2", "s3"],
            "azure": ["azure", "microsoft"],
            "gcp": ["gcp", "google cloud"],
            "terraform": ["terraform", "iac", "infrastructure"],
            "ci": ["ci/cd", "pipeline", "ci ", " continuous integration"],
            "cd": ["ci/cd", "cd ", "continuous delivery", "deployment"],
            "pipeline": ["pipeline", "workflow", "github actions", "gitlab ci"],
            "research": ["research", "paper", "journal", "study", "bgp"],
            "trading": ["trading", "trade", "stock", "crypto", "btc", "eth", "portfolio", "market", "investasi"],
            "crypto": ["crypto", "bitcoin", "btc", "ethereum", "eth"],
            "stock": ["stock", "saham", "equity", "nasdaq", "sp500"],
            "self-development": ["audit", "bottleneck", "refactor", "improve", "optimize", "self-improve", "patch", "dead code"],
        }

        for entity, keywords in entity_keywords.items():
            if any(kw in lower_input for kw in keywords):
                entities.append(entity)
        return entities

    def _extract_constraints(self, user_input: str) -> list[str]:
        constraints = []
        lower_input = user_input.lower()
        if "budget" in lower_input or "cost" in lower_input:
            constraints.append("budget")
        if "fast" in lower_input or "quick" in lower_input or "urgent" in lower_input:
            constraints.append("timeline")
        if "secure" in lower_input or "security" in lower_input:
            constraints.append("security")
        if "compliance" in lower_input or "regulation" in lower_input:
            constraints.append("compliance")
        return constraints


intent_router = IntentRouter()
