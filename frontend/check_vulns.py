import json
with open('npm_audit.json', 'rb') as f:
    data = json.load(f)
vulns = data.get('vulnerabilities', {})
for k, v in vulns.items():
    if isinstance(v, dict) and v.get('severity') == 'high':
        print(f"=== {k} ===")
        print(f"  name: {v.get('name')}")
        print(f"  title: {v.get('title')}")
        via = v.get('via', [])
        for item in via:
            if isinstance(item, dict):
                title = item.get('title', item.get('url', ''))
                print(f"  via: {item.get('name')} - {str(title)[:100]}")
        print()
