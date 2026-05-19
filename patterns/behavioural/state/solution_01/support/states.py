from __future__ import annotations

from abc import ABC
from collections.abc import MutableSequence, Sequence
from dataclasses import dataclass, field, replace
from datetime import date, datetime
from decimal import Decimal
from typing import Self

from .errors import InvalidTransition
from .formatting import format_date
from .interview import Interviewer, InterviewRound
from .rejection import Rejection
from .source import DirectApplication, Source, SourcedFromRecruiter


@dataclass(frozen=True)
class CandidateData:
    """Identity and accumulated history carried across post-screening states."""

    candidate_name: str
    role: str
    source: Source
    screening_score: float
    screened_at: datetime
    rejections: MutableSequence[Rejection] = field(default_factory=list[Rejection])


class State(ABC):
    def screen(self, *, score: float, at: datetime) -> Screened:
        raise InvalidTransition("screen is not allowed from this state")

    def interview(
        self,
        *,
        panel: Sequence[Interviewer],
        notes: str,
        at: datetime,
    ) -> Interviewed:
        raise InvalidTransition("interview is not allowed from this state")

    def make_offer(
        self,
        *,
        offer_salary: Decimal,
        offer_expires_at: datetime,
        at: datetime,
    ) -> OfferExtended:
        raise InvalidTransition("make_offer is not allowed from this state")

    def hire(self, *, start_date: date, employee_id: str, at: datetime) -> Hired:
        raise InvalidTransition("hire is not allowed from this state")

    def reject(self, *, reason: str, at: datetime) -> Rejected:
        raise InvalidTransition("reject is not allowed from this state")

    def abandon(self, *, at: datetime) -> Abandoned:
        raise InvalidTransition("abandon is not allowed from this state")


@dataclass(frozen=True)
class Abandoned(State):
    candidate_name: str
    role: str
    abandoned_at: datetime
    data: CandidateData | None = None
    rounds: MutableSequence[InterviewRound] = field(
        default_factory=list[InterviewRound]
    )
    offer_salary: Decimal | None = None
    offer_at: datetime | None = None
    offer_expires_at: datetime | None = None

    def __str__(self) -> str:
        return f"abandoned ({format_date(self.abandoned_at)})"

    def abandon(self, *, at: datetime) -> Self:
        raise InvalidTransition("abandon is not allowed from a terminal state")


@dataclass(frozen=True)
class Hired(State):
    data: CandidateData
    rounds: MutableSequence[InterviewRound]
    offer_salary: Decimal
    offer_at: datetime
    offer_expires_at: datetime
    start_date: date
    employee_id: str
    hire_at: datetime

    def __str__(self) -> str:
        return (
            f"hired ({self.employee_id}, {format_date(self.hire_at)}, "
            f"starts {format_date(self.start_date)})"
        )

    def abandon(self, *, at: datetime) -> Abandoned:
        raise InvalidTransition("abandon is not allowed from a terminal state")


@dataclass(frozen=True)
class OfferExtended(State):
    data: CandidateData
    rounds: MutableSequence[InterviewRound]
    offer_salary: Decimal
    offer_at: datetime
    offer_expires_at: datetime

    def __str__(self) -> str:
        return (
            f"offer extended ({self.offer_salary}, "
            f"{format_date(self.offer_at)}, "
            f"expires {format_date(self.offer_expires_at)})"
        )

    def hire(self, *, start_date: date, employee_id: str, at: datetime) -> Hired:
        return Hired(
            data=self.data,
            rounds=self.rounds,
            offer_salary=self.offer_salary,
            offer_at=self.offer_at,
            offer_expires_at=self.offer_expires_at,
            start_date=start_date,
            employee_id=employee_id,
            hire_at=at,
        )

    def reject(self, *, reason: str, at: datetime) -> Rejected:
        return Rejected(
            data=replace(
                self.data,
                rejections=[*self.data.rejections, Rejection(reason=reason, at=at)],
            ),
            rounds=self.rounds,
            offer_salary=self.offer_salary,
            offer_at=self.offer_at,
            offer_expires_at=self.offer_expires_at,
        )

    def abandon(self, *, at: datetime) -> Abandoned:
        return Abandoned(
            candidate_name=self.data.candidate_name,
            role=self.data.role,
            abandoned_at=at,
            data=self.data,
            rounds=self.rounds,
            offer_salary=self.offer_salary,
            offer_at=self.offer_at,
            offer_expires_at=self.offer_expires_at,
        )


