"""
F0 — Repository Intelligence
=============================

Scans a repository and produces structured intelligence about:
- Languages, frameworks, architecture style
- Dependencies, entry points, build system, test system
- Containerization, CI/CD, documentation
- Project type classification

This is the foundational capability for all Full Stack Engineer modules.
Every other module (F1–F6) depends on F0's output for context-aware analysis.
"""

import ast
import json
import logging
import os
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# ────────────────────────────────────────────────────────────
# Constants
# ────────────────────────────────────────────────────────────

LANGUAGE_EXTENSIONS: dict[str, str] = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript (React JSX)",
    ".ts": "TypeScript",
    ".tsx": "TypeScript (React TSX)",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".kt": "Kotlin",
    ".swift": "Swift",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".cpp": "C++",
    ".c": "C",
    ".h": "C/C++ Header",
    ".hpp": "C++ Header",
    ".scala": "Scala",
    ".vue": "Vue",
    ".svelte": "Svelte",
    ".sol": "Solidity",
    ".sql": "SQL",
    ".sh": "Shell",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".json": "JSON",
    ".toml": "TOML",
    ".md": "Markdown",
    ".css": "CSS",
    ".scss": "SCSS",
    ".less": "LESS",
    ".html": "HTML",
    ".dart": "Dart",
    ".zig": "Zig",
    ".ex": "Elixir",
    ".exs": "Elixir Script",
}

