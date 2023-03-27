from abc import ABC, abstractmethod

from dataclasses import dataclass
from typing import Callable, Self


@dataclass
class FileType(ABC):
    name: str = ""

    @abstractmethod
    def accept(self, visitor: Callable[[Self], None]) -> None:
        visitor(self)
