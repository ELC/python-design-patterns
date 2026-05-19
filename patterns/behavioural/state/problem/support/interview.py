from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Interviewer:
    name: str
    title: str


@dataclass(frozen=True)
class InterviewRound:
    panel: Sequence[Interviewer]
    notes: str
    at: datetime
