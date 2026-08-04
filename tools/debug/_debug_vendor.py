import asyncio
from pathlib import Path
from apps.network_engineer import get_app

async def main():
    app = get_app()
    
    test_cases = [
        'real_cases/fortinet/wireless_employee_wifi/config.txt',
        'real_cases/fortinet/firewall_policy_dmz/config.txt',
    ]
    
    for path in test_cases:
        config = Path(path).read_text(encoding='utf-8')
        parsed = app._parse_config(config)
        vendor = getattr(parsed, 'vendor', 'MISSING')
        raw_lines = getattr(parsed, 'raw_lines', [])
        print(f"{path}: vendor={vendor!r}, type={type(parsed).__name__}, raw_lines_count={len(raw_lines)}")

asyncio.run(main())