@dataclass(frozen=True)
class Rejected(State):
    data: CandidateData
    rounds: MutableSequence[InterviewRound]
    offer_salary: Decimal | None = None
    offer_at: datetime | None = None
    offer_expires_at: datetime | None = None

    def __str__(self) -> str:
        latest = self.data.rejections[-1]
        return f"rejected: {latest.reason} ({format_date(latest.at)})"

    def screen(self, *, score: float, at: datetime) -> Screened:
        return Screened(data=replace(self.data, screening_score=score, screened_at=at))

    def interview(
        self,
        *,
        panel: Sequence[Interviewer],
        notes: str,
        at: datetime,
    ) -> Interviewed:
        round_entry = InterviewRound(panel=panel, notes=notes, at=at)
        return Interviewed(
            data=self.data,
            rounds=[*self.rounds, round_entry],
        )

    def abandon(self, *, at: datetime) -> Abandoned:
        return Abandoned(
            candidate_name=self.data.candidate_name,
            role=self.data.role,
            abandoned_at=at,
            data=self.data,
            rounds=self.rounds,
            offer_salary=self.offer_salary,
            offer_at=self.offer_at,
            offer_expires_at=self.offer_expires_at,
        )


@dataclass(frozen=True)
class Interviewed(State):
    data: CandidateData
    rounds: MutableSequence[InterviewRound]

    def __post_init__(self) -> None:
        self._require_rounds()

    def _require_rounds(self) -> None:
        if len(self.rounds) == 0:
            raise ValueError("Interviewed requires at least one interview round")

    def __str__(self) -> str:
        self._require_rounds()
        round_dates = ", ".join(
            round_entry.at.strftime("%Y-%m-%d") for round_entry in self.rounds
        )
        return f"interviewed -- rounds: {round_dates}"

    def interview(
        self,
        *,
        panel: Sequence[Interviewer],
        notes: str,
        at: datetime,
    ) -> Self:
        round_entry = InterviewRound(panel=panel, notes=notes, at=at)
        return replace(self, rounds=[*self.rounds, round_entry])

    def make_offer(
        self,
        *,
        offer_salary: Decimal,
        offer_expires_at: datetime,
        at: datetime,
    ) -> OfferExtended:
        return OfferExtended(
            data=self.data,
            rounds=self.rounds,
            offer_salary=offer_salary,
            offer_at=at,
            offer_expires_at=offer_expires_at,
        )

    def reject(self, *, reason: str, at: datetime) -> Rejected:
        return Rejected(
            data=replace(
                self.data,
                rejections=[*self.data.rejections, Rejection(reason=reason, at=at)],
            ),
            rounds=self.rounds,
        )

    def abandon(self, *, at: datetime) -> Abandoned:
        return Abandoned(
            candidate_name=self.data.candidate_name,
            role=self.data.role,
            abandoned_at=at,
            data=self.data,
            rounds=self.rounds,
        )


@dataclass(frozen=True)
class Screened(State):
    data: CandidateData

    def __str__(self) -> str:
        if isinstance(self.data.source, DirectApplication):
            return f"screened (direct, {format_date(self.data.screened_at)})"
        return (
            f"screened (via {self.data.source.recruiter}, "
            f"{format_date(self.data.screened_at)})"
        )

    def interview(
        self,
        *,
        panel: Sequence[Interviewer],
        notes: str,
        at: datetime,
    ) -> Interviewed:
        round_entry = InterviewRound(panel=panel, notes=notes, at=at)
        return Interviewed(data=self.data, rounds=[round_entry])

    def reject(self, *, reason: str, at: datetime) -> Rejected:
        return Rejected(
            data=replace(
                self.data,
                rejections=[*self.data.rejections, Rejection(reason=reason, at=at)],
            ),
            rounds=[],
        )

    def abandon(self, *, at: datetime) -> Abandoned:
        return Abandoned(
            candidate_name=self.data.candidate_name,
            role=self.data.role,
            abandoned_at=at,
            data=self.data,
        )


@dataclass(frozen=True)
class Applied(State):
    candidate_name: str
    role: str
    applied_at: datetime

    def __str__(self) -> str:
        return (
            f"{self.candidate_name} applied for {self.role} "
            f"({format_date(self.applied_at)})"
        )

    def screen(self, *, score: float, at: datetime) -> Screened:
        return Screened(
            data=CandidateData(
                candidate_name=self.candidate_name,
                role=self.role,
                source=DirectApplication(),
                screening_score=score,
                screened_at=at,
            )
        )

    def abandon(self, *, at: datetime) -> Abandoned:
        return Abandoned(
            candidate_name=self.candidate_name,
            role=self.role,
            abandoned_at=at,
        )


@dataclass(frozen=True)
class Sourced(State):
    candidate_name: str
    role: str
    recruiter: str
    sourced_at: datetime

    def __str__(self) -> str:
        return (
            f"{self.candidate_name} sourced by {self.recruiter} for {self.role} "
            f"({format_date(self.sourced_at)})"
        )

    def screen(self, *, score: float, at: datetime) -> Screened:
        return Screened(
            data=CandidateData(
                candidate_name=self.candidate_name,
                role=self.role,
                source=SourcedFromRecruiter(recruiter=self.recruiter),
                screening_score=score,
                screened_at=at,
            )
        )

    def abandon(self, *, at: datetime) -> Abandoned:
        return Abandoned(
            candidate_name=self.candidate_name,
            role=self.role,
            abandoned_at=at,
        )
