"""
Data Engineer — ETL/ELT Pipeline.

Extracts data from heterogeneous sources (CSV, JSON, API, database, file),
applies transformations, and loads into standardized formats.
"""

from __future__ import annotations

import csv
import io
import json
import logging
from typing import Any

from apps.data_engineer.schemas import (
    DataSource,
    SourceType,
    TransformOperation,
    Operation,
)

logger = logging.getLogger(__name__)


class ETLPipeline:
    """
    Extracts, transforms, and loads data from heterogeneous sources.

    Usage::

        pipeline = ETLPipeline()
        data = pipeline.extract(source)
        transformed = pipeline.transform(data, operations)
        loaded = pipeline.load(transformed, target_schema)
    """

    def extract(self, source: DataSource) -> list[dict[str, Any]]:
        """
        Extract data from the specified source.

        Args:
            source: DataSource with type, location, and optional schema.

        Returns:
            List of row dicts.
        """
        if source.type == SourceType.csv:
            return self._extract_csv(source.location)
        elif source.type == SourceType.json:
            return self._extract_json(source.location)
        elif source.type == SourceType.file:
            return self._extract_file(source.location)
        elif source.type == SourceType.api:
            return self._extract_api(source.location)
        elif source.type == SourceType.database:
            return self._extract_database(source.location)
        return []

    def transform(
        self,
        data: list[dict[str, Any]],
        operations: list[TransformOperation],
    ) -> list[dict[str, Any]]:
        """
        Apply a sequence of transformations to the data.

        Args:
            data: List of row dicts.
            operations: List of TransformOperation to apply.

        Returns:
            Transformed list of row dicts.
        """
        result = data
        for op in operations:
            result = self._apply_operation(result, op)
        return result

    def load(
        self,
        data: list[dict[str, Any]],
        target_schema: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Load data into standardized format, optionally validating against schema.

        Args:
            data: Transformed data.
            target_schema: Optional schema to validate against.

        Returns:
            Validated and standardized data.
        """
        if not data:
            return data

        if target_schema:
            data = self._validate_schema(data, target_schema)

        return data

    # ------------------------------------------------------------------
    # Extraction helpers
    # ------------------------------------------------------------------

    def _extract_csv(self, location: str) -> list[dict[str, Any]]:
        """Extract data from a CSV file."""
        try:
            with open(location, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return [dict(row) for row in reader]
        except FileNotFoundError:
            logger.warning("CSV file not found: %s", location)
            return []
        except Exception as e:
            logger.error("Failed to extract CSV from %s: %s", location, e)
            return []

    def _extract_json(self, location: str) -> list[dict[str, Any]]:
        """Extract data from a JSON file."""
        try:
            with open(location, "r", encoding="utf-8") as f:
                content = json.load(f)
                if isinstance(content, list):
                    return content
                elif isinstance(content, dict):
                    return [content]
                return []
        except FileNotFoundError:
            logger.warning("JSON file not found: %s", location)
            return []
        except Exception as e:
            logger.error("Failed to extract JSON from %s: %s", location, e)
            return []

    def _extract_file(self, location: str) -> list[dict[str, Any]]:
        """Extract data from a generic file."""
        try:
            with open(location, "r", encoding="utf-8") as f:
                content = f.read()
            return [{"content": content, "source": location}]
        except FileNotFoundError:
            logger.warning("File not found: %s", location)
            return []

    def _extract_api(self, location: str) -> list[dict[str, Any]]:
        """Extract data from an API endpoint (simulated)."""
        logger.info("API extraction requested for %s (simulated)", location)
        return [{"source": location, "data": [], "note": "API extraction simulated"}]

    def _extract_database(self, location: str) -> list[dict[str, Any]]:
        """Extract data from a database (simulated)."""
        logger.info("Database extraction requested for %s (simulated)", location)
        return [{"source": location, "data": [], "note": "Database extraction simulated"}]

    # ------------------------------------------------------------------
    # Transformation helpers
    # ------------------------------------------------------------------

    def _apply_operation(
        self,
        data: list[dict[str, Any]],
        op: TransformOperation,
    ) -> list[dict[str, Any]]:
        """Apply a single transformation operation."""
        op_name = op.operation.value
        params = op.parameters or {}

        if op_name == "drop_duplicates":
            return self._op_drop_duplicates(data, params)
        elif op_name == "fill_missing":
            return self._op_fill_missing(data, params)
        elif op_name == "remove_outliers":
            return self._op_remove_outliers(data, params)
        elif op_name == "normalize":
            return self._op_normalize(data, params)
        elif op_name == "encode":
            return self._op_encode(data, params)
        elif op_name == "aggregate":
            return self._op_aggregate(data, params)
        elif op_name == "interpolate":
            return self._op_interpolate(data, params)
        return data

    def _op_drop_duplicates(self, data: list[dict[str, Any]], params: dict[str, Any]) -> list[dict[str, Any]]:
        """Remove duplicate rows."""
        subset = params.get("subset", [])
        seen: set[tuple] = set()
        result: list[dict[str, Any]] = []
        for row in data:
            if subset:
                key = tuple(row.get(k) for k in subset)
            else:
                key = tuple(sorted(row.items()))
            if key not in seen:
                seen.add(key)
                result.append(row)
        return result

    def _op_fill_missing(self, data: list[dict[str, Any]], params: dict[str, Any]) -> list[dict[str, Any]]:
        """Fill missing values."""
        strategy = params.get("strategy", "zero")
        fill_value = params.get("fill_value", 0)
        columns = params.get("columns", [])

        result = []
        for row in data:
            new_row = dict(row)
            for col in (columns or row.keys()):
                if col not in new_row or new_row[col] is None or new_row[col] == "":
                    if strategy == "zero":
                        new_row[col] = 0
                    elif strategy == "mean":
                        new_row[col] = self._compute_mean(data, col)
                    elif strategy == "median":
                        new_row[col] = self._compute_median(data, col)
                    elif strategy == "mode":
                        new_row[col] = self._compute_mode(data, col)
                    else:
                        new_row[col] = fill_value
            result.append(new_row)
        return result

    def _op_remove_outliers(self, data: list[dict[str, Any]], params: dict[str, Any]) -> list[dict[str, Any]]:
        """Remove outliers using IQR method."""
        columns = params.get("columns", [])
        iqr_multiplier = params.get("iqr_multiplier", 1.5)
        result = data

        for col in columns:
            values = [float(v) for v in (row.get(col) for row in data) if isinstance(v, (int, float))]
            if not values:
                continue
            q1, q3 = self._quartiles(values)
            iqr = q3 - q1
            lower = q1 - iqr_multiplier * iqr
            upper = q3 + iqr_multiplier * iqr
            result = [row for row in result if not (isinstance(row.get(col), (int, float)) and (row[col] < lower or row[col] > upper))]

        return result

    def _op_normalize(self, data: list[dict[str, Any]], params: dict[str, Any]) -> list[dict[str, Any]]:
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

    def _op_encode(self, data: list[dict[str, Any]], params: dict[str, Any]) -> list[dict[str, Any]]:
        """Encode categorical columns."""
        columns = params.get("columns", [])
        encoding = params.get("encoding", "one_hot")
        result = []

        if encoding == "one_hot":
            for row in data:
                new_row = dict(row)
                for col in columns:
                    val = str(row.get(col, ""))
                    new_row[f"{col}_{val}"] = 1
                    for other_val in {str(r.get(col, "")) for r in data} - {val}:
                        new_row[f"{col}_{other_val}"] = 0
                result.append(new_row)
        else:
            # Label encoding.
            for row in data:
                new_row = dict(row)
                for col in columns:
                    val = str(row.get(col, ""))
                    new_row[col] = hash(val) % 1000
                result.append(new_row)

        return result

    def _op_aggregate(self, data: list[dict[str, Any]], params: dict[str, Any]) -> list[dict[str, Any]]:
        """Aggregate data by group."""
        group_by = params.get("group_by", [])
        aggregations = params.get("aggregations", {})

        if not group_by or not data:
            return data

        groups: dict[tuple, list[dict[str, Any]]] = {}
        for row in data:
            key = tuple(row.get(g) for g in group_by)
            groups.setdefault(key, []).append(row)

        result = []
        for key, rows in groups.items():
            agg_row: dict[str, Any] = {}
            for g, v in zip(group_by, key):
                agg_row[g] = v
            for col, agg_func in aggregations.items():
                raw_values = [r.get(col) for r in rows if isinstance(r.get(col), (int, float))]
                values: list[float] = [float(v) for v in raw_values if v is not None]
                if agg_func == "sum":
                    agg_row[col] = sum(values) if values else 0
                elif agg_func == "avg":
                    agg_row[col] = sum(values) / len(values) if values else 0
                elif agg_func == "count":
                    agg_row[col] = len(rows)
                elif agg_func == "min":
                    agg_row[col] = min(values) if values else 0
                elif agg_func == "max":
                    agg_row[col] = max(values) if values else 0
            result.append(agg_row)

        return result

    def _op_interpolate(self, data: list[dict[str, Any]], params: dict[str, Any]) -> list[dict[str, Any]]:
        """Interpolate missing values (delegates to TimeSeriesHandler)."""
        return data  # Handled by TimeSeriesHandler

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------

    def _validate_schema(self, data: list[dict[str, Any]], schema: dict[str, Any]) -> list[dict[str, Any]]:
        """Filter data to match schema."""
        result = []
        for row in data:
            new_row = {k: v for k, v in row.items() if k in schema}
            result.append(new_row)
        return result

    def _compute_mean(self, data: list[dict[str, Any]], col: str) -> float:
        values: list[float] = [row[col] for row in data if isinstance(row.get(col), (int, float))]
        return sum(values) / len(values) if values else 0

    def _compute_median(self, data: list[dict[str, Any]], col: str) -> float:
        values: list[float] = sorted([row[col] for row in data if isinstance(row.get(col), (int, float))])
        if not values:
            return 0
        mid = len(values) // 2
        return (values[mid] + values[~mid]) / 2

    def _compute_mode(self, data: list[dict[str, Any]], col: str) -> Any:
        from collections import Counter
        values: list[Any] = [row[col] for row in data if row.get(col) is not None]
        if not values:
            return 0
        counts = Counter(values)
        return counts.most_common(1)[0][0]

    def _quartiles(self, values: list[float]) -> tuple[float, float]:
        sorted_v = sorted(values)
        n = len(sorted_v)
        q1 = sorted_v[n // 4]
        q3 = sorted_v[3 * n // 4]
        return q1, q3

    def _col_min_max(self, data: list[dict[str, Any]], col: str) -> tuple[float, float]:
        values: list[float] = [row[col] for row in data if isinstance(row.get(col), (int, float))]
        if not values:
            return 0.0, 1.0
        return min(values), max(values)
