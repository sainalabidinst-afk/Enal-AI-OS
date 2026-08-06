import logging
import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from backend.app.core.auth import require_permission
from apps.organization.capability_lifecycle import (
    CapabilityLifecycleManager,
    CapabilityRecord,
    CapabilityState,
    CapabilityHealth,
    capability_lifecycle_manager,
)

router = APIRouter()
logger = logging.getLogger(__name__)


def _serialize(record: CapabilityRecord) -> dict[str, Any]:
    return {
        "id": record.capability_id,
        "name": record.name,
        "category": record.category,
        "state": record.state.value,
        "health": record.health.value,
        "version": {
            "major": record.version.major,
            "minor": record.version.minor,
            "patch": record.version.patch,
            "build": record.version.build,
            "contract_version": record.version.contract_version,
            "display": str(record.version),
        },
        "dependencies": record.dependencies,
        "dependents": record.dependents,
        "metrics": {
            "execution_count": record.metrics.execution_count,
            "success_count": record.metrics.success_count,
            "failure_count": record.metrics.failure_count,
            "success_rate": round(record.metrics.success_rate, 4),
            "avg_latency_ms": round(record.metrics.avg_latency_ms, 2),
            "last_executed_at": record.metrics.last_executed_at,
            "last_success_at": record.metrics.last_success_at,
            "last_failure_at": record.metrics.last_failure_at,
            "last_error": record.metrics.last_error,
        },
        "loaded_at": record.loaded_at,
        "updated_at": record.updated_at,
        "metadata": record.metadata,
    }


@router.get("/capabilities/lifecycle")
async def list_capability_lifecycle():
    records = capability_lifecycle_manager.list_records()
    return {
        "capabilities": [_serialize(r) for r in records],
        "summary": {
            "total": len(records),
            "loaded": sum(1 for r in records if r.state == CapabilityState.LOADED),
            "unloaded": sum(1 for r in records if r.state == CapabilityState.UNLOADED),
            "suspended": sum(1 for r in records if r.state == CapabilityState.SUSPENDED),
            "upgrading": sum(1 for r in records if r.state == CapabilityState.UPGRADING),
            "error": sum(1 for r in records if r.state == CapabilityState.ERROR),
            "healthy": sum(1 for r in records if r.health == CapabilityHealth.HEALTHY),
            "degraded": sum(1 for r in records if r.health == CapabilityHealth.DEGRADED),
            "unhealthy": sum(1 for r in records if r.health == CapabilityHealth.UNHEALTHY),
        },
    }


@router.get("/capabilities/{capability_id}/lifecycle")
async def get_capability_lifecycle(capability_id: str):
    record = capability_lifecycle_manager.get(capability_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Capability '{capability_id}' not found")
    return _serialize(record)


@router.post("/capabilities/{capability_id}/load", dependencies=[Depends(require_permission("admin"))])
async def load_capability(capability_id: str):
    try:
        record = await capability_lifecycle_manager.load(capability_id)
        return _serialize(record)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/capabilities/{capability_id}/unload", dependencies=[Depends(require_permission("admin"))])
async def unload_capability(capability_id: str):
    try:
        record = await capability_lifecycle_manager.unload(capability_id)
        return _serialize(record)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/capabilities/{capability_id}/suspend", dependencies=[Depends(require_permission("admin"))])
async def suspend_capability(capability_id: str):
    try:
        record = await capability_lifecycle_manager.suspend(capability_id)
        return _serialize(record)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/capabilities/{capability_id}/resume", dependencies=[Depends(require_permission("admin"))])
async def resume_capability(capability_id: str):
    try:
        record = await capability_lifecycle_manager.resume(capability_id)
        return _serialize(record)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/capabilities/{capability_id}/upgrade", dependencies=[Depends(require_permission("admin"))])
async def upgrade_capability(capability_id: str, version: dict[str, Any]):
    try:
        new_version = CapabilityVersion(
            capability_id=capability_id,
            major=version.get("major", 1),
            minor=version.get("minor", 0),
            patch=version.get("patch", 0),
            build=version.get("build", ""),
            contract_version=version.get("contract_version", "1"),
        )
        record = await capability_lifecycle_manager.upgrade(capability_id, new_version)
        return _serialize(record)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/capabilities/{capability_id}/dependencies")
async def get_capability_dependencies(capability_id: str):
    record = capability_lifecycle_manager.get(capability_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Capability '{capability_id}' not found")

    ok, missing = capability_lifecycle_manager.check_dependencies(capability_id)
    return {
        "capability_id": capability_id,
        "dependencies": record.dependencies,
        "dependents": record.dependents,
        "satisfied": ok,
        "missing": missing,
    }


@router.get("/capabilities/{capability_id}/compatibility")
async def check_capability_compatibility(capability_id: str, contract_version: str = "1"):
    ok, message = capability_lifecycle_manager.check_compatibility(capability_id, contract_version)
    return {
        "capability_id": capability_id,
        "required_contract": contract_version,
        "compatible": ok,
        "message": message,
    }
