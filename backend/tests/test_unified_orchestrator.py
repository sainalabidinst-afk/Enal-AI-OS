import pytest

from backend.app.core.unified_orchestrator import (
    OrchestrationMode,
    TeamFormation,
    UnifiedOrchestrator,
    get_unified_orchestrator,
)


class FakeOrgTree:
    def __init__(self, nodes):
        self._nodes = nodes


class FakeNode:
    def __init__(self, id, capabilities):
        self.id = id
        self.capabilities = capabilities


class TestOrchestrationMode:
    def test_modes(self):
        assert OrchestrationMode.DIRECT == "direct"
        assert OrchestrationMode.MULTI_AGENT == "multi_agent"
        assert OrchestrationMode.WORKFLOW == "workflow"
        assert OrchestrationMode.COGNITIVE == "cognitive"


class TestTeamFormation:
    def test_defaults(self):
        team = TeamFormation(
            team_id="team-1",
            task="task1",
            agents=[],
            strategy="skill-based",
            estimated_duration_ms=1000.0,
        )
        assert team.agents == []
        assert team.strategy == "skill-based"
        assert team.created_at is not None


class TestUnifiedOrchestrator:
    def test_get_unified_orchestrator_returns_same_instance(self):
        a = get_unified_orchestrator()
        b = get_unified_orchestrator()
        assert a is b

    def test_extract_skills_network(self):
        orch = UnifiedOrchestrator()
        skills = orch._extract_skills("configure firewall and router", {})
        assert "network" in skills
        assert "security" in skills

    def test_extract_skills_coding(self):
        orch = UnifiedOrchestrator()
        skills = orch._extract_skills("write python code for testing", {})
        assert "coding" in skills
        assert "python" in skills
        assert "testing" in skills

    def test_extract_skills_research(self):
        orch = UnifiedOrchestrator()
        skills = orch._extract_skills("research and analyze data", {})
        assert "research" in skills
        assert "analysis" in skills

    def test_extract_skills_database(self):
        orch = UnifiedOrchestrator()
        skills = orch._extract_skills("sql query for database", {})
        assert "data-analysis" in skills
        assert "sql" in skills

    def test_extract_skills_writing(self):
        orch = UnifiedOrchestrator()
        skills = orch._extract_skills("write documentation manual", {})
        assert "writing" in skills
        assert "documentation" in skills

    def test_find_agent_by_skill_found(self):
        orch = UnifiedOrchestrator()
        tree = FakeOrgTree({
            "1": FakeNode("agent-1", ["coding", "python"]),
            "2": FakeNode("agent-2", ["research", "analysis"]),
        })
        node = orch._find_agent_by_skill("python", tree)
        assert node is not None
        assert node.id == "agent-1"

    def test_find_agent_by_skill_not_found(self):
        orch = UnifiedOrchestrator()
        tree = FakeOrgTree({
            "1": FakeNode("agent-1", ["coding", "python"]),
        })
        node = orch._find_agent_by_skill("network", tree)
        assert node is None

    async def test_execute_direct_mode(self, monkeypatch):
        orch = UnifiedOrchestrator()

        async def fake_execute_cognitive(self, task, project_id, context):
            return {"mode": "direct", "task": task}

        monkeypatch.setattr(UnifiedOrchestrator, "_execute_direct", fake_execute_cognitive)
        result = await orch.execute("do something", mode="direct")
        assert result["mode"] == "direct"

    async def test_execute_cognitive_mode(self, monkeypatch):
        orch = UnifiedOrchestrator()

        async def fake_execute_cognitive(self, task, project_id, context):
            return {"mode": "cognitive", "task": task}

        monkeypatch.setattr(UnifiedOrchestrator, "_execute_cognitive", fake_execute_cognitive)
        result = await orch.execute("do something", mode="cognitive")
        assert result["mode"] == "cognitive"

    def test_list_teams_empty(self):
        orch = UnifiedOrchestrator()
        assert orch.list_teams() == []

    async def test_form_team_creates_team(self, monkeypatch):
        orch = UnifiedOrchestrator()
        monkeypatch.setattr(orch, "_extract_skills", lambda task, context: ["coding"])
        tree = FakeOrgTree({
            "1": FakeNode("agent-1", ["coding", "python"]),
        })
        monkeypatch.setattr("backend.app.core.organization.organization_tree", tree)
        team = await orch._form_team("write python code", {})
        assert team.team_id.startswith("team-")
        assert team.strategy == "skill-based"

    async def test_execute_workflow_mode(self, monkeypatch):
        orch = UnifiedOrchestrator()

        class FakeResult:
            status = type("Status", (), {"value": "completed"})()
            aggregated_result = {"ok": True}

        class FakeMultiAgent:
            async def execute_plan(self, plan):
                return FakeResult()

        class FakePlanner:
            def plan_from_goal(self, task, context):
                return type("Plan", (), {"plan_id": "plan-1", "steps": []})()

        monkeypatch.setattr(orch, "_get_multi_agent", lambda: FakeMultiAgent())
        monkeypatch.setattr(orch, "_get_planner", lambda: (FakePlanner(), None))
        result = await orch.execute("do something", mode="workflow")
        assert result["plan_id"] == "plan-1"
        assert result["status"] == "completed"

    async def test_execute_multi_agent_mode(self, monkeypatch):
        orch = UnifiedOrchestrator()

        class FakeResult:
            status = type("Status", (), {"value": "completed"})()
            aggregated_result = {"ok": True}

        class FakeMultiAgent:
            async def execute_plan(self, plan):
                return FakeResult()

        class FakePlanner:
            def plan_from_goal(self, task, context):
                return type("Plan", (), {"plan_id": "plan-1", "steps": []})()

        async def fake_form_team(task, context):
            return type("Team", (), {"team_id": "team-1"})()

        monkeypatch.setattr(orch, "_get_multi_agent", lambda: FakeMultiAgent())
        monkeypatch.setattr(orch, "_get_planner", lambda: (FakePlanner(), None))
        monkeypatch.setattr(orch, "_form_team", fake_form_team)
        result = await orch.execute("do something", mode="multi_agent")
        assert result["team_id"] == "team-1"
        assert result["plan_id"] == "plan-1"

    async def test_execute_cognitive_mode_full(self, monkeypatch):
        orch = UnifiedOrchestrator()

        class FakeBudget:
            complexity = "medium"

            def estimate(self, task):
                return self

        class FakeKernel:
            async def execute_pipeline(self, pipeline, context):
                return {"input": context["input"], "pipeline": pipeline}

        class FakeRuntime:
            def __init__(self):
                self.budget = FakeBudget()

        monkeypatch.setattr(orch, "_get_kernel", lambda: FakeKernel())
        monkeypatch.setattr(orch, "_get_runtime", lambda: (FakeRuntime(), {"medium": ["p1"]}, type("TC", (), {"MEDIUM": "medium"})()))
        result = await orch.execute("do something", mode="cognitive")
        assert result["input"] == "do something"
        assert "pipeline" in result

    def test_get_kernel_returns_cognitive_kernel(self, monkeypatch):
        orch = UnifiedOrchestrator()
        import backend.app.core.cognitive_kernel as ck_module
        monkeypatch.setattr(ck_module, "cognitive_kernel", "fake-kernel")
        kernel = orch._get_kernel()
        assert kernel == "fake-kernel"

    def test_get_runtime_returns_adaptive_runtime(self, monkeypatch):
        orch = UnifiedOrchestrator()
        import backend.app.core.adaptive_runtime as ar_module
        fake_runtime = "fake-runtime"
        fake_presets = {"medium": ["p1"]}
        fake_complexity = type("TC", (), {"MEDIUM": "medium"})()
        monkeypatch.setattr(ar_module, "adaptive_runtime", fake_runtime)
        monkeypatch.setattr(ar_module, "PIPELINE_PRESETS", fake_presets)
        monkeypatch.setattr(ar_module, "TaskComplexity", fake_complexity)
        runtime, presets, complexity = orch._get_runtime()
        assert runtime == "fake-runtime"
        assert presets == {"medium": ["p1"]}

    def test_get_planner_returns_ai_planner(self, monkeypatch):
        orch = UnifiedOrchestrator()
        import apps.organization.ai_planner as ap_module
        fake_planner = "fake-planner"
        fake_status = type("PS", (), {})()
        monkeypatch.setattr(ap_module, "ai_planner", fake_planner)
        monkeypatch.setattr(ap_module, "PlanStatus", fake_status)
        planner, PlanStatus = orch._get_planner()
        assert planner == "fake-planner"

    def test_get_multi_agent_returns_orchestrator(self, monkeypatch):
        orch = UnifiedOrchestrator()
        import apps.organization.multi_agent as ma_module
        fake_multi = "fake-multi"
        monkeypatch.setattr(ma_module, "multi_agent_orchestrator", fake_multi)
        multi_agent = orch._get_multi_agent()
        assert multi_agent == "fake-multi"

    async def test_list_teams_returns_teams(self, monkeypatch):
        orch = UnifiedOrchestrator()
        monkeypatch.setattr(orch, "_extract_skills", lambda task, context: ["coding"])
        tree = FakeOrgTree({
            "1": FakeNode("agent-1", ["coding", "python"]),
        })
        monkeypatch.setattr("backend.app.core.organization.organization_tree", tree)
        await orch._form_team("write python code", {})
        teams = orch.list_teams()
        assert len(teams) == 1
        assert teams[0]["team_id"].startswith("team-")
