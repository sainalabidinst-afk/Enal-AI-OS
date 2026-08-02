"""
Business Analyst — Functional Specification Generator.

Generates executable functional specifications from BRD,
user stories, and use cases for downstream capability packs.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.business_analyst.schemas import (
    BusinessAnalysisRequest,
    BusinessAnalysisReport,
    Requirement,
    UserStory,
    UseCase,
    BusinessContext,
    Priority,
    RequirementType,
)

logger = logging.getLogger(__name__)


class SpecGenerator:
    """
    Generates functional specifications for downstream packs.

    Usage::

        generator = SpecGenerator()
        spec = generator.generate(request, requirements, user_stories, use_cases)
    """

    def generate(
        self,
        request: BusinessAnalysisRequest,
        requirements: list[Requirement],
        user_stories: list[UserStory],
        use_cases: list[UseCase],
    ) -> dict[str, Any]:
        """
        Generate a functional specification.

        Args:
            request: Original business analysis request.
            requirements: Structured requirements.
            user_stories: Generated user stories.
            use_cases: Generated use cases.

        Returns:
            Functional specification as a dict.
        """
        context = request.business_context

        # Build API-like specification from functional requirements.
        endpoints: list[dict[str, Any]] = []
        for req in requirements:
            if req.type == RequirementType.functional:
                endpoint = self._requirement_to_endpoint(req)
                if endpoint:
                    endpoints.append(endpoint)

        # Build user journey from user stories.
        journeys: list[dict[str, Any]] = []
        for story in user_stories:
            journeys.append({
                "id": story.id,
                "title": story.title,
                "acceptance_criteria": story.acceptance_criteria,
                "priority": story.priority.value,
                "story_points": story.story_points,
            })

        # Build actor-system interactions from use cases.
        interactions: list[dict[str, Any]] = []
        for uc in use_cases:
            interactions.append({
                "id": uc.id,
                "name": uc.name,
                "primary_actor": uc.primary_actor,
                "preconditions": uc.preconditions,
                "postconditions": uc.postconditions,
                "main_scenario_steps": len(uc.main_scenario),
                "exception_count": len(uc.exceptions),
            })

        return {
            "project": context.project_name,
            "domain": context.domain,
            "version": "1.0.0",
            "generated_at": self._timestamp(),
            "functional_requirements": [
                {
                    "id": req.id,
                    "title": req.title,
                    "description": req.description,
                    "priority": req.priority.value,
                    "type": req.type.value,
                    "acceptance_criteria": req.acceptance_criteria,
                }
                for req in requirements
                if req.type == RequirementType.functional
            ],
            "non_functional_requirements": [
                {
                    "id": req.id,
                    "title": req.title,
                    "description": req.description,
                    "priority": req.priority.value,
                    "acceptance_criteria": req.acceptance_criteria,
                }
                for req in requirements
                if req.type == RequirementType.non_functional
            ],
            "api_specification": {
                "endpoints": endpoints,
                "base_path": f"/api/v1/{context.domain.lower().replace(' ', '_')}",
            },
            "user_journeys": journeys,
            "use_case_interactions": interactions,
            "data_model_hints": self._infer_data_model(requirements),
            "integration_points": self._infer_integrations(requirements),
        }

    def _requirement_to_endpoint(self, req: Requirement) -> dict[str, Any] | None:
        """Convert a functional requirement to an API endpoint hint."""
        desc_lower = req.description.lower()
        path = "/items"
        method = "POST"

        if any(w in desc_lower for w in ("retrieve", "get", "view", "list", "show")):
            method = "GET"
            path = "/items"
        elif any(w in desc_lower for w in ("create", "add", "new")):
            method = "POST"
            path = "/items"
        elif any(w in desc_lower for w in ("update", "modify", "edit")):
            method = "PUT"
            path = "/items/{id}"
        elif any(w in desc_lower for w in ("delete", "remove")):
            method = "DELETE"
            path = "/items/{id}"

        return {
            "method": method,
            "path": path,
            "requirement_id": req.id,
            "priority": req.priority.value,
            "description": req.description[:80],
        }

    def _infer_data_model(self, requirements: list[Requirement]) -> list[dict[str, Any]]:
        """Infer data model entities from requirements."""
        entities: dict[str, list[str]] = {}
        for req in requirements:
            if req.type == RequirementType.functional:
                entity = self._extract_entity(req.description)
                if entity:
                    entities.setdefault(entity, []).append(req.id)

        return [
            {"entity": entity, "related_requirements": req_ids}
            for entity, req_ids in entities.items()
        ]

    def _extract_entity(self, text: str) -> str | None:
        """Extract entity name from requirement text."""
        entity_keywords = {
            "user": "User", "customer": "Customer", "order": "Order",
            "product": "Product", "invoice": "Invoice", "payment": "Payment",
            "account": "Account", "transaction": "Transaction", "report": "Report",
            "notification": "Notification", "session": "Session", "file": "File",
        }
        lowered = text.lower()
        for keyword, entity in entity_keywords.items():
            if keyword in lowered:
                return entity
        return None

    def _infer_integrations(self, requirements: list[Requirement]) -> list[str]:
        """Infer external integration points from requirements."""
        integrations: set[str] = set()
        integration_keywords = {
            "email": "Email Service",
            "payment": "Payment Gateway",
            "sms": "SMS Provider",
            "notification": "Notification Service",
            "auth": "Identity Provider",
            "storage": "Object Storage",
            "api": "External API",
            "webhook": "Webhook Handler",
            "analytics": "Analytics Platform",
        }
        for req in requirements:
            lowered = req.description.lower()
            for keyword, integration in integration_keywords.items():
                if keyword in lowered:
                    integrations.add(integration)
        return list(integrations)

    def _timestamp(self) -> str:
        """Get current timestamp string."""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
