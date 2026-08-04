"""
Dependency Models
===================

Data models for the dependency graph module.
"""

from dataclasses import dataclass, field
from typing import Any


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
    is_from_import: bool = False
    imported_names: list[str] = field(default_factory=list)
    line_number: int = 0


@dataclass
class ModuleDependencies:
    """Dependency information for a single module."""
    module_path: str
    dependencies: list[Dependency] = field(default_factory=list)
    dependents: list[str] = field(default_factory=list)
    is_circular: bool = False
    circular_with: list[str] = field(default_factory=list)
    impact_score: float = 0.0
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
    orphan_modules: list[str] = field(default_factory=list)
