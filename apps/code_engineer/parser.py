"""
Code Engineer Parser
=====================

Parses Python code into a universal AST.
"""

import ast
import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class CodeFunction:
    name: str
    lineno: int
    args: list[str] = field(default_factory=list)
    decorators: list[str] = field(default_factory=list)
    docstring: str = ""
    is_async: bool = False


@dataclass
class CodeClass:
    name: str
    lineno: int
    bases: list[str] = field(default_factory=list)
    methods: list[CodeFunction] = field(default_factory=list)
    decorators: list[str] = field(default_factory=list)
    docstring: str = ""


@dataclass
class CodeImport:
    module: str
    names: list[str] = field(default_factory=list)
    alias: str = ""


@dataclass
class CodeAST:
    vendor: str = "python"
    functions: list[CodeFunction] = field(default_factory=list)
    classes: list[CodeClass] = field(default_factory=list)
    imports: list[CodeImport] = field(default_factory=list)
    raw_lines: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def system_identity(self):
        class _Identity:
            def __init__(self, name):
                self.name = name
        return _Identity(self.metadata.get("filename", "unknown"))

    @property
    def errors(self):
        return self.metadata.get("parser_errors", [])


class CodeParser:
    """Parses Python code into Universal Code AST."""

    def parse(self, code_text: str, filename: str = "<unknown>") -> CodeAST:
        ast_obj = CodeAST(vendor="python", metadata={"filename": filename})
        ast_obj.raw_lines = code_text.splitlines()

        try:
            tree = ast.parse(code_text, filename=filename)
        except SyntaxError as e:
            ast_obj.metadata["parser_errors"] = [f"Syntax error: {e}"]
            return ast_obj

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                func = CodeFunction(
                    name=node.name,
                    lineno=node.lineno,
                    args=[arg.arg for arg in node.args.args],
                    decorators=[self._get_decorator_name(d) for d in node.decorator_list],
                    docstring=ast.get_docstring(node) or "",
                    is_async=isinstance(node, ast.AsyncFunctionDef),
                )
                ast_obj.functions.append(func)
            elif isinstance(node, ast.ClassDef):
                cls = CodeClass(
                    name=node.name,
                    lineno=node.lineno,
                    bases=[self._get_name(b) for b in node.bases],
                    decorators=[self._get_decorator_name(d) for d in node.decorator_list],
                    docstring=ast.get_docstring(node) or "",
                )
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        method = CodeFunction(
                            name=item.name,
                            lineno=item.lineno,
                            args=[arg.arg for arg in item.args.args],
                            decorators=[self._get_decorator_name(d) for d in item.decorator_list],
                            docstring=ast.get_docstring(item) or "",
                            is_async=isinstance(item, ast.AsyncFunctionDef),
                        )
                        cls.methods.append(method)
                ast_obj.classes.append(cls)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    ast_obj.imports.append(CodeImport(module=alias.name, alias=alias.asname or ""))
            elif isinstance(node, ast.ImportFrom):
                names = [alias.name for alias in node.names]
                ast_obj.imports.append(CodeImport(module=node.module or "", names=names))

        logger.info("Parsed %s: %d functions, %d classes", filename, len(ast_obj.functions), len(ast_obj.classes))
        return ast_obj

    def _get_name(self, node: ast.expr) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return "unknown"

    def _get_decorator_name(self, node: ast.expr) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            return node.func.id
        return "unknown"


code_parser = CodeParser()
