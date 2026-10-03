"""
Decorator Registry, Chain Builder, Hot-Swap Manager, and Contract Validator.

Completes the RFC-0003 Decorator SDK with:
- Registry: catalogs available decorators
- ChainBuilder: composes multiple decorators declaratively
- HotSwapManager: zero-downtime decorator replacement
- DecoratorContractValidator: validates decorator BaseApp compliance
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Any, TypeVar

from backend.app.core.base_app import BaseApp
from backend.app.core.decorators.base import DecoratorBase
from backend.app.core.decorators.concrete import (
    CachingDecorator,
    CircuitBreakerDecorator,
    LoggingDecorator,
    MetricsDecorator,
    RetryDecorator,
)

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseApp)


class DecoratorRegistry:
    """Catalogs available decorators."""

    _decorators: dict[str, type[DecoratorBase]] = {
        "logging": LoggingDecorator,
        "caching": CachingDecorator,
        "metrics": MetricsDecorator,
        "retry": RetryDecorator,
        "circuit_breaker": CircuitBreakerDecorator,
    }
    _lock: threading.RLock = threading.RLock()

    @classmethod
    def register(cls, name: str, decorator_cls: type[DecoratorBase]) -> None:
        """Register a new decorator type."""
        with cls._lock:
            cls._decorators[name] = decorator_cls
            logger.info("Registered decorator: %s", name)

    @classmethod
    def unregister(cls, name: str) -> None:
        """Unregister a decorator type."""
        with cls._lock:
            cls._decorators.pop(name, None)

    @classmethod
    def get(cls, name: str) -> type[DecoratorBase] | None:
        """Retrieve a decorator class by name."""
        with cls._lock:
            return cls._decorators.get(name)

    @classmethod
    def list_available(cls) -> list[str]:
        """List all registered decorator names."""
        with cls._lock:
            return list(cls._decorators.keys())

    @classmethod
    def create_decorator(
        cls,
        name: str,
        wrapped: BaseApp | None = None,
        config: dict[str, Any] | None = None,
    ) -> DecoratorBase | None:
        """Create an instance of a registered decorator."""
        decorator_cls = cls.get(name)
        if decorator_cls is None:
            return None
        return decorator_cls(wrapped=wrapped, config=config or {})

    @classmethod
    def clear(cls) -> None:
        """Clear all registered decorators."""
        with cls._lock:
            cls._decorators.clear()


class ChainBuilder:
    """Composes multiple decorators declaratively around a BaseApp."""

    def __init__(self) -> None:
        self._decorator_specs: list[tuple[str, dict[str, Any]]] = []

    def add(self, decorator_name: str, config: dict[str, Any] | None = None) -> ChainBuilder:
        """Add a decorator to the chain."""
        self._decorator_specs.append((decorator_name, config or {}))
        return self

    def add_decorator(
        self, decorator_cls: type[DecoratorBase], config: dict[str, Any] | None = None
    ) -> ChainBuilder:
        """Add a decorator class directly to the chain."""
        name = decorator_cls.__name__.lower().replace("decorator", "")
        DecoratorRegistry.register(name, decorator_cls)
        self._decorator_specs.append((name, config or {}))
        return self

    def build(self, app: T) -> DecoratorBase:
        """Build the decorator chain around the given app.

        Decorators are applied in order: the first decorator added wraps
        the app directly, subsequent decorators wrap the previous result.
        """
        wrapped: BaseApp = app
        for name, config in self._decorator_specs:
            decorator = DecoratorRegistry.create_decorator(name, wrapped=wrapped, config=config)
            if decorator is None:
                raise ValueError(f"Unknown decorator: {name}")
            wrapped = decorator
        if isinstance(wrapped, DecoratorBase):
            return wrapped
        raise RuntimeError("ChainBuilder did not produce a DecoratorBase instance")

    def clear(self) -> ChainBuilder:
        """Clear the decorator chain."""
        self._decorator_specs = []
        return self

    @property
    def decorator_count(self) -> int:
        """Return the number of decorators in the chain."""
        return len(self._decorator_specs)


class HotSwapManager:
    """Manages zero-downtime decorator replacement."""

    def __init__(self) -> None:
        self._active: dict[str, DecoratorBase] = {}
        self._lock: threading.RLock = threading.RLock()

    def swap(
        self,
        app_id: str,
        app: BaseApp,
        chain_specs: list[tuple[str, dict[str, Any]]],
        new_decorator: tuple[str, dict[str, Any]],
    ) -> DecoratorBase:
        """Replace one decorator in the chain with another.

        Args:
            app_id: Identifier for the app being managed.
            app: Original BaseApp instance.
            chain_specs: Current decorator chain specification.
            new_decorator: (name, config) of the new decorator to swap in.

        Returns:
            New DecoratorBase with the swapped chain.
        """
        with self._lock:
            start = time.perf_counter()
            new_specs = list(chain_specs)
            new_specs.append(new_decorator)
            builder = ChainBuilder()
            for spec_name, spec_config in new_specs:
                builder.add(spec_name, spec_config)
            new_chain = builder.build(app)
            latency_ms = (time.perf_counter() - start) * 1000
            self._active[app_id] = new_chain
            logger.info(
                "Hot-swapped decorator for %s in %.3fms (chain: %d decorators)",
                app_id,
                latency_ms,
                len(new_specs),
            )
            return new_chain

    def get_active(self, app_id: str) -> DecoratorBase | None:
        """Get the currently active decorator chain for an app."""
        with self._lock:
            return self._active.get(app_id)

    def remove(self, app_id: str) -> bool:
        """Remove an app from hot-swap management."""
        with self._lock:
            return self._active.pop(app_id, None) is not None

    @property
    def swap_count(self) -> int:
        """Return the number of active hot-swap registrations."""
        return len(self._active)


class DecoratorContractValidator:
    """Validates that decorators comply with the BaseApp contract."""

    REQUIRED_METHODS = ["get_capabilities", "execute", "validate_input"]

    def validate(self, decorator: DecoratorBase) -> dict[str, Any]:
        """Validate a decorator against the BaseApp contract.

        Returns a dict with validation results.
        """
        results: dict[str, Any] = {
            "class": type(decorator).__name__,
            "is_baseapp": isinstance(decorator, BaseApp),
            "methods_present": {},
            "has_wrapped": hasattr(decorator, "_wrapped"),
            "contract_compliant": True,
            "issues": [],
        }

        for method in self.REQUIRED_METHODS:
            has = hasattr(decorator, method) and callable(getattr(decorator, method))
            results["methods_present"][method] = has
            if not has:
                results["contract_compliant"] = False
                results["issues"].append(f"Missing required method: {method}")

        if results["has_wrapped"] and decorator._wrapped is None:
            results["issues"].append("Decorator has _wrapped but it is None")
            results["contract_compliant"] = False

        return results

    def validate_chain(self, decorator: DecoratorBase) -> list[dict[str, Any]]:
        """Validate a decorator chain. Returns list of per-layer results."""
        results: list[dict[str, Any]] = []
        current: DecoratorBase | None = decorator
        while current is not None:
            results.append(self.validate(current))
            current = getattr(current, "_wrapped", None) if hasattr(current, "_wrapped") else None
            if current is not None and not isinstance(current, DecoratorBase):
                break
        return results


__all__ = [
    "DecoratorRegistry",
    "ChainBuilder",
    "HotSwapManager",
    "DecoratorContractValidator",
]
