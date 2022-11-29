# Iterator Pattern

## Problem

A CLI developer want to write a ConsolePrinter that can print the content of
arbitrary complex objects.

It should be possible to traverse the object content in a simple way at
compatible with concurrent reads.

## Naive Solution


First, some base classes and objects are defined, in this example, there are
three *container* classes: `Classroom` which has `Students`; `Train` which has
different types of `TrainCar`; and `Memory` which has `float`.

To better illustrate the complexity, each container class uses a different data
structure: `Classroom` uses `set`, `Train` uses `list` and `Memory` uses
`array`. Each of this data structures has different methods and properties.

In the terminology of the pattern, these container classes are called
*Aggregates*.

The code for each is presented below:

```python
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
```

```python
from dataclasses import dataclass, field
from array import array
from typing import MutableSequence


@dataclass
class Memory:
    size: int
    addresses: MutableSequence[float] = field(init=False)

    def __post_init__(self):
        self.addresses = array("f", [0] * self.size)
```

```python
from dataclasses import dataclass


@dataclass
class TrainCar:
    """See https://www.wikiwand.com/en/Railroad_car"""

    length_in_meters: float
    tare_in_kilograms: float


@dataclass
class TankWagon(TrainCar):
    """See https://www.wikiwand.com/en/Tank_car"""

    capacity_in_liters: float


@dataclass
class PassengerCoach(TrainCar):
    """See https://www.wikiwand.com/en/Passenger_car_(rail)"""

    number_of_seats: int


@dataclass
class Locomotive(TrainCar):
    """See https://www.wikiwand.com/en/Passenger_car_(rail)"""

    horse_power: float
    maximum_speed_in_kmh: float


@dataclass
class Train:
    cars: list[TrainCar]

    def __post_init__(self):
        first_car, *_, last_car = self.cars

        if Locomotive not in [type(first_car), type(last_car)]:
            raise ValueError("A train must start or end with a Locomotive")
```


Then, a `ConsoloPrinter` class is defined which can take any of the Aggregate
classes.


```python
from ..iterables import Train, Classroom, Memory


class ConsolePrinter:
    def print(self, collection: Train | Classroom | Memory, alphabetical: bool = False):

        if isinstance(collection, Classroom):
            if alphabetical:
                collection_items = sorted(collection.students, key=lambda x: x.name)
            else:
                collection_items = list(collection.students)

        elif isinstance(collection, Train):
            collection_items = collection.cars

        else:
            collection_items = list(collection.addresses)

        for item in collection_items:
            print(item)
```


Finally, a `main.py` script is defined that uses all the previous defined
classes to show how the `ConsolePrinter` can traverse the different Aggregate
classes.



```python
from .consumer import ConsolePrinter
from .iterables import (
    Train,
    TankWagon,
    PassengerCoach,
    Locomotive,
    Classroom,
    Student,
    Memory,
)


def main():
    train = Train(
        [
            TankWagon(
                length_in_meters=6.10,
                tare_in_kilograms=1250,
                capacity_in_liters=23000,
            ),
            PassengerCoach(
                length_in_meters=6.10,
                tare_in_kilograms=5750,
                number_of_seats=40,
            ),
            Locomotive(
                length_in_meters=23.16,
                tare_in_kilograms=192000,
                horse_power=6000,
                maximum_speed_in_kmh=121,
            ),
        ]
    )

    classroom = Classroom(
        {
            Student("Matthew", 12),
            Student("Sofia", 13),
            Student("Alex", 11),
        }
    )

    memory = Memory(4)

    printer = ConsolePrinter()

    printer.print(train)
    printer.print(classroom, alphabetical=True)
    printer.print(memory)
```

Some of the problems with this solution are:

- It requires to modify `ConsolePrinter` each time there is a new Aggregate.
- `ConsolePrinter` is violating encapsulation by accessing private members of
  the Aggregates.
- It is not clear whether this approach is thread-safe.

