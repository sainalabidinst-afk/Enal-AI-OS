"""
Test Knowledge Layer
======================

Tests Network Ontology, Concept Enricher, and Compliance Profiles.
"""

from pathlib import Path

import pytest

from apps.network_engineer import get_app
from apps.network_engineer.nic.knowledge.enricher import knowledge_enricher
from apps.network_engineer.nic.knowledge.ontology import UniversalConcept
from apps.network_engineer.nic.knowledge.profiles import (
    PROFILES,
    get_compliance_engine,
)
from apps.network_engineer.vendor.detector import parse_config

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


def test_ontology_fortinet_ha():
    config = load_config(GOLDEN_DIR / "fortinet" / "home-expanded")
    ast = parse_config(config, vendor="fortinet")
    tags = knowledge_enricher.enrich(ast)
    concepts = [tag.concept for tag in tags]
    assert UniversalConcept.HIGH_AVAILABILITY in concepts, "Should detect HA concept"
    assert UniversalConcept.VPN in concepts, "Should detect VPN concept"


def test_cross_vendor_ha_mapping():
    cisco_ha = knowledge_enricher.get_cross_vendor_mapping("hsrp", "cisco", "fortinet")
    fortinet_ha = knowledge_enricher.get_cross_vendor_mapping("ha", "fortinet", "cisco")
    mikrotik_ha = knowledge_enricher.get_cross_vendor_mapping("vrrp", "mikrotik", "cisco")
    assert cisco_ha == "ha", f"Cisco HSRP should map to Fortinet HA, got {cisco_ha}"
    assert fortinet_ha == "hsrp", f"Fortinet HA should map to Cisco HSRP, got {fortinet_ha}"
    assert mikrotik_ha == "hsrp", f"MikroTik VRRP should map to Cisco HSRP, got {mikrotik_ha}"


def test_cross_vendor_firewall_mapping():
    cisco_fw = knowledge_enricher.get_cross_vendor_mapping("acl", "cisco", "mikrotik")
    fortinet_fw = knowledge_enricher.get_cross_vendor_mapping("firewall_policy", "fortinet", "mikrotik")
    mikrotik_fw = knowledge_enricher.get_cross_vendor_mapping("firewall_filter", "mikrotik", "cisco")
    assert cisco_fw == "firewall filter", f"Cisco ACL should map to MikroTik firewall filter, got {cisco_fw}"
    assert fortinet_fw == "firewall filter", f"Fortinet policy should map to MikroTik firewall filter, got {fortinet_fw}"
    assert mikrotik_fw == "access-list", f"MikroTik filter should map to Cisco ACL, got {mikrotik_fw}"


def test_compliance_cis_cisco():
    config = load_config(GOLDEN_DIR / "cisco" / "home-expanded")
    engine = get_compliance_engine("CIS")
    ast = parse_config(config, vendor="cisco")
    report = engine.check(ast)
    assert report.profile == "CIS"
    assert report.score >= 0
    assert len(report.checks) > 0


def test_compliance_cis_fortinet():
    config = load_config(GOLDEN_DIR / "fortinet" / "home-expanded")
    engine = get_compliance_engine("CIS")
    ast = parse_config(config, vendor="fortinet")
    report = engine.check(ast)
    assert report.profile == "CIS"
    assert report.score >= 0


def test_compliance_nist():
    config = load_config(GOLDEN_DIR / "cisco" / "home-expanded")
    engine = get_compliance_engine("NIST")
    ast = parse_config(config, vendor="cisco")
    report = engine.check(ast)
    assert report.profile == "NIST"
    assert len(report.checks) == 4, f"NIST should have 4 rules, got {len(report.checks)}"


def test_compliance_pci_dss():
    config = load_config(GOLDEN_DIR / "fortinet" / "home-expanded")
    engine = get_compliance_engine("PCI-DSS")
    ast = parse_config(config, vendor="fortinet")
    report = engine.check(ast)
    assert report.profile == "PCI-DSS"
    assert len(report.checks) == 4, f"PCI-DSS should have 4 rules, got {len(report.checks)}"


def test_compliance_profiles_list():
    assert "CIS" in PROFILES
    assert "NIST" in PROFILES
    assert "PCI-DSS" in PROFILES
    assert "ISP-Best-Practice" in PROFILES
    assert "SMB-Best-Practice" in PROFILES


@pytest.mark.asyncio
async def test_app_compliance_integration():
    app = get_app()
    cisco_config = load_config(GOLDEN_DIR / "cisco" / "home-expanded")
    result = await app.check_compliance(cisco_config, profile="CIS")
    assert result["profile"] == "CIS"
    assert "score" in result
    assert len(result["checks"]) > 0


@pytest.mark.asyncio
async def test_app_explain_finding():
    app = get_app()
    cisco_config = load_config(GOLDEN_DIR / "cisco" / "home-expanded")
    explanation = await app.explain_finding(cisco_config, "Firewall")
    assert explanation is not None
    assert "traffic" in explanation.lower() or "filter" in explanation.lower()


@pytest.mark.asyncio
async def test_app_translate_config():
    app = get_app()
    mikrotik_config = load_config(GOLDEN_DIR / "mikrotik" / "home")
    result = await app.translate_config(mikrotik_config, target_vendor="cisco")
    assert result["status"] == "not_implemented"
    assert result["source_vendor"] == "mikrotik"
    assert result["target_vendor"] == "cisco"


@pytest.mark.asyncio
async def test_app_generate_documentation_with_concepts():
    app = get_app()
    cisco_config = load_config(GOLDEN_DIR / "cisco" / "home-expanded")
    docs = await app.generate_documentation(cisco_config)
    assert "Detected Concepts" in docs
    assert "High Availability" in docs or "high availability" in docs