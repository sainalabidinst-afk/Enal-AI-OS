"""
Business Analyst — Use Case Modeler.

Generates detailed use cases from requirements and personas.
Includes actors, pre/post conditions, scenarios, and exceptions.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.business_analyst.schemas import (
    Requirement,
    Persona,
    UseCase,
    BusinessContext,
)

logger = logging.getLogger(__name__)


class UseCaseModeler:
    """
    Generates use cases from requirements.

    Usage::

        modeler = UseCaseModeler()
        use_cases = modeler.model(requirements, personas)
    """

    def model(
        self,
        requirements: list[Requirement],
        personas: list[Persona] | None = None,
    ) -> list[UseCase]:
        """
        Generate use cases from requirements.

        Args:
            requirements: List of structured requirements.
            personas: Optional list of user personas.

        Returns:
            List of UseCase objects.
        """
        use_cases: list[UseCase] = []
        default_actor = "User"

        for req in requirements:
            actor = self._determine_actor(req, personas)
            uc = self._create_use_case(req, actor)
            use_cases.append(uc)

        return use_cases

    def _determine_actor(self, req: Requirement, personas: list[Persona] | None) -> str:
        """Determine the primary actor for a requirement."""
        if personas:
            return personas[0].role
        if req.source and "admin" in req.source.lower():
            return "Administrator"
        if req.type.value == "non_functional":
            return "System"
        return "User"

    def _create_use_case(self, req: Requirement, actor: str) -> UseCase:
        """Create a use case from a requirement."""
        name = req.title[:60] or "Unnamed Use Case"
        preconditions = self._infer_preconditions(req)
        postconditions = self._infer_postconditions(req)
        main_scenario = self._build_main_scenario(req, actor)
        alternative_scenarios = self._build_alternative_scenarios(req, actor)
        exceptions = self._build_exceptions(req, actor)

        return UseCase(
            name=name,
            primary_actor=actor,
            preconditions=preconditions,
            postconditions=postconditions,
            main_scenario=main_scenario,
            alternative_scenarios=alternative_scenarios,
            exceptions=exceptions,
        )

    def _infer_preconditions(self, req: Requirement) -> list[str]:
        """Infer preconditions from requirement."""
        preconditions = ["User is authenticated and authorized"]
        if req.type.value == "functional":
            preconditions.append("Required resources are available")
        return preconditions

    def _infer_postconditions(self, req: Requirement) -> list[str]:
        """Infer postconditions from requirement."""
        postconditions = ["System state is consistent"]
        if req.type.value == "functional":
            postconditions.append("Requested action is completed successfully")
            postconditions.append("Appropriate notifications are sent")
        return postconditions

    def _build_main_scenario(self, req: Requirement, actor: str) -> list[str]:
        """Build main success scenario."""
        return [
            f"{actor} initiates the action: {req.title[:50]}",
            "System validates input parameters",
            "System performs the requested operation",
            "System returns a success response",
            "System updates relevant state and logs the action",
        ]

    def _build_alternative_scenarios(self, req: Requirement, actor: str) -> list[str]:
        """Build alternative scenarios."""
        return [
            f"1a. {actor} cancels the operation at any step — system returns to previous state",
            f"2a. System encounters a recoverable error — system retries up to 3 times",
        ]

    def _build_exceptions(self, req: Requirement, actor: str) -> list[str]:
        """Build exception scenarios."""
        return [
            f"E1. Invalid input — system returns validation error with details",
            f"E2. Authorization failure — system returns 403 Forbidden",
            f"E3. System unavailable — system returns 503 Service Unavailable",
        ]
