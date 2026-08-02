"""
Business Analyst — Process Modeler.

Models business workflows using BPMN-like notation.
Produces process models with activities, gateways, and data flows.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from apps.business_analyst.schemas import (
    ProcessModel,
    ProcessActivity,
    ProcessActivityType,
    BusinessContext,
)

logger = logging.getLogger(__name__)


# Keywords indicating process steps.
_ACTION_KEYWORDS = {
    "create", "generate", "send", "receive", "process", "validate", "approve",
    "reject", "submit", "review", "notify", "calculate", "store", "retrieve",
    "update", "delete", "escalate", "complete", "start", "end", "log",
}

# Keywords indicating decisions.
_DECISION_KEYWORDS = {
    "if", "check", "validate", "verify", "approved", "rejected", "pass", "fail",
    "success", "failure", "error", "valid", "invalid", "eligible",
}


class ProcessModeler:
    """
    Models business workflows from descriptions.

    Usage::

        modeler = ProcessModeler()
        model = modeler.model(process_description)
    """

    def model(self, description: str) -> ProcessModel:
        """
        Model a business process from a description.

        Args:
            description: Natural language process description.

        Returns:
            ProcessModel with activities and flow.
        """
        if not description:
            return ProcessModel(name="Unnamed Process")

        name = self._extract_name(description)
        activities = self._extract_activities(description)
        start = activities[0].id if activities else ""
        end = activities[-1].id if activities else ""

        return ProcessModel(
            name=name,
            activities=activities,
            start_activity=start,
            end_activity=end,
        )

    def _extract_name(self, description: str) -> str:
        """Extract process name from description."""
        first_line = description.strip().split("\n")[0].strip()
        if first_line:
            return first_line[:80]
        return "Business Process"

    def _extract_activities(self, description: str) -> list[ProcessActivity]:
        """Extract activities from process description."""
        activities: list[ProcessActivity] = []
        sentences = re.split(r'[.!?\n]+', description)
        activity_id = 1

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence or len(sentence) < 5:
                continue

            act_type = self._classify_activity(sentence)
            name = self._extract_activity_name(sentence)
            actor = self._extract_actor(sentence)

            activity = ProcessActivity(
                id=f"act_{activity_id}",
                type=act_type,
                name=name,
                description=sentence,
                actor=actor,
                inputs=self._extract_io(sentence, "input"),
                outputs=self._extract_io(sentence, "output"),
                next_activities=[f"act_{activity_id + 1}"] if activity_id < 10 else [],
            )
            activities.append(activity)
            activity_id += 1

        return activities

    def _classify_activity(self, text: str) -> ProcessActivityType:
        """Classify text as a process activity type."""
        lowered = text.lower()

        if any(w in lowered for w in ("start", "begin", "initiate", "trigger")):
            return ProcessActivityType.start
        if any(w in lowered for w in ("end", "complete", "finish", "close")):
            return ProcessActivityType.end
        if any(w in lowered for w in ("if", "check", "validate", "verify", "approved", "rejected")):
            return ProcessActivityType.decision
        if any(w in lowered for w in ("subprocess", "workflow", "nested")):
            return ProcessActivityType.subprocess

        return ProcessActivityType.task

    def _extract_activity_name(self, text: str) -> str:
        """Extract short activity name from text."""
        verbs = ["create", "generate", "send", "receive", "process", "validate", "approve",
                 "reject", "submit", "review", "notify", "calculate", "store", "update",
                 "check", "verify", "escalate", "complete", "start", "end"]
        words = text.split()
        for word in words:
            if word.lower() in verbs:
                return f"{word.capitalize()} {words[words.index(word) + 1] if words.index(word) + 1 < len(words) else 'item'}"
        return text[:30]

    def _extract_actor(self, text: str) -> str:
        """Extract actor from text."""
        patterns = [
            r'by (\w+)',
            r'from (\w+)',
            r'to (\w+)',
            r'(\w+) (?:will|shall|must|should|can)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return "system"

    def _extract_io(self, text: str, io_type: str) -> list[str]:
        """Extract inputs or outputs from text."""
        if io_type == "input":
            patterns = [r'from (\w+)', r'receive (\w+)', r'given (\w+)']
        else:
            patterns = [r'to (\w+)', r'send (\w+)', r'produce (\w+)', r'generate (\w+)']

        results: list[str] = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            results.extend(matches)
        return list(set(results))
