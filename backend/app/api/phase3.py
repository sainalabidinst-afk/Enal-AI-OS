from fastapi import APIRouter, HTTPException
from backend.app.core.organization import organization_tree, RoleType, OrgNode
from backend.app.core.agent_reputation import agent_reputation
from backend.app.core.experience import experience_learning
from backend.app.core.observability import observability
from backend.app.core.governance import policy_engine, Permission
from backend.app.core.state_recovery import state_recovery
from backend.app.core.evaluation import evaluation_framework
from backend.app.core.mcp_registry import mcp_registry
from backend.app.core.artifact_service import artifact_service
from backend.app.core.semantic_graph import semantic_graph, NodeType, RelationType
from backend.app.core.prompt_compiler import prompt_compiler
from backend.app.core.cognitive_budget import cognitive_budget
from backend.app.core.goal_engine import goal_engine
from backend.app.core.long_task import long_task_manager
from backend.app.core.cognitive.reasoning_engine import reasoning_engine
from backend.app.core.cognitive.debate_engine import debate_engine
from backend.app.core.cognitive.self_verification import self_verification
from backend.app.core.cognitive.simulation_engine import simulation_engine
from backend.app.core.cognitive.world_model import world_model
from backend.app.core.cognitive.strategic_planner import strategic_planner
from backend.app.core.cognitive.continuous_learning import continuous_learning
from backend.app.core.cognitive import cognitive_orchestrator
from backend.app.core.cognitive_kernel import cognitive_kernel
from backend.app.core.meta_cognition import meta_cognition
from backend.app.core.decision_engine import decision_engine
from backend.app.plugins import register_default_plugins

router = APIRouter()

register_default_plugins()


@router.post("/organization")
async def create_org_node(name: str, role: str, agent_type: str, parent_id: str | None = None, capabilities: list[str] | None = None):
    try:
        role_enum = RoleType(role)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid role: {role}")
    node_id = f"node-{__import__('uuid').uuid4().hex[:8]}"
    node = OrgNode(
        id=node_id,
        name=name,
        role=role_enum,
        agent_type=agent_type,
        parent_id=parent_id,
        capabilities=capabilities or [],
    )
    organization_tree.add_node(node)
    return {"id": node_id, "name": name, "role": role}


