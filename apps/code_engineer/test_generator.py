"""
Test Generator
===============

Automated test generation for Python repositories.
Analyzes code structure and generates pytest unit tests
with mocks, fixtures, and edge case coverage.

Pipeline:
  Source Code → AST Analysis → Test Generation → Mock/Fixture Generation
  → Edge Case Detection → Coverage Analysis
"""

import ast
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Union

logger = logging.getLogger(__name__)


@dataclass
class GeneratedTest:
    """A single generated test function."""
    name: str
    source_code: str
    target_function: str = ""
    target_class: str = ""
    test_type: str = "unit"
    coverage_lines: list[int] = field(default_factory=list)
    fixtures_needed: list[str] = field(default_factory=list)
    mocks_needed: list[str] = field(default_factory=list)


@dataclass
class TestFile:
    """A complete generated test file."""
    file_path: str
    module_path: str
    imports: list[str] = field(default_factory=list)
    fixtures: list[str] = field(default_factory=list)
    mock_definitions: list[str] = field(default_factory=list)
    tests: list[GeneratedTest] = field(default_factory=list)
    edge_case_tests: list[GeneratedTest] = field(default_factory=list)
    coverage_estimate: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def render(self) -> str:
        """Render the test file as complete Python source."""
        lines = [
            '"""',
            f"Auto-generated tests for {self.module_path}",
            '"""',
            "",
        ]
        for imp in self.imports:
            lines.append(imp)
        lines.append("")
        for fixture in self.fixtures:
            lines.append(fixture)
            lines.append("")
        for test in self.tests + self.edge_case_tests:
            lines.append(test.source_code)
            lines.append("")
        return "\n".join(lines)


@dataclass
class TestGenerationReport:
    """Report of all generated tests."""
    source_path: str
    test_files: list[TestFile] = field(default_factory=list)
    total_tests: int = 0
    total_fixtures: int = 0
    total_mocks: int = 0
    edge_cases_found: int = 0
    estimated_coverage: float = 0.0
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_path": self.source_path,
            "test_files": len(self.test_files),
            "total_tests": self.total_tests,
            "total_fixtures": self.total_fixtures,
            "total_mocks": self.total_mocks,
            "edge_cases_found": self.edge_cases_found,
            "estimated_coverage": round(self.estimated_coverage, 2),
            "warnings": self.warnings,
        }


