"""
ECP Platform Analyzer
=====================

Analyzes the ECP platform itself to detect:
- Core module issues
- Capability pack overlaps and gaps
- Governance violations
- Cross-pack patterns
- Documentation gaps
"""

from __future__ import annotations

import hashlib
import logging
import os
from pathlib import Path
from typing import Any

from apps.self_development.schemas import (
    CapabilityProposal,
    CapabilityTier,
    ECPPlatformAnalysis,
    ImprovementProposal,
    ImprovementType,
    ProblemType,
    ProposalStatus,
)

logger = logging.getLogger(__name__)


def capability_proposal_id(domain: str) -> str:
    """Stable id for a capability proposal, keyed by its domain."""
    return f"cap-{domain}"


def improvement_proposal_id(target_type: str, target_id: str, improvement_type: str) -> str:  # noqa: E501
    """Stable id for an improvement proposal, keyed by its natural key."""
    digest = hashlib.sha1(f"{target_type}|{target_id}|{improvement_type}".encode()).hexdigest()[:8]
    return f"imp-{digest}"


CORE_DIRS = [
    "backend/app/core",
    "backend/app/api",
    "apps",
    "frontend/components",
    "frontend/app",
]

HOTSPOT_CANDIDATES = [
    "cognitive_kernel.py",
    "memory_layer.py",
    "artifact_service.py",
    "workspace_service.py",
    "execution_integration.py",
    "conversation_manager.py",
    "intent_router.py",
    "society.py",
    "organization.py",
    "pipeline_engine.py",
    "tool_engine.py",
    "mcp_registry.py",
    "event_bus.py",
    "governance.py",
    "security_model.py",
]

SOURCE_DIRS = ("backend", "apps", "frontend", "sdk", "tests")
IGNORED_SOURCE_DIRS = {
    ".git",
    ".next",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "venv",
}
PACK_ALIASES = {
    "ai-ethics": {"ai-ethics-pack"},
    "supply-chain": {"supply-chain-analyst"},
    "translator": {"translator-expert"},
}
REAL_CASE_ALIASES = {
    "ai_ethics_pack": "ai-ethics-governance",
    "business_analyst": "business",
    "code_engineer": "code",
    "data_engineer": "data",
    "database_engineer": "database",
    "decision_intelligence": "decision",
    "devops_assistant": "devops",
    "full_stack_engineer": "full_stack",
    "network_engineer": "network",
    "product_manager": "product",
    "qa_engineer": "qa",
    "research_assistant": "research",
    "security_engineer": "security",
    "system_architect": "system",
    "trading_analyst": "trading",
    "ui_ux_designer": "ui_ux",
}


