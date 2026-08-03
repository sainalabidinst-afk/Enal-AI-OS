import ast
import os
from collections import defaultdict

def analyze_file(path):
    with open(path, encoding='utf-8', errors='ignore') as f:
        src = f.read()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None
    
    classes = []
    functions = []
    calls = []
    imports = []
    complexity = 0
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            classes.append((node.name, methods))
        elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            functions.append(node.name)
            # Simple complexity: count branches
            comp = 1
            for child in ast.walk(node):
                if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler, ast.With, ast.AsyncWith)):
                    comp += 1
                elif isinstance(child, ast.BoolOp):
                    comp += len(child.values) - 1
            complexity += comp
        elif isinstance(node, ast.Call):
            if hasattr(node.func, 'id'):
                calls.append(node.func.id)
            elif hasattr(node.func, 'attr'):
                calls.append(node.func.attr)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split('.')[0])
    
    return {
        'path': path,
        'classes': classes,
        'functions': functions,
        'calls': calls,
        'imports': imports,
        'complexity': complexity,
        'loc': len(src.splitlines()),
    }

# Analyze all Python files
results = []
for root, dirs, files in os.walk('backend'):
    dirs[:] = [d for d in dirs if d != '__pycache__']
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            r = analyze_file(path)
            if r:
                results.append(r)
for root, dirs, files in os.walk('apps'):
    dirs[:] = [d for d in dirs if d != '__pycache__']
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            r = analyze_file(path)
            if r:
                results.append(r)

print(f"Total files analyzed: {len(results)}")
print(f"Total LOC: {sum(r['loc'] for r in results)}")

# Cyclomatic complexity stats
complexities = [r['complexity'] for r in results]
avg_complexity = sum(complexities) / len(complexities) if complexities else 0
max_complexity = max(complexities) if complexities else 0
high_complexity = [(r['path'], r['complexity']) for r in results if r['complexity'] > 50]
high_complexity.sort(key=lambda x: x[1], reverse=True)

print(f"\nCyclomatic Complexity:")
print(f"  Average: {avg_complexity:.1f}")
print(f"  Max: {max_complexity}")
print(f"  Files with complexity > 50: {len(high_complexity)}")
for path, comp in high_complexity[:10]:
    print(f"    {comp:3d} {path}")

# Dead code: find functions/classes that are never called
all_function_names = set()
for r in results:
    for cls, methods in r['classes']:
        all_function_names.add(cls)
        all_function_names.update(methods)
    all_function_names.update(r['functions'])

# Check which functions are never called from OTHER files
call_graph = defaultdict(set)
for r in results:
    mod = r['path'].replace('/', '.').replace('\\', '.').replace('.py', '')
    if mod.endswith('.__init__'):
        mod = mod[:-9]
    for call in r['calls']:
        call_graph[mod].add(call)

# Find potentially dead code (functions defined but not called anywhere)
all_called = set()
for calls in call_graph.values():
    all_called.update(calls)

potentially_dead = []
for r in results:
    for func in r['functions']:
        if func not in all_called and not func.startswith('_'):
            potentially_dead.append((r['path'], func))
    for cls, methods in r['classes']:
        if cls not in all_called:
            potentially_dead.append((r['path'], f"class {cls}"))

print(f"\nPotentially dead code (exported but never called): {len(potentially_dead)}")
for path, name in potentially_dead[:20]:
    print(f"  {name} in {path}")

# Duplicate code detection (similar function names)
func_locations = defaultdict(list)
for r in results:
    for func in r['functions']:
        func_locations[func].append(r['path'])
duplicates = {k: v for k, v in func_locations.items() if len(v) > 1}
print(f"\nDuplicate function names: {len(duplicates)}")
for name, paths in list(duplicates.items())[:10]:
    print(f"  {name}: {paths}")