FRAMEWORK_SIGNATURES: dict[str, list[str]] = {
    # Python Backend
    "FastAPI": ["fastapi", "FastAPI", "APIRouter"],
    "Django": ["django", "DJANGO_SETTINGS_MODULE", "django.core"],
    "Flask": ["flask", "Flask"],
    "Starlette": ["starlette", "Starlette"],
    "Tornado": ["tornado", "Tornado"],
    "Sanic": ["sanic", "Sanic"],
    "AIOHTTP": ["aiohttp", "AIOHTTP"],
    "Litestar": ["litestar", "Litestar"],
    # Python Data / ML
    "Pandas": ["pandas", "DataFrame"],
    "NumPy": ["numpy", "NumPy"],
    "PyTorch": ["torch", "PyTorch"],
    "TensorFlow": ["tensorflow", "TensorFlow"],
    "Scikit-learn": ["sklearn", "scikit_learn"],
    "LangChain": ["langchain", "LangChain"],
    "CrewAI": ["crewai", "CrewAI"],
    "DSPy": ["dspy", "DSPy"],
    # Python ORM / DB
    "SQLAlchemy": ["sqlalchemy", "SQLAlchemy", "declarative_base"],
    "Django ORM": ["django.db"],
    "Peewee": ["peewee", "Peewee"],
    "Tortoise ORM": ["tortoise", "Tortoise"],
    "Beanie": ["beanie", "Beanie"],
    "MongoEngine": ["mongoengine", "MongoEngine"],
    # Python Async / Queue
    "Celery": ["celery", "Celery"],
    "Redis": ["redis", "Redis"],
    "Rq": ["rq", "RQ"],
    "Huey": ["huey", "Huey"],
    "APScheduler": ["apscheduler", "APScheduler"],
    # Python Testing
    "pytest": ["pytest", "pytest_"],
    "unittest": ["unittest"],
    "behave": ["behave", "behave_"],
    "tox": ["tox", "tox_"],
    "nox": ["nox", "nox_"],
    # Python Tooling
    "Pydantic": ["pydantic", "BaseModel"],
    "Click": ["click", "click."],
    "Typer": ["typer", "typer."],
    "Rich": ["rich", "Rich"],
    "Alembic": ["alembic", "Alembic"],
    # JavaScript / TypeScript Frontend
    "React": ["react", "React", "create-react-app"],
    "Next.js": ["next", "Next.js", "next/"],
    "Vue": ["vue", "Vue", "create-vue"],
    "Nuxt": ["nuxt", "Nuxt"],
    "Angular": ["@angular", "angular", "Angular"],
    "Svelte": ["svelte", "Svelte"],
    "SvelteKit": ["@sveltejs/kit", "SvelteKit"],
    "Solid": ["solid-js", "Solid"],
    "Qwik": ["@builder.io/qwik", "Qwik"],
    "Preact": ["preact", "Preact"],
    "Remix": ["@remix-run", "remix"],
    "Gatsby": ["gatsby", "Gatsby"],
    "Astro": ["astro", "Astro"],
    "Eleventy": ["@11ty/eleventy", "Eleventy"],
    "Docusaurus": ["docusaurus", "Docusaurus"],
    "Storybook": ["@storybook", "storybook"],
    # JavaScript / TypeScript Backend
    "Express": ["express", "Express"],
    "NestJS": ["@nestjs", "NestJS"],
    "Fastify": ["fastify", "Fastify"],
    "Hono": ["hono", "Hono"],
    "Koa": ["koa", "Koa"],
    "Socket.io": ["socket.io", "Socket.IO"],
    "GraphQL": ["graphql", "GraphQL"],
    "Apollo": ["@apollo", "Apollo"],
    "tRPC": ["@trpc", "trpc"],
    "Prisma": ["@prisma", "prisma"],
    "TypeORM": ["typeorm", "TypeORM"],
    "Drizzle": ["drizzle-orm", "Drizzle"],
    "Mongoose": ["mongoose", "Mongoose"],
    "Sequelize": ["sequelize", "Sequelize"],
    "Knex": ["knex", "Knex"],
    "MikroORM": ["@mikro-orm", "MikroORM"],
    # JS Testing
    "Jest": ["jest", "Jest"],
    "Vitest": ["vitest", "Vitest"],
    "Playwright": ["@playwright", "playwright"],
    "Cypress": ["cypress", "Cypress"],
    "Testing Library": ["@testing-library"],
    "Mocha": ["mocha", "Mocha"],
    "Chai": ["chai", "Chai"],
    "Jasmine": ["jasmine", "Jasmine"],
    # JS State Management
    "Redux": ["redux", "Redux", "@reduxjs"],
    "Zustand": ["zustand", "Zustand"],
    "Jotai": ["jotai", "Jotai"],
    "Recoil": ["recoil", "Recoil"],
    "MobX": ["mobx", "MobX"],
    "Pinia": ["pinia", "Pinia"],
    "Vuex": ["vuex", "Vuex"],
    # JS Build Tools
    "Vite": ["vite", "Vite"],
    "Webpack": ["webpack", "Webpack"],
    "Turbopack": ["turbopack", "Turbopack"],
    "esbuild": ["esbuild", "esbuild"],
    "Rollup": ["rollup", "Rollup"],
    "Parcel": ["parcel", "Parcel"],
    "SWC": ["@swc", "swc"],
    "Babel": ["@babel", "babel"],
    "tsup": ["tsup", "tsup"],
    # CSS / UI
    "Tailwind CSS": ["tailwindcss", "tailwind"],
    "Styled Components": ["styled-components", "styled"],
    "Emotion": ["@emotion", "emotion"],
    "Sass": ["sass", "Sass", "node-sass"],
    "Less": ["less", "Less"],
    "Bootstrap": ["bootstrap", "Bootstrap"],
    "Material UI": ["@mui", "MUI"],
    "Chakra UI": ["@chakra", "Chakra"],
    "Ant Design": ["antd", "ant-design"],
    "Shadcn/ui": ["shadcn", "@radix-ui"],
    "Radix UI": ["@radix-ui"],
    "Headless UI": ["@headlessui"],
    "DaisyUI": ["daisyui", "DaisyUI"],
    "PrimeReact": ["primereact", "PrimeReact"],
    # Go
    "Gin": ["gin-gonic", "gin"],
    "Echo": ["echo", "labstack/echo"],
    "Fiber": ["gofiber", "fiber"],
    "Chi": ["go-chi", "chi"],
    "Gorilla": ["gorilla/mux", "Gorilla"],
    "Cobra": ["spf13/cobra", "cobra"],
    "Viper": ["spf13/viper", "viper"],
    "GORM": ["gorm.io", "gorm"],
    "Ent": ["entgo.io", "ent"],
    "Testify": ["stretchr/testify", "testify"],
    "GoKit": ["go-kit"],
    "Micro": ["micro"],
    # Rust
    "Axum": ["axum", "Axum"],
    "Actix Web": ["actix-web", "actix_web"],
    "Rocket": ["rocket", "Rocket"],
    "Tower": ["tower", "Tower"],
    "Tokio": ["tokio", "Tokio"],
    "Serde": ["serde", "Serde"],
    "Diesel": ["diesel", "Diesel"],
    "SQLx": ["sqlx", "SQLx"],
    "SeaORM": ["sea-orm", "SeaORM"],
    "Clap": ["clap", "Clap"],
    "Tauri": ["tauri", "Tauri"],
    # Java / Kotlin
    "Spring Boot": ["spring-boot", "SpringBoot"],
    "Spring MVC": ["spring-webmvc"],
    "Quarkus": ["quarkus", "Quarkus"],
    "Micronaut": ["micronaut", "Micronaut"],
    "Jakarta EE": ["jakarta"],
    "Hibernate": ["hibernate", "Hibernate"],
    "JPA": ["javax.persistence", "jakarta.persistence"],
    "Grails": ["grails", "Grails"],
    "Ktor": ["ktor", "Ktor"],
    "Exposed": ["org.jetbrains.exposed", "Exposed"],
    # Ruby
    "Ruby on Rails": ["rails", "Rails"],
    "Sinatra": ["sinatra", "Sinatra"],
    "RSpec": ["rspec", "RSpec"],
    # PHP
    "Laravel": ["laravel", "Laravel"],
    "Symfony": ["symfony", "Symfony"],
    "Composer": ["composer", "Composer"],
    # Mobile
    "Flutter": ["flutter", "Flutter"],
    "React Native": ["react-native", "ReactNative"],
    # Databases
    "PostgreSQL": ["psycopg2", "pg", "postgres", "postgresql", "@neondatabase"],
    "MySQL": ["mysql", "mysql2", "MySQL"],
    "SQLite": ["sqlite3", "sqlite", "SQLite"],
    "MongoDB": ["pymongo", "mongodb", "mongoose", "MongoDB", "motor"],
    "Redis": ["redis", "ioredis", "Redis"],
    "Elasticsearch": ["elasticsearch", "elastic", "ELK"],
    "ClickHouse": ["clickhouse", "ClickHouse"],
    "DuckDB": ["duckdb", "DuckDB"],
    "Supabase": ["supabase", "Supabase"],
    "Firebase": ["firebase", "Firebase"],
    "Neo4j": ["neo4j", "Neo4j"],
    # Cloud / Infrastructure
    "Docker": ["docker", "Docker", "docker-compose"],
    "Kubernetes": ["kubernetes", "Kubernetes", "k8s", "kube"],
    "AWS SDK": ["boto3", "aws-sdk", "@aws-sdk"],
    "Terraform": ["terraform", "Terraform", "cdktf"],
    "Pulumi": ["pulumi", "Pulumi"],
    "Ansible": ["ansible", "Ansible"],
    "Serverless": ["serverless", "Serverless"],
    "Packer": ["packer", "Packer"],
    # CI/CD
    "GitHub Actions": [".github/workflows"],
    "GitLab CI": [".gitlab-ci", "gitlab-ci"],
    "Jenkins": ["Jenkinsfile", "jenkins"],
    "CircleCI": [".circleci"],
    "Travis CI": [".travis.yml"],
    "Drone CI": [".drone.yml"],
    # Message Queue / Streaming
    "Kafka": ["kafka", "Kafka", "confluent"],
    "RabbitMQ": ["rabbitmq", "RabbitMQ", "aio-pika", "pika"],
    "NATS": ["nats", "NATS"],
    "ZeroMQ": ["zmq", "pyzmq", "zeromq"],
    "Pulsar": ["pulsar", "Pulsar"],
    # Monitoring
    "Prometheus": ["prometheus", "Prometheus", "prometheus_client"],
    "Grafana": ["grafana", "Grafana"],
    "Datadog": ["datadog", "Datadog"],
    "Sentry": ["sentry", "Sentry"],
    "OpenTelemetry": ["opentelemetry", "OpenTelemetry"],
    "New Relic": ["newrelic", "new_relic"],
    # API / Documentation
    "Swagger": ["swagger", "Swagger"],
    "OpenAPI": ["openapi", "OpenAPI"],
    "Redoc": ["redoc", "Redoc"],
    "Postman": ["postman", "Postman"],
    "JSDoc": ["jsdoc", "JSDoc"],
    "Sphinx": ["sphinx", "Sphinx"],
    "MkDocs": ["mkdocs", "MkDocs"],
    "Docsify": ["docsify", "Docsify"],
    "TypeDoc": ["typedoc", "TypeDoc"],
}

