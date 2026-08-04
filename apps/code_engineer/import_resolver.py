"""
Import Resolver
================

Resolves Python imports to determine if they're stdlib, third-party, or local.
"""

import sys
from pathlib import Path

from apps.code_engineer.dependency_models import DependencyType


class ImportResolver:
    """Resolves Python imports to determine their type and local path."""

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
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
        source_path = Path(source_file)
        source_dir = source_path.parent

        local_path = source_dir / f"{module_name.replace('.', '/')}.py"
        if local_path.exists():
            try:
                return str(local_path.relative_to(self.repo_path))
            except ValueError:
                return str(local_path)

        local_pkg = source_dir / module_name.replace(".", "/") / "__init__.py"
        if local_pkg.exists():
            try:
                return str(local_pkg.relative_to(self.repo_path))
            except ValueError:
                return str(local_pkg)

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
        clean_name = module_name.lstrip(".")
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

        top_level = clean_name.split(".")[0]
        if top_level in self._stdlib_modules:
            return DependencyType.STDLIB

        return DependencyType.THIRD_PARTY
