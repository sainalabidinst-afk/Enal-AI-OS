"""
Golden tests for Decorator SDK (RFC-0003).

Verifies:
- DecoratorBase provides transparent BaseApp proxying
- LoggingDecorator logs method calls
- CachingDecorator caches execute() results
- MetricsDecorator collects latency and error metrics
- RetryDecorator retries failed calls
- CircuitBreakerDecorator breaks on repeated failures
- ChainBuilder composes multiple decorators
- HotSwapManager performs zero-downtime replacement
- ContractValidator validates decorator compliance
- DecoratorIsolationTester verifies augmentations don't alter results

Scenario IDs:
- DEC-GT-001 through DEC-GT-010
"""

from __future__ import annotations

import logging
import time

import pytest

from backend.app.core.decorators import (
    CachingDecorator,
    ChainBuilder,
    CircuitBreakerDecorator,
    DecoratorBase,
    DecoratorContractValidator,
    DecoratorIsolationTester,
    DecoratorRegistry,
    HotSwapManager,
    LoggingDecorator,
    MetricsDecorator,
    MockBaseApp,
    RetryDecorator,
)


class TestDecoratorBase:
    def test_decorator_proxies_execute(self):
        """DEC-GT-001: DecoratorBase transparently proxies execute()."""
        mock_app = MockBaseApp()
        decorator = LoggingDecorator(wrapped=mock_app)
        task = {"input": "test"}
        result = decorator.execute(task)
        assert result["result"] == "success"
        assert result["count"] == 1

    def test_decorator_proxies_get_capabilities(self):
        """DEC-GT-002: DecoratorBase transparently proxies get_capabilities()."""
        mock_app = MockBaseApp()
        decorator = LoggingDecorator(wrapped=mock_app)
        caps = decorator.get_capabilities()
        assert len(caps) == 1
        assert caps[0]["name"] == "mock_capability"

    def test_decorator_proxies_validate_input(self):
        """DEC-GT-003: DecoratorBase transparently proxies validate_input()."""
        mock_app = MockBaseApp()
        decorator = LoggingDecorator(wrapped=mock_app)
        assert decorator.validate_input({"test": True}) is True


class TestLoggingDecorator:
    def test_logging_decorator_logs_calls(self, caplog):
        """DEC-GT-004: LoggingDecorator logs method invocations."""
        mock_app = MockBaseApp()
        decorator = LoggingDecorator(wrapped=mock_app)
        with caplog.at_level(logging.INFO):
            decorator.execute({"input": "test"})
        assert any("execute" in r.message for r in caplog.records)

    def test_logging_decorator_propagates_errors(self, caplog):
        """DEC-GT-005: LoggingDecorator logs and re-raises errors."""
        mock_app = MockBaseApp()
        mock_app._should_fail = True
        decorator = LoggingDecorator(wrapped=mock_app)
        with caplog.at_level(logging.ERROR):
            with pytest.raises(RuntimeError):
                decorator.execute({"input": "fail"})
        assert any("raised" in r.message for r in caplog.records)


class TestCachingDecorator:
    def test_caching_decorator_caches_results(self):
        """DEC-GT-007: CachingDecorator caches execute() results (skips wrapped on cache hit)."""
        mock_app = MockBaseApp()
        decorator = CachingDecorator(wrapped=mock_app, config={"max_size": 10, "ttl": 60.0})
        task = {"input": "cached"}
        r1 = decorator.execute(task)
        r2 = decorator.execute(task)
        assert r1["result"] == r2["result"]
        assert r2["task"] == r1["task"]
        assert mock_app._execute_count == 1  # Cache hit on second call

    def test_caching_decorator_different_tasks_not_cached(self):
        """DEC-GT-007: CachingDecorator distinguishes different tasks."""
        mock_app = MockBaseApp()
        decorator = CachingDecorator(wrapped=mock_app, config={"max_size": 10, "ttl": 60.0})
        r1 = decorator.execute({"input": "task1"})
        r2 = decorator.execute({"input": "task2"})
        assert r1 != r2
        assert mock_app._execute_count == 2

    def test_caching_decorator_clear_cache(self):
        """DEC-GT-008: CachingDecorator can clear cache."""
        mock_app = MockBaseApp()
        decorator = CachingDecorator(wrapped=mock_app, config={"max_size": 10, "ttl": 60.0})
        decorator.execute({"input": "task"})
        assert len(decorator._cache) == 1
        decorator.clear_cache()
        assert len(decorator._cache) == 0


