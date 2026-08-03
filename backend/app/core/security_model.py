import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class SecurityLevel(str, Enum):
    SAFE = "safe"
    RESTRICTED = "restricted"
    PRIVILEGED = "privileged"


class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DEPLOY = "deploy"
    ADMIN = "admin"
    NETWORK = "network"
    SYSTEM = "system"


class AccessModel(str, Enum):
    RBAC = "rbac"
    ABAC = "abac"
    CAPABILITY = "capability"


@dataclass
class SecurityPolicy:
    plugin_id: str
    security_level: SecurityLevel
    tenant_id: str | None = None
    allowed_permissions: list[Permission] = field(default_factory=list)
    denied_permissions: list[Permission] = field(default_factory=list)
    allowed_capabilities: list[str] = field(default_factory=list)
    denied_capabilities: list[str] = field(default_factory=list)
    resource_limits: dict[str, Any] = field(default_factory=dict)
    requires_approval: bool = True
    approved: bool = False
    access_model: AccessModel = AccessModel.RBAC
    metadata: dict[str, Any] = field(default_factory=dict)


class PolicyEvaluator:
    def evaluate(self, policy: SecurityPolicy, permission: Permission, capability: str | None = None, context: dict[str, Any] | None = None) -> bool:
        if policy.access_model == AccessModel.RBAC:
            return self._evaluate_rbac(policy, permission)
        elif policy.access_model == AccessModel.ABAC:
            return self._evaluate_abac(policy, permission, context or {})
        elif policy.access_model == AccessModel.CAPABILITY:
            return self._evaluate_capability(policy, capability)
        return False

    def _evaluate_rbac(self, policy: SecurityPolicy, permission: Permission) -> bool:
        if permission in policy.denied_permissions:
            return False
        return permission in policy.allowed_permissions

    def _evaluate_abac(self, policy: SecurityPolicy, permission: Permission, context: dict[str, Any]) -> bool:
        if permission in policy.denied_permissions:
            return False
        if permission not in policy.allowed_permissions:
            return False
        for key, value in policy.metadata.items():
            if context.get(key) != value:
                return False
        return True

    def _evaluate_capability(self, policy: SecurityPolicy, capability: str | None) -> bool:
        if not capability:
            return False
        if capability in policy.denied_capabilities:
            return False
        return capability in policy.allowed_capabilities


class SecurityModel:
    def __init__(self):
        self._policies: dict[str, SecurityPolicy] = {}
        self._pending_approval: dict[str, SecurityPolicy] = {}
        self._evaluator = PolicyEvaluator()
        self._audit_log: list[dict[str, Any]] = []
        self._max_audit_log_size = 10000
        self._max_pending_approval_size = 100

    def _log_audit(self, action: str, plugin_id: str, permission: Permission | None = None, allowed: bool | None = None):
        self._audit_log.append({
            "timestamp": datetime.now(UTC).isoformat(),
            "action": action,
            "plugin_id": plugin_id,
            "permission": permission.value if permission else None,
            "allowed": allowed,
        })
        if len(self._audit_log) > self._max_audit_log_size:
            self._audit_log = self._audit_log[-self._max_audit_log_size:]

    def register_policy(self, policy: SecurityPolicy) -> bool:
        if policy.security_level == SecurityLevel.PRIVILEGED and not policy.approved:
            if len(self._pending_approval) >= self._max_pending_approval_size:
                oldest = next(iter(self._pending_approval))
                del self._pending_approval[oldest]
            self._pending_approval[policy.plugin_id] = policy
            logger.warning(f"Plugin {policy.plugin_id} requires approval (privileged)")
            return False
        self._policies[policy.plugin_id] = policy
        logger.info(f"Security policy registered for plugin {policy.plugin_id}")
        return True

    def approve_plugin(self, plugin_id: str) -> bool:
        if plugin_id in self._pending_approval:
            policy = self._pending_approval[plugin_id]
            policy.approved = True
            self._policies[plugin_id] = policy
            del self._pending_approval[plugin_id]
            logger.info(f"Plugin {plugin_id} approved")
            return True
        return False

    def check_permission(self, plugin_id: str, permission: Permission, capability: str | None = None, context: dict[str, Any] | None = None) -> bool:
        policy = self._policies.get(plugin_id)
        if not policy:
            self._log_audit("check_permission", plugin_id, permission, False)
            return False
        # Tenant isolation check
        tenant_id = context.get("tenant_id") if context else None
        if policy.tenant_id and tenant_id and policy.tenant_id != tenant_id:
            self._log_audit("check_permission", plugin_id, permission, False)
            return False
        result = self._evaluator.evaluate(policy, permission, capability, context)
        self._log_audit("check_permission", plugin_id, permission, result)
        return result

    def get_audit_log(self) -> list[dict[str, Any]]:
        return list(self._audit_log)

    def get_policy(self, plugin_id: str) -> SecurityPolicy | None:
        self._log_audit("get_policy", plugin_id)
        return self._policies.get(plugin_id)

    def get_pending_approvals(self) -> list[SecurityPolicy]:
        return list(self._pending_approval.values())


security_model = SecurityModel()

