"""
Organization Kernel Tests
=========================

Tests Organization Kernel, Economics, Optimizer, and Learning.
"""

import pytest
from apps.organization.registry import agent_registry
from apps.organization.kernel import organization_kernel
from apps.organization.economics import organizational_economics
from apps.organization.optimizer import workforce_optimizer
from apps.organization.learning import organizational_learning
from apps.society.agent import Agent, AgentRole, Department


class SimpleAgent(Agent):
    async def _execute(self, task: dict[str, Any]) -> dict[str, Any]:
        return {"agent_id": self.agent_id, "status": "completed"}


@pytest.fixture(autouse=True)
def clear_state():
    agent_registry._agents = {}
    agent_registry._skill_index = {}
    agent_registry._department_index = {}
    organization_kernel._resource_requests.clear()
    organization_kernel._conflicts.clear()
    organization_kernel._productivity.clear()
    organization_kernel._worker_lifecycle.clear()
    organizational_learning._lessons.clear()
    organizational_learning._best_practices.clear()
    organizational_learning._reusable_assets.clear()
    organizational_learning._mistakes.clear()
    organizational_learning._project_learnings.clear()
    workforce_optimizer._suggestions.clear()
    yield


def test_kernel_budget_allocation():
    organization_kernel.set_budget(10000.0)
    assert organization_kernel.allocate_budget(5000.0, "ceo-1", "Project Alpha")
    assert not organization_kernel.allocate_budget(6000.0, "ceo-1", "Project Beta")
    status = organization_kernel.get_budget_status()
    assert status["total"] == 10000.0
    assert status["allocated"] == 5000.0
    print(f"[PASS] Kernel Budget: allocated={status['allocated']}, available={status['available']}")


def test_kernel_resource_request():
    request = organization_kernel.request_resource("ceo-1", "worker", "Need Python developer", 1000.0)
    assert request.id is not None
    assert request.status == "pending"
    approved = organization_kernel.approve_resource(request.id, "cto-1")
    assert approved.status == "approved"
    print(f"[PASS] Kernel Resource: request={request.id}, status={approved.status}")


def test_kernel_conflict_resolution():
    conflict = organization_kernel.detect_conflict(level=2, parties=["worker-1", "worker-2"], description="Resource conflict")
    assert conflict.status == "open"
    resolved = organization_kernel.resolve_conflict(conflict.id, "Split resources equally", "manager-1")
    assert resolved.status == "resolved"
    assert resolved.resolution == "Split resources equally"
    print(f"[PASS] Kernel Conflict: detected and resolved level {conflict.level}")


def test_kernel_productivity_tracking():
    organization_kernel.track_productivity("worker-1", task_completed=True, completion_time_seconds=120.0, quality_score=0.9)
    metrics = organization_kernel.get_productivity("worker-1")
    assert metrics.tasks_completed == 1
    assert metrics.quality_score == 0.9
    print(f"[PASS] Kernel Productivity: tasks={metrics.tasks_completed}, quality={metrics.quality_score}")


def test_economics_team_formation():
    analysis = organizational_economics.analyze_team_formation(
        team_size=3, avg_cost_per_worker=0.001, estimated_duration_hours=8, expected_quality=0.85
    )
    assert analysis.roi != 0
    assert len(analysis.costs) > 0
    assert len(analysis.benefits) > 0
    print(f"[PASS] Economics Team ROI: {analysis.roi:.2f}%")


def test_economics_model_selection():
    analysis = organizational_economics.analyze_model_selection(
        model_cost_per_1k=0.0005, estimated_tokens=10000, quality_score=0.9, latency_ms=500
    )
    assert analysis.roi > 0
    print(f"[PASS] Economics Model ROI: {analysis.roi:.2f}%")


def test_economics_meeting():
    analysis = organizational_economics.analyze_meeting_cost(participants=5, duration_minutes=30)
    assert analysis.roi != 0
    print(f"[PASS] Economics Meeting ROI: {analysis.roi:.2f}%")


def test_optimizer_team_composition():
    team = [SimpleAgent(f"w{i}", f"Worker {i}", AgentRole.WORKER, Department.ENGINEERING) for i in range(8)]
    suggestions = workforce_optimizer.optimize_team_composition(team, {"complexity": "high"})
    assert len(suggestions) > 0
    assert any(s.category == "team_composition" for s in suggestions)
    print(f"[PASS] Optimizer Team: {len(suggestions)} suggestions")


def test_optimizer_model_allocation():
    suggestion = workforce_optimizer.optimize_model_allocation("worker-1", "reasoning", "gpt-4o", 0.0015, 0.7)
    assert suggestion is not None
    assert suggestion.category == "model_allocation"
    print(f"[PASS] Optimizer Model: {suggestion.description}")


def test_optimizer_budget():
    suggestions = workforce_optimizer.optimize_budget({"utilization": 95.0})
    assert len(suggestions) > 0
    assert suggestions[0].priority == "critical"
    print(f"[PASS] Optimizer Budget: {suggestions[0].description}")


def test_learning_lessons():
    lesson = organizational_learning.record_lesson("proj-1", "architecture", "Microservices worked well", "High", "Use microservices for future projects")
    assert lesson.id is not None
    lessons = organizational_learning.get_project_lessons("proj-1")
    assert len(lessons) == 1
    print(f"[PASS] Learning Lessons: {len(lessons)} lesson(s) recorded")


def test_learning_best_practices():
    practice = organizational_learning.record_best_practice(
        name="API Versioning",
        description="Always version APIs from day one",
        context="software engineering",
        evidence="Reduced breaking changes by 80%",
        applicability=["software", "api"],
    )
    practices = organizational_learning.get_best_practices(context="software")
    assert len(practices) == 1
    print(f"[PASS] Learning Best Practices: {len(practices)} practice(s) found")


def test_learning_mistakes():
    mistake = organizational_learning.record_mistake("proj-1", "high", "No backup configured", "Oversight", "Data loss risk", "Always configure backup")
    assert mistake.id is not None
    mistakes = organizational_learning.get_mistakes(severity="high")
    assert len(mistakes) == 1
    print(f"[PASS] Learning Mistakes: {len(mistakes)} mistake(s) recorded")


def test_learning_reusable_assets():
    asset = organizational_learning.record_reusable_asset(
        name="Docker Compose Template",
        asset_type="template",
        content={"version": "3.8", "services": {}},
        description="Standard Docker Compose template",
        tags=["docker", "devops"],
    )
    assets = organizational_learning.get_reusable_assets(asset_type="template")
    assert len(assets) == 1
    print(f"[PASS] Learning Assets: {len(assets)} asset(s) found")


def test_society_kernel_integration():
    organization_kernel.set_budget(50000.0)
    status = organization_kernel.get_budget_status()
    assert status["total"] == 50000.0

    request = organization_kernel.request_resource("ceo-1", "worker", "Need backend developer", 2000.0)
    assert request.status == "pending"

    conflict = organization_kernel.detect_conflict(1, ["worker-1", "worker-2"], "Task conflict")
    assert conflict.status == "open"

    resolved = organization_kernel.resolve_conflict(conflict.id, "Prioritize task A", "manager-1")
    assert resolved.status == "resolved"

    print(f"[PASS] Society Kernel Integration: budget, resources, conflicts, economics")