class ECPAnalyzer:
    """Analyzes ECP platform for improvement opportunities."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = (root or Path(".").resolve()).resolve()
        apps_dir = self.root / "apps"
        if not apps_dir.exists():
            for parent in [self.root.parent, *list(self.root.parents)[:3]]:
                if (parent / "apps").exists():
                    self.root = parent.resolve()
                    break

    def _pack_dirs(self) -> list[Path]:
        apps_dir = (self.root / "apps").resolve()
        if not apps_dir.exists():
            return []
        return sorted(
            [
                d
                for d in apps_dir.iterdir()
                if d.is_dir()
                and not d.name.startswith("__pycache__")
                and d.name not in {"society", "organization", "integration"}
                and ((d / "__init__.py").is_file() or (d / "skills.yaml").is_file())
            ]
        )

    def analyze(self) -> ECPPlatformAnalysis:
        py_files = self._python_files()
        hotspots = self._find_hotspots(py_files)
        governance_issues = self._detect_governance_issues()
        pack_gaps = self._detect_pack_gaps()
        patterns = self._detect_cross_pack_patterns()

        core_dir = self.root / "backend" / "app" / "core"
        core_modules = (
            len([f for f in py_files if f.is_relative_to(core_dir)]) if core_dir.exists() else 0
        )
        capability_packs = len(self._pack_dirs())

        complexity = "medium"
        if core_modules > 50 or capability_packs > 30:
            complexity = "high"

        return ECPPlatformAnalysis(
            core_modules=core_modules,
            capability_packs=capability_packs,
            total_files=len(py_files),
            complexity=complexity,
            hotspots=hotspots,
            governance_issues=governance_issues,
            pack_gaps=pack_gaps,
            cross_pack_patterns=patterns,
            metadata={
                "root": str(self.root),
                "pack_names": [d.name for d in self._pack_dirs()],
            },
        )

    def propose_capabilities(self, analysis: ECPPlatformAnalysis) -> list[CapabilityProposal]:
        proposals: list[CapabilityProposal] = []
        existing = self._existing_pack_names()

        candidates = [
            (
                "observability",
                "Observability Engineer",
                "Metrics, tracing, logging, anomaly detection",
                CapabilityTier.TIER_A,
            ),
            (
                "cybersecurity_analyst",
                "Cybersecurity Analyst",
                "Threat modeling, incident detection, compliance mapping",
                CapabilityTier.TIER_A,
            ),
            (
                "ai_ethics",
                "AI Ethics & Governance",
                "Fairness, bias detection, explainability, regulatory compliance",
                CapabilityTier.TIER_B,
            ),
            (
                "supply_chain",
                "Supply Chain Analyst",
                "Logistics optimization, demand forecasting, risk management",
                CapabilityTier.TIER_C,
            ),
            (
                "data_scientist",
                "Data Scientist",
                "Advanced ML pipelines, feature engineering, model evaluation",
                CapabilityTier.TIER_B,
            ),
            (
                "business_intelligence",
                "Business Intelligence",
                "Dashboarding, KPI tracking, scenario planning",
                CapabilityTier.TIER_B,
            ),
            (
                "innovation_strategist",
                "Innovation Strategist",
                "Trend analysis, R&D portfolio, foresight modeling",
                CapabilityTier.TIER_C,
            ),
            (
                "devsecops",
                "DevSecOps",
                "Security-by-design, shift-left, compliance-as-code",
                CapabilityTier.TIER_B,
            ),
            (
                "translator",
                "Translator Expert",
                "Document translation, multilingual support, localization",
                CapabilityTier.TIER_C,
            ),
            (
                "document_processing",
                "Document Processing",
                "PDF, DOCX, CSV parsing, extraction, OCR",
                CapabilityTier.TIER_C,
            ),
            (
                "voice_interaction",
                "Voice Interaction",
                "STT, TTS, voice commands, telephony",
                CapabilityTier.TIER_C,
            ),
        ]

        for domain, name, description, tier in candidates:
            if not self._has_pack(domain, existing):
                reuse = self._estimate_reuse(domain, analysis)
                effort = self._estimate_effort(tier)
                risk = "low" if tier == CapabilityTier.TIER_C else "medium"
                confidence = 0.85 if reuse >= 3 else 0.7
                rationale = f"Gap identified: {name} capabilities not covered by existing packs. Reuse potential: {reuse} packs."  # noqa: E501

                proposals.append(
                    CapabilityProposal(
                        id=capability_proposal_id(domain),
                        name=name,
                        domain=domain,
                        description=description,
                        tier=tier.value if isinstance(tier, CapabilityTier) else tier,
                        reuse_potential=reuse,
                        estimated_effort=effort,
                        risk=risk,
                        confidence=confidence,
                        rationale=rationale,
                        required_packs=self._required_packs(domain),
                        status=ProposalStatus.DRAFT.value,
                    )
                )

        return proposals

    def propose_improvements(self, analysis: ECPPlatformAnalysis) -> list[ImprovementProposal]:
        improvements: list[ImprovementProposal] = []

        for issue in analysis.governance_issues:
            improvements.append(
                ImprovementProposal(
                    id=improvement_proposal_id(
                        "governance", issue.get("location", ""), ImprovementType.GOVERNANCE.value
                    ),
                    target_type="governance",
                    target_id=issue.get("location", ""),
                    improvement_type=ImprovementType.GOVERNANCE.value,
                    description=issue.get("description", ""),
                    estimated_effort="low",
                    risk="low",
                    confidence=0.9,
                    expected_impact="Governance compliance improved",
                )
            )

        for gap in analysis.pack_gaps:
            improvements.append(
                ImprovementProposal(
                    id=improvement_proposal_id(
                        "capability_pack",
                        gap.get("pack", ""),
                        ImprovementType.NEW_CAPABILITY.value,
                    ),
                    target_type="capability_pack",
                    target_id=gap.get("pack", ""),
                    improvement_type=ImprovementType.NEW_CAPABILITY.value,
                    description=gap.get("description", ""),
                    estimated_effort="high",
                    risk="medium",
                    confidence=0.7,
                    expected_impact=f"New capability: {gap.get('pack', '')}",
                )
            )

        for pattern in analysis.cross_pack_patterns:
            improvements.append(
                ImprovementProposal(
                    id=improvement_proposal_id(
                        "cross_pack",
                        pattern.get("id", ""),
                        ImprovementType.REFACTOR.value,
                    ),
                    target_type="cross_pack",
                    target_id=pattern.get("id", ""),
                    improvement_type=ImprovementType.REFACTOR.value,
                    description=f"Extract shared pattern: {pattern.get('pattern_type', '')}",
                    estimated_effort="medium",
                    risk="low",
                    confidence=0.8,
                    expected_impact="Reduce duplication across packs",
                )
            )

        return improvements

    def _find_hotspots(self, py_files: list[Path]) -> list[str]:
        hotspots: list[str] = []
        candidates = set(HOTSPOT_CANDIDATES)
        found: set[str] = set()
        for path in py_files:
            if path.name in candidates and path.name not in found:
                hotspots.append(path.relative_to(self.root).as_posix())
                found.add(path.name)
            if found == candidates:
                break
        return hotspots

    def _python_files(self) -> list[Path]:
        files: list[Path] = []
        for source_dir in SOURCE_DIRS:
            base = self.root / source_dir
            if not base.is_dir():
                continue
            for current, dirs, filenames in os.walk(base):
                dirs[:] = sorted(d for d in dirs if d not in IGNORED_SOURCE_DIRS)
                files.extend(
                    Path(current) / name for name in sorted(filenames) if name.endswith(".py")
                )
        return files

    def _existing_pack_names(self) -> set[str]:
        return {directory.name.lower().replace("_", "-") for directory in self._pack_dirs()}

    @staticmethod
    def _has_pack(domain: str, existing: set[str]) -> bool:
        normalized = domain.lower().replace("_", "-")
        aliases = PACK_ALIASES.get(normalized, set())
        return normalized in existing or bool(aliases & existing)

    def _detect_governance_issues(self) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []

        for pack_dir in self._pack_dirs():
            pack_name = pack_dir.name.lower()
            pack_slug = pack_name.replace("_", "-")
            has_benchmark = (
                (pack_dir / "benchmarks").exists()
                or (pack_dir / "benchmark").exists()
                or (self.root / "benchmarks" / f"{pack_name}_benchmark.py").is_file()
                or (self.root / "benchmarks" / f"{pack_slug}_benchmark.py").is_file()
            )
            real_case_names = {
                pack_name,
                pack_slug,
                REAL_CASE_ALIASES.get(pack_name, ""),
            }
            has_real_cases = (
                (pack_dir / "real_cases").exists()
                or (pack_dir / "cases").exists()
                or any(
                    (self.root / "real_cases" / name).is_dir() for name in real_case_names if name
                )
            )
            has_docs = (pack_dir / "docs").exists() or (
                (self.root / "docs" / "capabilities" / f"{pack_name}.md").is_file()
                or (self.root / "docs" / "capabilities" / f"{pack_slug}.md").is_file()
            )
            location = pack_dir.relative_to(self.root).as_posix()

            if not has_benchmark:
                issues.append(
                    {
                        "type": ProblemType.TEST_COVERAGE_GAP.value,
                        "location": location,
                        "description": f"Pack {pack_dir.name} missing benchmark",
                        "severity": "medium",
                    }
                )
            if not has_real_cases:
                issues.append(
                    {
                        "type": ProblemType.TEST_COVERAGE_GAP.value,
                        "location": location,
                        "description": f"Pack {pack_dir.name} missing real_cases",
                        "severity": "medium",
                    }
                )
            if not has_docs:
                issues.append(
                    {
                        "type": ProblemType.DOCUMENTATION_GAP.value,
                        "location": location,
                        "description": f"Pack {pack_dir.name} missing capability docs",
                        "severity": "low",
                    }
                )

        return issues

    def _detect_pack_gaps(self) -> list[dict[str, Any]]:
        gaps: list[dict[str, Any]] = []
        existing = self._existing_pack_names()

        expected = [
            (
                "observability",
                "Observability Engineer",
                "Metrics, tracing, logging, anomaly detection",
            ),
            (
                "cybersecurity-analyst",
                "Cybersecurity Analyst",
                "Threat modeling, incident detection",
            ),
            ("ai-ethics", "AI Ethics & Governance", "Fairness, bias detection, explainability"),
            ("supply-chain", "Supply Chain Analyst", "Logistics optimization, demand forecasting"),
            ("data-scientist", "Data Scientist", "Advanced ML pipelines, model evaluation"),
            ("business-intelligence", "Business Intelligence", "Dashboarding, KPI tracking"),
            ("innovation-strategist", "Innovation Strategist", "Trend analysis, R&D portfolio"),
            ("devsecops", "DevSecOps", "Security-by-design, shift-left"),
            ("translator", "Translator Expert", "Document translation, multilingual support"),
            ("document-processing", "Document Processing", "PDF, DOCX, CSV parsing"),
            ("voice-interaction", "Voice Interaction", "STT, TTS, voice commands"),
        ]

        for domain, name, description in expected:
            if not self._has_pack(domain, existing):
                gaps.append(
                    {
                        "pack": name,
                        "domain": domain,
                        "description": description,
                        "tier": "tier_b",
                    }
                )

        return gaps

    def _detect_cross_pack_patterns(self) -> list[dict[str, Any]]:
        patterns: list[dict[str, Any]] = []

        common_tools = {
            "code_analysis": ["code_engineer", "full_stack_engineer", "self_development"],
            "testing": ["qa_engineer", "code_engineer", "self_development"],
            "deployment": ["devops_assistant", "full_stack_engineer", "infrastructure_engineer"],
            "security": ["security_engineer", "devsecops", "network_engineer"],
            "data_processing": ["data_engineer", "data_scientist", "business_intelligence"],
        }
        for pattern_type, packs in common_tools.items():
            pack_dirs = [p for p in packs if any(d.name == p for d in self._pack_dirs())]
            if len(pack_dirs) >= 2:
                patterns.append(
                    {
                        "id": f"pattern-{pattern_type}",
                        "pattern_type": pattern_type,
                        "description": f"Shared {pattern_type} pattern across multiple packs",
                        "source_packs": pack_dirs,
                        "target_packs": pack_dirs,
                        "reusability_score": min(1.0, len(pack_dirs) / 5.0),
                        "implementation_complexity": "medium",
                    }
                )

        return patterns

    def _estimate_reuse(self, domain: str, analysis: ECPPlatformAnalysis) -> int:
        reuse_keywords = {
            "observability": ["metrics", "logging", "tracing", "monitoring"],
            "cybersecurity_analyst": ["security", "threat", "incident"],
            "ai_ethics": ["bias", "fairness", "explainability"],
            "supply_chain": ["logistics", "forecasting", "optimization"],
            "data_scientist": ["data", "ml", "model"],
            "business_intelligence": ["dashboard", "kpi", "reporting"],
            "innovation_strategist": ["trend", "forecast", "strategy"],
            "devsecops": ["security", "devops", "compliance"],
            "translator": ["language", "translation", "localization"],
            "document_processing": ["document", "pdf", "extraction"],
            "voice_interaction": ["voice", "stt", "tts"],
        }

        keywords = reuse_keywords.get(domain, [])
        reuse = 0
        for pattern in analysis.cross_pack_patterns:
            if any(kw in pattern.get("pattern_type", "") for kw in keywords):
                reuse += len(pattern.get("source_packs", []))
        return max(1, reuse)

    def _estimate_effort(self, tier: str) -> str:
        if tier == CapabilityTier.TIER_A:
            return "high"
        if tier == CapabilityTier.TIER_B:
            return "medium"
        return "low"

    def _required_packs(self, domain: str) -> list[str]:
        deps: dict[str, list[str]] = {
            "observability": ["infrastructure_engineer", "devops_assistant"],
            "cybersecurity_analyst": ["security_engineer", "devsecops"],
            "ai_ethics": ["ai_engineer", "decision_intelligence"],
            "supply_chain": ["data_engineer", "business_analyst"],
            "data_scientist": ["data_engineer", "ai_engineer"],
            "business_intelligence": ["data_engineer", "business_analyst"],
            "innovation_strategist": ["research_assistant", "business_analyst"],
            "devsecops": ["security_engineer", "devops_assistant"],
            "translator": ["document_processing", "research_assistant"],
            "document_processing": ["ai_engineer", "data_engineer"],
            "voice_interaction": ["ai_engineer", "document_processing"],
        }
        return deps.get(domain, [])
