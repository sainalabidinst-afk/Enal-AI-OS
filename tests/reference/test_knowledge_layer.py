"""
Test Knowledge Layer
=====================

Tests Network Ontology, Concept Enricher, and Compliance Profiles.
"""

import asyncio
from pathlib import Path

from apps.network_engineer import get_app
from apps.network_engineer.vendor.detector import detect_vendor, parse_config
from apps.network_engineer.nic.knowledge.ontology import concept_mapper, UniversalConcept
from apps.network_engineer.nic.knowledge.enricher import knowledge_enricher
from apps.network_engineer.nic.knowledge.profiles import (
    get_compliance_engine,
    CISProfile,
    NISTProfile,
    PCIDSSProfile,
    PROFILES,
)

GOLDEN_DIR = Path(__file__).resolve().parents[2] / "golden"


def load_config(path: Path) -> str:
    return (path / "config.rsc").read_text(encoding="utf-8")


def test_ontology_cisco_ha():
    config = load_config(GOLDEN_DIR / "cisco" / "home-expanded")
    ast = parse_config(config, vendor="cisco")
    tags = knowledge_enricher.enrich(ast)
    concepts = [tag.concept for tag in tags]
    assert UniversalConcept.HIGH_AVAILABILITY in concepts, "Should detect HSRP as HA concept"
    assert UniversalConcept.TRAFFIC_FILTERING in concepts, "Should detect ACL as Traffic Filtering"
    print(f"[PASS] Cisco Ontology: detected {len(tags)} concepts")
    return True


def test_ontology_fortinet_ha():
    config = load_config(GOLDEN_DIR / "fortinet" / "home-expanded")
    ast = parse_config(config, vendor="fortinet")
    tags = knowledge_enricher.enrich(ast)
    concepts = [tag.concept for tag in tags]
    assert UniversalConcept.HIGH_AVAILABILITY in concepts, "Should detect HA concept"
    assert UniversalConcept.VPN in concepts, "Should detect VPN concept"
    print(f"[PASS] Fortinet Ontology: detected {len(tags)} concepts")
    return True


def test_cross_vendor_ha_mapping():
    cisco_ha = knowledge_enricher.get_cross_vendor_mapping("hsrp", "cisco", "fortinet")
    fortinet_ha = knowledge_enricher.get_cross_vendor_mapping("ha", "fortinet", "cisco")
    mikrotik_ha = knowledge_enricher.get_cross_vendor_mapping("vrrp", "mikrotik", "cisco")
    assert cisco_ha == "ha", f"Cisco HSRP should map to Fortinet HA, got {cisco_ha}"
    assert fortinet_ha == "hsrp", f"Fortinet HA should map to Cisco HSRP, got {fortinet_ha}"
    assert mikrotik_ha == "hsrp", f"MikroTik VRRP should map to Cisco HSRP, got {mikrotik_ha}"
    print("[PASS] Cross-Vendor HA Mapping: hsrp ↔ ha ↔ vrrp")
    return True


def test_cross_vendor_firewall_mapping():
    cisco_fw = knowledge_enricher.get_cross_vendor_mapping("acl", "cisco", "mikrotik")
    fortinet_fw = knowledge_enricher.get_cross_vendor_mapping("firewall_policy", "fortinet", "mikrotik")
    mikrotik_fw = knowledge_enricher.get_cross_vendor_mapping("firewall_filter", "mikrotik", "cisco")
    assert cisco_fw == "firewall filter", f"Cisco ACL should map to MikroTik firewall filter, got {cisco_fw}"
    assert fortinet_fw == "firewall filter", f"Fortinet policy should map to MikroTik firewall filter, got {fortinet_fw}"
    assert mikrotik_fw == "access-list", f"MikroTik filter should map to Cisco ACL, got {mikrotik_fw}"
    print("[PASS] Cross-Vendor Firewall Mapping: acl ↔ firewall_policy ↔ firewall_filter")
    return True


def test_compliance_cis_cisco():
    config = load_config(GOLDEN_DIR / "cisco" / "home-expanded")
    engine = get_compliance_engine("CIS")
    from apps.network_engineer.vendor.detector import parse_config
    ast = parse_config(config, vendor="cisco")
    report = engine.check(ast)
    assert report.profile == "CIS"
    assert report.score >= 0
    assert len(report.checks) > 0
    passed = sum(1 for c in report.checks if c.status == "pass")
    failed = sum(1 for c in report.checks if c.status == "fail")
    print(f"[PASS] CIS Compliance (Cisco): score={report.score:.1f}%, passed={passed}, failed={failed}")
    return True


