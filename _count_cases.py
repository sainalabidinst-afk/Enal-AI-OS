from real_cases.collector import list_cases

cases = list_cases()
cats = ['cisco', 'fortinet', 'mikrotik']
for c in cats:
    count = sum(1 for x in cases if x.get('category') == c)
    print(f'{c}: {count}')
total = sum(1 for x in cases if x.get('category') in cats)
print(f'total: {total}')
