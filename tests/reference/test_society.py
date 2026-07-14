"""
Society Runtime Tests
=====================

Tests AI Organization Platform:
- Agent registration
- Role assignment (CEO → Director → Manager → Lead → Worker)
- Dynamic team formation
- Project execution
- Organizational metrics
"""

import pytest
from apps.organization.registry import AgentRecord, AgentRole, Department, agent_registry
from apps.organization.runtime import organization_runtime
from apps.organization.team_builder import TaskRequirement, team_builder
from apps.organization.communication import mailbox, blackboard
from apps.organization.collective_memory import collective_memory
from apps.society.society import create_society, SocietyRuntime
from apps.society.agent import Agent, AgentContext
from apps.society.workers.network_worker import network_worker
from apps.society.workers.code_worker import code_worker
from apps.society.workers.research_worker import research_worker
from apps.society.workers.devops_worker import devops_worker
from apps.society.workers.trading_worker import trading_worker
from apps.society.workers.self_development_worker import self_development_worker


class SimpleAgent(Agent):
    async def _execute(self, task: dict[str, Any]) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "task": task.get("description", ""),
            "status": "completed",
            "result": f"Executed by {self.name}",
        }


@pytest.fixture(autouse=True)
def clear_registry():
    agent_registry._agents = {}
    agent_registry._skill_index = {}
    agent_registry._department_index = {}
    yield


def test_society_creation():
    society = create_society("Test AI Corp", "Test organization")
    assert society.config.name == "Test AI Corp"
    state = society.get_organization_state()
    assert state["total_agents"] == 0
    assert state["active_projects"] == 0


def test_agent_registration_and_role_assignment():
    society = create_society("Test Corp")
    
    ceo = SimpleAgent("ceo-1", "Alice", AgentRole.CEO, Department.ENGINEERING)
    cto = SimpleAgent("cto-1", "Bob", AgentRole.DIRECTOR, Department.ENGINEERING)
    backend_lead = SimpleAgent("lead-1", "Charlie", AgentRole.LEAD, Department.ENGINEERING)
    worker = SimpleAgent("worker-1", "Dave", AgentRole.WORKER, Department.ENGINEERING)
    
    society.register_agent(ceo)
    society.register_agent(cto)
    society.register_agent(backend_lead)
    society.register_agent(worker)
    
    assert society.get_organization_state()["total_agents"] == 4
    
    society.assign_role("ceo-1", AgentRole.CEO, Department.ENGINEERING)
    society.assign_role("cto-1", AgentRole.DIRECTOR, Department.ENGINEERING, manager_id="ceo-1")
    society.assign_role("lead-1", AgentRole.LEAD, Department.ENGINEERING, manager_id="cto-1")
    society.assign_role("worker-1", AgentRole.WORKER, Department.ENGINEERING, manager_id="lead-1")
    
    cto_record = agent_registry.get("cto-1")
    assert cto_record.manager_id == "ceo-1"
    assert cto_record.role == AgentRole.DIRECTOR
    
    worker_record = agent_registry.get("worker-1")
    assert worker_record.manager_id == "lead-1"
    assert worker_record.role == AgentRole.WORKER


def test_team_formation():
    society = create_society("Test Corp")
    
    for i in range(5):
        agent = SimpleAgent(
            f"agent-{i}",
            f"Agent {i}",
            AgentRole.WORKER,
            Department.ENGINEERING,
            skills=["python", "api", "database"] if i < 3 else ["frontend", "ui"],
        )
        society.register_agent(agent)
    
    team = society.form_team_for_task({
        "description": "Build a web application",
        "required_skills": ["python", "api"],
        "team_size": 3,
        "min_quality": 0.5,
    })
    
    assert len(team.members) <= 3
    assert team.team_id is not None


@pytest.mark.asyncio
async def test_project_execution():
    society = create_society("Test Corp")
    
    ceo = SimpleAgent("ceo-1", "Alice", AgentRole.CEO, Department.ENGINEERING)
    worker = SimpleAgent("worker-1", "Bob", AgentRole.WORKER, Department.ENGINEERING, skills=["python"])
    
    society.register_agent(ceo)
    society.register_agent(worker)
    society.assign_role("ceo-1", AgentRole.CEO, Department.ENGINEERING)
    society.assign_role("worker-1", AgentRole.WORKER, Department.ENGINEERING)
    
    team = society.form_team_for_task({
        "description": "Build API",
        "required_skills": ["python"],
        "team_size": 1,
    })
    
    result = await society.run_project("proj-1", team.team_id, {
        "type": "build",
        "target": "api",
    })
    
    assert result is not None
    assert "results" in result
    assert len(result["results"]) > 0


