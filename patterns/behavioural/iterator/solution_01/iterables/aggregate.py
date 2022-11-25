from abc import ABC, abstractmethod

from typing import Generic, TypeVar

from .iterator import IIterator

T = TypeVar("T", covariant=True)


class Aggregate(ABC, Generic[T]):
    @abstractmethod
    def create_iterator(self) -> IIterator[T]:
        ...
