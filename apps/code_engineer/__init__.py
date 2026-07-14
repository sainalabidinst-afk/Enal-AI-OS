"""
Code Engineer
=============

Reference application #2: AI-powered code analysis and generation.
"""

from typing import Any
from apps.base import BaseReferenceApp
from apps.code_engineer.parser import code_parser, CodeAST
from apps.code_engineer.analyzer import code_analyzer, CodeIssue


class CodeEngineerApp(BaseReferenceApp):
    name = "code-engineer"
    version = "1.0.0"
    description = "AI-powered code analysis, review, and generation"
    category = "software-engineering"
    pipeline = ["perception", "memory", "reasoning", "decision", "action"]

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        from backend.app.core.adaptive_runtime import adaptive_runtime
        context = context or {}
        project_id = context.get("project_id", "code-engineer-default")
        result = await adaptive_runtime.execute(
            user_input,
            project_id=project_id,
            force_pipeline=self.pipeline,
        )
        return {
            "app": self.name,
            "version": self.version,
            "input": user_input,
            "result": result,
        }

    def parse_code(self, code: str, filename: str = "<unknown>") -> CodeAST:
        return code_parser.parse(code, filename=filename)

    def analyze_code(self, code: str, filename: str = "<unknown>") -> dict[str, Any]:
        code_ast = self.parse_code(code, filename)
        issues = code_analyzer.analyze(code_ast)
        return {
            "filename": filename,
            "functions": len(code_ast.functions),
            "classes": len(code_ast.classes),
            "issues": [
                {
                    "severity": issue.severity,
                    "category": issue.category,
                    "description": issue.description,
                    "recommendation": issue.recommendation,
                    "line": issue.line_number,
                    "confidence": issue.confidence,
                }
                for issue in issues
            ],
        }


def get_app() -> CodeEngineerApp:
    return CodeEngineerApp()
