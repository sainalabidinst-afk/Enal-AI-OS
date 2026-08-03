import hashlib
from pathlib import Path

root = Path('.')
files = [p for p in root.rglob('*.py') if '.venv' not in p.parts and '__pycache__' not in p.parts]
by_hash = {}
for p in files:
    try:
        data = p.read_bytes()
    except Exception:
        continue
    h = hashlib.sha1(data).hexdigest()
    by_hash.setdefault(h, []).append(str(p))

dups = {h: paths for h, paths in by_hash.items() if len(paths) > 1}
print('PY_FILES', len(files))
print('DUPLICATE_GROUPS', len(dups))
for h, paths in list(dups.items())[:20]:
    print('GROUP', h)
    for p in paths:
        print(' ', p)
