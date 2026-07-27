#!/usr/bin/env python3
"""Run ruff and capture output safely, handling encoding issues."""
import subprocess
import sys
import os

def run_ruff():
    """Run ruff check and capture output."""
    
    # Method 1: Run directly with UTF-8 mode
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    result = subprocess.run(
        [sys.executable, '-X', 'utf8', '-m', 'ruff', 'check', 'apps/', 'backend/'],
        capture_output=True,
        timeout=120,
        env=env
    )
    
    stdout = result.stdout.decode('utf-8', errors='replace')
    stderr = result.stderr.decode('utf-8', errors='replace')
    
    print(f"Return code: {result.returncode}")
    print(f"\nSTDOUT ({len(stdout)} chars):")
    print(stdout[:5000])
    if stderr:
        print(f"\nSTDERR ({len(stderr)} chars):")
        print(stderr[:1000])
    
    # Count issues
    issues = [l for l in stdout.split('\n') if l.strip() and l.strip().endswith('.py') or ':' in l and l.strip()[0].isalpha()]
    print(f"\n\nTotal lines in output: {len(stdout.split(chr(10)))}")
    
    # Check for specific patterns
    if 'f-string' in stdout.lower() and ('escape' in stdout.lower() or 'backslash' in stdout.lower()):
        print("\n⚠️  F-STRING BACKSLASH ISSUES DETECTED BY RUFF!")
    
    if 'unused import' in stdout.lower():
        print("\n⚠️  UNUSED IMPORTS DETECTED!")

if __name__ == '__main__':
    run_ruff()

