import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from real_cases.benchmark import load_cases_from_disk

cases = load_cases_from_disk()
print(f"Total cases from load_cases_from_disk: {len(cases)}")

network_cases = [c for c in cases if c.category in {"network", "mikrotik", "cisco", "fortinet"}]
print(f"After filtering: {len(network_cases)}")

for c in network_cases[:3]:
    p = Path(c.source_files[0]) if c.source_files else None
    print(f"  {c.id}: category={c.category}, vendor={c.vendor}, path_exists={p.exists() if p else False}")
