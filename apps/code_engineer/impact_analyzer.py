"""
Impact Analyzer
=================

Change propagation analysis for Python repositories.
Determines which modules, functions, classes, and tests are affected by a change.

Features:
- Change propagation engine
- Affected function/class/module detection
- Test impact prediction
- Risk scoring for changes
"""

import ast
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class ChangeType:
    ADDED = "added"
    MODIFIED = "modified"
    REMOVED = "removed"
    SIGNATURE_CHANGED = "signature_changed"
    TYPE_CHANGED = "type_changed"
    DEPENDENCY_CHANGED = "dependency_changed"


class ImpactSeverity:
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


@dataclass
class Change:
    """Representation of a code change."""
    module_path: str
    change_type: str
    target_name: str  # Function, class, or module name
    target_type: str  # "function", "class", "module", "import"
    line_number: int = 0
    description: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ImpactedItem:
    """An item impacted by a change."""
    module_path: str
    item_name: str
    item_type: str  # "function", "class", "module"
    impact_type: str  # "direct", "transitive", "test"
    severity: str
    confidence: float  # 0.0 - 1.0
    reason: str = ""
    line_number: int = 0


@dataclass
class ImpactAnalysisResult:
    """Complete impact analysis result."""
    changes: list[Change] = field(default_factory=list)
    impacted_items: list[ImpactedItem] = field(default_factory=list)
    impacted_tests: list[str] = field(default_factory=list)
    total_impacted: int = 0
    total_tests_impacted: int = 0
    max_severity: str = ImpactSeverity.NONE
    risk_score: float = 0.0  # 0.0 - 1.0
    recommended_actions: list[str] = field(default_factory=list)
    summary: str = ""


