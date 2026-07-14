"""
Rule Coverage Tracker
======================

Tracks rule hit counts, false positives, and false negatives.
"""

import logging
from typing import Any
from dataclasses import dataclass, field
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class RuleStats:
    rule_name: str
    hit_count: int = 0
    false_positive_count: int = 0
    false_negative_count: int = 0
    total_executions: int = 0

    @property
    def precision(self) -> float:
        if self.hit_count == 0:
            return 0.0
        return (self.hit_count - self.false_positive_count) / self.hit_count

    @property
    def recall(self) -> float:
        if (self.hit_count + self.false_negative_count) == 0:
            return 0.0
        return (self.hit_count - self.false_positive_count) / (self.hit_count + self.false_negative_count)

    @property
    def f1_score(self) -> float:
        p = self.precision
        r = self.recall
        if p + r == 0:
            return 0.0
        return 2 * (p * r) / (p + r)


class RuleCoverageTracker:
    """Tracks rule coverage and quality metrics."""

    def __init__(self):
        self._stats: dict[str, RuleStats] = defaultdict(lambda: RuleStats(rule_name=""))
        self._rule_names: list[str] = []

    def register_rule(self, rule_name: str):
        """Register a rule for tracking."""
        if rule_name not in self._stats:
            self._stats[rule_name] = RuleStats(rule_name=rule_name)
            self._rule_names.append(rule_name)

    def record_execution(self, rule_name: str, hit: bool):
        """Record a rule execution."""
        if rule_name not in self._stats:
            self.register_rule(rule_name)
        self._stats[rule_name].total_executions += 1
        if hit:
            self._stats[rule_name].hit_count += 1

    def record_false_positive(self, rule_name: str):
        """Record a false positive."""
        if rule_name not in self._stats:
            self.register_rule(rule_name)
        self._stats[rule_name].false_positive_count += 1

    def record_false_negative(self, rule_name: str):
        """Record a false negative."""
        if rule_name not in self._stats:
            self.register_rule(rule_name)
        self._stats[rule_name].false_negative_count += 1

    def get_stats(self, rule_name: str) -> RuleStats:
        """Get stats for a specific rule."""
        return self._stats.get(rule_name, RuleStats(rule_name=rule_name))

    def get_all_stats(self) -> dict[str, RuleStats]:
        """Get stats for all rules."""
        return dict(self._stats)

    def get_summary(self) -> dict[str, Any]:
        """Get overall summary."""
        total_executions = sum(s.total_executions for s in self._stats.values())
        total_hits = sum(s.hit_count for s in self._stats.values())
        total_fp = sum(s.false_positive_count for s in self._stats.values())
        total_fn = sum(s.false_negative_count for s in self._stats.values())

        return {
            "total_rules": len(self._stats),
            "total_executions": total_executions,
            "total_hits": total_hits,
            "total_false_positives": total_fp,
            "total_false_negatives": total_fn,
            "overall_precision": (total_hits - total_fp) / total_hits if total_hits > 0 else 0.0,
            "overall_recall": (total_hits - total_fp) / (total_hits + total_fn) if (total_hits + total_fn) > 0 else 0.0,
        }

    def generate_report(self) -> str:
        """Generate coverage report."""
        lines = ["Rule Coverage Report", "=" * 80, ""]
        lines.append(f"{'Rule':<40} {'Hits':>6} {'FP':>6} {'FN':>6} {'Precision':>10} {'Recall':>8} {'F1':>8}")
        lines.append("-" * 80)

        for rule_name in self._rule_names:
            stats = self._stats[rule_name]
            lines.append(
                f"{rule_name:<40} {stats.hit_count:>6} {stats.false_positive_count:>6} {stats.false_negative_count:>6} "
                f"{stats.precision:>10.2%} {stats.recall:>8.2%} {stats.f1_score:>8.2%}"
            )

        lines.append("-" * 80)
        summary = self.get_summary()
        lines.append(f"Total Rules: {summary['total_rules']}")
        lines.append(f"Total Executions: {summary['total_executions']}")
        lines.append(f"Overall Precision: {summary['overall_precision']:.2%}")
        lines.append(f"Overall Recall: {summary['overall_recall']:.2%}")
        return "\n".join(lines)


rule_coverage_tracker = RuleCoverageTracker()
