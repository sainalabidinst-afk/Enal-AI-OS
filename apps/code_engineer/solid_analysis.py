"""
SOLID Analysis
===============

SOLID Principle analysis.

- S: Single Responsibility -- classes should have one reason to change
- O: Open/Closed -- open for extension, closed for modification
- L: Liskov Substitution -- subtypes must be substitutable for base types
- I: Interface Segregation -- many specific interfaces > one general
- D: Dependency Inversion -- depend on abstractions, not concretions
"""

from apps.code_engineer.architecture_patterns import ArchitectureFinding, ArchitectureSeverity


class SOLIDAnalyzer:
    """SOLID Principle analysis."""

    def analyze_single_responsibility(self, code_ast) -> list[ArchitectureFinding]:
        """Check SRP: classes with too many methods or mixed responsibilities."""
        findings: list[ArchitectureFinding] = []
        for cls in code_ast.classes:
            num_methods = len(cls.methods)
            if num_methods > 15:
                findings.append(ArchitectureFinding(
                    category="solid",
                    severity=ArchitectureSeverity.HIGH,
                    description=f"Class '{cls.name}' has {num_methods} methods (SRP violation)",
                    recommendation=(
                        "Split class into smaller, single-responsibility classes. "
                        "Each class should have one reason to change."
                    ),
                    line_number=cls.lineno,
                    confidence=0.85,
                    pattern="single_responsibility",
                ))

            has_data = any(m.name.startswith("get_") or m.name.startswith("set_") for m in cls.methods)
            has_business = any(
                m.name in ("save", "validate", "process", "calculate", "compute", "execute")
                for m in cls.methods
            )
            if has_data and has_business and num_methods > 8:
                findings.append(ArchitectureFinding(
                    category="solid",
                    severity=ArchitectureSeverity.MEDIUM,
                    description=f"Class '{cls.name}' mixes data and business logic (SRP concern)",
                    recommendation=(
                        "Separate data holders (DTOs) from business logic. "
                        "Use service classes for business operations."
                    ),
                    line_number=cls.lineno,
                    confidence=0.65,
                    pattern="single_responsibility",
                ))
        return findings

    def analyze_open_closed(self, code_ast) -> list[ArchitectureFinding]:
        """Check OCP: long if-elif chains that could use strategy pattern."""
        findings: list[ArchitectureFinding] = []
        raw = "\n".join(code_ast.raw_lines)

        for cls in code_ast.classes:
            for method in cls.methods:
                if "elif" in raw[:2000]:
                    lines = [l for l in code_ast.raw_lines if "elif" in l]
                    if len(lines) > 3:
                        findings.append(ArchitectureFinding(
                            category="solid",
                            severity=ArchitectureSeverity.MEDIUM,
                            description=f"Method '{method.name}' in '{cls.name}' has long elif chain (OCP violation)",
                            recommendation=(
                                "Use Strategy pattern or polymorphic dispatch instead of "
                                "conditional branching. New behavior should not require "
                                "modifying existing code."
                            ),
                            line_number=method.lineno,
                            confidence=0.7,
                            pattern="open_closed",
                        ))
                        break
        return findings

    def analyze_liskov_substitution(self, code_ast) -> list[ArchitectureFinding]:
        """Check LSP: mutable defaults, improper inheritance."""
        findings: list[ArchitectureFinding] = []
        raw = "\n".join(code_ast.raw_lines)

        if "= []" in raw or "= {}" in raw:
            findings.append(ArchitectureFinding(
                category="solid",
                severity=ArchitectureSeverity.HIGH,
                description="Mutable default arguments detected (LSP violation)",
                recommendation=(
                    "Use None as default and instantiate the mutable object inside the function. "
                    "Mutable defaults are shared across all calls, causing unexpected behavior."
                ),
                line_number=1,
                confidence=0.95,
                pattern="liskov_substitution",
            ))

        for cls in code_ast.classes:
            if "pass" in raw and cls.bases:
                findings.append(ArchitectureFinding(
                    category="solid",
                    severity=ArchitectureSeverity.INFO,
                    description=f"Class '{cls.name}' inherits from {cls.bases} but only uses 'pass'",
                    recommendation=(
                        "Empty subclass may violate LSP if it doesn't fulfill the base class contract. "
                        "Either implement the required methods or reconsider the inheritance."
                    ),
                    line_number=cls.lineno,
                    confidence=0.5,
                    pattern="liskov_substitution",
                ))
        return findings

    def analyze_interface_segregation(self, code_ast) -> list[ArchitectureFinding]:
        """Check ISP: classes with many abstract methods or large protocols."""
        findings: list[ArchitectureFinding] = []
        for cls in code_ast.classes:
            is_abc = "ABC" in cls.bases or "abc" in cls.bases
            cls_name = cls.name.lower()
            if is_abc or "interface" in cls_name or "protocol" in cls_name:
                abstract_methods = sum(
                    1 for m in cls.methods
                    if "abstractmethod" in m.decorators or "abstract" in m.name.lower()
                )
                if abstract_methods > 5:
                    findings.append(ArchitectureFinding(
                        category="solid",
                        severity=ArchitectureSeverity.MEDIUM,
                        description=f"Interface '{cls.name}' has {abstract_methods} abstract methods (ISP concern)",
                        recommendation=(
                            "Split large interfaces into smaller, focused interfaces. "
                            "Clients should not depend on interfaces they don't use."
                        ),
                        line_number=cls.lineno,
                        confidence=0.7,
                        pattern="interface_segregation",
                    ))
        return findings

    def analyze_dependency_inversion(self, code_ast) -> list[ArchitectureFinding]:
        """Check DIP: high-level modules importing concrete implementations."""
        findings: list[ArchitectureFinding] = []
        for imp in code_ast.imports:
            module = imp.module.lower()
            if any(concrete in module for concrete in [
                "sqlalchemy", "fastapi", "django", "redis", "kafka", "rabbitmq", "requests"
            ]):
                findings.append(ArchitectureFinding(
                    category="solid",
                    severity=ArchitectureSeverity.MEDIUM,
                    description=f"High-level module imports concrete implementation '{imp.module}' (DIP concern)",
                    recommendation=(
                        "Depend on abstractions (interfaces/protocols), not concretions. "
                        "Inject infrastructure dependencies via constructors."
                    ),
                    line_number=1,
                    confidence=0.6,
                    pattern="dependency_inversion",
                ))
                break
        return findings

    def analyze(self, code_ast) -> list[ArchitectureFinding]:
        findings: list[ArchitectureFinding] = []
        findings.extend(self.analyze_single_responsibility(code_ast))
        findings.extend(self.analyze_open_closed(code_ast))
        findings.extend(self.analyze_liskov_substitution(code_ast))
        findings.extend(self.analyze_interface_segregation(code_ast))
        findings.extend(self.analyze_dependency_inversion(code_ast))
        return findings
