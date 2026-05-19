from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import TYPE_CHECKING

from .errors import InvalidCandidateState
from .hiring_state import HiringState
from .source import DirectApplication, SourcedFromRecruiter

if TYPE_CHECKING:
    from .hiring_process import HiringProcess


@dataclass(frozen=True)
class HiringProcessDescription:
    process: HiringProcess

    def __str__(self) -> str:
        match self.process.state:
            case HiringState.APPLIED:
                return self._applied()
            case HiringState.SOURCED:
                return self._sourced()
            case HiringState.SCREENED:
                return self._screened()
            case HiringState.INTERVIEWED:
                return self._interviewed()
            case HiringState.OFFER_EXTENDED:
                return self._offer_extended()
            case HiringState.REJECTED:
                return self._rejected()
            case HiringState.HIRED:
                return self._hired()
            case HiringState.ABANDONED:
                return self._abandoned()

    @staticmethod
    def _format_date(value: datetime | date) -> str:
        return value.strftime("%Y-%m-%d")

    def _applied(self) -> str:
        if self.process.applied_at is None:
            raise InvalidCandidateState(
                state=HiringState.APPLIED,
                detail="requires an application timestamp",
            )
        return (
            f"{self.process.candidate_name} applied for {self.process.role} "
            f"({self._format_date(self.process.applied_at)})"
        )

    def _sourced(self) -> str:
        if self.process.recruiter is None or self.process.sourced_at is None:
            raise InvalidCandidateState(
                state=HiringState.SOURCED,
                detail="requires a recruiter and sourcing timestamp",
            )
        return (
            f"{self.process.candidate_name} sourced by {self.process.recruiter} "
            f"for {self.process.role} "
            f"({self._format_date(self.process.sourced_at)})"
        )

    def _screened(self) -> str:
        if self.process.screened_at is None:
            raise InvalidCandidateState(
                state=HiringState.SCREENED,
                detail="requires a screening timestamp",
            )
        screened_on = self._format_date(self.process.screened_at)
        match self.process.source:
            case DirectApplication():
                return f"screened (direct, {screened_on})"
            case SourcedFromRecruiter(recruiter=recruiter):
                return f"screened (via {recruiter}, {screened_on})"
            case None:
                raise InvalidCandidateState(
                    state=HiringState.SCREENED,
                    detail="requires a screening source",
                )

    def _interviewed(self) -> str:
        if len(self.process.rounds) == 0:
            raise InvalidCandidateState(
                state=HiringState.INTERVIEWED,
                detail="requires at least one interview round",
            )
        round_dates = ", ".join(
            round_entry.at.strftime("%Y-%m-%d") for round_entry in self.process.rounds
        )
        return f"interviewed -- rounds: {round_dates}"

    def _offer_extended(self) -> str:
        if (
            self.process.offer_salary is None
            or self.process.offer_at is None
            or self.process.offer_expires_at is None
        ):
            raise InvalidCandidateState(
                state=HiringState.OFFER_EXTENDED,
                detail="requires offer salary, offer timestamp, and expiry",
            )
        return (
            f"offer extended ({self.process.offer_salary}, "
            f"{self._format_date(self.process.offer_at)}, "
            f"expires {self._format_date(self.process.offer_expires_at)})"
        )

    def _rejected(self) -> str:
        if len(self.process.rejections) == 0:
            raise InvalidCandidateState(
                state=HiringState.REJECTED,
                detail="requires at least one rejection",
            )
        latest = self.process.rejections[-1]
        return f"rejected: {latest.reason} ({self._format_date(latest.at)})"

    def _hired(self) -> str:
        if (
            self.process.employee_id is None
            or self.process.hire_at is None
            or self.process.start_date is None
        ):
            raise InvalidCandidateState(
                state=HiringState.HIRED,
                detail="requires employee id, hire timestamp, and start date",
            )
        return (
            f"hired ({self.process.employee_id}, "
            f"{self._format_date(self.process.hire_at)}, "
            f"starts {self._format_date(self.process.start_date)})"
        )

    def _abandoned(self) -> str:
        if self.process.abandoned_at is None:
            raise InvalidCandidateState(
                state=HiringState.ABANDONED,
                detail="requires an abandonment timestamp",
            )
        return f"abandoned ({self._format_date(self.process.abandoned_at)})"