Below are different solutions to this problem, the first one is the one
proposed in the GoF Book and the following ones are incremental updates to
incorporate Python native features such as dunder methods (`Iterator`,
`Iterable`, `__iter__` and `__next__`), implicit iterator consumption using
`for`, simplification of iterators using generators and simplify the case for
multiple iterators using the Strategy pattern.

## Solution 01: the GoF Approach

The GoF pattern requires the definition of two abstract classes: `Aggregate`
and `IIterator`:

The IIterator class defines two abstract methods: `next` and `has_more`, it
also uses Generics since the type of the element to be returned by the `next`
method should be provided by the inheriting class.

```python
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
```

The Aggregate class has a single method that generates an iterator, since the
`IIterator` itself is a generic, the Aggregate class must be a generic as well.

```python
from abc import ABC, abstractmethod

from typing import Generic, TypeVar

from .iterator import IIterator

T = TypeVar("T", covariant=True)


class Aggregate(ABC, Generic[T]):
    @abstractmethod
    def create_iterator(self) -> IIterator[T]:
        ...
```

For each of the aggregate classes, an additional iterator class that inherits
from IIterator must be defined.

These classes will have all the logic necessary for the iteration, they can and
should known how the aggregate class works and should expose a generic `next`
method that will return the next element and a `has_more` method that will tell
whether there are more items to fetch.

```python
@dataclass
class TrainIterator(IIterator[TrainCar]):
    cars: list[TrainCar]
    __position: int = 0

    def next(self) -> TrainCar:
        current_car = self.cars[self.__position]
        self.__position += 1
        return current_car

    def has_more(self):
        return self.__position < len(self.cars)
```

```python
@dataclass
class MemoryIterator(IIterator[float]):
    addresses: MutableSequence[float]
    __position: int = 0

    def next(self) -> float:
        current_address = self.addresses[self.__position]
        self.__position += 1
        return current_address

    def has_more(self):
        return self.__position < len(self.addresses)
```

In the particular case of the `Classroom` class, two separate iterators are
defined, one for random ordering and another for alphabetical ordering. To
avoid code duplication, a base abstract class is also defined.

```python
@dataclass
class BaseStudentIterator(IIterator[Student], ABC):
    students: set[Student]
    __position: int = 0
    students_list: list[Student] = field(init=False)

    @abstractmethod
    def __post_init__(self):
        ...

    def next(self) -> Student:
        current_student = self.students_list[self.__position]
        self.__position += 1
        return current_student

    def has_more(self):
        return self.__position < len(self.students_list)


@dataclass
class RandomStudentIterator(BaseStudentIterator):
    def __post_init__(self):
        self.students_list = list(self.students)


@dataclass
class AlphabeticalStudentIterator(BaseStudentIterator):
    def __post_init__(self):
        self.students_list = sorted(self.students, key=lambda x: x.name)
```


To use these different iterator classes into the Aggregates some changes are
needed. In the case of `Train` and `Memory` the `create_iterator` method is
added to be compliant with the `Aggregate` abstract class.

```diff
from dataclasses import dataclass
+from .iterator import IIterator
+from .aggregate import Aggregate

...

@dataclass
-class Train:
+class Train(Aggregate[TrainCar]):
    cars: list[TrainCar]

    def __post_init__(self):
        first_car, *_, last_car = self.cars

        if Locomotive not in [type(first_car), type(last_car)]:
            raise ValueError("A train must start or end with a Locomotive")

+    def create_iterator(self) -> IIterator[TrainCar]:
+        return TrainIterator(self.cars)
```


```diff
+from .iterator import IIterator
+from .aggregate import Aggregate

@dataclass
-class Memory:
+class Memory(Aggregate[float]):
    size: int
    addresses: MutableSequence[float] = field(init=False)

    def __post_init__(self):
        self.addresses = array("f", [0] * self.size)
    
+    def create_iterator(self) -> IIterator[float]:
+        return MemoryIterator(self.addresses)
```

