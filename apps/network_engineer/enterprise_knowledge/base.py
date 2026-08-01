"""
Base classes for Enterprise Knowledge modules.
Shared types used by all enterprise knowledge analyzers.
"""


class EnterpriseKnowledgeFinding:
    """A single finding from enterprise knowledge analysis."""

    def __init__(
        self,
        domain: str,
        category: str,
        severity: str,
        description: str,
        recommendation: str,
        confidence: float = 0.8,
        vendor: str = "all",
        references: list[str] | None = None,
    ):
        self.domain = domain
        self.category = category
        self.severity = severity
        self.description = description
        self.recommendation = recommendation
        self.confidence = confidence
        self.vendor = vendor
        self.references = references or []

    def to_dict(self) -> dict:
        return {
            "domain": self.domain,
            "category": self.category,
            "severity": self.severity,
            "description": self.description,
            "recommendation": self.recommendation,
            "confidence": round(self.confidence, 2),
            "vendor": self.vendor,
            "references": self.references,
        }
