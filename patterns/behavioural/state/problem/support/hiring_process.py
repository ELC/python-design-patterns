from collections.abc import MutableSequence, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Self

from .description import HiringProcessDescription
from .errors import InvalidTransition
from .hiring_state import HiringState
from .interview import Interviewer, InterviewRound
from .rejection import Rejection
from .source import DirectApplication, Source, SourcedFromRecruiter


@dataclass
class HiringProcess:
    state: HiringState
    candidate_name: str
    role: str
    recruiter: str | None = None
    applied_at: datetime | None = None
    sourced_at: datetime | None = None
    source: Source | None = None
    screening_score: float | None = None
    screened_at: datetime | None = None
    rounds: MutableSequence[InterviewRound] = field(
        default_factory=list[InterviewRound]
    )
    offer_salary: Decimal | None = None
    offer_at: datetime | None = None
    offer_expires_at: datetime | None = None
    start_date: date | None = None
    hire_at: datetime | None = None
    employee_id: str | None = None
    rejections: MutableSequence[Rejection] = field(default_factory=list[Rejection])
    abandoned_at: datetime | None = None

    @classmethod
    def applied(cls, *, candidate_name: str, role: str, at: datetime) -> Self:
        return cls(
            state=HiringState.APPLIED,
            candidate_name=candidate_name,
            role=role,
            applied_at=at,
        )

    @classmethod
    def sourced(
        cls,
        *,
        candidate_name: str,
        role: str,
        recruiter: str,
        at: datetime,
    ) -> Self:
        return cls(
            state=HiringState.SOURCED,
            candidate_name=candidate_name,
            role=role,
            recruiter=recruiter,
            sourced_at=at,
        )

    def __str__(self) -> str:
        return str(HiringProcessDescription(self))

    def screen(self, *, score: float, at: datetime) -> Self:
        if self.state not in (
            HiringState.APPLIED,
            HiringState.SOURCED,
            HiringState.REJECTED,
        ):
            raise InvalidTransition(
                f"screen is not allowed from {self.state.name}; "
                f"allowed states: APPLIED, SOURCED, REJECTED"
            )
        if self.state is HiringState.APPLIED:
            self.source = DirectApplication()
        elif self.state is HiringState.SOURCED:
            assert self.recruiter is not None
            self.source = SourcedFromRecruiter(recruiter=self.recruiter)
        self.screening_score = score
        self.screened_at = at
        self.state = HiringState.SCREENED
        return self

    def interview(
        self,
        *,
        panel: Sequence[Interviewer],
        notes: str,
        at: datetime,
    ) -> Self:
        if self.state not in (
            HiringState.SCREENED,
            HiringState.INTERVIEWED,
            HiringState.REJECTED,
        ):
            raise InvalidTransition(
                f"interview is not allowed from {self.state.name}; "
                f"allowed states: SCREENED, INTERVIEWED, REJECTED"
            )
        round_entry = InterviewRound(panel=panel, notes=notes, at=at)
        self.rounds.append(round_entry)
        self.state = HiringState.INTERVIEWED
        return self

    def make_offer(
        self,
        *,
        offer_salary: Decimal,
        offer_expires_at: datetime,
        at: datetime,
    ) -> Self:
        if self.state is not HiringState.INTERVIEWED:
            raise InvalidTransition(
                f"make_offer is not allowed from {self.state.name}; "
                f"allowed states: INTERVIEWED"
            )
        self.offer_salary = offer_salary
        self.offer_at = at
        self.offer_expires_at = offer_expires_at
        self.state = HiringState.OFFER_EXTENDED
        return self

    def hire(self, *, start_date: date, employee_id: str, at: datetime) -> Self:
        if self.state is not HiringState.OFFER_EXTENDED:
            raise InvalidTransition(
                f"hire is not allowed from {self.state.name}; "
                f"allowed states: OFFER_EXTENDED"
            )
        self.start_date = start_date
        self.employee_id = employee_id
        self.hire_at = at
        self.state = HiringState.HIRED
        return self

    def reject(self, *, reason: str, at: datetime) -> Self:
        if self.state not in (
            HiringState.SCREENED,
            HiringState.INTERVIEWED,
            HiringState.OFFER_EXTENDED,
        ):
            raise InvalidTransition(
                f"reject is not allowed from {self.state.name}; "
                f"allowed states: SCREENED, INTERVIEWED, OFFER_EXTENDED"
            )
        self.rejections.append(Rejection(reason=reason, at=at))
        self.state = HiringState.REJECTED
        return self

    def abandon(self, *, at: datetime) -> Self:
        if self.state not in (
            HiringState.APPLIED,
            HiringState.SOURCED,
            HiringState.SCREENED,
            HiringState.INTERVIEWED,
            HiringState.OFFER_EXTENDED,
            HiringState.REJECTED,
        ):
            raise InvalidTransition(
                f"abandon is not allowed from {self.state.name}; "
                f"allowed states: APPLIED, SOURCED, SCREENED, INTERVIEWED, "
                f"OFFER_EXTENDED, REJECTED"
            )
        self.abandoned_at = at
        self.state = HiringState.ABANDONED
        return self
