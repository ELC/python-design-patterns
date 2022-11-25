from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class IIterator(ABC, Generic[T]):
    @abstractmethod
    def next(self) -> T:
        ...

    @abstractmethod
    def has_more(self) -> bool:
        ...
