import asyncio
from pathlib import Path
from apps.network_engineer import get_app

async def main():
    app = get_app()
    
    # Test a few configs
    cases = [
        ("real_cases/cisco/firewall_asa_acl_strict/config.txt", "cisco"),
        ("real_cases/fortinet/firewall_policy_dmz/config.txt", "fortinet"),
        ("real_cases/mikrotik/security_insecure_defaults/config.rsc", "mikrotik"),
    ]
    
    for path, vendor in cases:
        config = Path(path).read_text(encoding="utf-8")
        result = await app.analyze_config(config)
        issues = result.get("issues", [])
        print(f"\n=== {vendor}: {Path(path).parent.name} ===")
        print(f"Issues: {len(issues)}")
        for issue in issues:
            print(f"  [{issue['severity']}] {issue['category']}: {issue['description']}")

asyncio.run(main())
