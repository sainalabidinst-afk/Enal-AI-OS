#!/usr/bin/env python3
"""Find all f-string backslash issues incompatible with Python 3.11."""
import os
import re

def find_fstring_backslash_issues(root_dir='.'):
    """Find f-strings with backslash in expression parts (Python 3.11 incompatible)."""
    results = []
    skip_dirs = {'__pycache__', '.git', 'node_modules', '.venv', 'venv', '.mypy_cache', '.pytest_cache'}
    
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden/venv dirs
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.') and d not in ('__pycache__',)]
        
        for f in files:
            if not f.endswith('.py'):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                    lines = fp.readlines()
            except Exception:
                continue
            
            for i, line in enumerate(lines, 1):
                stripped = line.rstrip()
                
                # Check if line contains f-string with backslash
                # We look for patterns like: f"..." or f'...' that contain {...\...}
                fstring_match = re.search(r"f(['\"])(.*?)(\1)", stripped)
                if not fstring_match:
                    continue
                
                quote = fstring_match.group(1)
                content = fstring_match.group(2)
                
                # Parse brace depth and find backslashes inside expressions
                brace_depth = 0
                expr_start = -1
                for j, c in enumerate(content):
                    if c == '{':
                        if brace_depth == 0:
                            expr_start = j
                        brace_depth += 1
                    elif c == '}':
                        brace_depth -= 1
                        if brace_depth == 0 and expr_start >= 0:
                            # Check if expression contains backslash
                            expr = content[expr_start+1:j]
                            if '\\' in expr:
                                results.append((path, i, stripped.strip()))
                            expr_start = -1
                    elif c == '\\' and brace_depth > 0:
                        # Backslash inside expression - already caught above
                        pass
    
    return results

# Also find triple-quote f-strings
def find_triple_fstring_issues(root_dir='.'):
    """Find triple-quoted f-strings with backslash issues."""
    results = []
    skip_dirs = {'__pycache__', '.git', 'node_modules', '.venv', 'venv', '.mypy_cache', '.pytest_cache'}
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.') and d not in ('__pycache__',)]
        
        for f in files:
            if not f.endswith('.py'):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
            except Exception:
                continue
            
            # Find f"""...""" patterns
            for m in re.finditer(r'f("""|\'\'\')(.*?)\1', content, re.DOTALL):
                fstring_content = m.group(2)
                lines = fstring_content.split('\n')
                brace_depth = 0
                expr_start = -1
                for line_idx, line in enumerate(lines):
                    for j, c in enumerate(line):
                        if c == '{':
                            if brace_depth == 0:
                                expr_start = j
                            brace_depth += 1
                        elif c == '}':
                            brace_depth -= 1
                            if brace_depth == 0 and expr_start >= 0:
                                expr = line[expr_start+1:j]
                                if '\\' in expr:
                                    lineno = content[:m.start()].count('\n') + line_idx + 1
                                    results.append((path, lineno, line.strip()))
                                expr_start = -1
    
    return results

if __name__ == '__main__':
    root = '.'
    
    print("=" * 80)
    print("SCANNING FOR F-STRING BACKSLASH ISSUES (Python 3.11 incompatible)")
    print("=" * 80)
    
    issues = find_fstring_backslash_issues(root)
    triple_issues = find_triple_fstring_issues(root)
    
    all_issues = issues + triple_issues
    
    if not all_issues:
        print("\n✅ NO F-STRING BACKSLASH ISSUES FOUND")
        print("The codebase appears to be compatible with Python 3.11 f-string rules.")
    else:
        print(f"\n❌ Found {len(all_issues)} potential f-string backslash issues:\n")
        for path, lineno, code in sorted(all_issues, key=lambda x: (x[0], x[1])):
            print(f"  {path}:{lineno}")
            print(f"    {code}")
            print()
    
    print("\n" + "=" * 80)
    print("SCANNING FOR OTHER HYGIENE ISSUES")
    print("=" * 80)
    
    # Find bare except
    bare_except = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in {'__pycache__', '.git', 'node_modules', '.venv', 'venv', '.mypy_cache', '.pytest_cache'} and not d.startswith('.')]
        for f in files:
            if not f.endswith('.py'):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                    lines = fp.readlines()
            except Exception:
                continue
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                # bare except: or except Exception: (without specific handling)
                if re.match(r'^except\s*(Exception)?\s*:', stripped):
                    bare_except.append((path, i, stripped))
    
    if bare_except:
        print(f"\n⚠️ Found {len(bare_except)} bare/generic except clauses:\n")
        for path, lineno, code in sorted(bare_except, key=lambda x: (x[0], x[1])):
            print(f"  {path}:{lineno}: {code}")
    else:
        print("\n✅ No bare/generic except clauses found.")
    
    # Find subprocess.run without check=False
    subprocess_issues = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in {'__pycache__', '.git', 'node_modules', '.venv', 'venv', '.mypy_cache', '.pytest_cache'} and not d.startswith('.')]
        for f in files:
            if not f.endswith('.py'):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
            except Exception:
                continue
            
            for m in re.finditer(r'subprocess\.run\(', content):
                # Check if 'check=' is in the same call
                start = m.start()
                # Find matching closing paren
                paren_depth = 0
                end = start
                for k in range(m.start(), len(content)):
                    if content[k] == '(':
                        paren_depth += 1
                    elif content[k] == ')':
                        paren_depth -= 1
                        if paren_depth == 0:
                            end = k
                            break
                call_content = content[start:end+1]
                if 'check=' not in call_content:
                    lineno = content[:start].count('\n') + 1
                    subprocess_issues.append((path, lineno, call_content[:80]))
    
    if subprocess_issues:
        print(f"\n⚠️ Found {len(subprocess_issues)} subprocess.run() calls without check=:\n")
        for path, lineno, code in sorted(subprocess_issues, key=lambda x: (x[0], x[1])):
            print(f"  {path}:{lineno}: {code}")
    else:
        print("\n✅ All subprocess.run() calls have explicit check= parameter.")

