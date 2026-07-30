"""
F3 — Refactoring Planner
=========================

Produces a structured refactoring plan:
Problem -> Cause -> Proposal -> Expected Benefit -> Risk -> Migration Steps
"""

import ast
import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class RefactoringStep:
    step: str
    description: str


@dataclass
class RefactoringPlan:
    problem: str
    cause: str
    proposal: str
    expected_benefit: str
    risk: str
    migration_steps: list[RefactoringStep]
    confidence: float = 0.8
    effort: str = "medium"

    def to_dict(self) -> dict[str, Any]:
        return {
            "problem": self.problem,
            "cause": self.cause,
            "proposal": self.proposal,
            "expected_benefit": self.expected_benefit,
            "risk": self.risk,
            "migration_steps": [{"step": s.step, "description": s.description} for s in self.migration_steps],
            "confidence": self.confidence,
            "effort": self.effort,
        }


class RefactoringPlanner:
    """Generates refactoring plans without modifying code."""

    async def plan(self, code: str, filename: str = "<unknown>") -> dict[str, Any]:
        try:
            tree = ast.parse(code, filename=filename)
        except SyntaxError:
            return {"error": "Syntax error in code", "filename": filename}

        plans: list[RefactoringPlan] = []
        raw = code
        lines = code.splitlines()

        if any(" = []" in raw.splitlines()[i] or " = {}" in raw.splitlines()[i] for i in range(min(20, len(raw.splitlines())))):
            plans.append(RefactoringPlan(
                problem="Mutable default arguments",
                cause="Function parameters use mutable defaults (list/dict).",
                proposal="Replace mutable defaults with None and instantiate inside function.",
                expected_benefit="Eliminates shared-state bugs across calls.",
                risk="Low",
                migration_steps=[
                    RefactoringStep(step="1", description="Identify all mutable default arguments."),
                    RefactoringStep(step="2", description="Change default to None."),
                    RefactoringStep(step="3", description="Instantiate new object inside function if arg is None."),
                ],
                confidence=0.95,
                effort="low",
            ))

        long_functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.end_lineno and (node.end_lineno - node.lineno) > 50]
        if long_functions:
            func = long_functions[0]
            assert func.end_lineno is not None
            plans.append(RefactoringPlan(
                problem=f"Long function '{func.name}' ({func.end_lineno - func.lineno} lines)",
                cause="Function violates single responsibility and is difficult to test.",
                proposal="Extract logical blocks into well-named helper functions.",
                expected_benefit="Improved readability, testability, and reuse.",
                risk="Low",
                migration_steps=[
                    RefactoringStep(step="1", description="Identify logical blocks within function."),
                    RefactoringStep(step="2", description="Extract each block into a helper function."),
                    RefactoringStep(step="3", description="Write unit tests for extracted helpers."),
                ],
                confidence=0.85,
                effort="medium",
            ))

        if raw.count("import ") > 15 and len(raw) < 3000:
            plans.append(RefactoringPlan(
                problem="High import density",
                cause="Module imports many dependencies, increasing coupling.",
                proposal="Group imports, remove unused imports, and split module by responsibility.",
                expected_benefit="Faster import times, reduced coupling, clearer ownership.",
                risk="Low",
                migration_steps=[
                    RefactoringStep(step="1", description="Run linter to identify unused imports."),
                    RefactoringStep(step="2", description="Group standard, third-party, and local imports."),
                    RefactoringStep(step="3", description="Split module if imports span unrelated domains."),
                ],
                confidence=0.8,
                effort="low",
            ))

        if not plans:
            plans.append(RefactoringPlan(
                problem="No major refactoring opportunities detected",
                cause="Code follows common best practices.",
                proposal="Continue monitoring for code smells as codebase evolves.",
                expected_benefit="Maintains current code quality.",
                risk="Low",
                migration_steps=[
                    RefactoringStep(step="1", description="Run periodic static analysis."),
                    RefactoringStep(step="2", description="Address new findings incrementally."),
                ],
                confidence=0.7,
                effort="low",
            ))

        return {
            "filename": filename,
            "total_plans": len(plans),
            "plans": [p.to_dict() for p in plans],
        }


refactoring_planner = RefactoringPlanner()