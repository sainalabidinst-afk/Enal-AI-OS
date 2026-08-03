import asyncio
import sys

sys.path.insert(0, ".")

from apps.network_engineer import get_app

app = get_app()

CASES = [
    "fortinet/qos_traffic_shaping",
    "fortinet/wireless_employee_wifi",
    "cisco/qos_voice_priority",
    "mikrotik/sample_hotspot",
    "mikrotik/wireless_wlan_corporate",
    "cisco/vpn_site_to_site_ipsec",
    "fortinet/security_admin_exposed",
]


async def main():
    for case in CASES:
        import glob

        cfg_files = glob.glob(f"real_cases/{case}/config.*")
        if not cfg_files:
            print(f"\n=== {case} (NO CONFIG) ===")
            continue
        text = open(cfg_files[0], encoding="utf-8").read()
        result = await app.analyze_config(text)
        print(f"\n=== {case} (vendor={result['vendor']}) ===")
        print(f"summary: {result['summary']}")
        for issue in result["issues"]:
            print(f"  [{issue['severity']}] {issue['category']}: {issue['description'][:70]}")
        print(f"  total issues: {len(result['issues'])}")


asyncio.run(main())
