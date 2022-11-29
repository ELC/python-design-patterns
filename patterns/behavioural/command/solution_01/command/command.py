from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, Any

T = TypeVar("T", bound=Any, covariant=True)

@dataclass
class Command(ABC, Generic[T]):
    receiver: T
      
    @abstractmethod
    def execute(self) -> None:
        ...

    @abstractmethod
    def undo(self) -> None:
        ...
