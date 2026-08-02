"""
Data Engineer — Data Cleaner.

Detects and remediates missing values, duplicates, outliers,
and format inconsistencies in datasets.
"""

from __future__ import annotations

import logging
import re
from collections import Counter
from typing import Any

from apps.data_engineer.schemas import (
    QualityIssue,
    IssueType,
    IssueSeverity,
)

logger = logging.getLogger(__name__)


class DataCleaner:
    """
    Detects and remediates data quality issues.

    Usage::

        cleaner = DataCleaner()
        cleaned, issues = cleaner.clean(data, operations)
    """

    def clean(
        self,
        data: list[dict[str, Any]],
        operations: list[Any],
    ) -> tuple[list[dict[str, Any]], list[QualityIssue]]:
        """
        Clean data by detecting and remediating issues.

        Args:
            data: List of row dicts.
            operations: TransformOperation list specifying cleaning ops.

        Returns:
            Tuple of (cleaned_data, list of QualityIssue found).
        """
        if not data:
            return [], []

        issues: list[QualityIssue] = []
        result = data

        # Detect issues.
        issues.extend(self._detect_missing(result))
        issues.extend(self._detect_duplicates(result))
        issues.extend(self._detect_outliers(result))
        issues.extend(self._detect_format_issues(result))

        # Apply remediation based on operations.
        for op in operations:
            op_name = op.operation.value if hasattr(op, 'operation') else str(op)
            if op_name == "fill_missing":
                result = self._fill_missing(result, op.parameters if hasattr(op, 'parameters') else {})
            elif op_name == "drop_duplicates":
                result = self._drop_duplicates(result)
            elif op_name == "remove_outliers":
                result = self._remove_outliers(result)
            elif op_name == "normalize":
                result = self._normalize(result, op.parameters if hasattr(op, 'parameters') else {})

        return result, issues

    def _detect_missing(self, data: list[dict[str, Any]]) -> list[QualityIssue]:
        """Detect missing values."""
        issues: list[QualityIssue] = []
        if not data:
            return issues

        columns = data[0].keys()
        for col in columns:
            missing_count = sum(1 for row in data if row.get(col) is None or row.get(col) == "")
            if missing_count > 0:
                pct = missing_count / len(data)
                severity = IssueSeverity.critical if pct > 0.3 else (IssueSeverity.high if pct > 0.1 else IssueSeverity.medium)
                issues.append(QualityIssue(
                    type=IssueType.missing_values,
                    column=col,
                    severity=severity,
                    count=missing_count,
                    remediation=f"Fill missing values using mean/median imputation or drop rows",
                    confidence=0.9,
                ))
        return issues

    def _detect_duplicates(self, data: list[dict[str, Any]]) -> list[QualityIssue]:
        """Detect duplicate rows."""
        issues: list[QualityIssue] = []
        if not data:
            return issues

        seen = set()
        dup_count = 0
        for row in data:
            key = tuple(sorted(row.items()))
            if key in seen:
                dup_count += 1
            else:
                seen.add(key)

        if dup_count > 0:
            issues.append(QualityIssue(
                type=IssueType.duplicate_rows,
                column="",
                severity=IssueSeverity.medium,
                count=dup_count,
                remediation="Remove duplicate rows using drop_duplicates",
                confidence=0.95,
            ))
        return issues

    def _detect_outliers(self, data: list[dict[str, Any]]) -> list[QualityIssue]:
        """Detect outliers using IQR method."""
        issues: list[QualityIssue] = []
        if not data:
            return issues

        for col in data[0].keys():
            values = [row[col] for row in data if isinstance(row.get(col), (int, float))]
            if len(values) < 4:
                continue
            values_sorted = sorted(values)
            n = len(values_sorted)
            q1 = values_sorted[n // 4]
            q3 = values_sorted[3 * n // 4]
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            outliers = [v for v in values if v < lower or v > upper]
            if outliers:
                issues.append(QualityIssue(
                    type=IssueType.outlier,
                    column=col,
                    severity=IssueSeverity.medium,
                    count=len(outliers),
                    remediation=f"Review outliers in {col} (range: {lower:.2f} - {upper:.2f})",
                    confidence=0.8,
                ))
        return issues

    def _detect_format_issues(self, data: list[dict[str, Any]]) -> list[QualityIssue]:
        """Detect format inconsistencies."""
        issues: list[QualityIssue] = []
        if not data:
            return issues

        for col in data[0].keys():
            values = [row.get(col) for row in data if row.get(col) is not None]
            if not values:
                continue

            types = Counter(type(v).__name__ for v in values)
            if len(types) > 1:
                issues.append(QualityIssue(
                    type=IssueType.invalid_format,
                    column=col,
                    severity=IssueSeverity.low,
                    count=sum(1 for v in values if type(v).__name__ != types.most_common(1)[0][0]),
                    remediation=f"Normalize types in column '{col}' to consistent type",
                    confidence=0.7,
                ))
        return issues

    def _fill_missing(self, data: list[dict[str, Any]], params: dict[str, Any]) -> list[dict[str, Any]]:
        """Fill missing values."""
        strategy = params.get("strategy", "zero")
        fill_value = params.get("fill_value", 0)
        columns = params.get("columns", [])
        result = []

        for row in data:
            new_row = dict(row)
            for col in (columns or row.keys()):
                if new_row.get(col) is None or new_row.get(col) == "":
                    if strategy == "zero":
                        new_row[col] = 0
                    elif strategy == "mean":
                        new_row[col] = self._compute_col_mean(data, col)
                    elif strategy == "median":
                        new_row[col] = self._compute_col_median(data, col)
                    else:
                        new_row[col] = fill_value
            result.append(new_row)
        return result

    def _drop_duplicates(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Remove duplicate rows."""
        seen: set[tuple] = set()
        result = []
        for row in data:
            key = tuple(sorted(row.items()))
            if key not in seen:
                seen.add(key)
                result.append(row)
        return result

    def _remove_outliers(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Remove outliers using IQR method."""
        result = data
        columns = [col for col in data[0].keys() if any(isinstance(row.get(col), (int, float)) for row in data)]

        for col in columns:
            values = [row[col] for row in data if isinstance(row.get(col), (int, float))]
            if len(values) < 4:
                continue
            sorted_v = sorted(values)
            n = len(sorted_v)
            q1 = sorted_v[n // 4]
            q3 = sorted_v[3 * n // 4]
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            result = [row for row in result if not (isinstance(row.get(col), (int, float)) and (row[col] < lower or row[col] > upper))]

        return result

    def _normalize(self, data: list[dict[str, Any]], params: dict[str, Any]) -> list[dict[str, Any]]:
        """Normalize numeric columns to 0-1 range."""
        columns = params.get("columns", [])
        result = []
        for row in data:
            new_row = dict(row)
            for col in columns:
                if isinstance(row.get(col), (int, float)):
                    col_min, col_max = self._col_min_max(data, col)
                    if col_max > col_min:
                        new_row[col] = (row[col] - col_min) / (col_max - col_min)
            result.append(new_row)
        return result

    def _compute_col_mean(self, data: list[dict[str, Any]], col: str) -> float:
        values = [row[col] for row in data if isinstance(row.get(col), (int, float))]
        return sum(values) / len(values) if values else 0

    def _compute_col_median(self, data: list[dict[str, Any]], col: str) -> float:
        values = sorted([row[col] for row in data if isinstance(row.get(col), (int, float))])
        if not values:
            return 0
        mid = len(values) // 2
        return (values[mid] + values[~mid]) / 2

    def _col_min_max(self, data: list[dict[str, Any]], col: str) -> tuple[float, float]:
        values = [row[col] for row in data if isinstance(row.get(col), (int, float))]
        if not values:
            return 0.0, 1.0
        return min(values), max(values)
