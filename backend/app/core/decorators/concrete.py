"""
Concrete decorator implementations for RFC-0003.

Each decorator extends DecoratorBase and overrides the appropriate
hook methods to inject behavior (logging, caching, metrics, retry,
circuit breaker).
"""

from __future__ import annotations

import logging
import time
from collections import OrderedDict
from collections.abc import Callable
from typing import Any

from backend.app.core.decorators.base import DecoratorBase

logger = logging.getLogger(__name__)


class LoggingDecorator(DecoratorBase):
    """Logs all method invocations on the wrapped app."""

    name = "logging_decorator"
    version = "1.0.0"

    def _before(self, method_name: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> None:
        logger.info("→ %s.%s called with args=%s kwargs=%s",
                     type(self._wrapped).__name__ if self._wrapped else "None",
                     method_name, args, kwargs)

    def _after(
        self,
        method_name: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        result: Any,
    ) -> Any:
        logger.info("← %s.%s returned: %s",
                     type(self._wrapped).__name__ if self._wrapped else "None",
                     method_name, result)
        return result

    def _on_error(
        self,
        method_name: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        exc: Exception,
    ) -> Any:
        logger.error("✗ %s.%s raised: %s",
                      type(self._wrapped).__name__ if self._wrapped else "None",
                      method_name, exc)
        raise exc


class CachingDecorator(DecoratorBase):
    """Caches results of execute() calls based on input hash."""

    name = "caching_decorator"
    version = "1.0.0"

    def __init__(self, wrapped: Any = None, config: dict[str, Any] | None = None) -> None:
        super().__init__(wrapped, config)
        self._cache: OrderedDict[str, Any] = OrderedDict()
        self._max_size: int = config.get("max_size", 128) if config else 128
        self._ttl: float = config.get("ttl", 300.0) if config else 300.0
        self._timestamps: dict[str, float] = {}

    def _cache_key(self, method_name: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> str:
        import json
        key_data = {
            "method": method_name,
            "args": [repr(a) for a in args],
            "kwargs": {k: repr(v) for k, v in sorted(kwargs.items())},
        }
        return json.dumps(key_data, sort_keys=True)

    def _before(self, method_name: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> None:
        if method_name == "execute":
            key = self._cache_key(method_name, args, kwargs)
            now = time.monotonic()
            if key in self._cache:
                if now - self._timestamps.get(key, 0) < self._ttl:
                    logger.debug("Cache HIT for key: %s", key)
                else:
                    del self._cache[key]
                    del self._timestamps[key]

    def _around(
        self,
        method_name: str,
        func: Callable[..., Any],
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        """Short-circuit cache hits before calling the wrapped method."""
        if method_name == "execute":
            key = self._cache_key(method_name, args, kwargs)
            now = time.monotonic()
            if key in self._cache:
                if now - self._timestamps.get(key, 0) < self._ttl:
                    logger.debug("Cache HIT (around) for key: %s", key)
                    return self._cache[key]
                else:
                    del self._cache[key]
                    del self._timestamps[key]
        return func(*args, **kwargs)

    def _after(
        self,
        method_name: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        result: Any,
    ) -> Any:
        if method_name == "execute":
            key = self._cache_key(method_name, args, kwargs)
            now = time.monotonic()
            self._cache[key] = result
            self._timestamps[key] = now
            while len(self._cache) > self._max_size:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
                del self._timestamps[oldest_key]
        return result

    def clear_cache(self) -> None:
        """Clear all cached entries."""
        self._cache.clear()
        self._timestamps.clear()


class MetricsDecorator(DecoratorBase):
    """Collects execution metrics (latency, call count, error count)."""

    name = "metrics_decorator"
    version = "1.0.0"

    def __init__(self, wrapped: Any = None, config: dict[str, Any] | None = None) -> None:
        super().__init__(wrapped, config)
        self._metrics: dict[str, dict[str, Any]] = {}

    def _before(self, method_name: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> None:
        if method_name not in self._metrics:
            self._metrics[method_name] = {
                "call_count": 0,
                "error_count": 0,
                "total_latency_ms": 0.0,
                "min_latency_ms": float("inf"),
                "max_latency_ms": 0.0,
            }
        m = self._metrics[method_name]
        m["call_count"] += 1
        m["_start_time"] = time.perf_counter()

    def _after(
        self,
        method_name: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        result: Any,
    ) -> Any:
        m = self._metrics.get(method_name, {})
        start = m.pop("_start_time", time.perf_counter())
        latency_ms = (time.perf_counter() - start) * 1000.0
        m["total_latency_ms"] += latency_ms
        m["min_latency_ms"] = min(m["min_latency_ms"], latency_ms)
        m["max_latency_ms"] = max(m["max_latency_ms"], latency_ms)
        m["last_latency_ms"] = round(latency_ms, 3)
        m["avg_latency_ms"] = round(m["total_latency_ms"] / m["call_count"], 3)
        return result

    def _on_error(
        self,
        method_name: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        exc: Exception,
    ) -> Any:
        m = self._metrics.get(method_name, {})
        if "_start_time" in m:
            start = m.pop("_start_time")
            elapsed = (time.perf_counter() - start) * 1000.0
            m["total_latency_ms"] += elapsed
        m["error_count"] += 1
        m["last_error"] = str(exc)
        m["last_error_type"] = type(exc).__name__
        raise exc

    def get_metrics(self) -> dict[str, dict[str, Any]]:
        """Return collected metrics."""
        return dict(self._metrics)

    def reset_metrics(self) -> None:
        """Reset all collected metrics."""
        self._metrics.clear()


class RetryDecorator(DecoratorBase):
    """Retries failed method calls with exponential backoff."""

    name = "retry_decorator"
    version = "1.0.0"

    def __init__(self, wrapped: Any = None, config: dict[str, Any] | None = None) -> None:
        super().__init__(wrapped, config)
        self._max_retries: int = config.get("max_retries", 3) if config else 3
        self._base_delay: float = config.get("base_delay", 0.1) if config else 0.1
        self._max_delay: float = config.get("max_delay", 5.0) if config else 5.0
        self._backoff_factor: float = config.get("backoff_factor", 2.0) if config else 2.0
        self._retry_counts: dict[str, int] = {}

    def _around(
        self,
        method_name: str,
        func: Callable[..., Any],
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        last_exc: Exception | None = None
        for attempt in range(self._max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                last_exc = exc
                self._retry_counts[method_name] = attempt + 1
                if attempt < self._max_retries:
                    delay = min(
                        self._base_delay * (self._backoff_factor ** attempt),
                        self._max_delay,
                    )
                    logger.warning(
                        "Retry %d/%d for %s in %.3fs: %s",
                        attempt + 1, self._max_retries, method_name, delay, exc,
                    )
                    time.sleep(delay)
                else:
                    logger.error("Max retries exceeded for %s", method_name)
        if last_exc:
            raise last_exc

    def get_retry_stats(self) -> dict[str, int]:
        """Return retry statistics per method."""
        return dict(self._retry_counts)


class CircuitBreakerDecorator(DecoratorBase):
    """Implements circuit breaker pattern for fault tolerance."""

    name = "circuit_breaker_decorator"
    version = "1.0.0"

    class State:
        CLOSED = "closed"
        OPEN = "open"
        HALF_OPEN = "half_open"

    def __init__(self, wrapped: Any = None, config: dict[str, Any] | None = None) -> None:
        super().__init__(wrapped, config)
        self._failure_threshold: int = config.get("failure_threshold", 5) if config else 5
        self._recovery_timeout: float = config.get("recovery_timeout", 30.0) if config else 30.0
        self._states: dict[str, dict[str, Any]] = {}

    def _get_state(self, method_name: str) -> dict[str, Any]:
        if method_name not in self._states:
            self._states[method_name] = {
                "state": self.State.CLOSED,
                "failure_count": 0,
                "last_failure_time": 0.0,
            }
        return self._states[method_name]

    def _around(
        self,
        method_name: str,
        func: Callable[..., Any],
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        s = self._get_state(method_name)
        now = time.monotonic()

        if s["state"] == self.State.OPEN:
            if now - s["last_failure_time"] < self._recovery_timeout:
                raise RuntimeError(
                    f"Circuit breaker OPEN for {method_name} — "
                    f"retrying after {self._recovery_timeout}s"
                )
            s["state"] = self.State.HALF_OPEN

        try:
            result = func(*args, **kwargs)
            s["state"] = self.State.CLOSED
            s["failure_count"] = 0
            return result
        except Exception:
            s["failure_count"] += 1
            s["last_failure_time"] = now
            if s["failure_count"] >= self._failure_threshold:
                s["state"] = self.State.OPEN
            raise


__all__ = [
    "LoggingDecorator",
    "CachingDecorator",
    "MetricsDecorator",
    "RetryDecorator",
    "CircuitBreakerDecorator",
]