ARCHITECTURE_SIGNATURES: dict[str, list[dict[str, Any]]] = {
    "Clean Architecture": [
        {"must_have": ["domain", "entities", "use_cases", "application"]},
        {"should_have": ["infrastructure", "repositories", "interfaces", "controllers"]},
        {"must_not": ["core/.+api", "domain/.+framework"]},
    ],
    "Hexagonal Architecture": [
        {"must_have": ["port", "adapter", "core", "domain"]},
        {"should_have": ["inbound", "outbound", "application"]},
    ],
    "Layered Architecture": [
        {"must_have": ["controller", "service", "repository"]},
        {"should_have": ["middleware", "config", "routes"]},
    ],
    "Microservices": [
        {"must_have": ["service", "api-gateway"]},
        {"should_have": ["docker-compose", "kubernetes", "service-discovery"]},
    ],
    "Event-Driven Architecture": [
        {"must_have": ["event", "message", "queue", "broker", "pub", "sub"]},
        {"should_have": ["kafka", "rabbitmq", "nats", "sqs", "event-bus"]},
    ],
    "CQRS": [
        {"must_have": ["command", "query", "read", "write", "projection"]},
        {"should_have": ["event-store", "separate-db"]},
    ],
    "Serverless": [
        {"must_have": ["lambda", "function", "handler"]},
        {"should_have": ["serverless.yml", "serverless.ts", "cloudformation"]},
    ],
    "Monolithic": [
        {"must_have": ["app.py", "main.py", "routes.py", "models.py"]},
        {"should_not_have": ["docker-compose.*multi.*service", "kubernetes"]},
    ],
}

