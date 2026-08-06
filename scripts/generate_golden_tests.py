"""
Generate Golden Test scaffolding for all 19 Capability Packs.

This script creates 10 golden test JSON files per pack in golden_tests/<pack_id>/
"""

from __future__ import annotations

import json
import os

PACKS = [
    "network_engineer",
    "code_engineer",
    "research_assistant",
    "devops_assistant",
    "trading_analyst",
    "self_development",
    "decision_intelligence",
    "system_architect",
    "security_engineer",
    "data_engineer",
    "database_engineer",
    "qa_engineer",
    "business_analyst",
    "infrastructure_engineer",
    "ai_engineer",
    "documentation_engineer",
    "product_manager",
    "ui_ux_designer",
    "full_stack_engineer",
]

BASE_TEMPLATES = {
    "network_engineer": [
        {"category": "security_audit", "inputs": {"config_type": "mikrotik", "config_content": "sample_config_here"}},
        {"category": "topology_analysis", "inputs": {"configs": ["config1", "config2"]}},
        {"category": "design_review", "inputs": {"topology": "sample_topology"}},
        {"category": "troubleshooting", "inputs": {"symptoms": ["packet_loss", "high_latency"]}},
        {"category": "migration_planning", "inputs": {"source": "mikrotik", "target": "cisco"}},
        {"category": "compliance", "inputs": {"standard": "ISO27001"}},
        {"category": "firewall_audit", "inputs": {"rules": ["rule1", "rule2"]}},
        {"category": "vpn_design", "inputs": {"type": "site-to-site"}},
        {"category": "bgp_analysis", "inputs": {"config": "sample_bgp_config"}},
        {"category": "performance_review", "inputs": {"metrics": {"latency": "10ms", "packet_loss": "0.01%"}}},
    ],
    "code_engineer": [
        {"category": "security_review", "inputs": {"code": "sample_code_here", "language": "python"}},
        {"category": "architecture_review", "inputs": {"repo_path": "."}},
        {"category": "refactoring_plan", "inputs": {"code": "sample_code_here", "issue": "long_method"}},
        {"category": "test_generation", "inputs": {"code": "sample_code_here", "test_type": "unit"}},
        {"category": "dependency_analysis", "inputs": {"repo_path": "."}},
        {"category": "solid_check", "inputs": {"code": "sample_code_here", "principle": "SRP"}},
        {"category": "cqrs_analysis", "inputs": {"code": "sample_code_here"}},
        {"category": "injection_detection", "inputs": {"code": "sample_code_here", "language": "python"}},
        {"category": "secret_detection", "inputs": {"code": "sample_code_here"}},
        {"category": "performance_analysis", "inputs": {"code": "sample_code_here"}},
    ],
    "research_assistant": [
        {"category": "literature_review", "inputs": {"query": "sample_query", "sources": ["source1", "source2"]}},
        {"category": "evidence_ranking", "inputs": {"sources": ["source1", "source2"]}},
        {"category": "contradiction_detection", "inputs": {"claims": ["claim1", "claim2"]}},
        {"category": "citation_assessment", "inputs": {"citations": ["citation1", "citation2"]}},
        {"category": "confidence_estimation", "inputs": {"evidence": ["evidence1", "evidence2"]}},
        {"category": "synthesis", "inputs": {"sources": ["source1", "source2"]}},
        {"category": "report_generation", "inputs": {"findings": ["finding1", "finding2"]}},
        {"category": "source_quality", "inputs": {"sources": ["source1", "source2"]}},
        {"category": "bias_detection", "inputs": {"text": "sample_text"}},
        {"category": "knowledge_gap", "inputs": {"topic": "sample_topic"}},
    ],
    "devops_assistant": [
        {"category": "pipeline_generation", "inputs": {"service": "sample_service", "platform": "github_actions"}},
        {"category": "infrastructure_design", "inputs": {"service": "sample_service", "platform": "kubernetes"}},
        {"category": "deployment_planning", "inputs": {"service": "sample_service", "strategy": "rolling"}},
        {"category": "monitoring_config", "inputs": {"service": "sample_service", "stack": "prometheus"}},
        {"category": "project_scanning", "inputs": {"project_path": "."}},
        {"category": "security_hardening", "inputs": {"artifact": {"type": "dockerfile", "content": "sample"}}},
        {"category": "gitops_setup", "inputs": {"platform": "argocd"}},
        {"category": "chaos_engineering", "inputs": {"service": "sample_service"}},
        {"category": "cost_optimization", "inputs": {"infrastructure": {"type": "kubernetes", "nodes": 3}}},
        {"category": "disaster_recovery", "inputs": {"service": "sample_service", "rpo": 15, "rto": 30}},
    ],
    "trading_analyst": [
        {"category": "wyckoff_analysis", "inputs": {"symbol": "AAPL", "timeframe": "1D"}},
        {"category": "smc_analysis", "inputs": {"symbol": "AAPL", "timeframe": "4H"}},
        {"category": "elliott_wave", "inputs": {"symbol": "AAPL", "timeframe": "1D"}},
        {"category": "volume_profile", "inputs": {"symbol": "AAPL", "session": "daily"}},
        {"category": "psychology_analysis", "inputs": {"symbol": "AAPL"}},
        {"category": "macro_analysis", "inputs": {"event": "Fed rate decision"}},
        {"category": "derivatives_analysis", "inputs": {"symbol": "AAPL"}},
        {"category": "risk_assessment", "inputs": {"portfolio": {"positions": [{"symbol": "AAPL", "quantity": 100}]}}},
        {"category": "strategy_backtest", "inputs": {"strategy": "momentum", "historical_data": [{"date": "2025-01-01", "price": 100}]}},
        {"category": "multi_strategy_debate", "inputs": {"strategies": [{"name": "strategy1", "score": 0.8}]}},
    ],
    "self_development": [
        {"category": "project_scanning", "inputs": {"project_path": "."}},
        {"category": "smell_detection", "inputs": {"code": "sample_code"}},
        {"category": "architecture_analysis", "inputs": {"repo_path": "."}},
        {"category": "refactoring_proposal", "inputs": {"issue": "long_method", "code": "sample_code"}},
        {"category": "impact_prediction", "inputs": {"change": "refactor_auth", "repo_path": "."}},
        {"category": "risk_modeling", "inputs": {"change": "refactor_auth"}},
        {"category": "cross_project_learning", "inputs": {"projects": ["project1", "project2"]}},
        {"category": "improvement_suggestion", "inputs": {"scan_result": {"hotspots": ["module_a"]}}},
        {"category": "approval_workflow", "inputs": {"proposal": {"id": "prop1", "changes": ["file_a.py"]}}},
        {"category": "pattern_forecasting", "inputs": {"history": [{"pattern": "debt", "frequency": "monthly"}]}},
    ],
    "decision_intelligence": [
        {"category": "evidence_collection", "inputs": {"query": "sample_query", "sources": ["source1"]}},
        {"category": "alternative_generation", "inputs": {"problem": "sample_problem", "constraints": ["constraint1"]}},
        {"category": "risk_analysis", "inputs": {"alternatives": [{"name": "alt1", "probability": 0.3, "impact": 1000}]}},
        {"category": "tradeoff_analysis", "inputs": {"alternatives": [{"name": "alt1"}], "objectives": [{"name": "cost", "weight": 0.5}]}},
        {"category": "scoring", "inputs": {"alternatives": [{"name": "alt1"}], "criteria": {"cost": {"weight": 0.5}}}},
        {"category": "confidence_estimation", "inputs": {"evidence": [{"source": "source1", "quality": 0.9}]}},
        {"category": "explanation_generation", "inputs": {"decision": {"chosen": "alt1", "score": 0.9}}},
        {"category": "simulation", "inputs": {"scenario": "sample_scenario", "parameters": {"iterations": 1000}}},
        {"category": "debate", "inputs": {"strategies": [{"name": "strategy1", "arguments": []}]}},
        {"category": "decision_history", "inputs": {"decision": {"id": "dec1", "timestamp": "2025-01-01"}}},
    ],
    "system_architect": [
        {"category": "architecture_review", "inputs": {"repo_path": "."}},
        {"category": "dependency_analysis", "inputs": {"repo_path": "."}},
        {"category": "layer_violation", "inputs": {"repo_path": "."}},
        {"category": "ddd_analysis", "inputs": {"repo_path": "."}},
        {"category": "event_driven_review", "inputs": {"repo_path": "."}},
        {"category": "cqrs_evaluation", "inputs": {"repo_path": "."}},
        {"category": "microservices_decomposition", "inputs": {"repo_path": "."}},
        {"category": "boundary_enforcement", "inputs": {"repo_path": "."}},
        {"category": "adr_generation", "inputs": {"decision": "sample_decision", "context": "sample_context"}},
        {"category": "scalability_review", "inputs": {"architecture": {"style": "microservices", "services": 10}}},
    ],
    "security_engineer": [
        {"category": "owasp_analysis", "inputs": {"code": "sample_code", "language": "python"}},
        {"category": "secret_detection", "inputs": {"code": "sample_code", "language": "python"}},
        {"category": "dependency_audit", "inputs": {"manifest": "sample_manifest", "type": "pip"}},
        {"category": "threat_modeling", "inputs": {"architecture": {"components": ["web", "api"]}, "components": ["web", "api"], "data_flows": [{"from": "web", "to": "api"}]}},
        {"category": "vulnerability_scanning", "inputs": {"code": "sample_code", "language": "python"}},
        {"category": "hardening_review", "inputs": {"config": "sample_config", "type": "docker"}},
        {"category": "compliance_mapping", "inputs": {"findings": [{"id": "f1"}], "standards": ["owasp", "pci_dss"]}},
        {"category": "xss_detection", "inputs": {"code": "sample_code", "language": "javascript"}},
        {"category": "sqli_detection", "inputs": {"code": "sample_code", "language": "python"}},
        {"category": "access_control_review", "inputs": {"code": "sample_code", "auth_type": "RBAC"}},
    ],
    "data_engineer": [
        {"category": "etl_pipeline", "inputs": {"source": "csv", "target": "postgresql", "transformations": ["clean", "enrich"]}},
        {"category": "data_cleaning", "inputs": {"dataset": {"rows": 1000, "columns": 10}, "issues": ["missing_values", "duplicates"]}},
        {"category": "dataset_validation", "inputs": {"schema": {"columns": [{"name": "id", "type": "int"}]}, "data": [{"id": 1}]}},
        {"category": "schema_evolution", "inputs": {"current_schema": {"columns": ["id"]}, "new_schema": {"columns": ["id", "name"]}}},
        {"category": "feature_engineering", "inputs": {"dataset": {"rows": 1000}, "target": "label"}},
        {"category": "time_series_handling", "inputs": {"data": [{"timestamp": "2025-01-01", "value": 100}], "frequency": "1H"}},
        {"category": "data_quality", "inputs": {"dataset": {"rows": 1000}, "checks": ["completeness", "uniqueness"]}},
        {"category": "lineage_tracking", "inputs": {"pipeline": {"steps": ["extract", "transform", "load"]}}},
        {"category": "streaming_etl", "inputs": {"source": "kafka", "target": "elasticsearch"}},
        {"category": "data_classification", "inputs": {"dataset": {"columns": ["email", "phone"]}, "categories": ["PII", "sensitive"]}},
    ],
    "database_engineer": [
        {"category": "query_optimization", "inputs": {"query": "SELECT * FROM users WHERE id = 1", "db_type": "postgresql"}},
        {"category": "index_recommendation", "inputs": {"query": "SELECT * FROM users WHERE email = ?", "table": "users", "db_type": "postgresql"}},
        {"category": "migration_planning", "inputs": {"current_schema": {"tables": ["users"]}, "target_schema": {"tables": ["users", "profiles"]}}},
        {"category": "replication_design", "inputs": {"db_type": "postgresql", "topology": "master-slave"}},
        {"category": "backup_recovery", "inputs": {"db_type": "postgresql", "rpo": 15, "rto": 30}},
        {"category": "performance_analysis", "inputs": {"slow_queries": ["SELECT * FROM logs WHERE..."]}},
        {"category": "schema_design", "inputs": {"requirements": ["users", "orders"], "db_type": "postgresql"}},
        {"category": "partitioning_strategy", "inputs": {"table": "logs", "rows": 100000000, "db_type": "postgresql"}},
        {"category": "deadlock_analysis", "inputs": {"transactions": ["tx1", "tx2"], "db_type": "postgresql"}},
        {"category": "capacity_planning", "inputs": {"current_usage": {"storage_gb": 100}, "growth_rate": "20%", "db_type": "postgresql"}},
    ],
    "qa_engineer": [
        {"category": "unit_test_generation", "inputs": {"code": "sample_code", "language": "python"}},
        {"category": "integration_test_generation", "inputs": {"api_spec": {"endpoints": [{"path": "/users", "method": "GET"}]}}},
        {"category": "regression_testing", "inputs": {"changes": ["feature_x"], "existing_tests": ["test_a", "test_b"]}},
        {"category": "mutation_testing", "inputs": {"code": "sample_code", "test_suite": ["test_a", "test_b"]}},
        {"category": "flaky_test_detection", "inputs": {"test_history": [{"test": "test_a", "results": ["pass", "fail", "pass"]}]}},
        {"category": "coverage_analysis", "inputs": {"code": "sample_code", "tests": ["test_a", "test_b"]}},
        {"category": "performance_validation", "inputs": {"requirements": {"p95_latency_ms": 200}, "results": {"p95_latency_ms": 180}}},
        {"category": "golden_test_generation", "inputs": {"pack_id": "network_engineer", "scenarios": ["scenario1"]}},
        {"category": "benchmark_testing", "inputs": {"pack_id": "network_engineer", "scenarios": ["scenario1"]}},
        {"category": "security_testing", "inputs": {"code": "sample_code", "standard": "OWASP"}},
    ],
    "business_analyst": [
        {"category": "requirement_gathering", "inputs": {"stakeholder_notes": "sample_notes", "domain": "e-commerce"}},
        {"category": "process_modeling", "inputs": {"description": "order fulfillment process", "domain": "e-commerce"}},
        {"category": "user_story_generation", "inputs": {"requirements": [{"id": "REQ-1", "title": "User login"}], "personas": [{"name": "Buyer"}]}},
        {"category": "use_case_modeling", "inputs": {"requirements": [{"id": "REQ-1"}], "actors": ["Buyer", "Seller"]}},
        {"category": "brd_generation", "inputs": {"requirements": [{"id": "REQ-1"}], "context": {"project": "Online Shop"}}},
        {"category": "functional_spec", "inputs": {"requirements": [{"id": "REQ-1"}], "user_stories": [{"id": "US-1"}]}},
        {"category": "gap_analysis", "inputs": {"current_state": "manual process", "target_state": "automated system", "constraints": ["budget", "time"]}},
        {"category": "roi_analysis", "inputs": {"costs": {"development": 100000, "maintenance": 20000}, "benefits": {"revenue_increase": 150000}, "time_horizon": 36}},
        {"category": "process_optimization", "inputs": {"process_description": "order fulfillment", "metrics": {"cycle_time": "3 days"}}},
        {"category": "acceptance_criteria", "inputs": {"user_story": "As a Buyer I want to login so that I can access my account", "domain": "e-commerce"}},
    ],
    "infrastructure_engineer": [
        {"category": "kubernetes_design", "inputs": {"service": "web-api", "node_count": 3, "k8s_version": "1.28"}},
        {"category": "ha_cluster_design", "inputs": {"service": "postgres", "node_count": 3, "availability": "99.99%"}},
        {"category": "storage_design", "inputs": {"workload": "database", "size_gb": 500, "iops": 10000}},
        {"category": "disaster_recovery", "inputs": {"service": "web-api", "rpo": 15, "rto": 30}},
        {"category": "load_balancer_design", "inputs": {"service": "web-api", "backend_count": 5}},
        {"category": "proxmox_design", "inputs": {"node_count": 3, "vm_count": 20}},
        {"category": "ceph_design", "inputs": {"osd_count": 12, "replication_factor": 3}},
        {"category": "docker_swarm_design", "inputs": {"manager_count": 3, "worker_count": 5}},
        {"category": "vmware_design", "inputs": {"esxi_count": 4, "vm_count": 50}},
        {"category": "multi_region_dr", "inputs": {"primary_region": "us-east-1", "secondary_region": "eu-west-1"}},
    ],
    "ai_engineer": [
        {"category": "rag_design", "inputs": {"use_case": "customer_support", "chunking_strategy": "hybrid", "top_k": 5}},
        {"category": "agent_design", "inputs": {"agent_type": "hierarchical", "agent_count": 3}},
        {"category": "prompt_engineering", "inputs": {"template_type": "code_generation", "language": "python"}},
        {"category": "llmops_deployment", "inputs": {"environment": "production", "scaling_min": 2}},
        {"category": "fine_tuning", "inputs": {"base_model": "llama-3-8b", "epochs": 3, "batch_size": 8}},
        {"category": "evaluation_framework", "inputs": {"metrics": ["accuracy", "f1", "latency"], "test_cases": 100}},
        {"category": "guardrails", "inputs": {"guardrail_types": ["content_filter", "pii_detection"]}},
        {"category": "observability", "inputs": {"metrics": ["latency", "token_usage", "drift"]}},
        {"category": "graph_rag", "inputs": {"entity_types": ["person", "org", "document"]}},
        {"category": "agent_pipeline", "inputs": {"steps": ["search", "filter", "summarize", "synthesize"]}},
    ],
    "documentation_engineer": [
        {"category": "openapi_generation", "inputs": {"source_type": "fastapi", "output_format": "yaml"}},
        {"category": "sdk_docs_generation", "inputs": {"language": "python", "include_examples": True}},
        {"category": "architecture_docs", "inputs": {"source_type": "adr", "adr_count": 5}},
        {"category": "release_notes", "inputs": {"version": "1.2.0", "changes_count": 15}},
        {"category": "documentation_validation", "inputs": {"validation_rules": ["broken_links", "missing_sections"]}},
        {"category": "rfc_documentation", "inputs": {"rfc_type": "feature", "sections": ["motivation", "design"]}},
        {"category": "multi_language_docs", "inputs": {"languages": ["python", "typescript", "go"]}},
        {"category": "changelog_generation", "inputs": {"versions": ["v1", "v2"], "include_breaking": True}},
        {"category": "docs_sync", "inputs": {"packs": ["code_engineer", "devops_assistant"], "sync_frequency": "daily"}},
        {"category": "coverage_analysis", "inputs": {"coverage_target": 0.95, "include_undocumented": True}},
    ],
    "product_manager": [
        {"category": "product_vision", "inputs": {"market": "SMB", "vision_horizon_years": 3, "target_users": ["startups", "freelancers"]}},
        {"category": "roadmap_planning", "inputs": {"quarters": 4, "themes": ["growth", "retention"]}},
        {"category": "backlog_prioritization", "inputs": {"items_count": 50, "framework": "RICE"}},
        {"category": "sprint_planning", "inputs": {"sprint_duration_weeks": 2, "team_capacity_points": 30}},
        {"category": "okr_tracking", "inputs": {"objectives_count": 3, "krs_per_objective": 3}},
        {"category": "kpi_dashboard", "inputs": {"metrics": ["MRR", "Churn", "NPS", "CAC"], "target_accuracy": 0.95}},
        {"category": "product_discovery", "inputs": {"user_segments": ["enterprise", "smb"], "research_methods": ["interview", "survey"]}},
        {"category": "release_planning", "inputs": {"features_count": 8, "rollout_strategy": "canary", "target_date": "2025-06-01"}},
        {"category": "prioritization_matrix", "inputs": {"features": 20, "criteria": ["impact", "effort", "risk", "strategic_fit"]}},
        {"category": "stakeholder_alignment", "inputs": {"stakeholders": ["engineering", "sales", "support"], "conflicts": ["resource", "timeline"]}},
    ],
    "ui_ux_designer": [
        {"category": "user_journey", "inputs": {"user_segments": ["buyer", "seller"], "touchpoints": 8}},
        {"category": "design_system", "inputs": {"components_count": 30, "tokens": ["color", "typography", "spacing"]}},
        {"category": "wireframe", "inputs": {"screens_count": 12, "platform": "mobile"}},
        {"category": "prototype", "inputs": {"fidelity": "high", "interactions": 15, "screens": 6}},
        {"category": "accessibility_audit", "inputs": {"target_level": "AA", "check_contrast": True, "check_keyboard": True}},
        {"category": "interaction_design", "inputs": {"form_fields": 20, "validation_rules": 15, "error_states": True}},
        {"category": "ux_research", "inputs": {"user_interviews": 10, "surveys": 100, "personas": 3}},
        {"category": "design_review", "inputs": {"screens": 20, "review_criteria": ["consistency", "accessibility", "usability"]}},
        {"category": "responsive_design", "inputs": {"breakpoints": ["mobile", "tablet", "desktop"], "components": 50}},
        {"category": "component_specs", "inputs": {"component_types": ["button", "input", "modal"], "variants_per_component": 4}},
    ],
    "full_stack_engineer": [
        {"category": "architecture_review", "inputs": {"repo_path": ".", "language": "python"}},
        {"category": "code_review", "inputs": {"code": "sample_code", "language": "python"}},
        {"category": "refactoring_plan", "inputs": {"repo_path": ".", "issue": "circular_dependency"}},
        {"category": "test_engineering", "inputs": {"repo_path": ".", "test_type": "unit"}},
        {"category": "performance_analysis", "inputs": {"code": "sample_code", "language": "python"}},
        {"category": "release_readiness", "inputs": {"repo_path": ".", "version": "1.2.0"}},
        {"category": "api_design_review", "inputs": {"api_spec": {"openapi": "3.0.0"}}},
        {"category": "integration_testing", "inputs": {"components": ["api", "frontend"], "interfaces": ["REST", "GraphQL"]}},
        {"category": "deployment_readiness", "inputs": {"repo_path": ".", "platform": "kubernetes"}},
        {"category": "security_review", "inputs": {"code": "sample_code", "language": "python", "standard": "OWASP"}},
    ],
}