def test_communication():
    society = create_society("Test Corp")
    
    sender = SimpleAgent("sender-1", "Alice", AgentRole.WORKER, Department.ENGINEERING)
    recipient = SimpleAgent("recipient-1", "Bob", AgentRole.WORKER, Department.ENGINEERING)
    
    society.register_agent(sender)
    society.register_agent(recipient)
    
    society.send_message("sender-1", "recipient-1", "Task Update", {"status": "in_progress"})
    from apps.organization.communication import mailbox
    messages = mailbox.receive("recipient-1")
    assert len(messages) == 1
    assert messages[0].subject == "Task Update"


def test_blackboard():
    society = create_society("Test Corp")
    blackboard.write("architecture", "microservices")
    assert blackboard.read("architecture") == "microservices"
    assert "architecture" in blackboard.read_all()


def test_collective_memory():
    society = create_society("Test Corp")
    entry_id = collective_memory.store("project_decision", {"decision": "use FastAPI"})
    entry = collective_memory.recall(entry_id)
    assert entry is not None
    assert entry.content["decision"] == "use FastAPI"


def test_organization_state():
    agent_registry._agents.clear()
    agent_registry._skill_index.clear()
    agent_registry._department_index.clear()
    
    society = create_society("Test Corp")
    
    ceo = SimpleAgent("ceo-1", "Alice", AgentRole.CEO, Department.ENGINEERING)
    cto = SimpleAgent("cto-1", "Bob", AgentRole.DIRECTOR, Department.ENGINEERING)
    qa = SimpleAgent("qa-1", "Charlie", AgentRole.WORKER, Department.QUALITY)
    
    society.register_agent(ceo)
    society.register_agent(cto)
    society.register_agent(qa)
    
    society.assign_role("ceo-1", AgentRole.CEO, Department.ENGINEERING)
    society.assign_role("cto-1", AgentRole.DIRECTOR, Department.ENGINEERING, manager_id="ceo-1")
    society.assign_role("qa-1", AgentRole.WORKER, Department.QUALITY, manager_id="cto-1")
    
    state = society.get_organization_state()
    assert state["total_agents"] == 3
    assert state["agents_by_role"]["ceo"] == 1
    assert state["agents_by_role"]["director"] == 1
    assert state["agents_by_department"]["engineering"] == 2
    assert state["agents_by_department"]["quality"] == 1


@pytest.mark.asyncio
async def test_process_user_request_returns_task_and_execution_plan():
    society = create_society("Enal AI OS")
    net = SimpleAgent("net-1", "NetWorker", AgentRole.WORKER, Department.NETWORK, skills=["config-analysis"])
    society.register_agent(net)
    result = await society.process_user_request("Audit network configuration")
    assert result["status"] == "completed"
    assert result["task_plan"] is not None
    assert len(result["task_plan"]["subtasks"]) > 0
    assert result["execution_plan"] is not None
    assert len(result["execution_plan"]["stages"]) > 0


@pytest.mark.asyncio
async def test_network_worker_end_to_end():
    society = create_society("Enal AI OS")
    net_worker = SimpleAgent(
        "net-1", "MikroTikWorker", AgentRole.WORKER, Department.NETWORK,
        skills=["config-analysis", "security-audit"],
    )
    society.register_agent(net_worker)
    society.register_worker("network", network_worker)
    result = await society.process_user_request("Analyze MikroTik configuration")
    assert result["status"] == "completed"
    assert result["intent"]["domain"] == "network"
    assert result["team_size"] >= 1
    assert "result" in result
    assert result["project_id"] is not None


@pytest.mark.asyncio
async def test_code_worker_end_to_end():
    society = create_society("Enal AI OS")
    code_worker_agent = SimpleAgent(
        "code-1", "CodeReviewer", AgentRole.WORKER, Department.ENGINEERING,
        skills=["python", "code-review", "security"],
    )
    society.register_agent(code_worker_agent)
    society.register_worker("code", code_worker)
    result = await society.process_user_request("Review this Python code for security issues")
    assert result["status"] == "completed"
    assert result["intent"]["domain"] == "code"
    assert result["team_size"] >= 1
    assert "result" in result
    assert result["project_id"] is not None