# Files/dirs that should be ignored during scanning
IGNORE_DIRS: set[str] = {
    ".git", "__pycache__", "node_modules", "venv", ".venv", "env",
    ".env", ".tox", ".nox", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".next", ".nuxt", "dist", "build", ".output", ".vercel",
    ".serverless", ".terraform", ".docusaurus", ".turbo",
    ".yarn", ".pnpm-store", "target", "vendor", ".bundle",
    "coverage", ".coverage", "htmlcov", ".eggs", "*.egg-info",
    ".gradle", "Pods", ".idea", ".vscode", ".DS_Store",
}

IGNORE_FILES: set[str] = {
    ".DS_Store", "Thumbs.db", "desktop.ini",
}

BUILD_SYSTEM_FILES: dict[str, str] = {
    "package.json": "npm / yarn / pnpm",
    "pnpm-lock.yaml": "pnpm",
    "yarn.lock": "yarn",
    "package-lock.json": "npm",
    "pyproject.toml": "poetry / peps",
    "Pipfile": "pipenv",
    "Pipfile.lock": "pipenv",
    "requirements.txt": "pip",
    "setup.py": "setuptools",
    "setup.cfg": "setuptools",
    "Cargo.toml": "cargo",
    "Cargo.lock": "cargo",
    "go.mod": "go modules",
    "go.sum": "go modules",
    "Gemfile": "bundler",
    "Gemfile.lock": "bundler",
    "composer.json": "composer",
    "composer.lock": "composer",
    "build.gradle": "gradle",
    "build.gradle.kts": "gradle",
    "pom.xml": "maven",
    "gradle.build": "gradle",
    "pubspec.yaml": "pub / dart",
    "mix.exs": "mix (elixir)",
    "Project.toml": "julia",
    "DESCRIPTION": "R / renv",
}

