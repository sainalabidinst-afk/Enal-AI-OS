"""
Migration Planner
=================

Generates cross-vendor migration plans with risk assessment, rollback, and validation.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class MigrationPhase(str, Enum):
    DISCOVERY = "discovery"
    PLANNING = "planning"
    PREPARATION = "preparation"
    EXECUTION = "execution"
    VALIDATION = "validation"
    ROLLBACK = "rollback"
    COMPLETED = "completed"


class MigrationRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class MigrationTask:
    phase: MigrationPhase
    title: str
    description: str
    estimated_duration_minutes: int = 30
    rollback_steps: list[str] = field(default_factory=list)
    validation_steps: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    risk: MigrationRisk = MigrationRisk.LOW


@dataclass
class MigrationPlan:
    source_vendor: str
    target_vendor: str
    device_count: int = 0
    estimated_downtime_minutes: int = 0
    overall_risk: MigrationRisk = MigrationRisk.MEDIUM
    tasks: list[MigrationTask] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_vendor": self.source_vendor,
            "target_vendor": self.target_vendor,
            "device_count": self.device_count,
            "estimated_downtime_minutes": self.estimated_downtime_minutes,
            "overall_risk": self.overall_risk.value,
            "phases": [
                {
                    "phase": task.phase.value,
                    "title": task.title,
                    "description": task.description,
                    "estimated_duration_minutes": task.estimated_duration_minutes,
                    "rollback_steps": task.rollback_steps,
                    "validation_steps": task.validation_steps,
                    "dependencies": task.dependencies,
                    "risk": task.risk.value,
                }
                for task in self.tasks
            ],
            "warnings": self.warnings,
            "recommendations": self.recommendations,
        }


VENDOR_ALIGNMENT = {
    ("cisco", "mikrotik"): {
        "firewall": ("access-list", "/ip firewall filter"),
        "nat": ("ip nat", "/ip firewall nat"),
        "vrrp": ("hsrp", "/interface vrrp"),
        "dhcp": ("ip dhcp", "/ip dhcp-server"),
    },
    ("cisco", "fortinet"): {
        "firewall": ("access-list", "config firewall policy"),
        "nat": ("ip nat", "config firewall nat"),
        "ha": ("hsrp", "config system ha"),
        "vpn": ("crypto map", "config vpn ipsec"),
    },
    ("mikrotik", "cisco"): {
        "firewall": ("/ip firewall filter", "access-list"),
        "nat": ("/ip firewall nat", "ip nat"),
        "vrrp": ("/interface vrrp", "standby"),
        "dhcp": ("/ip dhcp-server", "ip dhcp"),
    },
    ("mikrotik", "fortinet"): {
        "firewall": ("/ip firewall filter", "config firewall policy"),
        "nat": ("/ip firewall nat", "config firewall nat"),
        "ha": ("/interface vrrp", "config system ha"),
    },
    ("fortinet", "cisco"): {
        "firewall": ("config firewall policy", "access-list"),
        "nat": ("config firewall nat", "ip nat"),
        "ha": ("config system ha", "hsrp"),
    },
    ("fortinet", "mikrotik"): {
        "firewall": ("config firewall policy", "/ip firewall filter"),
        "nat": ("config firewall nat", "/ip firewall nat"),
        "ha": ("config system ha", "/interface vrrp"),
    },
}


class MigrationPlanner:
    """Generates cross-vendor migration plans."""

    async def plan(self, source_config: str, source_vendor: str, target_vendor: str, config_content: str = "") -> MigrationPlan:
        plan = MigrationPlan(source_vendor=source_vendor, target_vendor=target_vendor)
        alignment = VENDOR_ALIGNMENT.get((source_vendor, target_vendor), {})

        if source_vendor == target_vendor:
            plan.warnings.append("Source and target vendor are identical; migration plan is a no-op.")
            plan.recommendations.append("Consider refactoring or version upgrade instead of full migration.")
            plan.tasks.append(MigrationTask(
                phase=MigrationPhase.PLANNING,
                title="Validate Same-Vendor Migration",
                description="Verify whether a same-vendor migration is truly needed.",
                risk=MigrationRisk.LOW,
            ))
            return plan

        plan.device_count = 1
        plan.overall_risk = MigrationRisk.MEDIUM

        plan.tasks.extend([
            MigrationTask(
                phase=MigrationPhase.DISCOVERY,
                title="Discover Source Configuration",
                description="Parse source configuration and extract all features, interfaces, routing, and security rules.",
                estimated_duration_minutes=30,
                rollback_steps=["No rollback needed during discovery."],
                validation_steps=["Verify parsed config matches source file."],
                risk=MigrationRisk.LOW,
            ),
            MigrationTask(
                phase=MigrationPhase.PLANNING,
                title="Map Features to Target Vendor",
                description=f"Map {source_vendor} concepts to {target_vendor} equivalents. Alignment coverage: {len(alignment)} concepts.",
                estimated_duration_minutes=60,
                dependencies=["Discover Source Configuration"],
                rollback_steps=["No rollback needed during planning."],
                validation_steps=["Review mapping table with network team."],
                risk=MigrationRisk.LOW,
            ),
            MigrationTask(
                phase=MigrationPhase.PREPARATION,
                title="Prepare Target Device",
                description=f"Provision {target_vendor} device with baseline configuration: management, NTP, logging, and AAA.",
                estimated_duration_minutes=45,
                dependencies=["Map Features to Target Vendor"],
                rollback_steps=[
                    "Keep source device online until validation completes.",
                    "Document rollback commands.",
                ],
                validation_steps=["Verify management access to target device."],
                risk=MigrationRisk.LOW,
            ),
            MigrationTask(
                phase=MigrationPhase.EXECUTION,
                title="Migrate Firewall and Security",
                description=f"Translate firewall and security policies from {source_vendor} to {target_vendor}.",
                estimated_duration_minutes=90,
                dependencies=["Prepare Target Device"],
                rollback_steps=[
                    "Revert to source device configuration.",
                    "Restore original routing and firewall rules.",
                ],
                validation_steps=[
                    "Test firewall rules in lab before production.",
                    "Verify security policy parity.",
                ],
                risk=MigrationRisk.HIGH,
            ),
            MigrationTask(
                phase=MigrationPhase.EXECUTION,
                title="Migrate Routing and Services",
                description=f"Translate static routes, dynamic routing, DHCP, and DNS from {source_vendor} to {target_vendor}.",
                estimated_duration_minutes=120,
                dependencies=["Migrate Firewall and Security"],
                rollback_steps=[
                    "Restore source routing configuration.",
                    "Verify rollback route propagation.",
                ],
                validation_steps=[
                    "Validate end-to-end connectivity.",
                    "Run routing protocol adjacency checks.",
                ],
                risk=MigrationRisk.MEDIUM,
            ),
            MigrationTask(
                phase=MigrationPhase.VALIDATION,
                title="Validate Migration",
                description="Run full validation suite: connectivity, performance, security, and compliance.",
                estimated_duration_minutes=60,
                dependencies=["Migrate Routing and Services"],
                rollback_steps=[
                    "Execute rollback plan if critical issues found.",
                    "Notify stakeholders of rollback.",
                ],
                validation_steps=[
                    "Ping and traceroute all critical paths.",
                    "Run golden test suite.",
                    "Verify compliance posture.",
                ],
                risk=MigrationRisk.MEDIUM,
            ),
        ])

        plan.estimated_downtime_minutes = sum(t.estimated_duration_minutes for t in plan.tasks if t.phase == MigrationPhase.EXECUTION)
        plan.warnings.append("Always maintain rollback capability during execution phase.")
        plan.warnings.append("Test migration in lab environment before production cutover.")
        plan.recommendations.append("Use maintenance window for execution phase.")
        plan.recommendations.append("Document all changes for audit trail.")
        plan.recommendations.append("Verify backup of source configuration before starting.")

        return plan


migration_planner = MigrationPlanner()