"""
RFC-0003 Decorator SDK (Decorator Base, Chain Builder, Hot-Swap, Contract Validator).

This package provides the foundation for decorating Capability Pack BaseApp
instances with cross-cutting concerns: logging, caching, metrics, retry,
circuit breaking, and more — all through transparent proxying.

Usage::

    from backend.app.core.decorators import ChainBuilder, DecoratorRegistry

    builder = ChainBuilder()
    builder.add("logging").add("metrics").add("retry", {"max_retries": 3})
    decorated_app = builder.build(my_base_app)
"""

from __future__ import annotations

from backend.app.core.decorators.base import (
    AugmentationPoint,
    DecoratorBase,
    decorate,
    timing_decorator,
)
from backend.app.core.decorators.concrete import (
    CachingDecorator,
    CircuitBreakerDecorator,
    LoggingDecorator,
    MetricsDecorator,
    RetryDecorator,
)
from backend.app.core.decorators.sdk import (
    ChainBuilder,
    DecoratorContractValidator,
    DecoratorRegistry,
    HotSwapManager,
)
from backend.app.core.decorators.testing import (
    DecoratorIsolationTester,
    DecoratorTestHarness,
    MockBaseApp,
)

__version__ = "1.0.0"

__all__ = [
    "AugmentationPoint",
    "DecoratorBase",
    "decorate",
    "timing_decorator",
    "LoggingDecorator",
    "CachingDecorator",
    "MetricsDecorator",
    "RetryDecorator",
    "CircuitBreakerDecorator",
    "DecoratorRegistry",
    "ChainBuilder",
    "HotSwapManager",
    "DecoratorContractValidator",
    "MockBaseApp",
    "DecoratorTestHarness",
    "DecoratorIsolationTester",
]
