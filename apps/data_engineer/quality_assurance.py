"""
Data Engineer — Data Quality Assurance.

Measures and reports data quality metrics across 5 dimensions:
completeness, uniqueness, validity, freshness, and consistency.
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


class DataQualityAssurance:
    """
    Measures and reports data quality metrics.

    Usage::

        dqa = DataQualityAssurance()
        report = dqa.assess(data, validation_result, cleaning_issues, quality_rules)
    """

    def assess(
        self,
        data: list[dict[str, Any]],
        validation_result: QualityReport,
        cleaning_issues: list[QualityIssue],
        quality_rules: list[QualityRuleSpec],
    ) -> QualityReport:
        """
        Assess overall data quality.

        Args:
            data: Cleaned dataset rows.
            validation_result: Result from DatasetValidator.
            cleaning_issues: Issues found during cleaning.
            quality_rules: Applied quality rules.

        Returns:
            QualityReport with scores across all dimensions.
        """
        if not data:
            return QualityReport(
                overall_score=0.0,
                issues=[QualityIssue(
                    type=IssueType.invalid_format,
                    column="",
                    severity=IssueSeverity.critical,
                    remediation="Dataset is empty",
                    confidence=1.0,
                )],
            )

        # Start from validation report.
        report = QualityReport(
            completeness=validation_result.completeness,
            uniqueness=validation_result.uniqueness,
            validity=validation_result.validity,
            freshness=validation_result.freshness,
            consistency=validation_result.consistency,
            overall_score=validation_result.overall_score,
            issues=list(validation_result.issues),
        )

        # Adjust scores based on cleaning issues.
        if cleaning_issues:
            for issue in cleaning_issues:
                if issue.type == IssueType.outlier and issue.count > 0:
                    report.consistency = max(0.0, report.consistency - 0.05)
                    report.issues.append(issue)
                elif issue.type == IssueType.missing_values:
                    report.completeness = max(0.0, report.completeness - 0.03)
                    report.issues.append(issue)

        # Recompute overall score.
        report.overall_score = round(
            (report.completeness + report.uniqueness + report.validity +
             report.freshness + report.consistency) / 5,
            4,
        )

        # Deduplicate issues by (type, column).
        seen: set[str] = set()
        unique_issues: list[QualityIssue] = []
        for issue in report.issues:
            key = f"{issue.type.value}:{issue.column}"
            if key not in seen:
                seen.add(key)
                unique_issues.append(issue)
        report.issues = unique_issues

        # Generate recommendations.
        recommendations = self._generate_recommendations(report)
        if recommendations:
            for rec in recommendations:
                report.issues.append(QualityIssue(
                    type=IssueType.invalid_format,
                    column="",
                    severity=IssueSeverity.low,
                    count=0,
                    remediation=rec,
                    confidence=0.7,
                ))

        return report

    def _generate_recommendations(self, report: QualityReport) -> list[str]:
        """Generate prioritized recommendations based on quality scores."""
        recs: list[str] = []
        if report.completeness < 0.8:
            recs.append("Completeness below 80%: implement missing value imputation strategy")
        if report.uniqueness < 0.9:
            recs.append("Uniqueness below 90%: investigate duplicate sources")
        if report.validity < 0.9:
            recs.append("Validity below 90%: enforce strict schema validation at ingestion")
        if report.consistency < 0.9:
            recs.append("Consistency below 90%: standardize data formats and units")
        if report.freshness < 0.8:
            recs.append("Freshness below 80%: reduce data latency in pipeline")
        return recs
