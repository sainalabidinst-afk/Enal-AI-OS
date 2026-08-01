"""
System Architect — Dependency Graph Builder.

Builds a full import/dependency graph for a project, classifies modules into
architectural layers, detects circular dependencies, and identifies
cross-package boundary violations.

Features:
- Python import resolution (stdlib, third-party, local)
- Cross-file dependency mapping
- Circular dependency detection
- Architectural layer classification (entities / use_cases / interface_adapters / frameworks / infrastructure)
- Package boundary violation detection
- Cross-layer dependency rule enforcement (dependency direction)
"""

from __future__ import annotations

import ast
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Layer classification
# ---------------------------------------------------------------------------

class Layer:
    """Architectural layer identifiers (Clean Architecture / hexagonal)."""

    ENTITIES = "entities"
    USE_CASES = "use_cases"
    INTERFACE_ADAPTERS = "interface_adapters"
    FRAMEWORKS = "frameworks"
    INFRASTRUCTURE = "infrastructure"
    UNKNOWN = "unknown"

    # Order defines the dependency direction. Inner layers are more stable.
    ORDER = [
        ENTITIES,
        USE_CASES,
        INTERFACE_ADAPTERS,
        FRAMEWORKS,
        INFRASTRUCTURE,
        UNKNOWN,
    ]

    INNER = [ENTITIES, USE_CASES]
    OUTER = [INTERFACE_ADAPTERS, FRAMEWORKS, INFRASTRUCTURE]

    LAYER_SCORES = {
        ENTITIES: 5,
        USE_CASES: 4,
        INTERFACE_ADAPTERS: 3,
        FRAMEWORKS: 2,
        INFRASTRUCTURE: 1,
        UNKNOWN: 0,
    }

    # Directory / module name hints for layer classification.
    _HINTS: list[tuple[tuple[str, ...], str]] = [
        (("domain", "entities", "models", "model"), ENTITIES),
        (("usecases", "use_cases", "services", "application", "interactors"), USE_CASES),
        (("controllers", "presenters", "adapters", "serializers", "views", "schemas"), INTERFACE_ADAPTERS),
        (("frameworks", "web", "routes", "api", "endpoints", "cli"), FRAMEWORKS),
        (("infrastructure", "repositories", "repos", "db", "database", "persistence", "cache", "mq", "external"), INFRASTRUCTURE),
    ]

    @classmethod
    def classify_from_path(cls, module_path: str) -> str:
        """Classify a module into an architectural layer based on its path."""
        parts = module_path.replace("\\", "/").split("/")
        lowered = [p.lower() for p in parts]
        for hints, layer in cls._HINTS:
            for hint in hints:
                if any(hint in p for p in lowered):
                    return layer
        return cls.UNKNOWN

    @classmethod
    def classify_from_imports(cls, module_path: str, is_pkg: bool) -> str:
        """Classify a module based on its location within an application-typed package."""
        # Fall back to path-based classification.
        return cls.classify_from_path(module_path)


class DependencyType:
    STDLIB = "stdlib"
    THIRD_PARTY = "third_party"
    LOCAL = "local"
    UNKNOWN = "unknown"


@dataclass
class Dependency:
    """A single dependency edge between modules."""

    source: str
    target: str
    dependency_type: str = DependencyType.UNKNOWN
    alias: str = ""
    line_number: int = 0
    source_layer: str = Layer.UNKNOWN
    target_layer: str = Layer.UNKNOWN
    is_layer_violation: bool = False
    is_boundary_violation: bool = False


@dataclass
class ModuleInfo:
    """Dependency information for a single module."""

    module_path: str
    layer: str = Layer.UNKNOWN
    dependencies: list[Dependency] = field(default_factory=list)
    dependents: list[str] = field(default_factory=list)
    is_circular: bool = False
    circular_with: list[str] = field(default_factory=list)


@dataclass
class DependencyGraphSnapshot:
    """Complete dependency analysis output."""

    modules: dict[str, ModuleInfo] = field(default_factory=dict)
    circular_dependencies: list[list[str]] = field(default_factory=list)
    layer_violations: list[Dependency] = field(default_factory=list)
    boundary_violations: list[Dependency] = field(default_factory=list)
    total_modules: int = 0
    total_dependencies: int = 0
    layer_counts: dict[str, int] = field(default_factory=dict)