class TestGenerator:
    """Generates pytest tests from Python source code."""

    TEST_IMPORTS = [
        "import pytest",
        "from unittest.mock import Mock, patch, MagicMock, AsyncMock",
    ]

    def __init__(self) -> None:
        self._detected_frameworks: dict[str, bool] = {}

    async def generate_for_module(
        self,
        source_path: str,
        module_path: str,
        output_dir: Optional[str] = None,
    ) -> TestFile:
        """Generate tests for a single Python module."""
        source = Path(source_path)
        if not source.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")

        code = source.read_text(encoding="utf-8")
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return TestFile(
                file_path=str(source),
                module_path=module_path,
                metadata={"error": str(e)},
            )

        self._detect_framework(code)
        functions = self._extract_functions(tree)
        classes = self._extract_classes(tree)

        test_file = TestFile(
            file_path=self._determine_test_path(source, output_dir),
            module_path=module_path,
        )

        # Build import statement
        func_names = [f.name for f in functions]
        cls_names = [c.name for c in classes]
        all_names = func_names + cls_names

        if all_names:
            if len(all_names) <= 8:
                test_file.imports.append(
                    f"from {module_path} import {', '.join(all_names)}"
                )
            else:
                test_file.imports.append(f"from {module_path} import (")
                for name in all_names:
                    test_file.imports.append(f"    {name},")
                test_file.imports.append(")")
        else:
            test_file.imports.append(f"import {module_path}")

        for imp in self.TEST_IMPORTS:
            test_file.imports.insert(0, imp)

        # Generate fixtures
        for cls in classes:
            fixture = self._generate_fixture(cls)
            if fixture:
                test_file.fixtures.append(fixture)

        # Generate tests for functions
        for func in functions:
            test = self._gen_function_test(func)
            if test:
                test_file.tests.append(test)

        # Generate tests for class methods
        for cls in classes:
            for item in cls.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    method = item
                    if method.name.startswith("__"):
                        continue
                    if method.name.startswith("_"):
                        continue
                    test = self._gen_method_test(method, cls)
                    if test:
                        test_file.tests.append(test)

        # Generate edge case tests
        for func in functions:
            edges = self._gen_edge_tests(func)
            test_file.edge_case_tests.extend(edges)

        for cls in classes:
            for item in cls.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    method = item
                    if method.name.startswith("_") or method.name == "__init__":
                        continue
                    edges = self._gen_edge_method_tests(method, cls)
                    test_file.edge_case_tests.extend(edges)

        # Estimate coverage
        total_fns = len([f for f in functions if not f.name.startswith("_")])
        total_cls_methods = 0
        for cls in classes:
            total_cls_methods += sum(
                1 for m in cls.body
                if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))
                and not m.name.startswith("_") and not m.name == "__init__"
            )
        total_items = total_fns + total_cls_methods
        total_gen = len(test_file.tests) + len(test_file.edge_case_tests)
        test_file.coverage_estimate = min(1.0, (total_gen / max(total_items, 1)) * 0.8)

        logger.info(
            f"Generated {len(test_file.tests)} tests + "
            f"{len(test_file.edge_case_tests)} edge cases for {module_path}"
        )
        return test_file

    def _detect_framework(self, code: str) -> None:
        """Detect framework usage."""
        self._detected_frameworks["asyncio"] = "async def" in code

    def _extract_functions(self, tree: ast.Module) -> list[ast.FunctionDef]:
        """Extract top-level functions."""
        return [n for n in tree.body if isinstance(n, ast.FunctionDef)]

    def _extract_classes(self, tree: ast.Module) -> list[ast.ClassDef]:
        """Extract classes."""
        return [n for n in tree.body if isinstance(n, ast.ClassDef)]

    def _determine_test_path(self, source: Path, output_dir: Optional[str]) -> str:
        """Determine test file output path."""
        if output_dir:
            test_dir = Path(output_dir)
        else:
            parent = source.parent
            test_dir = (
                parent.parent / "tests"
                if parent.name in ("app", "apps")
                else parent / "tests"
            )
            if not test_dir.exists():
                test_dir = parent
        test_dir.mkdir(parents=True, exist_ok=True)
        stem = source.stem
        test_name = f"test_{stem}" if not stem.startswith("test_") else stem
        return str(test_dir / f"{test_name}.py")

    def _generate_fixture(self, cls: ast.ClassDef) -> Optional[str]:
        """Generate pytest fixture from __init__ method."""
        init_m = None
        for item in cls.body:
            if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                init_m = item
                break
        if init_m is None:
            return None

        args = init_m.args
        params = args.args[1:] if args.args and args.args[0].arg == "self" else args.args
        names = [p.arg for p in params]
        num_no_default = len(names) - len(args.defaults)

        vals: list[Optional[str]] = []
        for i, name in enumerate(names):
            if i < num_no_default:
                vals.append(None)
            else:
                idx = i - num_no_default
                if idx < len(args.defaults):
                    vals.append(self._render_default(args.defaults[idx]))

        fixture_params = []
        call_args = []
        for i, name in enumerate(names):
            if vals[i] is not None:
                call_args.append(f"{name}={vals[i]}")
            else:
                call_args.append(f"{name}=None")
                fixture_params.append(f"{name}=None")

        if fixture_params:
            result = (
                f"@pytest.fixture\n"
                f"def {cls.name.lower()}_instance({', '.join(fixture_params)}):\n"
                f"    return {cls.name}({', '.join(call_args)})"
            )
        else:
            result = (
                f"@pytest.fixture\n"
                f"def {cls.name.lower()}_instance():\n"
                f"    return {cls.name}({', '.join(call_args)})"
            )
        return result

    def _render_default(self, node: ast.expr) -> str:
        """Render a default value node as source code."""
        if isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, (ast.List, ast.Dict, ast.Tuple)):
            return "None"
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Call):
            return "None"
        return "None"

    def _gen_function_test(self, func: ast.FunctionDef) -> Optional[GeneratedTest]:
        """Generate test for a function."""
        name = func.name
        args = func.args
        has_return = self._has_return(func)
        is_async = isinstance(func, ast.AsyncFunctionDef)
        decorator = "async " if is_async else ""

        params = args.args
        if params and params[0].arg == "self":
            params = params[1:]
        pnames = [p.arg for p in params]
        test_args = ", ".join(pnames) if pnames else ""

        if has_return:
            src = (
                f"{decorator}def test_{name}_returns_expected_result(self, {test_args}):\n"
                f'    """Test that {name} returns expected result."""\n'
                f"    # Arrange\n"
                f"    result = {name}({test_args})\n"
                f"    # Assert\n"
                f"    assert result is not None\n"
            )
        else:
            src = (
                f"{decorator}def test_{name}_executes_successfully(self, {test_args}):\n"
                f'    """Test that {name} executes without error."""\n'
                f"    # Arrange\n"
                f"    result = {name}({test_args})\n"
                f"    # Assert\n"
                f"    assert result is None\n"
            )

        return GeneratedTest(
            name=f"test_{name}",
            source_code=src,
            target_function=name,
            test_type="unit",
            mocks_needed=self._infer_mocks(func),
        )

    def _gen_method_test(
        self, method: Union[ast.FunctionDef, ast.AsyncFunctionDef], cls: ast.ClassDef
    ) -> Optional[GeneratedTest]:
        """Generate test for a class method."""
        name = method.name
        args = method.args
        params = args.args[1:] if args.args and args.args[0].arg == "self" else args.args
        pnames = [p.arg for p in params]
        test_args = ", ".join(pnames) if pnames else ""

        is_async = isinstance(method, ast.AsyncFunctionDef)
        decorator = "async " if is_async else ""
        inst = f"{cls.name.lower()}_instance"

        src = (
            f"{decorator}def test_{cls.name.lower()}_{name}(self, {inst}):\n"
            f'    """Test {cls.name}.{name}."""\n'
            f"    instance = {inst}\n"
            f"    result = instance.{name}({test_args})\n"
            f"    assert result is not None\n"
        )

        return GeneratedTest(
            name=f"test_{cls.name.lower()}_{name}",
            source_code=src,
            target_function=name,
            target_class=cls.name,
            test_type="unit",
            fixtures_needed=[inst],
        )

    def _gen_edge_tests(self, func: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> list[GeneratedTest]:
        """Generate edge case tests for a function."""
        results: list[GeneratedTest] = []
        name = func.name
        args = func.args
        params = args.args
        if params and params[0].arg == "self":
            params = params[1:]

        for param in params:
            if not hasattr(param, "annotation") or not param.annotation:
                continue
            t = self._get_type_name(param.annotation)
            if t in ("str", "Optional[str]"):
                src = f"def test_{name}_empty_{param.arg}(self):\n"
                src += f'    """Test {name} with empty {param.arg}."""\n'
                src += f"    result = {name}({param.arg}='')\n"
                src += f"    assert result is not None\n"
                results.append(GeneratedTest(
                    name=f"test_{name}_empty_{param.arg}",
                    source_code=src,
                    target_function=name,
                    test_type="edge_case",
                ))
                src2 = f"def test_{name}_none_{param.arg}(self):\n"
                src2 += f'    """Test {name} with None {param.arg}."""\n'
                src2 += f"    result = {name}({param.arg}=None)\n"
                src2 += f"    assert result is not None\n"
                results.append(GeneratedTest(
                    name=f"test_{name}_none_{param.arg}",
                    source_code=src2,
                    target_function=name,
                    test_type="edge_case",
                ))
            elif t.replace("Optional[", "").replace("]", "") in ("int", "float"):
                src = f"def test_{name}_zero_{param.arg}(self):\n"
                src += f'    """Test {name} with zero {param.arg}."""\n'
                src += f"    result = {name}({param.arg}=0)\n"
                src += f"    assert result is not None\n"
                results.append(GeneratedTest(
                    name=f"test_{name}_zero_{param.arg}",
                    source_code=src,
                    target_function=name,
                    test_type="edge_case",
                ))
                src2 = f"def test_{name}_negative_{param.arg}(self):\n"
                src2 += f'    """Test {name} with negative {param.arg}."""\n'
                src2 += f"    result = {name}({param.arg}=-1)\n"
                src2 += f"    assert result is not None\n"
                results.append(GeneratedTest(
                    name=f"test_{name}_negative_{param.arg}",
                    source_code=src2,
                    target_function=name,
                    test_type="edge_case",
                ))
            elif "list" in t.lower():
                src = f"def test_{name}_empty_{param.arg}(self):\n"
                src += f'    """Test {name} with empty {param.arg}."""\n'
                src += f"    result = {name}({param.arg}=[])\n"
                src += f"    assert result is not None\n"
                results.append(GeneratedTest(
                    name=f"test_{name}_empty_{param.arg}",
                    source_code=src,
                    target_function=name,
                    test_type="edge_case",
                ))
        return results

    def _gen_edge_method_tests(
        self, method: Union[ast.FunctionDef, ast.AsyncFunctionDef], cls: ast.ClassDef
    ) -> list[GeneratedTest]:
        """Generate edge case tests for a method."""
        results: list[GeneratedTest] = []
        name = method.name
        args = method.args
        params = args.args[1:] if args.args and args.args[0].arg == "self" else args.args
        inst = f"{cls.name.lower()}_instance"

        for param in params:
            if not hasattr(param, "annotation") or not param.annotation:
                continue
            t = self._get_type_name(param.annotation)
            prefix = f"{cls.name.lower()}_{name}"
            if t in ("str", "Optional[str]"):
                src = f"def test_{prefix}_empty_{param.arg}(self, {inst}):\n"
                src += f"    inst = {inst}\n"
                src += f"    result = inst.{name}({param.arg}='')\n"
                src += f"    assert result is not None\n"
                results.append(GeneratedTest(
                    name=f"test_{prefix}_empty_{param.arg}",
                    source_code=src,
                    target_function=name,
                    target_class=cls.name,
                    test_type="edge_case",
                    fixtures_needed=[inst],
                ))
                src2 = f"def test_{prefix}_none_{param.arg}(self, {inst}):\n"
                src2 += f"    inst = {inst}\n"
                src2 += f"    result = inst.{name}({param.arg}=None)\n"
                src2 += f"    assert result is not None\n"
                results.append(GeneratedTest(
                    name=f"test_{prefix}_none_{param.arg}",
                    source_code=src2,
                    target_function=name,
                    target_class=cls.name,
                    test_type="edge_case",
                    fixtures_needed=[inst],
                ))
            elif t.replace("Optional[", "").replace("]", "") in ("int", "float"):
                src = f"def test_{prefix}_zero_{param.arg}(self, {inst}):\n"
                src += f"    inst = {inst}\n"
                src += f"    result = inst.{name}({param.arg}=0)\n"
                src += f"    assert result is not None\n"
                results.append(GeneratedTest(
                    name=f"test_{prefix}_zero_{param.arg}",
                    source_code=src,
                    target_function=name,
                    target_class=cls.name,
                    test_type="edge_case",
                    fixtures_needed=[inst],
                ))
                src2 = f"def test_{prefix}_negative_{param.arg}(self, {inst}):\n"
                src2 += f"    inst = {inst}\n"
                src2 += f"    result = inst.{name}({param.arg}=-1)\n"
                src2 += f"    assert result is not None\n"
                results.append(GeneratedTest(
                    name=f"test_{prefix}_negative_{param.arg}",
                    source_code=src2,
                    target_function=name,
                    target_class=cls.name,
                    test_type="edge_case",
                    fixtures_needed=[inst],
                ))
        return results

    def _has_return(self, func: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> bool:
        """Check if function has a return statement with a value."""
        for node in ast.walk(func):
            if isinstance(node, ast.Return) and node.value is not None:
                return True
        return False

    def _infer_mocks(self, func: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> list[str]:
        """Infer which mocks are needed based on function body."""
        mocks: list[str] = []
        for node in ast.walk(func):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                        if node.func.value.id in ("self",):
                            continue
                        mocks.append(f"{node.func.value.id}.{node.func.attr}")
        return mocks

    def _get_type_name(self, annotation: ast.expr) -> str:
        """Get the string representation of a type annotation."""
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Subscript):
            if isinstance(annotation.value, ast.Name):
                return f"{annotation.value.id}[...]"
        elif isinstance(annotation, ast.Attribute):
            return annotation.attr
        elif isinstance(annotation, ast.Constant):
            return str(annotation.value)
        return "Any"


test_generator = TestGenerator()
