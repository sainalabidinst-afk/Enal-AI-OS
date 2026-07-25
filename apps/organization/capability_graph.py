"""
Capability Graph
================

Maps capabilities to required skills, dependencies, and subtasks.
Used by Task Planner to decompose user intent into executable subtasks,
and by Team Builder to select agents with the right skills.

This is the knowledge layer that makes team formation intelligent
instead of hardcoded.

Contract: Capability Contract v1
"""

import logging

from apps.organization.capability_contract import (
    CAPABILITY_CONTRACT_VERSION,
    CapabilityNode,
    SubtaskTemplate,
    validate_capability_node,
    validate_capability_pack,
)

logger = logging.getLogger(__name__)


class CapabilityGraph:
    """Graph of capabilities, skills, and subtasks."""

    def __init__(self):
        self._capabilities: dict[str, CapabilityNode] = {}
        self._subtask_templates: dict[str, list[SubtaskTemplate]] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        capabilities = {
            "network-design": CapabilityNode(
                capability_id="network-design",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Network Design",
                description="Design network topology, IP schema, routing",
                required_skills=["network-design", "topology", "ip-subnetting"],
                dependencies=[],
                estimated_complexity="high",
                tags=["network"],
            ),
            "config-analysis": CapabilityNode(
                capability_id="config-analysis",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Configuration Analysis",
                description="Parse and analyze router/switch/firewall configs",
                required_skills=["config-analysis", "parsing"],
                dependencies=["network-design"],
                estimated_complexity="medium",
                tags=["network"],
            ),
            "security-audit": CapabilityNode(
                capability_id="security-audit",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Security Audit",
                description="Audit configs for vulnerabilities and best practices",
                required_skills=["security-audit", "config-analysis"],
                dependencies=["config-analysis"],
                estimated_complexity="medium",
                tags=["network", "security"],
            ),
            "compliance-check": CapabilityNode(
                capability_id="compliance-check",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Compliance Check",
                description="Validate against standards (PCI, HIPAA, etc.)",
                required_skills=["compliance-check", "security-audit"],
                dependencies=["security-audit"],
                estimated_complexity="medium",
                tags=["network", "compliance"],
            ),
            "troubleshooting": CapabilityNode(
                capability_id="troubleshooting",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Network Troubleshooting",
                description="Diagnose connectivity, routing, and performance issues",
                required_skills=["troubleshooting", "config-analysis"],
                dependencies=["config-analysis"],
                estimated_complexity="high",
                tags=["network"],
            ),
            "code-generation": CapabilityNode(
                capability_id="code-generation",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Code Generation",
                description="Write source code from requirements",
                required_skills=["python", "javascript", "api-design"],
                dependencies=[],
                estimated_complexity="high",
                tags=["code"],
            ),
            "code-review": CapabilityNode(
                capability_id="code-review",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Code Review",
                description="Review code for quality, security, and correctness",
                required_skills=["code-review", "static-analysis"],
                dependencies=["code-generation"],
                estimated_complexity="medium",
                tags=["code"],
            ),
            "refactoring": CapabilityNode(
                capability_id="refactoring",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Refactoring",
                description="Improve code structure without changing behavior",
                required_skills=["refactoring", "code-review"],
                dependencies=["code-generation"],
                estimated_complexity="medium",
                tags=["code"],
            ),
            "testing": CapabilityNode(
                capability_id="testing",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Testing",
                description="Write and run unit, integration, and E2E tests",
                required_skills=["testing", "qa", "code-generation"],
                dependencies=["code-generation"],
                estimated_complexity="medium",
                tags=["code", "quality"],
            ),
            "documentation": CapabilityNode(
                capability_id="documentation",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Documentation",
                description="Write technical docs, API specs, runbooks",
                required_skills=["documentation", "writing"],
                dependencies=[],
                estimated_complexity="low",
                tags=["code", "research"],
            ),
            "literature-review": CapabilityNode(
                capability_id="literature-review",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Literature Review",
                description="Survey and synthesize existing research",
                required_skills=["research", "literature-review"],
                dependencies=[],
                estimated_complexity="high",
                tags=["research"],
            ),
            "data-analysis": CapabilityNode(
                capability_id="data-analysis",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Data Analysis",
                description="Analyze datasets, produce insights and visualizations",
                required_skills=["data-analysis", "statistics", "python"],
                dependencies=[],
                estimated_complexity="medium",
                tags=["research", "data"],
            ),
            "experiment-design": CapabilityNode(
                capability_id="experiment-design",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Experiment Design",
                description="Design experiments to validate hypotheses",
                required_skills=["experiment-design", "statistics"],
                dependencies=["literature-review"],
                estimated_complexity="high",
                tags=["research"],
            ),
            "report-writing": CapabilityNode(
                capability_id="report-writing",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Report Writing",
                description="Produce structured research reports with citations",
                required_skills=["writing", "documentation"],
                dependencies=["literature-review", "data-analysis"],
                estimated_complexity="medium",
                tags=["research"],
            ),
            "infrastructure-design": CapabilityNode(
                capability_id="infrastructure-design",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Infrastructure Design",
                description="Design cloud, Kubernetes, and network infra",
                required_skills=["infrastructure", "kubernetes", "terraform"],
                dependencies=[],
                estimated_complexity="high",
                tags=["devops"],
            ),
            "ci-cd": CapabilityNode(
                capability_id="ci-cd",
                version=CAPABILITY_CONTRACT_VERSION,
                name="CI/CD Pipeline",
                description="Build and automate CI/CD pipelines",
                required_skills=["ci-cd", "devops", "automation"],
                dependencies=["infrastructure-design"],
                estimated_complexity="medium",
                tags=["devops"],
            ),
            "monitoring": CapabilityNode(
                capability_id="monitoring",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Monitoring",
                description="Set up observability, alerts, and dashboards",
                required_skills=["monitoring", "observability", "infrastructure"],
                dependencies=["infrastructure-design"],
                estimated_complexity="medium",
                tags=["devops"],
            ),
            "deployment": CapabilityNode(
                capability_id="deployment",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Deployment",
                description="Deploy services to production environments",
                required_skills=["deployment", "kubernetes", "ci-cd"],
                dependencies=["ci-cd", "monitoring"],
                estimated_complexity="high",
                tags=["devops"],
            ),
            "automation": CapabilityNode(
                capability_id="automation",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Automation",
                description="Automate repetitive operational tasks",
                required_skills=["automation", "python", "ci-cd"],
                dependencies=[],
                estimated_complexity="medium",
                tags=["devops"],
            ),
            "market-analysis": CapabilityNode(
                capability_id="market-analysis",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Market Analysis",
                description="Analyze market data, trends, and indicators",
                required_skills=["market-analysis", "data-analysis", "finance"],
                dependencies=[],
                estimated_complexity="high",
                tags=["trading"],
            ),
            "risk-assessment": CapabilityNode(
                capability_id="risk-assessment",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Risk Assessment",
                description="Assess financial and market risks",
                required_skills=["risk-assessment", "statistics", "finance"],
                dependencies=["market-analysis"],
                estimated_complexity="high",
                tags=["trading"],
            ),
            "portfolio-optimization": CapabilityNode(
                capability_id="portfolio-optimization",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Portfolio Optimization",
                description="Optimize asset allocation and portfolio weights",
                required_skills=["portfolio-optimization", "risk-assessment", "statistics"],
                dependencies=["risk-assessment"],
                estimated_complexity="high",
                tags=["trading"],
            ),
            "strategy-backtesting": CapabilityNode(
                capability_id="strategy-backtesting",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Strategy Backtesting",
                description="Backtest trading strategies against historical data",
                required_skills=["backtesting", "python", "market-analysis"],
                dependencies=["market-analysis"],
                estimated_complexity="high",
                tags=["trading"],
            ),
            "vulnerability-scan": CapabilityNode(
                capability_id="vulnerability-scan",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Vulnerability Scanning",
                description="Scan systems and code for vulnerabilities",
                required_skills=["vulnerability-scan", "security-audit"],
                dependencies=[],
                estimated_complexity="medium",
                tags=["security"],
            ),
            "penetration-test": CapabilityNode(
                capability_id="penetration-test",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Penetration Testing",
                description="Simulate attacks to find security weaknesses",
                required_skills=["penetration-test", "vulnerability-scan"],
                dependencies=["vulnerability-scan"],
                estimated_complexity="high",
                tags=["security"],
            ),
            "compliance-audit": CapabilityNode(
                capability_id="compliance-audit",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Compliance Audit",
                description="Audit systems against security/compliance standards",
                required_skills=["compliance-audit", "security-audit"],
                dependencies=["security-audit"],
                estimated_complexity="medium",
                tags=["security", "compliance"],
            ),
            "incident-response": CapabilityNode(
                capability_id="incident-response",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Incident Response",
                description="Respond to and remediate security incidents",
                required_skills=["incident-response", "troubleshooting"],
                dependencies=["vulnerability-scan"],
                estimated_complexity="high",
                tags=["security"],
            ),
            "architecture-analysis": CapabilityNode(
                capability_id="architecture-analysis",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Architecture Analysis",
                description="Analyze project architecture and identify improvements",
                required_skills=["architecture", "analysis", "system-design"],
                dependencies=[],
                estimated_complexity="high",
                tags=["self-development"],
            ),
            "approval-management": CapabilityNode(
                capability_id="approval-management",
                version=CAPABILITY_CONTRACT_VERSION,
                name="Approval Management",
                description="Present changes and manage user approval workflow",
                required_skills=["communication", "documentation"],
                dependencies=[],
                estimated_complexity="low",
                tags=["self-development"],
            ),
        }
        for node in capabilities.values():
            validate_capability_node(node)
        self._capabilities = capabilities

        subtask_templates = {
            "code": [
                SubtaskTemplate(
                    subtask_id="code-req-analysis",
                    name="Requirement Analysis",
                    description="Analyze and document requirements",
                    required_skills=["requirements", "communication"],
                    produces_artifact="requirements_doc",
                    estimated_duration_minutes=30,
                    priority=1,
                    can_parallelize=False,
                ),
                SubtaskTemplate(
                    subtask_id="code-architecture",
                    name="Architecture Design",
                    description="Design system architecture and interfaces",
                    required_skills=["architecture", "system-design"],
                    produces_artifact="architecture_doc",
                    estimated_duration_minutes=60,
                    priority=2,
                    can_parallelize=False,
                ),
                SubtaskTemplate(
                    subtask_id="code-backend",
                    name="Backend Development",
                    description="Implement backend services and APIs",
                    required_skills=["python", "api", "database"],
                    produces_artifact="backend_code",
                    estimated_duration_minutes=120,
                    priority=3,
                    can_parallelize=False,
                ),
                SubtaskTemplate(
                    subtask_id="code-frontend",
                    name="Frontend Development",
                    description="Implement user interface",
                    required_skills=["javascript", "react", "ui"],
                    produces_artifact="frontend_code",
                    estimated_duration_minutes=120,
                    priority=3,
                    can_parallelize=True,
                ),
                SubtaskTemplate(
                    subtask_id="code-database",
                    name="Database Design",
                    description="Design schema and migrations",
                    required_skills=["sql", "database", "architecture"],
                    produces_artifact="database_schema",
                    estimated_duration_minutes=60,
                    priority=2,
                    can_parallelize=True,
                ),
                SubtaskTemplate(
                    subtask_id="code-testing",
                    name="Testing",
                    description="Write and run tests",
                    required_skills=["testing", "qa"],
                    produces_artifact="test_suite",
                    estimated_duration_minutes=90,
                    priority=4,
                    can_parallelize=False,
                ),
                SubtaskTemplate(
                    subtask_id="code-docs",
                    name="Documentation",
                    description="Write API docs and runbooks",
                    required_skills=["documentation", "writing"],
                    produces_artifact="docs",
                    estimated_duration_minutes=45,
                    priority=5,
                    can_parallelize=True,
                ),
            ],
            "network": [
                SubtaskTemplate(
                    subtask_id="net-topology",
                    name="Topology Analysis",
                    description="Analyze network topology and IP schema",
                    required_skills=["network-design", "topology", "parsing"],
                    produces_artifact="topology_diagram",
                    estimated_duration_minutes=60,
                    priority=1,
                    can_parallelize=False,
                ),
                SubtaskTemplate(
                    subtask_id="net-config-review",
                    name="Configuration Review",
                    description="Review device configurations for issues",
                    required_skills=["config-analysis", "security-audit"],
                    produces_artifact="config_review",
                    estimated_duration_minutes=90,
                    priority=2,
                    can_parallelize=True,
                ),
                SubtaskTemplate(
                    subtask_id="net-security-audit",
                    name="Security Audit",
                    description="Audit network security posture",
                    required_skills=["security-audit", "compliance-check"],
                    produces_artifact="security_report",
                    estimated_duration_minutes=120,
                    priority=2,
                    can_parallelize=True,
                ),
                SubtaskTemplate(
                    subtask_id="net-compliance",
                    name="Compliance Check",
                    description="Validate against compliance standards",
                    required_skills=["compliance-check", "security-audit"],
                    produces_artifact="compliance_report",
                    estimated_duration_minutes=60,
                    priority=3,
                    can_parallelize=False,
                ),
                SubtaskTemplate(
                    subtask_id="net-troubleshoot",
                    name="Troubleshooting",
                    description="Diagnose network issues and propose fixes",
                    required_skills=["troubleshooting", "config-analysis"],
                    produces_artifact="troubleshooting_report",
                    estimated_duration_minutes=90,
                    priority=2,
                    can_parallelize=False,
                ),
                SubtaskTemplate(
                    subtask_id="net-docs",
                    name="Documentation",
                    description="Generate network documentation",
                    required_skills=["documentation", "writing"],
                    produces_artifact="network_docs",
                    estimated_duration_minutes=45,
                    priority=5,
                    can_parallelize=True,
                ),
            ],
            "research": [
                SubtaskTemplate(
                    subtask_id="res-literature",
                    name="Literature Review",
                    description="Survey existing research and papers",
                    required_skills=["research", "literature-review"],
                    produces_artifact="literature_review",
                    estimated_duration_minutes=120,
                    priority=1,
                    can_parallelize=False,
                ),
                SubtaskTemplate(
                    subtask_id="res-data-analysis",
                    name="Data Analysis",
                    description="Analyze collected data",
                    required_skills=["data-analysis", "statistics", "python"],
                    produces_artifact="analysis_results",
                    estimated_duration_minutes=90,
                    priority=2,
                    can_parallelize=True,
                ),
                SubtaskTemplate(
                    subtask_id="res-experiment",
                    name="Experiment Design",
                    description="Design and run experiments",
                    required_skills=["experiment-design", "statistics"],
                    produces_artifact="experiment_plan",
                    estimated_duration_minutes=60,
                    priority=2,
                    can_parallelize=True,
                ),
                SubtaskTemplate(
                    subtask_id="res-report",
                    name="Report Writing",
                    description="Write research report with findings",
                    required_skills=["writing", "documentation"],
                    produces_artifact="research_report",
                    estimated_duration_minutes=90,
                    priority=4,
                    can_parallelize=False,
                ),
            ],
            "devops": [
                SubtaskTemplate(
                    subtask_id="devops-infra",
                    name="Infrastructure Design",
                    description="Design cloud and container infrastructure",
                    required_skills=["infrastructure", "kubernetes", "terraform"],
                    produces_artifact="infra_design",
                    estimated_duration_minutes=90,
                    priority=1,
                    can_parallelize=False,
                ),
                SubtaskTemplate(
                    subtask_id="devops-cicd",
                    name="CI/CD Pipeline",
                    description="Build CI/CD pipelines",
                    required_skills=["ci-cd", "devops", "automation"],
                    produces_artifact="ci_cd_config",
                    estimated_duration_minutes=90,
                    priority=2,
                    can_parallelize=True,
                ),
                SubtaskTemplate(
                    subtask_id="devops-monitoring",
                    name="Monitoring Setup",
                    description="Set up monitoring, alerts, and dashboards",
                    required_skills=["monitoring", "observability", "infrastructure"],
                    produces_artifact="monitoring_config",
                    estimated_duration_minutes=60,
                    priority=3,
                    can_parallelize=True,
                ),
                SubtaskTemplate(
                    subtask_id="devops-deploy",
                    name="Deployment",
                    description="Deploy services to production",
                    required_skills=["deployment", "kubernetes", "ci-cd"],
                    produces_artifact="deployment_manifest",
                    estimated_duration_minutes=60,
                    priority=4,
                    can_parallelize=False,
                ),
            ],
            "trading": [
                SubtaskTemplate(
                    subtask_id="trading-market-analysis",
                    name="Market Analysis",
                    description="Analyze market data and trends",
                    required_skills=["market-analysis", "data-analysis", "finance"],
                    produces_artifact="market_report",
                    estimated_duration_minutes=90,
                    priority=1,
                    can_parallelize=False,
                ),
                SubtaskTemplate(
                    subtask_id="trading-risk",
                    name="Risk Assessment",
                    description="Assess portfolio and strategy risks",
                    required_skills=["risk-assessment", "statistics", "finance"],
                    produces_artifact="risk_report",
                    estimated_duration_minutes=60,
                    priority=2,
                    can_parallelize=True,
                ),
                SubtaskTemplate(
                    subtask_id="trading-portfolio",
                    name="Portfolio Optimization",
                    description="Optimize asset allocation",
                    required_skills=["portfolio-optimization", "risk-assessment", "statistics"],
                    produces_artifact="portfolio_plan",
                    estimated_duration_minutes=90,
                    priority=3,
                    can_parallelize=False,
                ),
                SubtaskTemplate(
                    subtask_id="trading-backtest",
                    name="Strategy Backtesting",
                    description="Backtest strategy against historical data",
                    required_skills=["backtesting", "python", "market-analysis"],
                    produces_artifact="backtest_results",
                    estimated_duration_minutes=90,
                    priority=3,
                    can_parallelize=True,
                ),
            ],
            "security": [
                SubtaskTemplate(
                    subtask_id="sec-vuln-scan",
                    name="Vulnerability Scan",
                    description="Scan for vulnerabilities",
                    required_skills=["vulnerability-scan", "security-audit"],
                    produces_artifact="vulnerability_report",
                    estimated_duration_minutes=60,
                    priority=1,
                    can_parallelize=False,
                ),
                SubtaskTemplate(
                    subtask_id="sec-pentest",
                    name="Penetration Test",
                    description="Simulate attacks to find weaknesses",
                    required_skills=["penetration-test", "vulnerability-scan"],
                    produces_artifact="penetration_report",
                    estimated_duration_minutes=120,
                    priority=2,
                    can_parallelize=True,
                ),
                SubtaskTemplate(
                    subtask_id="sec-compliance",
                    name="Compliance Audit",
                    description="Audit compliance posture",
                    required_skills=["compliance-audit", "security-audit"],
                    produces_artifact="compliance_report",
                    estimated_duration_minutes=90,
                    priority=3,
                    can_parallelize=True,
                ),
                SubtaskTemplate(
                    subtask_id="sec-incident",
                    name="Incident Response",
                    description="Respond to security incidents",
                    required_skills=["incident-response", "troubleshooting"],
                    produces_artifact="incident_report",
                    estimated_duration_minutes=90,
                    priority=4,
                    can_parallelize=False,
                ),
            ],
            "self-development": [
                SubtaskTemplate(
                    subtask_id="sd-analyze",
                    name="Analyze Project",
                    description="Analyze project structure and complexity",
                    required_skills=["architecture", "analysis"],
                    produces_artifact="project_analysis",
                    estimated_duration_minutes=60,
                    priority=1,
                    can_parallelize=False,
                ),
                SubtaskTemplate(
                    subtask_id="sd-identify",
                    name="Identify Problems",
                    description="Identify bottlenecks, dead code, and improvements",
                    required_skills=["code-review", "static-analysis"],
                    produces_artifact="problems_report",
                    estimated_duration_minutes=90,
                    priority=2,
                    can_parallelize=False,
                ),
                SubtaskTemplate(
                    subtask_id="sd-propose",
                    name="Propose Solution",
                    description="Generate improvement proposal",
                    required_skills=["architecture", "system-design"],
                    produces_artifact="improvement_proposal",
                    estimated_duration_minutes=45,
                    priority=3,
                    can_parallelize=True,
                ),
                SubtaskTemplate(
                    subtask_id="sd-patch",
                    name="Generate Patch",
                    description="Generate code patch for approved proposal",
                    required_skills=["coding", "refactoring"],
                    produces_artifact="patch",
                    estimated_duration_minutes=60,
                    priority=4,
                    can_parallelize=False,
                ),
                SubtaskTemplate(
                    subtask_id="sd-test",
                    name="Run Tests",
                    description="Run tests to validate patch",
                    required_skills=["testing", "qa"],
                    produces_artifact="test_report",
                    estimated_duration_minutes=90,
                    priority=5,
                    can_parallelize=False,
                ),
                SubtaskTemplate(
                    subtask_id="sd-approval",
                    name="Await Approval",
                    description="Present changes and wait for user approval",
                    required_skills=["communication", "documentation"],
                    produces_artifact="approval_status",
                    estimated_duration_minutes=5,
                    priority=6,
                    can_parallelize=False,
                ),
            ],
        }
        for node in capabilities.values():
            validate_capability_node(node)
        self._capabilities = capabilities

        for templates in subtask_templates.values():
            validate_capability_pack("contract-validation", templates)
        self._subtask_templates = subtask_templates

    def get_capability_node(self, capability_id: str) -> CapabilityNode | None:
        return self._capabilities.get(capability_id)

    def get_required_skills(self, capability_id: str) -> list[str]:
        node = self._capabilities.get(capability_id)
        return list(node.required_skills) if node else []

    def get_dependencies(self, capability_id: str) -> list[str]:
        node = self._capabilities.get(capability_id)
        return list(node.dependencies) if node else []

    def get_subtask_templates(self, domain: str) -> list[SubtaskTemplate]:
        return list(self._subtask_templates.get(domain, []))

    def get_all_capabilities(self) -> list[str]:
        return list(self._capabilities.keys())

    def get_related_capabilities(self, capability_id: str) -> list[str]:
        related: list[str] = []
        node = self._capabilities.get(capability_id)
        if not node:
            return related
        for skill in node.required_skills:
            for cap_id, cap_node in self._capabilities.items():
                if cap_id != capability_id and skill in cap_node.required_skills:
                    related.append(cap_id)
        return list(set(related))

    def suggest_capabilities(self, skills: list[str]) -> list[str]:
        scored = []
        for cap_id, node in self._capabilities.items():
            match = len(set(skills) & set(node.required_skills))
            if match > 0:
                scored.append((match, cap_id))
        scored.sort(reverse=True)
        return [cap_id for _, cap_id in scored]


capability_graph = CapabilityGraph()
