from dataclasses import dataclass, field
from array import array

from typing import MutableSequence
from collections.abc import Iterator, Iterable


@dataclass
class Memory(Iterable[float]):
    size: int
    addresses: MutableSequence[float] = field(init=False)

    def __post_init__(self):
        self.addresses = array("f", [0] * self.size)

    def __iter__(self) -> Iterator[float]:
        return MemoryIterator(self.addresses)


@dataclass
class MemoryIterator(Iterator[float]):
    addresses: MutableSequence[float]
    __position: int = 0

    def __next__(self) -> float:
        if self.__position == len(self.addresses):
            raise StopIteration()

        current_address = self.addresses[self.__position]
        self.__position += 1
        return current_address
