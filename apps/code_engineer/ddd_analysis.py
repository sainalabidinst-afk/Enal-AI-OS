"""
DDD Analysis
=============

Domain-Driven Design pattern analysis.

- Bounded Contexts: clear module boundaries
- Entities: objects with identity (id, uuid)
- Value Objects: immutable objects without identity
- Aggregates: root entity + related entities
- Domain Events: events emitted by aggregates
- Repositories: persistence abstraction
- Anti-Corruption Layer: translation between contexts
"""

from apps.code_engineer.architecture_patterns import ArchitectureFinding, ArchitectureSeverity


class DDDAnalyzer:
    """Domain-Driven Design pattern analysis."""

    def analyze_entities(self, code_ast) -> list[ArchitectureFinding]:
        """Detect Entity and Value Object patterns."""
        findings: list[ArchitectureFinding] = []
        raw = "\n".join(code_ast.raw_lines)

        for cls in code_ast.classes:
            method_names = [m.name for m in cls.methods]
            has_identity = any(
                "id" in m.name.lower() or "uuid" in m.name.lower() or "identity" in m.name.lower()
                for m in cls.methods
            ) or "id" in raw[:1000]

            if has_identity and not any(kw in cls.name.lower() for kw in ["value", "dto", "vo"]):
                findings.append(ArchitectureFinding(
                    category="ddd",
                    severity=ArchitectureSeverity.INFO,
                    description=f"Class '{cls.name}' looks like a DDD Entity (has identity)",
                    recommendation=(
                        "Ensure Entity has: identity-based equality, domain methods "
                        "expressing business rules, and no framework dependencies."
                    ),
                    line_number=cls.lineno,
                    confidence=0.65,
                    pattern="entity",
                ))

            has_eq = "__eq__" in method_names
            is_namedtuple = "NamedTuple" in cls.bases or "namedtuple" in cls.bases
            is_dataclass = "dataclass" in cls.decorators or "dataclasses" in raw

            if (has_eq and not has_identity) or is_namedtuple or (is_dataclass and not has_identity):
                findings.append(ArchitectureFinding(
                    category="ddd",
                    severity=ArchitectureSeverity.INFO,
                    description=f"Class '{cls.name}' looks like a DDD Value Object",
                    recommendation=(
                        "Value Objects are immutable, compared by value, and have no identity. "
                        "Consider using @dataclass(frozen=True)."
                    ),
                    line_number=cls.lineno,
                    confidence=0.7,
                    pattern="value_object",
                ))

            has_children = any(
                m.name in ("add_", "remove_", "add_item", "add_entity", "children", "items", "parts")
                or m.name.startswith("add_")
                for m in cls.methods
            )
            if has_identity and has_children:
                findings.append(ArchitectureFinding(
                    category="ddd",
                    severity=ArchitectureSeverity.INFO,
                    description=f"Class '{cls.name}' looks like a DDD Aggregate Root",
                    recommendation=(
                        "Aggregate Root controls consistency boundary: all invariants "
                        "are enforced through the root. External entities reference the root by ID only."
                    ),
                    line_number=cls.lineno,
                    confidence=0.6,
                    pattern="aggregate_root",
                ))
        return findings

    def analyze_repositories(self, code_ast) -> list[ArchitectureFinding]:
        """Detect Repository pattern and anti-corruption layer."""
        findings: list[ArchitectureFinding] = []
        for cls in code_ast.classes:
            cls_name = cls.name.lower()
            is_repository = "repository" in cls_name or "repo" in cls_name
            is_acl = "acl" in cls_name or "anti_corruption" in cls_name or "translation" in cls_name

            if is_repository:
                has_crud = any(
                    m.name in ("save", "delete", "find", "find_by_id", "find_all", "get_by_id", "update")
                    for m in cls.methods
                )
                if has_crud:
                    findings.append(ArchitectureFinding(
                        category="ddd",
                        severity=ArchitectureSeverity.INFO,
                        description=f"Repository pattern detected: '{cls.name}'",
                        recommendation=(
                            "Repository abstracts persistence. The domain layer depends on the "
                            "repository interface, not on infrastructure implementation."
                        ),
                        line_number=cls.lineno,
                        confidence=0.85,
                        pattern="repository",
                    ))
            if is_acl:
                findings.append(ArchitectureFinding(
                    category="ddd",
                    severity=ArchitectureSeverity.INFO,
                    description=f"Anti-Corruption Layer detected: '{cls.name}'",
                    recommendation=(
                        "ACL translates between bounded contexts, protecting the domain "
                        "from external model corruption."
                    ),
                    line_number=cls.lineno,
                    confidence=0.8,
                    pattern="anti_corruption_layer",
                ))
        return findings

    def analyze_domain_events(self, code_ast) -> list[ArchitectureFinding]:
        """Detect Domain Events patterns."""
        findings: list[ArchitectureFinding] = []
        for cls in code_ast.classes:
            cls_name = cls.name.lower()
            is_event = any(kw in cls_name for kw in [
                "event", "occurred", "happened", "raised", "created", "updated", "deleted"
            ])
            if is_event:
                findings.append(ArchitectureFinding(
                    category="ddd",
                    severity=ArchitectureSeverity.INFO,
                    description=f"Domain Event detected: '{cls.name}'",
                    recommendation=(
                        "Domain Events capture significant business occurrences. "
                        "They are immutable and include a timestamp and event ID."
                    ),
                    line_number=cls.lineno,
                    confidence=0.8,
                    pattern="domain_event",
                ))
        return findings

    def analyze(self, code_ast) -> list[ArchitectureFinding]:
        findings: list[ArchitectureFinding] = []
        findings.extend(self.analyze_entities(code_ast))
        findings.extend(self.analyze_repositories(code_ast))
        findings.extend(self.analyze_domain_events(code_ast))
        return findings