For the `Classroom` class, since more than one iterator is possible (random and
alphabetical), an extra attribute `iterator_strategy` is added. This attribute
will be a class that will get instantiated when `create_iterator` is called.

```diff
-from dataclasses import dataclass
+from dataclasses import dataclass, field
+from abc import ABC, abstractmethod

+from typing import Type

+from .iterator import IIterator
+from .aggregate import Aggregate

...

@dataclass
-class Classroom:
+class Classroom(Aggregate[Student]):
    students: set[Student]
+    iterator_strategy: Type[BaseStudentIterator] = RandomStudentIterator
+
+    def create_iterator(self) -> IIterator[Student]:
+        return self.iterator_strategy(self.students)

```

Now that the way the classes are organized has changed, the `ConsolePrinter`
must be adapted.

Since the `ConsolePrinter` will print the content, a suitable Protocol called
`PrintableItem` is defined to be passed to the Aggregate Generic.

Then the references to the particular aggregates are removed and are replaced
by the abstract `Aggregate` and the if-else logic is replaced with a simple
while-loop.

The while iterates over the collection generated by the `create_iterator`
method and the stoping condition is reached by checking the `has_more` method.
The item is obtained in each iteration by calling the `next` method.

```diff
-from ..iterables import Train, Classroom, Memory

+from ..iterables import Aggregate

+from typing import Protocol


+class PrintableItem(Protocol):
+    def __str__(self) -> str:
+        ...


class ConsolePrinter:
-    def print(self, collection: Train | Classroom | Memory, alphabetical: bool = False):
+    def print(self, collection: Aggregate[PrintableItem]):

-        if isinstance(collection, Classroom):
-            if alphabetical:
-                collection_items = sorted(collection.students, key=lambda x: x.name)
-            else:
-                collection_items = list(collection.students)
-
-        elif isinstance(collection, Train):
-            collection_items = collection.cars
-
-        else:
-            collection_items = list(collection.addresses)
-
-        for item in collection_items:

+       iterator = collection.create_iterator()
+       while iterator.has_more():
+           item = iterator.next()
            print(item)
```

Finally the `main.py` script is modified accordingly:

```diff
from .iterables import (
    ...
+    AlphabeticalStudentIterator,
)


def main():
    ...

    classroom = Classroom(
        ...
    )

+    classroom.iterator_strategy = AlphabeticalStudentIterator

    memory = Memory(4)

    printer = ConsolePrinter()

    printer.print(train)
-    printer.print(classroom, alphabetical=True)
+    printer.print(classroom)
    printer.print(memory)

```

The GoF solution is already introducing a lot of code and complexity to
implement this pattern. This extra complexity is not worth it for this such
simple data structures. However in the following solutions it is shown how the
code could be simplified by great amount.

## Solution 02: the GoF Approach Using dunder methods

The traditional GoF implementation has an abstract `Aggregate` and `IIterator`
classes, however, Python already have such classes available under the
`collections.abc` module of the Standard Library. The classes are called
`Iterable` (replacing Aggregate) and `Iterator` (replacing IIterator).

These two classes do not specify a `create_iterator`, `next` or `has_more`
methods, instead, they rely on the `__iter__` and `__next__` methods.

The first thing to implement these changes is to remove the `Aggregate` and
`IIterator` classes.

```diff
-from abc import ABC, abstractmethod
-from typing import TypeVar, Generic
-
-T = TypeVar("T")
-
-
-class IIterator(ABC, Generic[T]):
-    @abstractmethod
-    def next(self) -> T:
-        ...
-
-    @abstractmethod
-    def has_more(self) -> bool:
-        ...
```

```diff
-from abc import ABC, abstractmethod
-
-from typing import Generic, TypeVar
-
-from .iterator import IIterator
-
-T = TypeVar("T", covariant=True)
-
-
-class Aggregate(ABC, Generic[T]):
-    @abstractmethod
-    def create_iterator(self) -> IIterator[T]:
-        ...
```

