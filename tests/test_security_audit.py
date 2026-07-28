"""
Tests for Enterprise Security & Governance
==========================================
Tests for audit logging and policy management.
"""



class TestSecurityModelAudit:
    """Tests for SecurityModel audit logging."""

    def test_audit_log_initialization(self):
        from backend.app.core.security_model import SecurityModel
        sm = SecurityModel()
        assert isinstance(sm._audit_log, list)

    def test_check_permission_logs_audit(self):
        from backend.app.core.security_model import SecurityModel, SecurityPolicy, SecurityLevel, Permission
        sm = SecurityModel()
        policy = SecurityPolicy(
            plugin_id="test-plugin",
            security_level=SecurityLevel.SAFE,
            allowed_permissions=[Permission.READ],
        )
        sm.register_policy(policy)
        result = sm.check_permission("test-plugin", Permission.READ)
        assert result is True
        assert len(sm.get_audit_log()) == 1

    def test_get_audit_log(self):
        from backend.app.core.security_model import SecurityModel
        sm = SecurityModel()
        log = sm.get_audit_log()
        assert isinstance(log, list)


class TestSecurityPolicy:
    """Tests for SecurityPolicy."""

    def test_policy_creation(self):
        from backend.app.core.security_model import SecurityPolicy, SecurityLevel, Permission
        policy = SecurityPolicy(
            plugin_id="my-plugin",
            security_level=SecurityLevel.RESTRICTED,
            allowed_permissions=[Permission.READ, Permission.WRITE],
        )
        assert policy.plugin_id == "my-plugin"
        assert len(policy.allowed_permissions) == 2


class TestPolicyEvaluator:
    """Tests for PolicyEvaluator."""

    def test_rbac_evaluation(self):
        from backend.app.core.security_model import PolicyEvaluator, SecurityPolicy, Permission
        evaluator = PolicyEvaluator()
        policy = SecurityPolicy(
            plugin_id="test",
            security_level="safe",
            allowed_permissions=[Permission.READ],
        )
        assert evaluator.evaluate(policy, Permission.READ) is True
        assert evaluator.evaluate(policy, Permission.WRITE) is False

    def test_abac_evaluation(self):
        from backend.app.core.security_model import PolicyEvaluator, SecurityPolicy, AccessModel, Permission
        evaluator = PolicyEvaluator()
        policy = SecurityPolicy(
            plugin_id="test",
            security_level="safe",
            allowed_permissions=[Permission.READ],
            access_model=AccessModel.ABAC,
            metadata={"user": "admin"},
        )
        assert evaluator.evaluate(policy, Permission.READ, context={"user": "admin"}) is True