TEST_PATTERNS: dict[str, list[str]] = {
    "pytest": ["test_*.py", "*_test.py", "tests/", "test_"],
    "jest": ["*.test.js", "*.test.ts", "*.spec.js", "*.spec.ts", "__tests__/", "jest.config"],
    "vitest": ["*.test.js", "*.test.ts", "vitest.config"],
    "playwright": ["playwright.config", "*.spec.ts", "e2e/"],
    "cypress": ["cypress/", "cypress.config", "*.cy.js", "*.cy.ts"],
    "go test": ["*_test.go"],
    "cargo test": ["*_test.rs", "tests/"],
    "unittest": ["test_*.py", "unittest"],
    "rspec": ["spec/", "*_spec.rb"],
    "jasmine": ["spec/", "jasmine"],
    "mocha": ["test/", "mocha"],
    "kotlin test": ["*Test.kt", "test/"],
}


class LanguageStat:
    """Statistics for a single language in the repository."""
    files: int = 0
    lines: int = 0
    percentage: float = 0.0


# ────────────────────────────────────────────────────────────
# Data Models
# ────────────────────────────────────────────────────────────

@dataclass
class RepositoryIntelligence:
    """Complete intelligence report for a repository."""

    # Project Identity
    project_name: str = ""
    project_root: str = ""
    total_files: int = 0
    total_lines: int = 0
    total_dirs: int = 0

    # Language Breakdown
    languages: dict[str, LanguageStat] = field(default_factory=dict)
    primary_language: str = ""

    # Framework Detection
    frameworks: list[dict[str, Any]] = field(default_factory=list)
    frontend_frameworks: list[str] = field(default_factory=list)
    backend_frameworks: list[str] = field(default_factory=list)
    database_frameworks: list[str] = field(default_factory=list)
    testing_frameworks: list[str] = field(default_factory=list)

    # Architecture Detection
    architecture_styles: list[str] = field(default_factory=list)
    architecture_confidence: float = 0.0

    # Dependencies
    dependencies: dict[str, list[str]] = field(default_factory=dict)
    dependency_files: list[str] = field(default_factory=list)
    total_dependencies: int = 0

    # Entry Points
    entry_points: list[str] = field(default_factory=list)
    entry_type: str = ""

    # Build System
    build_system: str = ""
    build_tools: list[str] = field(default_factory=list)

    # Infrastructure
    has_docker: bool = False
    has_docker_compose: bool = False
    has_kubernetes: bool = False
    has_ci_cd: bool = False
    ci_cd_type: str = ""
    has_terraform: bool = False

    # Documentation
    has_readme: bool = False
    has_api_docs: bool = False
    has_storybook: bool = False
    documentation_paths: list[str] = field(default_factory=list)
    doc_coverage: float = 0.0

    # Quality Signals
    has_tests: bool = False
    test_frameworks: list[str] = field(default_factory=list)
    test_count_estimate: int = 0
    lint_configs: list[str] = field(default_factory=list)

    # Monorepo Detection
    is_monorepo: bool = False
    packages: list[str] = field(default_factory=list)

    # Summary
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        base = asdict(self)
        base["languages"] = {
            lang: {"files": stat.files, "lines": stat.lines, "percentage": round(stat.percentage, 1)}
            for lang, stat in sorted(self.languages.items(), key=lambda x: x[1].percentage, reverse=True)
        }
        return base

    def to_markdown(self) -> str:
        lines = [
            "# Repository Intelligence Report",
            "",
            f"**Project**: {self.project_name or 'Unknown'}",
            f"**Root**: `{self.project_root}`",
            f"**Total Files**: {self.total_files} | **Total Lines**: {self.total_lines:,} | **Directories**: {self.total_dirs}",
            "",
            "---",
            "",
            "## Language Breakdown",
            "",
            "| Language | Files | Lines | % |",
            "|----------|-------|-------|---|",
        ]
        for lang, stat in sorted(self.languages.items(), key=lambda x: x[1].percentage, reverse=True):
            lines.append(f"| {lang} | {stat.files} | {stat.lines:,} | {stat.percentage:.1f}% |")

        lines += [
            "",
            "---",
            "",
            "## Frameworks",
            "",
        ]
        if self.frameworks:
            lines.append(f"**Frontend**: {', '.join(self.frontend_frameworks) if self.frontend_frameworks else 'None detected'}")
            lines.append(f"**Backend**: {', '.join(self.backend_frameworks) if self.backend_frameworks else 'None detected'}")
            lines.append(f"**Database**: {', '.join(self.database_frameworks) if self.database_frameworks else 'None detected'}")
            lines.append(f"**Testing**: {', '.join(self.testing_frameworks) if self.testing_frameworks else 'None detected'}")
        else:
            lines.append("No frameworks detected.")

        lines += [
            "",
            "---",
            "",
            f"## Architecture Style",
            "",
            f"**Detected**: {', '.join(self.architecture_styles) if self.architecture_styles else 'Unknown'}",
            f"**Confidence**: {self.architecture_confidence:.0%}",
            "",
            "---",
            "",
            f"## Infrastructure",
            "",
            f"- **Docker**: {'✅' if self.has_docker else '❌'} | **Docker Compose**: {'✅' if self.has_docker_compose else '❌'} | **Kubernetes**: {'✅' if self.has_kubernetes else '❌'}",
            f"- **CI/CD**: {'✅ ' + self.ci_cd_type if self.has_ci_cd else '❌'}",
            f"- **Terraform**: {'✅' if self.has_terraform else '❌'}",
            f"- **Build System**: {self.build_system or 'None detected'}",
            "",
            "---",
            "",
            "## Entry Points",
            "",
        ]
        if self.entry_points:
            for ep in self.entry_points:
                lines.append(f"- `{ep}`")
            lines.append(f"\n**Entry Type**: {self.entry_type.title().replace('_', ' ')}")
        else:
            lines.append("No entry points detected.")

        lines += [
            "",
            "---",
            "",
            f"## Testing & Quality",
            "",
            f"- **Has Tests**: {'✅' if self.has_tests else '❌'}",
            f"- **Test Frameworks**: {', '.join(self.test_frameworks) if self.test_frameworks else 'None'}",
            f"- **Lint Configs**: {', '.join(self.lint_configs) if self.lint_configs else 'None'}",
            "",
            "---",
            "",
            "## Documentation",
            "",
            f"- **README**: {'✅' if self.has_readme else '❌'}",
            f"- **API Docs**: {'✅' if self.has_api_docs else '❌'}",
            f"- **Storybook**: {'✅' if self.has_storybook else '❌'}",
            f"- **Documentation Coverage**: {self.doc_coverage:.1f}%",
            "",
        ]
        if self.documentation_paths:
            lines.append("**Doc Paths:**")
            for p in self.documentation_paths[:10]:
                lines.append(f"- `{p}`")
            if len(self.documentation_paths) > 10:
                lines.append(f"- ... and {len(self.documentation_paths) - 10} more")
        lines.append("")

        # Summary
        lines += [
            "---",
            "",
            "## Summary",
            "",
            self.summary or "No summary generated.",
        ]

        return "\n".join(lines)


