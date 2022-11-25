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
        for address in self.addresses:
            yield address
