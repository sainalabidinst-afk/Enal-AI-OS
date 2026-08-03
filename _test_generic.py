import asyncio
import json
from pathlib import Path
from backend.app.core.attachments.analyzer import analyze_attachment
from backend.app.core.attachments.detector import detect_from_content

async def main():
    base = Path("real_cases/mikrotik/firewall_input_filter_strict")
    config = (base / "config.rsc").read_text(encoding="utf-8")
    meta = detect_from_content("config.rsc", config)
    result = analyze_attachment(meta, config)
    ast = result.ast.to_dict() if hasattr(result.ast, "to_dict") else result.ast
    print("VENDOR:", ast.get("vendor"))
    print("FORMAT:", ast.get("format"))
    print("FINDINGS:")
    for f in ast.get("findings", []):
        print(f"  [{f.get('severity')}] {f.get('title')}: {f.get('description')}")
    print(f"Total findings: {len(ast.get('findings', []))}")
    print("INTERFACES:", len(ast.get("interfaces", [])))
    print("FIREWALL:", len(ast.get("firewall", [])))
    print("ROUTING:", len(ast.get("routing", [])))

asyncio.run(main())