# ────────────────────────────────────────────────────────────
# Repository Scanner
# ────────────────────────────────────────────────────────────

class RepositoryScanner:
    """Scans a repository directory and produces RepositoryIntelligence."""

    def __init__(self, repo_path: str | Path):
        self.repo_path = Path(repo_path).resolve()

    async def scan(self) -> RepositoryIntelligence:
        """Perform a full scan of the repository."""
        if not self.repo_path.exists():
            raise FileNotFoundError(f"Repository path not found: {self.repo_path}")

        info = RepositoryIntelligence(
            project_name=self._detect_project_name(),
            project_root=str(self.repo_path),
        )

        # Collect all files
        all_files = self._collect_files()
        info.total_files = len(all_files["files"])
        info.total_lines = all_files["total_lines"]
        info.total_dirs = all_files["total_dirs"]

        # Language analysis
        info.languages = all_files["languages"]
        info.primary_language = self._determine_primary_language(info.languages)

        # Framework detection
        info.frameworks = self._detect_frameworks(all_files)
        info.frontend_frameworks = [f["name"] for f in info.frameworks if f["category"] == "frontend"]
        info.backend_frameworks = [f["name"] for f in info.frameworks if f["category"] == "backend"]
        info.database_frameworks = [f["name"] for f in info.frameworks if f["category"] == "database"]
        info.testing_frameworks = [f["name"] for f in info.frameworks if f["category"] == "testing"]

        # Architecture detection
        arch_styles, arch_conf = self._detect_architecture(info)
        info.architecture_styles = arch_styles
        info.architecture_confidence = arch_conf

        # Build system
        info.build_system, info.build_tools = self._detect_build_system()

        # Entry points
        info.entry_points, info.entry_type = self._detect_entry_points(all_files)

        # Dependencies
        info.dependencies, info.dependency_files, info.total_dependencies = self._collect_dependencies()

        # Infrastructure
        info.has_docker = self._has_file("Dockerfile")
        info.has_docker_compose = self._has_any_file(["docker-compose.yml", "docker-compose.yaml", "docker-compose.json"])
        info.has_kubernetes = self._has_any_file(["kubernetes/", "k8s/", "K8s/", "Kubernetes/"])
        info.has_ci_cd, info.ci_cd_type = self._detect_ci_cd()
        info.has_terraform = self._has_any_file(["*.tf", "*.tfvars", "terraform/"])

        # Documentation
        info.has_readme = self._has_any_file(["README.md", "README.rst", "README.txt", "README"])
        info.has_api_docs = self._has_any_file(["docs/", "api-docs/", "swagger/", "openapi/", "redoc/"])
        info.has_storybook = self._has_any_file([".storybook/", "storybook-static/"])
        info.documentation_paths = self._find_documentation_paths()
        info.doc_coverage = self._compute_doc_coverage(all_files)

        # Testing
        info.has_tests, info.test_frameworks, info.test_count_estimate = self._detect_tests(all_files)

        # Lint
        info.lint_configs = self._detect_lint_configs()

        # Monorepo detection
        info.is_monorepo, info.packages = self._detect_monorepo()

        # Generate summary
        info.summary = self._generate_summary(info)

        return info

    def _collect_files(self) -> dict[str, Any]:
        """Recursively collect all files with language stats."""
        language_stats: dict[str, LanguageStat] = {}
        all_files: list[Path] = []
        total_lines = 0
        total_dirs = 0

        for root, dirs, files in os.walk(self.repo_path):
            # Filter ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]

            for file in files:
                if file in IGNORE_FILES:
                    continue
                file_path = Path(root) / file
                rel_path = file_path.relative_to(self.repo_path)
                all_files.append(rel_path)

                ext = file_path.suffix.lower()
                lang = LANGUAGE_EXTENSIONS.get(ext, "Other")
                if lang not in language_stats:
                    language_stats[lang] = LanguageStat()
                language_stats[lang].files += 1

                # Count lines
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        line_count = sum(1 for _ in f)
                    total_lines += line_count
                    language_stats[lang].lines += line_count
                except Exception:
                    pass

        # Calculate percentages
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
        # pyproject.toml
        pyproject = self.repo_path / "pyproject.toml"
        if pyproject.exists():
            try:
                import tomllib
                data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
                return data.get("project", {}).get("name", "") or data.get("tool", {}).get("poetry", {}).get("name", "")
            except Exception:
                pass

        # package.json
        pkg_json = self.repo_path / "package.json"
        if pkg_json.exists():
            try:
                data = json.loads(pkg_json.read_text(encoding="utf-8"))
                return data.get("name", "")
            except Exception:
                pass

        # Cargo.toml
        cargo = self.repo_path / "Cargo.toml"
        if cargo.exists():
            try:
                import tomllib
                data = tomllib.loads(cargo.read_text(encoding="utf-8"))
                return data.get("package", {}).get("name", "")
            except Exception:
                pass

        # go.mod
        gomod = self.repo_path / "go.mod"
        if gomod.exists():
            for line in gomod.read_text(encoding="utf-8").splitlines():
                if line.startswith("module "):
                    return line.replace("module ", "").strip().split("/")[-1]

        return self.repo_path.name

    def _detect_frameworks(self, all_files: dict[str, Any]) -> list[dict[str, Any]]:
        """Detect frameworks from dependency files and imports."""
        detected: dict[str, dict[str, Any]] = {}

        # Read dependency files
        dep_files = self._find_dep_files()

        # Scan dependency content
        dep_content = ""
        for df in dep_files:
            try:
                content = (self.repo_path / df).read_text(encoding="utf-8", errors="ignore")
                dep_content += content + "\n"
            except Exception:
                pass

        # Scan source file imports
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

        # Categorize
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

        # Deduplicate by name
        result = list(detected.values())
        result.sort(key=lambda x: x["confidence"], reverse=True)
        return result

    def _detect_architecture(self, info: RepositoryIntelligence) -> tuple[list[str], float]:
        """Detect architecture style from directory structure and naming."""
        # Collect directory names
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

            # Compute confidence score
            if must_total > 0:
                style_score = (must_score / must_total) * 0.7
            else:
                style_score = 0.0
            if should_total > 0:
                style_score += (should_score / should_total) * 0.3
            else:
                style_score += 0.3  # bonus if no should conditions

            if style_score > best_score:
                best_score = style_score
                best_style = style

        # Additional heuristics for monorepo
        if info.is_monorepo:
            if best_score < 0.5:
                best_style = "Monorepo"
                best_score = 0.6

        # Clean architecture may also match DDD
        if best_style == "Clean Architecture" and best_score > 0.3:
            # Check for DDD additional signals
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
            # Pick the most specific
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
        # Additional dep files
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

        # Check each test pattern
        for fw_name, patterns in TEST_PATTERNS.items():
            for pattern in patterns:
                # Check if any file matches the pattern
                for rf in relative_files:
                    if pattern in rf or rf.endswith(pattern.replace("*", "")):
                        if fw_name not in test_frameworks:
                            test_frameworks.append(fw_name)
                        test_file_count += 1
                        break

        # Also detect from config files
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

        # Check for workspace configs
        pkg_json = self.repo_path / "package.json"
        if pkg_json.exists():
            try:
                data = json.loads(pkg_json.read_text(encoding="utf-8"))
                workspaces = data.get("workspaces", [])
                if workspaces:
                    packages = list(workspaces)
            except Exception:
                pass

        # Check for pnpm-workspace.yaml
        if (self.repo_path / "pnpm-workspace.yaml").exists():
            if not packages:
                packages = ["pnpm workspace"]

        # Check for multiple apps/ or packages/ dirs
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
                # Glob pattern
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

    def _determine_primary_language(self, languages: dict[str, LanguageStat]) -> str:
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


# ────────────────────────────────────────────────────────────
# Module-level convenience
# ────────────────────────────────────────────────────────────

class RepositoryIntelligenceEngine:
    """Engine that orchestrates repository intelligence gathering."""

    async def analyze(self, repo_path: str | Path) -> dict[str, Any]:
        """Analyze a repository and return structured intelligence."""
        scanner = RepositoryScanner(repo_path)
        info = await scanner.scan()
        return info.to_dict()

    async def analyze_markdown(self, repo_path: str | Path) -> str:
        """Analyze a repository and return a Markdown report."""
        scanner = RepositoryScanner(repo_path)
        info = await scanner.scan()
        return info.to_markdown()


repo_intelligence_engine = RepositoryIntelligenceEngine()

