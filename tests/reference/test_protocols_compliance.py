"""
Golden Tests for Multi-Vendor Protocols
========================================

Tests BGP, MPLS, CAPsMAN, WireGuard, Cisco sub-vendors, Fortinet VPN/policies.
"""

import pytest
from pathlib import Path

from apps.network_engineer import get_app
from apps.network_engineer.compliance import compliance_engine
from apps.network_engineer.vendor.detector import detect_vendor

GOLDEN_DIR = Path(__file__).resolve().parents[2] / "golden"


def load_config(scenario_path: Path) -> str:
    return (scenario_path / "config.rsc").read_text(encoding="utf-8")


@pytest.mark.asyncio
async def test_bgp_parsing():
    config = load_config(GOLDEN_DIR / "mikrotik" / "bgp")
    app = get_app()
    result = await app.analyze_config(config)
    assert len(result["issues"]) > 0, "Should find issues in BGP config"


@pytest.mark.asyncio
async def test_mpls_parsing():
    config = load_config(GOLDEN_DIR / "mikrotik" / "mpls")
    app = get_app()
    result = await app.analyze_config(config)
    assert len(result["issues"]) > 0, "Should find issues in MPLS config"


@pytest.mark.asyncio
async def test_capsman_parsing():
    config = load_config(GOLDEN_DIR / "mikrotik" / "capsman")
    app = get_app()
    result = await app.analyze_config(config)
    assert len(result["issues"]) > 0, "Should find issues in CAPsMAN config"


@pytest.mark.asyncio
async def test_wireguard_parsing():
    config = load_config(GOLDEN_DIR / "mikrotik" / "wireguard")
    app = get_app()
    result = await app.analyze_config(config)
    assert len(result["issues"]) > 0, "Should find issues in WireGuard config"


@pytest.mark.asyncio
async def test_cisco_ios_xe_detection():
    config = load_config(GOLDEN_DIR / "cisco" / "home")
    vendor = detect_vendor(config)
    assert vendor == "cisco", f"Expected cisco, got {vendor}"


@pytest.mark.asyncio
async def test_fortinet_vpn_parsing():
    config = load_config(GOLDEN_DIR / "fortinet" / "home")
    app = get_app()
    result = await app.analyze_config(config)
    assert len(result["issues"]) > 0, "Should find issues in Fortinet config"


@pytest.mark.asyncio
async def test_compliance_engine():
    config = load_config(GOLDEN_DIR / "mikrotik" / "home")
    app = get_app()
    await app.analyze_config(config)
    from apps.network_engineer.vendor.models import NetworkAST
    ast = NetworkAST(vendor="mikrotik")
    ast.system.hostname = "test-router"
    report = compliance_engine.check(ast)
    assert report.score >= 0, "Compliance score should be >= 0"
    assert report.score <= 100, "Compliance score should be <= 100"