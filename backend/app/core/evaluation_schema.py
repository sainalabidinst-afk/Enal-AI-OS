"""
Evaluation schema and dataclasses for multi-dimensional scoring.

Defines the evaluation dimensions, scoring rubrics, and result structures
used by the enhanced quality scorer and evaluator engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EvaluationDimension(str, Enum):
    """Evaluation dimensions for multi-dimensional scoring."""

    PERFORMANCE = "performance"
    SCALABILITY = "scalability"
    COST = "cost"
    COMPLIANCE = "compliance"
    OBSERVABILITY = "observability"
    SECURITY = "security"
    ACCURACY = "accuracy"
    COHERENCE = "coherence"
    COMPLETENESS = "completeness"
    RELEVANCE = "relevance"


EVALUATION_DIMENSIONS = list(EvaluationDimension)

DIMENSION_RUBRICS: dict[EvaluationDimension, dict[str, Any]] = {
    EvaluationDimension.PERFORMANCE: {
        "weight": 0.15,
        "description": "Response time, throughput, latency",
        "thresholds": {
            "excellent": 0.9,
            "good": 0.7,
            "acceptable": 0.5,
            "poor": 0.0,
        },
    },
    EvaluationDimension.SCALABILITY: {
        "weight": 0.10,
        "description": "Ability to handle increased load",
        "thresholds": {
            "excellent": 0.9,
            "good": 0.7,
            "acceptable": 0.5,
            "poor": 0.0,
        },
    },
    EvaluationDimension.COST: {
        "weight": 0.10,
        "description": "Resource efficiency and cost optimization",
        "thresholds": {
            "excellent": 0.9,
            "good": 0.7,
            "acceptable": 0.5,
            "poor": 0.0,
        },
    },
    EvaluationDimension.COMPLIANCE: {
        "weight": 0.15,
        "description": "Regulatory and policy adherence",
        "thresholds": {
            "excellent": 0.95,
            "good": 0.8,
            "acceptable": 0.6,
            "poor": 0.0,
        },
    },
    EvaluationDimension.OBSERVABILITY: {
        "weight": 0.10,
        "description": "Logging, metrics, tracing, alerting",
        "thresholds": {
            "excellent": 0.9,
            "good": 0.7,
            "acceptable": 0.5,
            "poor": 0.0,
        },
    },
    EvaluationDimension.SECURITY: {
        "weight": 0.15,
        "description": "Security best practices and vulnerability assessment",
        "thresholds": {
            "excellent": 0.95,
            "good": 0.8,
            "acceptable": 0.6,
            "poor": 0.0,
        },
    },
    EvaluationDimension.ACCURACY: {
        "weight": 0.10,
        "description": "Correctness of output and factual accuracy",
        "thresholds": {
            "excellent": 0.95,
            "good": 0.8,
            "acceptable": 0.6,
            "poor": 0.0,
        },
    },
    EvaluationDimension.COHERENCE: {
        "weight": 0.05,
        "description": "Logical flow and consistency",
        "thresholds": {
            "excellent": 0.9,
            "good": 0.7,
            "acceptable": 0.5,
            "poor": 0.0,
        },
    },
    EvaluationDimension.COMPLETENESS: {
        "weight": 0.05,
        "description": "Coverage of required aspects",
        "thresholds": {
            "excellent": 0.95,
            "good": 0.8,
            "acceptable": 0.6,
            "poor": 0.0,
        },
    },
    EvaluationDimension.RELEVANCE: {
        "weight": 0.05,
        "description": "Alignment with requirements and context",
        "thresholds": {
            "excellent": 0.95,
            "good": 0.8,
            "acceptable": 0.6,
            "poor": 0.0,
        },
    },
}


@dataclass
class DimensionScore:
    """Score for a single evaluation dimension."""

    dimension: EvaluationDimension
    score: float = 0.0
    max_score: float = 1.0
    weight: float = 0.0
    feedback: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    @property
    def weighted_score(self) -> float:
        """Calculate weighted contribution to overall score."""
        return min(self.score * self.weight, 1.0)


@dataclass
class EvaluationResult:
    """Complete evaluation result with multi-dimensional scoring."""

    overall_score: float = 0.0
    dimension_scores: list[DimensionScore] = field(default_factory=list)
    feedback: str = ""
    passed: bool = False
    threshold: float = 0.7
    metadata: dict[str, Any] = field(default_factory=dict)

    def calculate_overall(self) -> float:
        """Calculate overall score from dimension scores."""
        if not self.dimension_scores:
            return 0.0
        total_weighted = sum(ds.weighted_score for ds in self.dimension_scores)
        total_weight = sum(ds.weight for ds in self.dimension_scores)
        if total_weight == 0:
            return 0.0
        score = total_weighted / total_weight
        self.overall_score = min(max(score, 0.0), 1.0)
        self.passed = self.overall_score >= self.threshold
        return self.overall_score


@dataclass
class EvaluationCase:
    """Evaluation case with input, expected output, and rubric."""

    case_id: str
    scenario: str
    vendor: str | None = None
    domain: str | None = None
    dimensions: list[EvaluationDimension] = field(default_factory=list)
    expected_output: str | None = None
    rubric: dict[str, Any] = field(default_factory=dict)
    golden_case_path: str | None = None
    tags: list[str] = field(default_factory=list)
