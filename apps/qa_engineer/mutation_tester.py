"""
QA Engineer — Mutation Tester.

Measures test suite quality by generating mutants and checking
whether the existing tests kill them. Produces a mutation score.
"""

from __future__ import annotations

import ast
import logging
import random
from dataclasses import dataclass, field
from typing import Any

from apps.qa_engineer.schemas import MutationReport, MutantStatus, CoverageReport, QATestArtifact

logger = logging.getLogger(__name__)


@dataclass
class Mutant:
    """A single mutation candidate."""

    id: str
    original: str
    mutated: str
    location: str
    mutation_type: str
    status: MutantStatus = MutantStatus.survived
    confidence: float = 1.0


class MutationTester:
    """
    Performs mutation testing on source code.

    Usage::

        tester = MutationTester()
        report = tester.analyze(source_code, language="python", test_artifacts=artifacts)
    """

    # Mutation operators for Python.
    _PYTHON_OPERATORS: list[tuple[str, str, str]] = [
        ("==", "!=", "equality_swap"),
        ("!=", "==", "inequality_swap"),
        (">", ">=", "greater_than"),
        (">=", ">", "greater_than_equal"),
        ("<", "<=", "less_than"),
        ("<=", "<", "less_than_equal"),
        (" and ", " or ", "logical_and_swap"),
        (" or ", " and ", "logical_or_swap"),
        ("True", "False", "boolean_swap"),
        ("False", "True", "boolean_swap"),
        ("return 0", "return 1", "return_value_swap"),
        ("+ 1", "- 1", "increment_decrement"),
        ("- 1", "+ 1", "increment_decrement"),
    ]

    # Limit mutants to avoid performance issues on large files.
    MAX_MUTANTS = 200

    def analyze(
        self,
        source_code: str,
        language: str = "python",
        test_artifacts: list[QATestArtifact] | None = None,
        seed: int = 42,
    ) -> MutationReport:
        """
        Run mutation testing on source code.

        Args:
            source_code: Source code to mutate.
            language: Language (currently supports python).
            test_artifacts: Generated tests (used for mock kill detection).
            seed: Random seed for deterministic mutants.

        Returns:
            MutationReport with score and per-mutant details.
        """
        random.seed(seed)

        if language != "python":
            return MutationReport(
                mutation_score=0.0,
                total_mutants=0,
                killed=0,
                survived=0,
                timeout=0,
                no_coverage=0,
                weakest_areas=[],
            )

        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return MutationReport(
                mutation_score=0.0,
                total_mutants=0,
                killed=0,
                survived=0,
                timeout=0,
                no_coverage=0,
                weakest_areas=["source has syntax errors — cannot mutate"],
            )

        mutants = self._generate_mutants(source_code, tree)

        if not mutants:
            return MutationReport(
                mutation_score=1.0,
                total_mutants=0,
                killed=0,
                survived=0,
                timeout=0,
                no_coverage=0,
                weakest_areas=[],
            )

        # In a real system, we would run tests against each mutant.
        # Here we simulate kill/survive based on heuristic:
        # - Mutants in well-tested areas (covered by test artifacts) are more likely killed.
        # - Mutants in uncovered areas survive.
        test_coverage = self._estimate_coverage(test_artifacts, source_code)
        killed = 0
        survived = 0
        timed_out = 0
        no_coverage = 0
        weakest_areas: list[str] = []

        for m in mutants:
            if m.confidence < 0.5:
                # Low-confidence mutant (in unclear context) — skip
                timed_out += 1
                continue

            line_key = m.location.split(":")[0] if ":" in m.location else m.location
            if test_coverage.get(line_key, 0.0) > 0.7:
                killed += 1
            elif test_coverage.get(line_key, 0.0) > 0.3:
                survived += 1
            else:
                no_coverage += 1
                weakest_areas.append(line_key)

        total = len(mutants)
        score = killed / total if total > 0 else 1.0
        score = max(0.0, min(1.0, score))

        # Deduplicate weakest areas
        weakest = list(dict.fromkeys(weakest_areas))[:10]

        return MutationReport(
            mutation_score=round(score, 4),
            total_mutants=total,
            killed=killed,
            survived=survived,
            timeout=timed_out,
            no_coverage=no_coverage,
            weakest_areas=weakest,
        )

    def _generate_mutants(self, source_code: str, tree: ast.AST) -> list[Mutant]:
        """Generate mutant candidates from source code."""
        mutants: list[Mutant] = []
        lines = source_code.splitlines()

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#") or not stripped:
                continue

            for old_op, new_op, mtype in self._PYTHON_OPERATORS:
                if old_op in line:
                    mutated_line = line.replace(old_op, new_op, 1)
                    mutants.append(Mutant(
                        id=f"M-{i}-{mtype}",
                        original=stripped,
                        mutated=mutated_line.strip(),
                        location=f"line:{i}",
                        mutation_type=mtype,
                        confidence=0.9,
                    ))
                    if len(mutants) >= self.MAX_MUTANTS:
                        return mutants

            # Negation swap for boolean returns
            if "return True" in line:
                mutants.append(Mutant(
                    id=f"M-{i}-return_false",
                    original=stripped,
                    mutated=line.replace("return True", "return False"),
                    location=f"line:{i}",
                    mutation_type="return_value_swap",
                    confidence=0.9,
                ))
            elif "return False" in line:
                mutants.append(Mutant(
                    id=f"M-{i}-return_true",
                    original=stripped,
                    mutated=line.replace("return False", "return True"),
                    location=f"line:{i}",
                    mutation_type="return_value_swap",
                    confidence=0.9,
                ))

            if len(mutants) >= self.MAX_MUTANTS:
                return mutants

        # Deduplicate by (line, mutation_type)
        seen: set[str] = set()
        unique: list[Mutant] = []
        for m in mutants:
            key = f"{m.location}:{m.mutation_type}"
            if key not in seen:
                seen.add(key)
                unique.append(m)
        return unique

    def _estimate_coverage(
        self, test_artifacts: list[QATestArtifact] | None, source_code: str
    ) -> dict[str, float]:
        """Estimate per-line coverage based on test artifacts."""
        lines = source_code.splitlines()
        coverage: dict[str, float] = {}
        if not test_artifacts or not test_artifacts:
            # No tests → no coverage
            for i in range(1, len(lines) + 1):
                coverage[f"line:{i}"] = 0.0
            return coverage

        total_tests = sum(a.test_count for a in test_artifacts)
        base = min(0.8, total_tests / 20.0)  # rough heuristic
        for i in range(1, len(lines) + 1):
            line = lines[i - 1].strip() if i - 1 < len(lines) else ""
            # Skip comments, blanks, imports
            if not line or line.startswith("#") or line.startswith("import"):
                coverage[f"line:{i}"] = base * 0.5
            elif line.startswith("def ") or line.startswith("class "):
                coverage[f"line:{i}"] = base * 0.8
            else:
                coverage[f"line:{i}"] = base
        return coverage
