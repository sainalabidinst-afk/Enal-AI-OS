"""
Capability Lifecycle Manager
=============================

Manages the full lifecycle of capability packs:
- load / unload
- suspend / resume
- upgrade
- health monitoring
- metrics collection
- version tracking
- dependency checking
- compatibility validation

Designed as a Core Platform service so all capability packs
are managed through a single, consistent interface.
"""

from __future__ import annotations

import logging
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class CapabilityState(str, Enum):
    LOADED = "loaded"
    UNLOADED = "unloaded"
    SUSPENDED = "suspended"
    UPGRADING = "upgrading"
    ERROR = "error"


class CapabilityHealth(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class CapabilityVersion:
    capability_id: str
    major: int
    minor: int
    patch: int
    build: str = ""
    contract_version: str = "1"

    def __str__(self) -> str:
        base = f"{self.major}.{self.minor}.{self.patch}"
        return f"{base}-{self.build}" if self.build else base


@dataclass
class CapabilityMetrics:
    capability_id: str
    execution_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    total_latency_ms: float = 0.0
    last_executed_at: float | None = None
    last_success_at: float | None = None
    last_failure_at: float | None = None
    last_error: str | None = None

    @property
    def success_rate(self) -> float:
        if self.execution_count == 0:
            return 0.0
        return self.success_count / self.execution_count

    @property
    def avg_latency_ms(self) -> float:
        if self.execution_count == 0:
            return 0.0
        return self.total_latency_ms / self.execution_count


@dataclass
class CapabilityRecord:
    capability_id: str
    name: str
    category: str
    version: CapabilityVersion
    state: CapabilityState = CapabilityState.UNLOADED
    health: CapabilityHealth = CapabilityHealth.UNKNOWN
    dependencies: list[str] = field(default_factory=list)
    dependents: list[str] = field(default_factory=list)
    metrics: CapabilityMetrics = field(default_factory=lambda: CapabilityMetrics(capability_id=""))
    metadata: dict[str, Any] = field(default_factory=dict)
    loaded_at: float | None = None
    updated_at: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        self.metrics.capability_id = self.capability_id


class CapabilityLifecycleManager:
    """Core service for capability lifecycle management."""

    def __init__(self) -> None:
        self._records: dict[str, CapabilityRecord] = {}
        self._handlers: dict[CapabilityState, list[Any]] = {
            state: [] for state in CapabilityState
        }
        self._register_defaults()

    def _register_defaults(self) -> None:
        from apps import APPS, get_app

        for app_id, app in APPS.items():
            if app is None:
                continue
            version = _parse_version(getattr(app, "version", "1.0.0"))
            record = CapabilityRecord(
                capability_id=app_id,
                name=getattr(app, "name", app_id),
                category=getattr(app, "category", "general"),
                version=version,
                state=CapabilityState.LOADED,
                health=CapabilityHealth.HEALTHY,
            )
            self._records[app_id] = record

    def register(self, record: CapabilityRecord) -> None:
        self._records[record.capability_id] = record
        logger.info("Registered capability: %s", record.capability_id)

    def get(self, capability_id: str) -> CapabilityRecord | None:
        return self._records.get(capability_id)

    def list_records(self) -> list[CapabilityRecord]:
        return list(self._records.values())

    async def load(self, capability_id: str) -> CapabilityRecord:
        record = self._records.get(capability_id)
        if record is None:
            raise ValueError(f"Capability '{capability_id}' is not registered")

        missing = [dep for dep in record.dependencies if self._records.get(dep, CapabilityRecord(capability_id=dep)).state != CapabilityState.LOADED]
        if missing:
            raise ValueError(f"Cannot load '{capability_id}': missing dependencies {missing}")

        record.state = CapabilityState.LOADED
        record.loaded_at = time.time()
        record.updated_at = record.loaded_at
        record.health = CapabilityHealth.HEALTHY
        await self._emit("loaded", record)
        return record

    async def unload(self, capability_id: str) -> CapabilityRecord:
        record = self._records.get(capability_id)
        if record is None:
            raise ValueError(f"Capability '{capability_id}' is not registered")

        dependents = [dep for dep in record.dependents if self._records[dep].state == CapabilityState.LOADED]
        if dependents:
            raise ValueError(f"Cannot unload '{capability_id}': dependents still loaded {dependents}")

        record.state = CapabilityState.UNLOADED
        record.loaded_at = None
        record.updated_at = time.time()
        record.health = CapabilityHealth.UNKNOWN
        await self._emit("unloaded", record)
        return record

    async def suspend(self, capability_id: str) -> CapabilityRecord:
        record = self._records.get(capability_id)
        if record is None:
            raise ValueError(f"Capability '{capability_id}' is not registered")
        if record.state != CapabilityState.LOADED:
            raise ValueError(f"Cannot suspend '{capability_id}': not loaded")

        record.state = CapabilityState.SUSPENDED
        record.updated_at = time.time()
        await self._emit("suspended", record)
        return record

    async def resume(self, capability_id: str) -> CapabilityRecord:
        record = self._records.get(capability_id)
        if record is None:
            raise ValueError(f"Capability '{capability_id}' is not registered")
        if record.state != CapabilityState.SUSPENDED:
            raise ValueError(f"Cannot resume '{capability_id}': not suspended")

        record.state = CapabilityState.LOADED
        record.updated_at = time.time()
        await self._emit("resumed", record)
        return record

    async def upgrade(self, capability_id: str, new_version: CapabilityVersion) -> CapabilityRecord:
        record = self._records.get(capability_id)
        if record is None:
            raise ValueError(f"Capability '{capability_id}' is not registered")
        if record.state == CapabilityState.UPGRADING:
            raise ValueError(f"Capability '{capability_id}' is already upgrading")

        record.state = CapabilityState.UPGRADING
        record.updated_at = time.time()
        await self._emit("upgrading", record)

        record.version = new_version
        record.state = CapabilityState.LOADED
        record.loaded_at = time.time()
        record.updated_at = record.loaded_at
        await self._emit("upgraded", record)
        return record

    def check_dependencies(self, capability_id: str) -> tuple[bool, list[str]]:
        record = self._records.get(capability_id)
        if record is None:
            return False, [f"Capability '{capability_id}' is not registered"]

        missing = []
        for dep in record.dependencies:
            dep_record = self._records.get(dep)
            if dep_record is None:
                missing.append(f"missing dependency '{dep}'")
            elif dep_record.state != CapabilityState.LOADED:
                missing.append(f"dependency '{dep}' is {dep_record.state.value}")
        return len(missing) == 0, missing

    def check_compatibility(self, capability_id: str, required_contract: str) -> tuple[bool, str]:
        record = self._records.get(capability_id)
        if record is None:
            return False, f"Capability '{capability_id}' is not registered"
        if record.version.contract_version == required_contract:
            return True, "Compatible"
        return False, f"Contract mismatch: {record.version.contract_version} != {required_contract}"

    def record_execution(self, capability_id: str, success: bool, latency_ms: float, error: str | None = None) -> None:
        record = self._records.get(capability_id)
        if record is None:
            return

        metrics = record.metrics
        metrics.execution_count += 1
        metrics.total_latency_ms += latency_ms
        now = time.time()

        if success:
            metrics.success_count += 1
            metrics.last_success_at = now
        else:
            metrics.failure_count += 1
            metrics.last_failure_at = now
            metrics.last_error = error

        metrics.last_executed_at = now
        record.updated_at = now

        if metrics.failure_count > 0 and metrics.success_rate < 0.5:
            record.health = CapabilityHealth.UNHEALTHY
        elif metrics.failure_count > 0 and metrics.success_rate < 0.85:
            record.health = CapabilityHealth.DEGRADED
        else:
            record.health = CapabilityHealth.HEALTHY

    def on(self, state: CapabilityState, handler: Any) -> None:
        self._handlers[state].append(handler)

    async def _emit(self, event: str, record: CapabilityRecord) -> None:
        handlers = self._handlers.get(CapabilityState(record.state), [])
        for handler in handlers:
            try:
                if hasattr(handler, "__call__"):
                    await handler(event, record)
            except Exception as exc:
                logger.debug("Lifecycle handler failed for %s: %s", record.capability_id, exc)


def _parse_version(version_str: str) -> CapabilityVersion:
    parts = version_str.split(".")
    major = int(parts[0]) if len(parts) > 0 else 1
    minor = int(parts[1]) if len(parts) > 1 else 0
    patch = int(parts[2].split("-")[0]) if len(parts) > 2 else 0
    build = parts[2].split("-")[1] if len(parts) > 2 and "-" in parts[2] else ""
    return CapabilityVersion(
        capability_id="",
        major=major,
        minor=minor,
        patch=patch,
        build=build,
    )


capability_lifecycle_manager = CapabilityLifecycleManager()
