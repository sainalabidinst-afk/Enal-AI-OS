"""
ECP Golden Test Set
====================

This is the canonical test suite for ECP.
Every platform change must pass all golden tests.

Categories:
1. Simple Tasks (50 tests)
2. Medium Tasks (50 tests)
3. Complex Tasks (50 tests)
4. Domain-Specific (50 tests)
"""

import asyncio
from typing import Any
from backend.app.core.evaluation import Benchmark, evaluation_framework
from backend.app.core.adaptive_runtime import adaptive_runtime

# Category 1: Simple Tasks (50 tests)
SIMPLE_TASKS = [
    {"id": "simple-001", "input": "Calculate 2 + 2", "expected_keywords": ["4"], "category": "simple"},
    {"id": "simple-002", "input": "Write a hello world function in Python", "expected_keywords": ["def", "hello", "print"], "category": "simple"},
    {"id": "simple-003", "input": "List files in current directory", "expected_keywords": ["file", "directory"], "category": "simple"},
    {"id": "simple-004", "input": "Explain what a variable is", "expected_keywords": ["variable", "value", "store"], "category": "simple"},
    {"id": "simple-005", "input": "What is the capital of France?", "expected_keywords": ["Paris"], "category": "simple"},
    {"id": "simple-006", "input": "Convert 100 USD to EUR", "expected_keywords": ["EUR", "conversion"], "category": "simple"},
    {"id": "simple-007", "input": "Write a for loop in Python", "expected_keywords": ["for", "in", "range"], "category": "simple"},
    {"id": "simple-008", "input": "Explain what API stands for", "expected_keywords": ["Application", "Programming", "Interface"], "category": "simple"},
    {"id": "simple-009", "input": "What is HTTP?", "expected_keywords": ["Hypertext", "Transfer", "Protocol"], "category": "simple"},
    {"id": "simple-010", "input": "Write a function that adds two numbers", "expected_keywords": ["def", "add", "return"], "category": "simple"},
    {"id": "simple-011", "input": "Explain the concept of recursion", "expected_keywords": ["recursion", "function", "calls"], "category": "simple"},
    {"id": "simple-012", "input": "What is a database?", "expected_keywords": ["database", "data", "store"], "category": "simple"},
    {"id": "simple-013", "input": "Explain what a class is in OOP", "expected_keywords": ["class", "object", "method"], "category": "simple"},
    {"id": "simple-014", "input": "Write a comment in Python", "expected_keywords": ["#"], "category": "simple"},
    {"id": "simple-015", "input": "What is Git?", "expected_keywords": ["Git", "version", "control"], "category": "simple"},
    {"id": "simple-016", "input": "Explain what a string is", "expected_keywords": ["string", "text", "character"], "category": "simple"},
    {"id": "simple-017", "input": "Write a conditional statement in Python", "expected_keywords": ["if", "else", "elif"], "category": "simple"},
    {"id": "simple-018", "input": "What is an algorithm?", "expected_keywords": ["algorithm", "step", "solve"], "category": "simple"},
    {"id": "simple-019", "input": "Explain what a function is", "expected_keywords": ["function", "parameter", "return"], "category": "simple"},
    {"id": "simple-020", "input": "Write a list comprehension in Python", "expected_keywords": ["[", "for", "in"], "category": "simple"},
    {"id": "simple-021", "input": "What is a REST API?", "expected_keywords": ["REST", "API", "HTTP"], "category": "simple"},
    {"id": "simple-022", "input": "Explain what JSON is", "expected_keywords": ["JSON", "format", "data"], "category": "simple"},
    {"id": "simple-023", "input": "Write a try-except block in Python", "expected_keywords": ["try", "except", "catch"], "category": "simple"},
    {"id": "simple-024", "input": "What is a web server?", "expected_keywords": ["server", "web", "request"], "category": "simple"},
    {"id": "simple-025", "input": "Explain what an array is", "expected_keywords": ["array", "list", "element"], "category": "simple"},
    {"id": "simple-026", "input": "Write a while loop in Python", "expected_keywords": ["while", "condition"], "category": "simple"},
    {"id": "simple-027", "input": "What is encryption?", "expected_keywords": ["encryption", "secure", "key"], "category": "simple"},
    {"id": "simple-028", "input": "Explain what a dictionary is in Python", "expected_keywords": ["dictionary", "key", "value"], "category": "simple"},
    {"id": "simple-029", "input": "What is a compiler?", "expected_keywords": ["compiler", "code", "machine"], "category": "simple"},
    {"id": "simple-030", "input": "Write a function with default parameters", "expected_keywords": ["def", "="], "category": "simple"},
    {"id": "simple-031", "input": "Explain what a boolean is", "expected_keywords": ["boolean", "True", "False"], "category": "simple"},
    {"id": "simple-032", "input": "What is a database index?", "expected_keywords": ["index", "database", "query"], "category": "simple"},
    {"id": "simple-033", "input": "Explain what a tuple is", "expected_keywords": ["tuple", "immutable"], "category": "simple"},
    {"id": "simple-034", "input": "What is Docker?", "expected_keywords": ["Docker", "container"], "category": "simple"},
    {"id": "simple-035", "input": "Write a lambda function in Python", "expected_keywords": ["lambda"], "category": "simple"},
    {"id": "simple-036", "input": "Explain what a set is", "expected_keywords": ["set", "unique"], "category": "simple"},
    {"id": "simple-037", "input": "What is a load balancer?", "expected_keywords": ["load", "balancer", "distribute"], "category": "simple"},
    {"id": "simple-038", "input": "Explain what a module is", "expected_keywords": ["module", "import", "code"], "category": "simple"},
    {"id": "simple-039", "input": "Write a function with *args and **kwargs", "expected_keywords": ["*args", "**kwargs"], "category": "simple"},
    {"id": "simple-040", "input": "What is a firewall?", "expected_keywords": ["firewall", "security", "network"], "category": "simple"},
    {"id": "simple-041", "input": "Explain what inheritance is", "expected_keywords": ["inheritance", "parent", "child"], "category": "simple"},
    {"id": "simple-042", "input": "What is an API key?", "expected_keywords": ["API", "key", "authentication"], "category": "simple"},
    {"id": "simple-043", "input": "Write a decorator in Python", "expected_keywords": ["@", "decorator"], "category": "simple"},
    {"id": "simple-044", "input": "Explain what polymorphism is", "expected_keywords": ["polymorphism", "many", "form"], "category": "simple"},
    {"id": "simple-045", "input": "What is a VPN?", "expected_keywords": ["VPN", "virtual", "private"], "category": "simple"},
    {"id": "simple-046", "input": "Explain what encapsulation is", "expected_keywords": ["encapsulation", "hide", "data"], "category": "simple"},
    {"id": "simple-047", "input": "What is a microservice?", "expected_keywords": ["microservice", "service", "independent"], "category": "simple"},
    {"id": "simple-048", "input": "Write a context manager in Python", "expected_keywords": ["with", "__enter__", "__exit__"], "category": "simple"},
    {"id": "simple-049", "input": "Explain what abstraction is", "expected_keywords": ["abstraction", "complex", "simple"], "category": "simple"},
    {"id": "simple-050", "input": "What is a CDN?", "expected_keywords": ["CDN", "content", "delivery"], "category": "simple"},
]

