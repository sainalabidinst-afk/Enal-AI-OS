from real_cases.benchmark import load_cases_from_disk

cases = load_cases_from_disk()
print(f'total cases loaded: {len(cases)}')
cats = {}
for case in cases:
    cats[case.category] = cats.get(case.category, 0) + 1
for cat, count in sorted(cats.items()):
    print(f'{cat}: {count}')
