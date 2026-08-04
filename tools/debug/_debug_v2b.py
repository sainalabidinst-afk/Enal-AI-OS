import asyncio
from pathlib import Path
from apps.network_engineer import get_app

async def main():
    app = get_app()
    
    test_cases = [
        ('real_cases/fortinet/wireless_employee_wifi/config.txt', 'fortinet wifi'),
        ('real_cases/mikrotik/qos_traffic_shaping_enterprise/config.rsc', 'mikrotik qos'),
        ('real_cases/fortinet/qos_traffic_shaping/config.txt', 'fortinet qos'),
        ('real_cases/cisco/wireless_corporate_ssid/config.txt', 'cisco wireless'),
        ('real_cases/mikrotik/high_availability_bgpi_peer_tracking/config.rsc', 'mikrotik ha'),
    ]
    
    for path, name in test_cases:
        config = Path(path).read_text(encoding='utf-8')
        result = await app.analyze_config(config)
        issues = result.get('issues', [])
        print(f"\n=== {name} ({len(issues)} issues) ===")
        for issue in issues:
            print(f"  [{issue['severity']}] {issue['category']}: {issue['description']}")

asyncio.run(main())
