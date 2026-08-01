"""
QA Engineer — Flaky Test Detector.

Detects, classifies, and reports intermittent test failures by
analyzing test execution history.
"""

from __future__ import annotations

import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from apps.qa_engineer.schemas import FlakyClassification, FindingSeverity

logger = logging.getLogger(__name__)


@dataclass
class TestExecution:
    """A single test execution record."""

    test_name: str
    passed: bool
    duration_ms: float
    error_message: str | None = None
    build_id: str | None = None
    timestamp: str | None = None


@dataclass
class FlakyFinding:
    """A flaky test identified in history."""

    test_name: str
    failure_rate: float
    classification: str
    severity: str
    evidence: list[str]
    confidence: float


# Keywords for classification.
_NETWORK_KEYWORDS = {"timeout", "connection", "socket", "network", "request", "api", "http", "503", "502", "504"}
_TIMING_KEYWORDS = {"sleep", "wait", "timing", "delay", "race", "async", "concurrent", "thread"}
_SHARED_STATE_KEYWORDS = {"shared", "global", "fixture", "singleton", "static", "cache", "state"}
_ORDER_KEYWORDS = {"order", "sequence", "before", "after", "setup", "teardown", "depend"}


class FlakyDetector:
    """
    Detects flaky tests from execution history.

    Usage::

        detector = FlakyDetector()
        findings = detector.detect(test_results=[...])
    """

    FLAKY_THRESHOLD = 0.1  # 10% failure rate => potentially flaky
    MIN_EXECUTIONS = 5  # need at least 5 runs to classify

    def detect(self, test_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Detect flaky tests from historical execution data.

        Args:
            test_results: List of execution records, each with:
                - test_name: str
                - passed: bool
                - duration_ms: float
                - error_message: str (optional)
                - build_id: str (optional)

        Returns:
            List of flaky test findings as dicts.
        """
        # Group results by test name.
        by_test: dict[str, list[TestExecution]] = defaultdict(list)
        for raw in test_results:
            exec_record = TestExecution(
                test_name=raw.get("test_name", ""),
                passed=raw.get("passed", False),
                duration_ms=raw.get("duration_ms", 0),
                error_message=raw.get("error_message"),
                build_id=raw.get("build_id"),
                timestamp=raw.get("timestamp"),
            )
            by_test[exec_record.test_name].append(exec_record)

        findings: list[dict[str, Any]] = []

        for test_name, executions in by_test.items():
            if len(executions) < self.MIN_EXECUTIONS:
                continue

            failures = [e for e in executions if not e.passed]
            failure_rate = len(failures) / len(executions)

            if failure_rate < self.FLAKY_THRESHOLD:
                continue

            classification = self._classify_flakiness(failures)
            severity = self._severity_for(failure_rate, classification)
            evidence = [e.error_message or "Failed" for e in failures[:5]]
            confidence = min(1.0, failure_rate * 1.2)

            findings.append({
                "test_name": test_name,
                "failure_rate": round(failure_rate, 4),
                "classification": classification.value,
                "severity": severity.value,
                "evidence": evidence,
                "total_executions": len(executions),
                "total_failures": len(failures),
                "confidence": round(confidence, 4),
            })

        # Sort by failure rate descending.
        findings.sort(key=lambda f: f["failure_rate"], reverse=True)
        return findings

    def detect_from_ci_logs(self, log_content: str) -> list[dict[str, Any]]:
        """
        Parse CI logs to extract test execution results, then detect flaky tests.

        Parses common formats: pytest, JUnit XML results, GitHub Actions output.
        """
        results = self._parse_ci_logs(log_content)
        return self.detect(results)

    def _parse_ci_logs(self, log_content: str) -> list[dict[str, Any]]:
        """Extract test execution records from CI logs."""
        parsed: list[dict[str, Any]] = []
        lines = log_content.splitlines()
        current_build = "unknown"

        for line in lines:
            # Track build IDs.
            build_match = re.search(r'build[#:\s]+(\S+)', line, re.IGNORECASE)
            if build_match:
                current_build = build_match.group(1)

            # Pytest format: "PASSED tests/test_foo.py::TestBar::test_baz" or "FAILED ..."
            test_match = re.match(
                r'\s*(PASSED|FAILED|ERROR|SKIPPED)\s+(.+?)(?:\s+\[.*?\])?$',
                line.strip(),
            )
            if test_match:
                status, test_name = test_match.group(1), test_match.group(2)
                parsed.append({
                    "test_name": test_name.strip(),
                    "passed": status in ("PASSED", "SKIPPED"),
                    "duration_ms": 0,
                    "error_message": None if status == "PASSED" else f"{status} in {test_name}",
                    "build_id": current_build,
                    "timestamp": None,
                })

            # JUnit format: <testcase ...> or <failure ...>
            tc_match = re.match(r'\s*<testcase[^>]*name="([^"]+)"[^>]*>', line)
            if tc_match:
                test_name = tc_match.group(1)
                # Look ahead for failure in the same block (simplified).
                passed = "failure" not in line.lower() and "error" not in line.lower()
                parsed.append({
                    "test_name": test_name,
                    "passed": passed,
                    "duration_ms": 0,
                    "error_message": None if passed else "Test failure in JUnit report",
                    "build_id": current_build,
                    "timestamp": None,
                })

        return parsed

    def _classify_flakiness(self, failures: list[TestExecution]) -> FlakyClassification:
        """Classify the root cause of flaky failures based on error messages."""
        combined_text = " ".join(e.error_message or "" for e in failures).lower()

        if any(kw in combined_text for kw in _NETWORK_KEYWORDS):
            return FlakyClassification.network
        if any(kw in combined_text for kw in _TIMING_KEYWORDS):
            return FlakyClassification.timing
        if any(kw in combined_text for kw in _SHARED_STATE_KEYWORDS):
            return FlakyClassification.shared_state
        if any(kw in combined_text for kw in _ORDER_KEYWORDS):
            return FlakyClassification.order_dependent
        return FlakyClassification.unknown

    def _severity_for(
        self, failure_rate: float, classification: FlakyClassification
    ) -> FindingSeverity:
        """Determine severity based on failure rate and classification."""
        if failure_rate >= 0.5:
            return FindingSeverity.critical
        if failure_rate >= 0.3:
            return FindingSeverity.high
        if failure_rate >= 0.2:
            return FindingSeverity.medium
        return FindingSeverity.low
