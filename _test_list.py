from real_cases.collector import list_cases
cases = list_cases()
print(f'total: {len(cases)}')
for c in cases[:3]:
    print(c.get('id'), c.get('category'))
