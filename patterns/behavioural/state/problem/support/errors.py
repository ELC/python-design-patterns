from dataclasses import dataclass

from .hiring_state import HiringState


class InvalidTransition(Exception):
    pass


@dataclass
class InvalidCandidateState(Exception):
    state: HiringState
    detail: str

    def __post_init__(self) -> None:
        super().__init__(f"{self.state.name} cannot be described: {self.detail}")
