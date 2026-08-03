import asyncio
from pathlib import Path
from apps.network_engineer import get_app

async def main():
    app = get_app()
    
    # Check Cisco firewall
    config = Path('real_cases/cisco/firewall_asa_acl_strict/config.txt').read_text(encoding='utf-8')
    result = await app.analyze_config(config)
    print("=== Cisco Firewall ===")
    for issue in result.get('issues', []):
        print(f"  [{issue['severity']}] {issue['category']}: {issue['description']}")
    print(f"Total: {len(result.get('issues', []))}")
    
    # Check MikroTik switching
    config = Path('real_cases/mikrotik/switching_vlan_switch/config.rsc').read_text(encoding='utf-8')
    result = await app.analyze_config(config)
    print("\n=== MikroTik Switching ===")
    for issue in result.get('issues', []):
        print(f"  [{issue['severity']}] {issue['category']}: {issue['description']}")
    print(f"Total: {len(result.get('issues', []))}")

asyncio.run(main())
