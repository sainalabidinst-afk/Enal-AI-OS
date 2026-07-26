"""
Architecture Reader
=====================

Multi-file repository structure analysis.
Detects project architecture, frameworks, entry points, module organization.

Features:
- Module tree builder (Python packages, modules)
- Framework detection (FastAPI, Django, Flask, CLI tools)
- Entry point detection (main.py, app.py, CLI entrypoints)
- Test directory detection
- Static resource detection
- Project type classification
"""

import ast
import logging
import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


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
    api_routes: list[dict[str, Any]] = field(default_factory=list)
    has_docker: bool = False
    has_ci_cd: bool = False
    has_docs: bool = False
    has_config: bool = False
    has_tests: bool = False
    dependency_files: list[str] = field(default_factory=list)
    directory_tree: str = ""
    missing_init_files: list[str] = field(default_factory=list)


class ArchitectureReader:
    """Reads and analyzes repository architecture."""

    # Framework signatures
    FRAMEWORK_SIGNATURES: dict[str, list[str]] = {
        "fastapi": ["fastapi", "FastAPI", "APIRouter"],
        "django": ["django", "DJANGO_SETTINGS_MODULE", "django.core"],
        "flask": ["flask", "Flask", "flask_"],
        "click": ["click", "click.", "click.group"],
        "typer": ["typer", "typer."],
        "pydantic": ["pydantic", "BaseModel"],
        "sqlalchemy": ["sqlalchemy", "SQLAlchemy", "declarative_base"],
        "tortoise": ["tortoise", "Tortoise"],
        "redis": ["redis", "Redis"],
        "celery": ["celery", "Celery"],
        "pytest": ["pytest", "pytest_"],
        "asyncio": ["asyncio", "async def"],
    }

    # Entry point patterns
    ENTRY_POINT_PATTERNS: list[str] = [
        "main.py", "app.py", "cli.py", "run.py",
        "server.py", "manage.py", "wsgi.py", "asgi.py",
        "__main__.py",
    ]

    def __init__(self, repo_path: str | Path):
        self.repo_path = Path(repo_path)
        self._modules: list[ModuleInfo] = []
        self._entry_points: list[str] = []
        self._test_modules: list[str] = []
        self._frameworks_found: list[str] = []
        self._api_routes: list[dict[str, Any]] = []
        self._dependency_files: list[str] = []
        self._missing_init: list[str] = []
        self._total_files = 0
        self._total_lines = 0

    async def read(self) -> ArchitectureSummary:
        """Analyze the repository and return architecture summary."""
        if not self.repo_path.exists():
            raise FileNotFoundError(f"Repository path not found: {self.repo_path}")

        # Scan all Python files recursively
        python_files = list(self.repo_path.rglob("*.py"))
        self._total_files = len(python_files)

        # Check for project metadata
        project_name = self._detect_project_name()

        # Analyze each Python file
        module_tree_lines = []
        for py_file in sorted(python_files):
            try:
                relative = py_file.relative_to(self.repo_path)
                depth = len(relative.parts) - 1
                indent = "  " * depth
                module_tree_lines.append(f"{indent}{'📄 ' if not py_file.name == '__init__.py' else '📦 '}{py_file.name}")

                module_info = await self._analyze_file(py_file, relative)
                if module_info:
                    self._modules.append(module_info)

                    # Detect entry points
                    if py_file.name in self.ENTRY_POINT_PATTERNS:
                        self._entry_points.append(str(relative))
                        module_info.module_type = ModuleType.ENTRY_POINT

                    # Detect test modules
                    if "test" in py_file.name.lower() or "test" in relative.parts:
                        self._test_modules.append(str(relative))
                        module_info.module_type = ModuleType.TEST_MODULE

            except Exception as e:
                logger.warning(f"Error analyzing {py_file}: {e}")

        # Detect framework
        self._frameworks_found = self._detect_frameworks()

        # Check for __init__.py files
        self._missing_init = self._check_missing_init(python_files)

        # Check infrastructure files
        has_docker = bool(list(self.repo_path.glob("Dockerfile")) or list(self.repo_path.glob("docker-compose*")))
        has_ci_cd = bool(list(self.repo_path.glob(".github/workflows/*")) or list(self.repo_path.glob(".gitlab-ci*")))
        has_docs = bool((self.repo_path / "docs").exists() or (self.repo_path / "README.md").exists())
        has_config = bool(list(self.repo_path.glob("pyproject.toml")) or list(self.repo_path.glob("setup.py")) or list(self.repo_path.glob("setup.cfg")))
        has_tests = bool(self._test_modules) or (self.repo_path / "tests").exists()

        # Detect dependency files
        for dep_file in ["pyproject.toml", "setup.py", "setup.cfg", "requirements.txt", "Pipfile", "poetry.lock"]:
            if (self.repo_path / dep_file).exists():
                self._dependency_files.append(dep_file)

        # Detect project type
        project_type = self._classify_project_type()

        directory_tree = "\n".join(module_tree_lines)

        return ArchitectureSummary(
            project_type=project_type,
            project_name=project_name,
            total_files=self._total_files,
            total_lines=self._total_lines,
            modules=self._modules,
            entry_points=self._entry_points,
            test_modules=self._test_modules,
            frameworks=self._frameworks_found,
            api_routes=self._api_routes,
            has_docker=has_docker,
            has_ci_cd=bool(has_ci_cd),
            has_docs=has_docs,
            has_config=has_config,
            has_tests=has_tests,
            dependency_files=self._dependency_files,
            directory_tree=directory_tree,
            missing_init_files=self._missing_init,
        )

    async def _analyze_file(self, py_file: Path, relative: Path) -> Optional[ModuleInfo]:
        """Analyze a single Python file."""
        try:
            content = py_file.read_text(encoding="utf-8")
            lines = content.splitlines()
            loc = len(lines)
            self._total_lines += loc

            # Parse AST
            tree = ast.parse(content, filename=str(py_file))

            imports: list[str] = []
            classes: list[str] = []
            functions: list[str] = []
            decorators: list[str] = []
            docstring = None

            if isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant):
                docstring = ast.get_docstring(tree)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                    for dec in node.decorator_list:
                        dec_name = self._extract_decorator_name(dec)
                        if dec_name:
                            decorators.append(dec_name)
                    # Detect API routes from decorators
                    for dec in node.decorator_list:
                        dec_name = self._extract_decorator_name(dec)
                        if dec_name and dec_name in ("router", "api_router", "app"):
                            self._api_routes.append({
                                "module": str(relative),
                                "class": node.name,
                                "decorator": dec_name,
                                "line": node.lineno,
                            })
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                    for dec in node.decorator_list:
                        dec_name = self._extract_decorator_name(dec)
                        if dec_name:
                            decorators.append(dec_name)
                            # Detect HTTP method decorators
                            if dec_name in ("get", "post", "put", "delete", "patch", "route", "api_route"):
                                self._api_routes.append({
                                    "module": str(relative),
                                    "function": node.name,
                                    "method": dec_name,
                                    "line": node.lineno,
                                })

            name = str(relative)
            module_type = self._classify_module(name)
            is_package = py_file.name == "__init__.py"

            return ModuleInfo(
                name=name,
                path=str(py_file),
                module_type=module_type,
                is_package=is_package,
                has_tests="test" in name.lower(),
                imports=imports,
                classes=classes,
                functions=functions,
                decorators=decorators,
                lines_of_code=loc,
                docstring=docstring,
            )

        except SyntaxError:
            logger.warning(f"Syntax error in {py_file}, skipping AST analysis")
            return None
        except Exception as e:
            logger.error(f"Error analyzing {py_file}: {e}")
            return None

    def _extract_decorator_name(self, node: ast.expr) -> Optional[str]:
        """Extract decorator name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                return node.func.id
            elif isinstance(node.func, ast.Attribute):
                return node.func.attr
        return None

    def _detect_frameworks(self) -> list[str]:
        """Detect frameworks used in the project."""
        found: list[str] = []
        for framework, signatures in self.FRAMEWORK_SIGNATURES.items():
            for sig in signatures:
                if any(sig in " ".join(m.imports) for m in self._modules if m.imports):
                    if framework not in found:
                        found.append(framework)
                    break
        return found

    def _classify_project_type(self) -> ProjectType:
        """Classify the overall project type."""
        if "fastapi" in self._frameworks_found:
            return ProjectType.FASTAPI
        if "django" in self._frameworks_found:
            return ProjectType.DJANGO
        if "flask" in self._frameworks_found:
            return ProjectType.FLASK
        if "click" in self._frameworks_found or "typer" in self._frameworks_found:
            return ProjectType.CLI
        if self._modules and all(m.is_package for m in self._modules[:3]):
            return ProjectType.PACKAGE
        if self._total_files > 10:
            return ProjectType.FULLSTACK
        if self._total_files > 1:
            return ProjectType.LIBRARY
        return ProjectType.SCRIPT

    def _classify_module(self, name: str) -> ModuleType:
        """Classify a module based on its path."""
        name_lower = name.lower()
        if "api" in name_lower or "route" in name_lower or "endpoint" in name_lower:
            return ModuleType.API_MODULE
        if "core" in name_lower or "kernel" in name_lower or "engine" in name_lower:
            return ModuleType.CORE_MODULE
        if "model" in name_lower or "schema" in name_lower or "entity" in name_lower:
            return ModuleType.MODEL_MODULE
        if "service" in name_lower or "use_case" in name_lower or "handler" in name_lower:
            return ModuleType.SERVICE_MODULE
        if "util" in name_lower or "helper" in name_lower or "common" in name_lower:
            return ModuleType.UTILITY_MODULE
        if "config" in name_lower or "setting" in name_lower:
            return ModuleType.CONFIG_MODULE
        if "cli" in name_lower or "command" in name_lower:
            return ModuleType.CLI_MODULE
        if "test" in name_lower:
            return ModuleType.TEST_MODULE
        if name.endswith("__main__.py") or name.startswith("main"):
            return ModuleType.ENTRY_POINT
        return ModuleType.UNKNOWN

    def _detect_project_name(self) -> str:
        """Detect project name from pyproject.toml or setup.py."""
        pyproject = self.repo_path / "pyproject.toml"
        if pyproject.exists():
            try:
                content = pyproject.read_text(encoding="utf-8")
                import tomllib
                data = tomllib.loads(content)
                if "project" in data and "name" in data["project"]:
                    return data["project"]["name"]
            except (ImportError, tomllib.TOMLDecodeError):
                # Python 3.11+ tomllib or fallback
                try:
                    import tomli as tomllib
                except ImportError:
                    pass
                try:
                    import toml
                    data = toml.loads(content)
                    if "project" in data and "name" in data["project"]:
                        return data["project"]["name"]
                except ImportError:
                    pass

        # Fallback: use directory name
        return self.repo_path.name

    def _check_missing_init(self, python_files: list[Path]) -> list[str]:
        """Check for missing __init__.py in Python package directories."""
        missing = []
        dirs_with_py = set()
        for pf in python_files:
            parent = pf.parent
            if parent != self.repo_path:
                dirs_with_py.add(parent)

        for d in dirs_with_py:
            if not (d / "__init__.py").exists():
                try:
                    rel = d.relative_to(self.repo_path)
                    missing.append(str(rel))
                except ValueError:
                    pass
        return missing

    def get_import_context(self, module_name: str) -> dict[str, Any]:
        """Get import context for a specific module."""
        for m in self._modules:
            if m.name == module_name or m.name.endswith(f"/{module_name}.py"):
                return {
                    "name": m.name,
                    "imports": m.imports,
                    "classes": m.classes,
                    "functions": m.functions,
                    "module_type": m.module_type.value,
                }
        return {}


# Singleton instance
architecture_reader_cache: dict[str, ArchitectureSummary] = {}


async def read_architecture(repo_path: str | Path) -> ArchitectureSummary:
    """Read and cache architecture summary for a repository."""
    repo_path = str(repo_path)
    if repo_path in architecture_reader_cache:
        return architecture_reader_cache[repo_path]

    reader = ArchitectureReader(repo_path)
    summary = await reader.read()
    architecture_reader_cache[repo_path] = summary
    return summary


def invalidate_cache(repo_path: str | None = None):
    """Invalidate architecture cache."""
    global architecture_reader_cache
    if repo_path:
        architecture_reader_cache.pop(str(repo_path), None)
    else:
        architecture_reader_cache.clear()


# Default singleton for backward compatibility
architecture_reader = None  # Lazy-initialized when needed

