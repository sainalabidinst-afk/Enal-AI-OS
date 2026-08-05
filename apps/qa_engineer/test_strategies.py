"""
QA Engineer — Test Generation Strategies.

Provides specialized strategies for generating different types of tests:
- Unit test patterns (arrange-act-assert, given-when-then)
- Integration test patterns (API contracts, database transactions)
- Regression test strategies (risk-based, change-impact)
- Performance test patterns (load, stress, soak)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from apps.qa_engineer.schemas import FindingSeverity, Finding

logger = logging.getLogger(__name__)


@dataclass
class TestStrategy:
    """Test generation strategy configuration."""
    strategy_name: str
    pattern_type: str
    applicable_operations: list[str]
    priority: FindingSeverity = FindingSeverity.medium


class TestGenerationStrategies:
    """
    Provides test generation strategies for different scenarios.

    Usage::

        strategies = TestGenerationStrategies()
        strategy = strategies.get_strategy("unit_test", "python")
    """

    def get_strategy(self, operation: str, language: str) -> TestStrategy | None:
        """Get appropriate test strategy for operation and language."""
        strategies = {
            ("unit_test", "python"): TestStrategy(
                strategy_name="pytest_unittest",
                pattern_type="arrange_act_assert",
                applicable_operations=["unit_test"],
                priority=FindingSeverity.high,
            ),
            ("unit_test", "javascript"): TestStrategy(
                strategy_name="jest_unittest",
                pattern_type="given_when_then",
                applicable_operations=["unit_test"],
                priority=FindingSeverity.high,
            ),
            ("integration_test", "python"): TestStrategy(
                strategy_name="pytest_integration",
                pattern_type="api_contract",
                applicable_operations=["integration_test"],
                priority=FindingSeverity.high,
            ),
            ("performance_validation", "any"): TestStrategy(
                strategy_name="locust_performance",
                pattern_type="load_stress_soak",
                applicable_operations=["performance_validation", "benchmark_test"],
                priority=FindingSeverity.medium,
            ),
        }
        key = (operation, language)
        if key not in strategies:
            key = (operation, "any")
        return strategies.get(key)

    def to_findings(self, operation: str, language: str) -> list[Finding]:
        """Convert strategy recommendations to findings."""
        findings: list[Finding] = []
        strategy = self.get_strategy(operation, language)
        if strategy:
            findings.append(Finding(
                category="schema",
                severity=strategy.priority,
                title=f"Test Strategy: {strategy.strategy_name}",
                description=f"Recommended pattern: {strategy.pattern_type} for {operation} in {language}",
                recommendation=f"Use {strategy.strategy_name} pattern for {operation} generation",
                confidence=0.8,
            ))
        return findings
