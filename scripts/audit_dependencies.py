from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\Sabidin\OneDrive - PT Petrosea Tbk\Documents\Enal-AI-OS")
BACKEND = ROOT / "backend"

declared = {
    "fastapi": ["fastapi"],
    "uvicorn": ["uvicorn"],
    "sqlalchemy": ["sqlalchemy"],
    "qdrant-client": ["qdrant_client"],
    "redis": ["redis"],
    "pydantic": ["pydantic"],
    "pydantic-settings": ["pydantic_settings"],
    "litellm": ["litellm"],
    "langchain-openai": ["langchain_openai"],
    "langchain-core": ["langchain_core"],
    "httpx": ["httpx"],
    "pyyaml": ["yaml"],
    "aiohttp": ["aiohttp"],
    "python-multipart": ["multipart"],
    "psycopg2-binary": ["psycopg2"],
}

used = defaultdict(list)
stdlib = {
    "asyncio", "logging", "json", "uuid", "dataclasses", "datetime", "typing",
    "enum", "os", "sys", "pathlib", "time", "re", "io", "shlex", "tempfile",
    "collections", "random", "statistics", "math", "functools", "itertools",
    "contextlib", "copy", "hashlib", "base64", "string", "textwrap", "types",
    "inspect", "builtins", "abc", "http", "email", "csv", "sqlite3", "zlib",
    "gzip", "bz2", "lzma", "struct", "socket", "selectors", "signal",
    "subprocess", "threading", "multiprocessing", "queue", "weakref",
    "userdict", "userlist", "userstring", "numbers",     "fractions", "decimal",
    "backend", "apps", "plugins", "golden", "real_cases", "benchmarks",
}

pyproject = BACKEND / "pyproject.toml"
print("## Dependency Audit Report")
print()
print("| Module | Status | Action |")
print("|--------|--------|--------|")

for path in BACKEND.rglob("*.py"):
    text = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for idx, line in enumerate(text, 1):
        m = re.match(r"^(from|import)\s+([a-zA-Z_][a-zA-Z0-9_.]*)", line)
        if not m:
            continue
        top = m.group(2).split(".")[0]
        if top in stdlib or top.startswith("_"):
            continue
        rel = path.relative_to(BACKEND)
        used[top].append(f"{rel}:{idx}")

for top in sorted(used):
    found = any(top in v for v in declared.values())
    if not found:
        print(f"| `{top}` | ❌ Undeclared | {len(used[top])} usages |")

print()
print("## Unused Declared Dependencies")
print()
for dep, tops in sorted(declared.items()):
    if not any(top in used for top in tops):
        print(f"- `{dep}` — declared but no direct import found")

print()
print("## Package Structure")
print()
for req in [BACKEND / "__init__.py", BACKEND / "app" / "__init__.py"]:
    status = "✅" if req.exists() else "❌ MISSING"
    print(f"- `{req.relative_to(BACKEND)}` — {status}")

print()
print("## CI/Makefile/Dockerfile Alignment")
print()
makefile = ROOT / "Makefile"
dockerfile = BACKEND / "Dockerfile"
ci = ROOT / ".github" / "workflows" / "ci.yml"
for label, path in [("Makefile", makefile), ("Dockerfile", dockerfile), ("CI", ci)]:
    status = "✅" if path.exists() else "❌ MISSING"
    print(f"- `{label}` — {status}")
    if path.exists():
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "poetry" in text:
            print("  - Uses poetry")
        if "pip install -e" in text:
            print("  - Uses editable install")
