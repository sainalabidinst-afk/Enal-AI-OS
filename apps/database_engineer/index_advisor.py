"""
Database Engineer — Index Advisor.

Recommends indexes based on query patterns, schema, and workload profile.
Prioritizes indexes by estimated impact.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from apps.database_engineer.schemas import (
    SchemaDefinition,
    TableDefinition,
    WorkloadProfile,
    IndexRecommendation,
    Severity,
    FindingCategory,
)

logger = logging.getLogger(__name__)


class IndexAdvisor:
    """
    Recommends indexes based on query patterns and workload.

    Usage::

        advisor = IndexAdvisor()
        recs = advisor.recommend(queries, schema, workload_profile)
    """

    def recommend(
        self,
        queries: list[str],
        schema: SchemaDefinition | None,
        workload: WorkloadProfile | None = None,
    ) -> list[IndexRecommendation]:
        """
        Generate index recommendations.

        Args:
            queries: List of SQL queries.
            schema: Current schema definition.
            workload: Workload profile with read/write ratio, QPS.

        Returns:
            List of IndexRecommendation objects sorted by priority.
        """
        recs: list[IndexRecommendation] = []
        table_columns: dict[str, set[str]] = {}

        if schema:
            for table in schema.tables:
                table_columns[table.name.lower()] = {c.name.lower() for c in table.columns}

        # Analyze each query for index opportunities.
        for query in queries:
            recs.extend(self._analyze_query(query, table_columns, workload))

        # Deduplicate by (table, columns).
        seen: set[str] = set()
        unique: list[IndexRecommendation] = []
        for rec in recs:
            key = f"{rec.table}:{','.join(sorted(rec.columns))}"
            if key not in seen:
                seen.add(key)
                unique.append(rec)

        return unique

    def _analyze_query(
        self,
        query: str,
        table_columns: dict[str, set[str]],
        workload: WorkloadProfile | None,
    ) -> list[IndexRecommendation]:
        """Analyze a single query for index opportunities."""
        recs: list[IndexRecommendation] = []
        lowered = query.lower()

        # Extract tables and aliases.
        tables = self._extract_tables(lowered)
        aliases = self._extract_aliases(lowered)
        where_columns = self._extract_where_columns(lowered)
        join_columns = self._extract_join_columns(lowered)
        order_columns = self._extract_order_columns(lowered)

        # Resolve aliases to actual table names.
        alias_map = self._build_alias_map(aliases, tables)

        for alias_or_table, cols in where_columns.items():
            if alias_or_table == "_unqualified":
                # Map unqualified columns to all available tables.
                for t in tables:
                    actual_table = alias_map.get(t, t)
                    if actual_table not in table_columns:
                        continue
                    valid_cols = cols & table_columns.get(actual_table, set())
                    if valid_cols:
                        impact = "High"
                        priority = Severity.high
                        if workload and workload.read_write_ratio < 0.5:
                            impact = "Medium (write-heavy workload)"
                            priority = Severity.medium
                        recs.append(IndexRecommendation(
                            table=actual_table,
                            columns=sorted(valid_cols),
                            index_type="btree",
                            estimated_impact=impact,
                            priority=priority,
                        ))
                continue

            actual_table = alias_map.get(alias_or_table, alias_or_table)
            if actual_table not in table_columns:
                continue
            valid_cols = cols & table_columns.get(actual_table, set())
            if not valid_cols:
                continue

            impact = "High"
            priority = Severity.high
            if workload and workload.read_write_ratio < 0.5:
                impact = "Medium (write-heavy workload)"
                priority = Severity.medium

            recs.append(IndexRecommendation(
                table=actual_table,
                columns=sorted(valid_cols),
                index_type="btree",
                estimated_impact=impact,
                priority=priority,
            ))

        return recs

    def _extract_aliases(self, query: str) -> dict[str, str]:
        """Extract table aliases from FROM/JOIN clauses."""
        aliases: dict[str, str] = {}
        for match in re.finditer(r'\b(?:from|join)\s+(\w+)(?:\s+(\w+))?\b', query, re.IGNORECASE):
            table = match.group(1)
            alias = match.group(2)
            if alias:
                aliases[alias] = table
        return aliases

    def _build_alias_map(self, aliases: dict[str, str], tables: set[str]) -> dict[str, str]:
        """Build a map from alias/table name to actual table name."""
        mapping: dict[str, str] = {}
        for alias, table in aliases.items():
            mapping[alias] = table
        for table in tables:
            mapping[table] = table
        return mapping

    def _extract_tables(self, query: str) -> set[str]:
        """Extract table names from a query."""
        tables: set[str] = set()
        for match in re.finditer(r'\bfrom\s+(\w+)', query):
            tables.add(match.group(1))
        for match in re.finditer(r'\bjoin\s+(\w+)', query):
            tables.add(match.group(1))
        return tables

    def _extract_where_columns(self, query: str) -> dict[str, set[str]]:
        """Extract columns used in WHERE clauses by table."""
        result: dict[str, set[str]] = {}
        for match in re.finditer(r'\bwhere\s+(.+?)(?:\bgroup\b|\border\b|\blimit\b|$)', query, re.IGNORECASE):
            where_clause = match.group(1)
            # Extract qualified columns (table.column).
            for col_match in re.finditer(r'(\w+)\.(\w+)\s*[=<>!]', where_clause):
                table = col_match.group(1)
                col = col_match.group(2)
                result.setdefault(table, set()).add(col)
            # Extract unqualified columns and map to FROM tables.
            for col_match in re.finditer(r'(?<!\.)\b(\w+)\s*[=<>!]', where_clause):
                col = col_match.group(1)
                if col.lower() not in ("and", "or", "not", "null", "true", "false"):
                    result.setdefault("_unqualified", set()).add(col)
        return result

    def _extract_join_columns(self, query: str) -> dict[str, set[str]]:
        """Extract columns used in JOIN conditions."""
        result: dict[str, set[str]] = {}
        for match in re.finditer(r'\bjoin\s+(\w+)\s+\w+\s+on\s+(\w+)\.(\w+)\s*=\s*(\w+)\.(\w+)', query, re.IGNORECASE):
            table1 = match.group(2)
            col1 = match.group(3)
            table2 = match.group(4)
            col2 = match.group(5)
            result.setdefault(table1, set()).add(col1)
            result.setdefault(table2, set()).add(col2)
        return result

    def _extract_order_columns(self, query: str) -> dict[str, set[str]]:
        """Extract columns used in ORDER BY."""
        result: dict[str, set[str]] = {}
        for match in re.finditer(r'\border\s+by\s+(.+?)(?:\blimit\b|$)', query, re.IGNORECASE):
            order_clause = match.group(1)
            for col_match in re.finditer(r'(\w+)\.(\w+)', order_clause):
                table = col_match.group(1)
                col = col_match.group(2)
                result.setdefault(table, set()).add(col)
        return result
