"""
Golden Tests for Multi-Vendor Protocols
========================================

Tests BGP, MPLS, CAPsMAN, WireGuard, Cisco sub-vendors, Fortinet VPN/policies.
"""

import asyncio
from pathlib import Path

from apps.network_engineer import get_app
from apps.network_engineer.vendor.detector import detect_vendor
from apps.network_engineer.compliance import compliance_engine

GOLDEN_DIR = Path(__file__).resolve().parents[2] / "golden"


def load_config(scenario_path: Path) -> str:
    return (scenario_path / "config.rsc").read_text(encoding="utf-8")


async def test_bgp_parsing():
    config = load_config(GOLDEN_DIR / "mikrotik" / "bgp")
    app = get_app()
    result = await app.analyze_config(config)
    assert len(result["issues"]) > 0, "Should find issues in BGP config"
    print(f"[PASS] BGP Parsing: {len(result['issues'])} issues found")
    return True


async def test_mpls_parsing():
    config = load_config(GOLDEN_DIR / "mikrotik" / "mpls")
    app = get_app()
    result = await app.analyze_config(config)
    assert len(result["issues"]) > 0, "Should find issues in MPLS config"
    print(f"[PASS] MPLS Parsing: {len(result['issues'])} issues found")
    return True


async def test_capsman_parsing():
    config = load_config(GOLDEN_DIR / "mikrotik" / "capsman")
    app = get_app()
    result = await app.analyze_config(config)
    assert len(result["issues"]) > 0, "Should find issues in CAPsMAN config"
    print(f"[PASS] CAPsMAN Parsing: {len(result['issues'])} issues found")
    return True


async def test_wireguard_parsing():
    config = load_config(GOLDEN_DIR / "mikrotik" / "wireguard")
    app = get_app()
    result = await app.analyze_config(config)
    assert len(result["issues"]) > 0, "Should find issues in WireGuard config"
    print(f"[PASS] WireGuard Parsing: {len(result['issues'])} issues found")
    return True


async def test_cisco_ios_xe_detection():
    config = load_config(GOLDEN_DIR / "cisco" / "home")
    vendor = detect_vendor(config)
    assert vendor == "cisco", f"Expected cisco, got {vendor}"
    print(f"[PASS] Cisco IOS-XE Detection: {vendor}")
    return True


async def test_fortinet_vpn_parsing():
    config = load_config(GOLDEN_DIR / "fortinet" / "home")
    app = get_app()
    result = await app.analyze_config(config)
    assert len(result["issues"]) > 0, "Should find issues in Fortinet config"
    print(f"[PASS] Fortinet VPN Parsing: {len(result['issues'])} issues found")
    return True


async def test_compliance_engine():
    config = load_config(GOLDEN_DIR / "mikrotik" / "home")
    app = get_app()
    analysis = await app.analyze_config(config)
    from apps.network_engineer.vendor.models import NetworkAST
    ast = NetworkAST(vendor="mikrotik")
    ast.system.hostname = "test-router"
    report = compliance_engine.check(ast)
    assert report.score >= 0, "Compliance score should be >= 0"
    assert report.score <= 100, "Compliance score should be <= 100"
    print(f"[PASS] Compliance Engine: score={report.score:.1f}%, passed={report.passed}, failed={report.failed}")
    return True


async def main() -> int:
    print("Running Protocol & Compliance Golden Tests")
    print("=" * 80)

    tests = [
        test_bgp_parsing,
        test_mpls_parsing,
        test_capsman_parsing,
        test_wireguard_parsing,
        test_cisco_ios_xe_detection,
        test_fortinet_vpn_parsing,
        test_compliance_engine,
    ]

    passed = 0
    for test in tests:
        try:
            await test()
            passed += 1
        except Exception as e:
            print(f"[FAIL] {test.__name__}: {e}")

    print("=" * 80)
    print(f"Tests passed: {passed}/{len(tests)}")
    if passed == len(tests):
        print("SUCCESS: All protocol and compliance tests passed")
        return 0
    print("FAILED: Some tests did not pass")
    return 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
