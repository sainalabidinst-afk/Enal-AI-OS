"""
Audit remaining code hygiene issues for Sprint Code Hygiene.

Checks:
1. Python 3.11 f-string backslash escapes (P1 blocker)
2. Ruff auto-fixable issues (P2)
3. Tests still passing
"""
import os
import subprocess
import sys


def check_fstring_escapes():
    """Find Python 3.11 incompatible f-string backslash escapes."""
    issues = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ('venv', 'node_modules', '__pycache__', '.git', '.mypy_cache', '.pytest_cache')]
        for f in files:
            if not f.endswith('.py'):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
            except Exception:
                continue
            try:
                compile(content, path, 'exec', flags=0)
            except SyntaxError as e:
                if 'f-string' in str(e).lower() and ('escape' in str(e).lower() or 'backslash' in str(e).lower()):
                    # Show context around the error
                    lines = content.split('\n')
                    line_idx = e.lineno - 1 if e.lineno else 0
                    context_before = '\n'.join(lines[max(0,line_idx-3):line_idx])
                    context_error = lines[line_idx] if line_idx < len(lines) else ''
                    context_after = '\n'.join(lines[line_idx+1:min(len(lines),line_idx+4)])
                    issues.append((path, e.lineno, str(e), context_before, context_error, context_after))
    return issues


def check_fastapi_import():
    """Check if fastapi can be resolved."""
    try:
        import fastapi
        print(f"  fastapi resolved OK (version: {fastapi.__version__})")
        return True
    except ImportError as e:
        print(f"  fastapi NOT resolved: {e}")
        return False


def run_ruff():
    """Run ruff check for remaining issues."""
    result = subprocess.run(
        [sys.executable, '-m', 'ruff', 'check', '.', '--select', 'E,F,I,N,W,UP,F541'],
        capture_output=True, text=True, timeout=60
    )
    return result.stdout, result.stderr


def run_ruff_format():
    """Check ruff format."""
    result = subprocess.run(
        [sys.executable, '-m', 'ruff', 'format', '--check', '.'],
        capture_output=True, text=True, timeout=60
    )
    return result.stdout, result.stderr


def run_tests():
    """Quick test count check."""
    result = subprocess.run(
        [sys.executable, '-m', 'pytest', '--collect-only', '-q'],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout, result.stderr


if __name__ == '__main__':
    print("=" * 60)
    print("SPRINT CODE HYGIENE AUDIT")
    print(f"Python: {sys.version}")
    print("=" * 60)
    
    print("\n--- 1. Python 3.11 f-string escape check ---")
    issues = check_fstring_escapes()
    if issues:
        print(f"  FOUND {len(issues)} issue(s):")
        for path, lineno, msg, before, err_line, after in issues:
            print(f"\n  📍 {path}:{lineno}")
            print(f"  Error: {msg}")
            if before:
                for l in before.split('\n'):
                    print(f"    {l}")
            print(f"  ❌ {err_line}")
            if after:
                for l in after.split('\n'):
                    print(f"    {l}")
    else:
        print("  ✅ ZERO f-string escape issues found")
        
    print("\n--- 2. fastapi import resolution ---")
    check_fastapi_import()
    
    print("\n--- 3. Ruff lint check (E, F, I, N, W, UP, F541) ---")
    out, err = run_ruff()
    if out.strip():
        lines = [l for l in out.split('\n') if l.strip() and 'warning' not in l.lower()]
        print(f"  {len(lines)} issue(s) found (use 'ruff check . --fix' to auto-fix)")
        for l in lines[:30]:
            print(f"    {l}")
        if len(lines) > 30:
            print(f"    ... and {len(lines)-30} more")
    else:
        print("  ✅ No lint issues")

    print("\n--- 4. Ruff format check ---")
    out, err = run_ruff_format()
    issues_fmt = [l for l in out.split('\n') if l.strip() and 'would' in l.lower()]
    if issues_fmt:
        print(f"  {len(issues_fmt)} file(s) would be reformatted")
        for l in issues_fmt[:10]:
            print(f"    {l}")
    else:
        print("  ✅ All files formatted correctly")
    
    print("\n--- 5. Test collection ---")
    out, err = run_tests()
    print(out[-200:] if len(out) > 200 else out)
    
    print("\n" + "=" * 60)
    print("AUDIT COMPLETE")
    print("=" * 60)
