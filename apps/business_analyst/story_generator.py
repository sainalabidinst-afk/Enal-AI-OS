"""
Business Analyst — Story Generator.

Generates INVEST-compliant user stories with acceptance criteria
from requirements and personas.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.business_analyst.schemas import (
    Requirement,
    Persona,
    UserStory,
    Priority,
    StoryPoint,
)

logger = logging.getLogger(__name__)


class StoryGenerator:
    """
    Generates user stories from requirements.

    Usage::

        generator = StoryGenerator()
        stories = generator.generate_from_requirements(requirements, personas)
    """

    def generate_from_requirements(
        self,
        requirements: list[Requirement],
        personas: list[Persona] | None = None,
    ) -> list[UserStory]:
        """
        Generate user stories from requirements.

        Args:
            requirements: List of structured requirements.
            personas: Optional list of user personas.

        Returns:
            List of UserStory objects.
        """
        stories: list[UserStory] = []
        default_persona = Persona(
            name="User",
            role="End User",
            goals=["Use the system effectively"],
            pain_points=["Unclear interfaces"],
        )

        for req in requirements:
            persona = personas[0] if personas else default_persona
            story = self._create_story(req, persona)
            stories.append(story)

        return stories

    def generate_from_personas(
        self,
        personas: list[Persona],
        requirements: list[Requirement] | None = None,
    ) -> list[UserStory]:
        """
        Generate user stories from personas.

        Args:
            personas: List of user personas.
            requirements: Optional requirements for context.

        Returns:
            List of UserStory objects.
        """
        stories: list[UserStory] = []

        for persona in personas:
            for goal in persona.goals:
                story = UserStory(
                    title=f"As a {persona.role}, I want to {goal.lower()} so that I can achieve my objectives",
                    description=f"User persona: {persona.name} ({persona.role}). Goal: {goal}. Pain points: {', '.join(persona.pain_points)}",
                    acceptance_criteria=self._default_acceptance_criteria(goal),
                    story_points=StoryPoint.m.value,
                    priority=Priority.should_have,
                )
                stories.append(story)

        return stories

    def _create_story(self, req: Requirement, persona: Persona) -> UserStory:
        """Create a user story from a requirement and persona."""
        goal = req.title.lower().replace("the system shall", "").replace("must", "").strip()
        if not goal:
            goal = req.description[:60]

        benefit = self._infer_benefit(req.description, persona)

        return UserStory(
            title=f"As a {persona.role}, I want to {goal} so that {benefit}",
            description=req.description,
            acceptance_criteria=req.acceptance_criteria or self._default_acceptance_criteria(goal),
            story_points=self._estimate_points(req),
            priority=req.priority,
            dependencies=req.dependencies,
        )

    def _infer_benefit(self, description: str, persona: Persona) -> str:
        """Infer the benefit part of a user story."""
        lowered = description.lower()
        if any(w in lowered for w in ("efficiency", "faster", "quickly")):
            return "I can complete my work more efficiently"
        if any(w in lowered for w in ("accuracy", "correct", "reliable")):
            return "I can trust the system to give correct results"
        if any(w in lowered for w in ("convenience", "easy", "simple")):
            return "I can accomplish tasks with minimal effort"
        if any(w in lowered for w in ("compliance", "audit", "security")):
            return "the organization meets compliance requirements"
        return "I can achieve my objectives effectively"

    def _estimate_points(self, req: Requirement) -> str:
        """Estimate story points based on requirement complexity."""
        complexity = len(req.description) + len(req.acceptance_criteria) * 5
        if complexity < 50:
            return StoryPoint.xs.value
        elif complexity < 100:
            return StoryPoint.s.value
        elif complexity < 200:
            return StoryPoint.m.value
        elif complexity < 400:
            return StoryPoint.l.value
        else:
            return StoryPoint.xl.value

    def _default_acceptance_criteria(self, goal: str) -> list[str]:
        """Generate default acceptance criteria for a goal."""
        return [
            f"Given a user with appropriate permissions, when they attempt to {goal}, then the system allows the action",
            f"Given a user without appropriate permissions, when they attempt to {goal}, then the system denies access with an appropriate message",
            f"Given invalid input, when the user attempts to {goal}, then the system returns a validation error",
        ]
