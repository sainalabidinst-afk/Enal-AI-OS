"""
DevOps Assistant Benchmark
===========================

Benchmark scenarios for validating DevOps Assistant capability pack.
Target: A+ (≥90%) with 10 scenarios across 6 dimensions.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.devops_assistant.schemas import Problem, ProblemType

logger = logging.getLogger(__name__)

SCENARIOS: list[dict[str, Any]] = [
    {
        "id": "devops-001",
        "name": "CI/CD Pipeline untuk Microservice",
        "category": "ci-cd",
        "artifact": {
            "path": ".github/workflows/ci.yml",
            "content": "name: CI\non: [push, pull_request]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n      - run: pip install -e .[dev]\n      - run: pytest tests/\n      - run: docker build -t app .\n",
        },
        "min_problems": 1,
        "min_solutions": 1,
    },
    {
        "id": "devops-002",
        "name": "Kubernetes Deployment dengan Health Check",
        "category": "infrastructure",
        "artifact": {
            "path": "k8s/deployment.yaml",
            "content": "apiVersion: apps/v1\nkind: Deployment\nspec:\n  replicas: 3\n  template:\n    spec:\n      containers:\n      - name: app\n        image: app:latest\n        ports:\n        - containerPort: 8080\n        resources:\n          requests:\n            cpu: 500m\n            memory: 256Mi\n          limits:\n            cpu: 1000m\n            memory: 512Mi\n",
        },
        "min_problems": 1,
        "min_solutions": 1,
    },
    {
        "id": "devops-003",
        "name": "Terraform AWS Infrastructure",
        "category": "infrastructure",
        "artifact": {
            "path": "terraform/main.tf",
            "content": 'provider "aws" {\n  region = "us-east-1"\n}\nresource "aws_instance" "app" {\n  ami           = "ami-0c55b159cbfafe1f0"\n  instance_type = "t3.micro"\n  tags = {\n    Name = "app-server"\n  }\n}\n',
        },
        "min_problems": 1,
        "min_solutions": 1,
    },
    {
        "id": "devops-004",
        "name": "GitLab CI Pipeline",
        "category": "ci-cd",
        "artifact": {
            "path": ".gitlab-ci.yml",
            "content": "stages:\n  - test\n  - build\n  - deploy\ntest:\n  stage: test\n  script:\n    - pytest tests/\nbuild:\n  stage: build\n  script:\n    - docker build -t app .\n",
        },
        "min_problems": 1,
        "min_solutions": 1,
    },
    {
        "id": "devops-005",
        "name": "Monitoring Stack Configuration",
        "category": "monitoring",
        "artifact": {
            "path": "monitoring/prometheus.yml",
            "content": "global:\n  scrape_interval: 15s\nscrape_configs:\n  - job_name: 'app'\n    static_configs:\n      - targets: ['localhost:8080']\n",
        },
        "min_problems": 1,
        "min_solutions": 1,
    },
    {
        "id": "devops-006",
        "name": "Helm Chart dengan Security Issues",
        "category": "security",
        "artifact": {
            "path": "helm/values.yaml",
            "content": "image:\n  repository: app\n  tag: latest\ncontainer:\n  securityContext:\n    privileged: true\n    runAsUser: 0\n",
        },
        "min_problems": 2,
        "min_solutions": 2,
    },
    {
        "id": "devops-007",
        "name": "Multi-Environment Deployment Strategy",
        "category": "deployment",
        "artifact": {
            "path": "deploy/staging.yaml",
            "content": "apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: app-staging\nspec:\n  replicas: 2\n  strategy:\n    type: RollingUpdate\n    rollingUpdate:\n      maxSurge: 1\n      maxUnavailable: 0\n",
        },
        "min_problems": 1,
        "min_solutions": 1,
    },
    {
        "id": "devops-008",
        "name": "GitOps dengan ArgoCD",
        "category": "gitops",
        "artifact": {
            "path": "argocd/application.yaml",
            "content": "apiVersion: argoproj.io/v1alpha1\nkind: Application\nmetadata:\n  name: app\nspec:\n  project: default\n  source:\n    repoURL: https://github.com/org/app.git\n    targetRevision: main\n    path: k8s\n  destination:\n    server: https://kubernetes.default.svc\n    namespace: default\n  syncPolicy:\n    automated:\n      prune: true\n",
        },
        "min_problems": 1,
        "min_solutions": 1,
    },
    {
        "id": "devops-009",
        "name": "Policy-as-Code dengan OPA",
        "category": "policy",
        "artifact": {
            "path": "policy/opa.rego",
            "content": 'package kubernetes.admission\nviolation[{"msg": msg}] {\n  input.request.kind.kind == "Pod"\n  container := input.request.object.spec.containers[_]\n  container.securityContext.privileged == true\n  msg := sprintf("Container %v is privileged", [container.name])\n}\n',
        },
        "min_problems": 0,
        "min_solutions": 0,
    },
    {
        "id": "devops-010",
        "name": "Chaos Engineering Configuration",
        "category": "chaos",
        "artifact": {
            "path": "chaos/experiment.yaml",
            "content": "apiVersion: chaos-mesh.org/v1alpha1\nkind: NetworkChaos\nmetadata:\n  name: network-delay\nspec:\n  action: delay\n  mode: one\n  selector:\n    namespaces:\n      - default\n  delay:\n    latency: 10ms\n  duration: 30s\n",
        },
        "min_problems": 1,
        "min_solutions": 1,
    },
]


class DevOpsBenchmark:
    """Benchmark for DevOps Assistant capability pack."""

    def __init__(self) -> None:
        self.scenarios = SCENARIOS
        self.results: list[dict[str, Any]] = []

    def run(self) -> dict[str, Any]:
        from apps.devops_assistant.suggestion_generator import DevOpsSuggestionGenerator

        generator = DevOpsSuggestionGenerator()
        passed = 0
        total = len(self.scenarios)

        for scenario in self.scenarios:
            result = generator.analyze(scenario["artifact"])
            problems_count = len(result["problems"])
            solutions_count = len(result["suggestions"])

            min_problems = scenario.get("min_problems", 0)
            min_solutions = scenario.get("min_solutions", 0)

            problems_met = problems_count >= min_problems
            solutions_met = solutions_count >= min_solutions

            scenario_passed = problems_met and solutions_met
            if scenario_passed:
                passed += 1

            self.results.append({
                "scenario_id": scenario["id"],
                "name": scenario["name"],
                "category": scenario["category"],
                "passed": scenario_passed,
                "problems_detected": problems_count,
                "solutions_proposed": solutions_count,
                "min_problems_required": min_problems,
                "min_solutions_required": min_solutions,
            })

        overall_percentage = (passed / total) * 100 if total > 0 else 0.0
        grade = self._calculate_grade(overall_percentage)

        return {
            "total_scenarios": total,
            "passed": passed,
            "failed": total - passed,
            "overall_percentage": overall_percentage,
            "grade": grade,
            "target_grade": "A+",
            "target_percentage": 90,
            "passed_target": overall_percentage >= 90,
            "results": self.results,
        }

    def _calculate_grade(self, percentage: float) -> str:
        if percentage >= 95:
            return "A+"
        if percentage >= 90:
            return "A"
        if percentage >= 80:
            return "B+"
        if percentage >= 70:
            return "B"
        return "C"
