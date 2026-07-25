"""
Meeting System
===============

Synchronous, mediated collaboration between multiple entities.
Meetings have agendas, timeboxes, and produce outcomes written to Blackboard.
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from apps.organization.communication import blackboard

logger = logging.getLogger(__name__)


class MeetingStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    TIMED_OUT = "timed_out"


class MeetingType(str, Enum):
    TEAM_SYNC = "team_sync"
    PLANNING = "planning"
    REVIEW = "review"
    RETROSPECTIVE = "retrospective"
    CRISIS = "crisis"
    BRAINSTORM = "brainstorm"


@dataclass
class MeetingParticipant:
    entity_id: str
    role: str
    required: bool = True


@dataclass
class AgendaItem:
    id: str
    title: str
    description: str
    owner: str
    time_allocated_minutes: int = 5


@dataclass
class MeetingOutcome:
    decisions: list[dict[str, Any]] = field(default_factory=list)
    action_items: list[dict[str, Any]] = field(default_factory=list)
    blockers: list[dict[str, Any]] = field(default_factory=list)
    summary: str = ""


@dataclass
class Meeting:
    id: str
    title: str
    meeting_type: MeetingType
    organizer_id: str
    participants: list[MeetingParticipant]
    agenda: list[AgendaItem]
    status: MeetingStatus = MeetingStatus.SCHEDULED
    started_at: datetime | None = None
    ended_at: datetime | None = None
    timebox_minutes: int = 30
    outcome: MeetingOutcome | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class MeetingSystem:
    """Manages synchronous meetings between workforce entities."""

    def __init__(self, blackboard: Any):
        self._meetings: dict[str, Meeting] = {}
        self._blackboard = blackboard

    def schedule_meeting(
        self,
        title: str,
        meeting_type: MeetingType,
        organizer_id: str,
        participant_ids: list[str],
        agenda_titles: list[str] | None = None,
        timebox_minutes: int = 30,
    ) -> Meeting:
        meeting_id = f"meeting-{uuid.uuid4().hex[:8]}"
        participants = [MeetingParticipant(entity_id=pid, role="participant", required=True) for pid in participant_ids]
        participants.append(MeetingParticipant(entity_id=organizer_id, role="organizer", required=True))

        agenda: list[AgendaItem] = []
        if agenda_titles:
            for i, agenda_title in enumerate(agenda_titles):
                agenda.append(AgendaItem(
                    id=f"agenda-{i+1}",
                    title=agenda_title,
                    description="",
                    owner=organizer_id,
                    time_allocated_minutes=max(5, timebox_minutes // len(agenda_titles)),
                ))

        meeting = Meeting(
            id=meeting_id,
            title=title,
            meeting_type=meeting_type,
            organizer_id=organizer_id,
            participants=participants,
            agenda=agenda,
            timebox_minutes=timebox_minutes,
        )
        self._meetings[meeting_id] = meeting
        logger.info("Meeting scheduled: %s - %s", meeting_id, title)
        return meeting

    def start_meeting(self, meeting_id: str) -> Meeting | None:
        meeting = self._meetings.get(meeting_id)
        if meeting and meeting.status == MeetingStatus.SCHEDULED:
            meeting.status = MeetingStatus.IN_PROGRESS
            meeting.started_at = datetime.utcnow()
            logger.info("Meeting started: %s", meeting_id)
            return meeting
        return None

    def end_meeting(self, meeting_id: str, outcome: MeetingOutcome) -> Meeting | None:
        meeting = self._meetings.get(meeting_id)
        if meeting and meeting.status == MeetingStatus.IN_PROGRESS:
            meeting.status = MeetingStatus.COMPLETED
            meeting.ended_at = datetime.utcnow()
            meeting.outcome = outcome
            self._write_outcome_to_blackboard(meeting)
            logger.info("Meeting completed: %s - %d decisions, %d action items", meeting_id, len(outcome.decisions), len(outcome.action_items))
            return meeting
        return None

    def cancel_meeting(self, meeting_id: str) -> Meeting | None:
        meeting = self._meetings.get(meeting_id)
        if meeting and meeting.status in (MeetingStatus.SCHEDULED, MeetingStatus.IN_PROGRESS):
            meeting.status = MeetingStatus.CANCELLED
            logger.info("Meeting cancelled: %s", meeting_id)
            return meeting
        return None

    def get_meeting(self, meeting_id: str) -> Meeting | None:
        return self._meetings.get(meeting_id)

    def get_meetings_by_organizer(self, organizer_id: str) -> list[Meeting]:
        return [m for m in self._meetings.values() if m.organizer_id == organizer_id]

    def get_meetings_by_participant(self, entity_id: str) -> list[Meeting]:
        return [m for m in self._meetings.values() if any(p.entity_id == entity_id for p in m.participants)]

    def _write_outcome_to_blackboard(self, meeting: Meeting) -> None:
        if not meeting.outcome:
            return
        self._blackboard.write(f"meeting-{meeting.id}-outcome", {
            "meeting_id": meeting.id,
            "title": meeting.title,
            "type": meeting.meeting_type.value,
            "decisions": meeting.outcome.decisions,
            "action_items": meeting.outcome.action_items,
            "blockers": meeting.outcome.blockers,
            "summary": meeting.outcome.summary,
            "timestamp": datetime.utcnow().isoformat(),
        })


meeting_system = MeetingSystem(blackboard)
