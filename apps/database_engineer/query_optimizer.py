"""
Database Engineer — Query Optimizer.

Analyzes SQL queries for performance issues and produces
optimized versions with execution plan recommendations.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from apps.database_engineer.schemas import Finding, Severity, FindingCategory

logger = logging.getLogger(__name__)


# Anti-patterns that indicate slow queries.
_SLOW_PATTERNS: list[tuple[str, str, Severity, str]] = [
    (r'(?i)select\s+\*', "SELECT * retrieves all columns", Severity.medium, "Specify only required columns"),
    (r'(?i)like\s+[\'"]%', "Leading wildcard LIKE prevents index usage", Severity.high, "Avoid leading wildcards; use full-text search"),
    (r'(?i)order\s+by\s+\w+\s+asc', "ORDER BY without LIMIT on large tables", Severity.medium, "Add LIMIT or ensure index covers ORDER BY"),
    (r'(?i)group\s+by\s+.*order\s+by', "GROUP BY with ORDER BY may require temp table", Severity.low, "Consider covering index"),
    (r'(?i)join\s+\w+\s+on\s+\w+\.\w+\s*=\s*\w+\.\w+(?!\s+and)', "JOIN without WHERE filter may produce large result sets", Severity.low, "Add WHERE clause or LIMIT"),
    (r'(?i)not\s+in\s*\(', "NOT IN with subquery may be slow", Severity.high, "Use NOT EXISTS or LEFT JOIN ... IS NULL"),
    (r'(?i)or\s+\w+\.\w+\s*=\s*\w+\.\w+.*or\s+\w+\.\w+\s*=\s*\w+\.\w+', "Multiple OR conditions may prevent index usage", Severity.medium, "Consider UNION or separate queries"),
    (r'(?i)count\s*\(\s*\*\s*\)', "COUNT(*) without WHERE on large table", Severity.low, "Ensure proper WHERE clause or use estimate for large tables"),
    (r'(?i)distinct\s+\w+', "DISTINCT may indicate data quality issue or need for index", Severity.low, "Review need for DISTINCT; add index if required"),
    (r'(?i)having\s+', "HAVING without GROUP BY", Severity.low, "Move conditions to WHERE clause if no aggregation"),
]


class QueryOptimizer:
    """
    Analyzes and optimizes SQL queries.

    Usage::

        optimizer = QueryOptimizer()
        result = optimizer.optimize(queries, database_type)
    """

    def optimize(
        self,
        queries: list[str],
        database_type: Any = "postgresql",
    ) -> dict[str, Any]:
        """
        Analyze and optimize a list of SQL queries.

        Args:
            queries: List of SQL query strings.
            database_type: Target database type.

        Returns:
            Dict with findings and optimized queries.
        """
        findings: list[Finding] = []
        optimized: list[str] = []

        for i, query in enumerate(queries):
            query_findings = self._analyze_query(query, i)
            findings.extend(query_findings)
            optimized.append(self._optimize_query(query, query_findings))

        return {
            "findings": findings,
            "optimized_queries": optimized,
        }

    def _analyze_query(self, query: str, index: int) -> list[Finding]:
        """Analyze a single query for performance issues."""
        findings: list[Finding] = []
        seen: set[str] = set()

        for pattern, description, severity, _ in _SLOW_PATTERNS:
            if re.search(pattern, query):
                key = f"{pattern}:{description}"
                if key not in seen:
                    seen.add(key)
                    findings.append(Finding(
                        category=FindingCategory.query_performance,
                        severity=severity,
                        title=f"Query {index + 1}: {description}",
                        description=f"Query: {query[:200]}...",
                        evidence={"query": query, "pattern": pattern},
                        recommendation=self._get_recommendation(pattern),
                        confidence=0.85,
                    ))

        # Check for missing WHERE clause on large tables (heuristic).
        if re.search(r'(?i)select\s+.*\bfrom\s+\w+', query) and not re.search(r'(?i)\bwhere\b', query):
            if "limit" not in query.lower():
                findings.append(Finding(
                    category=FindingCategory.query_performance,
                    severity=Severity.medium,
                    title=f"Query {index + 1}: Missing WHERE clause",
                    description="Query may scan entire table without filtering.",
                    evidence={"query": query},
                    recommendation="Add WHERE clause to limit rows scanned",
                    confidence=0.8,
                ))

        return findings

    def _optimize_query(self, query: str, findings: list[Finding]) -> str:
        """Produce an optimized version of the query."""
        optimized = query

        # Replace SELECT * with specific columns if possible.
        if any("SELECT *" in f.title for f in findings):
            # Heuristic: suggest removing * (actual column selection requires schema).
            optimized = optimized.replace("SELECT *", "SELECT col1, col2, col3  -- specify columns")

        # Add LIMIT if missing for non-aggregate queries.
        if any("Missing WHERE" in f.title for f in findings):
            if "LIMIT" not in optimized.upper() and "GROUP BY" not in optimized.upper():
                optimized = optimized.rstrip(";") + " LIMIT 1000"

        return optimized

    def _get_recommendation(self, pattern: str) -> str:
        """Get optimization recommendation for a pattern."""
        recommendations = {
            r'(?i)select\s+\*': "Replace SELECT * with explicit column list",
            r'(?i)like\s+[\'"]%': "Use full-text search or trigram index instead of leading wildcard LIKE",
            r'(?i)not\s+in\s*\(': "Use NOT EXISTS or LEFT JOIN ... IS NULL for better performance",
            r'(?i)or\s+\w+\.\w+': "Consider UNION ALL or separate queries with individual indexes",
        }
        for pat, rec in recommendations.items():
            if re.search(pat, pattern):
                return rec
        return "Review query execution plan and add appropriate indexes"
