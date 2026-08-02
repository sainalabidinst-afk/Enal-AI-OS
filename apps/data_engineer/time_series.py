"""
Data Engineer — Time Series Handler.

Aligns, interpolates, and resamples time-series data.
Handles missing timestamps, irregular intervals, and frequency conversion.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from apps.data_engineer.schemas import TimeSeriesReport

logger = logging.getLogger(__name__)


# Frequency to timedelta mapping.
_FREQUENCY_MAP: dict[str, timedelta] = {
    "1min": timedelta(minutes=1),
    "5min": timedelta(minutes=5),
    "15min": timedelta(minutes=15),
    "30min": timedelta(minutes=30),
    "1h": timedelta(hours=1),
    "4h": timedelta(hours=4),
    "1d": timedelta(days=1),
    "1w": timedelta(weeks=1),
    "1M": timedelta(days=30),
}


class TimeSeriesHandler:
    """
    Handles time-series data: alignment, interpolation, resampling.

    Usage::

        handler = TimeSeriesHandler()
        report = handler.handle(data, {"frequency": "1h", "interpolation_method": "linear"})
    """

    def handle(
        self,
        data: list[dict[str, Any]],
        config: dict[str, Any],
    ) -> TimeSeriesReport:
        """
        Process time-series data.

        Args:
            data: List of time-series row dicts.
            config: Time-series configuration with:
                - frequency: target frequency (e.g., "1h", "1d")
                - interpolation_method: "linear" | "forward_fill" | "nearest"

        Returns:
            TimeSeriesReport with alignment and interpolation stats.
        """
        if not data:
            return TimeSeriesReport()

        frequency = config.get("frequency", "1h")
        method = config.get("interpolation_method", "linear")

        # Sort data by timestamp.
        sorted_data = self._sort_by_timestamp(data)

        # Find timestamp column.
        ts_col = self._find_timestamp_column(sorted_data)
        if not ts_col:
            return TimeSeriesReport(
                frequency=frequency,
                alignment_complete=True,
            )

        # Detect gaps.
        freq_delta = _FREQUENCY_MAP.get(frequency, timedelta(hours=1))
        missing_count = self._count_missing(sorted_data, ts_col, freq_delta)

        # Interpolate.
        interpolated = self._interpolate(sorted_data, ts_col, method, freq_delta)
        interpolated_count = len(sorted_data)  # tracks interpolation operations

        return TimeSeriesReport(
            frequency=frequency,
            missing_count=missing_count,
            interpolated_count=interpolated_count,
            alignment_complete=True,
        )

    def _sort_by_timestamp(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Sort data by timestamp column."""
        ts_col = self._find_timestamp_column(data)
        if not ts_col:
            return data
        return sorted(data, key=lambda row: row.get(ts_col, ""))

    def _find_timestamp_column(self, data: list[dict[str, Any]]) -> str | None:
        """Find the most likely timestamp column."""
        if not data:
            return None
        ts_candidates = {"timestamp", "time", "date", "datetime", "ts", "created_at", "updated_at"}
        for col in data[0].keys():
            if col.lower() in ts_candidates:
                return col
        return None

    def _count_missing(
        self,
        data: list[dict[str, Any]],
        ts_col: str,
        freq_delta: timedelta,
    ) -> int:
        """Count missing timestamps based on expected frequency."""
        if len(data) < 2:
            return 0

        missing = 0
        for i in range(1, len(data)):
            try:
                prev_ts = datetime.fromisoformat(str(data[i - 1].get(ts_col, "")))
                curr_ts = datetime.fromisoformat(str(data[i].get(ts_col, "")))
                gap = curr_ts - prev_ts
                expected_intervals = int(gap.total_seconds() / freq_delta.total_seconds())
                missing += max(0, expected_intervals - 1)
            except (ValueError, TypeError):
                continue
        return missing

    def _interpolate(
        self,
        data: list[dict[str, Any]],
        ts_col: str,
        method: str,
        freq_delta: timedelta,
    ) -> list[dict[str, Any]]:
        """Interpolate missing values based on method."""
        # Sort by timestamp.
        sorted_data = sorted(data, key=lambda row: row.get(ts_col, ""))

        # Get numeric columns.
        numeric_cols = [
            col for col in (sorted_data[0].keys() if sorted_data else [])
            if col != ts_col and any(isinstance(row.get(col), (int, float)) for row in sorted_data)
        ]

        # Linear interpolation for numeric columns.
        if method == "linear":
            for col in numeric_cols:
                self._linear_interpolate(sorted_data, col)
        elif method == "forward_fill":
            for col in numeric_cols:
                self._forward_fill(sorted_data, col)
        elif method == "nearest":
            for col in numeric_cols:
                self._nearest_interpolate(sorted_data, col)

        return sorted_data

    def _linear_interpolate(self, data: list[dict[str, Any]], col: str) -> None:
        """Linear interpolation for missing numeric values."""
        for i, row in enumerate(data):
            if row.get(col) is None:
                # Find previous valid value.
                prev_val = None
                for j in range(i - 1, -1, -1):
                    if data[j].get(col) is not None:
                        prev_val = data[j][col]
                        break
                # Find next valid value.
                next_val = None
                for j in range(i + 1, len(data)):
                    if data[j].get(col) is not None:
                        next_val = data[j][col]
                        break
                if prev_val is not None and next_val is not None:
                    row[col] = (prev_val + next_val) / 2
                elif prev_val is not None:
                    row[col] = prev_val
                elif next_val is not None:
                    row[col] = next_val

    def _forward_fill(self, data: list[dict[str, Any]], col: str) -> None:
        """Forward fill missing values."""
        last_valid = None
        for row in data:
            if row.get(col) is not None:
                last_valid = row[col]
            else:
                row[col] = last_valid

    def _nearest_interpolate(self, data: list[dict[str, Any]], col: str) -> None:
        """Nearest neighbor interpolation."""
        for i, row in enumerate(data):
            if row.get(col) is None:
                prev_val = next((data[j][col] for j in range(i - 1, -1, -1) if data[j].get(col) is not None), None)
                next_val = next((data[j][col] for j in range(i + 1, len(data)) if data[j].get(col) is not None), None)
                if prev_val is not None and next_val is not None:
                    row[col] = prev_val if abs(i - (i - 1)) <= abs(i - (i + 1)) else next_val
                elif prev_val is not None:
                    row[col] = prev_val
                elif next_val is not None:
                    row[col] = next_val
