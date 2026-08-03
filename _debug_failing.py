import asyncio
from pathlib import Path
from apps.network_engineer import get_app

async def main():
    app = get_app()
    
    failing_cases = [
        "real_cases/fortinet/wireless_employee_wifi/config.txt",
        "real_cases/mikrotik/sample_hotspot/config.rsc",
        "real_cases/mikrotik/qos_traffic_shaping_enterprise/config.rsc",
        "real_cases/mikrotik/switching_vlan_switch/config.rsc",
        "real_cases/fortinet/services_dns_ntp_mgmt/config.txt",
        "real_cases/fortinet/switching_managed_vlan/config.txt",
        "real_cases/fortinet/security_admin_exposed/config.txt",
        "real_cases/cisco/nat_pat_dmz/config.txt",
        "real_cases/cisco/qos_voice_priority/config.txt",
        "real_cases/cisco/services_dns_ntp_snmp/config.txt",
    ]
    
    for path in failing_cases:
        config = Path(path).read_text(encoding="utf-8")
        result = await app.analyze_config(config)
        issues = result.get("issues", [])
        print(f"\n=== {Path(path).parent.name} ===")
        print(f"Issues: {len(issues)}")
        for issue in issues:
            print(f"  [{issue['severity']}] {issue['category']}: {issue['description']}")

asyncio.run(main())
