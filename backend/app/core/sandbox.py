import asyncio
import logging
import os
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class SandboxLanguage(str, Enum):
    PYTHON = "python"
    BASH = "bash"
    JAVASCRIPT = "javascript"
    DOCKER = "docker"


@dataclass
class SandboxExecution:
    id: str
    language: SandboxLanguage
    code: str
    result: str | None = None
    error: str | None = None
    exit_code: int = 0
    duration_ms: float = 0.0
    started_at: datetime = field(default_factory=datetime.utcnow)
    finished_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class SandboxRuntime:
    def __init__(self, base_path: str = "./workspace/sandbox"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._allowed_tools: list[str] = []
        self._max_execution_time = 30

    async def execute(self, language: SandboxLanguage, code: str, tools: list[str] | None = None) -> SandboxExecution:
        execution_id = f"sandbox-{datetime.now(timezone.utc).timestamp()}"
        execution = SandboxExecution(id=execution_id, language=language, code=code)
        start = datetime.now(timezone.utc)
        try:
            if language == SandboxLanguage.PYTHON:
                result, error = await self._execute_python(code, tools or [])
            elif language == SandboxLanguage.BASH:
                result, error = await self._execute_bash(code, tools or [])
            else:
                raise ValueError(f"Unsupported language: {language}")
            execution.result = result
            execution.error = error
            execution.exit_code = 0 if error is None else 1
        except Exception as e:
            execution.error = str(e)
            execution.exit_code = 1
        execution.finished_at = datetime.now(timezone.utc)
        execution.duration_ms = (execution.finished_at - start).total_seconds() * 1000
        logger.info(f"Sandbox execution {execution.id}: {execution.duration_ms:.2f}ms, exit={execution.exit_code}")
        return execution

    async def _execute_python(self, code: str, tools: list[str]) -> tuple[str, str | None]:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            f.flush()
            temp_path = f.name
        try:
            proc = await asyncio.create_subprocess_exec(
                'python', temp_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=self._max_execution_time)
            return stdout.decode('utf-8'), stderr.decode('utf-8') if stderr else None
        except TimeoutError:
            return "", f"Execution timeout after {self._max_execution_time}s"
        finally:
            os.unlink(temp_path)

    async def _execute_bash(self, code: str, tools: list[str]) -> tuple[str, str | None]:
        import shlex
        allowed = set(self._allowed_tools) if self._allowed_tools else None
        if allowed:
            for cmd_part in shlex.split(code)[:1]:
                if cmd_part not in allowed:
                    return "", f"Command not allowed: {cmd_part}"
        proc = await asyncio.create_subprocess_shell(
            code,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(self.base_path),
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=self._max_execution_time)
            return stdout.decode('utf-8'), stderr.decode('utf-8') if stderr else None
        except TimeoutError:
            proc.kill()
            return "", f"Execution timeout after {self._max_execution_time}s"

    def set_tools(self, tools: list[str]):
        self._allowed_tools = tools

    def set_max_execution_time(self, seconds: int):
        self._max_execution_time = seconds


sandbox_runtime = SandboxRuntime()

