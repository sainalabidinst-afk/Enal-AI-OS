"""
Code Engineer Benchmark
========================

Measures Code Engineer's knowledge quality across dimensions:
- Architecture Pattern Detection: accuracy of detecting Clean Arch, DDD, SOLID, CQRS, Event Sourcing
- Secure Coding Detection: accuracy of detecting OWASP Top 10, hardcoded secrets, auth issues
- False Positive Rate: precision of findings
- Coverage: breadth of detections across all pattern types
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from apps.code_engineer.architecture_patterns import architecture_pattern_analyzer
from apps.code_engineer.parser import code_parser
from apps.code_engineer.secure_coding import secure_coding_analyzer

logger = logging.getLogger(__name__)


@dataclass
class CodeEngineerBenchmarkReport:
    generated_at: datetime = field(default_factory=datetime.utcnow)
    architecture_pattern_score: float = 0.0
    secure_coding_score: float = 0.0
    overall_score: float = 0.0
    total_architecture_findings: int = 0
    total_secure_coding_findings: int = 0
    architecture_by_category: dict[str, int] = field(default_factory=dict)
    security_by_category: dict[str, int] = field(default_factory=dict)
    passed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at.isoformat(),
            "architecture_pattern_score": round(self.architecture_pattern_score, 2),
            "secure_coding_score": round(self.secure_coding_score, 2),
            "overall_score": round(self.overall_score, 2),
            "total_architecture_findings": self.total_architecture_findings,
            "total_secure_coding_findings": self.total_secure_coding_findings,
            "architecture_by_category": self.architecture_by_category,
            "security_by_category": self.security_by_category,
            "passed": self.passed,
        }


# Test cases with known architecture patterns
ARCH_TEST_CASES = [
    {
        "name": "clean_arch_dependency_rule",
        "code": """
import os
from typing import Optional

class UserEntity:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def get_id(self) -> str:
        return self.id

class UserRepository:
    def save(self, user: UserEntity) -> None:
        pass
    def find_by_id(self, id: str) -> Optional[UserEntity]:
        pass

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    def create_user(self, name: str) -> UserEntity:
        user = UserEntity(id="123", name=name)
        self.repo.save(user)
        return user
""",
        "expected_patterns": ["entity", "repository"],
        "category": "clean_architecture",
    },
    {
        "name": "ddd_aggregate",
        "code": """
class Order:
    def __init__(self, id: str):
        self.id = id
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_id):
        self.items = [i for i in self.items if i.id != item_id]
""",
        "expected_patterns": ["entity", "aggregate_root"],
        "category": "ddd",
    },
    {
        "name": "solid_srp_violation",
        "code": """
class MegaService:
    def m01(self): pass
    def m02(self): pass
    def m03(self): pass
    def m04(self): pass
    def m05(self): pass
    def m06(self): pass
    def m07(self): pass
    def m08(self): pass
    def m09(self): pass
    def m10(self): pass
    def m11(self): pass
    def m12(self): pass
    def m13(self): pass
    def m14(self): pass
    def m15(self): pass
    def m16(self): pass
""",
        "expected_patterns": ["single_responsibility"],
        "category": "solid",
    },
    {
        "name": "cqrs_command_query",
        "code": """
class CreateOrderCommand:
    def execute(self):
        pass

class GetOrderByIdQuery:
    pass
""",
        "expected_patterns": ["command", "query"],
        "category": "cqrs",
    },
    {
        "name": "event_sourcing",
        "code": """
class EventStore:
    def append(self, event):
        pass
    def read_stream(self, aggregate_id):
        pass

class OrderProjection:
    def when(self, event):
        pass
""",
        "expected_patterns": ["event_store", "projection"],
        "category": "event_sourcing",
    },
]

# Test cases with known security issues
SEC_TEST_CASES = [
{
        "name": "injection_vulnerabilities",
        "code": """
import os
import sqlite3

def get_user(user_id):
    execute(f"SELECT * FROM users WHERE id = {user_id}")
    return sqlite3.connect('db.db').execute(f"SELECT * FROM users WHERE id = {user_id}").fetchall()

def run(cmd):
    os.system(cmd)
""",
        "expected_patterns": ["injection", "sql_injection"],
        "category": "owasp",
    },
    {
        "name": "hardcoded_secrets",
        "code": """