class ImpactAnalyzer:
    """Analyzes the impact of code changes across a repository."""

    def __init__(self, repo_path: str | Path):
        self.repo_path = Path(repo_path)
        self._module_ast_cache: dict[str, ast.Module] = {}

    async def analyze_changes(
        self,
        changes: list[Change],
        dependency_summary=None,
    ) -> ImpactAnalysisResult:
        """Analyze impact of a list of changes."""
        result = ImpactAnalysisResult(changes=changes)
        impacted: list[ImpactedItem] = []

        for change in changes:
            items = await self._analyze_single_change(change, dependency_summary)
            impacted.extend(items)

        # Deduplicate
        seen = set()
        unique_impacted = []
        for item in impacted:
            key = (item.module_path, item.item_name, item.impact_type)
            if key not in seen:
                seen.add(key)
                unique_impacted.append(item)
        result.impacted_items = unique_impacted

        # Extract impacted tests
        result.impacted_tests = list(set(
            item.module_path for item in unique_impacted
            if item.item_type == "test"
        ))

        # Compute stats
        result.total_impacted = len(unique_impacted)
        result.total_tests_impacted = len(result.impacted_tests)

        # Determine max severity
        severity_order = [ImpactSeverity.NONE, ImpactSeverity.LOW, ImpactSeverity.MEDIUM, ImpactSeverity.HIGH, ImpactSeverity.CRITICAL]
        max_sev = ImpactSeverity.NONE
        for item in unique_impacted:
            if severity_order.index(item.severity) > severity_order.index(max_sev):
                max_sev = item.severity
        result.max_severity = max_sev

        # Compute risk score
        result.risk_score = self._compute_risk_score(unique_impacted, len(changes))

        # Generate recommended actions
        result.recommended_actions = self._generate_recommendations(result)

        # Generate summary
        result.summary = self._generate_summary(result)

        return result

    async def _analyze_single_change(
        self,
        change: Change,
        dependency_summary=None,
    ) -> list[ImpactedItem]:
        """Analyze impact of a single change."""
        impacted: list[ImpactedItem] = []

        # Get the module AST
        tree = await self._get_ast(change.module_path)
        if tree is None:
            return impacted

        if change.target_type == "function":
            impacted.extend(self._analyze_function_impact(change, tree))
        elif change.target_type == "class":
            impacted.extend(self._analyze_class_impact(change, tree))
        elif change.target_type == "module":
            impacted.extend(self._analyze_module_impact(change, tree))
        elif change.target_type == "import":
            impacted.extend(self._analyze_import_impact(change, tree))

        # Add transitive impact from dependency graph
        if dependency_summary and hasattr(dependency_summary, 'modules'):
            trans = self._get_transitive_impact(change.module_path, dependency_summary)
            impacted.extend(trans)

        return impacted

    def _analyze_function_impact(self, change: Change, tree: ast.Module) -> list[ImpactedItem]:
        """Analyze impact of a function change."""
        impacted: list[ImpactedItem] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Same function?
                if node.name == change.target_name:
                    for caller_node in ast.walk(tree):
                        if isinstance(caller_node, ast.Call):
                            if isinstance(caller_node.func, ast.Name) and caller_node.func.id == change.target_name:
                                impacted.append(ImpactedItem(
                                    module_path=change.module_path,
                                    item_name=f"{change.target_name}() caller",
                                    item_type="function",
                                    impact_type="direct",
                                    severity=self._severity_for_change(change),
                                    confidence=0.9,
                                    reason=f"Calls modified function {change.target_name}()",
                                    line_number=caller_node.lineno,
                                ))
                    break

                # Methods in classes
                for cls_node in ast.walk(tree):
                    if isinstance(cls_node, ast.ClassDef):
                        for method in cls_node.body:
                            if isinstance(method, ast.FunctionDef) and method.name == change.target_name:
                                # All usages of this class method
                                impacted.append(ImpactedItem(
                                    module_path=change.module_path,
                                    item_name=f"{cls_node.name}.{change.target_name}()",
                                    item_type="function",
                                    impact_type="direct",
                                    severity=self._severity_for_change(change),
                                    confidence=0.85,
                                    reason=f"Method {change.target_name} in class {cls_node.name} modified",
                                ))

        return impacted

    def _analyze_class_impact(self, change: Change, tree: ast.Module) -> list[ImpactedItem]:
        """Analyze impact of a class change."""
        impacted: list[ImpactedItem] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == change.target_name:
                # Impact on subclasses and usages
                for other_node in ast.walk(tree):
                    if isinstance(other_node, ast.ClassDef) and other_node != node:
                        for base in other_node.bases:
                            if isinstance(base, ast.Name) and base.id == change.target_name:
                                impacted.append(ImpactedItem(
                                    module_path=change.module_path,
                                    item_name=other_node.name,
                                    item_type="class",
                                    impact_type="direct",
                                    severity=ImpactSeverity.HIGH,
                                    confidence=0.9,
                                    reason=f"Inherits from modified class {change.target_name}",
                                ))
                break

        return impacted

    def _analyze_module_impact(self, change: Change, tree: ast.Module) -> list[ImpactedItem]:
        """Analyze impact of a module-level change."""
        impacted: list[ImpactedItem] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if change.target_name in alias.name or (change.module_path and change.module_path in str(alias.name)):
                        impacted.append(ImpactedItem(
                            module_path=change.module_path,
                            item_name=alias.name,
                            item_type="module",
                            impact_type="direct",
                            severity=ImpactSeverity.HIGH,
                            confidence=0.8,
                            reason=f"Depends on modified module {change.module_path}",
                        ))
            elif isinstance(node, ast.ImportFrom):
                if node.module and (change.target_name in node.module or change.module_path in str(node.module)):
                    for alias in node.names:
                        impacted.append(ImpactedItem(
                            module_path=change.module_path,
                            item_name=f"{node.module}.{alias.name}",
                            item_type="function",
                            impact_type="direct",
                            severity=ImpactSeverity.HIGH,
                            confidence=0.8,
                            reason=f"Imports from modified module {change.module_path}",
                        ))

        return impacted

    def _analyze_import_impact(self, change: Change, tree: ast.Module) -> list[ImpactedItem]:
        """Analyze impact of an import change."""
        impacted: list[ImpactedItem] = []
        # Any usage of the removed/changed import
        for node in ast.walk(tree):
            # Check for usage of the imported name
            for child in ast.walk(node):
                if isinstance(child, ast.Name) and child.id == change.target_name:
                    impacted.append(ImpactedItem(
                        module_path=change.module_path,
                        item_name=child.id,
                        item_type="module",
                        impact_type="direct",
                        severity=ImpactSeverity.CRITICAL if change.change_type == ChangeType.REMOVED else ImpactSeverity.HIGH,
                        confidence=0.95,
                        reason=f"Uses {change.target_name} which was {change.change_type}",
                        line_number=child.lineno,
                    ))
        return impacted

    def _get_transitive_impact(self, module_path: str, dep_summary) -> list[ImpactedItem]:
        """Get transitive impact from dependency graph."""
        impacted: list[ImpactedItem] = []
        if module_path not in dep_summary.modules:
            return impacted

        mod_info = dep_summary.modules[module_path]
        for dependent in mod_info.dependents:
            impacted.append(ImpactedItem(
                module_path=dependent,
                item_name=Path(dependent).stem,
                item_type="module",
                impact_type="transitive",
                severity=ImpactSeverity.MEDIUM,
                confidence=0.6,
                reason=f"Transitively depends on changed module {module_path}",
            ))

            # If dependent is a test, tag it
            if "test" in dependent.lower():
                impacted.append(ImpactedItem(
                    module_path=dependent,
                    item_name=Path(dependent).stem,
                    item_type="test",
                    impact_type="transitive",
                    severity=ImpactSeverity.MEDIUM,
                    confidence=0.7,
                    reason=f"Test for module affected by changes to {module_path}",
                ))

        return impacted

    def _severity_for_change(self, change: Change) -> str:
        """Map change type to severity."""
        mapping = {
            ChangeType.REMOVED: ImpactSeverity.CRITICAL,
            ChangeType.SIGNATURE_CHANGED: ImpactSeverity.HIGH,
            ChangeType.TYPE_CHANGED: ImpactSeverity.HIGH,
            ChangeType.MODIFIED: ImpactSeverity.MEDIUM,
            ChangeType.DEPENDENCY_CHANGED: ImpactSeverity.HIGH,
            ChangeType.ADDED: ImpactSeverity.LOW,
        }
        return mapping.get(change.change_type, ImpactSeverity.MEDIUM)

    def _compute_risk_score(self, impacted: list[ImpactedItem], num_changes: int) -> float:
        """Compute overall risk score from impact analysis."""
        if not impacted:
            return 0.0

        # Weight factors
        critical_count = sum(1 for i in impacted if i.severity == ImpactSeverity.CRITICAL)
        high_count = sum(1 for i in impacted if i.severity == ImpactSeverity.HIGH)
        medium_count = sum(1 for i in impacted if i.severity == ImpactSeverity.MEDIUM)

        total_weighted = (critical_count * 10 + high_count * 5 + medium_count * 2)
        max_possible = len(impacted) * 10

        # Normalize to 0-1
        risk = min(1.0, total_weighted / max_possible) if max_possible > 0 else 0.0

        # Scale by number of changes (more changes = higher risk)
        change_factor = min(1.0, num_changes / 10)
        risk = risk * 0.7 + change_factor * 0.3

        return round(risk, 3)

    def _generate_recommendations(self, result: ImpactAnalysisResult) -> list[str]:
        """Generate recommended actions based on impact analysis."""
        recommendations = []

        if result.max_severity in (ImpactSeverity.CRITICAL, ImpactSeverity.HIGH):
            recommendations.append("⚠️  High-risk change detected. Consider splitting into smaller changes.")

        if result.total_tests_impacted > 0:
            recommendations.append(f"🧪 Run {result.total_tests_impacted} impacted test(s) after applying changes.")

        if result.risk_score > 0.5:
            recommendations.append("🔍 Risk score is above 0.5. Consider adding more tests before deployment.")

        if any(i.impact_type == "transitive" for i in result.impacted_items):
            recommendations.append("📦 Transitive dependencies affected. Verify integration points.")

        if not recommendations:
            recommendations.append("✅ Low-risk change. No special actions required.")

        return recommendations

    def _generate_summary(self, result: ImpactAnalysisResult) -> str:
        """Generate human-readable summary."""
        lines = [
            "# Impact Analysis Summary",
            "",
            f"**Changes**: {len(result.changes)}",
            f"**Impacted Items**: {result.total_impacted}",
            f"**Impacted Tests**: {result.total_tests_impacted}",
            f"**Max Severity**: {result.max_severity}",
            f"**Risk Score**: {result.risk_score:.1%}",
            "",
        ]

        # Group by severity
        for severity in [ImpactSeverity.CRITICAL, ImpactSeverity.HIGH, ImpactSeverity.MEDIUM, ImpactSeverity.LOW]:
            items = [i for i in result.impacted_items if i.severity == severity]
            if items:
                lines.append(f"## {severity.upper()} ({len(items)})")
                for item in items[:10]:
                    lines.append(f"- [{item.impact_type}] {item.module_path}: {item.reason}")
                if len(items) > 10:
                    lines.append(f"  ... and {len(items) - 10} more")
                lines.append("")

        return "\n".join(lines)

    async def _get_ast(self, module_path: str) -> Optional[ast.Module]:
        """Get cached AST for a module."""
        if module_path in self._module_ast_cache:
            return self._module_ast_cache[module_path]

        full_path = self.repo_path / module_path
        if not full_path.exists():
            return None

        try:
            content = full_path.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=module_path)
            self._module_ast_cache[module_path] = tree
            return tree
        except SyntaxError:
            logger.warning(f"Syntax error in {module_path}")
            return None
        except Exception as e:
            logger.error(f"Error reading {module_path}: {e}")
            return None

    def create_change(
        self,
        module_path: str,
        change_type: str,
        target_name: str,
        target_type: str = "function",
        line_number: int = 0,
        description: str = "",
    ) -> Change:
        """Helper to create a Change object."""
        return Change(
            module_path=module_path,
            change_type=change_type,
            target_name=target_name,
            target_type=target_type,
            line_number=line_number,
            description=description,
        )

