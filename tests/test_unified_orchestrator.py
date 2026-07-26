"""
Tests for Unified Orchestrator
=================================
Tests for orchestrator unification and dynamic team formation.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock


class TestUnifiedOrchestratorExtractSkills:
    """Tests for skill extraction."""

    def test_extract_skills_network(self):
        from backend.app.core.unified_orchestrator import UnifiedOrchestrator
        orch = UnifiedOrchestrator()
        skills = orch._extract_skills("audit network security", {})
        assert "network" in skills

    def test_extract_skills_code(self):
        from backend.app.core.unified_orchestrator import UnifiedOrchestrator
        orch = UnifiedOrchestrator()
        skills = orch._extract_skills("build coding functionality", {})
        assert "coding" in skills or "python" in skills or "testing" in skills

    def test_extract_skills_research(self):
        from backend.app.core.unified_orchestrator import UnifiedOrchestrator
        orch = UnifiedOrchestrator()
        skills = orch._extract_skills("research the market trends", {})
        assert "research" in skills


class TestUnifiedOrchestratorTeamFormation:
    """Tests for team formation."""

    @pytest.mark.asyncio
    async def test_form_team(self):
        from backend.app.core.unified_orchestrator import UnifiedOrchestrator
        orch = UnifiedOrchestrator()
        team = await orch._form_team("network audit", {})
        assert team.team_id is not None
        assert "network" in team.task


class TestUnifiedOrchestratorExecution:
    """Tests for orchestrator execution."""

    def test_list_teams(self):
        from backend.app.core.unified_orchestrator import UnifiedOrchestrator
        orch = UnifiedOrchestrator()
        teams = orch.list_teams()
        assert isinstance(teams, list)

    def test_orchestration_modes(self):
        from backend.app.core.unified_orchestrator import OrchestrationMode, UnifiedOrchestrator
        orch = UnifiedOrchestrator()
        assert OrchestrationMode.DIRECT.value == "direct"
        assert OrchestrationMode.MULTI_AGENT.value == "multi_agent"
        assert OrchestrationMode.WORKFLOW.value == "workflow"
        assert OrchestrationMode.COGNITIVE.value == "cognitive"