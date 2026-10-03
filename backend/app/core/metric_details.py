"""
Metric details for evaluation dashboards.

Provides per-metric deep-dive analytics.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class MetricDetails:
    """Per-metric deep-dive analytics."""

    def get_metric_details(self, metric_name: str) -> dict[str, Any]:
        return {
            "metric": metric_name,
            "values": [],
            "average": 0.0,
            "min": 0.0,
            "max": 0.0,
            "trend": "stable",
        }


metric_details = MetricDetails()
