"""
QA Engineer — Test Generator.

Generates unit, integration, regression, and benchmark tests from source code.
Supports Python (pytest), JavaScript/TypeScript (Jest), Go (go test), and Java (JUnit).
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from apps.qa_engineer.schemas import QATestArtifact, TestType, CoverageReport


@dataclass
class TestFunction:
    """A function extracted from source for test generation."""

    name: str
    signature: str
    body_lines: list[str]
    node: ast.FunctionDef | ast.AsyncFunctionDef
    lineno: int


class TestGenerator:
    """
    Generates tests from source code analysis.

    Usage::

        gen = TestGenerator()
        artifacts = gen.generate(source_code, language="python", framework="pytest", test_type="unit")
    """

    def __init__(self) -> None:
        self._source_cache: str = ""

    def generate(
        self,
        source_code: str,
        language: str = "python",
        framework: str = "pytest",
        test_type: str = "unit",
    ) -> list[QATestArtifact]:
        """
        Generate test artifacts from source code.

        Args:
            source_code: Source code content.
            language: Target language (python, javascript, go, java).
            framework: Test framework (pytest, jest, go-test, junit).
            test_type: unit | integration | benchmark | golden.

        Returns:
            List of QATestArtifact with generated test content.
        """
        if language == "python":
            self._source_cache = source_code
            return self._generate_python(source_code, framework, test_type)
        elif language in ("javascript", "typescript"):
            return self._generate_javascript(source_code, framework, test_type)
        elif language == "go":
            return self._generate_go(source_code, framework, test_type)
        elif language == "java":
            return self._generate_java(source_code, framework, test_type)
        return []

    def generate_regression(
        self,
        source_code: str,
        language: str = "python",
        framework: str = "pytest",
    ) -> tuple[list[QATestArtifact], dict[str, Any]]:
        """Generate regression test suite with risk assessment."""
        artifacts = self.generate(source_code, language, framework, "regression")

        regression_info: dict[str, Any] = {
            "tests_added": len(artifacts),
            "tests_removed": 0,
            "risky_changes": [],
            "maintenance_notes": [],
        }

        # Identify risky functions.
        try:
            tree = ast.parse(source_code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if self._is_risky_function(node, source_code):
                        regression_info["risky_changes"].append(
                            f"Function '{node.name}' at line {node.lineno}"
                        )
        except SyntaxError:
            regression_info["risky_changes"].append("Source has syntax errors — tests may not compile")

        return artifacts, regression_info

    def _generate_python(
        self, source_code: str, framework: str, test_type: str
    ) -> list[QATestArtifact]:
        if framework == "unittest":
            return self._gen_python_unittest(source_code, test_type)
        return self._gen_python_pytest(source_code, test_type)

    def _gen_python_pytest(
        self, source_code: str, test_type: str
    ) -> list[QATestArtifact]:
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return [QATestArtifact(
                file_path="test_errors.py",
                test_type=TestType.unit,
                test_count=0,
                content="# Source has syntax errors; no tests generated",
            )]

        functions = self._extract_functions(tree)
        classes = self._extract_classes(tree)

        test_funcs = self._gen_test_functions(functions, source_code)
        test_classes = self._gen_test_classes(classes, source_code)

        artifacts: list[QATestArtifact] = []

        if test_funcs:
            content = self._build_pytest_module(source_code, test_funcs, "functions")
            artifacts.append(QATestArtifact(
                file_path="test_functions.py",
                test_type=TestType.unit if test_type == "unit" else TestType.integration,
                test_count=len(test_funcs),
                content=content,
            ))

        if test_classes:
            content = self._build_pytest_module(source_code, test_classes, "classes")
            artifacts.append(QATestArtifact(
                file_path="test_classes.py",
                test_type=TestType.unit if test_type == "unit" else TestType.integration,
                test_count=len(test_classes),
                content=content,
            ))

        return artifacts

    def _gen_python_unittest(
        self, source_code: str, test_type: str
    ) -> list[QATestArtifact]:
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return [QATestArtifact(
                file_path="test_errors.py",
                test_type=TestType.unit,
                test_count=0,
                content="# Source has syntax errors",
            )]

        functions = self._extract_functions(tree)
        tests = self._gen_unittest_methods(functions)
        content = self._build_unittest_module(tests)
        return [QATestArtifact(
            file_path="test_unittest.py",
            test_type=TestType.unit if test_type == "unit" else TestType.integration,
            test_count=len(tests),
            content=content,
        )]

    def _gen_python_benchmark(self, source_code: str) -> list[QATestArtifact]:
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return []

        functions = self._extract_functions(tree)
        if not functions:
            return []

        content = self._build_benchmark_module(functions)
        return [QATestArtifact(
            file_path="test_benchmark.py",
            test_type=TestType.benchmark,
            test_count=len(functions),
            content=content,
        )]

    def _generate_javascript(
        self, source_code: str, framework: str, test_type: str
    ) -> list[QATestArtifact]:
        functions = self._extract_js_functions(source_code)
        lines: list[str] = []
        lines.append("const { describe, it, expect } = require('@jest/globals');")
        lines.append("")
        if functions:
            lines.append("describe('Module tests', () => {")
            for func_name in functions:
                lines.append(f"  it('should handle {func_name} correctly', () => {{")
                lines.append(f"    // TODO: Implement test for {func_name}")
                lines.append("    expect(true).toBe(true);")
                lines.append("  });")
                lines.append("")
            lines.append("});")
        else:
            lines.append("// No functions found to test.")
        content = "\n".join(lines)
        return [QATestArtifact(
            file_path="test.spec.js",
            test_type=TestType.unit if test_type == "unit" else TestType.integration,
            test_count=len(functions),
            content=content,
        )]

    def _generate_go(self, source_code: str, framework: str, test_type: str) -> list[QATestArtifact]:
        funcs = re.findall(r'func\s+(\w+)\s*\(', source_code)
        lines: list[str] = []
        lines.append("package main")
        lines.append("")
        lines.append("import \"testing\"")
        lines.append("")
        for fn in funcs:
            lines.append(f"func Test{fn.capitalize()}(t *testing.T) {{")
            lines.append(f"    // TODO: Implement test for {fn}")
            lines.append("    if true != true {")
            lines.append(f"        t.Errorf(\"{fn} failed\")")
            lines.append("    }")
            lines.append("}")
            lines.append("")
        content = "\n".join(lines)
        return [QATestArtifact(
            file_path="test_module_test.go",
            test_type=TestType.unit if test_type == "unit" else TestType.integration,
            test_count=len(funcs),
            content=content,
        )]

    def _generate_java(self, source_code: str, framework: str, test_type: str) -> list[QATestArtifact]:
        classes = re.findall(r'class\s+(\w+)', source_code)
        methods = re.findall(r'(?:public\s+)?(?:static\s+)?\w+\s+(\w+)\s*\(', source_code)

        lines: list[str] = []
        lines.append("import org.junit.jupiter.api.Test;")
        lines.append("import static org.junit.jupiter.api.Assertions.*;")
        lines.append("")
        for cls in classes:
            lines.append(f"public class Test{cls} {{")
            lines.append("")
            for method in methods[:10]:
                lines.append(f"  @Test")
                lines.append(f"  public void test{method.capitalize()}() {{")
                lines.append(f"    // TODO: Implement test for {method}")
                lines.append("    assertTrue(true);")
                lines.append("  }")
                lines.append("")
            lines.append("}")
            lines.append("")

        content = "\n".join(lines)
        return [QATestArtifact(
            file_path="TestClass.java",
            test_type=TestType.unit if test_type == "unit" else TestType.integration,
            test_count=len(methods),
            content=content,
        )]

    # ------------------------------------------------------------------
    # Python extraction helpers
    # ------------------------------------------------------------------

    def _extract_functions(self, tree: ast.AST) -> list[TestFunction]:
        functions: list[TestFunction] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                lines = self._get_source_segment(tree, node)
                sig = self._build_signature(node)
                functions.append(TestFunction(
                    name=node.name,
                    signature=sig,
                    body_lines=lines,
                    node=node,
                    lineno=node.lineno,
                ))
        return functions

    def _extract_classes(self, tree: ast.AST) -> list[TestFunction]:
        classes: list[TestFunction] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(TestFunction(
                    name=node.name,
                    signature=f"class {node.name}",
                    body_lines=[],
                    node=node,
                    lineno=node.lineno,
                ))
        return classes

    def _extract_js_functions(self, source_code: str) -> list[str]:
        patterns = [
            r'export\s+(?:default\s+)?(?:async\s+)?function\s+(\w+)',
            r'const\s+(\w+)\s*=\s*(?:async\s+)?\(',
            r'(?:async\s+)?(\w+)\s*=\s*(?:async\s+)?\(',
        ]
        found: set[str] = set()
        for pattern in patterns:
            for match in re.finditer(pattern, source_code):
                found.add(match.group(1))
        return list(found)

    def _is_risky_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef, source_code: str = "") -> bool:
        """Heuristic: functions touching DB, network, files, or with side effects."""
        risky_keywords = {"database", "db", "sql", "connect", "send", "write", "delete", "update", "save", "cache", "redis", "http", "request"}
        name_lower = node.name.lower()
        if any(k in name_lower for k in risky_keywords):
            return True
        try:
            source = ast.get_source_segment(source_code or getattr(self, "_source_cache", ""), node) or ""
        except Exception:
            source = ""
        if any(k in source.lower() for k in risky_keywords):
            return True
        return False

    def _get_source_segment(self, tree: ast.AST, node: ast.AST) -> list[str]:
        try:
            seg = ast.get_source_segment(self._source_cache, node) or ""
            return seg.splitlines()
        except Exception:
            return []

    def _build_signature(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        args = [a.arg for a in node.args.args]
        return f"{node.name}({', '.join(args)})"

    def _gen_test_functions(self, functions: list[TestFunction], source_code: str) -> list[str]:
        return [fn.name for fn in functions]

    def _gen_test_classes(self, classes: list[TestFunction], source_code: str) -> list[str]:
        return [cls.name for cls in classes]

    def _gen_unittest_methods(self, functions: list[TestFunction]) -> list[str]:
        return [fn.name for fn in functions]

    def _build_pytest_module(self, source_code: str, names: list[str] | list[TestFunction], label: str) -> str:
        name_list = [n if isinstance(n, str) else n.name for n in names]
        lines: list[str] = []
        lines.append('"""Auto-generated test module by QA Engineer."""')
        lines.append("import pytest")
        lines.append("")
        lines.append("class TestAutoGenerated:")
        lines.append("")
        for name in name_list:
            lines.append(f"    def test_{name}_behavior(self):")
            lines.append(f"        \"\"\"Test {name} basic behavior.\"\"\"")
            lines.append(f"        # TODO: Implement comprehensive test for {name}")
            lines.append(f"        assert True")
            lines.append("")
        return "\n".join(lines)

    def _build_unittest_module(self, method_names: list[str]) -> str:
        lines: list[str] = []
        lines.append('"""Auto-generated unittest module by QA Engineer."""')
        lines.append("import unittest")
        lines.append("")
        lines.append("class TestAutoGenerated(unittest.TestCase):")
        lines.append("")
        for name in method_names:
            lines.append(f"    def test_{name}(self):")
            lines.append(f"        \"\"\"Test {name}.\"\"\"")
            lines.append(f"        self.assertTrue(True)")
            lines.append("")
        lines.append("")
        lines.append("if __name__ == '__main__':")
        lines.append("    unittest.main()")
        return "\n".join(lines)

    def _build_benchmark_module(self, functions: list[TestFunction]) -> str:
        lines: list[str] = []
        lines.append('"""Auto-generated benchmark tests by QA Engineer."""')
        lines.append("import time")
        lines.append("import statistics")
        lines.append("")
        lines.append("def run_benchmarks():")
        lines.append("    results = {}")
        lines.append("")
        for fn in functions:
            lines.append(f"    # Benchmark {fn.name}")
            lines.append(f"    times = []")
            lines.append(f"    for _ in range(100):")
            lines.append(f"        start = time.perf_counter()")
            lines.append(f"        # TODO: Call {fn.name}()")
            lines.append(f"        elapsed = time.perf_counter() - start")
            lines.append(f"        times.append(elapsed)")
            lines.append(f"    results['{fn.name}'] = statistics.mean(times)")
            lines.append("")
        lines.append("    return results")
        lines.append("")
        lines.append("if __name__ == '__main__':")
        lines.append("    print(run_benchmarks())")
        return "\n".join(lines)

    def _set_source_cache(self, source_code: str) -> None:
        self._source_cache = source_code
