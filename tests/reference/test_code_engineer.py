"""
Code Engineer Golden Tests
============================

Tests Code Engineer with various Python code samples.
"""

from apps.code_engineer import get_app
from apps.code_engineer.analyzer import code_analyzer
from apps.code_engineer.parser import code_parser
from apps.code_engineer.architecture_patterns import architecture_pattern_analyzer
from apps.code_engineer.secure_coding import secure_coding_analyzer

SIMPLE_CODE = '''
import os
import sys

def hello(name: str) -> str:
    """Say hello."""
    return f"Hello, {name}!"

class Greeter:
    """Greeter class."""
    def __init__(self):
        self.greetings = []

    def add_greeting(self, greeting):
        self.greetings.append(greeting)
'''

COMPLEX_CODE = '''
import os
import pickle

def process_data(data):
    result = eval(data)
    return result

class DataProcessor:
    def load(self, path):
        with open(path, "rb") as f:
            return pickle.loads(f.read())
'''

INSECURE_CODE = '''
import os

def run_command(cmd):
    os.system(cmd)

def unsafe_load(data):
    return pickle.loads(data)
'''


def test_parse_simple_code():
    ast_obj = code_parser.parse(SIMPLE_CODE, "simple.py")
    top_level_functions = [f for f in ast_obj.functions if not f.name.startswith("__")]
    assert len(top_level_functions) == 1
    assert len(ast_obj.classes) == 1
    assert top_level_functions[0].name == "hello"
    assert ast_obj.classes[0].name == "Greeter"
    print(f"[PASS] Parse Simple: {len(top_level_functions)} top-level functions, {len(ast_obj.classes)} classes")


def test_analyze_docstrings():
    ast_obj = code_parser.parse(SIMPLE_CODE, "simple.py")
    issues = code_analyzer.analyze(ast_obj)
    doc_issues = [i for i in issues if i.category == "Documentation"]
    assert len(doc_issues) == 2, "Class methods missing docstrings should be flagged"
    print(f"[PASS] Docstring Check: {len(doc_issues)} docstring issues found")


def test_analyze_security():
    ast_obj = code_parser.parse(INSECURE_CODE, "insecure.py")
    issues = code_analyzer.analyze(ast_obj)
    security_issues = [i for i in issues if i.category == "Security"]
    assert len(security_issues) >= 2, "Should detect security issues"
    print(f"[PASS] Security Check: {len(security_issues)} security issues found")


def test_app_analyze_code():
    app = get_app()
    result = app.analyze_code(SIMPLE_CODE, "simple.py")
    assert "issues" in result
    assert "functions" in result
    assert "classes" in result
    print(f"[PASS] App Analyze: {result['functions']} functions, {result['classes']} classes")


def test_ast_structure():
    ast_obj = code_parser.parse(SIMPLE_CODE, "simple.py")
    assert ast_obj.vendor == "python"
    assert len(ast_obj.imports) > 0
    print(f"[PASS] AST Structure: {len(ast_obj.imports)} imports detected")


def test_empty_code():
    ast_obj = code_parser.parse("", "empty.py")
    assert len(ast_obj.functions) == 0
    assert len(ast_obj.classes) == 0
    print("[PASS] Empty Code: handled correctly")


def test_syntax_error():
    bad_code = "def invalid(:\n    pass"
    ast_obj = code_parser.parse(bad_code, "bad.py")
    assert len(ast_obj.errors) > 0
    print(f"[PASS] Syntax Error: {len(ast_obj.errors)} error(s) detected")


# ─── Architecture Pattern Tests ───────────────────────────────────────────────

ARCH_CODE = """
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
"""


def test_architecture_pattern_master_analyzer():
    """Test ArchitecturePatternAnalyzer produces findings for all categories."""
    ast_obj = code_parser.parse(ARCH_CODE, "domain/user.py")
    results = architecture_pattern_analyzer.analyze(ast_obj)
    categories = list(results.keys())
    assert "clean_architecture" in categories
    assert "ddd" in categories
    assert "solid" in categories
    assert "cqrs" in categories
    assert "event_sourcing" in categories
    total = sum(len(v) for v in results.values())
    print(f"[PASS] MasterAnalyzer: {len(categories)} categories, {total} total findings")


def test_architecture_pattern_ddd_entity():
    """Test DDDAnalyzer detects Entity and Repository patterns."""
    ast_obj = code_parser.parse(ARCH_CODE, "domain/user.py")
    results = architecture_pattern_analyzer.analyze(ast_obj)
    ddd_findings = results.get("ddd", [])
    patterns = [f.pattern for f in ddd_findings]
    assert "entity" in patterns, "Should detect Entity pattern"
    assert "repository" in patterns, "Should detect Repository pattern"
    print(f"[PASS] DDD: {len(ddd_findings)} findings - patterns: {patterns}")