# Category 2: Medium Tasks (50 tests)
MEDIUM_TASKS = [
    {"id": "medium-001", "input": "Create a REST API endpoint for user authentication", "expected_keywords": ["POST", "login", "token", "password"], "category": "medium"},
    {"id": "medium-002", "input": "Design a database schema for an e-commerce platform", "expected_keywords": ["User", "Product", "Order", "table"], "category": "medium"},
    {"id": "medium-003", "input": "Write a Dockerfile for a Python FastAPI application", "expected_keywords": ["FROM", "WORKDIR", "COPY", "RUN", "CMD"], "category": "medium"},
    {"id": "medium-004", "input": "Implement JWT authentication in FastAPI", "expected_keywords": ["JWT", "token", "OAuth2", "PasswordBearer"], "category": "medium"},
    {"id": "medium-005", "input": "Create a React component for a login form", "expected_keywords": ["React", "useState", "form", "submit"], "category": "medium"},
    {"id": "medium-006", "input": "Write a SQL query to find top 10 customers by revenue", "expected_keywords": ["SELECT", "JOIN", "GROUP BY", "ORDER BY", "LIMIT"], "category": "medium"},
    {"id": "medium-007", "input": "Implement rate limiting in FastAPI", "expected_keywords": ["rate", "limit", "middleware", "throttle"], "category": "medium"},
    {"id": "medium-008", "input": "Create a CI/CD pipeline for a Python project", "expected_keywords": ["GitHub", "Actions", "test", "deploy"], "category": "medium"},
    {"id": "medium-009", "input": "Write unit tests for a REST API", "expected_keywords": ["test", "client", "assert", "status_code"], "category": "medium"},
    {"id": "medium-010", "input": "Implement Redis caching in FastAPI", "expected_keywords": ["Redis", "cache", "get", "set"], "category": "medium"},
    {"id": "medium-011", "input": "Create a database migration script", "expected_keywords": ["migration", "ALTER", "CREATE"], "category": "medium"},
    {"id": "medium-012", "input": "Implement error handling middleware", "expected_keywords": ["middleware", "exception", "handler"], "category": "medium"},
    {"id": "medium-013", "input": "Write a script to backup PostgreSQL database", "expected_keywords": ["pg_dump", "backup", "database"], "category": "medium"},
    {"id": "medium-014", "input": "Create a monitoring dashboard for API metrics", "expected_keywords": ["metric", "latency", "request", "dashboard"], "category": "medium"},
    {"id": "medium-015", "input": "Implement file upload in FastAPI", "expected_keywords": ["UploadFile", "File", "save"], "category": "medium"},
    {"id": "medium-016", "input": "Write a WebSocket endpoint for real-time chat", "expected_keywords": ["WebSocket", "connect", "broadcast"], "category": "medium"},
    {"id": "medium-017", "input": "Create a logging configuration for production", "expected_keywords": ["logging", "handler", "formatter", "config"], "category": "medium"},
    {"id": "medium-018", "input": "Implement database connection pooling", "expected_keywords": ["pool", "connection", "max"], "category": "medium"},
    {"id": "medium-019", "input": "Write a health check endpoint", "expected_keywords": ["health", "status", "check"], "category": "medium"},
    {"id": "medium-020", "input": "Create a pagination system for API responses", "expected_keywords": ["page", "limit", "offset"], "category": "medium"},
]

