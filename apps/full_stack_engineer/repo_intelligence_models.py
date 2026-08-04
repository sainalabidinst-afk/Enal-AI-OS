"""
Repository Intelligence Models
================================

Data models and constants for the repository intelligence module.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Any


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
    "FastAPI": ["fastapi", "FastAPI", "APIRouter"],
    "Django": ["django", "DJANGO_SETTINGS_MODULE", "django.core"],
    "Flask": ["flask", "Flask"],
    "Starlette": ["starlette", "Starlette"],
    "Tornado": ["tornado", "Tornado"],
    "Sanic": ["sanic", "Sanic"],
    "AIOHTTP": ["aiohttp", "AIOHTTP"],
    "Litestar": ["litestar", "Litestar"],
    "Pandas": ["pandas", "DataFrame"],
    "NumPy": ["numpy", "NumPy"],
    "PyTorch": ["torch", "PyTorch"],
    "TensorFlow": ["tensorflow", "TensorFlow"],
    "Scikit-learn": ["sklearn", "scikit_learn"],
    "LangChain": ["langchain", "LangChain"],
    "CrewAI": ["crewai", "CrewAI"],
    "DSPy": ["dspy", "DSPy"],
    "SQLAlchemy": ["sqlalchemy", "SQLAlchemy", "declarative_base"],
    "Django ORM": ["django.db"],
    "Peewee": ["peewee", "Peewee"],
    "Tortoise ORM": ["tortoise", "Tortoise"],
    "Beanie": ["beanie", "Beanie"],
    "MongoEngine": ["mongoengine", "MongoEngine"],
    "Celery": ["celery", "Celery"],
    "Redis": ["redis", "Redis"],
    "Rq": ["rq", "RQ"],
    "Huey": ["huey", "Huey"],
    "APScheduler": ["apscheduler", "APScheduler"],
    "pytest": ["pytest", "pytest_"],
    "unittest": ["unittest"],
    "behave": ["behave", "behave_"],
    "tox": ["tox", "tox_"],
    "nox": ["nox", "nox_"],
    "Pydantic": ["pydantic", "BaseModel"],
    "Click": ["click", "click."],
    "Typer": ["typer", "typer."],
    "Rich": ["rich", "Rich"],
    "Alembic": ["alembic", "Alembic"],
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
    "Jest": ["jest", "Jest"],
    "Vitest": ["vitest", "Vitest"],
    "Playwright": ["@playwright", "playwright"],
    "Cypress": ["cypress", "Cypress"],
    "Testing Library": ["@testing-library"],
    "Mocha": ["mocha", "Mocha"],
    "Chai": ["chai", "Chai"],
    "Jasmine": ["jasmine", "Jasmine"],
    "Redux": ["redux", "Redux", "@reduxjs"],
    "Zustand": ["zustand", "Zustand"],
    "Jotai": ["jotai", "Jotai"],
    "Recoil": ["recoil", "Recoil"],
    "MobX": ["mobx", "MobX"],
    "Pinia": ["pinia", "Pinia"],
    "Vuex": ["vuex", "Vuex"],
    "Vite": ["vite", "Vite"],
    "Webpack": ["webpack", "Webpack"],
    "Turbopack": ["turbopack", "Turbopack"],
    "esbuild": ["esbuild", "esbuild"],
    "Rollup": ["rollup", "Rollup"],
    "Parcel": ["parcel", "Parcel"],
    "SWC": ["@swc", "swc"],
    "Babel": ["@babel", "babel"],
    "tsup": ["tsup", "tsup"],
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
    "Ruby on Rails": ["rails", "Rails"],
    "Sinatra": ["sinatra", "Sinatra"],
    "RSpec": ["rspec", "RSpec"],
    "Laravel": ["laravel", "Laravel"],
    "Symfony": ["symfony", "Symfony"],
    "Composer": ["composer", "Composer"],
    "Flutter": ["flutter", "Flutter"],
    "React Native": ["react-native", "ReactNative"],
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
    "Docker": ["docker", "Docker", "docker-compose"],
    "Kubernetes": ["kubernetes", "Kubernetes", "k8s", "kube"],
    "AWS SDK": ["boto3", "aws-sdk", "@aws-sdk"],
    "Terraform": ["terraform", "Terraform", "cdktf"],
    "Pulumi": ["pulumi", "Pulumi"],
    "Ansible": ["ansible", "Ansible"],
    "Serverless": ["serverless", "Serverless"],
    "Packer": ["packer", "Packer"],
    "GitHub Actions": [".github/workflows"],
    "GitLab CI": [".gitlab-ci", "gitlab-ci"],
    "Jenkins": ["Jenkinsfile", "jenkins"],
    "CircleCI": [".circleci"],
    "Travis CI": [".travis.yml"],
    "Drone CI": [".drone.yml"],
    "Kafka": ["kafka", "Kafka", "confluent"],
    "RabbitMQ": ["rabbitmq", "RabbitMQ", "aio-pika", "pika"],
    "NATS": ["nats", "NATS"],
    "ZeroMQ": ["zmq", "pyzmq", "zeromq"],
    "Pulsar": ["pulsar", "Pulsar"],
    "Prometheus": ["prometheus", "Prometheus", "prometheus_client"],
    "Grafana": ["grafana", "Grafana"],
    "Datadog": ["datadog", "Datadog"],
    "Sentry": ["sentry", "Sentry"],
    "OpenTelemetry": ["opentelemetry", "OpenTelemetry"],
    "New Relic": ["newrelic", "new_relic"],
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


@dataclass
class RepositoryIntelligence:
    """Complete intelligence report for a repository."""

    project_name: str = ""
    project_root: str = ""
    total_files: int = 0
    total_lines: int = 0
    total_dirs: int = 0

    languages: dict[str, Any] = field(default_factory=dict)
    primary_language: str = ""

    frameworks: list[dict[str, Any]] = field(default_factory=list)
    frontend_frameworks: list[str] = field(default_factory=list)
    backend_frameworks: list[str] = field(default_factory=list)
    database_frameworks: list[str] = field(default_factory=list)
    testing_frameworks: list[str] = field(default_factory=list)

    architecture_styles: list[str] = field(default_factory=list)
    architecture_confidence: float = 0.0

    dependencies: dict[str, list[str]] = field(default_factory=dict)
    dependency_files: list[str] = field(default_factory=list)
    total_dependencies: int = 0

    entry_points: list[str] = field(default_factory=list)
    entry_type: str = ""

    build_system: str = ""
    build_tools: list[str] = field(default_factory=list)

    has_docker: bool = False
    has_docker_compose: bool = False
    has_kubernetes: bool = False
    has_ci_cd: bool = False
    ci_cd_type: str = ""
    has_terraform: bool = False

    has_readme: bool = False
    has_api_docs: bool = False
    has_storybook: bool = False
    documentation_paths: list[str] = field(default_factory=list)
    doc_coverage: float = 0.0

    has_tests: bool = False
    test_frameworks: list[str] = field(default_factory=list)
    test_count_estimate: int = 0
    lint_configs: list[str] = field(default_factory=list)

    is_monorepo: bool = False
    packages: list[str] = field(default_factory=list)

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

        lines += [
            "---",
            "",
            "## Summary",
            "",
            self.summary or "No summary generated.",
        ]

        return "\n".join(lines)