class ImportResolver:
    """Resolves Python imports to determine if they're stdlib, third-party, or local."""

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self._stdlib_modules: set[str] = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else {
            "os", "sys", "re", "json", "math", "datetime", "typing", "pathlib",
            "collections", "itertools", "functools", "hashlib", "random", "time",
            "uuid", "logging", "abc", "enum", "dataclasses", "io", "textwrap",
            "copy", "inspect", "types", "fractions", "decimal", "statistics",
            "asyncio", "concurrent", "multiprocessing", "threading", "subprocess",
            "socket", "ssl", "http", "urllib", "email", "base64", "binascii",
            "zlib", "gzip", "tarfile", "zipfile", "csv", "configparser",
            "argparse", "getopt", "shlex", "tempfile", "fileinput", "fnmatch",
            "glob", "linecache", "pickle", "shelve", "marshal", "dbm", "sqlite3",
            "xml", "html", "webbrowser", "tkinter", "unittest", "doctest",
            "traceback", "warnings", "contextlib", "signal", "platform",
            "errno", "ctypes", "struct", "array", "weakref", "numbers",
        }
        self.allowed_packages: set[str] = self._discover_allowed_packages()

    def _discover_allowed_packages(self) -> set[str]:
        """Discover top-level directories/packages considered local (boundary-safe)."""
        allowed: set[str] = set()
        if self.repo_path.exists():
            for child in self.repo_path.iterdir():
                if child.is_dir() and not child.name.startswith((".", "_")):
                    allowed.add(child.name)
                elif child.suffix == ".py":
                    allowed.add(child.stem)
        return allowed

    def is_allowed_local(self, module_name: str) -> bool:
        """Whether a module name refers to a local package that is boundary-safe."""
        top = module_name.split(".")[0]
        return top in self.allowed_packages

    def classify(self, module_name: str, source_file: str) -> str:
        """Classify an import as stdlib, third-party, or local."""
        clean_name = module_name.lstrip(".")
        source_path = Path(source_file)
        source_dir = source_path.parent

        candidates = [
            source_dir / f"{clean_name.replace('.', '/')}.py",
            source_dir / clean_name.replace(".", "/") / "__init__.py",
            self.repo_path / f"{clean_name.replace('.', '/')}.py",
            self.repo_path / clean_name.replace(".", "/") / "__init__.py",
        ]
        for cand in candidates:
            if cand.exists():
                return DependencyType.LOCAL

        top_level = clean_name.split(".")[0]
        if top_level in self._stdlib_modules:
            return DependencyType.STDLIB

        return DependencyType.THIRD_PARTY


