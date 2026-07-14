"""
Controlled Deployment
======================

Orchestrates the full controlled deployment pipeline:
Analyze → Generate → Diff → Simulation → Risk Score → Human Approval → Backup → Deploy → Verification → Rollback → Audit Report

Key principle: Human approval is required in the middle of the pipeline.
"""

import logging
from typing import Any
from dataclasses import dataclass, field
from enum import Enum

from apps.network_engineer import get_app
from apps.network_engineer.diff_engine import semantic_diff_engine
from apps.network_engineer.backup_manager import backup_manager
from apps.network_engineer.risk_scorer import risk_scoring_engine
from apps.network_engineer.verification_engine import verification_engine
from apps.network_engineer.audit_trail import audit_trail_manager, AuditEventType

logger = logging.getLogger(__name__)


class RollbackStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    UNAVAILABLE = "unavailable"
    COMPLETED = "completed"


ROLLBACK_STATUS_DISPLAY = {
    RollbackStatus.PENDING: "[!] Pending (backup will be created after approval)",
    RollbackStatus.READY: "[+] Ready",
    RollbackStatus.UNAVAILABLE: "[-] Unavailable",
    RollbackStatus.COMPLETED: "[~] Rollback Completed",
}


class DeploymentStatus(str, Enum):
    PENDING = "pending"
    ANALYZED = "analyzed"
    DIFFED = "diffed"
    RISK_SCORED = "risk_scored"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    BACKED_UP = "backed_up"
    DEPLOYED = "deployed"
    VERIFIED = "verified"
    ROLLED_BACK = "rolled_back"
    FAILED = "failed"


@dataclass
class DeploymentPlan:
    """Runbook-style deployment plan shown to the user."""
    deployment_id: str
    device_id: str
    current_config: str
    proposed_config: str
    analysis: dict[str, Any] = field(default_factory=dict)
    diff_markdown: str = ""
    diff_summary: dict[str, int] = field(default_factory=dict)
    risk_score: dict[str, Any] = field(default_factory=dict)
    backup_id: str | None = None
    approval: dict[str, Any] = field(default_factory=dict)
    verification: dict[str, Any] = field(default_factory=dict)
    status: DeploymentStatus = DeploymentStatus.PENDING
    error: str | None = None
    timeline_step: str = "analyze"


@dataclass
class DeploymentRunbook:
    """Runbook-style deployment preview."""
    changes: str
    risk_level: str
    overall_risk: float
    pre_deployment: str
    deployment: str
    post_deployment: str
    recovery: str
    rollback_status: RollbackStatus = RollbackStatus.PENDING

    def to_markdown(self) -> str:
        lines = ["# Deployment Plan\n"]
        lines.append("## Changes")
        lines.append(self.changes)
        lines.append("")
        lines.append(f"## Risk: {self.risk_level} ({self.overall_risk:.0%})\n")
        lines.append("## Pre-Deployment")
        lines.append(self.pre_deployment)
        lines.append("")
        lines.append("## Deployment")
        lines.append(self.deployment)
        lines.append("")
        lines.append("## Post-Deployment")
        lines.append(self.post_deployment)
        lines.append("")
        lines.append("## Recovery")
        lines.append(self.recovery)
        lines.append("")
        lines.append(f"## Rollback Status: {ROLLBACK_STATUS_DISPLAY[self.rollback_status]}")
        return "\n".join(lines)


@dataclass
class DeploymentTimeline:
    """Visual timeline of deployment steps."""
    steps: dict[str, str] = field(default_factory=lambda: {
        "analyze": "[ ] Analyze",
        "diff": "[ ] Generate Diff",
        "risk": "[ ] Risk Assessment",
        "approval": "[ ] Waiting for Approval",
        "backup": "[ ] Backup",
        "deploy": "[ ] Deploy",
        "verify": "[ ] Verify",
        "complete": "[ ] Complete",
    })

    def mark_completed(self, step: str):
        if step in self.steps:
            self.steps[step] = f"[x] {self.steps[step][3:]}"

    def mark_in_progress(self, step: str):
        if step in self.steps:
            self.steps[step] = f"[*] {self.steps[step][3:]}"

    def to_markdown(self) -> str:
        return "\n".join(self.steps.values())


