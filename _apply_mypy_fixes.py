"""
Apply all remaining mypy fixes programmatically.
Uses direct file read/write to avoid edit_file corruption.
"""
import ast
import sys


def check_syntax(path):
    """Verify file is valid Python."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    try:
        ast.parse(content)
        return True, content
    except SyntaxError as e:
        return False, content


def fix_and_verify(path, fix_func):
    """Read, apply fix, verify syntax, write back."""
    print(f"\n=== Fixing: {path} ===")
    valid, content = check_syntax(path)
    if not valid:
        print(f"  WARNING: File has syntax errors BEFORE fix!")
    
    new_content = fix_func(content)
    
    try:
        ast.parse(new_content)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✓ Fixed and verified OK")
        return True
    except SyntaxError as e:
        print(f"  ✗ Syntax error after fix: {e}")
        print(f"  Rolling back - keeping original")
        return False


# ============ FIX 1: self_verification.py ============
def fix_self_verification(content):
    """Fix _compile being outside class and return types."""
    # The problem: edit_file pushed async def _compile outside the class at indent 0
    # Find the methods at indent 0 and move them into the class
    
    lines = content.split('\n')
    class_indent = 4  # methods should be at 4 spaces
    
    # Find where the class SelfVerification ends (before the last self_verification = SelfVerification())
    # Strategy: find all methods, re-indent those at < 4 spaces to 4 spaces
    
    result = []
    in_class = False
    class_ended = False
    
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        
        if stripped.startswith('class SelfVerification'):
            in_class = True
            class_ended = False
            result.append(line)
            continue
        
        if in_class:
            # Check if we've left the class (empty line + top-level statement)
            if indent == 0 and stripped.startswith('async def '):
                # This method is outside class - re-indent it
                result.append('    ' + line)
                continue
            
            if indent == 0 and stripped.startswith('self_verification'):
                # End of class reached
                class_ended = True
                result.append(line)
                continue
            
            if class_ended:
                result.append(line)
            else:
                result.append(line)
        else:
            result.append(line)
    
    content = '\n'.join(result)
    
    # Now fix return types
    # _compile: tuple[str, str | None] -> tuple[str | None, str | None]
    # _lint, _test, _security_scan, _review: keep as tuple[str, str | None]
    
    content = content.replace(
        '    async def _compile(self, code: str, language: str) -> tuple[str, str | None]:',
        '    async def _compile(self, code: str, language: str) -> tuple[str | None, str | None]:'
    )
    
    return content


# ============ FIX 2: benchmark/runner.py ============
# Already fixed - verify
def verify_benchmark_runner():
    path = 'backend/app/core/benchmark/runner.py'
    valid, content = check_syntax(path)
    if not valid:
        print(f"\n!!! {path} has syntax errors!")
        return False
    
    # Check _score_executive_report is inside class
    if '    def _score_executive_report(self, data: dict[str, Any] | None) -> float:' in content:
        print(f"\n✓ {path}: _score_executive_report correctly inside class")
        return True
    else:
        print(f"\n! {path}: _score_executive_report may be outside class or incorrect")
        return False


# ============ FIX 3: society.py ============
def fix_society(content):
    """Add SubtaskResult import."""
    if 'SubtaskResult' in content:
        return content  # already fixed
    content = content.replace(
        'from apps.organization.task_planner import SubTask, TaskPlan, task_planner',
        'from apps.organization.task_planner import SubTask, SubtaskResult, TaskPlan, task_planner'
    )
    return content


# ============ FIX 4: ai_planner.py ============
def fix_ai_planner(content):
    """Add type annotation to blocking_steps."""
    if 'blocking_steps: list' in content:
        return content  # already fixed
    if 'from typing import Any' not in content:
        content = 'from typing import Any\n' + content
    # Find blocking_steps = [] and add annotation
    # Look for it in a method
    content = content.replace(
        'blocking_steps = []',
        'blocking_steps: list[dict[str, Any]] = []'
    )
    return content


# ============ Apply all fixes ============

fix_and_verify('backend/app/core/cognitive/self_verification.py', fix_self_verification)
verify_benchmark_runner()
fix_and_verify('apps/society/society.py', fix_society)
fix_and_verify('apps/organization/ai_planner.py', fix_ai_planner)

# Clean up temp files
import os
for f in ['_fix_mypy_errors.py', '_fix_remaining_mypy.py', '_fix_self_verification.py', '_fix_all_remaining.py']:
    if os.path.exists(f):
        os.remove(f)
        print(f"Cleaned up: {f}")

print("\n=== All fixes applied! ===")
