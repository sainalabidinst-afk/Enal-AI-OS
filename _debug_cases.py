import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from real_cases.benchmark import load_cases_from_disk

cases = load_cases_from_disk()
print(f"Total cases loaded: {len(cases)}")

# Check categories
cats = {}
for c in cases:
    cats[c.category] = cats.get(c.category, 0) + 1
print("Categories:", cats)

# Check first case
if cases:
    c = cases[0]
    print(f"\nFirst case:")
    print(f"  id: {c.id}")
    print(f"  category: {c.category}")
    print(f"  vendor: {c.vendor}")
    print(f"  source_files: {c.source_files}")
    if c.source_files:
        p = Path(c.source_files[0])
        print(f"  path exists: {p.exists()}")
