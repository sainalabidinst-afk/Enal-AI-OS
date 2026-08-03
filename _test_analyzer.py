import asyncio
import json
from pathlib import Path
from apps.network_engineer import get_app

async def main():
    app = get_app()
    base = Path("real_cases/mikrotik/firewall_input_filter_strict")
    config = (base / "config.rsc").read_text(encoding="utf-8")
    result = await app.analyze_config(config)
    print("VENDOR:", result.get("vendor"))
    print("DEVICE:", result.get("device"))
    print("ISSUES:")
    for issue in result.get("issues", []):
        print(f"  [{issue['severity']}] {issue['category']}: {issue['description']}")
    print(f"Total issues: {len(result.get('issues', []))}")

asyncio.run(main())
