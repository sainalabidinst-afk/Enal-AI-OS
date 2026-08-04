"""
Architecture Models
====================

Data models for the architecture reader module.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ProjectType(str, Enum):
    UNKNOWN = "unknown"
    FASTAPI = "fastapi"
    DJANGO = "django"
    FLASK = "flask"
    CLI = "cli"
    LIBRARY = "library"
    PACKAGE = "package"
    FULLSTACK = "fullstack"
    DATA_SCIENCE = "data_science"
    SCRIPT = "script"


class ModuleType(str, Enum):
    ENTRY_POINT = "entry_point"
    API_MODULE = "api_module"
    CORE_MODULE = "core_module"
    MODEL_MODULE = "model_module"
    SERVICE_MODULE = "service_module"
    UTILITY_MODULE = "utility_module"
    TEST_MODULE = "test_module"
    CONFIG_MODULE = "config_module"
    CLI_MODULE = "cli_module"
    UNKNOWN = "unknown"


@dataclass
class ModuleInfo:
    """Information about a Python module."""
    name: str
    path: str
    module_type: ModuleType = ModuleType.UNKNOWN
    is_package: bool = False
    has_tests: bool = False
    imports: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)
    decorators: list[str] = field(default_factory=list)
    lines_of_code: int = 0
    docstring: Optional[str] = None


@dataclass
class ArchitectureSummary:
    """Complete architecture analysis of a repository."""
    project_type: ProjectType = ProjectType.UNKNOWN
    project_name: str = ""
    python_version: str = ""
    total_files: int = 0
    total_lines: int = 0
    modules: list[ModuleInfo] = field(default_factory=list)
    entry_points: list[str] = field(default_factory=list)
    test_modules: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)
    api_routes: list[dict] = field(default_factory=list)
    has_docker: bool = False
    has_ci_cd: bool = False
    has_docs: bool = False
    has_config: bool = False
    has_tests: bool = False
    dependency_files: list[str] = field(default_factory=list)
    directory_tree: str = ""
    missing_init_files: list[str] = field(default_factory=list)
