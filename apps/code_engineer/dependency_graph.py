"""
Dependency Graph
==================

Full import resolution and dependency mapping for Python repositories.
Tracks cross-file dependencies, detects circular imports, computes impact scores.

Features:
- Python import resolver (stdlib, third-party, local)
- Cross-file dependency mapping
- Circular dependency detection
- Dependency impact scoring
- Third-party vs local dependency classification
"""

import ast
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class DependencyType:
    STDLIB = "stdlib"
    THIRD_PARTY = "third_party"
    LOCAL = "local"
    UNKNOWN = "unknown"


@dataclass
class Dependency:
    """A single dependency edge between modules."""
    source: str          # Source module path (relative)
    target: str          # Target module/package name
    dependency_type: str = DependencyType.UNKNOWN
    alias: str = ""
    is_from_import: bool = False
    imported_names: list[str] = field(default_factory=list)
    line_number: int = 0


@dataclass
class ModuleDependencies:
    """Dependency information for a single module."""
    module_path: str
    dependencies: list[Dependency] = field(default_factory=list)
    dependents: list[str] = field(default_factory=list)  # modules that depend on this
    is_circular: bool = False
    circular_with: list[str] = field(default_factory=list)
    impact_score: float = 0.0  # 0.0 - 1.0, how many modules would be affected
    dependency_count: int = 0
    dependent_count: int = 0


@dataclass
class DependencyGraphSummary:
    """Complete dependency analysis of a repository."""
    modules: dict[str, ModuleDependencies] = field(default_factory=dict)
    circular_dependencies: list[list[str]] = field(default_factory=list)
    total_modules: int = 0
    total_dependencies: int = 0
    total_stdlib_imports: int = 0
    total_third_party_imports: int = 0
    total_local_imports: int = 0
    max_depth: int = 0
    avg_dependencies: float = 0.0
    avg_dependents: float = 0.0
    most_dependent_modules: list[tuple[str, int]] = field(default_factory=list)
    orphan_modules: list[str] = field(default_factory=list)  # no deps, no dependents