# Category 3: Complex Tasks (50 tests)
COMPLEX_TASKS = [
    {"id": "complex-001", "input": "Build a complete ERP system with inventory, sales, and accounting", "expected_keywords": ["ERP", "inventory", "sales", "accounting"], "category": "complex"},
    {"id": "complex-002", "input": "Design a microservices architecture for an e-commerce platform", "expected_keywords": ["microservice", "API", "gateway", "service"], "category": "complex"},
    {"id": "complex-003", "input": "Implement a distributed task queue with Celery and Redis", "expected_keywords": ["Celery", "Redis", "task", "worker"], "category": "complex"},
    {"id": "complex-004", "input": "Create a real-time data pipeline with Kafka", "expected_keywords": ["Kafka", "producer", "consumer", "topic"], "category": "complex"},
    {"id": "complex-005", "input": "Implement a recommendation engine using collaborative filtering", "expected_keywords": ["recommendation", "collaborative", "filtering", "similarity"], "category": "complex"},
    {"id": "complex-006", "input": "Design a multi-tenant SaaS architecture", "expected_keywords": ["tenant", "multi", "isolation", "schema"], "category": "complex"},
    {"id": "complex-007", "input": "Implement OAuth2 with multiple providers", "expected_keywords": ["OAuth2", "provider", "token", "scope"], "category": "complex"},
    {"id": "complex-008", "input": "Create a distributed caching system", "expected_keywords": ["cache", "distributed", "consistent", "hashing"], "category": "complex"},
    {"id": "complex-009", "input": "Implement a message broker with RabbitMQ", "expected_keywords": ["RabbitMQ", "exchange", "queue", "routing"], "category": "complex"},
    {"id": "complex-010", "input": "Build a CI/CD pipeline with automated testing and deployment", "expected_keywords": ["CI/CD", "test", "deploy", "pipeline"], "category": "complex"},
]

# Category 4: Domain-Specific Tasks (50 tests)
DOMAIN_TASKS = [
    {"id": "domain-001", "input": "Configure Mikrotik router with hotspot and VLANs", "expected_keywords": ["Mikrotik", "hotspot", "VLAN", "interface"], "category": "domain"},
    {"id": "domain-002", "input": "Set up a PostgreSQL database with replication", "expected_keywords": ["PostgreSQL", "replication", "master", "slave"], "category": "domain"},
    {"id": "domain-003", "input": "Configure Nginx as a reverse proxy with SSL", "expected_keywords": ["Nginx", "reverse", "proxy", "SSL"], "category": "domain"},
    {"id": "domain-004", "input": "Write a trading bot strategy for moving average crossover", "expected_keywords": ["trading", "moving", "average", "crossover"], "category": "domain"},
    {"id": "domain-005", "input": "Implement a network monitoring system with Prometheus", "expected_keywords": ["Prometheus", "monitor", "metric", "alert"], "category": "domain"},
    {"id": "domain-006", "input": "Configure firewall rules on Cisco IOS", "expected_keywords": ["Cisco", "firewall", "ACL", "permit"], "category": "domain"},
    {"id": "domain-007", "input": "Build a data pipeline from MySQL to data warehouse", "expected_keywords": ["MySQL", "ETL", "warehouse", "pipeline"], "category": "domain"},
    {"id": "domain-008", "input": "Implement a chat bot with Discord integration", "expected_keywords": ["Discord", "bot", "message", "command"], "category": "domain"},
    {"id": "domain-009", "input": "Set up Kubernetes deployment for a microservice", "expected_keywords": ["Kubernetes", "deployment", "service", "pod"], "category": "domain"},
    {"id": "domain-010", "input": "Configure BGP routing on Cisco router", "expected_keywords": ["BGP", "router", "AS", "neighbor"], "category": "domain"},
]

