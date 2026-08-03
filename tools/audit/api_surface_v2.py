import ast
import os
import re
import subprocess
import sys

print("=== API SURFACE ANALYSIS (v2) ===\n")

# 1. Find all endpoints using regex (more reliable)
api_files = []
for root, dirs, files in os.walk('backend/app/api'):
    dirs[:] = [d for d in dirs if d != '__pycache__']
    for f in files:
        if f.endswith('.py') and f != '__init__.py':
            api_files.append(os.path.join(root, f))

endpoints = []
routers = []

for path in api_files:
    with open(path, encoding='utf-8', errors='ignore') as f:
        src = f.read()
    router_name = os.path.basename(path).replace('.py', '')
    routers.append(router_name)
    
    # Use regex to find @router.METHOD("path") patterns
    for match in re.finditer(r'@router\.(get|post|put|delete|patch|websocket)\(["\']([^"\']+)["\']', src):
        method = match.group(1).upper()
        endpoint_path = match.group(2)
        # Find the function name after the decorator
        func_match = re.search(r'@router\.' + match.group(1) + r'\([^)]+\)\s+async def (\w+)', src, re.DOTALL)
        func_name = func_match.group(1) if func_match else 'unknown'
        endpoints.append({
            'file': path,
            'router': router_name,
            'method': method,
            'path': endpoint_path,
            'function': func_name,
        })

print(f"Total routers: {len(routers)}")
print(f"Total endpoints: {len(endpoints)}")
print("\nEndpoints by router:")
from collections import Counter
router_counts = Counter(e['router'] for e in endpoints)
for router, count in sorted(router_counts.items()):
    print(f"  {router}: {count} endpoints")

print("\nAll endpoints:")
for e in sorted(endpoints, key=lambda x: (x['router'], x['path'])):
    print(f"  {e['method']:10s} {e['path']:45s} [{e['router']}.{e['function']}]")

# 2. Check which routers are included in main.py
with open('backend/app/main.py', encoding='utf-8') as f:
    main_src = f.read()

included_routers = []
for line in main_src.splitlines():
    if 'include_router' in line:
        match = re.search(r'include_router\((\w+)', line)
        if match:
            included_routers.append(match.group(1))

print(f"\nRouters included in main.py: {len(included_routers)}")
for r in sorted(included_routers):
    status = "OK" if r in [os.path.basename(p).replace('.py', '') for p in api_files] else "?"
    print(f"  [{status}] {r}")

unused_routers = set(routers) - set(included_routers)
if unused_routers:
    print(f"\nOrphan routers (not included in main.py): {len(unused_routers)}")
    for r in sorted(unused_routers):
        print(f"  [ORPHAN] {r}")
else:
    print("\nNo orphan routers found.")

# 3. Check for unused endpoint paths (no tests, no references)
print("\n=== ENDPOINT USAGE ANALYSIS ===\n")
all_endpoint_paths = [e['path'] for e in endpoints]
referenced_paths = set()

# Search for endpoint references in tests and apps
for search_dir in ['tests', 'backend/tests', 'apps']:
    if not os.path.exists(search_dir):
        continue
    for root, dirs, files in os.walk(search_dir):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for f in files:
            if f.endswith('.py'):
                path = os.path.join(root, f)
                with open(path, encoding='utf-8', errors='ignore') as fh:
                    content = fh.read()
                    for ep in all_endpoint_paths:
                        if ep in content:
                            referenced_paths.add(ep)

unreferenced = set(all_endpoint_paths) - referenced_paths
print(f"Endpoints with NO references in tests/apps: {len(unreferenced)}")
for ep in sorted(unreferenced):
    print(f"  [UNREFERENCED] {ep}")

# 4. Memory leak risk analysis
print("\n=== MEMORY LEAK RISK ===\n")
memory_patterns = []

for root, dirs, files in os.walk('backend/app/core'):
    dirs[:] = [d for d in dirs if d != '__pycache__']
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            with open(path, encoding='utf-8', errors='ignore') as fh:
                src = fh.read()
            if 'self._audit_log.append' in src or '_pending_approval' in src:
                memory_patterns.append(('Unbounded log/approval dict', path))
            if '_episodes' in src and 'del self._episodes' not in src:
                memory_patterns.append(('EpisodicMemory may not clean up', path))
            if '_sessions' in src and 'del self._sessions' not in src:
                memory_patterns.append(('SessionMemory may not clean up', path))
            if 'self._plugins' in src and 'del self._plugins' not in src:
                memory_patterns.append(('Plugin registry may not clean up', path))

for pattern, path in memory_patterns[:20]:
    print(f"  {pattern}: {path}")

# 5. Test coverage estimation
print("\n=== TEST COVERAGE ESTIMATE ===\n")
test_files = []
for search_dir in ['tests', 'backend/tests']:
    if os.path.exists(search_dir):
        for root, dirs, files in os.walk(search_dir):
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for f in files:
                if f.startswith('test_') and f.endswith('.py'):
                    test_files.append(os.path.join(root, f))

# Count test functions
test_count = 0
for path in test_files:
    with open(path, encoding='utf-8', errors='ignore') as f:
        src = f.read()
    try:
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                test_count += 1
    except SyntaxError:
        pass

print(f"Test files: {len(test_files)}")
print(f"Test functions: {test_count}")

# 6. Async safety - blocking calls in async functions
print("\n=== ASYNC SAFETY ===\n")
async_issues = []

for root, dirs, files in os.walk('backend/app/core'):
    dirs[:] = [d for d in dirs if d != '__pycache__']
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            with open(path, encoding='utf-8', errors='ignore') as fh:
                src = fh.read()
            try:
                tree = ast.parse(src)
            except SyntaxError:
                continue
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
                    is_async = isinstance(node, ast.AsyncFunctionDef)
                    for child in ast.walk(node):
                        if isinstance(child, ast.Call):
                            func_name = ast.unparse(child.func) if hasattr(ast, 'unparse') else ''
                            if is_async:
                                if 'model_router.complete' in func_name or 'model_router.' in func_name and 'acomplete' not in func_name:
                                    async_issues.append(('Blocking LLM call in async', path, node.name))
                                if '.keys(' in func_name and 'redis' in path.lower():
                                    async_issues.append(('Blocking redis.keys() in async', path, node.name))
                                if 'time.sleep' in func_name:
                                    async_issues.append(('Blocking sleep in async', path, node.name))

print(f"Async safety issues: {len(async_issues)}")
for issue, path, func in async_issues[:20]:
    print(f"  {issue}: {func} in {os.path.basename(path)}")
