import asyncio
import sys

sys.path.insert(0, ".")

from apps.network_engineer import get_app

app = get_app()


async def main():
    text = open("real_cases/cisco/firewall_asa_acl_strict/config.txt", encoding="utf-8").read()
    result = await app.analyze_config(text)
    print("vendor:", result["vendor"])
    print("summary:", result["summary"])
    for issue in result["issues"][:20]:
        print(f"  [{issue['severity']}] {issue['category']}: {issue['description'][:80]}")


asyncio.run(main())