def test_compliance_cis_fortinet():
    config = load_config(GOLDEN_DIR / "fortinet" / "home-expanded")
    engine = get_compliance_engine("CIS")
    from apps.network_engineer.vendor.detector import parse_config
    ast = parse_config(config, vendor="fortinet")
    report = engine.check(ast)
    assert report.profile == "CIS"
    assert report.score >= 0
    print(f"[PASS] CIS Compliance (Fortinet): score={report.score:.1f}%")
    return True


def test_compliance_nist():
    config = load_config(GOLDEN_DIR / "cisco" / "home-expanded")
    engine = get_compliance_engine("NIST")
    from apps.network_engineer.vendor.detector import parse_config
    ast = parse_config(config, vendor="cisco")
    report = engine.check(ast)
    assert report.profile == "NIST"
    assert len(report.checks) == 4, f"NIST should have 4 rules, got {len(report.checks)}"
    print(f"[PASS] NIST Compliance: {len(report.checks)} rules checked")
    return True


def test_compliance_pci_dss():
    config = load_config(GOLDEN_DIR / "fortinet" / "home-expanded")
    engine = get_compliance_engine("PCI-DSS")
    from apps.network_engineer.vendor.detector import parse_config
    ast = parse_config(config, vendor="fortinet")
    report = engine.check(ast)
    assert report.profile == "PCI-DSS"
    assert len(report.checks) == 4, f"PCI-DSS should have 4 rules, got {len(report.checks)}"
    print(f"[PASS] PCI-DSS Compliance: {len(report.checks)} rules checked")
    return True


def test_compliance_profiles_list():
    assert "CIS" in PROFILES
    assert "NIST" in PROFILES
    assert "PCI-DSS" in PROFILES
    assert "ISP-Best-Practice" in PROFILES
    assert "SMB-Best-Practice" in PROFILES
    print("[PASS] Compliance Profiles: CIS, NIST, PCI-DSS, ISP-Best-Practice, SMB-Best-Practice")
    return True


async def test_app_compliance_integration():
    app = get_app()
    cisco_config = load_config(GOLDEN_DIR / "cisco" / "home-expanded")
    result = await app.check_compliance(cisco_config, profile="CIS")
    assert result["profile"] == "CIS"
    assert "score" in result
    assert len(result["checks"]) > 0
    print(f"[PASS] App Compliance Integration: CIS score={result['score']:.1f}%")
    return True


async def test_app_explain_finding():
    app = get_app()
    cisco_config = load_config(GOLDEN_DIR / "cisco" / "home-expanded")
    explanation = await app.explain_finding(cisco_config, "Firewall")
    assert explanation is not None
    assert "traffic" in explanation.lower() or "filter" in explanation.lower()
    print(f"[PASS] Explain Finding: {explanation[:60]}...")
    return True


async def test_app_translate_config():
    app = get_app()
    mikrotik_config = load_config(GOLDEN_DIR / "mikrotik" / "home")
    result = await app.translate_config(mikrotik_config, target_vendor="cisco")
    assert result["status"] == "not_implemented"
    assert result["source_vendor"] == "mikrotik"
    assert result["target_vendor"] == "cisco"
    print(f"[PASS] Cross-Vendor Translation: {result['source_vendor']} -> {result['target_vendor']}")
    return True


async def test_app_generate_documentation_with_concepts():
    app = get_app()
    cisco_config = load_config(GOLDEN_DIR / "cisco" / "home-expanded")
    docs = await app.generate_documentation(cisco_config)
    assert "Detected Concepts" in docs
    assert "High Availability" in docs or "high availability" in docs
    print(f"[PASS] Documentation with Concepts: {len(docs)} chars")
    return True


async def main() -> int:
    print("Running Knowledge Layer Tests")
    print("=" * 80)

    tests = [
        test_ontology_cisco_ha,
        test_ontology_fortinet_ha,
        test_cross_vendor_ha_mapping,
        test_cross_vendor_firewall_mapping,
        test_compliance_cis_cisco,
        test_compliance_cis_fortinet,
        test_compliance_nist,
        test_compliance_pci_dss,
        test_compliance_profiles_list,
        test_app_compliance_integration,
        test_app_explain_finding,
        test_app_translate_config,
        test_app_generate_documentation_with_concepts,
    ]

    passed = 0
    for test in tests:
        try:
            if asyncio.iscoroutinefunction(test):
                await test()
            else:
                test()
            passed += 1
        except Exception as e:
            print(f"[FAIL] {test.__name__}: {e}")

    print("=" * 80)
    print(f"Tests passed: {passed}/{len(tests)}")
    if passed == len(tests):
        print("SUCCESS: All knowledge layer tests passed")
        return 0
    print("FAILED: Some tests did not pass")
    return 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
