"""
Async queue for prioritized background execution.

Provides a simple priority queue for async task execution.
"""

from __future__ import annotations

import logging
import queue
import threading
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)


class AsyncQueue:
    """Simple async task queue with priority."""

    def __init__(self) -> None:
        self._queue: queue.PriorityQueue = queue.PriorityQueue()
        self._thread: threading.Thread | None = None
        self._running = False

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)

    def enqueue(self, priority: int, task: Callable[..., Any]) -> None:
        self._queue.put((priority, task))

    def _worker(self) -> None:
        while self._running:
            try:
                priority, task = self._queue.get(timeout=1)
                task()
            except queue.Empty:
                continue
            except Exception as exc:
                logger.error("Async queue task failed: %s", exc)


async_queue = AsyncQueue()
