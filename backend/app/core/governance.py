import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DEPLOY = "deploy"
    ADMIN = "admin"


class ApprovalStatus(str, Enum):
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
    created_at: datetime = field(default_factory=datetime.now(UTC))
    resolved_at: datetime | None = None


class PolicyEngine:
    def __init__(self):
        self._policies: dict[str, Policy] = {}
        self._approvals: dict[str, ApprovalRequest] = {}

    def add_policy(self, policy: Policy):
        self._policies[policy.id] = policy
        logger.info(f"Policy added: {policy.id} for {policy.agent}")

    def can_execute(self, agent: str, tool: str, permission: Permission, tenant_id: str | None = None) -> bool:
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

    def create_approval(self, agent: str, action: str, justification: str, requester: str) -> ApprovalRequest:
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

