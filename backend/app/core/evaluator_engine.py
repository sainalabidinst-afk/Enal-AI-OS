"""
Evaluator engine for running evaluations.

Runs scheduled evaluations and aggregates metrics.
Supports vendor-specific rule validation and golden case comparison.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from backend.app.core.evaluation_schema import (
    EvaluationCase,
    EvaluationDimension,
    EvaluationResult,
)
from backend.app.core.quality_scorer import quality_scorer
from backend.app.core.vendor_rules import evaluate_against_vendor_rules

logger = logging.getLogger(__name__)


class EvaluatorEngine:
    """Run evaluations against agent/tool outputs with vendor-specific rules."""

    def __init__(self, real_cases_dir: str | Path | None = None) -> None:
        self.real_cases_dir = Path(real_cases_dir) if real_cases_dir else Path("real_cases")

    async def evaluate(
        self,
        output: str,
        criteria: dict[str, Any] | None = None,
        vendor: str | None = None,
        scenario: str | None = None,
        case_id: str | None = None,
    ) -> dict[str, Any]:
        result = await quality_scorer.score(output, criteria, vendor=vendor, scenario=scenario)
        vendor_violations = evaluate_against_vendor_rules(output, vendor or "generic")
        insights = self._generate_insights(result, vendor_violations)
        return {
            "score": result.overall_score,
            "dimensions": [
                {
                    "dimension": ds.dimension.value,
                    "score": ds.score,
                    "weight": ds.weight,
                    "feedback": ds.feedback,
                }
                for ds in result.dimension_scores
            ],
            "vendor_violations": vendor_violations,
            "insights": insights,
            "feedback": result.feedback,
            "passed": result.passed,
            "threshold": result.threshold,
            "case_id": case_id,
            "scenario": scenario,
            "vendor": vendor,
        }

    async def evaluate_case(self, case: EvaluationCase, output: str) -> dict[str, Any]:
        result = await self.evaluate(
            output,
            criteria=case.rubric,
            vendor=case.vendor,
            scenario=case.scenario,
            case_id=case.case_id,
        )
        golden_comparison = None
        if case.golden_case_path:
            golden_comparison = await self._compare_with_golden(case.golden_case_path, output)
        result["golden_comparison"] = golden_comparison
        return result

    async def load_case_from_real_cases(self, pack: str, case_dir: str) -> EvaluationCase | None:
        """Load an evaluation case from real_cases directory."""
        case_path = self.real_cases_dir / pack / case_dir
        if not case_path.exists():
            return None
        eval_file = case_path / "evaluation.md"
        if not eval_file.exists():
            return None
        content = eval_file.read_text(encoding="utf-8")
        return self._parse_evaluation_md(case_dir, content)

    def _parse_evaluation_md(self, case_id: str, content: str) -> EvaluationCase:
        """Parse evaluation.md into EvaluationCase."""
        lines = content.splitlines()
        scenario = "generic"
        vendor = None
        domain = None
        dimensions: list[EvaluationDimension] = list(EvaluationDimension)
        rubric: dict[str, Any] = {}
        for line in lines:
            if line.startswith("Scenario:"):
                scenario = line.split(":", 1)[1].strip()
                if "aws" in scenario.lower():
                    vendor = "AWS"
                elif "azure" in scenario.lower():
                    vendor = "Azure"
                elif "gcp" in scenario.lower():
                    vendor = "GCP"
            elif line.startswith("Vendor:"):
                vendor = line.split(":", 1)[1].strip()
            elif line.startswith("Domain:"):
                domain = line.split(":", 1)[1].strip()
            elif line.startswith("## "):
                dim_name = line.replace("## ", "").strip().lower().replace(" ", "_")
                try:
                    dim = EvaluationDimension(dim_name)
                    if dim not in dimensions:
                        dimensions.append(dim)
                except ValueError:
                    pass
        return EvaluationCase(
            case_id=case_id,
            scenario=scenario,
            vendor=vendor,
            domain=domain,
            dimensions=dimensions,
            rubric=rubric,
            golden_case_path=None,
        )

    async def _compare_with_golden(
        self, golden_path: str | Path, output: str
    ) -> dict[str, Any] | None:
        """Compare output with golden case."""
        try:
            golden_file = Path(golden_path)
            if not golden_file.exists():
                return None
            golden_content = golden_file.read_text(encoding="utf-8")
            return {
                "golden_length": len(golden_content),
                "output_length": len(output),
                "length_ratio": len(output) / len(golden_content) if golden_content else 0.0,
                "match_score": self._calculate_similarity(output, golden_content),
            }
        except Exception as exc:
            logger.warning("Golden case comparison failed: %s", exc)
            return None

    def _calculate_similarity(self, output: str, golden: str) -> float:
        """Calculate similarity between output and golden case."""
        if not golden or not output:
            return 0.0
        output_words = set(output.lower().split())
        golden_words = set(golden.lower().split())
        if not golden_words:
            return 0.0
        intersection = output_words & golden_words
        return len(intersection) / len(golden_words)

    def _generate_insights(
        self, result: EvaluationResult, violations: list[dict[str, Any]]
    ) -> list[str]:
        """Generate actionable insights from evaluation results."""
        insights: list[str] = []
        for ds in result.dimension_scores:
            if ds.score < 0.5:
                if ds.dimension == EvaluationDimension.PERFORMANCE:
                    insights.append(
                        "Performance bottleneck detected — review response times and throughput."
                    )
                elif ds.dimension == EvaluationDimension.SECURITY:
                    insights.append(
                        "Security gap identified — review access controls and encryption."
                    )
                elif ds.dimension == EvaluationDimension.COST:
                    insights.append(
                        "Cost risk detected — review resource sizing and autoscaling policies."
                    )
                elif ds.dimension == EvaluationDimension.COMPLIANCE:
                    insights.append(
                        "Compliance gap — review regulatory requirements and audit trails."
                    )
                elif ds.dimension == EvaluationDimension.OBSERVABILITY:
                    insights.append(
                        "Observability gap — enable logging, metrics, and distributed tracing."
                    )
                elif ds.dimension == EvaluationDimension.SCALABILITY:
                    insights.append(
                        "Scalability concern — review capacity planning and load handling."
                    )
        for violation in violations:
            severity = violation.get("severity", "low")
            desc = violation.get("description", "Vendor rule violation")
            remediation = violation.get("remediation", "")
            insights.append(f"[{severity.upper()}] {desc}. Recommendation: {remediation}")
        return insights[:10]


evaluator_engine = EvaluatorEngine()