def get_scenario_template(pack_id, index):
    templates = BASE_TEMPLATES.get(pack_id, [{"category": "general", "inputs": {}}])
    template = templates[index % len(templates)]
    return {
        "test_id": f"{pack_id[:3]}-{index+1:03d}",
        "name": f"Golden Test {index+1} for {pack_id}",
        "category": template["category"],
        "inputs": template["inputs"],
        "expected_output": {"quality_score": 0.9, "valid": True},
        "acceptance_criteria": [
            "Output must be valid according to pack schema",
            "Quality score must be >= 0.9",
            "All required fields must be present",
            "No security violations in output",
            "Execution time must be < 5000ms"
        ],
        "edge_cases": ["empty_input", "max_input_size", "special_characters"],
        "negative_cases": ["invalid_schema", "missing_required_fields", "type_mismatch"],
        "performance_targets": {
            "latency_p95_ms": 5000,
            "memory_mb": 512,
            "token_budget": 4000
        },
        "explainability_requirements": {
            "summary": True,
            "evidence": True,
            "reasoning": True,
            "alternatives": True,
            "risk": True,
            "confidence": True,
            "decision": True,
            "next_action": True
        }
    }


def main():
    for pack_id in PACKS:
        os.makedirs(f"golden_tests/{pack_id}", exist_ok=True)
        for i in range(20):
            scenario = get_scenario_template(pack_id, i)
            path = f"golden_tests/{pack_id}/scenario_{i+1:02d}_{scenario['category']}.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(scenario, f, indent=2, ensure_ascii=False)
    print(f"Generated golden tests for {len(PACKS)} packs")


if __name__ == "__main__":
    main()
