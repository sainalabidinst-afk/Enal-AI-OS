import ast
import os
from collections import defaultdict

# Build import graph
graph = defaultdict(set)
all_files = []
for root, dirs, files in os.walk('backend'):
    dirs[:] = [d for d in dirs if d != '__pycache__']
    for f in files:
        if f.endswith('.py'):
            all_files.append(os.path.join(root, f))
for root, dirs, files in os.walk('apps'):
    dirs[:] = [d for d in dirs if d != '__pycache__']
    for f in files:
        if f.endswith('.py'):
            all_files.append(os.path.join(root, f))

module_map = {}
for path in all_files:
    mod = path.replace('/', '.').replace('\\', '.').replace('.py', '')
    if mod.endswith('.__init__'):
        mod = mod[:-9]
    module_map[path] = mod

for path in all_files:
    src = open(path, encoding='utf-8', errors='ignore').read()
    try:
        tree = ast.parse(src)
    except Exception:
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module:
                base = node.module
                graph[module_map.get(path, path)].add(base)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                graph[module_map.get(path, path)].add(alias.name.split('.')[0])

# Detect cycles using DFS
def find_cycles(graph):
    cycles = []
    visited = set()
    rec_stack = set()
    path = []
    
    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        for neighbor in list(graph.get(node, [])):
            if neighbor not in visited:
                dfs(neighbor)
            elif neighbor in rec_stack:
                try:
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append(cycle)
                except ValueError:
                    pass
        path.pop()
        rec_stack.remove(node)
    
    for node in list(graph.keys()):
        if node not in visited:
            dfs(node)
    return cycles

cycles = find_cycles(graph)
print(f"Total modules analyzed: {len(all_files)}")
print(f"Circular dependencies found: {len(cycles)}")
for c in cycles[:10]:
    print("  CYCLE:", " -> ".join(c))
