import logging  # noqa: I001
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum, Enum  # noqa: F401
from typing import Any

logger = logging.getLogger(__name__)


class Permission(StrEnum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DEPLOY = "deploy"
    ADMIN = "admin"


class ApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class Policy:
    id: str
    name: str
    agent: str
    permissions: list[Permission]
    tools: list[str]
    tenant_id: str | None = None
    conditions: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ApprovalRequest:
    id: str
    agent: str
    action: str
    justification: str
    requester: str
    status: ApprovalStatus = ApprovalStatus.PENDING
    approver: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    resolved_at: datetime | None = None


class PolicyEngine:
    def __init__(self):
        self._policies: dict[str, Policy] = {}
        self._approvals: dict[str, ApprovalRequest] = {}

    def add_policy(self, policy: Policy):
        self._policies[policy.id] = policy
        logger.info(f"Policy added: {policy.id} for {policy.agent}")

    def can_execute(
        self, agent: str, tool: str, permission: Permission, tenant_id: str | None = None
    ) -> bool:  # noqa: E501
        policy = next((p for p in self._policies.values() if p.agent == agent), None)
        if not policy:
            return False
        # Tenant isolation
        if policy.tenant_id and tenant_id and policy.tenant_id != tenant_id:
            return False
        if permission not in policy.permissions:
            return False
        if tool and tool not in policy.tools:
            return False
        return True

    def get_policy(self, agent: str) -> Policy | None:
        return next((p for p in self._policies.values() if p.agent == agent), None)

    def create_approval(
        self, agent: str, action: str, justification: str, requester: str
    ) -> ApprovalRequest:  # noqa: E501
        approval = ApprovalRequest(
            id=f"approval-{datetime.now(UTC).timestamp()}",
            agent=agent,
            action=action,
            justification=justification,
            requester=requester,
        )
        self._approvals[approval.id] = approval
        logger.info(f"Approval created: {approval.id}")
        return approval

    def approve(self, approval_id: str, approver: str) -> bool:
        approval = self._approvals.get(approval_id)
        if not approval or approval.status != ApprovalStatus.PENDING:
            return False
        approval.status = ApprovalStatus.APPROVED
        approval.approver = approver
        approval.resolved_at = datetime.now(UTC)
        logger.info(f"Approval {approval_id} approved by {approver}")
        return True

    def reject(self, approval_id: str, approver: str, reason: str = "") -> bool:
        approval = self._approvals.get(approval_id)
        if not approval or approval.status != ApprovalStatus.PENDING:
            return False
        approval.status = ApprovalStatus.REJECTED
        approval.approver = approver
        approval.resolved_at = datetime.now(UTC)
        logger.info(f"Approval {approval_id} rejected by {approver}: {reason}")
        return True

    def list_approvals(self, status: ApprovalStatus | None = None) -> list[ApprovalRequest]:
        approvals = list(self._approvals.values())
        if status:
            return [a for a in approvals if a.status == status]
        return approvals


policy_engine = PolicyEngine()


# Pilar 4 Governance (RFC-0055)


class PackStatus(StrEnum):
    DRAFT = "draft"
    TESTING = "testing"
    APPROVED = "approved"
    REJECTED = "rejected"
    REGISTERED = "registered"
    DEPRECATED = "deprecated"


@dataclass
class PackRecord:
    pack_id: str
    name: str
    domain: str
    status: PackStatus
    benchmark_score: float = 0.0
    coverage: float = 0.0
    tests_passed: int = 0
    tests_total: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class GovernanceSandbox:
    sandbox_id: str
    pack_id: str
    isolated: bool = True
    environment: str = "sandbox"
    allowed_operations: list[str] = field(default_factory=lambda: ["read", "execute", "benchmark"])
    blocked_operations: list[str] = field(
        default_factory=lambda: ["write", "network", "delete", "register"]
    )


@dataclass
class QualityGate:
    gate_id: str
    pack_id: str
    min_benchmark_score: float = 0.8
    min_coverage: float = 0.8
    min_test_pass_rate: float = 0.95
    max_governance_latency_ms: float = 500.0


@dataclass
class AuditEntry:
    entry_id: str
    actor: str
    action: str
    pack_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class GovernanceEngine:
    """Governance engine for pack lifecycle and quality gates."""

    def __init__(self) -> None:
        self._packs: dict[str, PackRecord] = {}
        self._sandboxes: dict[str, GovernanceSandbox] = {}
        self._gates: dict[str, QualityGate] = {}
        self._audit: list[AuditEntry] = []

    def register_pack(self, pack: PackRecord) -> PackRecord:
        self._packs[pack.pack_id] = pack
        self._audit.append(
            AuditEntry(
                entry_id=f"aud-{pack.pack_id}-{len(self._audit) + 1}",
                actor="system",
                action="pack_registered",
                pack_id=pack.pack_id,
                metadata={"status": pack.status.value},
            )
        )
        logger.info("Pack registered: %s (%s)", pack.pack_id, pack.status.value)
        return pack

    def create_sandbox(self, pack_id: str) -> GovernanceSandbox:
        sandbox = GovernanceSandbox(
            sandbox_id=f"sandbox-{pack_id}",
            pack_id=pack_id,
        )
        self._sandboxes[sandbox.sandbox_id] = sandbox
        self._audit.append(
            AuditEntry(
                entry_id=f"aud-sandbox-{pack_id}",
                actor="system",
                action="sandbox_created",
                pack_id=pack_id,
                metadata={"sandbox_id": sandbox.sandbox_id},
            )
        )
        logger.info("Sandbox created for pack %s", pack_id)
        return sandbox

    def update_pack_status(self, pack_id: str, status: PackStatus) -> PackRecord | None:
        pack = self._packs.get(pack_id)
        if pack is None:
            return None
        pack.status = status
        pack.updated_at = datetime.now(UTC)
        self._audit.append(
            AuditEntry(
                entry_id=f"aud-status-{pack_id}-{len(self._audit) + 1}",
                actor="system",
                action="pack_status_updated",
                pack_id=pack_id,
                metadata={"status": status.value},
            )
        )
        return pack

    def evaluate_gate(self, gate: QualityGate) -> dict[str, Any]:
        pack = self._packs.get(gate.pack_id)
        if pack is None:
            raise ValueError(f"Pack not found: {gate.pack_id}")
        passed = (
            pack.benchmark_score >= gate.min_benchmark_score
            and pack.coverage >= gate.min_coverage
            and (
                pack.tests_total == 0
                or pack.tests_passed / pack.tests_total >= gate.min_test_pass_rate
            )
        )
        result = {
            "pack_id": gate.pack_id,
            "passed": passed,
            "benchmark_score": pack.benchmark_score,
            "coverage": pack.coverage,
            "tests_passed": pack.tests_passed,
            "tests_total": pack.tests_total,
            "test_pass_rate": pack.tests_passed / pack.tests_total if pack.tests_total else 0.0,
            "min_benchmark_score": gate.min_benchmark_score,
            "min_coverage": gate.min_coverage,
            "min_test_pass_rate": gate.min_test_pass_rate,
        }
        if passed:
            self.update_pack_status(gate.pack_id, PackStatus.APPROVED)
        else:
            self.update_pack_status(gate.pack_id, PackStatus.REJECTED)
        self._audit.append(
            AuditEntry(
                entry_id=f"aud-gate-{gate.pack_id}-{len(self._audit) + 1}",
                actor="system",
                action="quality_gate_evaluated",
                pack_id=gate.pack_id,
                metadata=result,
            )
        )
        return result

    def get_pack(self, pack_id: str) -> PackRecord | None:
        return self._packs.get(pack_id)

    def list_packs(self, status: PackStatus | None = None) -> list[PackRecord]:
        packs = list(self._packs.values())
        if status is not None:
            packs = [p for p in packs if p.status == status]
        return packs

    def get_audit_trail(self, pack_id: str | None = None) -> list[dict[str, Any]]:
        entries = self._audit
        if pack_id is not None:
            entries = [e for e in entries if e.pack_id == pack_id]
        return [
            {
                "entry_id": e.entry_id,
                "actor": e.actor,
                "action": e.action,
                "pack_id": e.pack_id,
                "metadata": e.metadata,
                "created_at": e.created_at.isoformat(),
            }
            for e in entries
        ]


governance_engine = GovernanceEngine()
