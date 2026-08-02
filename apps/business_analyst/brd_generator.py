"""
Business Analyst — BRD Generator.

Generates Business Requirement Documents (BRD) from
structured requirements, user stories, and business context.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.business_analyst.schemas import (
    BusinessAnalysisRequest,
    BusinessAnalysisReport,
    Requirement,
    UserStory,
    BusinessContext,
    StakeholderInput,
    Priority,
    RequirementType,
)

logger = logging.getLogger(__name__)


class BRDGenerator:
    """
    Generates Business Requirement Documents.

    Usage::

        generator = BRDGenerator()
        brd = generator.generate(request, requirements, user_stories)
    """

    def generate(
        self,
        request: BusinessAnalysisRequest,
        requirements: list[Requirement],
        user_stories: list[UserStory],
    ) -> str:
        """
        Generate a BRD document in Markdown format.

        Args:
            request: Original business analysis request.
            requirements: Structured requirements.
            user_stories: Generated user stories.

        Returns:
            BRD document as a Markdown string.
        """
        context = request.business_context
        inputs = request.inputs

        lines: list[str] = []
        lines.append(f"# Business Requirement Document: {context.project_name or 'Untitled Project'}")
        lines.append("")
        lines.append(f"**Domain:** {context.domain}")
        lines.append(f"**Generated:** {self._timestamp()}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 1. Executive Summary.
        lines.append("## 1. Executive Summary")
        lines.append("")
        lines.append(context.description or "No project description provided.")
        lines.append("")
        lines.append(f"Total Requirements: {len(requirements)}")
        lines.append(f"Total User Stories: {len(user_stories)}")
        lines.append("")

        # 2. Business Context.
        lines.append("## 2. Business Context")
        lines.append("")
        lines.append(f"**Domain:** {context.domain}")
        lines.append(f"**Project:** {context.project_name}")
        lines.append("")

        # 3. Stakeholder Requirements.
        lines.append("## 3. Stakeholder Requirements")
        lines.append("")
        if inputs.natural_language_requirements:
            lines.append("### 3.1 Raw Requirements")
            lines.append("")
            for i, req in enumerate(inputs.natural_language_requirements, 1):
                lines.append(f"{i}. {req}")
            lines.append("")

        if inputs.stakeholder_notes:
            lines.append("### 3.2 Stakeholder Notes")
            lines.append("")
            for i, note in enumerate(inputs.stakeholder_notes, 1):
                lines.append(f"{i}. {note}")
            lines.append("")

        # 4. Structured Requirements.
        lines.append("## 4. Structured Requirements")
        lines.append("")
        for req in requirements:
            lines.append(f"### {req.id}: {req.title}")
            lines.append("")
            lines.append(f"- **Description:** {req.description}")
            lines.append(f"- **Type:** {req.type.value}")
            lines.append(f"- **Priority:** {req.priority.value}")
            lines.append(f"- **Clarity Score:** {req.clarity_score:.0%}")
            lines.append(f"- **Source:** {req.source}")
            if req.ambiguity_flags:
                lines.append(f"- **Ambiguity Flags:** {', '.join(req.ambiguity_flags)}")
            if req.acceptance_criteria:
                lines.append("- **Acceptance Criteria:**")
                for ac in req.acceptance_criteria:
                    lines.append(f"  - {ac}")
            if req.dependencies:
                lines.append(f"- **Dependencies:** {', '.join(req.dependencies)}")
            lines.append("")

        # 5. User Stories.
        lines.append("## 5. User Stories")
        lines.append("")
        for story in user_stories:
            lines.append(f"### {story.id}: {story.title}")
            lines.append("")
            lines.append(f"- **Description:** {story.description}")
            lines.append(f"- **Priority:** {story.priority.value}")
            lines.append(f"- **Story Points:** {story.story_points}")
            if story.acceptance_criteria:
                lines.append("- **Acceptance Criteria:**")
                for ac in story.acceptance_criteria:
                    lines.append(f"  - {ac}")
            lines.append("")

        # 6. Non-Functional Requirements.
        nf_reqs = [r for r in requirements if r.type == RequirementType.non_functional]
        if nf_reqs:
            lines.append("## 6. Non-Functional Requirements")
            lines.append("")
            for req in nf_reqs:
                lines.append(f"- **{req.id}:** {req.title} (Priority: {req.priority.value})")
            lines.append("")

        # 7. Technical Constraints.
        if inputs.technical_constraints:
            lines.append("## 7. Technical Constraints")
            lines.append("")
            for constraint in inputs.technical_constraints:
                lines.append(f"- {constraint}")
            lines.append("")

        # 8. Appendix.
        lines.append("## 8. Appendix")
        lines.append("")
        lines.append("This document was generated by the Business Analyst Capability Pack.")
        lines.append("")
        lines.append("---")
        lines.append("*End of BRD*")

        return "\n".join(lines)

    def _timestamp(self) -> str:
        """Get current timestamp string."""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
