"""
Step executor for tool blueprints.

Executes individual steps in a tool blueprint,
including LLM calls, Python code, API calls, KB search, etc.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from backend.app.core.model_router import model_router
from backend.app.core.sandbox import SandboxLanguage, sandbox_runtime

logger = logging.getLogger(__name__)


class StepExecutionError(Exception):
    """Raised when a tool step fails to execute."""


class StepExecutor:
    """Execute a single tool step by type."""

    async def execute(
        self,
        step: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        step_type = step.get("type", "unknown")
        step_id = step.get("id", "unknown")
        config = step.get("config", {})

        logger.info("Executing step %s of type %s", step_id, step_type)

        try:
            if step_type == "llm_call":
                return await self._execute_llm_call(config, context)
            elif step_type == "python_code":
                return await self._execute_python_code(config, context)
            elif step_type == "api_call":
                return await self._execute_api_call(config, context)
            elif step_type == "kb_search":
                return await self._execute_kb_search(config, context)
            elif step_type == "web_scraper":
                return await self._execute_web_scraper(config, context)
            elif step_type == "conditional":
                return await self._execute_conditional(config, context)
            elif step_type == "delay":
                return await self._execute_delay(config, context)
            else:
                raise StepExecutionError(f"Unknown step type: {step_type}")
        except Exception as exc:
            logger.error("Step %s failed: %s", step_id, exc)
            return {
                "step_id": step_id,
                "type": step_type,
                "success": False,
                "error": str(exc),
            }

    async def _execute_llm_call(
        self,
        config: dict[str, Any],
        context: dict[str, Any] | None,
    ) -> dict[str, Any]:
        prompt = config.get("prompt", "")
        model = config.get("model")
        temperature = float(config.get("temperature", 0.7))
        max_tokens = int(config.get("max_tokens", 1024))
        messages = [{"role": "user", "content": prompt}]
        try:
            response = await model_router.acomplete(
                messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            result_text = response.choices[0].message.content if response else ""
        except Exception as exc:
            return {
                "step_id": config.get("step_id", "unknown"),
                "type": "llm_call",
                "success": False,
                "error": str(exc),
                "output": "",
            }
        return {
            "step_id": config.get("step_id", "unknown"),
            "type": "llm_call",
            "success": True,
            "result": result_text,
            "output": result_text,
        }

    async def _execute_python_code(
        self,
        config: dict[str, Any],
        context: dict[str, Any] | None,
    ) -> dict[str, Any]:
        code = config.get("code", "")
        execution = await sandbox_runtime.execute(SandboxLanguage.PYTHON, code)
        return {
            "step_id": config.get("step_id", "unknown"),
            "type": "python_code",
            "success": execution.exit_code == 0,
            "result": execution.result or "",
            "output": execution.result or "",
            "error": execution.error,
        }

    async def _execute_api_call(
        self,
        config: dict[str, Any],
        context: dict[str, Any] | None,
    ) -> dict[str, Any]:
        url = config.get("url", "")
        method = config.get("method", "GET").upper()
        headers = config.get("headers", {})
        body = config.get("body", {})
        params = config.get("params", {})
        if not url:
            raise StepExecutionError("API call requires a URL")
        async with httpx.AsyncClient(timeout=30.0) as client:
            request_fn = {
                "GET": client.get,
                "POST": client.post,
                "PUT": client.put,
                "DELETE": client.delete,
                "PATCH": client.patch,
            }.get(method, client.get)
            response = await request_fn(
                url,
                headers=headers,
                json=body if method != "GET" else None,
                params=params if method == "GET" else None,
            )
            response.raise_for_status()
            try:
                data = response.json()
            except Exception:
                data = response.text
            return {
                "step_id": config.get("step_id", "unknown"),
                "type": "api_call",
                "success": True,
                "result": data,
                "output": {"status": response.status_code, "data": data},
            }

    async def _execute_kb_search(
        self,
        config: dict[str, Any],
        context: dict[str, Any] | None,
    ) -> dict[str, Any]:
        from backend.app.core.memory_layer import memory_manager

        kb_id = config.get("kb_id", "")
        query = config.get("query", "")
        limit = int(config.get("limit", 10))
        try:
            results = await memory_manager.search("knowledge", query, limit=limit)
        except Exception as exc:
            return {
                "step_id": config.get("step_id", "unknown"),
                "type": "kb_search",
                "success": False,
                "error": str(exc),
                "output": {"matches": []},
            }
        return {
            "step_id": config.get("step_id", "unknown"),
            "type": "kb_search",
            "success": True,
            "result": f"KB search in {kb_id} executed",
            "output": {"matches": results},
        }

    async def _execute_web_scraper(
        self,
        config: dict[str, Any],
        context: dict[str, Any] | None,
    ) -> dict[str, Any]:
        url = config.get("url", "")
        if not url:
            raise StepExecutionError("Web scraper requires a URL")
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            text = response.text[:10000]
            return {
                "step_id": config.get("step_id", "unknown"),
                "type": "web_scraper",
                "success": True,
                "result": f"Web scraper for {url} executed",
                "output": {
                    "content": text,
                    "url": str(response.url),
                    "status": response.status_code,
                },
            }

    async def _execute_conditional(
        self,
        config: dict[str, Any],
        context: dict[str, Any] | None,
    ) -> dict[str, Any]:
        condition = config.get("condition", "true")
        branch = "true" if condition else "false"
        return {
            "step_id": config.get("step_id", "unknown"),
            "type": "conditional",
            "success": True,
            "result": "Conditional evaluated",
            "output": {"branch": branch, "condition": condition},
        }

    async def _execute_delay(
        self,
        config: dict[str, Any],
        context: dict[str, Any] | None,
    ) -> dict[str, Any]:
        import asyncio

        delay_seconds = float(config.get("delay_seconds", 0))
        if delay_seconds > 0:
            await asyncio.sleep(delay_seconds)
        return {
            "step_id": config.get("step_id", "unknown"),
            "type": "delay",
            "success": True,
            "result": f"Delayed {delay_seconds}s",
            "output": {},
        }


step_executor = StepExecutor()
