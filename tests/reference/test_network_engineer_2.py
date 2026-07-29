"""
Network Engineer 2.0 Tests
===========================

Tests for:
- Design Review (N2)
- Troubleshooting Engine (N3)
- Migration Planner (N4)
- Network Advisor (N5)
"""

import asyncio
import json

from apps.network_engineer import get_app
from apps.network_engineer.advisor import NetworkAdvisor, network_advisor
from apps.network_engineer.design_review import DesignReviewEngine, design_review_engine
from apps.network_engineer.migration_planner import MigrationPlanner, migration_planner
from apps.network_engineer.topology import (
    DeviceType,
    InterfaceType,
    NetworkConnection,
    NetworkDevice,
    NetworkInterface,
    NetworkSegment,
    NetworkTopology,
    RedundancyRole,
)
from apps.network_engineer.troubleshooting import (
    TroubleshootingEngine,
    troubleshooting_engine,
)


def test_design_review_detects_spof():
    topology = NetworkTopology()
    router = NetworkDevice(
        id="router-1",
        name="core-router",
        device_type=DeviceType.ROUTER,
        interfaces=[
            NetworkInterface(name="ether1", interface_type=InterfaceType.ETHERNET, ip_address="203.0.113.1/24"),
            NetworkInterface(name="ether2", interface_type=InterfaceType.ETHERNET, ip_address="10.0.0.1/24"),
        ],
    )
    topology.add_device(router)

    async def run():
        report = await design_review_engine.review(topology)
        data = report.to_dict()
        assert data["network_score"] >= 0
        assert data["availability_grade"] in {"A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"}
        spof_issues = [i for i in data["issues"] if i["title"] == "Single Point of Failure"]
        assert len(spof_issues) >= 1
        assert spof_issues[0]["severity"] == "critical"

    asyncio.run(run())


def test_troubleshooting_session_lifecycle():
    session = troubleshooting_engine.create_session("ping timeout")

    assert session.status == "open"
    assert session.session_id

    troubleshooting_engine.add_evidence(session, "ping", "Destination unreachable", confidence=0.9)
    assert len(session.evidence) == 1

    hypotheses = troubleshooting_engine.generate_hypotheses(session)
    assert len(hypotheses) >= 1

    troubleshooting_engine.verify_hypothesis(session, hypotheses[0].id, status="confirmed")
    assert session.root_cause is not None

    troubleshooting_engine.conclude(session, "Restore physical link", confidence=0.9)
    assert session.status == "resolved"
    assert session.resolution == "Restore physical link"


def test_migration_plan_generates_phases():
    async def run():
        plan = await migration_planner.plan(
            source_config="",
            source_vendor="cisco",
            target_vendor="mikrotik",
        )
        data = plan.to_dict()
        assert data["source_vendor"] == "cisco"
        assert data["target_vendor"] == "mikrotik"
        assert data["overall_risk"] in {"low", "medium", "high", "critical"}
        phases = data["phases"]
        phase_names = [p["phase"] for p in phases]
        assert "discovery" in phase_names
        assert "planning" in phase_names
        assert "preparation" in phase_names
        assert "execution" in phase_names
        assert "validation" in phase_names
        assert data["estimated_downtime_minutes"] >= 0

    asyncio.run(run())


def test_network_advisor_multi_branch():
    async def run():
        result = await network_advisor.advise("Saya punya 500 cabang.")
        assert result["meta"]["total_proposals"] >= 1
        proposals = result["proposals"]
        titles = [p["title"] for p in proposals]
        assert any("Multi-Branch" in t for t in titles)

    asyncio.run(run())


def test_network_advisor_ha_datacenter():
    async def run():
        result = await network_advisor.advise("I want HA datacenter")
        assert result["meta"]["total_proposals"] >= 1
        proposals = result["proposals"]
        titles = [p["title"] for p in proposals]
        assert any("High Availability" in t for t in titles)

    asyncio.run(run())


def test_network_advisor_fallback():
    async def run():
        result = await network_advisor.advise("random unrelated query")
        assert result["meta"]["total_proposals"] == 1
        proposal = result["proposals"][0]
        assert proposal["title"] == "General Network Design Guidance"

    asyncio.run(run())


def test_advisor_zero_trust():
    async def run():
        result = await network_advisor.advise("security with zero trust")
        proposals = result["proposals"]
        titles = [p["title"] for p in proposals]
        assert any("Zero Trust" in t for t in titles)

    asyncio.run(run())


def test_design_review_vlan_leak():
    topology = NetworkTopology()
    switch = NetworkDevice(
        id="switch-1",
        name="core-switch",
        device_type=DeviceType.SWITCH,
        interfaces=[
            NetworkInterface(name="port1", interface_type=InterfaceType.ETHERNET, vlan_id=10),
            NetworkInterface(name="port2", interface_type=InterfaceType.ETHERNET, vlan_id=10),
            NetworkInterface(name="port3", interface_type=InterfaceType.ETHERNET, vlan_id=10),
            NetworkInterface(name="port4", interface_type=InterfaceType.ETHERNET, vlan_id=10),
        ],
    )
    topology.add_device(switch)

    async def run():
        report = await design_review_engine.review(topology)
        data = report.to_dict()
        vlan_issues = [i for i in data["issues"] if "VLAN Spanning" in i["title"]]
        assert len(vlan_issues) >= 1

    asyncio.run(run())


if __name__ == "__main__":
    test_design_review_detects_spof()
    test_troubleshooting_session_lifecycle()
    test_migration_plan_generates_phases()
    test_network_advisor_multi_branch()
    test_network_advisor_ha_datacenter()
    test_network_advisor_fallback()
    test_advisor_zero_trust()
    test_design_review_vlan_leak()
    print("All Network Engineer 2.0 tests passed.")