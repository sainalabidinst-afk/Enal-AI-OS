from __future__ import annotations

import json
from pathlib import Path

from apps.self_development.ecp_analyzer import ECPAnalyzer
from apps.self_development.proposal_repository import ProposalRepository
from apps.self_development.schemas import ECPPlatformAnalysis, ImprovementProposal


def _create_pack(root: Path, name: str) -> Path:
    pack_dir = root / "apps" / name
    pack_dir.mkdir(parents=True)
    (pack_dir / "__init__.py").write_text("")
    return pack_dir


def test_existing_pack_aliases_do_not_create_capability_gaps(tmp_path: Path) -> None:
    for name in ("ai_ethics_pack", "supply_chain_analyst", "translator_expert"):
        _create_pack(tmp_path, name)

    analyzer = ECPAnalyzer(root=tmp_path)
    analysis = ECPPlatformAnalysis(0, 3, 3, "low")

    gap_domains = {gap["domain"] for gap in analyzer._detect_pack_gaps()}
    proposal_domains = {proposal.domain for proposal in analyzer.propose_capabilities(analysis)}

    assert "ai-ethics" not in gap_domains
    assert "supply-chain" not in gap_domains
    assert "translator" not in gap_domains
    assert not {"ai_ethics", "supply_chain", "translator"} & proposal_domains


def test_governance_checks_repository_level_pack_assets(tmp_path: Path) -> None:
    _create_pack(tmp_path, "devsecops")
    _create_pack(tmp_path, "ai_ethics_pack")
    (tmp_path / "docs" / "capabilities").mkdir(parents=True)
    (tmp_path / "docs" / "capabilities" / "devsecops.md").write_text("# DevSecOps")
    (tmp_path / "docs" / "capabilities" / "ai-ethics-pack.md").write_text("# AI Ethics")
    (tmp_path / "benchmarks").mkdir()
    (tmp_path / "benchmarks" / "devsecops_benchmark.py").write_text("")
    (tmp_path / "benchmarks" / "ai_ethics_pack_benchmark.py").write_text("")
    (tmp_path / "real_cases" / "devsecops").mkdir(parents=True)
    (tmp_path / "real_cases" / "ai-ethics-governance").mkdir(parents=True)

    issues = ECPAnalyzer(root=tmp_path)._detect_governance_issues()

    assert issues == []


def test_governance_targets_are_relative_and_stable(tmp_path: Path) -> None:
    _create_pack(tmp_path, "example_pack")

    issues = ECPAnalyzer(root=tmp_path)._detect_governance_issues()

    assert issues
    assert {issue["location"] for issue in issues} == {"apps/example_pack"}


def test_pack_discovery_ignores_non_pack_scaffolds(tmp_path: Path) -> None:
    for name in ("benchmark_pack", "synthesized"):
        pack_dir = tmp_path / "apps" / name
        pack_dir.mkdir(parents=True)
        (pack_dir / "engine.py").write_text("")

    assert ECPAnalyzer(root=tmp_path)._pack_dirs() == []


def test_source_scan_skips_large_fixture_and_generated_directories(tmp_path: Path) -> None:
    _create_pack(tmp_path, "example_pack")
    source_dir = tmp_path / "apps" / "example_pack"
    (source_dir / "engine.py").write_text("value = 1")
    generated_dir = source_dir / "node_modules"
    generated_dir.mkdir()
    (generated_dir / "generated.py").write_text("value = 2")
    case_dir = tmp_path / "real_cases" / "large_case"
    case_dir.mkdir(parents=True)
    (case_dir / "fixture.py").write_text("value = 3")

    analysis = ECPAnalyzer(root=tmp_path).analyze()

    assert analysis.total_files == 2


def test_legacy_refactor_patterns_are_deduplicated_by_pattern(tmp_path: Path) -> None:
    proposal_fields = {
        "target_type": "cross_pack",
        "improvement_type": "refactor",
        "description": "Extract shared pattern: security",
        "estimated_effort": "medium",
        "risk": "low",
        "confidence": 0.8,
        "expected_impact": "Reduce duplication across packs",
        "status": "draft",
        "metadata": {},
    }
    proposal_file = tmp_path / "proposals.json"
    proposal_file.write_text(
        json.dumps(
            {
                "capabilities": [],
                "improvements": [
                    {**proposal_fields, "id": "imp-legacy-a", "target_id": "pattern-legacy-a"},
                    {**proposal_fields, "id": "imp-legacy-b", "target_id": "pattern-legacy-b"},
                ],
            }
        )
    )

    repository = ProposalRepository(storage_path=proposal_file)
    proposals = repository.list_improvements(target_type="cross_pack")

    assert len(proposals) == 1
    assert proposals[0].target_id == "pattern-security"

    repository.add_improvement(
        ImprovementProposal(
            id="imp-current",
            target_type="cross_pack",
            target_id="pattern-security",
            improvement_type="refactor",
            description="Extract shared pattern: security",
            estimated_effort="medium",
            risk="low",
            confidence=0.8,
            expected_impact="Reduce duplication across packs",
        )
    )
    assert len(repository.list_improvements(target_type="cross_pack")) == 1