Then, the different iterator classes are adapted to use the `Iterator` and
`Iterable` classes. The changes are minimal in each class:

- The `Aggregate` and `IIterator` classes are replaced by `Iterator` and
  `Iterable` respectively
- The method `create_iterator` is renamed to `__iter__`
- The method `next` is renamed to `__next__`
- The method `has_more` is removed and its logic is reversed and moved to the
  `__next__` method

```diff
from dataclasses import dataclass
-from .iterator import IIterator
-from .aggregate import Aggregate

+from collections.abc import Iterator, Iterable

...


@dataclass
-class Train(Aggregate[TrainCar]):
+class Train(Iterable[TrainCar]):
    cars: list[TrainCar]

    ...

-    def create_iterator(self) -> IIterator[TrainCar]:
+    def __iter__(self) -> Iterator[TrainCar]:
        return TrainIterator(self.cars)


@dataclass
-class TrainIterator(IIterator[TrainCar]):
+class TrainIterator(Iterator[TrainCar]):
    cars: list[TrainCar]
    __position: int = 0

-    def next(self) -> TrainCar:
+    def __next__(self) -> TrainCar:
+        if self.__position == len(self.cars):
+            raise StopIteration()
        current_car = self.cars[self.__position]
        self.__position += 1
        return current_car

-    def has_more(self):
-        return self.__position < len(self.cars)

```


```diff
+from collections.abc import Iterator, Iterable

-from .iterator import IIterator
-from .aggregate import Aggregate


@dataclass
-class Memory(Aggregate[float]):
+class Memory(Iterable[float]):
    size: int
    addresses: MutableSequence[float] = field(init=False)

    def __post_init__(self):
        self.addresses = array("f", [0] * self.size)

-    def create_iterator(self) -> IIterator[float]:
+    def __iter__(self) -> Iterator[float]:
        return MemoryIterator(self.addresses)


@dataclass
-class MemoryIterator(IIterator[float]):
+class MemoryIterator(Iterator[float]):
    addresses: MutableSequence[float]
    __position: int = 0

-    def next(self) -> float:
+    def __next__(self) -> float:
+        if self.__position == len(self.addresses):
+            raise StopIteration()
        current_address = self.addresses[self.__position]
        self.__position += 1
        return current_address

-    def has_more(self):
-        return self.__position < len(self.addresses)
```

```diff
+from collections.abc import Iterator, Iterable

-from .iterator import IIterator
-from .aggregate import Aggregate


@dataclass
-class BaseStudentIterator(IIterator[Student], ABC):
+class BaseStudentIterator(Iterator[Student], ABC):
    students: set[Student]
    __position: int = 0
    students_list: list[Student] = field(init=False)

    @abstractmethod
    def __post_init__(self):
        ...

-    def next(self) -> Student:
+    def __next__(self) -> Student:
+        if self.__position == len(self.students_list):
+            raise StopIteration()
+
        current_student = self.students_list[self.__position]
        self.__position += 1
        return current_student

-    def has_more(self):
-        return self.__position < len(self.students_list)

@dataclass
-class Classroom(Aggregate[Student]):
+class Classroom(Iterable[Student]):
    students: set[Student]
    iterator_strategy: Type[BaseStudentIterator] = RandomStudentIterator

-    def create_iterator(self) -> IIterator[Student]:
+    def __iter__(self) -> Iterator[Student]:
        return self.iterator_strategy(self.students)
```

The `ConsolePrinter` is also changed to remove the dependencies on `Aggregate`.
The while loop is kept but now a try-except is used to leverage the the
`StopIteration` exception that is built in to the language.

