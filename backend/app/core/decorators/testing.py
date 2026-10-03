"""
Decorator SDK testing framework for isolation testing.

Provides utilities for testing decorators in isolation:
- DecoratorTestHarness: runs decorator tests with mock apps
- MockBaseApp: a simple BaseApp implementation for testing
- DecoratorIsolationTester: tests decorator isolation properties
"""

from __future__ import annotations

import logging
import time
from typing import Any

from backend.app.core.base_app import BaseApp
from backend.app.core.decorators.base import DecoratorBase

logger = logging.getLogger(__name__)


class MockBaseApp(BaseApp):
    """A simple BaseApp implementation for testing decorators."""

    name: str = "mock_app"
    version: str = "1.0.0"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(config)
        self._execute_count: int = 0
        self._should_fail: bool = False
        self._fail_on_count: int | None = None

    def get_capabilities(self) -> list[dict[str, Any]]:
        return [{"name": "mock_capability", "description": "A mock capability"}]

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        self._execute_count += 1
        if self._should_fail:
            if self._fail_on_count is None or self._execute_count <= self._fail_on_count:
                raise RuntimeError("Mock error for testing")
        return {"result": "success", "task": task, "count": self._execute_count}

    def validate_input(self, task: dict[str, Any]) -> bool:
        return "input" in task or True

    def reset(self) -> None:
        """Reset test state."""
        self._execute_count = 0
        self._should_fail = False
        self._fail_on_count = None


class DecoratorTestHarness:
    """Test harness for running decorator isolation tests."""

    def __init__(self, decorator: DecoratorBase) -> None:
        self._decorator = decorator
        self._mock_app = MockBaseApp()
        self._decorator._wrapped = self._mock_app

    def run_with(self, method: str, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Run a method on the decorator with the mock app and return results."""
        start = time.perf_counter()
        try:
            result = getattr(self._decorator, method)(*args, **kwargs)
            return {
                "success": True,
                "result": result,
                "error": None,
                "latency_ms": round((time.perf_counter() - start) * 1000, 3),
                "execute_count": self._mock_app._execute_count,
            }
        except Exception as exc:
            return {
                "success": False,
                "result": None,
                "error": str(exc),
                "error_type": type(exc).__name__,
                "latency_ms": round((time.perf_counter() - start) * 1000, 3),
                "execute_count": self._mock_app._execute_count,
            }

    def get_decorator(self) -> DecoratorBase:
        """Return the decorator being tested."""
        return self._decorator

    def get_mock_app(self) -> MockBaseApp:
        """Return the mock app."""
        return self._mock_app


class DecoratorIsolationTester:
    """Tests that decorators properly isolate augmentation concerns."""

    @staticmethod
    def test_transparency(decorator: DecoratorBase, task: dict[str, Any]) -> dict[str, Any]:
        """Test that a decorator transparently proxies the wrapped app."""
        mock = MockBaseApp()
        decorator._wrapped = mock

        expected = mock.execute(task)
        actual = decorator.execute(task)

        return {
            "transparent": (
                actual["result"] == expected["result"]
                and actual["task"] == expected["task"]
            ),
            "expected": expected,
            "actual": actual,
        }

    @staticmethod
    def test_augmentation_isolation(
        decorator: DecoratorBase,
        task: dict[str, Any],
        method: str,
    ) -> dict[str, Any]:
        """Test that augmentation hooks don't alter the core result."""
        mock = MockBaseApp()
        decorator._wrapped = mock

        before_calls = mock._execute_count
        result = getattr(decorator, method)(task)
        after_calls = mock._execute_count

        return {
            "augmentation_isolated": after_calls == before_calls + 1,
            "call_count_delta": after_calls - before_calls,
            "result_unchanged": "result" in str(result),
        }

    @staticmethod
    def test_error_propagation(decorator: DecoratorBase) -> dict[str, Any]:
        """Test that exceptions from the wrapped app propagate correctly."""
        mock = MockBaseApp()
        mock._should_fail = True
        decorator._wrapped = mock

        try:
            decorator.execute({"test": True})
            return {"propagated": False, "error": "Expected exception was not raised"}
        except RuntimeError as exc:
            return {"propagated": True, "error": str(exc)}


__all__ = [
    "MockBaseApp",
    "DecoratorTestHarness",
    "DecoratorIsolationTester",
]
