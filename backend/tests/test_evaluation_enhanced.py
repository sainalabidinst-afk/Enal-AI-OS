"""
Tests for enhanced evaluation engine, quality scorer, and vendor rules.
"""

from __future__ import annotations

import pytest

from backend.app.core.evaluation_schema import (
    DIMENSION_RUBRICS,
    DimensionScore,
    EvaluationCase,
    EvaluationDimension,
    EvaluationResult,
)
from backend.app.core.evaluator_engine import evaluator_engine
from backend.app.core.quality_scorer import quality_scorer
from backend.app.core.vendor_rules import (
    evaluate_against_vendor_rules,
    get_vendor_rules,
)


class TestEvaluationSchema:
    def test_dimension_rubrics_have_required_fields(self):
        for dim, rubric in DIMENSION_RUBRICS.items():
            assert "weight" in rubric
            assert "description" in rubric
            assert "thresholds" in rubric
            assert dim in EvaluationDimension

    def test_dimension_score_weighted_score(self):
        ds = DimensionScore(dimension=EvaluationDimension.SECURITY, score=0.8, weight=0.15)
        assert abs(ds.weighted_score - 0.12) < 0.01

    def test_evaluation_result_calculate_overall(self):
        scores = [
            DimensionScore(dimension=EvaluationDimension.SECURITY, score=0.9, weight=0.15),
            DimensionScore(dimension=EvaluationDimension.PERFORMANCE, score=0.7, weight=0.15),
        ]
        result = EvaluationResult(dimension_scores=scores, threshold=0.7)
        overall = result.calculate_overall()
        assert 0.0 <= overall <= 1.0
        assert result.passed is True

    def test_evaluation_case_creation(self):
        case = EvaluationCase(
            case_id="case-001",
            scenario="aws_vpc_design",
            vendor="AWS",
            domain="networking",
            dimensions=[EvaluationDimension.SECURITY, EvaluationDimension.COMPLIANCE],
            tags=["aws", "vpc"],
        )
        assert case.vendor == "AWS"
        assert case.domain == "networking"
        assert len(case.dimensions) == 2


class TestVendorRules:
    def test_get_vendor_rules_aws(self):
        rules = get_vendor_rules("AWS")
        assert "iam" in rules
        assert "vpc" in rules
        assert "monitoring" in rules
        assert len(rules["iam"]["rules"]) > 0

    def test_get_vendor_rules_azure(self):
        rules = get_vendor_rules("Azure")
        assert "identity" in rules
        assert "network" in rules

    def test_get_vendor_rules_gcp(self):
        rules = get_vendor_rules("GCP")
        assert "iam" in rules
        assert "compute" in rules

    def test_get_vendor_rules_unknown(self):
        rules = get_vendor_rules("UnknownVendor")
        assert rules == {}

    def test_evaluate_aws_wildcard_violation(self):
        config = '{"Action": "*", "Resource": "*"}'
        violations = evaluate_against_vendor_rules(config, "AWS")
        assert len(violations) > 0
        assert any("wildcard" in v.get("remediation", "").lower() for v in violations)

    def test_evaluate_aws_no_violations(self):
        config = (
            '{"Action": "ec2:DescribeInstances", "Resource": "arn:aws:ec2:*", '
            '"monitoring": "enabled", "mfa": "enabled"}'
        )
        violations = evaluate_against_vendor_rules(config, "AWS")
        assert len(violations) == 0


class TestQualityScorer:
    @pytest.mark.asyncio
    async def test_score_returns_result_with_vendor(self):
        result = await quality_scorer.score(
            output="Test output",
            criteria={"security": 0.8},
            vendor="AWS",
            scenario="aws_vpc_design",
        )
        assert isinstance(result, EvaluationResult)
        assert 0.0 <= result.overall_score <= 1.0
        assert len(result.dimension_scores) == 10

    @pytest.mark.asyncio
    async def test_score_case(self):
        case = EvaluationCase(
            case_id="case-001",
            scenario="aws_stress_test",
            vendor="AWS",
            dimensions=[EvaluationDimension.PERFORMANCE, EvaluationDimension.SECURITY],
        )
        result = await quality_scorer.score_case(case, "Test output")
        assert result.metadata["case_id"] == "case-001"
        assert result.metadata["vendor"] == "AWS"


class TestEvaluatorEngine:
    @pytest.mark.asyncio
    async def test_evaluate_returns_structured_result(self):
        result = await evaluator_engine.evaluate(
            output="Deploy EC2 with open security group",
            criteria={"security": 0.9},
            vendor="AWS",
            scenario="aws_vpc_design",
        )
        assert "score" in result
        assert "dimensions" in result
        assert "vendor_violations" in result
        assert "insights" in result
        assert len(result["dimensions"]) == 10

    @pytest.mark.asyncio
    async def test_evaluate_detects_vendor_violations(self):
        result = await evaluator_engine.evaluate(
            output="Use wildcard IAM permissions",
            criteria={"security": 0.9},
            vendor="AWS",
            scenario="aws_iam_policy",
        )
        assert len(result["vendor_violations"]) > 0

    @pytest.mark.asyncio
    async def test_evaluate_generates_insights(self):
        result = await evaluator_engine.evaluate(
            output="Deploy without monitoring",
            criteria={"observability": 0.3},
            vendor="AWS",
            scenario="aws_deployment",
        )
        assert len(result["insights"]) > 0

    @pytest.mark.asyncio
    async def test_load_case_from_real_cases(self):
        case = await evaluator_engine.load_case_from_real_cases("cloud_architect", "cloud_001")
        assert case is not None
        assert case.case_id == "cloud_001"

    @pytest.mark.asyncio
    async def test_load_case_from_real_cases_not_found(self):
        case = await evaluator_engine.load_case_from_real_cases("nonexistent", "case_001")
        assert case is None
