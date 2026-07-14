"""
Code Engineer Golden Tests
============================

Tests Code Engineer with various Python code samples.
"""

import pytest
from apps.code_engineer import get_app
from apps.code_engineer.parser import code_parser, CodeAST
from apps.code_engineer.analyzer import code_analyzer


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
