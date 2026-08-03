with open("apps/network_engineer/analyzer.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "config: Any, report: NetworkAnalysisReport)"
new = "config: Any, report: NetworkAnalysisReport, vendor: str = \"\")"
print("count:", content.count(old))
content2 = content.replace(old, new)
print("new count:", content2.count(new))

with open("apps/network_engineer/analyzer.py", "w", encoding="utf-8") as f:
    f.write(content2)
print("saved")
