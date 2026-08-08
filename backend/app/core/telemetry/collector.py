from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from backend.app.core.telemetry.models import (
    AnalysisEvent,
    ChatEvent,
    EventType,
    ParserEvent,
    ReasoningEvent,
)


class TelemetryCollector:
    def __init__(self, base_dir: str | None = None) -> None:
        if base_dir is None:
            base_dir = os.path.join(os.getcwd(), "telemetry")
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._files: dict[str, Any] = {}

    def _path(self, event_type: EventType | str) -> Path:
        name = event_type.value if isinstance(event_type, EventType) else str(event_type)
        return self.base_dir / f"{name}_metrics.jsonl"

    def _get_file(self, path: Path) -> Any:
        key = str(path)
        if key not in self._files or self._files[key].closed:
            self._files[key] = open(path, mode="a", encoding="utf-8")
        return self._files[key]

    def record(self, event: AnalysisEvent | ChatEvent | ParserEvent | ReasoningEvent) -> None:
        payload = _dataclass_to_dict(event)
        payload.setdefault("timestamp", datetime.utcnow().isoformat() + "Z")
        path = self._path(event.event_type)
        file_handle = self._get_file(path)
        file_handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
        file_handle.flush()

    def close(self) -> None:
        for file_handle in self._files.values():
            try:
                file_handle.close()
            except Exception:
                pass
        self._files.clear()


def _dataclass_to_dict(obj: Any) -> dict[str, Any]:
    if hasattr(obj, "__dict__"):
        data = {}
        for key, value in obj.__dict__.items():
            if hasattr(value, "__dataclass_fields__"):
                data[key] = _dataclass_to_dict(value)
            else:
                data[key] = value
        return data
    return {}
