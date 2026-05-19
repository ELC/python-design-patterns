from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Rejection:
    reason: str
    at: datetime
