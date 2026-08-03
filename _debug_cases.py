import asyncio
import sys

sys.path.insert(0, ".")

from apps.network_engineer import get_app

app = get_app()

CASES = [
    ("cisco/nat_pat_dmz", "nat"),
    ("cisco/qos_voice_priority", "qos"),
    ("cisco/security_ssh_hardened", "ssh"),
    ("cisco/services_dns_ntp_snmp", "services"),
    ("fortinet/qos_traffic_shaping", "qos"),
    ("fortinet/services_dns_ntp_mgmt", "services"),
    ("fortinet/switching_managed_vlan", "vlan"),
    ("fortinet/wireless_employee_wifi", "wireless"),
    ("mikrotik/qos_traffic_shaping_enterprise", "qos"),
    ("mikrotik/sample_hotspot", "hotspot"),
    ("mikrotik/vpn_pptp_remote_access", "vpn"),
    ("mikrotik/wireless_wlan_corporate", "wireless"),
]


async def main():
    for path, tag in CASES:
        import glob
        files = glob.glob(f"real_cases/{path}/config.*")
        if not files:
            print(f"\n=== {path}: NO CONFIG FILE ===")
            continue
        text = open(files[0], encoding="utf-8", errors="ignore").read()
        result = await app.analyze_config(text)
        print(f"\n=== {path} (vendor={result['vendor']}) ===")
        for issue in result["issues"]:
            print(f"  [{issue['severity']}] {issue['category']}: {issue['description'][:70]}")


asyncio.run(main())