@router.get("/organization/{node_id}")
async def get_org_node(node_id: str):
    node = organization_tree.get(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return {"id": node.id, "name": node.name, "role": node.role.value, "agent_type": node.agent_type, "children": node.children}


@router.get("/organization/{node_id}/subtree")
async def get_org_subtree(node_id: str):
    return organization_tree.get_subtree(node_id)


@router.get("/reputation/leaderboard")
async def get_reputation_leaderboard(limit: int = 10):
    return agent_reputation.get_leaderboard(limit=limit)


@router.post("/reputation/record")
async def record_reputation(agent_id: str, success: bool, quality_score: float, latency_ms: float, cost: float):
    agent_reputation.record(agent_id, success, quality_score, latency_ms, cost)
    return {"recorded": True}


@router.get("/experience/search")
async def search_experience(query: str, category: str | None = None, limit: int = 5):
    lessons = experience_learning.search(query, category=category, limit=limit)
    return [{"id": lesson.id, "category": lesson.category, "situation": lesson.situation, "outcome": lesson.outcome, "quality_score": lesson.quality_score} for lesson in lessons]


@router.post("/experience/record")
async def record_experience(project_id: str, category: str, situation: str, action_taken: str, outcome: str, quality_score: float, tags: list[str] | None = None):
    lesson_id = experience_learning.record(project_id, category, situation, action_taken, outcome, quality_score, tags)
    return {"lesson_id": lesson_id}


@router.get("/observability/traces/{trace_id}")
async def get_trace(trace_id: str):
    return observability.get_trace(trace_id)


@router.get("/observability/metrics")
async def get_observability_metrics(agent: str | None = None):
    return observability.get_metrics(agent=agent)


@router.post("/governance/policies")
async def create_policy(name: str, agent: str, permissions: list[str], tools: list[str]):
    perm_enums = [Permission(p) for p in permissions if p in [e.value for e in Permission]]
    from backend.app.core.governance import Policy
    policy_obj = Policy(id=f"policy-{__import__('uuid').uuid4().hex[:8]}", name=name, agent=agent, permissions=perm_enums, tools=tools)
    policy_engine.add_policy(policy_obj)
    return {"policy_id": policy_obj.id}


@router.get("/recovery/checkpoints")
async def list_checkpoints():
    return await state_recovery.list_checkpoints()


@router.post("/evaluation/benchmarks")
async def create_benchmark(name: str, description: str, test_cases: list[dict]):
    benchmark_id = f"benchmark-{__import__('uuid').uuid4().hex[:8]}"
    from backend.app.core.evaluation import Benchmark
    benchmark = Benchmark(id=benchmark_id, name=name, description=description, test_cases=test_cases)
    evaluation_framework.register_benchmark(benchmark)
    return {"benchmark_id": benchmark_id}


@router.get("/mcp/tools")
async def list_mcp_tools(permissions: str | None = None):
    perms = permissions.split(",") if permissions else None
    tools = mcp_registry.list_tools(permissions=perms)
    return [{"name": t.name, "description": t.description, "sandbox": t.sandbox, "permissions": t.permissions} for t in tools]


@router.get("/mcp/plugins")
async def list_mcp_plugins():
    plugins = mcp_registry.list_plugins()
    return [{"id": p.id, "name": p.name, "version": p.version, "tools_count": len(p.tools)} for p in plugins]


@router.post("/artifacts")
async def create_artifact(project_id: str, name: str, artifact_type: str, content: str, parent_id: str | None = None):
    artifact = await artifact_service.create_artifact(workspace_id=project_id, name=name, artifact_type=artifact_type, content=content)
    return {"artifact_id": artifact.id, "name": name, "version": artifact.current_version}


@router.get("/artifacts/{artifact_id}")
async def get_artifact(artifact_id: str):
    artifact = await artifact_service.get_artifact(artifact_id)
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return {"id": artifact.id, "name": artifact.name, "type": artifact.type, "version": artifact.current_version}


@router.post("/graph/nodes")
async def create_graph_node(name: str, node_type: str, description: str, project_id: str | None = None):
    try:
        n_type = NodeType(node_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid node type: {node_type}")
    from backend.app.core.semantic_graph import GraphNode
    node = GraphNode(id=f"node-{__import__('uuid').uuid4().hex[:8]}", node_type=n_type, name=name, description=description, project_id=project_id)
    node_id = await semantic_graph.add_node(node)
    return {"node_id": node_id, "name": name}


@router.post("/graph/edges")
async def create_graph_edge(source_id: str, target_id: str, relation: str):
    try:
        rel = RelationType(relation)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid relation: {relation}")
    edge_id = await semantic_graph.add_edge(source_id, target_id, rel)
    return {"edge_id": edge_id}


@router.get("/graph/nodes/{node_id}/related")
async def get_related_nodes(node_id: str):
    related = await semantic_graph.get_related(node_id)
    return {"node_id": node_id, "related": related}


@router.post("/prompt/compile")
async def compile_prompt(user_input: str, agent_type: str, project_id: str | None = None):
    prompt = await prompt_compiler.compile(user_input, agent_type, project_id)
    return {"prompt": prompt}


@router.post("/budget/estimate")
async def estimate_budget(task_description: str):
    budget = cognitive_budget.estimate(task_description)
    return {
        "complexity": budget.complexity.value,
        "model": budget.model,
        "max_tokens": budget.max_tokens,
        "require_reflection": budget.require_reflection,
        "estimated_duration_seconds": budget.estimated_duration_seconds,
    }


@router.post("/goals")
async def create_goal(description: str, success_criteria: list[str], project_id: str | None = None):
    goal = await goal_engine.create_goal(description, success_criteria, project_id)
    return {"goal_id": goal.id, "description": description}


@router.post("/goals/{goal_id}/execute")
async def execute_goal(goal_id: str):
    result = await goal_engine.execute(goal_id)
    return result


@router.get("/goals/{goal_id}")
async def get_goal(goal_id: str):
    goal = goal_engine.get_goal(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"id": goal.id, "description": goal.description, "status": goal.status, "progress": goal.progress}


@router.post("/longtasks")
async def submit_long_task(name: str, workflow: list[dict]):
    task_id = await long_task_manager.submit(name, workflow)
    return {"task_id": task_id, "name": name}


@router.post("/longtasks/{task_id}/start")
async def start_long_task(task_id: str):
    result = await long_task_manager.start(task_id)
    return result


@router.get("/longtasks/{task_id}")
async def get_long_task_status(task_id: str):
    status = await long_task_manager.get_status(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Long task not found")
    return status


@router.post("/longtasks/{task_id}/pause")
async def pause_long_task(task_id: str):
    await long_task_manager.pause(task_id)
    return {"paused": True}


@router.post("/longtasks/{task_id}/resume")
async def resume_long_task(task_id: str):
    result = await long_task_manager.resume(task_id)
    return result or {"resumed": True}


@router.post("/cognitive/process")
async def cognitive_process(user_input: str, project_id: str | None = None):
    result = await cognitive_orchestrator.process(user_input, project_id)
    return result


@router.post("/cognitive/reason")
async def cognitive_reason(problem: str):
    hypotheses = await reasoning_engine.generate_hypotheses(problem)
    chain = await reasoning_engine.reason(problem, hypotheses)
    decision = await reasoning_engine.decide(chain)
    return {"hypotheses": [{"id": h.id, "description": h.description, "confidence": h.confidence} for h in hypotheses], "decision": decision}


@router.post("/cognitive/debate")
async def cognitive_debate(topic: str, agents: list[str], rounds: int = 2):
    debate = await debate_engine.conduct_debate(topic, agents, rounds)
    return {"id": debate.id, "winner": debate.winner, "synthesis": debate.synthesis, "confidence": debate.confidence}


@router.post("/cognitive/verify")
async def cognitive_verify(artifact_id: str, code: str, language: str = "python"):
    pipeline = await self_verification.run_pipeline(artifact_id, code, language)
    return {"passed": pipeline.passed, "results": [{"step": r.step.value, "passed": r.passed, "error": r.error} for r in pipeline.results]}


@router.post("/cognitive/simulate")
async def cognitive_simulate(plan: list[dict], dry_run: bool = True):
    simulation = await simulation_engine.run(plan, dry_run=dry_run)
    return {"id": simulation.id, "status": simulation.status.value, "failure_points": simulation.failure_points, "improvements": simulation.improvements}


@router.get("/cognitive/world/query")
async def cognitive_world_query(query: str):
    entities = await world_model.query(query)
    return {"query": query, "entities": entities}


@router.post("/cognitive/strategy")
async def cognitive_strategy(goal_description: str, context: dict | None = None):
    roadmap = await strategic_planner.create_strategy(goal_description, context)
    return {"roadmap_id": roadmap.id, "phases": roadmap.phases, "milestones": roadmap.milestones}


@router.post("/cognitive/learn")
async def cognitive_learn(benchmark_id: str):
    from backend.app.core.evaluation import evaluation_framework
    benchmark = evaluation_framework._benchmarks.get(benchmark_id)
    if not benchmark:
        raise HTTPException(status_code=404, detail="Benchmark not found")
    result = await continuous_learning.run_benchmark_and_learn(benchmark_id, lambda case: None)
    return result


@router.get("/cognitive/services")
async def list_cognitive_services():
    return {"services": cognitive_kernel.list_services()}


@router.post("/cognitive/execute")
async def execute_cognitive_service(service_name: str, context: dict):
    result = await cognitive_kernel.execute_service(service_name, context)
    return result


@router.post("/cognitive/adaptive")
async def adaptive_process(user_input: str, project_id: str | None = None):
    result = await cognitive_orchestrator.process(user_input, project_id)
    return result


@router.post("/cognitive/meta/optimize")
async def meta_optimize(user_input: str, result: dict):
    optimization = await meta_cognition.evaluate_and_optimize(user_input, result)
    return optimization


@router.get("/cognitive/meta/metrics")
async def meta_metrics():
    return meta_cognition.get_metrics()


@router.post("/cognitive/meta/choose-pipeline")
async def meta_choose_pipeline(user_input: str):
    selection = await meta_cognition.choose_pipeline(user_input)
    return selection


@router.post("/cognitive/decide")
async def cognitive_decide(options: list[dict], context: dict | None = None):
    from backend.app.core.decision_engine import DecisionOption
    decision_options = [DecisionOption(id=o.get("id", f"opt-{i}"), description=o.get("description", ""), utility=o.get("utility", 0.5), risk=o.get("risk", 0.5), cost=o.get("cost", 0.5), confidence=o.get("confidence", 0.5)) for i, o in enumerate(options)]
    result = await decision_engine.decide(decision_options, context)
    return {"selected_id": result.selected_option_id, "description": result.selected_description, "confidence": result.confidence, "expected_value": result.expected_value, "reasoning": result.reasoning, "all_options": result.all_options}
