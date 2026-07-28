"""
Multi-Vendor Golden Tests
=========================

Tests Network Engineer with MikroTik, Cisco IOS, and Fortinet configs.
"""

import pytest
from pathlib import Path

from apps.network_engineer import get_app
from apps.network_engineer.vendor.detector import detect_vendor, parse_config

GOLDEN_DIR = Path(__file__).resolve().parents[2] / "golden"


def load_config(scenario_path: Path) -> str:
    return (scenario_path / "config.rsc").read_text(encoding="utf-8")


@pytest.mark.asyncio
async def test_vendor_detection():
    """Test vendor auto-detection."""
    mikrotik_config = (GOLDEN_DIR / "mikrotik" / "home" / "config.rsc").read_text(encoding="utf-8")
    cisco_config = (GOLDEN_DIR / "cisco" / "home" / "config.rsc").read_text(encoding="utf-8")
    fortinet_config = (GOLDEN_DIR / "fortinet" / "home" / "config.rsc").read_text(encoding="utf-8")

    assert detect_vendor(mikrotik_config) == "mikrotik", "Should detect MikroTik"
    assert detect_vendor(cisco_config) == "cisco", "Should detect Cisco"
    assert detect_vendor(fortinet_config) == "fortinet", "Should detect Fortinet"


@pytest.mark.asyncio
async def test_mikrotik_analysis():
    app = get_app()
    config = load_config(GOLDEN_DIR / "mikrotik" / "home")
    result = await app.analyze_config(config)
    assert len(result["issues"]) > 0, "Should find issues"
    assert result["device"] != "", "Should have device name"


@pytest.mark.asyncio
async def test_cisco_analysis():
    app = get_app()
    config = load_config(GOLDEN_DIR / "cisco" / "home")
    result = await app.analyze_config(config)
    assert len(result["issues"]) > 0, "Should find issues"


@pytest.mark.asyncio
async def test_fortinet_analysis():
    app = get_app()
    config = load_config(GOLDEN_DIR / "fortinet" / "home")
    result = await app.analyze_config(config)
    assert len(result["issues"]) > 0, "Should find issues"


@pytest.mark.asyncio
async def test_cisco_expanded_parsing():
    """Test expanded Cisco IOS parser with more features."""
    config = load_config(GOLDEN_DIR / "cisco" / "home-expanded")
    ast = parse_config(config, vendor="cisco")

    assert ast.vendor == "cisco"
    assert ast.system.hostname == "cisco-home-router"
    assert len(ast.interfaces) >= 2, "Should have at least 2 interfaces"
    assert len(ast.vlans) == 2, "Should have 2 VLANs"
    assert any(v.name == "Management" for v in ast.vlans), "Should have Management VLAN"
    assert any(v.name == "Users" for v in ast.vlans), "Should have Users VLAN"
    assert len(ast.routes) == 2, "Should have 2 routes"
    assert any(r.dst_address == "0.0.0.0/0" for r in ast.routes), "Should have default route"
    assert len(ast.dhcp_servers) == 1, "Should have 1 DHCP server"
    assert len(ast.users) == 2, "Should have 2 users"
    assert ast.system.ntp_enabled is True, "NTP should be enabled"
    assert ast.system.logging_enabled is True, "Logging should be enabled"
    assert ast.dns is not None, "DNS should be configured"


@pytest.mark.asyncio
async def test_fortinet_expanded_parsing():
    """Test expanded Fortinet parser with more features."""
    config = load_config(GOLDEN_DIR / "fortinet" / "home-expanded")
    ast = parse_config(config, vendor="fortinet")

    assert ast.vendor == "fortinet"
    assert ast.system.hostname == "fortinet-home-expanded"
    assert len(ast.interfaces) >= 3, "Should have at least 3 interfaces"
    assert len(ast.vlans) == 2, "Should have 2 VLANs"
    assert len(ast.routes) >= 1, "Should have routes"
    assert len(ast.dhcp_servers) == 1, "Should have 1 DHCP server"
    assert ast.dns is not None and len(ast.dns.servers) == 2, "Should have 2 DNS servers"
    assert ast.system.ntp_enabled is True, "NTP should be enabled"
    assert ast.system.logging_enabled is True, "Logging should be enabled"
    assert len(ast.vpns) >= 1, "Should have VPN configured"
    assert len(ast.users) == 2, "Should have 2 users"


@pytest.mark.asyncio
async def test_cross_vendor_documentation():
    app = get_app()

    mikrotik_config = load_config(GOLDEN_DIR / "mikrotik" / "home")
    cisco_config = load_config(GOLDEN_DIR / "cisco" / "home")
    fortinet_config = load_config(GOLDEN_DIR / "fortinet" / "home")

    mikrotik_docs = await app.generate_documentation(mikrotik_config)
    cisco_docs = await app.generate_documentation(cisco_config)
    fortinet_docs = await app.generate_documentation(fortinet_config)

    assert len(mikrotik_docs) > 0, "MikroTik docs should not be empty"
    assert len(cisco_docs) > 0, "Cisco docs should not be empty"
    assert len(fortinet_docs) > 0, "Fortinet docs should not be empty"