```diff
-from ..iterables import Aggregate
+from collections.abc import Iterable

...

class ConsolePrinter:
-    def print(self, collection: Aggregate[PrintableItem]):
-
-        iterator = collection.create_iterator()
-
-        while iterator.has_more():
-            item = iterator.next()
-            print(item)
+    def print(self, collection: Iterable[PrintableItem]):
+   
+        iterator = iter(collection)
+   
+        while True:
+            try:
+                item = next(iterator)
+                print(item)
+            except StopIteration:
+                break
```

No changes are needed in the `main.py` script.

This solution enhances the GoF traditional approach by leveraging Python native
constructs. It still has significant more code than the naive approach but that
is going to be mitigated in the upcomming improvements.

## Solution 03: the GoF Approach Using dunder methods and for syntax

With the current implementation, it is also possible to leverage the built-in
`for` loop instead of the while loop. By using the for loop, the handling of
the `StopIteration` happens under the hood and no explicit manipulation is
needed.

The only file that needs to be changed is the `ConsolePrinter`:

```diff
...

class ConsolePrinter:
    def print(self, collection: Iterable[PrintableItem]):

        iterator = iter(collection)

-        while True:
-            try:
-                item = next(iterator)
-                print(item)
-            except StopIteration:
-                break
+        for item in collection:
+            print(item)
```

## Solution 04: Refactor to use generators

Python has native support for generators, generators allows the dynamic
creation of iterator objects. By using generators it is possible to combine the
`Aggregate` and the `Iterator` class in a single class without sacrificing
thread-safety.

To use a generator in Python, the keyword `yield` is used in the `__iter__`
method. This method combines the iteration logic of the iterator class in the
`Aggregate` class.

```diff
...


@dataclass
class Memory(Iterable[float]):
    size: int
    addresses: MutableSequence[float] = field(init=False)

    def __post_init__(self):
        self.addresses = array("f", [0] * self.size)

    def __iter__(self) -> Iterator[float]:
+        for address in self.addresses:
+            yield address
-        return MemoryIterator(self.addresses)
-
-
-@dataclass
-class MemoryIterator(Iterator[float]):
-    addresses: MutableSequence[float]
-    __position: int = 0
-
-    def __next__(self) -> float:
-        if self.__position == len(self.addresses):
-            raise StopIteration()
-
-        current_address = self.addresses[self.__position]
-        self.__position += 1
-        return current_address
```

```diff
...


@dataclass
class Train(Iterable[TrainCar]):
    cars: list[TrainCar]

    def __post_init__(self):
        first_car, *_, last_car = self.cars

        if Locomotive not in [type(first_car), type(last_car)]:
            raise ValueError("A train must start or end with a Locomotive")

    def __iter__(self) -> Iterator[TrainCar]:
+        for car in self.cars:
+            yield car    
-        return TrainIterator(self.cars)
-
-
-@dataclass
-class TrainIterator(Iterator[TrainCar]):
-    cars: list[TrainCar]
-    __position: int = 0

-    def __next__(self) -> TrainCar:
-        if self.__position == len(self.cars):
-            raise StopIteration()

-        current_car = self.cars[self.__position]
-        self.__position += 1
-        return current_car
```

In the case of the `Classroom` class, since there are multiple iterators, the
separate iterator class is kept and the `__iter__` method is defined there as
well.


```diff
...

@dataclass
-class BaseStudentIterator(Iterator[Student], ABC):
+class BaseStudentIterator(Iterable[Student], ABC):
    students: set[Student]
    __position: int = 0
    students_list: list[Student] = field(init=False)

    @abstractmethod
    def __post_init__(self):
        ...

+    def __iter__(self) -> Iterator[Student]:
+        for student in self.students_list:
+            yield student
-    def __next__(self) -> Student:
-        if self.__position == len(self.students_list):
-            raise StopIteration()
-
-        current_student = self.students_list[self.__position]
-        self.__position += 1
-        return current_student

...

@dataclass
class Classroom(Iterable[Student]):
    students: set[Student]
    iterator_strategy: Type[BaseStudentIterator] = RandomStudentIterator

    def __iter__(self) -> Iterator[Student]:
-        return self.iterator_strategy(self.students)
+        for student in self.iterator_strategy(self.students):
+            yield student
```

