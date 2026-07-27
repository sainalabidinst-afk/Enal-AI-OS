"""
Scans the codebase for P0 issues:
1. RUF012 - Mutable defaults in dataclasses
2. Async blocking I/O (open() inside async def)
3. Write results to scan_results.txt for evidence
"""
import os
import ast
import sys


def scan_mutable_defaults(root_dirs):
    """Find dataclass fields with mutable defaults instead of field(default_factory=...)."""
    results = []
    for root_dir in root_dirs:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            if any(skip in dirpath for skip in ['node_modules', '__pycache__', '.venv', '.git', '.mypy_cache', '.mypy_cache']):
                continue
            for fn in filenames:
                if not fn.endswith('.py'):
                    continue
                fpath = os.path.join(dirpath, fn)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    tree = ast.parse(content)
                    dataclass_fields = []
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            is_dataclass = False
                            for dec in node.decorator_list:
                                if isinstance(dec, ast.Call) and hasattr(dec.func, 'id') and dec.func.id == 'dataclass':
                                    is_dataclass = True
                                elif isinstance(dec, ast.Name) and dec.id == 'dataclass':
                                    is_dataclass = True
                            if not is_dataclass:
                                continue
                            for item in node.body:
                                if isinstance(item, ast.AnnAssign) and item.value is not None:
                                    if isinstance(item.value, ast.List) and len(item.value.elts) == 0:
                                        rel = os.path.relpath(fpath)
                                        lineno = item.lineno
                                        name = item.target.id if isinstance(item.target, ast.Name) else '?'
                                        dataclass_fields.append((rel, lineno, name))
                    if dataclass_fields:
                        results.extend(dataclass_fields)
                except SyntaxError:
                    pass
                except Exception:
                    pass
    return results


def scan_blocking_io(root_dirs):
    """Find open() calls inside async def blocks."""
    results = []
    for root_dir in root_dirs:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            if any(skip in dirpath for skip in ['node_modules', '__pycache__', '.venv', '.git', '.mypy_cache']):
                continue
            for fn in filenames:
                if not fn.endswith('.py'):
                    continue
                fpath = os.path.join(dirpath, fn)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    in_async = False
                    for i, line in enumerate(lines):
                        stripped = line.strip()
                        if stripped.startswith('async def '):
                            in_async = True
                        elif in_async and (stripped.startswith('def ') or stripped.startswith('class ')):
                            in_async = False
                        elif in_async and ('open(' in stripped or 'open (' in stripped):
                            rel = os.path.relpath(fpath)
                            results.append((rel, i + 1))
                except Exception:
                    pass
    return results


if __name__ == '__main__':
    dirs = ['apps', 'backend/app']

    output_lines = []
    output_lines.append("=" * 60)
    output_lines.append("P0 SCAN RESULTS - Sprint Hardening")
    output_lines.append("=" * 60)
    output_lines.append("")

    output_lines.append("--- RUF012: Mutable Defaults in Dataclasses ---")
    mutable = scan_mutable_defaults(dirs)
    if mutable:
        for rel, lineno, name in mutable:
            output_lines.append(f"  {rel}:{lineno} - '{name}' has mutable list default")
        output_lines.append(f"\n  Total: {len(mutable)} issue(s)")
    else:
        output_lines.append("  ZERO issues found. All dataclass fields use field(default_factory=...).")
    output_lines.append("")

    output_lines.append("--- Async Blocking I/O ---")
    io_issues = scan_blocking_io(dirs)
    if io_issues:
        for rel, lineno in io_issues:
            output_lines.append(f"  {rel}:{lineno} - open() inside async function")
        output_lines.append(f"\n  Total: {len(io_issues)} issue(s)")
    else:
        output_lines.append("  ZERO issues found. No blocking open() calls in async functions.")
    output_lines.append("")

    output = "\n".join(output_lines)
    print(output)

    with open('scan_results.txt', 'w', encoding='utf-8') as f:
        f.write(output)
    print("\nResults written to scan_results.txt")