class TestMetricsDecorator:
    def test_metrics_decorator_records_latency(self):
        """MetricsDecorator records execution latency."""
        mock_app = MockBaseApp()
        decorator = MetricsDecorator(wrapped=mock_app)
        decorator.execute({"input": "test"})
        metrics = decorator.get_metrics()
        assert "execute" in metrics
        assert metrics["execute"]["call_count"] == 1
        assert metrics["execute"]["last_latency_ms"] > 0

    def test_metrics_decorator_records_errors(self):
        """MetricsDecorator records errors."""
        mock_app = MockBaseApp()
        mock_app._should_fail = True
        decorator = MetricsDecorator(wrapped=mock_app)
        with pytest.raises(RuntimeError):
            decorator.execute({"input": "fail"})
        metrics = decorator.get_metrics()
        assert metrics["execute"]["error_count"] == 1


class TestRetryDecorator:
    def test_retry_decorator_retries_on_failure(self):
        """RetryDecorator retries failed calls."""
        mock_app = MockBaseApp()
        mock_app._should_fail = True
        mock_app._fail_on_count = 2
        decorator = RetryDecorator(
            wrapped=mock_app,
            config={"max_retries": 3, "base_delay": 0.01, "max_delay": 0.1, "backoff_factor": 2.0},
        )
        result = decorator.execute({"input": "retry_test"})
        assert result["result"] == "success"
        assert mock_app._execute_count == 3  # 2 failures + 1 success

    def test_retry_decorator_raises_after_max_retries(self):
        """RetryDecorator raises after max retries exhausted."""
        mock_app = MockBaseApp()
        mock_app._should_fail = True
        mock_app._fail_on_count = 999
        decorator = RetryDecorator(
            wrapped=mock_app,
            config={"max_retries": 2, "base_delay": 0.01, "max_delay": 0.05, "backoff_factor": 2.0},
        )
        with pytest.raises(RuntimeError):
            decorator.execute({"input": "always_fail"})


class TestCircuitBreakerDecorator:
    def test_circuit_breaker_closes_after_success(self):
        """CircuitBreaker works normally when no failures."""
        mock_app = MockBaseApp()
        decorator = CircuitBreakerDecorator(
            wrapped=mock_app,
            config={"failure_threshold": 3, "recovery_timeout": 1.0},
        )
        result = decorator.execute({"input": "test"})
        assert result["result"] == "success"

    def test_circuit_breaker_opens_after_threshold(self):
        """CircuitBreaker opens after threshold failures."""
        mock_app = MockBaseApp()
        mock_app._should_fail = True
        mock_app._fail_on_count = 999
        decorator = CircuitBreakerDecorator(
            wrapped=mock_app,
            config={"failure_threshold": 3, "recovery_timeout": 10.0},
        )
        # First 3 failures
        for _ in range(3):
            with pytest.raises(RuntimeError):
                decorator.execute({"input": "fail"})

        # 4th call should raise CircuitBreaker OPEN without calling the app
        with pytest.raises(RuntimeError, match="Circuit breaker OPEN"):
            decorator.execute({"input": "fail"})


