from dataclasses import dataclass


@dataclass
class Student:
    name: str
    age: float

    def __hash__(self):
        return hash(f"{self.name}-{self.age}")


@dataclass
class Classroom:
    students: set[Student]
