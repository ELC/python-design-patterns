from dataclasses import dataclass

from collections.abc import Iterator, Iterable

from typing import Callable


@dataclass
class Student:
    name: str
    age: float

    def __hash__(self):
        return hash(f"{self.name}-{self.age}")


def random_student_iterator(students: set[Student]) -> Iterator[Student]:
    yield from iter(students)


def alphabetical_student_iterator(students: set[Student]) -> Iterator[Student]:
    yield from sorted(students, key=lambda x: x.name)


@dataclass
class Classroom(Iterable[Student]):
    students: set[Student]
    iterator_strategy: Callable[
        [set[Student]], Iterator[Student]
    ] = random_student_iterator

    def __iter__(self) -> Iterator[Student]:
        for student in self.iterator_strategy(self.students):
            yield student
