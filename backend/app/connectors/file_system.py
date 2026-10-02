"""
File System Action Connector
============================

Provides file system operations for Jenny: read, write, list, search, delete.
Uses safe_path validation to prevent path traversal (ADR-024).
"""

from __future__ import annotations

import json
import logging
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from backend.app.connectors.base_action import (
    ActionConnectorError,
    ActionType,
    ActionResult,
    BaseActionConnector,
    safe_path,
)

logger = logging.getLogger(__name__)


class FileSystemConnector(BaseActionConnector):
    """File system connector for read/write/search/delete operations.

    All file operations are sandboxed to a configurable base directory.
    """

    DEFAULT_BASE_PATH = "."

    def __init__(
        self,
        base_path: str | None = None,
        connector_type: ActionType = ActionType.FILE_SYSTEM,
    ) -> None:
        super().__init__(connector_type=connector_type)
        self._base_path = base_path or os.environ.get("JENNY_FILESYSTEM_BASE", ".")
        self._connected = True

    async def connect(self) -> None:
        self._connected = True
        logger.info("FileSystemConnector connected, base_path=%s", self._base_path)

    async def disconnect(self) -> None:
        self._connected = False

    async def list_actions(self) -> list[str]:
        return [
            "read_file",
            "write_file",
            "list_directory",
            "search_files",
            "delete_file",
            "file_info",
        ]

    async def execute(self, action: str, params: dict[str, Any]) -> ActionResult:
        action_map = {
            "read_file": self._read_file,
            "write_file": self._write_file,
            "list_directory": self._list_directory,
            "search_files": self._search_files,
            "delete_file": self._delete_file,
            "file_info": self._file_info,
        }

        handler = action_map.get(action)
        if not handler:
            raise ActionConnectorError(f"Unknown action: {action}")

        try:
            data = await handler(params)
            return ActionResult(
                success=True,
                data=data,
                action=action,
                connector=self.connector_type.value,
            )
        except FileNotFoundError as e:
            return ActionResult(
                success=False,
                error=str(e),
                action=action,
                connector=self.connector_type.value,
            )
        except Exception as e:
            logger.error("FileSystem action '%s' failed: %s", action, e)
            return ActionResult(
                success=False,
                error=str(e),
                action=action,
                connector=self.connector_type.value,
            )

    async def _read_file(self, params: dict[str, Any]) -> dict[str, Any]:
        relative_path = params.get("path", "")
        target = safe_path(self._base_path, relative_path)
        content = target.read_text(encoding="utf-8")
        stat = target.stat()
        return {
            "path": str(target),
            "content": content,
            "size_bytes": stat.st_size,
            "modified_at": datetime.fromtimestamp(stat.st_mtime, UTC).isoformat(),
        }

    async def _write_file(self, params: dict[str, Any]) -> dict[str, Any]:
        relative_path = params.get("path", "")
        content = params.get("content", "")
        if not content and not isinstance(content, str):
            raise ActionConnectorError("content parameter is required for write_file")
        target = safe_path(self._base_path, relative_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        stat = target.stat()
        return {
            "path": str(target),
            "size_bytes": stat.st_size,
            "written": True,
        }

    async def _list_directory(self, params: dict[str, Any]) -> dict[str, Any]:
        relative_path = params.get("path", "")
        target = safe_path(self._base_path, relative_path)
        if not target.is_dir():
            raise ActionConnectorError(f"Not a directory: {relative_path}")

        entries = []
        for entry in sorted(target.iterdir()):
            entries.append({
                "name": entry.name,
                "type": "directory" if entry.is_dir() else "file",
                "size_bytes": entry.stat().st_size if entry.is_file() else 0,
            })
        return {"path": str(target), "entries": entries}

    async def _search_files(self, params: dict[str, Any]) -> dict[str, Any]:
        pattern = params.get("pattern", "*.md")
        relative_path = params.get("path", "")
        target = safe_path(self._base_path, relative_path)
        max_results = int(params.get("max_results", 100))

        results = []
        for match in sorted(target.rglob(pattern)):
            if len(results) >= max_results:
                break
            stat = match.stat()
            results.append({
                "path": str(match.relative_to(target)),
                "size_bytes": stat.st_size,
                "modified_at": datetime.fromtimestamp(stat.st_mtime, UTC).isoformat(),
            })
        return {"query": pattern, "base_path": str(target), "results": results, "count": len(results)}

    async def _delete_file(self, params: dict[str, Any]) -> dict[str, Any]:
        relative_path = params.get("path", "")
        target = safe_path(self._base_path, relative_path)
        if not target.exists():
            raise FileNotFoundError(f"File not found: {relative_path}")
        if target.is_file():
            target.unlink()
        elif target.is_dir():
            import shutil

            shutil.rmtree(target)
        return {"path": str(target), "deleted": True}

    async def _file_info(self, params: dict[str, Any]) -> dict[str, Any]:
        relative_path = params.get("path", "")
        target = safe_path(self._base_path, relative_path)
        stat = target.stat()
        return {
            "path": str(target),
            "size_bytes": stat.st_size,
            "is_file": target.is_file(),
            "is_dir": target.is_dir(),
            "created_at": datetime.fromtimestamp(stat.st_ctime, UTC).isoformat(),
            "modified_at": datetime.fromtimestamp(stat.st_mtime, UTC).isoformat(),
            "accessed_at": datetime.fromtimestamp(stat.st_atime, UTC).isoformat(),
        }
