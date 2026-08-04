"""
CQRS Analysis
=============

CQRS (Command Query Responsibility Segregation) analysis.

- Commands: write operations that change state (return void)
- Queries: read operations that return data (no side effects)
- Separate read/write models for complex domains
"""

from apps.code_engineer.architecture_patterns import ArchitectureFinding, ArchitectureSeverity


class CQRSAnalyzer:
    """CQRS (Command Query Responsibility Segregation) analysis."""

    def analyze_commands(self, code_ast) -> list[ArchitectureFinding]:
        """Detect Command pattern usage."""
        findings: list[ArchitectureFinding] = []
        for cls in code_ast.classes:
            cls_name = cls.name.lower()
            if "command" in cls_name or "cmd" in cls_name:
                has_execute = any(m.name == "execute" or m.name == "handle" for m in cls.methods)
                if has_execute:
                    findings.append(ArchitectureFinding(
                        category="cqrs",
                        severity=ArchitectureSeverity.INFO,
                        description=f"CQRS Command detected: '{cls.name}'",
                        recommendation=(
                            "Commands should be: named as imperative verbs (CreateOrder), "
                            "immutable, and return void or a result status."
                        ),
                        line_number=cls.lineno,
                        confidence=0.8,
                        pattern="command",
                    ))
        return findings

    def analyze_queries(self, code_ast) -> list[ArchitectureFinding]:
        """Detect Query pattern usage."""
        findings: list[ArchitectureFinding] = []
        for cls in code_ast.classes:
            cls_name = cls.name.lower()
            if "query" in cls_name or "query" in cls_name:
                findings.append(ArchitectureFinding(
                    category="cqrs",
                    severity=ArchitectureSeverity.INFO,
                    description=f"CQRS Query detected: '{cls.name}'",
                    recommendation=(
                        "Queries should be: named as questions (GetOrderById), "
                        "have no side effects, and return data only."
                    ),
                    line_number=cls.lineno,
                    confidence=0.7,
                    pattern="query",
                ))

        for func in code_ast.functions:
            fname = func.name.lower()
            if fname.startswith("get_") or fname.startswith("find_") or fname.startswith("list_"):
                findings.append(ArchitectureFinding(
                    category="cqrs",
                    severity=ArchitectureSeverity.INFO,
                    description=f"Query function detected: '{func.name}'",
                    recommendation=(
                        "Ensure this function has no side effects. "
                        "Queries only read data; commands change state."
                    ),
                    line_number=func.lineno,
                    confidence=0.5,
                    pattern="query_separation",
                ))
        return findings

    def analyze(self, code_ast) -> list[ArchitectureFinding]:
        findings: list[ArchitectureFinding] = []
        findings.extend(self.analyze_commands(code_ast))
        findings.extend(self.analyze_queries(code_ast))
        return findings
