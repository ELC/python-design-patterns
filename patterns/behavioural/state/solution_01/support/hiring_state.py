from enum import StrEnum, auto


class HiringState(StrEnum):
    APPLIED = auto()
    SOURCED = auto()
    SCREENED = auto()
    INTERVIEWED = auto()
    OFFER_EXTENDED = auto()
    HIRED = auto()
    REJECTED = auto()
    ABANDONED = auto()
