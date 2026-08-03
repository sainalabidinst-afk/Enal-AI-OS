import ast
import os
import re
import sys

print("=== API SURFACE ANALYSIS ===\n")

# 1. Find all routers and endpoints in backend
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
    try:
        tree = ast.parse(src)
    except SyntaxError:
        continue
    
    router_name = os.path.basename(path).replace('.py', '')
    routers.append(router_name)
    
    # Look for @router.get/post/etc patterns
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for dec in node.decorator_list:
                dec_str = ast.unparse(dec) if hasattr(ast, 'unparse') else ''
                if any(m in dec_str for m in ['router.get', 'router.post', 'router.put', 'router.delete', 'router.patch']):
                    method = 'UNKNOWN'
                    for m in ['get', 'post', 'put', 'delete', 'patch']:
                        if f'router.{m}' in dec_str:
                            method = m.upper()
                            break
                    # Try to extract path
                    path_match = re.search(r'["\']([^"\']+)["\']', dec_str)
                    endpoint_path = path_match.group(1) if path_match else 'unknown'
                    endpoints.append({
                        'file': path,
                        'router': router_name,
                        'method': method,
                        'path': endpoint_path,
                        'function': node.name,
                    })

print(f"Total routers: {len(routers)}")
print(f"Total endpoints: {len(endpoints)}")
print("\nEndpoints by router:")
from collections import Counter
router_counts = Counter(e['router'] for e in endpoints)
for router, count in sorted(router_counts.items()):
    print(f"  {router}: {count} endpoints")

if endpoints:
    print("\nAll endpoints:")
    for e in sorted(endpoints, key=lambda x: (x['router'], x['path'])):
        print(f"  {e['method']:6s} {e['path']:40s} [{e['router']}.{e['function']}]")

# 2. Check which endpoints are included in main.py
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

# 3. Check for dependency injection usage
print("\n=== DEPENDENCY INJECTION ANALYSIS ===\n")
di_count = 0
di_endpoints = []
for path in api_files:
    with open(path, encoding='utf-8', errors='ignore') as f:
        src = f.read()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        continue
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for dec in node.decorator_list:
                dec_str = ast.unparse(dec) if hasattr(ast, 'unparse') else ''
                if 'Depends(' in dec_str:
                    di_count += 1
                    di_endpoints.append((path, node.name, dec_str))

print(f"Endpoints using Depends(): {di_count}")
for path, func, dec in di_endpoints[:15]:
    print(f"  {func} in {os.path.basename(path)}: {dec}")

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
            # Check for unbounded data structures
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

# 5. Async safety analysis
print("\n=== ASYNC SAFETY ANALYSIS ===\n")
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
                if isinstance(node, ast.AsyncFunctionDef):
                    # Check for blocking calls inside async functions
                    for child in ast.walk(node):
                        if isinstance(child, ast.Call):
                            func_name = ast.unparse(child.func) if hasattr(ast, 'unparse') else ''
                            # Check for sync model calls
                            if 'model_router.complete' in func_name:
                                async_issues.append(('Blocking LLM call in async', path, node.name))
                            # Check for time.sleep
                            if 'time.sleep' in func_name:
                                async_issues.append(('Blocking sleep in async', path, node.name))
                            # Check for redis.keys()
                            if '.keys(' in func_name and 'redis' in src.lower():
                                async_issues.append(('Blocking redis.keys() in async', path, node.name))

print(f"Async safety issues found: {len(async_issues)}")
for issue, path, func in async_issues[:20]:
    print(f"  {issue}: {func} in {path}")