class ControlledDeployment:
    """Orchestrates controlled deployment pipeline."""

    async def analyze(self, device_id: str, current_config: str, proposed_config: str, deployment_id: str | None = None) -> DeploymentPlan:
        """Step 1-2: Analyze current and proposed configs."""
        import time
        deployment_id = deployment_id or f"dep-{int(time.time() * 1000)}"

        app = get_app()
        analysis = await app.analyze_config(proposed_config)

        plan = DeploymentPlan(
            deployment_id=deployment_id,
            device_id=device_id,
            current_config=current_config,
            proposed_config=proposed_config,
            analysis=analysis,
            status=DeploymentStatus.ANALYZED,
        )

        trail = audit_trail_manager.create_trail(deployment_id)
        trail.add_event(AuditEventType.DEPLOYMENT_START, "system", {"device_id": device_id})

        return plan

    async def diff(self, plan: DeploymentPlan) -> DeploymentPlan:
        """Step 3: Compute semantic diff."""
        diff = semantic_diff_engine.diff(plan.current_config, plan.proposed_config)
        plan.diff_markdown = diff.to_markdown()
        plan.diff_summary = diff.summary
        plan.status = DeploymentStatus.DIFFED

        trail = audit_trail_manager.get_trail(plan.deployment_id)
        if trail:
            trail.add_event(AuditEventType.DIFF, "system", {"summary": diff.summary})

        return plan

    async def score_risk(self, plan: DeploymentPlan, is_new_device: bool = False) -> DeploymentPlan:
        """Step 4: Compute risk score."""
        risk = risk_scoring_engine.score(plan.diff_summary, plan.analysis.get("issues", []), is_new_device)
        plan.risk_score = risk.to_dict()
        plan.status = DeploymentStatus.RISK_SCORED

        trail = audit_trail_manager.get_trail(plan.deployment_id)
        if trail:
            trail.add_event(AuditEventType.RISK_SCORE, "system", risk.to_dict())

        return plan

    def generate_runbook(self, plan: DeploymentPlan) -> DeploymentRunbook:
        """Generate runbook-style deployment preview."""
        added = plan.diff_summary.get("added", 0)
        removed = plan.diff_summary.get("removed", 0)
        modified = plan.diff_summary.get("modified", 0)

        changes = "[x] Changes:\n"
        if added:
            changes += f"    • {added} rules added\n"
        if removed:
            changes += f"    • {removed} rules removed\n"
        if modified:
            changes += f"    • {modified} rules modified\n"
        if not added and not removed and not modified:
            changes += "    • No changes\n"

        overall_risk = plan.risk_score.get("overall_risk", 0.0)
        risk_level = "Low" if overall_risk < 0.2 else "Medium" if overall_risk < 0.5 else "High" if overall_risk < 0.8 else "Critical"

        pre_deployment = (
            "[x] Human Approval Required\n"
            "[x] Configuration Validation\n"
            "[x] Backup will be created automatically after approval\n"
        )

        deployment = "[x] Apply Configuration\n"

        post_deployment = (
            "[x] Connectivity Check\n"
            "[x] DNS Check\n"
            "[x] DHCP Check\n"
            "[x] Firewall Validation\n"
        )

        recovery = "[x] Automatic Rollback if verification fails\n"

        rollback_status = RollbackStatus.PENDING
        if plan.backup_id:
            rollback_status = RollbackStatus.READY
        if plan.status == DeploymentStatus.ROLLED_BACK:
            rollback_status = RollbackStatus.COMPLETED

        return DeploymentRunbook(
            changes=changes,
            risk_level=risk_level,
            overall_risk=overall_risk,
            pre_deployment=pre_deployment,
            deployment=deployment,
            post_deployment=post_deployment,
            recovery=recovery,
            rollback_status=rollback_status,
        )

    def generate_timeline(self, plan: DeploymentPlan) -> DeploymentTimeline:
        """Generate deployment timeline."""
        timeline = DeploymentTimeline()

        # Mark completed steps
        if plan.status in {
            DeploymentStatus.ANALYZED,
            DeploymentStatus.DIFFED,
            DeploymentStatus.RISK_SCORED,
            DeploymentStatus.AWAITING_APPROVAL,
            DeploymentStatus.APPROVED,
            DeploymentStatus.BACKED_UP,
            DeploymentStatus.DEPLOYED,
            DeploymentStatus.VERIFIED,
            DeploymentStatus.ROLLED_BACK,
            DeploymentStatus.FAILED,
        }:
            timeline.mark_completed("analyze")
            timeline.mark_completed("diff")
            timeline.mark_completed("risk")

        if plan.status in {
            DeploymentStatus.AWAITING_APPROVAL,
            DeploymentStatus.APPROVED,
            DeploymentStatus.BACKED_UP,
            DeploymentStatus.DEPLOYED,
            DeploymentStatus.VERIFIED,
            DeploymentStatus.ROLLED_BACK,
            DeploymentStatus.FAILED,
        }:
            timeline.mark_completed("approval")

        if plan.approval.get("approved"):
            timeline.mark_in_progress("backup") if not plan.backup_id else timeline.mark_completed("backup")

        if plan.backup_id and plan.status == DeploymentStatus.DEPLOYED:
            timeline.mark_completed("backup")
            timeline.mark_in_progress("deploy")
        elif plan.backup_id:
            timeline.mark_completed("backup")

        if plan.status == DeploymentStatus.VERIFIED:
            timeline.mark_completed("deploy")
            timeline.mark_completed("verify")
            timeline.mark_completed("complete")
        elif plan.status == DeploymentStatus.ROLLED_BACK:
            timeline.mark_completed("deploy")
            timeline.mark_completed("verify")
            timeline.mark_completed("complete")

        return timeline

    async def request_approval(self, plan: DeploymentPlan, approver: str, approved: bool, comment: str = "") -> DeploymentPlan:
        """Step 5: Human approval (required in v1.0-dev)."""
        plan.approval = {
            "approver": approver,
            "approved": approved,
            "comment": comment,
            "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
        }
        plan.status = DeploymentStatus.APPROVED if approved else DeploymentStatus.FAILED

        trail = audit_trail_manager.get_trail(plan.deployment_id)
        if trail:
            trail.add_event(AuditEventType.HUMAN_APPROVAL, approver, {"approved": approved, "comment": comment})

        return plan

    async def backup(self, plan: DeploymentPlan) -> DeploymentPlan:
        """Step 6: Create backup before deploy."""
        record = backup_manager.create_backup(plan.device_id, plan.current_config)
        plan.backup_id = record.backup_id
        plan.status = DeploymentStatus.BACKED_UP

        trail = audit_trail_manager.get_trail(plan.deployment_id)
        if trail:
            trail.add_event(AuditEventType.BACKUP, "system", {"backup_id": record.backup_id}, artifact_id=record.backup_id)

        return plan

    async def deploy(self, plan: DeploymentPlan) -> DeploymentPlan:
        """Step 7: Deploy (simulated)."""
        if not plan.approval.get("approved", False):
            plan.status = DeploymentStatus.FAILED
            plan.error = "Deployment not approved"
            return plan

        if not plan.backup_id:
            plan.status = DeploymentStatus.FAILED
            plan.error = "No backup before deploy"
            return plan

        # Simulate deployment
        plan.status = DeploymentStatus.DEPLOYED

        trail = audit_trail_manager.get_trail(plan.deployment_id)
        if trail:
            trail.add_event(AuditEventType.DEPLOY, "system", {"device_id": plan.device_id})

        return plan

    async def verify(self, plan: DeploymentPlan) -> DeploymentPlan:
        """Step 8: Verify post-deploy."""
        result = await verification_engine.verify(plan.device_id, plan.proposed_config)
        plan.verification = result.to_dict()
        plan.status = DeploymentStatus.VERIFIED if result.passed else DeploymentStatus.ROLLED_BACK

        trail = audit_trail_manager.get_trail(plan.deployment_id)
        if trail:
            trail.add_event(AuditEventType.VERIFICATION, "system", result.to_dict())

        # If verification failed, rollback
        if not result.passed:
            await self.rollback(plan)

        return plan

    async def rollback(self, plan: DeploymentPlan) -> DeploymentPlan:
        """Step 9: Rollback if needed."""
        if plan.backup_id:
            restored = backup_manager.restore_backup(plan.backup_id)
            plan.status = DeploymentStatus.ROLLED_BACK
            plan.error = "Rolled back after verification failure"

            trail = audit_trail_manager.get_trail(plan.deployment_id)
            if trail:
                trail.add_event(AuditEventType.ROLLBACK, "system", {"restored_from": plan.backup_id}, artifact_id=plan.backup_id)

        return plan

    async def final_report(self, plan: DeploymentPlan) -> dict[str, Any]:
        """Step 10: Generate final audit report."""
        trail = audit_trail_manager.get_trail(plan.deployment_id)

        runbook = self.generate_runbook(plan)
        timeline = self.generate_timeline(plan)

        report = {
            "deployment_id": plan.deployment_id,
            "device_id": plan.device_id,
            "status": plan.status.value,
            "analysis": plan.analysis,
            "diff_summary": plan.diff_summary,
            "risk_score": plan.risk_score,
            "approval": plan.approval,
            "backup_id": plan.backup_id,
            "verification": plan.verification,
            "error": plan.error,
            "runbook": runbook.to_markdown(),
            "timeline": timeline.to_markdown(),
            "audit_report": trail.to_markdown() if trail else "",
        }

        if trail:
            trail.add_event(AuditEventType.FINAL_REPORT, "system", {"status": plan.status.value})

        return report

    async def run_pipeline(
        self,
        device_id: str,
        current_config: str,
        proposed_config: str,
        approver: str,
        approved: bool,
        deployment_id: str | None = None,
        is_new_device: bool = False,
    ) -> dict[str, Any]:
        """Run the full controlled deployment pipeline."""
        plan = await self.analyze(device_id, current_config, proposed_config, deployment_id)
        plan = await self.diff(plan)
        plan = await self.score_risk(plan, is_new_device)

        if not approved:
            plan = await self.request_approval(plan, approver, approved)
            return await self.final_report(plan)

        plan = await self.request_approval(plan, approver, approved)
        if not approved:
            return await self.final_report(plan)

        plan = await self.backup(plan)
        plan = await self.deploy(plan)
        plan = await self.verify(plan)

        return await self.final_report(plan)


controlled_deployment = ControlledDeployment()