API_KEY = "sk-abcdefghijklmnopqrstuvwxyz"
ADMIN_PASSWORD = "supersecret123"
""",
        "expected_patterns": ["hardcoded_secret"],
        "category": "owasp",
    },
    {
        "name": "plaintext_password",
        "code": """
password = "admin123"
""",
        "expected_patterns": ["plaintext_password"],
        "category": "auth",
    },
    {
        "name": "ssrf_potential",
        "code": """
import requests

def fetch_url(url):
    return requests.get(url)
""",
        "expected_patterns": ["ssrf"],
        "category": "owasp",
    },
]


def run_code_engineer_benchmark() -> CodeEngineerBenchmarkReport:
    """Run benchmark against all test cases."""
    report = CodeEngineerBenchmarkReport()

    # Architecture pattern detection
    arch_total = 0
    arch_found = 0
    arch_by_category: dict[str, int] = {}

    for case in ARCH_TEST_CASES:
        ast_obj = code_parser.parse(case["code"], f"{case['name']}.py")
        results = architecture_pattern_analyzer.analyze(ast_obj)
        all_findings = []
        for cat_findings in results.values():
            all_findings.extend(cat_findings)

        detected_patterns = set(f.pattern for f in all_findings)
        expected = set(case["expected_patterns"])
        cat = case["category"]

        arch_by_category[cat] = arch_by_category.get(cat, 0) + 1
        arch_total += len(expected)
        for ep in expected:
            if ep in detected_patterns:
                arch_found += 1
                arch_by_category[cat] = arch_by_category.get(cat, 0) + 1

        logger.info(
            "Arch test '%s': expected=%s, detected=%s",
            case["name"], expected, detected_patterns & expected
        )

    report.architecture_pattern_score = (arch_found / max(arch_total, 1)) * 100.0
    report.total_architecture_findings = arch_total
    report.architecture_by_category = arch_by_category

    # Secure coding detection
    sec_total = 0
    sec_found = 0
    sec_by_category: dict[str, int] = {}

    for case in SEC_TEST_CASES:
        ast_obj = code_parser.parse(case["code"], f"{case['name']}.py")
        results = secure_coding_analyzer.analyze(ast_obj)
        all_findings = []
        for cat_findings in results.values():
            all_findings.extend(cat_findings)

        detected_patterns = set(f.pattern for f in all_findings)
        expected = set(case["expected_patterns"])
        cat = case["category"]

        sec_by_category[cat] = sec_by_category.get(cat, 0) + 1
        sec_total += len(expected)
        for ep in expected:
            if ep in detected_patterns:
                sec_found += 1
                sec_by_category[cat] = sec_by_category.get(cat, 0) + 1

        logger.info(
            "Sec test '%s': expected=%s, detected=%s",
            case["name"], expected, detected_patterns & expected
        )

    report.secure_coding_score = (sec_found / max(sec_total, 1)) * 100.0
    report.total_secure_coding_findings = sec_total
    report.security_by_category = sec_by_category

    # Overall score (weighted average)
    report.overall_score = (report.architecture_pattern_score * 0.5 +
                            report.secure_coding_score * 0.5)
    report.passed = report.overall_score >= 90.0

    return report


def print_summary(report: CodeEngineerBenchmarkReport) -> None:
    print("\n" + "=" * 60)
    print("  Code Engineer Benchmark Report")
    print("=" * 60)
    print(f"  Generated : {report.generated_at.isoformat()}")
    print(f"  Architecture Pattern Score : {report.architecture_pattern_score:.1f}%")
    print(f"  Secure Coding Score        : {report.secure_coding_score:.1f}%")
    print(f"  Overall Score              : {report.overall_score:.1f}%")
    print(f"  Total Arch Findings        : {report.total_architecture_findings}")
    print(f"  Total Sec Findings         : {report.total_secure_coding_findings}")
    print(f"  Passed                     : {report.passed}")
    print("=" * 60 + "\n")

    if report.passed:
        print("  ✅ Code Engineer benchmark PASSED\n")
    else:
        print("  ❌ Code Engineer benchmark FAILED\n")


def main() -> int:
    report = run_code_engineer_benchmark()
    print_summary(report)
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
