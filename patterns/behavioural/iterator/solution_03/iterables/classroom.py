from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from collections.abc import Iterator, Iterable

from typing import Type


@dataclass
class Student:
    name: str
    age: float

    def __hash__(self):
        return hash(f"{self.name}-{self.age}")


@dataclass
class BaseStudentIterator(Iterator[Student], ABC):
    students: set[Student]
    __position: int = 0
    students_list: list[Student] = field(init=False)

    @abstractmethod
    def __post_init__(self):
        ...

    def __next__(self) -> Student:
        if self.__position == len(self.students_list):
            raise StopIteration()

        current_student = self.students_list[self.__position]
        self.__position += 1
        return current_student


@dataclass
class RandomStudentIterator(BaseStudentIterator):
    def __post_init__(self):
        self.students_list = list(self.students)


@dataclass
class AlphabeticalStudentIterator(BaseStudentIterator):
    def __post_init__(self):
        self.students_list = sorted(self.students, key=lambda x: x.name)


@dataclass
class Classroom(Iterable[Student]):
    students: set[Student]
    iterator_strategy: Type[BaseStudentIterator] = RandomStudentIterator

    def __iter__(self) -> Iterator[Student]:
        return self.iterator_strategy(self.students)
