"""
Refactoring Rules
===================

Rule-check functions for the RefactoringEngine.
Each function detects a specific code smell or anti-pattern.
"""

import ast

from apps.code_engineer.refactoring_models import (
    RefactoringCategory,
    RefactoringSeverity,
    RefactoringSuggestion,
)


def check_long_methods(tree: ast.Module, module_path: str, content: str) -> list[RefactoringSuggestion]:
    """Detect methods/functions that are too long."""
    suggestions: list[RefactoringSuggestion] = []
    lines = content.splitlines()

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            method_lines = node.end_lineno - node.lineno if node.end_lineno else 0
            if method_lines > 50:
                suggestions.append(RefactoringSuggestion(
                    category=RefactoringCategory.CODE_SMELL,
                    severity=RefactoringSeverity.MEDIUM,
                    module_path=module_path,
                    line_number=node.lineno,
                    description=f"Function '{node.name}' is {method_lines} lines long",
                    problem="Long functions are hard to understand, test, and maintain.",
                    suggestion=f"Split '{node.name}' into smaller functions of 10-20 lines each",
                    confidence=0.85,
                    effort="medium",
                    impact="medium",
                    example_before=f"# Line {node.lineno}: {method_lines} lines in one function",
                    example_after=f"# Consider: extract helper functions from the {method_lines}-line function",
                    references=["Clean Code: Functions should be small", "Single Responsibility Principle"],
                ))
    return suggestions


def check_too_many_params(tree: ast.Module, module_path: str) -> list[RefactoringSuggestion]:
    """Detect functions with too many parameters."""
    suggestions: list[RefactoringSuggestion] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = node.args.args
            if len(args) > 5:
                suggestions.append(RefactoringSuggestion(
                    category=RefactoringCategory.CODE_SMELL,
                    severity=RefactoringSeverity.MEDIUM,
                    module_path=module_path,
                    line_number=node.lineno,
                    description=f"Function '{node.name}' has {len(args)} parameters",
                    problem="Too many parameters makes functions hard to call and test.",
                    suggestion="Consider using a dataclass/object to group parameters, or split the function",
                    confidence=0.9,
                    effort="medium",
                    impact="medium",
                    example_before=f"def {node.name}({', '.join(a.arg for a in args[:7])}...):",
                    example_after=f"# @dataclass\n# class {node.name.title()}Params:\n#     ...\n# def {node.name}(params: {node.name.title()}Params):",
                ))
    return suggestions


def check_long_class(tree: ast.Module, module_path: str) -> list[RefactoringSuggestion]:
    """Detect classes that are too large."""
    suggestions: list[RefactoringSuggestion] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            num_methods = sum(1 for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)))
            if num_methods > 15:
                suggestions.append(RefactoringSuggestion(
                    category=RefactoringCategory.CODE_SMELL,
                    severity=RefactoringSeverity.MEDIUM,
                    module_path=module_path,
                    line_number=node.lineno,
                    description=f"Class '{node.name}' has {num_methods} methods",
                    problem="Large classes violate Single Responsibility Principle.",
                    suggestion=f"Consider splitting '{node.name}' into smaller focused classes",
                    confidence=0.75,
                    effort="high",
                    impact="high",
                    references=["Clean Code: Classes should be small", "Single Responsibility Principle"],
                ))
    return suggestions


def check_missing_type_hints(tree: ast.Module, module_path: str, content: str) -> list[RefactoringSuggestion]:
    """Detect functions missing type hints."""
    suggestions: list[RefactoringSuggestion] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("__") and node.name.endswith("__"):
                continue

            missing = False
            if not node.returns:
                missing = True

            for arg in node.args.args:
                if arg.arg in ("self", "cls"):
                    continue
                if not arg.annotation:
                    missing = True
                    break

            if missing:
                suggestions.append(RefactoringSuggestion(
                    category=RefactoringCategory.TYPE_HINT,
                    severity=RefactoringSeverity.LOW,
                    module_path=module_path,
                    line_number=node.lineno,
                    description=f"Function '{node.name}' is missing type hints",
                    problem="Without type hints, code is harder to understand and type checkers can't validate.",
                    suggestion=f"Add type hints to '{node.name}' parameters and return type",
                    confidence=0.9,
                    effort="low",
                    impact="medium",
                    example_before=f"def {node.name}(...):  # no type hints",
                    example_after=f"def {node.name}(...) -> ReturnType:  # with type hints",
                ))
    return suggestions


