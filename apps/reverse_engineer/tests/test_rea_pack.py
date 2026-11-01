"""
Tests for the REA Capability Pack.

Covers Pydantic schema validation and REA service degradation behaviour
when the CLI is unavailable.
"""

from __future__ import annotations

import pytest

from apps.reverse_engineer.models import (
    REAAnalysisResult,
    REAEvidence,
    REARequest,
    REAResponse,
    REATargetType,
)
from apps.reverse_engineer.rea_service import REAService

# ------------------------------------------------------------------
# Model tests
# ------------------------------------------------------------------


def test_rea_evidence_defaults():
    ev = REAEvidence(
        target_type=REATargetType.NATIVE,
        target_path="/bin/ls",
        summary="summary",
    )
    assert ev.evidence_id.startswith("EVID-")
    assert ev.target_type == REATargetType.NATIVE
    assert ev.observations == []
    assert ev.inferences == []
    assert ev.unknowns == []


def test_rea_analysis_result():
    result = REAAnalysisResult(
        target_path="/app",
        target_type=REATargetType.ELECTRON_JS,
        summary="js app analysed",
    )
    assert result.analysis_id.startswith("ANA-")
    assert result.target_type == REATargetType.ELECTRON_JS
    assert result.evidence == []
    assert result.artifacts == []


def test_rea_request_response():
    req = REARequest(query="analyse this", target_path="/bin/foo")
    assert req.query == "analyse this"
    assert req.target_path == "/bin/foo"
    assert req.deep_analysis is False

    resp = REAResponse(status="success", message="ok")
    assert resp.status == "success"
    assert resp.pack == "reverse-engineer"
    assert resp.version == "1.0.0"


# ------------------------------------------------------------------
# Service tests (degradation when CLI missing)
# ------------------------------------------------------------------


def test_rea_service_unavailable(tmp_path, monkeypatch):
    """When no REA CLI is on PATH, the service returns a graceful result."""
    import apps.reverse_engineer.rea_service as rs

    monkeypatch.setattr(rs.shutil, "which", lambda _: None)
    svc = REAService()
    assert svc.available is False

    # Create a temp JS file so type guessing can classify it
    js_file = tmp_path / "app.js"
    js_file.write_text("console.log('hi');")

    import asyncio

    result = asyncio.run(svc.analyze_target(str(js_file)))
    assert result.target_type == REATargetType.ELECTRON_JS
    assert "not available" in result.summary.lower()
    assert len(result.findings) > 0


def test_rea_service_target_not_found():
    import asyncio

    svc = REAService()
    result = asyncio.run(svc.analyze_target("/does/not/exist.bin"))
    assert result.target_type == REATargetType.UNKNOWN
    assert "not found" in result.summary.lower()


# ------------------------------------------------------------------
# Pack entrypoint tests
# ------------------------------------------------------------------


def test_pack_to_dict():
    from apps.reverse_engineer.app import ReverseEngineerCapabilityPack

    pack = ReverseEngineerCapabilityPack()
    meta = pack.to_dict()
    assert meta["name"] == "reverse-engineer"
    assert meta["version"] == "1.0.0"
    assert "rea_available" in meta


@pytest.mark.asyncio
async def test_pack_run_no_target():
    from apps.reverse_engineer.app import ReverseEngineerCapabilityPack

    pack = ReverseEngineerCapabilityPack()
    result = await pack.run(user_input="analyse something")
    assert result["status"] == "info"
    assert "No target artifact" in result["message"]
