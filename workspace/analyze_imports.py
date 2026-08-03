import ast
from pathlib import Path
from collections import defaultdict

root = Path('.').resolve()
backend_root = root / 'backend' / 'app'
apps_root = root / 'apps'

mods = {}
for path in list(backend_root.rglob('*.py')) + list(apps_root.rglob('*.py')):
    rel = path.relative_to(root)
    if path.name == '__init__.py':
        mod = '.'.join(rel.with_suffix('').parts)
    else:
        mod = '.'.join(rel.with_suffix('').parts)
    mods[str(path)] = mod

name_to_path = {mod: path for path, mod in mods.items()}


def module_name_from_import(node):
    names = []
    if isinstance(node, ast.Import):
        for n in node.names:
            if n.name.startswith('backend.') or n.name.startswith('apps.'):
                names.append(n.name)
    elif isinstance(node, ast.ImportFrom) and node.module:
        if node.module.startswith('backend.') or node.module.startswith('apps.'):
            names.append(node.module)
        elif node.module in {'backend', 'apps'}:
            names.append(node.module)
    return names


def resolve_imports(module_name, imports):
    res = []
    for imp in imports:
        if imp.startswith('backend.') or imp.startswith('apps.'):
            parts = imp.split('.')
            candidates = []
            for i in range(1, len(parts) + 1):
                cand = '.'.join(parts[:i])
                if cand in name_to_path:
                    candidates.append(cand)
            if candidates:
                res.append(candidates[-1])
            else:
                res.append(imp)
    return res

adj = defaultdict(list)
for path_str, module in sorted(mods.items()):
    path = Path(path_str)
    try:
        tree = ast.parse(path.read_text(encoding='utf-8'))
    except Exception:
        continue
    imports = []
    for node in ast.walk(tree):
        imports.extend(module_name_from_import(node))
    for imp in resolve_imports(module, imports):
        if imp != module and imp in name_to_path:
            adj[module].append(imp)

state = {}
stack = []
cycles = []


def dfs(node):
    state[node] = 1
    stack.append(node)
    for nbr in adj.get(node, []):
        if nbr not in state:
            dfs(nbr)
        elif state[nbr] == 1:
            idx = stack.index(nbr)
            cycles.append(stack[idx:] + [nbr])
    stack.pop()
    state[node] = 2

for mod in sorted(adj):
    if mod not in state:
        dfs(mod)

print('MODULES', len(mods))
print('EDGES', sum(len(v) for v in adj.values()))
print('CYCLES', len(cycles))
for c in cycles[:20]:
    print(' -> '.join(c))

incoming = defaultdict(int)
for src, dests in adj.items():
    for d in dests:
        incoming[d] += 1
print('TOP_INCOMING')
for mod, count in sorted(incoming.items(), key=lambda x: (-x[1], x[0]))[:20]:
    print(mod, count)
