import asyncio
from pathlib import Path
from apps.network_engineer import get_app

async def main():
    app = get_app()
    
    test_cases = [
        'real_cases/fortinet/wireless_employee_wifi/config.txt',
        'real_cases/fortinet/firewall_policy_dmz/config.txt',
        'real_cases/cisco/wireless_corporate_ssid/config.txt',
        'real_cases/mikrotik/high_availability_bgpi_peer_tracking/config.rsc',
        'real_cases/mikrotik/qos_traffic_shaping_enterprise/config.rsc',
        'real_cases/fortinet/qos_traffic_shaping/config.txt',
    ]
    
    for path in test_cases:
        config = Path(path).read_text(encoding='utf-8')
        parsed = app._parse_config(config)
        vendor = getattr(parsed, 'vendor', 'MISSING')
        result = await app.analyze_config(config)
        issues = result.get('issues', [])
        non_generic = [i for i in issues if not i['category'].startswith(('Backup', 'System:', 'Performance:', 'Interfaces:', 'Firewall:', 'Routing:', 'Security: No user'))]
        print(f"\n{path}: vendor={vendor!r}, total={len(issues)}, specific={len(non_generic)}")
        for issue in non_generic[:5]:
            print(f"  [{issue['severity']}] {issue['category']}: {issue['description']}")

asyncio.run(main())
