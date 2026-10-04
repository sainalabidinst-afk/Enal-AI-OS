"""
Governance API
==============

Endpoints for Pilar 4 governance (RFC-0055):
- POST /governance/packs — register new capability pack
- GET /governance/packs — list registered packs
- GET /governance/packs/{pack_id} — get pack details
- POST /governance/packs/{pack_id}/sandbox — create sandbox for pack
- POST /governance/packs/{pack_id}/evaluate — evaluate quality gate for pack
- GET /governance/audit — get audit trail
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from backend.app.core.governance import (
    PackRecord,
    PackStatus,
    QualityGate,
    governance_engine,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/packs")
async def register_pack(payload: dict[str, Any]) -> dict[str, Any]:
    """Register a new capability pack in the governance system."""
    pack_id = payload.get("pack_id") or f"pack-{uuid.uuid4().hex[:8]}"
    name = payload.get("name", "")
    domain = payload.get("domain", "")
    status = payload.get("status", PackStatus.DRAFT.value)
    metadata = payload.get("metadata", {})

    if not name or not domain:
        raise HTTPException(status_code=400, detail="name and domain are required")

    try:
        pack_status = PackStatus(status)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid status: {status}. Use: draft, testing, approved, "
                "rejected, registered, deprecated"
            ),
        )

    pack = PackRecord(
        pack_id=pack_id,
        name=name,
        domain=domain,
        status=pack_status,
        metadata=metadata,
    )
    record = governance_engine.register_pack(pack)
    return {
        "pack_id": record.pack_id,
        "name": record.name,
        "domain": record.domain,
        "status": record.status.value,
        "created_at": record.created_at.isoformat(),
    }


@router.get("/packs")
async def list_packs(status: str | None = None) -> dict[str, Any]:
    """List all registered packs, optionally filtered by status."""
    pack_status = None
    if status:
        try:
            pack_status = PackStatus(status)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    packs = governance_engine.list_packs(status=pack_status)
    return {
        "packs": [
            {
                "pack_id": p.pack_id,
                "name": p.name,
                "domain": p.domain,
                "status": p.status.value,
                "benchmark_score": p.benchmark_score,
                "coverage": p.coverage,
                "tests_passed": p.tests_passed,
                "tests_total": p.tests_total,
                "updated_at": p.updated_at.isoformat(),
            }
            for p in packs
        ]
    }


@router.get("/packs/{pack_id}")
async def get_pack(pack_id: str) -> dict[str, Any]:
    """Get details for a specific pack."""
    pack = governance_engine.get_pack(pack_id)
    if pack is None:
        raise HTTPException(status_code=404, detail=f"Pack '{pack_id}' not found")
    return {
        "pack_id": pack.pack_id,
        "name": pack.name,
        "domain": pack.domain,
        "status": pack.status.value,
        "benchmark_score": pack.benchmark_score,
        "coverage": pack.coverage,
        "tests_passed": pack.tests_passed,
        "tests_total": pack.tests_total,
        "metadata": pack.metadata,
        "created_at": pack.created_at.isoformat(),
        "updated_at": pack.updated_at.isoformat(),
    }


@router.post("/packs/{pack_id}/sandbox")
async def create_sandbox(pack_id: str) -> dict[str, Any]:
    """Create an isolated sandbox for a pack."""
    pack = governance_engine.get_pack(pack_id)
    if pack is None:
        raise HTTPException(status_code=404, detail=f"Pack '{pack_id}' not found")
    sandbox = governance_engine.create_sandbox(pack_id)
    return {
        "sandbox_id": sandbox.sandbox_id,
        "pack_id": pack_id,
        "isolated": sandbox.isolated,
        "environment": sandbox.environment,
        "allowed_operations": sandbox.allowed_operations,
        "blocked_operations": sandbox.blocked_operations,
    }


@router.post("/packs/{pack_id}/evaluate")
async def evaluate_pack(pack_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """Evaluate quality gate for a pack."""
    pack = governance_engine.get_pack(pack_id)
    if pack is None:
        raise HTTPException(status_code=404, detail=f"Pack '{pack_id}' not found")
    payload = payload or {}
    gate = QualityGate(
        gate_id=f"gate-{pack_id}",
        pack_id=pack_id,
        min_benchmark_score=float(payload.get("min_benchmark_score", 0.8)),
        min_coverage=float(payload.get("min_coverage", 0.8)),
        min_test_pass_rate=float(payload.get("min_test_pass_rate", 0.95)),
    )
    result = governance_engine.evaluate_gate(gate)
    return result


@router.get("/audit")
async def get_audit_trail(pack_id: str | None = None) -> dict[str, Any]:
    """Get audit trail, optionally filtered by pack_id."""
    entries = governance_engine.get_audit_trail(pack_id=pack_id)
    return {
        "entries": entries,
        "count": len(entries),
    }
