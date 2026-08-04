"""
Disaster Recovery Planner
=========================

Designs disaster recovery plans with RPO/RTO targets, backup schedules,
multi-site strategies, and compliance checks.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.infrastructure_engineer.schemas import (
    InfrastructureEngineerRequest,
    DRPlan,
    DisasterRecoveryStrategy,
    RecoveryPointObjective,
    RecoveryTimeObjective,
    BackupSchedule,
    BusinessContext,
)

logger = logging.getLogger(__name__)

STRATEGY_RPO_MAP: dict[str, tuple[int, int]] = {
    "backup_restore": (1440, 1440),
    "pilot_light": (60, 240),
    "warm_standby": (15, 60),
    "multi_site_active_active": (0, 0),
}


class DisasterRecoveryPlanner:
    """Designs and evaluates disaster recovery plans."""

    def plan(self, request: InfrastructureEngineerRequest) -> DRPlan:
        inputs = request.inputs
        strategy_value = inputs.get("strategy", "warm_standby")
        try:
            strategy = DisasterRecoveryStrategy(strategy_value)
        except ValueError:
            strategy = DisasterRecoveryStrategy.warm_standby

        rpo_min, rto_min = STRATEGY_RPO_MAP.get(strategy_value, (60, 240))
        rpo_min = inputs.get("rpo_minutes", rpo_min)
        rto_min = inputs.get("rto_minutes", rto_min)

        frequency = inputs.get("backup_frequency", "daily")
        retention = inputs.get("backup_retention_days", 30)

        return DRPlan(
            strategy=strategy,
            primary_region=inputs.get("primary_region", "us-east-1"),
            secondary_region=inputs.get("secondary_region", "us-west-2"),
            rpo=RecoveryPointObjective(rpo_minutes=rpo_min, rto_minutes=rto_min),
            backup_schedule=BackupSchedule(
                frequency=frequency,
                retention_days=retention,
                backup_type=inputs.get("backup_type", "full"),
                encryption=True,
                compression=True,
            ),
            failover_runbook=inputs.get("failover_runbook", "docs/runbooks/infrastructure-dr.md"),
            testing_schedule=inputs.get("testing_schedule", "quarterly"),
            communication_plan=inputs.get("communication_plan", []),
        )

    def get_recommendations(self, plan: DRPlan) -> list[str]:
        recs: list[str] = []
        if plan.strategy == DisasterRecoveryStrategy.backup_restore:
            recs.append("Pertimbangkan upgrade ke pilot_light atau warm_standby untuk RPO/RTO yang lebih baik")
        if plan.rpo.rpo_minutes > 60:
            recs.append("RPO target lebih tinggi dari 1 jam — evaluasi toleransi data loss")
        if plan.rpo.rto_minutes > 240:
            recs.append("RTO target lebih tinggi dari 4 jam — evaluasi toleransi downtime")
        if plan.testing_schedule == "annually":
            recs.append("Ubah schedule pengujian DR dari tahunan ke kuartalan")
        if not plan.failover_runbook:
            recs.append("Buat failover runbook terstruktur dengan langkah verifikasi")
        return recs

    def estimate_cost(self, plan: DRPlan) -> dict[str, float]:
        strategy_costs: dict[str, float] = {
            "backup_restore": 50.0,
            "pilot_light": 200.0,
            "warm_standby": 500.0,
            "multi_site_active_active": 2000.0,
        }
        monthly = strategy_costs.get(plan.strategy.value, 500.0)
        return {
            "dr_infrastructure_monthly": monthly,
            "backup_storage_monthly": 20.0,
            "data_transfer_monthly": 50.0,
            "total_monthly": monthly + 70.0,
        }

    def get_security_hardening(self, plan: DRPlan) -> list[str]:
        return [
            "Backup dienkripsi AES-256 — kunci terpisah dari data",
            "Data transfer antar region menggunakan VPN/PrivateLink",
            "Cross-region IAM least privilege diterapkan",
            "DR region memiliki kontrol akses yang terisolasi",
            "Backup tidak dapat dihapus oleh akun admin utama (WORM)",
        ]

    def check_compliance(self, plan: DRPlan) -> dict[str, bool]:
        return {
            "rpo_within_target": plan.rpo.rpo_minutes <= plan.rpo.rto_minutes,
            "rto_within_target": plan.rpo.rto_minutes <= 480,
            "backup_encrypted": plan.backup_schedule.encryption,
            "testing_scheduled": bool(plan.testing_schedule),
            "runbook_exists": bool(plan.failover_runbook),
            "communication_plan_defined": bool(plan.communication_plan),
            "secondary_region_configured": bool(plan.secondary_region),
        }

    def score_quality(self, plan: DRPlan) -> float:
        score = 0.6
        compliance = self.check_compliance(plan)
        score += sum(1 for v in compliance.values() if v) * 0.05
        if plan.strategy in (
            DisasterRecoveryStrategy.warm_standby,
            DisasterRecoveryStrategy.multi_site_active_active,
        ):
            score += 0.1
        return min(score, 1.0)
