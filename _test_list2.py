from real_cases.collector import list_cases
cases = list_cases()
cats = {}
for c in cases:
    cat = c.get('category')
    cats[cat] = cats.get(cat, 0) + 1
for cat, count in sorted(cats.items(), key=lambda x: x[1], reverse=True):
    print(f'{cat}: {count}')
