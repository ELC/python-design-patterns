from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Self

from .interview import Interviewer
from .states import State


@dataclass
class HiringProcess:
    state: State

    def __str__(self) -> str:
        return str(self.state)

    def screen(self, *, score: float, at: datetime) -> Self:
        self.state = self.state.screen(score=score, at=at)
        return self

    def interview(
        self,
        *,
        panel: Sequence[Interviewer],
        notes: str,
        at: datetime,
    ) -> Self:
        self.state = self.state.interview(panel=panel, notes=notes, at=at)
        return self

    def make_offer(
        self,
        *,
        offer_salary: Decimal,
        offer_expires_at: datetime,
        at: datetime,
    ) -> Self:
        self.state = self.state.make_offer(
            offer_salary=offer_salary,
            offer_expires_at=offer_expires_at,
            at=at,
        )
        return self

    def hire(self, *, start_date: date, employee_id: str, at: datetime) -> Self:
        self.state = self.state.hire(
            start_date=start_date,
            employee_id=employee_id,
            at=at,
        )
        return self

    def reject(self, *, reason: str, at: datetime) -> Self:
        self.state = self.state.reject(reason=reason, at=at)
        return self

    def abandon(self, *, at: datetime) -> Self:
        self.state = self.state.abandon(at=at)
        return self
