"""
Data Engineer — Feature Store.

Generates derived features for downstream analysis with
lineage tracking and versioning support.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.data_engineer.schemas import (
    FeatureSpec,
    FeatureType,
)

logger = logging.getLogger(__name__)


class FeatureStore:
    """
    Generates and manages derived features.

    Usage::

        store = FeatureStore()
        features = store.generate(data, feature_definitions)
    """

    def generate(
        self,
        data: list[dict[str, Any]],
        feature_defs: list[FeatureSpec],
    ) -> list[FeatureSpec]:
        """
        Generate derived features from raw data.

        Args:
            data: Source dataset rows.
            feature_defs: Feature specification list.

        Returns:
            List of FeatureSpec with generated feature metadata.
        """
        generated: list[FeatureSpec] = []

        for feat in feature_defs:
            try:
                self._compute_feature(data, feat)
                generated.append(feat)
            except Exception as e:
                logger.warning("Failed to compute feature '%s': %s", feat.name, e)

        return generated

    def _compute_feature(self, data: list[dict[str, Any]], feat: FeatureSpec) -> None:
        """
        Compute a single feature and add it to each row.

        Args:
            data: Dataset rows (modified in place).
            feat: Feature specification.
        """
        if not data or not feat.dependencies:
            return

        expression = feat.expression.lower()

        for row in data:
            deps = {dep: row.get(dep) for dep in feat.dependencies}

            # Simple expression evaluation.
            if "+" in expression:
                values = [deps.get(d, 0) or 0 for d in feat.dependencies]
                row[feat.name] = sum(v for v in values if isinstance(v, (int, float)))
            elif "-" in expression and len(feat.dependencies) == 2:
                a = deps.get(feat.dependencies[0]) or 0
                b = deps.get(feat.dependencies[1]) or 0
                row[feat.name] = (a or 0) - (b or 0) if isinstance(a, (int, float)) and isinstance(b, (int, float)) else 0
            elif "*" in expression:
                values = [deps.get(d, 1) or 1 for d in feat.dependencies]
                prod = 1
                for v in values:
                    prod *= v if isinstance(v, (int, float)) else 1
                row[feat.name] = prod
            elif "/" in expression and len(feat.dependencies) == 2:
                a = deps.get(feat.dependencies[0]) or 0
                b = deps.get(feat.dependencies[1]) or 0
                if isinstance(a, (int, float)) and isinstance(b, (int, float)) and b != 0:
                    row[feat.name] = a / b
                else:
                    row[feat.name] = 0.0
            elif "log" in expression:
                import math
                val = deps.get(feat.dependencies[0], 1) or 1
                row[feat.name] = math.log(abs(val)) if isinstance(val, (int, float)) and val > 0 else 0.0
            elif "sqrt" in expression:
                import math
                val = deps.get(feat.dependencies[0], 0) or 0
                row[feat.name] = math.sqrt(val) if isinstance(val, (int, float)) and val >= 0 else 0.0
            elif "abs" in expression:
                val = deps.get(feat.dependencies[0], 0) or 0
                row[feat.name] = abs(val) if isinstance(val, (int, float)) else 0
            elif "pow" in expression and len(feat.dependencies) == 2:
                a = deps.get(feat.dependencies[0]) or 0
                b = deps.get(feat.dependencies[1]) or 0
                if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                    row[feat.name] = a ** b
                else:
                    row[feat.name] = 0.0
            elif "max" in expression:
                values = [deps.get(d, 0) or 0 for d in feat.dependencies]
                row[feat.name] = max(values) if values else 0
            elif "min" in expression:
                values = [deps.get(d, 0) or 0 for d in feat.dependencies]
                row[feat.name] = min(values) if values else 0
            elif "avg" in expression or "mean" in expression:
                values = [deps.get(d, 0) or 0 for d in feat.dependencies]
                row[feat.name] = sum(values) / len(values) if values else 0
            else:
                # Default: use first dependency value.
                val = deps.get(feat.dependencies[0])
                row[feat.name] = val if val is not None else 0
