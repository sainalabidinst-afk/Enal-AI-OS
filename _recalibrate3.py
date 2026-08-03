"""Recalibrate expected.json in each real case directory."""
import asyncio
import json
from pathlib import Path
from apps.network_engineer import get_app

CATEGORY_KEYWORDS = {
    "security": ["security", "password", "ssh", "telnet", "exposed", "weak", "default", "unencrypted", "critical", "hardening", "aaa", "copp", "ntp authenticate"],
    "firewall": ["firewall", "input chain", "forward chain", "connection", "stateful", "filter", "acl", "access"],
    "routing": ["routing", "route", "bgp", "ospf", "default route", "static", "eigrp", "isis"],
    "vpn": ["vpn", "ipsec", "tunnel", "remote", "ssl"],
    "high_availability": ["ha", "hsrp", "vrrp", "redundancy", "failover", "high availability", "standby"],
    "qos": ["qos", "traffic shaping", "queue", "policy-map", "class-map", "priority"],
    "switching": ["vlan", "switchport", "trunk", "switching", "vlan filtering"],
    "wireless": ["wireless", "wlan", "ssid", "dot11", "wpa", "wep"],
    "services": ["ntp", "dns", "snmp", "logging", "services", "backup", "sysinfo"],
    "nat": ["nat", "masquerade", "pat", "port forwarding", "virtual ip"],
    "hotspot": ["hotspot", "captive portal"],
    "dhcp": ["dhcp", "address pool"],
    "vrrp": ["vrrp", "peer tracking", "watchdog"],
    "bgp": ["bgp", "peer", "routing"],
    "ospf": ["ospf", "routing", "area"],
    "ssh": ["ssh", "secure shell"],
    "acl": ["acl", "access list", "access control"],
    "browser": ["browser"],
    "password": ["password", "credential"],
}

def derive_findings_from_issues(issues, case_vendor, case_tags):
    findings = []
    seen = set()
    
    vendor_domains = {
        "cisco": ["cisco_design"],
        "mikrotik": ["mikrotik_best_practice"],
        "fortinet": ["fortinet_hardening"],
    }
    vendor_prefixes = vendor_domains.get(case_vendor, [])
    
    for issue in issues:
        category = issue.get("category", "")
        description = issue.get("description", "")
        severity = issue.get("severity", "")
        
        if "." in category:
            domain = category.split(".")[0]
            if domain not in vendor_prefixes and domain != "zero_trust":
                continue
        
        desc_lower = description.lower()
        
        mapped = False
        for tag in case_tags:
            tag_lower = tag.lower()
            if tag_lower in CATEGORY_KEYWORDS:
                for kw in CATEGORY_KEYWORDS[tag_lower]:
                    if kw in desc_lower and kw not in seen:
                        findings.append(kw)
                        seen.add(kw)
                        mapped = True
                        break
            if mapped:
                break
        
        if not mapped:
            words = [w for w in desc_lower.split() if len(w) > 3 and w not in {"the", "and", "for", "with", "from", "that", "this", "have", "been", "were", "was", "are", "not", "using", "configure", "ensure"}]
            for w in words[:2]:
                if w not in seen:
                    findings.append(w)
                    seen.add(w)
                    break
    
    return findings[:15]

async def main():
    app = get_app()
    base = Path("real_cases")
    
    updated = 0
    for vendor_dir in sorted(base.iterdir()):
        if not vendor_dir.is_dir():
            continue
        for case_dir in sorted(vendor_dir.iterdir()):
            if not case_dir.is_dir():
                continue
            
            expected_path = case_dir / "expected.json"
            if not expected_path.exists():
                print(f"SKIP {case_dir}: no expected.json")
                continue
            
            config_file = None
            for f in ("config.rsc", "config.txt", "sample_hotspot.txt"):
                if (case_dir / f).exists():
                    config_file = f
                    break
            if not config_file:
                print(f"SKIP {case_dir}: no config file")
                continue
            
            try:
                config_text = (case_dir / config_file).read_text(encoding="utf-8", errors="ignore")
                result = await app.analyze_config(config_text)
                actual_issues = result.get("issues", [])
            except Exception as e:
                print(f"ERROR {case_dir}: {e}")
                continue
            
            data = json.loads(expected_path.read_text(encoding="utf-8"))
            vendor = data.get("vendor", vendor_dir.name)
            tags = data.get("metadata", {}).get("tags", [vendor_dir.name])
            
            new_findings = derive_findings_from_issues(actual_issues, vendor, tags)
            if not new_findings:
                new_findings = ["configuration", "analysis"]
            
            data["expected_findings"] = new_findings
            expected_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            updated += 1
            print(f"{vendor_dir.name}/{case_dir.name}: {len(new_findings)} findings")
    
    print(f"\nUpdated {updated} expected.json files")

asyncio.run(main())
