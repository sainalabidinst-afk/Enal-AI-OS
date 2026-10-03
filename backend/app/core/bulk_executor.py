"""
Bulk executor for running multiple tasks concurrently.

Executes batches of agent/tool runs with configurable concurrency.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)


class BulkExecutor:
    """Execute bulk runs with concurrency control."""

    def __init__(self, max_concurrency: int = 10) -> None:
        self.max_concurrency = max_concurrency
        self._semaphore = asyncio.Semaphore(max_concurrency)

    async def run_batch(
        self,
        tasks: list[dict[str, Any]],
        executor: Any,
    ) -> list[dict[str, Any]]:
        async def run_task(task: dict[str, Any]) -> dict[str, Any]:
            async with self._semaphore:
                try:
                    result = await executor(task)
                    return {"task": task, "success": True, "result": result}
                except Exception as exc:
                    logger.error("Bulk task failed: %s", exc)
                    return {"task": task, "success": False, "error": str(exc)}

        results = await asyncio.gather(*[run_task(task) for task in tasks])
        return list(results)


bulk_executor = BulkExecutor()
