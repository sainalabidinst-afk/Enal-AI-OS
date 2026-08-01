"""
Architecture Patterns Knowledge
===============================

Implements RFC-0006 Code Knowledge Expansion:
- Clean Architecture: layer detection, dependency rule, boundaries
- DDD: bounded contexts, entities, value objects, aggregates, domain events
- SOLID: all 5 principles with detection logic
- CQRS: command/query separation, write/read models
- Event Sourcing: event store, replay, projection

This module produces structured findings about code architecture.
It does NOT modify code. It only analyzes and reports.
"""

import ast
import logging
from dataclasses import dataclass, field
from typing import Any, Optional

from apps.code_engineer.parser import CodeAST

logger = logging.getLogger(__name__)


class ArchitectureSeverity:
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class ArchitectureFinding:
    """A single architecture pattern finding."""
    category: str
    severity: str
    description: str
    recommendation: str
    line_number: int
    confidence: float = 1.0
    pattern: str = ""
    examples: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "severity": self.severity,
            "description": self.description,
            "recommendation": self.recommendation,
            "line_number": self.line_number,
            "confidence": round(self.confidence, 2),
            "pattern": self.pattern,
            "examples": self.examples,
        }


class CleanArchitectureAnalyzer:
    """
    Clean Architecture layer analysis.

    Layers:
    - Entities: domain objects with business rules (pure Python, no dependencies)
    - Use Cases: application-specific business rules
    - Interface Adapters: controllers, presenters, gateways
    - Frameworks & Drivers: web frameworks, DB, external services

    Dependency Rule: source code dependencies must point inward.
    Inner layers must not depend on outer layers.
    """

    LAYER_KEYWORDS = {
        "entity": ["entity", "domain", "model", "models", "aggregate"],
        "use_case": ["use_case", "usecase", "service", "interactor", "application"],
        "adapter": ["adapter", "controller", "presenter", "gateway", "repository_impl", "infrastructure"],
        "framework": ["api", "router", "views", "handlers", "main", "app", "web", "db", "database", "external"],
    }

    def analyze_layers(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
        """Detect layer organization and check dependency rule violations."""
        findings: list[ArchitectureFinding] = []
        module_name = code_ast.metadata.get("filename", "").lower()
        module_layer = self._classify_module_layer(module_name)
        if not module_layer:
            return findings

        for imp in code_ast.imports:
            import_name = imp.module.lower()
            imported_layer = self._classify_import_layer(import_name)
            if imported_layer:
                layer_order = {"entity": 0, "use_case": 1, "adapter": 2, "framework": 3}
                module_layer_rank = layer_order.get(module_layer, 0)
                imported_layer_rank = layer_order.get(imported_layer, 0)
                if imported_layer_rank > module_layer_rank:
                    findings.append(ArchitectureFinding(
                        category="clean_architecture",
                        severity=ArchitectureSeverity.HIGH,
                        description=(
                            f"Dependency rule violation: '{module_name}' ({module_layer} layer) "
                            f"imports '{imp.module}' ({imported_layer} layer)"
                        ),
                        recommendation=(
                            f"'{module_layer}' layer must not depend on '{imported_layer}' layer. "
                            "Dependencies must point inward."
                        ),
                        line_number=1,
                        confidence=0.7,
                        pattern="dependency_rule",
                        examples=[f"{module_layer} -> {imported_layer} (should point inward)"],
                    ))
        return findings

    def _classify_module_layer(self, module_name: str) -> Optional[str]:
        for layer, keywords in self.LAYER_KEYWORDS.items():
            for kw in keywords:
                if kw in module_name:
                    return layer
        return None

    def _classify_import_layer(self, import_name: str) -> Optional[str]:
        for layer, keywords in self.LAYER_KEYWORDS.items():
            for kw in keywords:
                if kw in import_name:
                    return layer
        return None

    def analyze_entity_purity(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
        """Check if Entities (domain layer) are pure -- no framework dependencies."""
        findings: list[ArchitectureFinding] = []
        module_name = code_ast.metadata.get("filename", "").lower()
        if "entity" not in module_name and "domain" not in module_name:
            return findings

        framework_imports = [
            "fastapi", "django", "flask", "sqlalchemy", "pydantic",
            "redis", "requests", "httpx", "kafka", "celery",
        ]
        for imp in code_ast.imports:
            for fw in framework_imports:
                if fw in imp.module.lower():
                    findings.append(ArchitectureFinding(
                        category="clean_architecture",
                        severity=ArchitectureSeverity.MEDIUM,
                        description=(
                            f"Domain/entity module '{module_name}' imports framework "
                            f"dependency '{imp.module}'"
                        ),
                        recommendation=(
                            "Entities must be pure Python with no framework dependencies. "
                            "Move framework concerns to the adapter layer."
                        ),
                        line_number=1,
                        confidence=0.8,
                        pattern="entity_purity",
                    ))
                    break
        return findings

    def analyze(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
        findings: list[ArchitectureFinding] = []
        findings.extend(self.analyze_layers(code_ast))
        findings.extend(self.analyze_entity_purity(code_ast))
        return findings


class DDDAnalyzer:
    """
    Domain-Driven Design pattern analysis.

    - Bounded Contexts: clear module boundaries
    - Entities: objects with identity (id, uuid)
    - Value Objects: immutable objects without identity
    - Aggregates: root entity + related entities
    - Domain Events: events emitted by aggregates
    - Repositories: persistence abstraction
    - Anti-Corruption Layer: translation between contexts
    """

    def analyze_entities(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
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

    def analyze_repositories(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
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

    def analyze_domain_events(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
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

    def analyze(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
        findings: list[ArchitectureFinding] = []
        findings.extend(self.analyze_entities(code_ast))
        findings.extend(self.analyze_repositories(code_ast))
        findings.extend(self.analyze_domain_events(code_ast))
        return findings


class SOLIDAnalyzer:
    """
    SOLID Principle analysis.

    - S: Single Responsibility -- classes should have one reason to change
    - O: Open/Closed -- open for extension, closed for modification
    - L: Liskov Substitution -- subtypes must be substitutable for base types
    - I: Interface Segregation -- many specific interfaces > one general
    - D: Dependency Inversion -- depend on abstractions, not concretions
    """

    def analyze_single_responsibility(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
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

            # Check for mixed data and logic
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

    def analyze_open_closed(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
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

    def analyze_liskov_substitution(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
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

        # Check for inheritance that weakens preconditions
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

    def analyze_interface_segregation(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
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

    def analyze_dependency_inversion(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
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

    def analyze(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
        findings: list[ArchitectureFinding] = []
        findings.extend(self.analyze_single_responsibility(code_ast))
        findings.extend(self.analyze_open_closed(code_ast))
        findings.extend(self.analyze_liskov_substitution(code_ast))
        findings.extend(self.analyze_interface_segregation(code_ast))
        findings.extend(self.analyze_dependency_inversion(code_ast))
        return findings


class CQRSAnalyzer:
    """
    CQRS (Command Query Responsibility Segregation) analysis.

    - Commands: write operations that change state (return void)
    - Queries: read operations that return data (no side effects)
    - Separate read/write models for complex domains
    """

    def analyze_commands(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
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

    def analyze_queries(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
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

        # Check for function naming indicating query/command separation
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

    def analyze(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
        findings: list[ArchitectureFinding] = []
        findings.extend(self.analyze_commands(code_ast))
        findings.extend(self.analyze_queries(code_ast))
        return findings


class EventSourcingAnalyzer:
    """
    Event Sourcing pattern analysis.

    - Event Store: append-only log of events
    - Replay: rebuild state from events
    - Projection: read models built from events
    - Snapshot: periodic state snapshots for performance
    """

    def analyze_event_store(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
        """Detect Event Store pattern."""
        findings: list[ArchitectureFinding] = []
        raw = "\n".join(code_ast.raw_lines)

        event_store_signals = [
            "event_store", "eventstore", "append", "event_stream",
            "event_repository", "event_log", "journal",
        ]
        for signal in event_store_signals:
            if signal in raw.lower():
                findings.append(ArchitectureFinding(
                    category="event_sourcing",
                    severity=ArchitectureSeverity.INFO,
                    description=f"Event Store pattern detected (signal: '{signal}')",
                    recommendation=(
                        "Event Store is an append-only log. Events are never modified or deleted. "
                        "Use snapshots for performance optimization on long streams."
                    ),
                    line_number=1,
                    confidence=0.8,
                    pattern="event_store",
                ))
                break

        for cls in code_ast.classes:
            cls_name = cls.name.lower()
            if "event" in cls_name and ("store" in cls_name or "repository" in cls_name or "log" in cls_name):
                findings.append(ArchitectureFinding(
                    category="event_sourcing",
                    severity=ArchitectureSeverity.INFO,
                    description=f"Event Store class detected: '{cls.name}'",
                    recommendation=(
                        "Event Store implementation should handle: append (write), "
                        "read_stream (get events by aggregate), and snapshot management."
                    ),
                    line_number=cls.lineno,
                    confidence=0.85,
                    pattern="event_store",
                ))
        return findings

    def analyze_projections(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
        """Detect Projection patterns."""
        findings: list[ArchitectureFinding] = []
        for cls in code_ast.classes:
            cls_name = cls.name.lower()
            if "projection" in cls_name or "projector" in cls_name or "read_model" in cls_name:
                has_when = any(m.name == "when" or m.name.startswith("project") for m in cls.methods)
                if has_when:
                    findings.append(ArchitectureFinding(
                        category="event_sourcing",
                        severity=ArchitectureSeverity.INFO,
                        description=f"Projection detected: '{cls.name}'",
                        recommendation=(
                            "Projections build read models from events. Each projection "
                            "handles specific event types. Rebuild from scratch by replaying all events."
                        ),
                        line_number=cls.lineno,
                        confidence=0.85,
                        pattern="projection",
                    ))
        return findings

    def analyze(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
        findings: list[ArchitectureFinding] = []
        findings.extend(self.analyze_event_store(code_ast))
        findings.extend(self.analyze_projections(code_ast))
        return findings


class ArchitecturePatternAnalyzer:
    """
    Master analyzer that coordinates all architecture pattern analyses.
    """

    def __init__(self):
        self.clean_arch = CleanArchitectureAnalyzer()
        self.ddd = DDDAnalyzer()
        self.solid = SOLIDAnalyzer()
        self.cqrs = CQRSAnalyzer()
        self.event_sourcing = EventSourcingAnalyzer()

    def analyze(self, code_ast: CodeAST) -> dict[str, list[ArchitectureFinding]]:
        """Run all architecture pattern analyses."""
        return {
            "clean_architecture": self.clean_arch.analyze(code_ast),
            "ddd": self.ddd.analyze(code_ast),
            "solid": self.solid.analyze(code_ast),
            "cqrs": self.cqrs.analyze(code_ast),
            "event_sourcing": self.event_sourcing.analyze(code_ast),
        }

    def analyze_all(self, code_ast: CodeAST) -> list[ArchitectureFinding]:
        """Get all findings as a flat list."""
        results = self.analyze(code_ast)
        all_findings: list[ArchitectureFinding] = []
        for category_findings in results.values():
            all_findings.extend(category_findings)
        return all_findings


architecture_pattern_analyzer = ArchitecturePatternAnalyzer()
