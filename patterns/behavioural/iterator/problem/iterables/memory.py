from dataclasses import dataclass, field
from array import array
from typing import MutableSequence


@dataclass
class Memory:
    size: int
    addresses: MutableSequence[float] = field(init=False)

    def __post_init__(self):
        self.addresses = array("f", [0] * self.size)
