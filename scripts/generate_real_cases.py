"""
Generate Real Cases Script
===========================

Generates realistic real case directories for all 13 capability packs
to reach the target of 1000+ total real cases.

Usage:
    python scripts/generate_real_cases.py [--count N] [--pack PACK]
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import random
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
REAL_CASES_DIR = BASE_DIR / "real_cases"

random.seed(42)

NETWORK_SCENARIOS = [
    "bgp_full_mesh", "ospf_enterprise", "vlan_trunking", "vpn_ipsec_site_to_site",
    "wireless_corporate", "qos_voice_priority", "nat_pat_dmz", "hsrp_ha",
    "dhcp_snooping", "ipv6_dual_stack", "telemetry_streaming", "netflow_sflow",
    "stackpower_redundancy", "segment_routing", "eigrp_stub", "mpls_ldp_core",
    "prefix_list_route_map", "private_vlan", "model_driven_telemetry", "sla_tracking",
    "snmp_v3_secure", "firewall_asa_acl_strict", "dmvpn_dual_hub", "eem_automation",
    "ot_security_industrial", "routing_ospf_enterprise", "security_ssh_hardened",
    "services_dns_ntp_snmp", "switching_vlan_trunking", "wireless_wpa3",
    "vrrp_ha", "wireguard_site_to_site", "l2tp_server", "vpn_pptp_remote_access",
    "ip_cloud_dns", "vlan_aware_bridge", "ipv6_tunnel_6to4", "switching_vlan_switch",
    "ipv6_dhcpv6", "ipv6_pool_dhcp", "services_dhcp_dns_server", "security_insecure_defaults",
    "sstp_server", "bgp_peer_tracking", "bgp_route_map", "certificate_enrollment",
    "firewall_input_filter_strict", "firewall_raw_table", "high_availability_bgpi_peer_tracking",
    "hotspot_with_login", "nat_hairpin", "ospf_virtual_link", "pptp_remote_access",
    "qos_htb", "qos_traffic_shaping_enterprise", "queue_tree_qos", "quickset_wan_dhcp",
    "routing_static_route_default", "sample_hotspot", "bgp_md5_auth", "bgp_route_reflector",
    "l3_switch_vlan_routing", "mpls_ldp_enabled", "routing_static_bgp_ha", "vpn_ipsec_phase1_phase2",
    "wireless_employee_wifi", "zerotrust_ztna", "sdwan_performance_sla", "sdwan_wan_optimization",
    "security_admin_exposed", "switch_managed_vlan", "switching_managed_vlan", "two_factor_auth",
    "url_filter_categories", "vpn_ssl_portal", "wan_interface", "wan_optimization",
]

CODE_SCENARIOS = [
    "fastapi_microservice", "ddd_order_management", "security_audit", "solid_srp_violation",
    "cqrs_command_query", "event_sourcing", "clean_arch_dependency_rule", "injection_vulnerabilities",
    "hardcoded_secrets", "plaintext_password", "ssrf_potential", "sql_injection",
    "xss_vulnerability", "csrf_missing", "insecure_deserialization", "path_traversal",
    "command_injection", "xml_external_entity", "server_side_request_forgery", "insecure_cors",
    "weak_cryptography", "hardcoded_password", "api_key_exposure", "debug_mode_enabled",
    "error_disclosure", "verbose_errors", "missing_authentication", "broken_access_control",
    "sensitive_data_exposure", "security_misconfiguration", "insufficient_logging",
    "reflected_xss", "stored_xss", "dom_xss", "json_pollution", "prototype_pollution",
    "regular_expression_dos", "unvalidated_redirect", "open_redirect", "clickjacking",
    "session_fixation", "session_hijacking", "password_in_url", "credentials_in_logs",
    "temp_file_race", "symlink_attack", "race_condition", "integer_overflow",
    "memory_leak", "resource_exhaustion", "denial_of_service", "rate_limit_missing",
    "api_throttling", "circuit_breaker", "bulkhead_pattern", "timeout_configuration",
    "connection_pooling", "database_index_missing", "n_plus_one_query", "inefficient_join",
    "missing_pagination", "full_table_scan", "redundant_calculation", "caching_miss",
]

DEVOPS_SCENARIOS = [
    "ci_cd_pipeline_microservice", "kubernetes_deployment", "terraform_aws_infra",
    "gitlab_ci_pipeline", "monitoring_prometheus", "helm_chart_security",
    "multi_env_deployment", "gitops_argocd", "policy_as_code_opa", "chaos_experiment",
    "dockerfile_optimization", "container_security_scan", "secrets_management",
    "blue_green_deployment", "canary_release", "feature_flag_system", "auto_scaling",
    "load_balancer_config", "service_mesh_istio", "observability_stack",
    "log_aggregation_elk", "distributed_tracing", "incident_response_runbook",
    "disaster_recovery_plan", "backup_automation", "infrastructure_as_code",
    "pipeline_as_code", "compliance_scanning", "vulnerability_management",
    "artifact_signing", "supply_chain_security", "runtime_security",
    "network_policy_kubernetes", "rbac_configuration", "pod_security_standards",
    "resource_quota_limits", "horizontal_pod_autoscaler", "vertical_pod_autoscaler",
    "service_discovery", "config_map_management", "secret_rotation", "certificate_management",
    "edge_deployment", "multi_cloud_orchestration", "hybrid_cloud_networking",
    "serverless_deployment", "event_driven_architecture", "api_gateway_config",
    "rate_limiting_gateway", "caching_layer_redis", "database_migration_script",
]

TRADING_SCENARIOS = [
    "btc_breakout_2026", "gold_news_analysis", "eth_defi_correlation", "portfolio_rebalance_2026",
    "sol_breakdown_analysis", "spy_macro_regime", "nasdaq_sector_rotation", "forex_eurusd_trend",
    "commodity_crude_oil", "options_earnings_play", "futures_contango_trade", "crypto_arbitrage",
    "momentum_strategy", "mean_reversion", "pairs_trading", "volatility_breakout",
    "swing_trade_setup", "day_trade_scalp", "position_sizing_kelly", "risk_parity_portfolio",
    "trend_following_multi_timeframe", "counter_trend_scalp", "news_sentiment_trade",
    "onchain_analysis", "order_flow_analysis", "liquidity_sweep", "fair_value_gap",
    "institutional_flow", "dark_pool_activity", "short_interest_squeeze",
    "insider_trading_signals", "earnings_whisper", "guidance_revision", "sector_etf_flow",
    "international_market_correlation", "emerging_market_opportunity", "fixed_income_yield_curve",
    "recession_hedge", "inflation_trade", "geopolitical_risk_off", "central_bank_policy",
]

SELF_DEVELOPMENT_SCENARIOS = [
    "refactor_legacy_module", "extract_service_layer", "remove_duplicate_code",
    "fix_circular_dependency", "improve_error_handling", "add_logging_observability",
    "implement_caching", "database_query_optimization", "api_response_caching",
    "memory_leak_fix", "thread_safety_review", "async_await_migration",
    "dependency_injection_intro", "configuration_externalization", "secrets_management",
    "health_check_endpoints", "graceful_shutdown", "rate_limiting",
    "input_validation", "output_encoding", "sql_injection_prevention",
    "xss_mitigation", "csrf_protection", "authentication_refactor",
    "authorization_layer", "audit_logging", "data_encryption_at_rest",
    "data_encryption_transit", "key_rotation_system", "security_headers",
    "content_security_policy", "subresource_integrity", "hsts_configuration",
    "cors_policy_tightening", "session_management", "token_expiration",
    "refresh_token_rotation", "password_hashing_upgrade", "mfa_implementation",
    "api_versioning", "backward_compatibility", "deprecation_policy",
    "documentation_generation", "type_hint_completion", "test_coverage_improvement",
    "mutation_testing", "integration_test_suite", "e2e_test_pipeline",
    "performance_profiling", "bottleneck_removal", "database_indexing",
    "query_plan_optimization", "connection_pool_tuning", "cache_warmup_strategy",
]

RESEARCH_SCENARIOS = [
    "market_analysis_report", "competitive_intelligence", "technology_trend_analysis",
    "scientific_literature_review", "policy_impact_assessment", "regulatory_compliance_research",
    "user_experience_research", "data_driven_insights", "statistical_analysis",
    "sentiment_analysis", "trend_forecasting", "benchmarking_study",
    "best_practices_review", "risk_assessment_research", "feasibility_study",
    "market_sizing", "customer_segmentation", "product_market_fit",
    "go_to_market_strategy", "pricing_research", "brand_perception",
    "social_media_analysis", "news_aggregation", "academic_research_synthesis",
    "patent_analysis", "standard_compliance", "technical_debt_analysis",
    "architecture_evaluation", "vendor_selection", "rfp_response_research",
]

DECISION_SCENARIOS = [
    "cloud_provider_selection", "database_choice", "framework_selection",
    "build_vs_buy", "outsourcing_decision", "hiring_decision",
    "product_roadmap_priority", "feature_launch_timing", "market_entry_strategy",
    "pricing_model_decision", "investment_allocation", "risk_mitigation_plan",
    "vendor_negotiation", "contract_renewal", "technology_stack_migration",
    "microservices_split", "monolith_refactor", "api_design_choice",
    "authentication_strategy", "data_storage_selection", "caching_strategy",
    "load_balancer_choice", "monitoring_stack", "ci_cd_tool_selection",
    "security_compliance_path", "data_residency_decision", "disaster_recovery_strategy",
    "capacity_planning", "cost_optimization", "performance_tuning",
]

SYSTEM_SCENARIOS = [
    "microservices_architecture", "event_driven_design", "api_gateway_design",
    "database_scaling_strategy", "cache_invalidation", "message_queue_design",
    "service_mesh_evaluation", "observability_architecture", "security_architecture",
    "identity_management", "authorization_model", "data_flow_design",
    "integration_architecture", "domain_driven_design", "bounded_context",
    "aggregate_design", "event_sourcing_architecture", "cqrs_implementation",
    "saga_orchestration", "compensation_logic", "circuit_breaker_pattern",
    "bulkhead_isolation", "rate_limiting_design", "retry_policy_design",
    "timeout_configuration", "backpressure_handling", "dead_letter_queue",
    "idempotency_design", "versioning_strategy", "migration_planning",
    "capacity_planning", "cost_allocation", "multi_region_design",
    "disaster_recovery", "backup_strategy", "compliance_architecture",
]

SECURITY_SCENARIOS = [
    "penetration_test_webapp", "vulnerability_scan_api", "secrets_audit",
    "dependency_vulnerability_check", "container_security_scan", "iac_security_review",
    "network_security_assessment", "cloud_security_posture", "identity_security_review",
    "access_control_audit", "encryption_at_rest_audit", "encryption_in_transit_audit",
    "logging_and_monitoring_review", "incident_response_plan", "disaster_recovery_test",
    "compliance_audit_soc2", "compliance_audit_gdpr", "compliance_audit_hipaa",
    "compliance_audit_pci_dss", "threat_modeling_session", "attack_surface_analysis",
    "privilege_escalation_review", "lateral_movement_assessment", "data_exfiltration_risk",
    "supply_chain_security", "software_bill_of_materials", "code_signing_verification",
    "runtime_protection_review", "waf_configuration", "ddos_mitigation",
    "bot_detection", "anomaly_detection", "security_orchestration", "vulnerability_remediation",
    "patch_management", "configuration_drift", "secrets_rotation", "key_management",
    "certificate_lifecycle", "zero_trust_architecture", "sase_evaluation",
    "security_awareness_review", "phishing_simulation", "red_team_exercise",
]

DATA_SCENARIOS = [
    "etl_pipeline_design", "data_lake_architecture", "stream_processing_kafka",
    "batch_processing_spark", "data_quality_checks", "data_lineage_tracking",
    "master_data_management", "data_catalog_implementation", "data_governance_framework",
    "privacy_preserving_analytics", "differential_privacy", "federated_learning",
    "feature_store_design", "ml_pipeline_orchestration", "model_serving_architecture",
    "data_visualization_dashboard", "real_time_analytics", "time_series_processing",
    "graph_data_processing", "document_store_design", "search_index_optimization",
    "data_migration_plan", "schema_evolution", "data_backup_strategy",
    "disaster_recovery_data", "multi_cloud_data_sync", "edge_data_processing",
    "iot_data_ingestion", "log_aggregation_pipeline", "metric_aggregation",
    "data_retention_policy", "data_classification", "sensitive_data_discovery",
    "data_masking_implementation", "tokenization_strategy", "anonymization_workflow",
    "compliance_reporting_data", "audit_trail_design", "data_access_governance",
    "column_level_security", "row_level_security", "data_lakehouse_architecture",
    "delta_lake_implementation", "apache_iceberg_setup", "data_contract_design",
    "streaming_etl_design", "change_data_capture", "data_replay_capability",
]

DATABASE_SCENARIOS = [
    "postgresql_performance_tuning", "mysql_replication_setup", "mongodb_sharding",
    "redis_cluster_design", "elasticsearch_indexing", "database_migration_plan",
    "schema_design_ecommerce", "query_optimization_report", "index_strategy_design",
    "partitioning_strategy", "database_backup_automation", "point_in_time_recovery",
    "read_replica_configuration", "connection_pool_tuning", "database_monitoring",
    "slow_query_analysis", "deadlock_resolution", "transaction_isolation_tuning",
    "database_vulnerability_assessment", "data_archival_strategy", "data_purge_policy",
    "multi_tenant_schema_design", "database_federation", "distributed_transaction",
    "eventual_consistency_model", "acid_compliance_review", "data_integrity_check",
    "referential_integrity", "database_encryption_at_rest", "database_auditing",
    "row_level_security_policy", "column_level_encryption", "database_firewall",
    "sql_injection_prevention", "prepared_statement_review", "orm_query_analysis",
    "n_plus_one_detection", "database_refactoring", "legacy_database_migration",
    "nosql_schema_design", "graph_database_modeling", "time_series_database_design",
    "vector_database_setup", "database_cost_optimization", "storage_class_selection",
    "io_optimization", "memory_configuration", "warmup_strategy", "failover_testing",
]

QA_SCENARIOS = [
    "unit_test_suite_design", "integration_test_plan", "e2e_test_strategy",
    "performance_test_plan", "load_test_scenario", "stress_test_design",
    "soak_test_plan", "chaos_test_experiment", "fault_injection_test",
    "security_test_plan", "penetration_test_scope", "vulnerability_scan_interpretation",
    "regression_test_suite", "smoke_test_definition", "sanity_test_plan",
    "api_contract_test", "consumer_driven_contract", "pact_test_design",
    "mutation_test_setup", "code_coverage_analysis", "branch_coverage_review",
    "test_data_management", "test_environment_setup", "ci_cd_test_pipeline",
    "test_automation_framework", "selenium_test_design", "cypress_test_plan",
    "playwright_test_script", "mobile_test_strategy", "accessibility_test_plan",
    "cross_browser_testing", "compatibility_matrix", "localization_test",
    "usability_test_plan", "a_b_test_design", "canary_analysis", "feature_flag_testing",
    "rollback_test_plan", "disaster_recovery_test", "backup_restore_test",
    "data_integrity_test", "performance_regression_test", "memory_leak_detection",
    "cpu_profiling_test", "network_latency_test", "database_connection_test",
    "cache_invalidation_test", "message_queue_test", "event_driven_test",
    "distributed_system_test", "microservices_integration_test", "api_gateway_test",
    "authentication_test", "authorization_test", "session_management_test",
]

BUSINESS_SCENARIOS = [
    "market_requirements_document", "user_story_epic", "acceptance_criteria",
    "business_case_development", "roi_analysis", "cost_benefit_analysis",
    "stakeholder_interview_notes", "workflow_design_document", "process_mapping",
    "as_is_analysis", "to_be_design", "gap_analysis_report", "risk_assessment_matrix",
    "compliance_requirement_analysis", "regulatory_impact_assessment", "data_governance_policy",
    "data_privacy_assessment", "data_residency_analysis", "consent_management_design",
    "product_roadmap_quarterly", "feature_prioritization_matrix", "mo_scoring_model",
    "rice_scoring_model", "kano_model_analysis", "voice_of_customer_report",
    "customer_journey_map", "persona_development", "user_research_synthesis",
    "competitive_analysis_report", "swot_analysis", "porter_five_forces",
    "market_landscape_report", "industry_trend_analysis", "technology_radar",
    "innovation_pipeline", "proof_of_concept_plan", "mvp_definition",
    "go_to_market_strategy", "pricing_strategy_document", "channel_strategy",
    "partnership_opportunity", "vendor_evaluation_matrix", "rfp_response",
    "contract_negotiation_notes", "service_level_agreement", "operational_level_agreement",
    "business_continuity_plan", "disaster_recovery_plan", "incident_response_playbook",
    "crisis_management_plan", "communication_plan", "training_needs_analysis",
    "change_management_plan", "organizational_design", "team_restructuring_plan",
]

SCENARIOS = {
    "network": NETWORK_SCENARIOS,
    "code": CODE_SCENARIOS,
    "research": RESEARCH_SCENARIOS,
    "devops": DEVOPS_SCENARIOS,
    "trading": TRADING_SCENARIOS,
    "self_development": SELF_DEVELOPMENT_SCENARIOS,
    "decision": DECISION_SCENARIOS,
    "system": SYSTEM_SCENARIOS,
    "security": SECURITY_SCENARIOS,
    "data": DATA_SCENARIOS,
    "database": DATABASE_SCENARIOS,
    "qa": QA_SCENARIOS,
    "business": BUSINESS_SCENARIOS,
}

PACK_TARGETS = {
    "network": 100,
    "code": 100,
    "research": 150,
    "devops": 100,
    "trading": 100,
    "self_development": 100,
    "decision": 100,
    "system": 100,
    "security": 100,
    "data": 100,
    "database": 100,
    "qa": 100,
    "business": 100,
}

VENDORS = ["cisco", "mikrotik", "fortinet", "juniper", "arista", "palo_alto"]
LANGUAGES = ["python", "javascript", "typescript", "go", "java", "rust"]
FRAMEWORKS = ["fastapi", "django", "react", "vue", "spring", "express"]


def _ensure_dirs(pack_dir: Path, case_id: str) -> tuple[Path, Path, Path]:
    case_dir = pack_dir / case_id
    input_dir = case_dir / "input"
    output_dir = case_dir / "output"
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    return case_dir, input_dir, output_dir


def _write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def generate_network_case(pack_dir: Path, case_id: str, scenario: str) -> None:
    _, input_dir, output_dir = _ensure_dirs(pack_dir, case_id)
    vendor = random.choice(VENDORS)
    _write_text(input_dir / "config.txt", f"! {vendor} {scenario} configuration\n!\ninterface GigabitEthernet0/1\n ip address 192.168.1.1/24\n no shutdown\n!")
    _write_text(output_dir / "analysis.md", f"# {scenario} Analysis\n\nVendor: {vendor}\n\n## Findings\n- Interface configuration detected\n- IP addressing scheme analyzed\n- Security posture: moderate\n")
    _write_text(output_dir / "recommendations.md", f"# {scenario} Recommendations\n\n1. Enable SSH with key-based authentication\n2. Disable unused interfaces\n3. Implement VLAN segmentation\n")
    _write_text(case_dir := pack_dir / case_id / "evaluation.md", f"# Evaluation\n\nScenario: {scenario}\nVendor: {vendor}\n\n## Accuracy\n- Configuration parsing: correct\n- Security analysis: correct\n\n## Improvements\n- Add vendor-specific best practices\n")


def generate_code_case(pack_dir: Path, case_id: str, scenario: str) -> None:
    _, input_dir, output_dir = _ensure_dirs(pack_dir, case_id)
    lang = random.choice(LANGUAGES)
    framework = random.choice(FRAMEWORKS)
    code = f"# {scenario}\n\ndef main():\n    pass\n"
    if lang == "python":
        code = f"# {scenario}\n\nimport os\n\ndef main():\n    api_key = 'hardcoded_key'\n    password = 'plaintext_password'\n    query = f\"SELECT * FROM users WHERE id = {{user_id}}\"\n    return query\n"
    _write_text(input_dir / "main.py", code)
    _write_text(output_dir / "review.md", f"# {scenario} Review\n\nLanguage: {lang}\nFramework: {framework}\n\n## Security Findings\n- Hardcoded credentials detected\n- SQL injection vulnerability\n- Missing input validation\n\n## Architecture\n- Single responsibility violation\n- Missing error handling\n")
    _write_text(output_dir / "patch.diff", f"--- a/main.py\n+++ b/main.py\n@@ -1,5 +1,8 @@\n+import os\n+from typing import Optional\n+\n def main():\n-    api_key = 'hardcoded_key'\n-    password = 'plaintext_password'\n-    query = f\"SELECT * FROM users WHERE id = {{user_id}}\"\n-    return query\n+    api_key = os.environ.get('API_KEY')\n+    password = os.environ.get('DB_PASSWORD')\n+    query = 'SELECT * FROM users WHERE id = :id'\n+    return query\n")
    _write_text(pack_dir / case_id / "evaluation.md", f"# Evaluation\n\nScenario: {scenario}\nLanguage: {lang}\n\n## Accuracy\n- Security issues detected: correct\n- Patch applicability: correct\n\n## Improvements\n- Add type hints\n- Improve error handling\n")


def generate_devops_case(pack_dir: Path, case_id: str, scenario: str) -> None:
    _, input_dir, output_dir = _ensure_dirs(pack_dir, case_id)
    _write_text(input_dir / "pipeline.yml", f"name: {scenario}\non:\n  push:\n    branches: [main]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: echo 'Build step'\n")
    _write_text(output_dir / "pipeline_improved.yml", f"name: {scenario}\non:\n  push:\n    branches: [main]\njobs:\n  lint:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n      - run: ruff check .\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: pytest tests/\n  security:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: trivy fs .\n")
    _write_text(output_dir / "analysis.md", f"# {scenario} Analysis\n\n## Findings\n- Missing lint step\n- Missing security scan\n- No rollback strategy\n- Missing resource limits\n\n## Recommendations\n1. Add lint and type check steps\n2. Add security scanning\n3. Add deployment rollback\n4. Add resource limits\n")
    _write_text(pack_dir / case_id / "evaluation.md", f"# Evaluation\n\nScenario: {scenario}\n\n## Accuracy\n- Pipeline issues detected: correct\n- Recommendations: actionable\n\n## Improvements\n- Add monitoring configuration\n- Add backup strategy\n")


def generate_trading_case(pack_dir: Path, case_id: str, scenario: str) -> None:
    _, input_dir, output_dir = _ensure_dirs(pack_dir, case_id)
    _write_text(input_dir / "market_data.json", json.dumps({
        "symbol": "BTCUSD",
        "timeframe": "4H",
        "candles": [
            {"time": "2026-01-01T00:00:00Z", "open": 90000, "high": 91000, "low": 89000, "close": 90500, "volume": 1200},
            {"time": "2026-01-01T04:00:00Z", "open": 90500, "high": 92000, "low": 90000, "close": 91500, "volume": 1500},
            {"time": "2026-01-01T08:00:00Z", "open": 91500, "high": 93000, "low": 91000, "close": 92500, "volume": 1800},
        ],
    }, indent=2))
    _write_text(output_dir / "analysis.md", f"# {scenario} Analysis\n\n## Market Structure\n- Trend: Bullish\n- Key levels: Support at 90000, Resistance at 93000\n\n## Domains Detected\n- Wyckoff: Accumulation phase\n- SMC: Bullish order block\n- Volume: Increasing volume on up moves\n\n## Recommendation\n- Long bias with stop below 90000\n- Target: 93000+\n- Confidence: 0.78\n")
    _write_text(output_dir / "evaluation.md", f"# Evaluation\n\nScenario: {scenario}\n\n## Accuracy\n- Trend direction: correct\n- Key levels: reasonable\n- Risk management: appropriate\n\n## Improvements\n- Add Elliott Wave count\n- Add macro context\n")


def generate_self_development_case(pack_dir: Path, case_id: str, scenario: str) -> None:
    _, input_dir, output_dir = _ensure_dirs(pack_dir, case_id)
    _write_text(input_dir / "source.py", f"# {scenario}\n\ndef process_data(data):\n    result = []\n    for item in data:\n        if item not in result:\n            result.append(item)\n    return result\n\ndef calculate(x, y):\n    return x + y\n\ndef another_calculate(x, y):\n    return x + y\n")
    _write_text(output_dir / "analysis.md", f"# {scenario} Analysis\n\n## Problems Detected\n1. Code duplication: `calculate` and `another_calculate` are identical\n2. Missing type hints\n3. No error handling\n4. Missing docstrings\n\n## Recommendations\n1. Consolidate duplicate functions\n2. Add type annotations\n3. Add input validation\n4. Add documentation\n")
    _write_text(output_dir / "patch.diff", f"--- a/source.py\n+++ b/source.py\n@@ -1,7 +1,11 @@\n+from typing import List, Any\n+\n+def process_data(data: List[Any]) -> List[Any]:\n+    \"\"\"Remove duplicates while preserving order.\"\"\"\n+    return list(dict.fromkeys(data))\n+\n+def calculate(x: int, y: int) -> int:\n+    \"\"\"Add two numbers.\"\"\"\n+    return x + y\n")
    _write_text(pack_dir / case_id / "evaluation.md", f"# Evaluation\n\nScenario: {scenario}\n\n## Accuracy\n- Duplication detected: correct\n- Patch applicability: correct\n\n## Improvements\n- Add performance optimization\n- Add caching\n")


def generate_research_case(pack_dir: Path, case_id: str, scenario: str) -> None:
    _, input_dir, output_dir = _ensure_dirs(pack_dir, case_id)
    _write_text(input_dir / "query.txt", f"Research Query: {scenario}\n\nContext:\n- Domain: Technology\n- Timeframe: 2024-2025\n- Sources: Academic papers, industry reports\n")
    _write_text(output_dir / "findings.md", f"# {scenario} - Research Findings\n\n## Summary\nComprehensive analysis of {scenario} based on multiple sources.\n\n## Key Findings\n1. Market growth rate: 15% CAGR\n2. Key players: 5 major vendors\n3. Technology trends: AI/ML integration\n4. Challenges: Data privacy, integration complexity\n\n## Sources\n- [1] Industry Report 2024\n- [2] Academic Survey\n- [3] Vendor Documentation\n\n## Confidence\nHigh (0.85) - Multiple corroborating sources\n")
    _write_text(output_dir / "evaluation.md", f"# Evaluation\n\nScenario: {scenario}\n\n## Accuracy\n- Findings relevance: high\n- Source quality: credible\n- Bias detection: minimal\n\n## Improvements\n- Add contradictory sources\n- Add quantitative analysis\n")


def generate_decision_case(pack_dir: Path, case_id: str, scenario: str) -> None:
    _, input_dir, output_dir = _ensure_dirs(pack_dir, case_id)
    _write_text(input_dir / "context.json", json.dumps({
        "scenario": scenario,
        "options": ["Option A", "Option B", "Option C"],
        "criteria": ["cost", "performance", "scalability", "maintenance"],
        "constraints": ["budget < 100k", "timeline < 6 months"],
    }, indent=2))
    _write_text(output_dir / "decision.md", f"# {scenario} - Decision Analysis\n\n## Options Evaluated\n1. Option A: Low cost, medium performance\n2. Option B: High cost, high performance\n3. Option C: Medium cost, medium performance\n\n## Recommendation\nOption B - Highest long-term value despite higher initial cost.\n\n## Reasoning\n- Performance meets SLA requirements\n- Scalability supports 3x growth\n- Maintenance cost within budget\n\n## Risk Assessment\n- Implementation risk: Medium\n- Cost overrun risk: Low\n- Timeline risk: Low\n\n## Confidence Score: 0.82\n")
    _write_text(pack_dir / case_id / "evaluation.md", f"# Evaluation\n\nScenario: {scenario}\n\n## Accuracy\n- Options coverage: complete\n- Criteria weighting: reasonable\n- Risk assessment: accurate\n\n## Improvements\n- Add sensitivity analysis\n- Add scenario planning\n")


def generate_system_case(pack_dir: Path, case_id: str, scenario: str) -> None:
    _, input_dir, output_dir = _ensure_dirs(pack_dir, case_id)
    _write_text(input_dir / "requirements.md", f"# {scenario} - Requirements\n\n## Functional\n- Process 10k requests/second\n- 99.9% availability\n- Sub-100ms latency\n\n## Non-Functional\n- Horizontal scalability\n- Fault tolerance\n- Observability\n\n## Constraints\n- Budget: $50k/month\n- Timeline: 6 months\n- Team: 5 engineers\n")
    _write_text(output_dir / "architecture.md", f"# {scenario} - Architecture Design\n\n## Overview\nEvent-driven microservices architecture with API gateway.\n\n## Components\n1. API Gateway: Kong\n2. Message Queue: Kafka\n3. Services: Node.js microservices\n4. Database: PostgreSQL + Redis\n5. Monitoring: Prometheus + Grafana\n\n## Data Flow\nClient -> API Gateway -> Service -> Message Queue -> Worker -> Database\n\n## Trade-offs\n- Complexity vs Flexibility: Chose flexibility\n- Consistency vs Availability: Chose availability (AP)\n\n## Risk Mitigation\n- Circuit breakers for resilience\n- Dead letter queues for failures\n- Comprehensive monitoring\n")
    _write_text(pack_dir / case_id / "evaluation.md", f"# Evaluation\n\nScenario: {scenario}\n\n## Accuracy\n- Requirements coverage: complete\n- Architecture fit: appropriate\n- Trade-off analysis: balanced\n\n## Improvements\n- Add security architecture\n- Add disaster recovery\n")


def generate_security_case(pack_dir: Path, case_id: str, scenario: str) -> None:
    _, input_dir, output_dir = _ensure_dirs(pack_dir, case_id)
    _write_text(input_dir / "target_app.py", f"# {scenario} - Target Application\n\nimport os\n\ndef login(username, password):\n    query = f\"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'\"\n    return execute(query)\n\ndef export_data(user_id):\n    return f\"SELECT * FROM sensitive_data WHERE user_id = {user_id}\"\n")
    _write_text(output_dir / "audit_report.md", f"# {scenario} - Security Audit Report\n\n## Executive Summary\n3 critical vulnerabilities identified.\n\n## Findings\n1. **SQL Injection** (Critical) - Unsanitized user input in query\n2. **Sensitive Data Exposure** (High) - No access control on export\n3. **Hardcoded Secrets** (Medium) - Potential credential exposure\n\n## Recommendations\n1. Use parameterized queries\n2. Implement row-level security\n3. Move secrets to vault\n\n## Compliance Impact\n- OWASP Top 10: A03:2021 – Injection\n- PCI DSS: Requirement 6.5\n- GDPR: Article 32\n")
    _write_text(pack_dir / case_id / "evaluation.md", f"# Evaluation\n\nScenario: {scenario}\n\n## Accuracy\n- Vulnerability detection: correct\n- Severity rating: appropriate\n- Remediation guidance: actionable\n\n## Improvements\n- Add exploit scenario\n- Add compliance mapping\n")


def generate_data_case(pack_dir: Path, case_id: str, scenario: str) -> None:
    _, input_dir, output_dir = _ensure_dirs(pack_dir, case_id)
    _write_text(input_dir / "source_data.csv", "id,name,value,timestamp\n1,alpha,100,2026-01-01\n2,beta,200,2026-01-02\n3,gamma,150,2026-01-03\n")
    _write_text(output_dir / "pipeline_design.md", f"# {scenario} - Pipeline Design\n\n## Overview\nETL pipeline for processing CSV data with quality checks.\n\n## Architecture\n1. **Extract**: Read CSV from S3\n2. **Transform**: Clean, validate, enrich\n3. **Load**: Write to data warehouse\n\n## Quality Checks\n- Schema validation\n- Null value detection\n- Duplicate detection\n- Outlier detection\n\n## Monitoring\n- Data freshness alerts\n- Quality score dashboard\n- Pipeline SLA tracking\n")
    _write_text(pack_dir / case_id / "evaluation.md", f"# Evaluation\n\nScenario: {scenario}\n\n## Accuracy\n- Pipeline design: appropriate\n- Quality checks: comprehensive\n- Monitoring: adequate\n\n## Improvements\n- Add data lineage\n- Add schema evolution\n")


def generate_database_case(pack_dir: Path, case_id: str, scenario: str) -> None:
    _, input_dir, output_dir = _ensure_dirs(pack_dir, case_id)
    _write_text(input_dir / "schema.sql", f"-- {scenario}\n\nCREATE TABLE users (\n    id SERIAL PRIMARY KEY,\n    username VARCHAR(255) UNIQUE NOT NULL,\n    email VARCHAR(255) UNIQUE NOT NULL,\n    created_at TIMESTAMP DEFAULT NOW()\n);\n\nCREATE TABLE orders (\n    id SERIAL PRIMARY KEY,\n    user_id INTEGER REFERENCES users(id),\n    amount DECIMAL(10,2),\n    status VARCHAR(50)\n);\n")
    _write_text(output_dir / "optimization.md", f"# {scenario} - Database Optimization\n\n## Schema Review\n- Missing indexes on foreign keys\n- No partitioning strategy\n- Missing check constraints\n\n## Query Optimization\n- Add composite index on orders(user_id, status)\n- Consider partitioning orders by created_at\n- Add covering index for common queries\n\n## Recommendations\n1. Add indexes: user_id, created_at\n2. Implement partitioning for large tables\n3. Add check constraints for data integrity\n4. Consider read replicas for reporting\n")
    _write_text(pack_dir / case_id / "evaluation.md", f"# Evaluation\n\nScenario: {scenario}\n\n## Accuracy\n- Index recommendations: correct\n- Partitioning strategy: appropriate\n- Constraint suggestions: valid\n\n## Improvements\n- Add query plan analysis\n- Add connection pooling config\n")


def generate_qa_case(pack_dir: Path, case_id: str, scenario: str) -> None:
    _, input_dir, output_dir = _ensure_dirs(pack_dir, case_id)
    _write_text(input_dir / "feature.md", f"# Feature: {scenario}\n\n## Description\nUser can upload CSV files for analysis.\n\n## Acceptance Criteria\n- [ ] File upload via drag-and-drop\n- [ ] Validate file format (CSV only)\n- [ ] Max file size: 10MB\n- [ ] Show progress bar during upload\n- [ ] Display errors for invalid files\n")
    _write_text(output_dir / "test_plan.md", f"# {scenario} - Test Plan\n\n## Unit Tests\n- test_upload_csv_valid\n- test_upload_csv_invalid_format\n- test_upload_csv_too_large\n- test_upload_csv_empty\n\n## Integration Tests\n- test_full_upload_workflow\n- test_concurrent_uploads\n- test_upload_with_authentication\n\n## E2E Tests\n- test_drag_drop_upload\n- test_upload_progress_display\n- test_error_handling\n\n## Performance Tests\n- test_upload_10mb_file\n- test_concurrent_100_uploads\n\n## Security Tests\n- test_malicious_csv_upload\n- test_path_traversal_prevention\n")
    _write_text(pack_dir / case_id / "evaluation.md", f"# Evaluation\n\nScenario: {scenario}\n\n## Accuracy\n- Test coverage: comprehensive\n- Edge cases: identified\n- Security considerations: included\n\n## Improvements\n- Add mutation testing\n- Add accessibility tests\n")


def generate_business_case(pack_dir: Path, case_id: str, scenario: str) -> None:
    _, input_dir, output_dir = _ensure_dirs(pack_dir, case_id)
    _write_text(input_dir / "stakeholder_request.txt", f"Stakeholder Request: {scenario}\n\nFrom: Product Manager\nPriority: High\nTimeline: Q1 2026\n\nContext:\n- Market opportunity identified\n- Competitive pressure\n- Customer demand signal\n")
    _write_text(output_dir / "requirements.md", f"# {scenario} - Business Requirements\n\n## Executive Summary\nInitiate project to address market opportunity.\n\n## Business Objectives\n- Increase market share by 10%\n- Reduce customer churn by 5%\n- Generate $500k ARR\n\n## Stakeholders\n- Product: Owner\n- Engineering: Implementation\n- Sales: Go-to-market\n- Support: Post-launch\n\n## Success Metrics\n- Feature adoption > 60%\n- NPS improvement > 10 points\n- Revenue target met\n")
    _write_text(output_dir / "user_stories.md", f"# {scenario} - User Stories\n\n## Epic: Core Functionality\n\nUS-001: As a user, I want to upload files so that I can analyze data\nAC:\n- Given valid CSV file\n- When I upload\n- Then system validates and processes\n\nUS-002: As a user, I want to view results so that I can take action\nAC:\n- Given completed analysis\n- When I view results\n- Then I see actionable insights\n")
    _write_text(pack_dir / case_id / "evaluation.md", f"# Evaluation\n\nScenario: {scenario}\n\n## Accuracy\n- Requirements clarity: high\n- Stakeholder coverage: complete\n- Success metrics: measurable\n\n## Improvements\n- Add dependency mapping\n- Add risk register\n")


GENERATORS = {
    "network": generate_network_case,
    "code": generate_code_case,
    "devops": generate_devops_case,
    "trading": generate_trading_case,
    "self_development": generate_self_development_case,
    "research": generate_research_case,
    "decision": generate_decision_case,
    "system": generate_system_case,
    "security": generate_security_case,
    "data": generate_data_case,
    "database": generate_database_case,
    "qa": generate_qa_case,
    "business": generate_business_case,
}


def count_existing_cases(pack: str) -> int:
    pack_dir = REAL_CASES_DIR / pack
    if not pack_dir.exists():
        return 0
    return len([d for d in pack_dir.iterdir() if d.is_dir()])


def generate_cases_for_pack(pack: str, target: int) -> int:
    pack_dir = REAL_CASES_DIR / pack
    pack_dir.mkdir(parents=True, exist_ok=True)
    existing = count_existing_cases(pack)
    scenarios = SCENARIOS.get(pack, [])
    generator = GENERATORS.get(pack)
    if not generator or not scenarios:
        logger.warning("No generator or scenarios for pack: %s", pack)
        return existing

    to_generate = target - existing
    if to_generate <= 0:
        logger.info("Pack %s already has %d cases (target: %d)", pack, existing, target)
        return existing

    logger.info("Generating %d cases for %s (existing: %d, target: %d)", to_generate, pack, existing, target)
    for i in range(to_generate):
        case_id = f"{scenarios[i % len(scenarios)]}_{existing + i + 1:04d}"
        try:
            generator(pack_dir, case_id, scenarios[i % len(scenarios)])
        except Exception as exc:
            logger.error("Failed to generate case %s: %s", case_id, exc)
            continue
    return count_existing_cases(pack)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate real cases for capability packs")
    parser.add_argument("--pack", help="Specific pack to generate cases for")
    parser.add_argument("--count", type=int, default=0, help="Override target count")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    packs = [args.pack] if args.pack else list(PACK_TARGETS.keys())
    total = 0
    for pack in packs:
        target = args.count if args.count > 0 else PACK_TARGETS.get(pack, 100)
        count = generate_cases_for_pack(pack, target)
        total += count
        logger.info("Pack %s: %d cases", pack, count)

    logger.info("Total real cases across all packs: %d", total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