def check_too_many_returns(tree: ast.Module, module_path: str) -> list[RefactoringSuggestion]:
    """Detect functions with too many return statements."""
    suggestions: list[RefactoringSuggestion] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            returns = [n for n in ast.walk(node) if isinstance(n, ast.Return)]
            if len(returns) > 3:
                suggestions.append(RefactoringSuggestion(
                    category=RefactoringCategory.CODE_SMELL,
                    severity=RefactoringSeverity.LOW,
                    module_path=module_path,
                    line_number=node.lineno,
                    description=f"Function '{node.name}' has {len(returns)} return statements",
                    problem="Multiple return points make control flow harder to follow.",
                    suggestion="Consider using a single exit point or guard clauses more consistently",
                    confidence=0.6,
                    effort="low",
                    impact="low",
                ))
    return suggestions


def check_deep_nesting(tree: ast.Module, module_path: str) -> list[RefactoringSuggestion]:
    """Detect deeply nested code blocks."""
    suggestions: list[RefactoringSuggestion] = []

    class NestingVisitor(ast.NodeVisitor):
        def __init__(self):
            self.depth = 0
            self.max_depth = 0
            self.deep_nodes: list[tuple[int, int]] = []

        def visit(self, node: ast.AST) -> None:
            self.depth += 1
            lineno = getattr(node, 'lineno', 0)
            if self.depth > 4 and lineno > 0:
                self.deep_nodes.append((self.depth, lineno))
            self.max_depth = max(self.max_depth, self.depth)
            self.generic_visit(node)
            self.depth -= 1

    visitor = NestingVisitor()
    visitor.visit(tree)

    for depth, lineno in visitor.deep_nodes[:5]:
        suggestions.append(RefactoringSuggestion(
            category=RefactoringCategory.CODE_SMELL,
            severity=RefactoringSeverity.MEDIUM,
            module_path=module_path,
            line_number=lineno,
            description=f"Deep nesting (level {depth}) at line {lineno}",
            problem="Deeply nested code is hard to read and maintain.",
            suggestion="Use early returns, guard clauses, or extract nested blocks into separate functions",
            confidence=0.8,
            effort="medium",
            impact="medium",
            references=["Clean Code: Avoid Deep Nesting", "Guard Clauses pattern"],
        ))
    return suggestions


def check_magic_numbers(tree: ast.Module, module_path: str, content: str) -> list[RefactoringSuggestion]:
    """Detect magic numbers in code."""
    suggestions: list[RefactoringSuggestion] = []
    allowed_values = {0, 1, -1, 0.0, 1.0, -1.0, 100, 1000, 2, 3, 4, 5}

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            if node.value in allowed_values:
                continue
            if isinstance(node.value, int) and abs(node.value) <= 5:
                continue
            suggestions.append(RefactoringSuggestion(
                category=RefactoringCategory.CODE_SMELL,
                severity=RefactoringSeverity.LOW,
                module_path=module_path,
                line_number=node.lineno,
                description=f"Magic number '{node.value}' at line {node.lineno}",
                problem="Magic numbers make code harder to understand and maintain.",
                suggestion=f"Replace '{node.value}' with a named constant",
                confidence=0.7,
                effort="low",
                impact="low",
                example_before=f"if x > {node.value}:",
                example_after=f"# MAX_RETRIES = {node.value}\n# if x > MAX_RETRIES:",
            ))
    return suggestions