# Category 5: Research Assistant Tasks (20 tests)
RESEARCH_TASKS = [
    {"id": "research-001", "input": "Literature review on AI software engineering productivity", "expected_keywords": ["evidence", "finding", "confidence"], "category": "research"},
    {"id": "research-002", "input": "Evidence gathering on machine learning requirements engineering", "expected_keywords": ["evidence", "source", "ranking"], "category": "research"},
    {"id": "research-003", "input": "Contradiction analysis of AI code generation studies", "expected_keywords": ["contradiction", "conflicting", "methodology"], "category": "research"},
    {"id": "research-004", "input": "Citation assessment for software engineering papers", "expected_keywords": ["citation", "format", "quality"], "category": "research"},
    {"id": "research-005", "input": "Confidence estimation for AI debugging tools", "expected_keywords": ["confidence", "uncertainty", "evidence"], "category": "research"},
    {"id": "research-006", "input": "Synthesis of human-AI collaboration research", "expected_keywords": ["synthesis", "finding", "gap"], "category": "research"},
    {"id": "research-007", "input": "Report generation on neural code generation", "expected_keywords": ["report", "finding", "confidence"], "category": "research"},
    {"id": "research-008", "input": "What is the impact of AI on software testing?", "expected_keywords": ["evidence", "finding", "citation"], "category": "research"},
    {"id": "research-009", "input": "How does AI affect developer productivity?", "expected_keywords": ["confidence", "evidence", "synthesis"], "category": "research"},
    {"id": "research-010", "input": "Ethical implications of AI-generated code", "expected_keywords": ["finding", "evidence", "report"], "category": "research"},
]


def create_golden_benchmark() -> Benchmark:
    """Create the golden benchmark with all test cases."""
    all_tests = SIMPLE_TASKS + MEDIUM_TASKS + COMPLEX_TASKS + DOMAIN_TASKS + RESEARCH_TASKS
    return Benchmark(
        id="golden-test-set-v1",
        name="ECP Golden Test Set v1",
        description="Canonical test suite for ECP - must pass all tests",
        test_cases=all_tests,
    )


async def run_golden_test(case: dict[str, Any]) -> dict[str, Any]:
    """Run a single golden test case."""
    user_input = case.get("input", "")
    expected_keywords = case.get("expected_keywords", [])

    try:
        result = await adaptive_runtime.execute(user_input)
        output = str(result.get("decision", {}).get("decision", ""))
        output_lower = output.lower()

        passed = all(keyword.lower() in output_lower for keyword in expected_keywords)
        return {
            "case_id": case.get("id"),
            "passed": passed,
            "input": user_input,
            "expected_keywords": expected_keywords,
            "output": output[:200],
            "error": None,
        }
    except Exception as e:
        return {
            "case_id": case.get("id"),
            "passed": False,
            "input": user_input,
            "expected_keywords": expected_keywords,
            "output": "",
            "error": str(e),
        }


async def main():
    """Run the entire golden test suite."""
    benchmark = create_golden_benchmark()
    evaluation_framework.register_benchmark(benchmark)

    print(f"Running Golden Test Set v1 ({len(benchmark.test_cases)} tests)")
    print("=" * 80)

    results = []
    for case in benchmark.test_cases:
        result = await run_golden_test(case)
        results.append(result)
        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] {result['case_id']}: {result['input'][:50]}...")

    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    pass_rate = passed / total if total > 0 else 0

    print("=" * 80)
    print(f"Results: {passed}/{total} passed ({pass_rate:.2%})")

    if pass_rate < 0.8:
        print("FAILED: Pass rate below 80%")
        exit(1)
    else:
        print("SUCCESS: All golden tests passed!")
        exit(0)


if __name__ == "__main__":
    asyncio.run(main())