@pytest.mark.asyncio
async def test_research_worker_end_to_end():
    society = create_society("Enal AI OS")
    research_agent = SimpleAgent(
        "res-1", "Researcher", AgentRole.WORKER, Department.QUALITY,
        skills=["research", "literature-review", "data-analysis"],
    )
    society.register_agent(research_agent)
    society.register_worker("research", research_worker)
    result = await society.process_user_request("Find latest research on BGP security")
    assert result["status"] == "completed"
    assert result["intent"]["domain"] == "research"
    assert result["team_size"] >= 1
    assert "result" in result
    assert result["project_id"] is not None


@pytest.mark.asyncio
async def test_devops_worker_end_to_end():
    society = create_society("Enal AI OS")
    devops_agent = SimpleAgent(
        "devops-1", "DevOpsEngineer", AgentRole.WORKER, Department.DEVOPS,
        skills=["kubernetes", "docker", "ci-cd", "terraform"],
    )
    society.register_agent(devops_agent)
    society.register_worker("devops", devops_worker)
    result = await society.process_user_request("Set up CI/CD pipeline for a containerized service")
    assert result["status"] == "completed"
    assert result["intent"]["domain"] == "devops"
    assert result["team_size"] >= 1
    assert "result" in result
    assert result["project_id"] is not None


@pytest.mark.asyncio
async def test_trading_worker_end_to_end():
    society = create_society("Enal AI OS")
    trading_agent = SimpleAgent(
        "trading-1", "TradingAnalyst", AgentRole.WORKER, Department.QUALITY,
        skills=["market-analysis", "risk-assessment", "portfolio-optimization"],
    )
    society.register_agent(trading_agent)
    society.register_worker("trading", trading_worker)
    result = await society.process_user_request("Analyze BTCUSDT and generate trading strategy")
    assert result["status"] == "completed"
    assert result["intent"]["domain"] == "trading"
    assert result["team_size"] >= 1
    assert "result" in result
    assert result["project_id"] is not None


@pytest.mark.asyncio
async def test_self_development_worker_end_to_end():
    society = create_society("Enal AI OS")
    dev_agent = SimpleAgent(
        "dev-1", "SelfDeveloper", AgentRole.WORKER, Department.ENGINEERING,
        skills=["architecture", "code-review", "testing", "documentation"],
    )
    society.register_agent(dev_agent)
    society.register_worker("self-development", self_development_worker)
    result = await society.process_user_request("Audit Enal AI OS for bottlenecks and propose improvements")
    assert result["status"] == "completed"
    assert result["intent"]["domain"] == "self-development"
    assert result["team_size"] >= 1
    assert "result" in result
    assert result["project_id"] is not None


@pytest.mark.asyncio
async def test_conversation_manager_flow():
    try:
        import redis.asyncio as aioredis
        aioredis.from_url("redis://localhost:6379")
    except Exception:
        pytest.skip("Redis not available for conversation manager test")
    from apps.society.conversation_manager import conversation_manager
    conversation_id = "conv-test-1"
    await conversation_manager.clear_history(conversation_id)
    response1 = await conversation_manager.send_message(conversation_id, "Analyze MikroTik configuration")
    assert response1["conversation_id"] == conversation_id
    assert response1["domain"] == "network"
    history = await conversation_manager.get_history(conversation_id)
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"

    response2 = await conversation_manager.send_message(conversation_id, "What about Cisco?")
    assert response2["conversation_id"] == conversation_id
    history2 = await conversation_manager.get_history(conversation_id)
    assert len(history2) == 4


@pytest.mark.asyncio
async def test_end_to_end_user_command_flow():
    society = create_society("Test AI Corp")
    
    net_worker = SimpleAgent(
        "net-1", "NetworkWorker", AgentRole.WORKER, Department.NETWORK,
        skills=["network-design", "config-analysis"],
    )
    net_worker2 = SimpleAgent(
        "net-2", "ConfigWorker", AgentRole.WORKER, Department.NETWORK,
        skills=["config-analysis", "security-audit"],
    )
    society.register_agent(net_worker)
    society.register_agent(net_worker2)
    
    result = await society.process_user_request("Analyze the network configuration")
    
    assert result["status"] == "completed"
    assert result["intent"]["domain"] in ["network", "general"]
    assert result["team_size"] >= 1
    assert result["team_size"] <= 2
    assert "result" in result
    assert result["project_id"] is not None
