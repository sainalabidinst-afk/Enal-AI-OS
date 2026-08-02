"""
Data Engineer — Dataset Validator.

Validates dataset integrity, schema compliance, and quality
before consumption by downstream packs.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.data_engineer.schemas import (
    QualityReport,
    QualityIssue,
    IssueType,
    IssueSeverity,
    QualityRule,
    QualityRuleSpec,
)

logger = logging.getLogger(__name__)


class DatasetValidator:
    """
    Validates datasets against schemas and quality rules.

    Usage::

        validator = DatasetValidator()
        result = validator.validate(data, schema, quality_rules)
    """

    def validate(
        self,
        data: list[dict[str, Any]],
        schema: dict[str, Any] | None,
        quality_rules: list[QualityRuleSpec],
    ) -> QualityReport:
        """
        Validate dataset against schema and quality rules.

        Args:
            data: Dataset rows.
            schema: Expected schema (column names and types).
            quality_rules: Quality rules to check.

        Returns:
            QualityReport with validation results and issues.
        """
        issues: list[QualityIssue] = []

        if not data:
            return QualityReport(
                overall_score=0.0,
                issues=[QualityIssue(
                    type=IssueType.invalid_format,
                    column="",
                    severity=IssueSeverity.critical,
                    count=0,
                    remediation="Dataset is empty — cannot validate",
                    confidence=1.0,
                )],
            )

        # Schema validation.
        if schema:
            issues.extend(self._validate_schema(data, schema))

        # Quality rule validation.
        for rule in quality_rules:
            issues.extend(self._check_quality_rule(data, rule))

        # Compute quality scores.
        scores = self._compute_scores(data, issues)
        return QualityReport(
            completeness=scores.get("completeness", 1.0),
            uniqueness=scores.get("uniqueness", 1.0),
            validity=scores.get("validity", 1.0),
            freshness=scores.get("freshness", 1.0),
            consistency=scores.get("consistency", 1.0),
            overall_score=scores.get("overall", 1.0),
            issues=issues,
        )

    def _validate_schema(self, data: list[dict[str, Any]], schema: dict[str, Any]) -> list[QualityIssue]:
        """Validate data against expected schema."""
        issues: list[QualityIssue] = []
        if not data:
            return issues

        expected_cols = set(schema.keys())
        actual_cols = set(data[0].keys()) if data else set()

        # Missing columns.
        missing = expected_cols - actual_cols
        for col in missing:
            issues.append(QualityIssue(
                type=IssueType.invalid_format,
                column=col,
                severity=IssueSeverity.high,
                count=len(data),
                remediation=f"Add missing column '{col}' to dataset",
                confidence=0.95,
            ))

        # Type mismatches.
        for col, expected_type in schema.items():
            if col not in actual_cols:
                continue
            mismatches = 0
            for row in data:
                val = row.get(col)
                if val is not None and not self._type_matches(val, expected_type):
                    mismatches += 1
            if mismatches > 0:
                issues.append(QualityIssue(
                    type=IssueType.invalid_format,
                    column=col,
                    severity=IssueSeverity.medium,
                    count=mismatches,
                    remediation=f"Convert column '{col}' to {expected_type}",
                    confidence=0.85,
                ))

        return issues

    def _check_quality_rule(
        self, data: list[dict[str, Any]], rule: QualityRuleSpec
    ) -> list[QualityIssue]:
        """Check a single quality rule."""
        issues: list[QualityIssue] = []
        rule_name = rule.rule.value
        thresholds = rule.thresholds or {}

        if not data:
            return issues

        if rule_name == "completeness":
            min_completeness = thresholds.get("min", 0.8)
            for col in data[0].keys():
                missing = sum(1 for row in data if row.get(col) is None or row.get(col) == "")
                completeness = 1 - (missing / len(data))
                if completeness < min_completeness:
                    issues.append(QualityIssue(
                        type=IssueType.missing_values,
                        column=col,
                        severity=IssueSeverity.high,
                        count=missing,
                        remediation=f"Impute or remove missing values in '{col}'",
                        confidence=0.9,
                    ))

        elif rule_name == "uniqueness":
            min_uniqueness = thresholds.get("min", 0.9)
            for col in data[0].keys():
                values = [row.get(col) for row in data if row.get(col) is not None]
                unique_count = len(set(values))
                uniqueness = unique_count / len(values) if values else 1.0
                if uniqueness < min_uniqueness:
                    issues.append(QualityIssue(
                        type=IssueType.duplicate_rows,
                        column=col,
                        severity=IssueSeverity.medium,
                        count=len(values) - unique_count,
                        remediation=f"Remove duplicates in '{col}'",
                        confidence=0.8,
                    ))

        elif rule_name == "validity":
            for col in data[0].keys():
                invalid = sum(1 for row in data if not self._is_valid_value(row.get(col)))
                if invalid > 0:
                    issues.append(QualityIssue(
                        type=IssueType.invalid_format,
                        column=col,
                        severity=IssueSeverity.medium,
                        count=invalid,
                        remediation=f"Fix invalid values in '{col}'",
                        confidence=0.8,
                    ))

        return issues

    def _type_matches(self, value: Any, expected_type: str) -> bool:
        """Check if a value matches an expected type string."""
        type_map = {
            "string": str,
            "int": int,
            "integer": int,
            "float": (int, float),
            "number": (int, float),
            "bool": bool,
            "boolean": bool,
            "datetime": str,
        }
        expected = type_map.get(expected_type.lower())
        if expected is None:
            return True
        return isinstance(value, expected)

    def _is_valid_value(self, value: Any) -> bool:
        """Check if a value is valid (not None, not empty)."""
        return value is not None and value != "" and not (isinstance(value, float) and (value != value))  # NaN check

    def _compute_scores(self, data: list[dict[str, Any]], issues: list[QualityIssue]) -> dict[str, float]:
        """Compute quality dimension scores."""
        if not data:
            return {"overall": 0.0}

        total_cells = len(data) * len(data[0]) if data else 1
        issue_cells = sum(i.count for i in issues)
        completeness = max(0.0, 1 - issue_cells / total_cells)

        # Uniqueness: ratio of unique rows.
        rows = [tuple(sorted(row.items())) for row in data]
        uniqueness = len(set(rows)) / len(rows) if rows else 1.0

        # Validity: based on invalid_format issues.
        invalid_count = sum(i.count for i in issues if i.type == IssueType.invalid_format)
        validity = max(0.0, 1 - invalid_count / total_cells)

        # Freshness: simulated as 1.0 (no timestamps in basic validation).
        freshness = 1.0

        # Consistency: based on format issues.
        format_issues = sum(i.count for i in issues if i.type == IssueType.invalid_format)
        consistency = max(0.0, 1 - format_issues / total_cells)

        overall = (completeness + uniqueness + validity + freshness + consistency) / 5

        return {
            "completeness": round(completeness, 4),
            "uniqueness": round(uniqueness, 4),
            "validity": round(validity, 4),
            "freshness": round(freshness, 4),
            "consistency": round(consistency, 4),
            "overall": round(overall, 4),
        }
