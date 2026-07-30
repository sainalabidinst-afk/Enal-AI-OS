"""
Full Stack Engineer Tests
==========================

Tests for F1–F6 capabilities.
"""

import asyncio

from apps.full_stack_engineer import get_app
from apps.full_stack_engineer.architecture_review import (
    architecture_review_engine,
)
from apps.full_stack_engineer.code_review import code_review_engine
from apps.full_stack_engineer.performance_engineer import performance_engineer
from apps.full_stack_engineer.refactoring_planner import refactoring_planner
from apps.full_stack_engineer.release_engineer import release_engineer
from apps.full_stack_engineer.test_engineer import test_engineer


def test_architecture_review_returns_score():
    async def run():
        result = await architecture_review_engine.review(".")
        assert "architecture_score" in result
        assert 0 <= result["architecture_score"] <= 100
        assert "layering_grade" in result
        assert result["layering_grade"] in {"A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"}

    asyncio.run(run())


def test_code_review_detects_eval():
    code = """
import os
def unsafe():
    return eval(input("Enter code: "))
"""
    async def run():
        result = await code_review_engine.review(code, filename="test.py")
        findings = result.get("findings", [])
        assert len(findings) >= 1
        eval_findings = [f for f in findings if "eval" in f.get("title", "").lower()]
        assert len(eval_findings) >= 1
        assert eval_findings[0]["severity"] == "critical"

    asyncio.run(run())


def test_code_review_detects_mutable_default():
    code = """
def append(item, items=[]):
    items.append(item)
    return items
"""
    async def run():
        result = await code_review_engine.review(code, filename="test.py")
        findings = result.get("findings", [])
        assert len(findings) >= 1

    asyncio.run(run())


def test_refactoring_planner_returns_plans():
    code = """
def foo():
    pass

def bar():
    pass

def baz():
    pass

def qux():
    pass

def quux():
    pass
"""
    async def run():
        result = await refactoring_planner.plan(code, filename="test.py")
        assert "plans" in result
        assert result["total_plans"] >= 1
        plan = result["plans"][0]
        assert "problem" in plan
        assert "cause" in plan
        assert "proposal" in plan
        assert "migration_steps" in plan

    asyncio.run(run())


def test_test_engineer_reports_coverage():
    async def run():
        result = await test_engineer.engineer(".", "")
        assert "coverage_adequate" in result
        assert "plans" in result
        assert len(result["plans"]) >= 1

    asyncio.run(run())


def test_performance_engineer_detects_n_plus_one():
    code = """
def get_users():
    users = db.query("SELECT * FROM users")
    result = []
    for user in users:
        orders = db.query(f"SELECT * FROM orders WHERE user_id = {user.id}")
        result.append({"user": user, "orders": orders})
    return result
"""
    async def run():
        result = await performance_engineer.analyze(code, filename="test.py")
        issues = result.get("issues", [])
        assert len(issues) >= 1
        n1 = [i for i in issues if "N+1" in i.get("title", "")]
        assert len(n1) >= 1

    asyncio.run(run())


def test_performance_engineer_detects_blocking_io():
    code = """
import asyncio
import time

async def slow():
    time.sleep(1)
    return "done"
"""
    async def run():
        result = await performance_engineer.analyze(code, filename="test.py")
        issues = result.get("issues", [])
        assert len(issues) >= 1
        blocking = [i for i in issues if "Blocking" in i.get("category", "")]
        assert len(blocking) >= 1

    asyncio.run(run())


def test_release_engineer_validates_missing_changelog():
    changes = [{"file": "main.py", "type": "modified"}]
    context = {"version": "1.2.3", "rollback_plan": "restore backup", "deployment_checklist": ["build", "test"], "post_deployment_verification": ["health_check"]}
    async def run():
        result = await release_engineer.review(changes, context)
        assert "ready" in result
        checks = result.get("checks", [])
        changelog_checks = [c for c in checks if c["name"] == "Changelog"]
        assert len(changelog_checks) == 1
        assert changelog_checks[0]["status"] == "missing"

    asyncio.run(run())


def test_release_engineer_validates_present_changelog():
    changes = [{"file": "main.py", "type": "modified"}]
    context = {"version": "1.2.3", "changelog": "Added feature X and fixed bug Y. Improved performance and updated dependencies.", "rollback_plan": "restore backup", "deployment_checklist": ["build", "test"], "post_deployment_verification": ["health_check"]}
    async def run():
        result = await release_engineer.review(changes, context)
        checks = result.get("checks", [])
        changelog_checks = [c for c in checks if c["name"] == "Changelog"]
        assert changelog_checks[0]["status"] == "present"

    asyncio.run(run())


def test_full_stack_app_registered():
    app = get_app()
    assert app.name == "full-stack-engineer"
    assert app.version == "1.0.0"


if __name__ == "__main__":
    test_architecture_review_returns_score()
    test_code_review_detects_eval()
    test_code_review_detects_mutable_default()
    test_refactoring_planner_returns_plans()
    test_test_engineer_reports_coverage()
    test_performance_engineer_detects_n_plus_one()
    test_performance_engineer_detects_blocking_io()
    test_release_engineer_validates_missing_changelog()
    test_release_engineer_validates_present_changelog()
    test_full_stack_app_registered()
    print("All Full Stack Engineer tests passed.")