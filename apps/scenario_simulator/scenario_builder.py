"""
Scenario Builder — builds scenario specifications from natural language.

Parses natural language "what-if" descriptions into structured
ScenarioRequest objects with variables, changes, and assumptions.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from apps.scenario_simulator.schemas import (
    ChangeType,
    DistributionType,
    ScenarioRequest,
    VariableChange,
)

logger = logging.getLogger(__name__)


class ScenarioBuilder:
    """
    Builds structured scenario specifications from natural language input.

    Usage::

        builder = ScenarioBuilder()
        request = builder.build(
            description="Jika suku bunga naik 1% dan kompetitor A turun harga 20%",
            base_state={"interest_rate": 0.05, "competitor_a_price": 100.0},
        )
    """

    # Keywords that map to variable change types
    _INCREASE_PATTERN = re.compile(r"(naik|increase|rising|up|higher|more)", re.IGNORECASE)
    _DECREASE_PATTERN = re.compile(r"(turun|decrease|falling|down|lower|less|drop)", re.IGNORECASE)
    _PERCENT_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*%", re.IGNORECASE)
    _ABSOLUTE_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*(?:percentage points?|ppt)", re.IGNORECASE)

    def build(
        self,
        description: str,
        base_state: dict[str, Any] | None = None,
        iterations: int = 100,
        seed: int | None = None,
    ) -> ScenarioRequest:
        """
        Build a ScenarioRequest from a natural language description.

        Args:
            description: Natural language what-if description.
            base_state: Known base state variables.
            iterations: Number of Monte Carlo iterations.
            seed: Optional random seed for reproducibility.

        Returns:
            ScenarioRequest with parsed variables and changes.
        """
        base_state = base_state or {}
        changes = self._parse_changes(description, base_state)

        assumptions = self._extract_assumptions(description)

        return ScenarioRequest(
            title=self._generate_title(description),
            description=description,
            base_state=base_state,
            variable_changes=changes,
            iterations=iterations,
            seed=seed,
            context={"assumptions": assumptions},
        )

    def parse_with_llm(
        self,
        description: str,
        base_state: dict[str, Any] | None = None,
        iterations: int = 100,
        seed: int | None = None,
    ) -> ScenarioRequest:
        """
        Parse a what-if description using LLM for more nuanced extraction.

        Falls back to regex-based parsing if LLM is unavailable.
        """
        import asyncio
        try:
            return asyncio.run(self._parse_with_llm(description, base_state, iterations, seed))
        except Exception as e:
            logger.warning(f"LLM parsing failed, falling back to regex: {e}")
            return self.build(description, base_state, iterations, seed)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _parse_changes(self, description: str, base_state: dict[str, Any]) -> list[VariableChange]:
        """Parse variable changes using pattern matching and base state knowledge."""
        changes: list[VariableChange] = []
        text = description.lower()

        # Detect interest rate changes
        if "suku bunga" in text or "interest rate" in text:
            change = self._detect_change(text, "interest_rate", base_state.get("interest_rate"))
            if change:
                changes.append(change)

        # Detect price changes
        for competitor_key in base_state:
            if "competitor" in competitor_key.lower() or "kompetitor" in competitor_key.lower():
                if competitor_key.replace("_", " ") in text or competitor_key in text:
                    change = self._detect_change(text, competitor_key, base_state.get(competitor_key))  # noqa: E501
                    if change:
                        changes.append(change)

        # Detect general percentage changes
        if not changes:
            changes = self._detect_generic_changes(text, base_state)

        # If no changes detected from text, create a generic change
        if not changes and base_state:
            first_var = list(base_state.keys())[0]
            changes.append(VariableChange(
                variable=first_var,
                change_type=ChangeType.ABSOLUTE_DELTA,
                value=0.0,
                distribution=DistributionType.FIXED,
            ))

        return changes

    def _detect_change(self, text: str, var_name: str, base_value: Any) -> VariableChange | None:
        """Detect a change for a specific variable."""
        # Look for percentage changes
        percent_match = self._PERCENT_PATTERN.search(text)
        abs_match = self._ABSOLUTE_PATTERN.search(text)

        if percent_match:
            pct = float(percent_match.group(1)) / 100.0
            if self._DECREASE_PATTERN.search(text):
                pct = -pct
            return VariableChange(
                variable=var_name,
                change_type=ChangeType.PERCENT_DELTA,
                value=pct,
                distribution=DistributionType.NORMAL,
                range_min=pct * 0.5 if pct < 0 else pct * 0.5,
                range_max=pct * 1.5 if pct < 0 else pct * 1.5,
                stddev=abs(pct) * 0.1,
            )

        if abs_match:
            delta = float(abs_match.group(1))
            if self._DECREASE_PATTERN.search(text):
                delta = -delta
            return VariableChange(
                variable=var_name,
                change_type=ChangeType.ABSOLUTE_DELTA,
                value=delta,
                distribution=DistributionType.UNIFORM,
                range_min=delta * 0.5 if delta >= 0 else delta * 1.5,
                range_max=delta * 1.5 if delta >= 0 else delta * 0.5,
            )

        return None

    def _detect_generic_changes(self, text: str, base_state: dict[str, Any]) -> list[VariableChange]:  # noqa: E501
        """Detect generic variable changes from any numeric patterns."""
        changes: list[VariableChange] = []
        for var_name, value in base_state.items():
            if isinstance(value, (int, float)):
                change = self._detect_change(text, var_name, value)
                if change:
                    changes.append(change)
        return changes

    def _extract_assumptions(self, description: str) -> list[str]:
        """Extract implicit assumptions from the description."""
        assumptions = [
            "All other variables remain constant unless stated otherwise",
            "Changes take effect immediately",
            "No external shocks beyond the described scenario",
        ]
        if "turun harga" in description.lower() or "discount" in description.lower():
            assumptions.append("Competitor pricing response is not modeled")
        if "sukses" in description.lower() or "revenue" in description.lower():
            assumptions.append("Cost structures remain unchanged")
        return assumptions

    def _generate_title(self, description: str) -> str:
        """Generate a title from the description."""
        words = description.split()[:8]
        return " ".join(words).rstrip(".,;:") + "..." if len(description.split()) > 8 else description  # noqa: E501

    async def _parse_with_llm(
        self,
        description: str,
        base_state: dict[str, Any] | None,
        iterations: int,
        seed: int | None,
    ) -> ScenarioRequest:
        """Use LLM to parse a natural language scenario into structured form."""
        prompt = (
            f"Parse the following 'what-if' scenario description into structured JSON.\n\n"
            f"Description: {description}\n\n"
            f"Base state variables: {json.dumps(base_state or {})}\n\n"
            "Output JSON:\n"
            "{\n"
            '  "title": "short scenario title",\n'
            '  "variable_changes": [\n'
            '    {\n'
            '      "variable": "variable_name",\n'
            '      "change_type": "absolute_delta | percent_delta | set_value",\n'
            '      "value": float,\n'
            '      "distribution": "fixed | uniform | normal | triangular",\n'
            '      "range_min": float_or_null,\n'
            '      "range_max": float_or_null,\n'
            '      "stddev": float_or_null\n'
            '    }\n'
            '  ],\n'
            '  "assumptions": ["assumption1", "assumption2"]\n'
            "}"
        )
        from backend.app.core.config import settings
        from backend.app.core.model_router import model_router

        response = await model_router.acomplete(
            [{"role": "user", "content": prompt}],
            model=settings.DEFAULT_REASONING_MODEL,
            temperature=0.3,
            max_tokens=1024,
        )
        data = json.loads(response.choices[0].message.content)
        changes = [
            VariableChange(**{k: v for k, v in c.items() if k in VariableChange.model_fields})
            for c in data.get("variable_changes", [])
        ]
        return ScenarioRequest(
            title=data.get("title", description[:50]),
            description=description,
            base_state=base_state or {},
            variable_changes=changes,
            iterations=iterations,
            seed=seed,
        )
