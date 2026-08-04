"""
Clean Architecture Analysis
=============================

Clean Architecture layer analysis and entity purity checks.
"""

from typing import Optional

from apps.code_engineer.architecture_models import ModuleInfo
from apps.code_engineer.architecture_patterns import ArchitectureFinding, ArchitectureSeverity


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

    def analyze_layers(self, code_ast) -> list[ArchitectureFinding]:
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

    def analyze_entity_purity(self, code_ast) -> list[ArchitectureFinding]:
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

    def analyze(self, code_ast) -> list[ArchitectureFinding]:
        findings: list[ArchitectureFinding] = []
        findings.extend(self.analyze_layers(code_ast))
        findings.extend(self.analyze_entity_purity(code_ast))
        return findings