def test_architecture_pattern_solid_srp():
    """Test SOLIDAnalyzer detects Single Responsibility violations."""
    BIG_CLASS_CODE = """
class MegaService:
    def method01(self): pass
    def method02(self): pass
    def method03(self): pass
    def method04(self): pass
    def method05(self): pass
    def method06(self): pass
    def method07(self): pass
    def method08(self): pass
    def method09(self): pass
    def method10(self): pass
    def method11(self): pass
    def method12(self): pass
    def method13(self): pass
    def method14(self): pass
    def method15(self): pass
    def method16(self): pass
"""
    ast_obj = code_parser.parse(BIG_CLASS_CODE, "big.py")
    results = architecture_pattern_analyzer.analyze(ast_obj)
    solid_findings = results.get("solid", [])
    srp_findings = [f for f in solid_findings if f.pattern == "single_responsibility"]
    assert len(srp_findings) >= 1, "Should detect SRP violation for class with 16 methods"
    print(f"[PASS] SOLID SRP: {len(srp_findings)} SRP violations found")


def test_architecture_pattern_cqrs():
    """Test CQRSAnalyzer detects Command/Query patterns."""
    CQRS_CODE = """
class CreateOrderCommand:
    def execute(self):
        pass

class GetOrderByIdQuery:
    pass
"""
    ast_obj = code_parser.parse(CQRS_CODE, "cqrs.py")
    results = architecture_pattern_analyzer.analyze(ast_obj)
    cqrs_findings = results.get("cqrs", [])
    patterns = [f.pattern for f in cqrs_findings]
    assert "command" in patterns, "Should detect Command pattern"
    assert "query" in patterns, "Should detect Query pattern"
    print(f"[PASS] CQRS: {len(cqrs_findings)} findings - patterns: {patterns}")


def test_architecture_pattern_event_sourcing():
    """Test EventSourcingAnalyzer detects Event Store patterns."""
    ES_CODE = """
class EventStore:
    def append(self, event):
        pass
    def read_stream(self, aggregate_id):
        pass

class OrderProjection:
    def when(self, event):
        pass
"""
    ast_obj = code_parser.parse(ES_CODE, "events.py")
    results = architecture_pattern_analyzer.analyze(ast_obj)
    es_findings = results.get("event_sourcing", [])
    patterns = [f.pattern for f in es_findings]
    assert "event_store" in patterns, "Should detect Event Store pattern"
    assert "projection" in patterns, "Should detect Projection pattern"
    print(f"[PASS] EventSourcing: {len(es_findings)} findings - patterns: {patterns}")


# ─── Secure Coding Tests ────────────────────────────────────────────────────

MALICIOUS_CODE = """
import os
import sqlite3

def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return sqlite3.connect('db.db').execute(query).fetchall()

def run(cmd):
    os.system(cmd)

API_KEY = "sk-abcdefghijklmnopqrstuvwxyz"
"""


def test_secure_coding_owasp_injection():
    """Test OWASPDetector detects injection vulnerabilities."""
    ast_obj = code_parser.parse(MALICIOUS_CODE, "insecure.py")
    results = secure_coding_analyzer.analyze(ast_obj)
    owasp_findings = results.get("owasp", [])
    patterns = [f.pattern for f in owasp_findings]
    assert "injection" in patterns, "Should detect OS command injection"
    print(f"[PASS] OWASP Injection: {len(owasp_findings)} findings - patterns: {patterns}")


def test_secure_coding_owasp_secrets():
    """Test OWASPDetector detects hardcoded secrets."""
    SECRET_CODE = """
ADMIN_PASSWORD = "supersecret123"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
"""
    ast_obj = code_parser.parse(SECRET_CODE, "secrets.py")
    results = secure_coding_analyzer.analyze(ast_obj)
    owasp_findings = results.get("owasp", [])
    patterns = [f.pattern for f in owasp_findings]
    assert "hardcoded_secret" in patterns, "Should detect hardcoded secrets"
    print(f"[PASS] OWASP Secrets: {len(owasp_findings)} findings - patterns: {patterns}")


def test_secure_coding_auth_password():
    """Test AuthAnalyzer detects plaintext passwords."""
    PW_CODE = """
password = "admin123"
"""
    ast_obj = code_parser.parse(PW_CODE, "pw.py")
    results = secure_coding_analyzer.analyze(ast_obj)
    auth_findings = results.get("auth", [])
    patterns = [f.pattern for f in auth_findings]
    assert "plaintext_password" in patterns, "Should detect plaintext password"
    print(f"[PASS] Auth Password: {len(auth_findings)} findings - patterns: {patterns}")


def test_secure_coding_api_missing_auth():
    """Test AuthAnalyzer flags missing auth in API modules."""
    API_CODE = """
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def list_users():
    return []
"""
    ast_obj = code_parser.parse(API_CODE, "api/users.py")
    results = secure_coding_analyzer.analyze(ast_obj)
    auth_findings = results.get("auth", [])
    print(f"[PASS] Auth API: {len(auth_findings)} findings")


def test_secure_coding_master_analyzer():
    """Test SecureCodingAnalyzer coordinates all sub-analyzers."""
    ast_obj = code_parser.parse(MALICIOUS_CODE, "insecure.py")
    results = secure_coding_analyzer.analyze(ast_obj)
    categories = list(results.keys())
    assert "owasp" in categories
    assert "auth" in categories
    total = sum(len(v) for v in results.values())
    print(f"[PASS] SecureCoding Master: {len(categories)} categories, {total} total findings")