class DependencyGraphBuilder:
    """Builds a complete dependency graph with layer and boundary analysis."""

    def __init__(self, repo_path: str | Path):
        self.repo_path = Path(repo_path)
        self.resolver = ImportResolver(self.repo_path)
        self._modules: dict[str, ModuleInfo] = {}

    async def build(self) -> DependencyGraphSnapshot:
        """Build the dependency graph and return snapshot."""
        python_files = sorted(self.repo_path.rglob("*.py"))

        # First pass: register modules
        for py_file in python_files:
            try:
                relative = str(py_file.relative_to(self.repo_path))
                layer = self._classify_module(py_file, relative)
                self._modules[relative] = ModuleInfo(module_path=relative, layer=layer)
            except ValueError:
                continue

        # Second pass: extract dependencies
        for py_file in python_files:
            try:
                relative = str(py_file.relative_to(self.repo_path))
                deps = self._extract_dependencies(py_file, relative)
                if relative in self._modules:
                    self._modules[relative].dependencies = deps
            except ValueError:
                continue
            except Exception as exc:  # pragma: no cover
                logger.warning("Error extracting deps from %s: %s", py_file, exc)

        self._build_dependents()
        cycles = self._detect_circular_dependencies()
        violations = self._detect_violations()

        return self._create_snapshot(cycles, violations)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _classify_module(self, py_file: Path, relative: str) -> str:
        path_layer = Layer.classify_from_path(relative)
        if path_layer != Layer.UNKNOWN:
            return path_layer
        return Layer.classify_from_imports(relative, is_pkg=py_file.name == "__init__.py")

    def _extract_dependencies(self, py_file: Path, relative: str) -> list[Dependency]:
        deps: list[Dependency] = []
        try:
            content = py_file.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(py_file))
        except SyntaxError:
            return deps
        except Exception:
            return deps

        source_layer = self._modules[relative].layer if relative in self._modules else Layer.UNKNOWN

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    deps.append(self._build_dependency(relative, alias.name, py_file, node.lineno, source_layer))
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        full_name = f"{node.module}.{alias.name}"
                        deps.append(self._build_dependency(relative, full_name, py_file, node.lineno, source_layer))
        return deps

    def _build_dependency(
        self,
        source: str,
        target_name: str,
        py_file: Path,
        lineno: int,
        source_layer: str,
    ) -> Dependency:
        dep_type = self.resolver.classify(target_name, str(py_file))
        target_layer = Layer.UNKNOWN
        if dep_type == DependencyType.LOCAL:
            target_layer = Layer.classify_from_path(target_name)

        dep = Dependency(
            source=source,
            target=target_name,
            dependency_type=dep_type,
            line_number=lineno,
            source_layer=source_layer,
            target_layer=target_layer,
        )
        # Layer violation: outer layer importing an inner-layer module is allowed;
        # inner-layer importing outer-layer is the violated direction.
        if dep_type == DependencyType.LOCAL and target_layer != Layer.UNKNOWN:
            src_idx = Layer.ORDER.index(source_layer) if source_layer in Layer.ORDER else len(Layer.ORDER)
            tgt_idx = Layer.ORDER.index(target_layer) if target_layer in Layer.ORDER else len(Layer.ORDER)
            # Violation when an inner (more stable) layer imports a more outer layer.
            if src_idx < tgt_idx:
                dep.is_layer_violation = True
            # Boundary violation: cross-package imports outside allowed root dirs.
            top = target_name.split(".")[0]
            if top not in self.resolver.allowed_packages:
                dep.is_boundary_violation = True
        return dep

    def _build_dependents(self) -> None:
        for mod_path, mod_info in self._modules.items():
            for dep in mod_info.dependencies:
                if dep.dependency_type == DependencyType.LOCAL:
                    target = dep.target
                    if target in self._modules and mod_path not in self._modules[target].dependents:
                        self._modules[target].dependents.append(mod_path)

    def _detect_circular_dependencies(self) -> list[list[str]]:
        cycles: list[list[str]] = []
        visited: set[str] = set()
        rec_stack: set[str] = set()
        path: list[str] = []

        def dfs(module: str) -> None:
            visited.add(module)
            rec_stack.add(module)
            path.append(module)
            mod_info = self._modules.get(module)
            if mod_info:
                for dep in mod_info.dependencies:
                    if dep.dependency_type != DependencyType.LOCAL:
                        continue
                    target = dep.target
                    if target in self._modules:
                        if target not in visited:
                            dfs(target)
                        elif target in rec_stack:
                            start = path.index(target)
                            cycle = path[start:] + [target]
                            if cycle not in cycles:
                                cycles.append(cycle)
                                for m in cycle:
                                    if m in self._modules:
                                        self._modules[m].is_circular = True
                                        if target not in self._modules[m].circular_with:
                                            self._modules[m].circular_with.append(target)
            path.pop()
            rec_stack.discard(module)

        for module in list(self._modules.keys()):
            if module not in visited:
                dfs(module)

        return cycles

    def _detect_violations(self) -> tuple[list[Dependency], list[Dependency]]:
        layer_violations: list[Dependency] = []
        boundary_violations: list[Dependency] = []
        for mod_info in self._modules.values():
            for dep in mod_info.dependencies:
                if dep.is_layer_violation:
                    layer_violations.append(dep)
                if dep.is_boundary_violation and dep.dependency_type in (DependencyType.THIRD_PARTY, DependencyType.UNKNOWN):
                    boundary_violations.append(dep)
        return layer_violations, boundary_violations

    def _create_snapshot(
        self,
        cycles: list[list[str]],
        violations: tuple[list[Dependency], list[Dependency]],
    ) -> DependencyGraphSnapshot:
        layer_violations, boundary_violations = violations
        total_deps = sum(len(m.dependencies) for m in self._modules.values())
        layer_counts: dict[str, int] = {}
        for mod in self._modules.values():
            layer_counts[mod.layer] = layer_counts.get(mod.layer, 0) + 1

        return DependencyGraphSnapshot(
            modules=self._modules,
            circular_dependencies=cycles,
            layer_violations=layer_violations,
            boundary_violations=boundary_violations,
            total_modules=len(self._modules),
            total_dependencies=total_deps,
            layer_counts=layer_counts,
        )


def build_graph(repo_path: str | Path) -> DependencyGraphSnapshot:
    """Synchronous convenience wrapper for building a dependency graph."""
    import asyncio

    builder = DependencyGraphBuilder(repo_path)
    return asyncio.run(builder.build())

