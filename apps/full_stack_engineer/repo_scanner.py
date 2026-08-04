"""
Repository Scanner
===================

Scans a repository directory and produces RepositoryIntelligence.
"""

import ast
import fnmatch
import json
import os
from pathlib import Path
from typing import Any

from apps.full_stack_engineer.repo_intelligence_models import (
    ARCHITECTURE_SIGNATURES,
    BUILD_SYSTEM_FILES,
    FRAMEWORK_SIGNATURES,
    IGNORE_DIRS,
    IGNORE_FILES,
    LanguageStat,
    RepositoryIntelligence,
    TEST_PATTERNS,
)


class RepositoryScanner:
    """Scans a repository directory and produces RepositoryIntelligence."""

    def __init__(self, repo_path: str | Path):
        self.repo_path = Path(repo_path).resolve()

    def scan(self) -> RepositoryIntelligence:
        """Perform a full scan of the repository."""
        if not self.repo_path.exists():
            raise FileNotFoundError(f"Repository path not found: {self.repo_path}")

        info = RepositoryIntelligence(
            project_name=self._detect_project_name(),
            project_root=str(self.repo_path),
        )

        all_files = self._collect_files()
        info.total_files = len(all_files["files"])
        info.total_lines = all_files["total_lines"]
        info.total_dirs = all_files["total_dirs"]

        info.languages = all_files["languages"]
        info.primary_language = self._determine_primary_language(info.languages)

        info.frameworks = self._detect_frameworks(all_files)
        info.frontend_frameworks = [f["name"] for f in info.frameworks if f.get("category") == "frontend"]
        info.backend_frameworks = [f["name"] for f in info.frameworks if f.get("category") == "backend"]
        info.database_frameworks = [f["name"] for f in info.frameworks if f.get("category") == "database"]
        info.testing_frameworks = [f["name"] for f in info.frameworks if f.get("category") == "testing"]

        arch_styles, arch_conf = self._detect_architecture(info)
        info.architecture_styles = arch_styles
        info.architecture_confidence = arch_conf

        info.build_system, info.build_tools = self._detect_build_system()

        info.entry_points, info.entry_type = self._detect_entry_points(all_files)

        info.dependencies, info.dependency_files, info.total_dependencies = self._collect_dependencies()

        info.has_docker = self._has_file("Dockerfile")
        info.has_docker_compose = self._has_any_file(["docker-compose.yml", "docker-compose.yaml", "docker-compose.json"])
        info.has_kubernetes = self._has_any_file(["kubernetes/", "k8s/", "K8s/", "Kubernetes/"])
        info.has_ci_cd, info.ci_cd_type = self._detect_ci_cd()
        info.has_terraform = self._has_any_file(["*.tf", "*.tfvars", "terraform/"])

        info.has_readme = self._has_any_file(["README.md", "README.rst", "README.txt", "README"])
        info.has_api_docs = self._has_any_file(["docs/", "api-docs/", "swagger/", "openapi/", "redoc/"])
        info.has_storybook = self._has_any_file([".storybook/", "storybook-static/"])
        info.documentation_paths = self._find_documentation_paths()
        info.doc_coverage = self._compute_doc_coverage(all_files)

        info.has_tests, info.test_frameworks, info.test_count_estimate = self._detect_tests(all_files)

        info.lint_configs = self._detect_lint_configs()

        info.is_monorepo, info.packages = self._detect_monorepo()

        info.summary = self._generate_summary(info)

        return info

    def _collect_files(self) -> dict[str, Any]:
        """Recursively collect all files with language stats."""
        language_stats: dict[str, LanguageStat] = {}
        all_files: list[Path] = []
        total_lines = 0
        total_dirs = 0

        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]

            for file in files:
                if file in IGNORE_FILES:
                    continue
                file_path = Path(root) / file
                rel_path = file_path.relative_to(self.repo_path)
                all_files.append(rel_path)

                ext = file_path.suffix.lower()
                lang = __import__('apps.full_stack_engineer.repo_intelligence_models', fromlist=['LANGUAGE_EXTENSIONS']).LANGUAGE_EXTENSIONS.get(ext, "Other")
                if lang not in language_stats:
                    language_stats[lang] = LanguageStat()
                language_stats[lang].files += 1

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        line_count = sum(1 for _ in f)
                    total_lines += line_count
                    language_stats[lang].lines += line_count
                except Exception:
                    pass

        for stat in language_stats.values():
            stat.percentage = (stat.lines / total_lines * 100) if total_lines > 0 else 0.0

        total_dirs = len(set(f.parent for f in all_files if str(f.parent) != "."))

        return {
            "files": all_files,
            "total_lines": total_lines,
            "total_dirs": total_dirs,
            "languages": language_stats,
        }

    def _detect_project_name(self) -> str:
        """Detect project name from various config files."""
        pyproject = self.repo_path / "pyproject.toml"
        if pyproject.exists():
            try:
                import tomllib
                data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
                return data.get("project", {}).get("name", "") or data.get("tool", {}).get("poetry", {}).get("name", "")
            except Exception:
                pass

        pkg_json = self.repo_path / "package.json"
        if pkg_json.exists():
            try:
                data = json.loads(pkg_json.read_text(encoding="utf-8"))
                return data.get("name", "")
            except Exception:
                pass

        cargo = self.repo_path / "Cargo.toml"
        if cargo.exists():
            try:
                import tomllib
                data = tomllib.loads(cargo.read_text(encoding="utf-8"))
                return data.get("package", {}).get("name", "")
            except Exception:
                pass

        gomod = self.repo_path / "go.mod"
        if gomod.exists():
            for line in gomod.read_text(encoding="utf-8").splitlines():
                if line.startswith("module "):
                    return line.replace("module ", "").strip().split("/")[-1]

        return self.repo_path.name

    def _detect_frameworks(self, all_files: dict[str, Any]) -> list[dict[str, Any]]:
        """Detect frameworks from dependency files and imports."""
        detected: dict[str, dict[str, Any]] = {}

        dep_files = self._find_dep_files()

        dep_content = ""
        for df in dep_files:
            try:
                content = (self.repo_path / df).read_text(encoding="utf-8", errors="ignore")
                dep_content += content + "\n"
            except Exception:
                pass

        source_imports = ""
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]
            for file in files:
                if file.endswith((".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs")):
                    try:
                        source_imports += (Path(root) / file).read_text(encoding="utf-8", errors="ignore") + "\n"
                    except Exception:
                        pass

        combined = dep_content + "\n" + source_imports
        combined_lower = combined.lower()

        for fw_name, signatures in FRAMEWORK_SIGNATURES.items():
            for sig in signatures:
                sig_lower = sig.lower()
                if sig_lower in combined_lower:
                    if fw_name not in detected:
                        detected[fw_name] = {"name": fw_name, "category": "unknown", "confidence": 0.7}
                    detected[fw_name]["confidence"] = min(1.0, detected[fw_name]["confidence"] + 0.1)
                    break

        frontend_keywords = ["react", "vue", "angular", "svelte", "next", "nuxt", "solid", "qwik",
                             "remix", "gatsby", "astro", "storybook", "tailwind", "mui", "chakra", "antd"]
        backend_keywords = ["fastapi", "django", "flask", "express", "nestjs", "fastify", "gin",
                            "echo", "actix", "axum", "rocket", "spring", "laravel", "rails", "hono"]
        database_keywords = ["postgresql", "mysql", "sqlite", "mongodb", "redis", "elasticsearch",
                             "sqlalchemy", "prisma", "typeorm", "drizzle", "gorm", "diesel"]
        testing_keywords = ["pytest", "jest", "vitest", "playwright", "cypress", "mocha", "chai",
                            "jasmine", "rspec", "testify"]

        for fw_name, info in detected.items():
            fw_lower = fw_name.lower()
            if any(kw in fw_lower for kw in frontend_keywords):
                info["category"] = "frontend"
            elif any(kw in fw_lower for kw in backend_keywords):
                info["category"] = "backend"
            elif any(kw in fw_lower for kw in database_keywords):
                info["category"] = "database"
            elif any(kw in fw_lower for kw in testing_keywords):
                info["category"] = "testing"
            else:
                info["category"] = "tooling"

        result = list(detected.values())
        result.sort(key=lambda x: x["confidence"], reverse=True)
        return result

    def _detect_architecture(self, info: RepositoryIntelligence) -> tuple[list[str], float]:
        """Detect architecture style from directory structure and naming."""
        dir_names: set[str] = set()
        file_names: set[str] = set()
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]
            for d in dirs:
                dir_names.add(d.lower())
            for f in files:
                file_names.add(f.lower())

        all_names = dir_names | file_names
        best_style = "Unknown"
        best_score = 0.0

        for style, rules in ARCHITECTURE_SIGNATURES.items():
            must_score = 0.0
            must_total = 0
            should_score = 0.0
            should_total = 0

            for rule in rules:
                if "must_have" in rule:
                    must_total += len(rule["must_have"])
                    for pattern in rule["must_have"]:
                        if any(pattern in name for name in all_names):
                            must_score += 1.0
                elif "should_have" in rule:
                    should_total += len(rule["should_have"])
                    for pattern in rule["should_have"]:
                        if any(pattern in name for name in all_names):
                            should_score += 1.0
                elif "must_not" in rule:
                    for pattern in rule["must_not"]:
                        if any(pattern in name for name in all_names):
                            must_score -= 1.0
                            must_total += 1
                elif "should_not_have" in rule:
                    for pattern in rule["should_not_have"]:
                        if any(pattern in name for name in all_names):
                            should_score -= 1.0
                            should_total += 1

            if must_total > 0:
                style_score = (must_score / must_total) * 0.7
            else:
                style_score = 0.0
            if should_total > 0:
                style_score += (should_score / should_total) * 0.3
            else:
                style_score += 0.3

            if style_score > best_score:
                best_score = style_score
                best_style = style

        if info.is_monorepo:
            if best_score < 0.5:
                best_style = "Monorepo"
                best_score = 0.6

        if best_style == "Clean Architecture" and best_score > 0.3:
            domain_events = any("event" in n or "domain_event" in n for n in dir_names | file_names)
            if domain_events:
                return ["Clean Architecture (DDD-inspired)"], best_score

        return [best_style], best_score

    def _detect_build_system(self) -> tuple[str, list[str]]:
        """Detect build system from config files."""
        tools: list[str] = []
        build_system = "Unknown"

        for filename, description in BUILD_SYSTEM_FILES.items():
            if (self.repo_path / filename).exists():
                tools.append(description)

        if tools:
            priority = ["pnpm", "yarn", "npm", "poetry", "pipenv", "setuptools", "cargo", "go modules",
                        "gradle", "maven", "bundler", "composer", "mix"]
            for p in priority:
                for t in tools:
                    if p in t.lower():
                        build_system = t
                        break
                if build_system != "Unknown":
                    break

        return build_system, tools

    def _detect_entry_points(self, all_files: dict[str, Any]) -> tuple[list[str], str]:
        """Detect entry points of the application."""
        entry_patterns = {
            "api_server": ["main.py", "app.py", "server.py", "api.py", "asgi.py", "wsgi.py",
                           "index.ts", "index.js", "server.ts", "server.js", "app.ts", "app.js"],
            "cli_tool": ["cli.py", "main.go", "main.rs", "cmd/", "__main__.py"],
            "web_app": ["index.html", "pages/", "app/", "src/App.tsx", "src/App.jsx", "src/app.tsx"],
            "library": ["__init__.py", "index.ts", "lib.rs"],
        }

        relative_files = {str(f) for f in all_files["files"]}
        entries: list[str] = []
        entry_type = "unknown"

        for etype, patterns in entry_patterns.items():
            for pattern in patterns:
                for rf in relative_files:
                    if rf == pattern or rf.endswith("/" + pattern):
                        entries.append(rf)
                        if entry_type == "unknown":
                            entry_type = etype
                        break

        return entries, entry_type

    def _find_dep_files(self) -> list[str]:
        """Find dependency/configuration files."""
        dep_files: list[str] = []
        for filename in BUILD_SYSTEM_FILES:
            if (self.repo_path / filename).exists():
                dep_files.append(filename)
        additional = ["requirements-dev.txt", "requirements-test.txt", "Cargo.toml"]
        for f in additional:
            if (self.repo_path / f).exists():
                dep_files.append(f)
        return dep_files

    def _collect_dependencies(self) -> tuple[dict[str, list[str]], list[str], int]:
        """Collect all dependencies from dependency files."""
        deps: dict[str, list[str]] = {}
        dep_files = self._find_dep_files()
        total = 0

        for filename in dep_files:
            filepath = self.repo_path / filename
            try:
                content = filepath.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            entries: list[str] = []

            if filename == "package.json":
                try:
                    data = json.loads(content)
                    entries.extend(data.get("dependencies", {}).keys())
                    entries.extend(data.get("devDependencies", {}).keys())
                    entries.extend(data.get("peerDependencies", {}).keys())
                except Exception:
                    pass
            elif filename == "pyproject.toml":
                import re
                matches = re.findall(r'([a-zA-Z0-9_-]+)\s*[=~><\^!]', content)
                entries.extend(matches)
            elif filename == "requirements.txt" or filename.startswith("requirements-"):
                for line in content.splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and not line.startswith("-"):
                        pkg = re.split(r'[=~><\^!@#;]', line)[0].strip()
                        if pkg:
                            entries.append(pkg)
            elif filename == "Cargo.toml":
                matches = re.findall(r'([a-zA-Z0-9_-]+)\s*=\s*["{]', content)
                entries.extend(matches)
            elif filename == "go.mod":
                for line in content.splitlines():
                    if line.strip().startswith("require") or "\t" in line:
                        parts = line.strip().split()
                        if len(parts) >= 1 and parts[0] not in ("require", ")"):
                            entries.append(parts[0].split("/")[-1])
            elif filename in ("Pipfile", "Pipfile.lock"):
                try:
                    data = json.loads(content) if filename.endswith(".lock") else {}
                    if filename == "Pipfile.lock":
                        entries.extend(data.get("default", {}).keys())
                        entries.extend(data.get("develop", {}).keys())
                except Exception:
                    pass
            elif filename in ("Gemfile", "Gemfile.lock"):
                for line in content.splitlines():
                    m = re.search(r"gem ['\"]([^'\"]+)['\"]", line)
                    if m:
                        entries.append(m.group(1))

            if entries:
                deps[filename] = sorted(set(entries))
                total += len(entries)

        return deps, dep_files, total

    def _detect_ci_cd(self) -> tuple[bool, str]:
        """Detect CI/CD configuration."""
        if (self.repo_path / ".github" / "workflows").exists():
            return True, "GitHub Actions"
        if (self.repo_path / ".gitlab-ci.yml").exists() or (self.repo_path / ".gitlab-ci.yaml").exists():
            return True, "GitLab CI"
        if any((self.repo_path / f).exists() for f in ["Jenkinsfile", ".jenkins/"]):
            return True, "Jenkins"
        if (self.repo_path / ".circleci").exists():
            return True, "CircleCI"
        if (self.repo_path / ".travis.yml").exists():
            return True, "Travis CI"
        if (self.repo_path / ".drone.yml").exists():
            return True, "Drone CI"
        return False, ""

    def _detect_tests(self, all_files: dict[str, Any]) -> tuple[bool, list[str], int]:
        """Detect test framework usage and estimate test count."""
        test_frameworks: list[str] = []
        test_file_count = 0

        relative_files = {str(f) for f in all_files["files"]}

        for fw_name, patterns in TEST_PATTERNS.items():
            for pattern in patterns:
                for rf in relative_files:
                    if pattern in rf or rf.endswith(pattern.replace("*", "")):
                        if fw_name not in test_frameworks:
                            test_frameworks.append(fw_name)
                        test_file_count += 1
                        break

        for fw_name, config_files in [
            ("pytest", ["pytest.ini", "pyproject.toml"]),
            ("jest", ["jest.config.js", "jest.config.ts", "jest.config.json"]),
            ("vitest", ["vitest.config.ts", "vitest.config.js"]),
            ("playwright", ["playwright.config.ts", "playwright.config.js"]),
        ]:
            for cf in config_files:
                if (self.repo_path / cf).exists():
                    if fw_name not in test_frameworks:
                        test_frameworks.append(fw_name)
                    break

        return len(test_frameworks) > 0, test_frameworks, test_file_count

    def _detect_lint_configs(self) -> list[str]:
        """Detect lint/format configuration files."""
        lint_configs = [
            ".pylintrc", ".flake8", "pyproject.toml", "ruff.toml", ".ruff.toml",
            ".eslintrc.js", ".eslintrc.json", ".eslintrc.yaml", ".eslintrc.yml",
            ".prettierrc", ".prettierrc.js", ".prettierrc.json",
            ".stylelintrc", ".stylelintrc.json",
            ".golangci.yml", ".golangci.yaml",
            "rustfmt.toml", "clippy.toml",
            ".rubocop.yml", ".rubocop.yaml",
            "tsconfig.json",
        ]
        found: list[str] = []
        for lc in lint_configs:
            if (self.repo_path / lc).exists():
                found.append(lc)
        return found

    def _detect_monorepo(self) -> tuple[bool, list[str]]:
        """Detect if repository is a monorepo with multiple packages."""
        packages: list[str] = []

        pkg_json = self.repo_path / "package.json"
        if pkg_json.exists():
            try:
                data = json.loads(pkg_json.read_text(encoding="utf-8"))
                workspaces = data.get("workspaces", [])
                if workspaces:
                    packages = list(workspaces)
            except Exception:
                pass

        if (self.repo_path / "pnpm-workspace.yaml").exists():
            if not packages:
                packages = ["pnpm workspace"]

        for d in ["apps/", "packages/", "services/"]:
            dir_path = self.repo_path / d
            if dir_path.exists() and dir_path.is_dir():
                subdirs = [str(p.relative_to(self.repo_path)) for p in dir_path.iterdir() if p.is_dir()]
                if len(subdirs) > 1:
                    packages.extend(subdirs)

        return len(packages) > 0, packages

    def _find_documentation_paths(self) -> list[str]:
        """Find documentation files and directories."""
        doc_paths: list[str] = []
        doc_patterns = [
            "README.md", "README.rst", "README.txt", "CONTRIBUTING.md",
            "CHANGELOG.md", "SECURITY.md", "LICENSE", "LICENSE.md",
            "docs/", "documentation/", "wiki/", "api-docs/", "swagger/",
            "openapi/", "redoc/", "storybook-static/",
        ]
        for pattern in doc_patterns:
            path = self.repo_path / pattern
            if path.exists():
                try:
                    doc_paths.append(str(path.relative_to(self.repo_path)))
                except ValueError:
                    doc_paths.append(pattern)
        return doc_paths

    def _compute_doc_coverage(self, all_files: dict[str, Any]) -> float:
        """Compute documentation coverage ratio."""
        total_files = len(all_files["files"])
        if total_files == 0:
            return 0.0

        doc_files = sum(
            1 for f in all_files["files"]
            if f.suffix in (".md", ".rst", ".txt") or "doc" in str(f).lower()
        )
        return min(100.0, (doc_files / total_files) * 100)

    def _has_file(self, filename: str) -> bool:
        """Check if a file exists at the repo root."""
        return (self.repo_path / filename).exists()

    def _has_any_file(self, patterns: list[str]) -> bool:
        """Check if any of the file patterns match."""
        for pattern in patterns:
            if pattern.endswith("/"):
                if (self.repo_path / pattern.rstrip("/")).exists():
                    return True
            elif "*" in pattern:
                import fnmatch
                for root, dirs, files in os.walk(self.repo_path):
                    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
                    if any(fnmatch.fnmatch(f, pattern) for f in files):
                        return True
                    if any(fnmatch.fnmatch(d, pattern) for d in dirs):
                        return True
            else:
                if (self.repo_path / pattern).exists() or any(
                    (self.repo_path / root / pattern).exists()
                    for root, _, _ in os.walk(self.repo_path)
                    if not any(ig in root.split(os.sep) for ig in IGNORE_DIRS)
                ):
                    return True
        return False

    def _determine_primary_language(self, languages: dict[str, Any]) -> str:
        """Determine the primary language by line count."""
        if not languages:
            return "Unknown"
        return max(languages, key=lambda lang: languages[lang].lines)

    def _generate_summary(self, info: RepositoryIntelligence) -> str:
        """Generate a human-readable summary of the repository."""
        lines = [
            f"This is a **{', '.join(info.architecture_styles)}** project primarily written in "
            f"**{info.primary_language}** ({info.languages.get(info.primary_language, LanguageStat()).percentage:.0f}% of codebase)."
        ]
        if info.frontend_frameworks:
            lines.append(f"Frontend uses **{', '.join(info.frontend_frameworks)}**.")
        if info.backend_frameworks:
            lines.append(f"Backend uses **{', '.join(info.backend_frameworks)}**.")
        if info.database_frameworks:
            lines.append(f"Database layer uses **{', '.join(info.database_frameworks)}**.")
        if info.testing_frameworks:
            lines.append(f"Testing via **{', '.join(info.testing_frameworks)}**.")
        if info.has_docker:
            lines.append("Containerized with Docker.")
        if info.has_ci_cd:
            lines.append(f"CI/CD via **{info.ci_cd_type}**.")

        if info.total_dependencies > 0:
            lines.append(f"**{info.total_dependencies}** total dependencies across {len(info.dependency_files)} manifest files.")

        if info.is_monorepo:
            lines.append(f"Monorepo with {len(info.packages)} packages: {', '.join(info.packages[:5])}.")

        return " ".join(lines)
