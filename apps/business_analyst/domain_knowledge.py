"""
Business Analyst — Domain Knowledge.

Provides specialized knowledge for different business domains:
- E-commerce: customer journey, conversion optimization, inventory
- Fintech: regulatory compliance, risk assessment, transaction flows
- Healthcare: HIPAA compliance, patient data, clinical workflows
- SaaS: subscription models, multi-tenancy, usage metrics
- Manufacturing: supply chain, quality control, production planning
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from apps.business_analyst.schemas import Severity, FindingCategory, Finding

logger = logging.getLogger(__name__)


@dataclass
class DomainKnowledge:
    """Specialized knowledge for a business domain."""
    domain: str
    common_requirements: list[str] = field(default_factory=list)
    regulatory_requirements: list[str] = field(default_factory=list)
    key_metrics: list[str] = field(default_factory=list)
    typical_stakeholders: list[str] = field(default_factory=list)


_DOMAIN_KNOWLEDGE: dict[str, DomainKnowledge] = {
    "ecommerce": DomainKnowledge(
        domain="e-commerce",
        common_requirements=[
            "User registration and authentication",
            "Product catalog and search",
            "Shopping cart and checkout",
            "Payment processing",
            "Order tracking",
            "Inventory management",
        ],
        regulatory_requirements=["PCI DSS", "GDPR", "consumer protection laws"],
        key_metrics=["conversion_rate", "cart_abandonment", "aov", "clv"],
        typical_stakeholders=["product owner", "marketing manager", "operations lead"],
    ),
    "fintech": DomainKnowledge(
        domain="fintech",
        common_requirements=[
            "KYC/AML compliance",
            "Transaction processing",
            " fraud detection",
            "Reporting and audit",
            "Multi-currency support",
        ],
        regulatory_requirements=["PCI DSS", "AML/KYC", "GDPR", "PSD2", "SOX"],
        key_metrics=["transaction_volume", "fraud_rate", "processing_time", "compliance_score"],
        typical_stakeholders=["compliance officer", "risk manager", "cto"],
    ),
    "healthcare": DomainKnowledge(
        domain="healthcare",
        common_requirements=[
            "Patient data management",
            "Appointment scheduling",
            "Clinical documentation",
            "Billing and insurance",
            "Telehealth",
        ],
        regulatory_requirements=["HIPAA", "HITECH", "FDA", "GDPR"],
        key_metrics=["patient_satisfaction", "wait_time", "readmission_rate", "compliance_rate"],
        typical_stakeholders=["medical director", "privacy officer", "administrator"],
    ),
    "saas": DomainKnowledge(
        domain="saas",
        common_requirements=[
            "Multi-tenancy",
            "Subscription management",
            "Usage tracking and billing",
            "API access and integration",
            "Role-based access control",
        ],
        regulatory_requirements=["GDPR", "SOC 2", "ISO 27001"],
        key_metrics=["mrr", "churn_rate", "arr", "cac", "ltv"],
        typical_stakeholders=["product manager", "engineering lead", "customer success"],
    ),
    "manufacturing": DomainKnowledge(
        domain="manufacturing",
        common_requirements=[
            "Production planning",
            "Quality control",
            "Supply chain management",
            "Equipment maintenance",
            "Traceability",
        ],
        regulatory_requirements=["ISO 9001", "FDA 21 CFR", "environmental regulations"],
        key_metrics=["oee", "defect_rate", "throughput", "downtime"],
        typical_stakeholders=["production manager", "quality engineer", "supply chain lead"],
    ),
}


class DomainKnowledgeEngine:
    """Provides domain-specific requirements and insights."""

    def get_domain_knowledge(self, domain: str) -> DomainKnowledge | None:
        """Get knowledge for a specific domain."""
        return _DOMAIN_KNOWLEDGE.get(domain.lower())

    def enrich_requirements(self, domain: str, requirements: list[dict[str, Any]]) -> list[Finding]:
        """Enrich requirements with domain-specific insights."""
        findings: list[Finding] = []
        knowledge = self.get_domain_knowledge(domain)
        if not knowledge:
            return findings

        for req in requirements:
            if req.get("type") == "functional":
                findings.append(Finding(
                    category=FindingCategory.schema,
                    severity=Severity.info,
                    title=f"{domain}: common requirement pattern",
                    description=f"Consider {req.get('title', 'requirement')} in context of {domain} best practices",
                    recommendation=f"Review {domain} common requirements: {', '.join(knowledge.common_requirements[:3])}",
                    confidence=0.7,
                ))

        return findings

    def get_regulatory_requirements(self, domain: str) -> list[str]:
        """Get regulatory requirements for a domain."""
        knowledge = self.get_domain_knowledge(domain)
        return knowledge.regulatory_requirements if knowledge else []
