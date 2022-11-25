from dataclasses import dataclass, field
from array import array

from .iterator import IIterator
from .aggregate import Aggregate
from typing import MutableSequence


@dataclass
class Memory(Aggregate[float]):
    size: int
    addresses: MutableSequence[float] = field(init=False)

    def __post_init__(self):
        self.addresses = array("f", [0] * self.size)

    def create_iterator(self) -> IIterator[float]:
        return MemoryIterator(self.addresses)


@dataclass
class MemoryIterator(IIterator[float]):
    addresses: MutableSequence[float]
    __position: int = 0

    def next(self) -> float:
        current_address = self.addresses[self.__position]
        self.__position += 1
        return current_address

    def has_more(self):
        return self.__position < len(self.addresses)