class TestChainBuilder:
    def test_chain_builder_composes_multiple_decorators(self):
        """ChainBuilder composes multiple decorators declaratively."""
        mock_app = MockBaseApp()
        builder = ChainBuilder()
        builder.add("logging").add("metrics").add("caching", {"max_size": 10, "ttl": 60.0})
        chain = builder.build(mock_app)
        assert isinstance(chain, DecoratorBase)
        result = chain.execute({"input": "chained"})
        assert result["result"] == "success"

    def test_chain_builder_preserves_decorator_count(self):
        """ChainBuilder reports correct decorator count."""
        builder = ChainBuilder()
        builder.add("logging").add("metrics")
        assert builder.decorator_count == 2

    def test_chain_builder_unknown_decorator_raises(self):
        """ChainBuilder raises on unknown decorator name."""
        mock_app = MockBaseApp()
        builder = ChainBuilder()
        builder.add("nonexistent_decorator")
        with pytest.raises(ValueError, match="Unknown decorator"):
            builder.build(mock_app)


class TestHotSwapManager:
    def test_hot_swap_replaces_decorator_chain(self):
        """HotSwapManager performs zero-downtime decorator replacement."""
        mock_app = MockBaseApp()
        manager = HotSwapManager()

        specs = [("logging", {}), ("metrics", {})]
        new_decorator = ("caching", {"max_size": 10, "ttl": 60.0})

        new_chain = manager.swap("test_app", mock_app, specs, new_decorator)
        assert isinstance(new_chain, DecoratorBase)
        assert manager.get_active("test_app") is not None

    def test_hot_swap_latency_under_100ms(self):
        """Hot-swap latency < 100ms."""
        mock_app = MockBaseApp()
        manager = HotSwapManager()
        specs = [("logging", {})]
        new_decorator = ("metrics", {})

        start = time.perf_counter()
        manager.swap("latency_test", mock_app, specs, new_decorator)
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert elapsed_ms < 100.0, f"Hot-swap took {elapsed_ms:.3f}ms, expected <100ms"


class TestDecoratorContractValidator:
    def test_validator_valid_decorator_passes(self):
        """ContractValidator validates a compliant decorator."""
        mock_app = MockBaseApp()
        decorator = LoggingDecorator(wrapped=mock_app)
        validator = DecoratorContractValidator()
        result = validator.validate(decorator)
        assert result["contract_compliant"] is True
        assert result["is_baseapp"] is True

    def test_validator_detects_missing_methods(self):
        """ContractValidator detects missing required methods."""
        class BadDecorator(DecoratorBase):
            name = "bad"
            version = "1.0"
            pass  # No get_capabilities, execute, validate_input

        validator = DecoratorContractValidator()
        result = validator.validate(BadDecorator())
        assert result["contract_compliant"] is False
        assert len(result["issues"]) > 0


class TestDecoratorIsolation:
    def test_augmentation_does_not_alter_result(self):
        """DecoratorIsolationTester verifies augmentation isolation."""
        mock_app = MockBaseApp()
        decorator = LoggingDecorator(wrapped=mock_app)
        tester = DecoratorIsolationTester()
        result = tester.test_transparency(decorator, {"input": "isolation_test"})
        assert result["transparent"] is True

    def test_error_propagation(self):
        """DecoratorIsolationTester verifies error propagation."""
        mock_app = MockBaseApp()
        mock_app._should_fail = True
        decorator = LoggingDecorator(wrapped=mock_app)
        tester = DecoratorIsolationTester()
        result = tester.test_error_propagation(decorator)
        assert result["propagated"] is True


class TestDecoratorRegistry:
    def test_registry_lists_available_decorators(self):
        """Registry lists all registered decorators."""
        available = DecoratorRegistry.list_available()
        assert "logging" in available
        assert "caching" in available
        assert "metrics" in available
        assert "retry" in available
        assert "circuit_breaker" in available

    def test_registry_creates_decorator_instances(self):
        """Registry can create decorator instances by name."""
        mock_app = MockBaseApp()
        decorator = DecoratorRegistry.create_decorator("logging", wrapped=mock_app)
        assert isinstance(decorator, LoggingDecorator)

    def test_registry_register_custom_decorator(self):
        """Registry supports custom decorator registration."""
        class CustomDecorator(DecoratorBase):
            name = "custom"
            version = "1.0"

        DecoratorRegistry.register("custom_test", CustomDecorator)
        assert "custom_test" in DecoratorRegistry.list_available()
        DecoratorRegistry.unregister("custom_test")
