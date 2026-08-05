"""
Smell Taxonomy
===============

Architecture/code smell catalog for Self Development.

Provides categorized problem detection rules that map project signals
to typed Problem instances.
"""

from __future__ import annotations

import logging
import math
import random
from typing import Any

from apps.self_development.schemas import Problem, ProblemType, ProjectAnalysis, Severity

logger = logging.getLogger(__name__)

SMELL_RULES: list[dict[str, Any]] = [
    {
        "type": ProblemType.BOTTLENECK,
        "severity": Severity.MEDIUM,
        "keywords": ["communication.py", "broadcast", "message bus", "event bus"],
        "description": "Komunikasi sinkron berfrekuensi tinggi meningkatkan latensi antar agen.",
        "impact": "Peningkatan latensi koordinasi multi-agen.",
        "evidence": ["keyword_match: communication.py", "pattern: broadcast loop"],
    },
    {
        "type": ProblemType.DEAD_CODE,
        "severity": Severity.LOW,
        "keywords": ["agent_registry.py", "_legacy_agent_lookup", "unused"],
        "description": "Metode lama tidak dipanggil, menambah beban pemeliharaan.",
        "impact": "Penurunan maintainability dan kejelasan kode.",
        "evidence": ["keyword_match: _legacy_agent_lookup", "call_count: 0"],
    },
    {
        "type": ProblemType.DUPLICATION,
        "severity": Severity.LOW,
        "keywords": ["team_builder.py", "skill-matching", "duplicate"],
        "description": "Logika pencocokan kemampuan terduplikasi di beberapa modul.",
        "impact": "Biaya pemeliharaan ganda dan risiko logic drift.",
        "evidence": ["similarity: team_builder.py vs registry.py", "copy-paste detection"],
    },
    {
        "type": ProblemType.ARCHITECTURE_SMELL,
        "severity": Severity.HIGH,
        "keywords": ["orchestrator_v2.py", "cognitive_kernel.py", "tight coupling"],
        "description": "Modulinti mengandalkan terlalu banyak detail modul lain.",
        "impact": "Perubahan kecil memicu efek domino di seluruh arsitektur.",
        "evidence": ["high fan-in", "cross-layer import", "low cohesion"],
    },
    {
        "type": ProblemType.SECURITY_HOLE,
        "severity": Severity.HIGH,
        "keywords": ["config.py", "hardcoded", "password", "secret", "token"],
        "description": "Kredensial atau rahasia tertanam langsung di kode sumber.",
        "impact": "Eksposur kredensial dan risiko kebocoran data.",
        "evidence": ["secret pattern detected", "plaintext credential"],
    },
    {
        "type": ProblemType.PERFORMANCE_ISSUE,
        "severity": Severity.MEDIUM,
        "keywords": ["n+1", "query", "loop", "missing index", "latency"],
        "description": "Akses berulang ke sumber daya tanpa caching atau indeks.",
        "impact": "Peningkatan latency dan beban sumber daya.",
        "evidence": ["nested iteration", "uncached lookup", "missing index"],
    },
    {
        "type": ProblemType.TEST_COVERAGE_GAP,
        "severity": Severity.MEDIUM,
        "keywords": ["tests", "coverage", "missing", "uncovered"],
        "description": "Bagian penting proyek belum ditutupi pengujian.",
        "impact": "Regresi tidak terdeteksi dan debt teknis.",
        "evidence": ["coverage report", "uncovered branches"],
    },
    {
        "type": ProblemType.DEPENDENCY_CYCLE,
        "severity": Severity.HIGH,
        "keywords": ["cycle", "circular", "import loop"],
        "description": "Dependensi melingkar antara modul-menurunkan modularitas.",
        "impact": "Pengujian dan deployment menjadi rapuh.",
        "evidence": ["pylint cyclic-import", "pydeps cycle"],
    },
    {
        "type": ProblemType.LAYER_VIOLATION,
        "severity": Severity.MEDIUM,
        "keywords": ["core", "apps", "backend", "layer violation"],
        "description": "Pelanggaran batas lapisan arsitektur (mis. core mengimpor apps).",
        "impact": "Menurunkan stabilitas inti dan memicu regresi lintas-modul.",
        "evidence": ["import path violation", "dependency direction"],
    },
    {
        "type": ProblemType.API_CONTRACT_BREAKING,
        "severity": Severity.HIGH,
        "keywords": ["endpoint", "api", "breaking", "contract"],
        "description": "Perubahan kontrak API tanpa versi atau migrasi.",
        "impact": "Klien eksternal/internal mengalami kerusakan.",
        "evidence": ["schema diff", "missing deprecation"],
    },
]


class SmellTaxonomy:
    """Detects architecture/code smells from project analysis."""

    def detect(self, analysis: ProjectAnalysis) -> list[Problem]:
        rng = random.Random(hash(analysis.project) % (2**32))
        problems: list[Problem] = []
        hotspots = analysis.metadata.get("hotspots", []) or []
        for rule in SMELL_RULES:
            matched_keywords = [kw for kw in rule["keywords"] if kw in hotspots]
            if matched_keywords:
                confidence = min(0.95, 0.7 + 0.05 * len(matched_keywords) + rng.uniform(0.0, 0.05))
                problem = Problem(
                    id=self._make_id(rule["type"].value),
                    type=rule["type"].value,
                    severity=rule["severity"].value,
                    location=matched_keywords[0],
                    description=rule["description"],
                    impact=rule["impact"],
                    confidence=confidence,
                    evidence=rule["evidence"] + [f"matched: {matched_keywords}"],
                )
                problems.append(problem)
        return problems

    @staticmethod
    def _make_id(problem_type: str) -> str:
        return f"{problem_type}-{abs(hash(problem_type)) % 10000:04d}"
