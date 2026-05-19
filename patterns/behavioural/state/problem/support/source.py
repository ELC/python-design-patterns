from dataclasses import dataclass


@dataclass(frozen=True)
class DirectApplication:
    pass


@dataclass(frozen=True)
class SourcedFromRecruiter:
    recruiter: str


type Source = DirectApplication | SourcedFromRecruiter