These changes have no impact on the `ConsolePrinter` and the `main.py`. This
change is the one that introduces one of Python features and it allows
significant code reduction while keeping functionality.


## Solution 05: Refactor to use simplify multiple iterators

As already explained in the Strategy Pattern section, it is possible to replace
classes with a single purposeful method with functions and pass those functions
as parameters when needed.

This is the case for the multiple iterators available for the `Classroom`
classs. By replacing them with functions, they can be used directly through the
`iterator_strategy` attribute.

One additional modification is the use of the construct `yield from` which is
equivalent to a `return` in this context but allows for lazy evaluation. In
this case all objects are in memory and there is no change but if these were
for example HTTP connection objects, the `yield from` would allow to pass one
at the time and avoid having multiple connections open simultaneously.

```diff
-from abc import ABC, abstractmethod
-from dataclasses import dataclass, field
+from dataclasses import dataclass

from collections.abc import Iterator, Iterable

-from typing import Type
+from typing import Callable


...


-@dataclass
-class BaseStudentIterator(Iterable[Student], ABC):
-    students: set[Student]
-    __position: int = 0
-    students_list: list[Student] = field(init=False)
-
-    @abstractmethod
-    def __post_init__(self):
-        ...
-
-    def __iter__(self) -> Iterator[Student]:
-        for student in self.students_list:
-            yield student


-@dataclass
-class RandomStudentIterator(BaseStudentIterator):
-    def __post_init__(self):
-        self.students_list = list(self.students)
+def random_student_iterator(students: set[Student]) -> Iterator[Student]:
+    yield from iter(students)



-@dataclass
-class AlphabeticalStudentIterator(BaseStudentIterator):
-    def __post_init__(self):
-        self.students_list = sorted(self.students, key=lambda x: x.name)
+def alphabetical_student_iterator(students: set[Student]) -> Iterator[Student]:
+    yield from sorted(students, key=lambda x: x.name)


@dataclass
class Classroom(Iterable[Student]):
    students: set[Student]
-    iterator_strategy: Type[BaseStudentIterator] = RandomStudentIterator
+    iterator_strategy: Callable[[set[Student]], Iterator[Student]] = random_student_iterator

    def __iter__(self) -> Iterator[Student]:
        for student in self.iterator_strategy(self.students):
            yield student
```

Even though the changes were not trivial in the `classroom.py` file, the
modifications needed in the `main.py` are minimal, since only the names changed
to follow the convention.

```diff
from .iterables import (
    ...
-    AlphabeticalStudentIterator,
+    alphabetical_student_iterator,
)


def main():
    ...

-    classroom.iterator_strategy = AlphabeticalStudentIterator
+    classroom.iterator_strategy = alphabetical_student_iterator

    ...
```

In the end, the final solution has a similar amount of lines of code than the
naive solution, but it has none of the disadvantages while at the same time
implements the Iterator pattern in a way that native Python features are used.


## Comparison Table

|                               | Problem | Solution 01 | Solution 02 | Solution 03 | Solution 04 | Solution 05 |
|-------------------------------|---------|-------------|-------------|-------------|-------------|-------------|
| Total Cyclomatic Complexity   | 28      | 55          | 53          | 51          | 46          | 36          |
| Average Cyclomatic Complexity | 2.00    | 1.45        | 1.77        | 1.70        | 1.77        | 1.71        |
| Average Maintainability Index | 88.18   | 83.48       | 79.53       | 79.53       | 87.52       | 87.52       |
| LOC                           | 159     | 278         | 248         | 242         | 213         | 195         |
| LLOC                          | 90      | 173         | 153         | 148         | 124         | 105         |
| SLOC                          | 114     | 199         | 177         | 172         | 152         | 138         |