class ImportResolver:
    """Resolves Python imports to determine if they're stdlib, third-party, or local."""

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        # Known stdlib modules
        self._stdlib_modules: set[str] = set(sys.stdlib_module_names) if hasattr(sys, 'stdlib_module_names') else {
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

    def resolve(self, module_name: str, source_file: str) -> str:
        """Resolve an import to determine its type and local path if applicable."""
        # Check if it's a direct local module
        source_path = Path(source_file)
        source_dir = source_path.parent

        # Try resolving relative to source file's directory
        local_path = source_dir / f"{module_name.replace('.', '/')}.py"
        if local_path.exists():
            try:
                return str(local_path.relative_to(self.repo_path))
            except ValueError:
                return str(local_path)

        # Try resolving as package __init__
        local_pkg = source_dir / module_name.replace(".", "/") / "__init__.py"
        if local_pkg.exists():
            try:
                return str(local_pkg.relative_to(self.repo_path))
            except ValueError:
                return str(local_pkg)

        # Check repo root
        root_path = self.repo_path / f"{module_name.replace('.', '/')}.py"
        if root_path.exists():
            try:
                return str(root_path.relative_to(self.repo_path))
            except ValueError:
                return str(root_path)

        root_pkg = self.repo_path / module_name.replace(".", "/") / "__init__.py"
        if root_pkg.exists():
            try:
                return str(root_pkg.relative_to(self.repo_path))
            except ValueError:
                return str(root_pkg)

        return module_name

    def classify(self, module_name: str, source_file: str) -> str:
        """Classify an import as stdlib, third-party, or local."""
        # Remove leading local imports (.)
        clean_name = module_name.lstrip(".")

        # Check if local
        source_path = Path(source_file)
        source_dir = source_path.parent

        local_path = source_dir / f"{clean_name.replace('.', '/')}.py"
        if local_path.exists():
            return DependencyType.LOCAL

        local_pkg = source_dir / clean_name.replace(".", "/") / "__init__.py"
        if local_pkg.exists():
            return DependencyType.LOCAL

        root_path = self.repo_path / f"{clean_name.replace('.', '/')}.py"
        if root_path.exists():
            return DependencyType.LOCAL

        root_pkg = self.repo_path / clean_name.replace(".", "/") / "__init__.py"
        if root_pkg.exists():
            return DependencyType.LOCAL

        # Check if stdlib
        top_level = clean_name.split(".")[0]
        if top_level in self._stdlib_modules:
            return DependencyType.STDLIB

        # Otherwise it's third-party
        return DependencyType.THIRD_PARTY


class DependencyGraphBuilder:
    """Builds a complete dependency graph from repository files."""

    def __init__(self, repo_path: str | Path):
        self.repo_path = Path(repo_path)
        self.resolver = ImportResolver(self.repo_path)
        self._modules: dict[str, ModuleDependencies] = {}
        self._file_module_map: dict[str, str] = {}

    async def build(self) -> DependencyGraphSummary:
        """Build the dependency graph and return summary."""
        # Scan all Python files
        python_files = sorted(self.repo_path.rglob("*.py"))

        # First pass: build module map
        for py_file in python_files:
            try:
                relative = str(py_file.relative_to(self.repo_path))
                self._file_module_map[relative] = relative
                if relative not in self._modules:
                    self._modules[relative] = ModuleDependencies(module_path=relative)
            except ValueError:
                continue

        # Second pass: extract dependencies
        for py_file in python_files:
            try:
                relative = str(py_file.relative_to(self.repo_path))
                deps = await self._extract_dependencies(py_file, relative)
                if relative in self._modules:
                    self._modules[relative].dependencies = deps
            except ValueError:
                continue
            except Exception as e:
                logger.warning(f"Error extracting deps from {py_file}: {e}")

        # Build reverse dependencies (dependents)
        self._build_dependents()

        # Detect circular dependencies
        cycles = self._detect_circular_dependencies()

        # Compute impact scores
        self._compute_impact_scores()

        # Compute statistics
        return self._create_summary(cycles)

    async def _extract_dependencies(self, py_file: Path, relative: str) -> list[Dependency]:
        """Extract all import dependencies from a Python file."""
        deps: list[Dependency] = []
        try:
            content = py_file.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(py_file))
        except (SyntaxError, Exception):
            return deps

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    dep_type = self.resolver.classify(alias.name, str(py_file))
                    resolved = self.resolver.resolve(alias.name, str(py_file))
                    deps.append(Dependency(
                        source=relative,
                        target=resolved,
                        dependency_type=dep_type,
                        alias=alias.asname or "",
                        line_number=node.lineno,
                    ))
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        full_name = f"{node.module}.{alias.name}"
                        dep_type = self.resolver.classify(full_name, str(py_file))
                        resolved = self.resolver.resolve(node.module, str(py_file))
                        deps.append(Dependency(
                            source=relative,
                            target=resolved,
                            dependency_type=dep_type,
                            alias=alias.asname or "",
                            is_from_import=True,
                            imported_names=[alias.name],
                            line_number=node.lineno,
                        ))

        return deps

    def _build_dependents(self):
        """Build reverse dependency map (who depends on whom)."""
        for mod_path, mod_info in self._modules.items():
            for dep in mod_info.dependencies:
                if dep.dependency_type == DependencyType.LOCAL:
                    target = dep.target
                    if target in self._modules:
                        if mod_path not in self._modules[target].dependents:
                            self._modules[target].dependents.append(mod_path)

    def _detect_circular_dependencies(self) -> list[list[str]]:
        """Detect circular dependencies using DFS."""
        cycles: list[list[str]] = []
        visited: set[str] = set()
        rec_stack: set[str] = set()
        path: list[str] = []

        def dfs(module: str):
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
                            # Found cycle
                            cycle_start = path.index(target)
                            cycle = path[cycle_start:] + [target]
                            if cycle not in cycles:
                                cycles.append(cycle)
                                # Mark modules as circular
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

    def _compute_impact_scores(self):
        """Compute dependency impact scores for each module."""
        total = len(self._modules)
        if total == 0:
            return

        for mod_path, mod_info in self._modules.items():
            # Count direct dependencies
            local_deps = sum(1 for d in mod_info.dependencies if d.dependency_type == DependencyType.LOCAL)
            mod_info.dependency_count = local_deps

            # Count direct dependents
            mod_info.dependent_count = len(mod_info.dependents)

            # Impact score: proportion of modules that depend on this (directly or indirectly)
            affected = set()
            queue = list(mod_info.dependents)
            while queue:
                current = queue.pop(0)
                if current in affected:
                    continue
                affected.add(current)
                # Add transitives
                if current in self._modules:
                    for dep_mod in self._modules[current].dependents:
                        if dep_mod not in affected and dep_mod != mod_path:
                            queue.append(dep_mod)

            mod_info.impact_score = len(affected) / total if total > 0 else 0.0

    def _create_summary(self, cycles: list[list[str]]) -> DependencyGraphSummary:
        """Create summary from analyzed data."""
        total_deps = sum(len(m.dependencies) for m in self._modules.values())
        stdlib = sum(
            sum(1 for d in m.dependencies if d.dependency_type == DependencyType.STDLIB)
            for m in self._modules.values()
        )
        third_party = sum(
            sum(1 for d in m.dependencies if d.dependency_type == DependencyType.THIRD_PARTY)
            for m in self._modules.values()
        )
        local = sum(
            sum(1 for d in m.dependencies if d.dependency_type == DependencyType.LOCAL)
            for m in self._modules.values()
        )

        # Most dependent modules
        dependent_counts = [
            (m.module_path, m.dependent_count) for m in self._modules.values() if m.dependent_count > 0
        ]
        dependent_counts.sort(key=lambda x: x[1], reverse=True)
        most_dependent = dependent_counts[:10]

        # Orphan modules (no deps, no dependents)
        orphans = [
            m.module_path for m in self._modules.values()
            if m.dependency_count == 0 and m.dependent_count == 0
            and not m.module_path.startswith("__init__")
            and not m.module_path.startswith("_")
        ]

        # Max dependency depth (approximate)
        max_depth = 0
        for mod_path in self._modules:
            depth = self._compute_depth(mod_path, set())
            max_depth = max(max_depth, depth)

        return DependencyGraphSummary(
            modules=self._modules,
            circular_dependencies=cycles,
            total_modules=len(self._modules),
            total_dependencies=total_deps,
            total_stdlib_imports=stdlib,
            total_third_party_imports=third_party,
            total_local_imports=local,
            max_depth=max_depth,
            avg_dependencies=total_deps / len(self._modules) if self._modules else 0,
            avg_dependents=sum(m.dependent_count for m in self._modules.values()) / len(self._modules) if self._modules else 0,
            most_dependent_modules=most_dependent,
            orphan_modules=orphans,
        )

    def _compute_depth(self, module: str, visited: set[str]) -> int:
        """Compute depth from this module to leaf dependencies."""
        if module in visited or module not in self._modules:
            return 0
        visited.add(module)

        max_child_depth = 0
        for dep in self._modules[module].dependencies:
            if dep.dependency_type == DependencyType.LOCAL and dep.target in self._modules:
                child_depth = self._compute_depth(dep.target, visited)
                max_child_depth = max(max_child_depth, child_depth)

        return max_child_depth + 1

    def get_impact_chain(self, module_path: str) -> list[str]:
        """Get all modules affected by a change to the given module."""
        affected: list[str] = []
        if module_path not in self._modules:
            return affected

        queue = list(self._modules[module_path].dependents)
        visited: set[str] = set()

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            affected.append(current)
            if current in self._modules:
                for dep_mod in self._modules[current].dependents:
                    if dep_mod not in visited:
                        queue.append(dep_mod)

        return affected


def find_circular_imports(repo_path: str | Path) -> list[list[str]]:
    """Quick function to find circular imports in a repository."""
    from apps.code_engineer.architecture_reader import ArchitectureReader
    import asyncio

    builder = DependencyGraphBuilder(repo_path)
    summary = asyncio.run(builder.build())
    return summary.circular_dependencies

