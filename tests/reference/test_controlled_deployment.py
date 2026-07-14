import asyncio
from pathlib import Path

from apps.network_engineer.controlled_deployment import controlled_deployment
from apps.network_engineer.diff_engine import semantic_diff_engine
from apps.network_engineer.backup_manager import backup_manager
from apps.network_engineer.risk_scorer import risk_scoring_engine
from apps.network_engineer.verification_engine import verification_engine
from apps.network_engineer.audit_trail import audit_trail_manager
from apps.network_engineer.controlled_deployment import RollbackStatus

GOLDEN_DIR = Path(__file__).resolve().parents[2] / "golden" / "mikrotik"


def load_config(scenario: str) -> str:
    return (GOLDEN_DIR / scenario / "config.rsc").read_text(encoding="utf-8")


async def test_diff_engine():
    current = load_config("home")
    proposed = current + "\n/ip firewall filter\nadd action=accept chain=input protocol=tcp port=22 comment=\"Allow SSH\"\n"
    diff = semantic_diff_engine.diff(current, proposed)
    assert diff.summary["added"] >= 1, "Expected at least 1 added rule"
    assert "Firewall" in [e.category for e in diff.entries], "Expected firewall category in diff"
    print(f"[PASS] Diff Engine: {diff.summary['added']} added, {diff.summary['removed']} removed, {diff.summary['modified']} modified")
    return True


async def test_backup_manager():
    config = load_config("home")
    record = backup_manager.create_backup("test-device", config)
    assert record.config_hash, "Backup should have hash"
    assert record.size_bytes > 0, "Backup should have size"
    restored = backup_manager.restore_backup(record.backup_id)
    assert restored == config, "Restored config should match original"
    assert backup_manager.verify_integrity(record.backup_id), "Integrity check should pass"
    print(f"[PASS] Backup Manager: {record.backup_id} created, restored, integrity OK")
    return True


async def test_risk_scorer():
    diff_summary = {"added": 3, "removed": 1, "modified": 2}
    findings = [{"severity": "critical", "category": "security", "description": "Weak password"}]
    risk = risk_scoring_engine.score(diff_summary, findings)
    assert 0 <= risk.overall_risk <= 1, "Risk should be between 0 and 1"
    assert risk.recommendation, "Should have recommendation"
    print(f"[PASS] Risk Scorer: overall={risk.overall_risk:.2f}, config={risk.config_risk:.2f}, security={risk.security_risk:.2f}")
    return True


async def test_verification_engine():
    config = load_config("home")
    result = await verification_engine.verify("test-device", config)
    assert result.passed, "Verification should pass for valid config"
    assert result.summary["total"] >= 5, "Should have at least 5 checks"
    print(f"[PASS] Verification Engine: {result.summary['passed']} passed, {result.summary['failed']} failed")
    return True


async def test_controlled_deployment_approved():
    current = load_config("campus")
    proposed = current + "\n/ip firewall filter\nadd action=accept chain=input protocol=tcp port=22\n"
    report = await controlled_deployment.run_pipeline(
        device_id="test-router-1",
        current_config=current,
        proposed_config=proposed,
        approver="admin",
        approved=True,
        deployment_id="test-dep-approved",
    )
    assert report["status"] == "verified", f"Expected verified, got {report['status']}"
    assert report["backup_id"], "Should have backup"
    assert report["approval"]["approved"], "Should be approved"
    assert report["verification"]["status"] == "passed", "Verification should pass"
    print(f"[PASS] Controlled Deployment (approved): {report['status']}, backup={report['backup_id']}")
    return True


async def test_controlled_deployment_rejected():
    current = load_config("campus")
    proposed = current + "\n/ip firewall filter\nadd action=accept chain=input protocol=tcp port=22\n"
    report = await controlled_deployment.run_pipeline(
        device_id="test-router-2",
        current_config=current,
        proposed_config=proposed,
        approver="admin",
        approved=False,
        deployment_id="test-dep-rejected",
    )
    assert report["status"] == "failed", f"Expected failed, got {report['status']}"
    assert not report["approval"]["approved"], "Should be rejected"
    print(f"[PASS] Controlled Deployment (rejected): {report['status']}")
    return True


async def test_explain_before_deploy():
    current = load_config("home")
    proposed = current + "\n/ip firewall filter\nadd action=accept chain=input protocol=tcp port=22\n"
    plan = await controlled_deployment.analyze("test-device", current, proposed, "test-explain")
    plan = await controlled_deployment.diff(plan)
    plan = await controlled_deployment.score_risk(plan)
    plan = await controlled_deployment.backup(plan)

    runbook = controlled_deployment.generate_runbook(plan)
    assert runbook.changes, "Should have changes"
    assert runbook.risk_level, "Should have risk level"
    assert runbook.rollback_status == RollbackStatus.READY, "Should have rollback ready after backup"

    timeline = controlled_deployment.generate_timeline(plan)
    timeline_markdown = timeline.to_markdown()
    assert "Analyze" in timeline_markdown, "Timeline should include Analyze step"

    print(f"[PASS] Deployment Runbook + Timeline: risk={runbook.risk_level}, rollback={runbook.rollback_status.value}")
    return True


async def main() -> int:
    print("Running Sprint 2 Controlled Deployment Tests")
    print("=" * 80)

    tests = [
        test_diff_engine,
        test_backup_manager,
        test_risk_scorer,
        test_verification_engine,
        test_controlled_deployment_approved,
        test_controlled_deployment_rejected,
        test_explain_before_deploy,
    ]

    passed = 0
    for test in tests:
        try:
            await test()
            passed += 1
        except Exception as e:
            print(f"[FAIL] {test.__name__}: {e}")

    print("=" * 80)
    print(f"Tests passed: {passed}/{len(tests)}")
    if passed == len(tests):
        print("SUCCESS: All Controlled Deployment tests passed")
        return 0
    print("FAILED: Some tests did not pass")
    return 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
