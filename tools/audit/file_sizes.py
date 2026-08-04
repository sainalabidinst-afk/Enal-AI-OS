import os

files = [
    "apps/full_stack_engineer/architecture_review.py",
    "apps/full_stack_engineer/repo_intelligence.py",
    "apps/network_engineer/vendor/cisco_ios.py",
    "apps/network_engineer/vendor/fortinet.py",
    "apps/code_engineer/refactoring_engine.py",
    "apps/code_engineer/architecture_patterns.py",
    "apps/code_engineer/architecture_reader.py",
    "apps/network_engineer/nic/knowledge/profiles.py",
    "apps/research_assistant/engine.py",
    "apps/code_engineer/dependency_graph.py",
]

for f in files:
    size = os.path.getsize(f)
    lines = len(open(f, encoding="utf-8", errors="ignore").readlines())
    print(f"{f}: {size} bytes, {lines} lines")