def check_duplicate_code(tree: ast.Module, module_path: str, content: str) -> list[RefactoringSuggestion]:
    """Detect duplicate or very similar code blocks."""
    suggestions: list[RefactoringSuggestion] = []
    lines = content.splitlines()

    func_bodies: list[tuple[str, int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body_start = node.lineno
            body_lines = lines[node.lineno:node.end_lineno] if node.end_lineno else []
            body_text = "\n".join(body_lines) if body_lines else ""
            if body_text:
                func_bodies.append((node.name, body_start, body_text))

    for i, (name1, start1, body1) in enumerate(func_bodies):
        for j, (name2, start2, body2) in enumerate(func_bodies):
            if j <= i:
                continue
            lines1 = {l.strip() for l in body1.split('\n') if l.strip() and not l.strip().startswith('#')}
            lines2 = {l.strip() for l in body2.split('\n') if l.strip() and not l.strip().startswith('#')}
            if not lines1 or not lines2:
                continue

            intersection = lines1 & lines2
            union = lines1 | lines2
            similarity = len(intersection) / len(union) if union else 0

            if similarity > 0.6:
                suggestions.append(RefactoringSuggestion(
                    category=RefactoringCategory.CODE_SMELL,
                    severity=RefactoringSeverity.MEDIUM,
                    module_path=module_path,
                    line_number=start1,
                    description=f"Duplicate code in '{name1}' (line {start1}) and '{name2}' (line {start2})",
                    problem=f"Code duplication ({similarity:.0%} similarity) increases maintenance cost.",
                    suggestion="Extract common logic into a shared helper function",
                    confidence=min(0.9, similarity),
                    effort="medium",
                    impact="medium",
                    references=["DRY (Don't Repeat Yourself) Principle"],
                ))
    return suggestions


def check_large_module(tree: ast.Module, module_path: str, repo_path: str) -> list[RefactoringSuggestion]:
    """Detect modules that are too large."""
    suggestions: list[RefactoringSuggestion] = []

    try:
        from pathlib import Path
        full_path = Path(repo_path) / module_path
        if full_path.exists():
            total_lines = len(full_path.read_text(encoding="utf-8").splitlines())
        else:
            return suggestions

        if total_lines > 500:
            suggestions.append(RefactoringSuggestion(
                category=RefactoringCategory.CODE_SMELL,
                severity=RefactoringSeverity.HIGH,
                module_path=module_path,
                line_number=1,
                description=f"Module '{module_path}' is {total_lines} lines long",
                problem="Large modules violate Single Responsibility Principle and become unmanageable.",
                suggestion="Split into smaller modules (aim for <300 lines per module)",
                confidence=0.8,
                effort="high",
                impact="high",
                references=["Clean Code: Modules should be small", "Single Responsibility Principle"],
            ))
        return suggestions
    except Exception:
        return suggestions


def check_string_concat(tree: ast.Module, module_path: str, content: str) -> list[RefactoringSuggestion]:
    """Detect string concatenation that should use f-strings."""
    suggestions: list[RefactoringSuggestion] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            if isinstance(node.left, (ast.Constant, ast.BinOp)) and isinstance(node.right, (ast.Constant, ast.BinOp)):
                has_string = any(
                    isinstance(n, ast.Constant) and isinstance(n.value, str)
                    for n in (node.left, node.right) if isinstance(n, ast.Constant)
                )
                if has_string:
                    suggestions.append(RefactoringSuggestion(
                        category=RefactoringCategory.STYLE,
                        severity=RefactoringSeverity.LOW,
                        module_path=module_path,
                        line_number=node.lineno,
                        description="String concatenation detected",
                        problem="String concatenation is less readable and slower than f-strings.",
                        suggestion="Use f-strings instead of concatenation",
                        confidence=0.85,
                        effort="low",
                        impact="low",
                        example_before='result = var1 + " " + var2',
                        example_after='result = f"{var1} {var2}"',
                    ))
    return suggestions


def check_single_letter_vars(tree: ast.Module, module_path: str) -> list[RefactoringSuggestion]:
    """Detect single-letter variable names (except i, j, k in loops)."""
    suggestions: list[RefactoringSuggestion] = []

    class VarVisitor(ast.NodeVisitor):
        def __init__(self):
            self.loop_vars: set[str] = set()

        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Store):
                if len(node.id) == 1 and node.id.isalpha() and node.id not in ('i', 'j', 'k'):
                    if node.id not in self.loop_vars:
                        suggestions.append(RefactoringSuggestion(
                            category=RefactoringCategory.STYLE,
                            severity=RefactoringSeverity.LOW,
                            module_path=module_path,
                            line_number=node.lineno,
                            description=f"Single-letter variable '{node.id}'",
                            problem="Single-letter names don't convey meaning.",
                            suggestion=f"Rename '{node.id}' to a descriptive name",
                            confidence=0.8,
                            effort="low",
                            impact="low",
                        ))

        def visit_For(self, node):
            if isinstance(node.target, ast.Name) and len(node.target.id) == 1:
                self.loop_vars.add(node.target.id)
            self.generic_visit(node)

    visitor = VarVisitor()
    visitor.visit(tree)
    return suggestions


def check_commented_code(tree: ast.Module, module_path: str, content: str) -> list[RefactoringSuggestion]:
    """Detect commented-out code."""
    suggestions: list[RefactoringSuggestion] = []
    lines = content.splitlines()

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#") and not stripped.startswith("# "):
            code_patterns = ["def ", "class ", "import ", "return ", "if ", "for ", "while ", "with ", "try:", "except"]
            if any(p in stripped for p in code_patterns):
                suggestions.append(RefactoringSuggestion(
                    category=RefactoringCategory.CODE_SMELL,
                    severity=RefactoringSeverity.INFO,
                    module_path=module_path,
                    line_number=i,
                    description=f"Commented-out code at line {i}",
                    problem="Commented-out code becomes stale and confuses readers.",
                    suggestion="Remove dead code. Use version control for history.",
                    confidence=0.6,
                    effort="low",
                    impact="low",
                ))
                break
    return suggestions


def check_mutable_defaults(tree: ast.Module, module_path: str) -> list[RefactoringSuggestion]:
    """Detect mutable default arguments."""
    suggestions: list[RefactoringSuggestion] = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    suggestions.append(RefactoringSuggestion(
                        category=RefactoringCategory.BEST_PRACTICE,
                        severity=RefactoringSeverity.HIGH,
                        module_path=module_path,
                        line_number=node.lineno,
                        description=f"Mutable default argument in '{node.name}'",
                        problem="Mutable defaults are shared across all calls, causing unexpected behavior.",
                        suggestion="Use None as default and create a new instance inside the function",
                        confidence=0.95,
                        effort="low",
                        impact="high",
                        example_before=f"def {node.name}(arg=[]):",
                        example_after=f"def {node.name}(arg=None):\n    if arg is None:\n        arg = []",
                        references=["Python anti-pattern: Mutable default arguments"],
                    ))
    return suggestions


def check_bare_excepts(tree: ast.Module, module_path: str) -> list[RefactoringSuggestion]:
    """Detect bare except clauses."""
    suggestions: list[RefactoringSuggestion] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            for handler in node.handlers:
                if handler.type is None:
                    suggestions.append(RefactoringSuggestion(
                        category=RefactoringCategory.BEST_PRACTICE,
                        severity=RefactoringSeverity.HIGH,
                        module_path=module_path,
                        line_number=handler.lineno,
                        description="Bare 'except:' clause",
                        problem="Bare except catches unexpected exceptions like KeyboardInterrupt.",
                        suggestion="Use 'except Exception:' or specify the exact exception type",
                        confidence=0.95,
                        effort="low",
                        impact="medium",
                        example_before="except:",
                        example_after="except Exception:  # or specific exception",
                        references=["Python anti-pattern: Bare except"],
                    ))
    return suggestions


def check_suggest_design_pattern(tree: ast.Module, module_path: str, content: str) -> list[RefactoringSuggestion]:
    """Suggest design patterns based on code structure."""
    suggestions: list[RefactoringSuggestion] = []
    lines = content.splitlines()

    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            chain_len = 0
            current = node
            while isinstance(current, ast.If):
                chain_len += 1
                el = current.orelse
                if el and isinstance(el[0], ast.If):
                    current = el[0]
                else:
                    break

            if chain_len > 4:
                suggestions.append(RefactoringSuggestion(
                    category=RefactoringCategory.DESIGN_PATTERN,
                    severity=RefactoringSeverity.MEDIUM,
                    module_path=module_path,
                    line_number=node.lineno,
                    description=f"Long if-elif chain ({chain_len} conditions)",
                    problem="Long conditional chains violate Open/Closed Principle.",
                    suggestion="Consider using Strategy pattern or a dictionary dispatch",
                    confidence=0.7,
                    effort="medium",
                    impact="high",
                    example_before=f"# Line {node.lineno}: {chain_len} conditions",
                    example_after="# strategies = {'type1': handler1, 'type2': handler2}\n# result = strategies[type]()",
                    references=["Strategy Design Pattern", "Open/Closed Principle"],
                ))
                break

    return suggestions
