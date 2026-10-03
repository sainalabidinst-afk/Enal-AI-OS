"""
Decorator SDK — Core foundation for capability pack decoration (RFC-0003).

Provides:
- DecoratorBase: transparent proxy over BaseApp
- AugmentationPoint: before/after/around/on_error hooks
- CapabilityWrapper: wraps a BaseApp instance with decorator layers
"""

from __future__ import annotations

import functools
import logging
import time
from collections.abc import Callable
from typing import Any, TypeVar, cast

from backend.app.core.base_app import BaseApp

logger = logging.getLogger(__name__)

T = TypeVar("T")


class AugmentationPoint:
    """Defines hook points for decorator augmentation."""

    BEFORE = "before"
    AFTER = "after"
    AROUND = "around"
    ON_ERROR = "on_error"


class DecoratorBase(BaseApp):
    """Base class for all decorators, providing transparent BaseApp proxying.

    Subclasses override the hook methods (_before, _after, _around, _on_error)
    to inject behavior. The wrapped app's methods are proxied transparently.
    """

    def __init__(
        self, wrapped: BaseApp | None = None, config: dict[str, Any] | None = None
    ) -> None:
        super().__init__(config)
        self._wrapped: BaseApp | None = wrapped
        self._hooks: dict[str, list[Callable[..., Any]]] = {
            AugmentationPoint.BEFORE: [],
            AugmentationPoint.AFTER: [],
            AugmentationPoint.AROUND: [],
            AugmentationPoint.ON_ERROR: [],
        }

    name: str = "decorator_base"
    version: str = "1.0.0"

    def _before(self, method_name: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> None:
        """Hook called before the wrapped method executes."""

    def _after(
        self,
        method_name: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        result: Any,
    ) -> Any:
        """Hook called after the wrapped method executes. Can modify result."""
        return result

    def _on_error(
        self,
        method_name: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        exc: Exception,
    ) -> Any:
        """Hook called when the wrapped method raises. Can suppress or re-raise."""
        raise exc

    def _around(
        self,
        method_name: str,
        func: Callable[..., Any],
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        """Hook that wraps the call to the wrapped method."""
        return func(*args, **kwargs)

    def _invoke(self, method_name: str, *args: Any, **kwargs: Any) -> Any:
        """Proxy method that invokes wrapped app's method with hooks."""
        self._before(method_name, args, kwargs)
        try:
            func: Callable[..., Any] | None = getattr(self._wrapped, method_name, None)
            if func is None:
                raise AttributeError(f"Method '{method_name}' not found on wrapped app")
            result = self._around(method_name, func, args, kwargs)
            return self._after(method_name, args, kwargs, result)
        except Exception as exc:
            return self._on_error(method_name, args, kwargs, exc)

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """Proxy execute to wrapped app with augmentation."""
        if self._wrapped is not None:
            return self._invoke("execute", task)
        return super().execute(task)  # type: ignore[safe-super]

    def validate_input(self, task: dict[str, Any]) -> bool:
        """Proxy validate_input to wrapped app."""
        if self._wrapped is not None:
            return cast(bool, self._invoke("validate_input", task))
        return super().validate_input(task)  # type: ignore[safe-super]

    def get_capabilities(self) -> list[dict[str, Any]]:
        """Proxy get_capabilities to wrapped app."""
        if self._wrapped is not None:
            return cast(list[dict[str, Any]], self._invoke("get_capabilities"))
        return []

    def register_event_handlers(self) -> None:
        """Proxy register_event_handlers to wrapped app."""
        if self._wrapped is not None:
            self._invoke("register_event_handlers")

    def shutdown(self) -> None:
        """Proxy shutdown to wrapped app."""
        if self._wrapped is not None:
            self._invoke("shutdown")


def decorate(cls: type[T]) -> type[T]:
    """Class decorator that adds proxy support to a BaseApp subclass."""
    original_init = cls.__init__

    @functools.wraps(original_init)
    def new_init(self: T, wrapped: BaseApp | None = None, **kwargs: Any) -> None:
        original_init(self, **kwargs)
        if isinstance(self, DecoratorBase):
            self._wrapped = wrapped

    cls.__init__ = new_init  # type: ignore[method-assign,assignment]
    return cls


def timing_decorator(func: Callable[..., T]) -> Callable[..., T]:
    """Function-level decorator for measuring execution time."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            logger.debug("Timing for %s: %.3fms", func.__name__, elapsed * 1000)

    return cast(Callable[..., T], wrapper)


__all__ = [
    "AugmentationPoint",
    "DecoratorBase",
    "decorate",
    "timing_decorator",
]
