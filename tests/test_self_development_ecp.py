"""
Tests for Self Development ECP meta-analysis capabilities.
"""

import pytest

from apps.self_development.engine import self_development_engine


@pytest.fixture
def isolated_proposal_store(monkeypatch, tmp_path):
    from apps.self_development.proposal_repository import ProposalRepository

    monkeypatch.setattr(
        "apps.self_development.engine.proposal_repository",
        ProposalRepository(storage_path=tmp_path / "proposals.json"),
    )


@pytest.mark.asyncio
async def test_analyze_ecp_returns_platform_metrics():
    result = await self_development_engine.analyze_ecp()

    assert "core_modules" in result
    assert "capability_packs" in result
    assert "total_files" in result
    assert "complexity" in result
    assert "hotspots" in result
    assert "governance_issues" in result
    assert "pack_gaps" in result
    assert "cross_pack_patterns" in result


@pytest.mark.asyncio
async def test_propose_capabilities_returns_proposals(isolated_proposal_store):
    proposals = await self_development_engine.propose_capabilities()

    assert isinstance(proposals, list)
    for proposal in proposals:
        assert "id" in proposal
        assert "name" in proposal
        assert "domain" in proposal
        assert "tier" in proposal
        assert "confidence" in proposal
        assert "rationale" in proposal


@pytest.mark.asyncio
async def test_propose_improvements_returns_improvements(isolated_proposal_store):
    improvements = await self_development_engine.propose_improvements()

    assert isinstance(improvements, list)
    assert len(improvements) > 0

    improvement = improvements[0]
    assert "id" in improvement
    assert "target_type" in improvement
    assert "improvement_type" in improvement
    assert "description" in improvement
    assert "confidence" in improvement


@pytest.mark.asyncio
async def test_app_run_ecp_mode(isolated_proposal_store):
    from apps.self_development import get_app

    app = get_app()
    result = await app.run("analyze ECP platform improvements", context={})

    assert result["app"] == "self-development"
    assert result["result"]["mode"] == "ecp_meta_analysis"
    assert "ecp_analysis" in result["result"]
    assert "capability_proposals" in result["result"]
    assert "improvement_proposals" in result["result"]
