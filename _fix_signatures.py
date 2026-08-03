import re

with open("apps/network_engineer/analyzer.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace all rule signatures
old = "(config: Any, report: NetworkAnalysisReport)"
new = "(config: Any, report: NetworkAnalysisReport, vendor: str = '')"
count = content.count(old)
print(f"Found {count} occurrences")
content = content.replace(old, new)

with open("apps/network_engineer/analyzer.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Done")
