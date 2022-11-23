# Strategy Pattern

## Problem

A Company's service desk wants to incorporate several approaches to handle
support tickets, each ticket has a customer name, a description, and an unique
id. Moreover, the tickets should have a meaningful console representation.

At the moment there are only three approaches planned: FIFO, FILO and Random.
However, the system should be able to incorporate more complex approaches in
the feature without changing the code for the existing ones.

**Develop a solution for the stated problem before continue reading**

## Naive Solution

Without knowledge of this pattern, one may develop a solution that looks like
the following.

First, the ticket class is defined:

```python
import uuid
from dataclasses import dataclass, field


@dataclass
class SupportTicket:
    customer: str
    issue: str
    id: str = field(init=False)

    def __post_init__(self) -> None:
        self.id = uuid.uuid4().hex

    def __str__(self) -> str:
        return (
            "=================================="
            f"Processing ticket id: {self.id}"
            f"Customer: {self.customer}"
            f"Issue: {self.issue}"
            "=================================="
        )

    def process(self) -> None:
        print(str(self))
```

Then, the different strategies could be represented with an `Enum`:


```python
from enum import Enum, auto

class ProcessingTypes(Enum):
    FIFO = auto()
    FILO = auto()
    RANDOM = auto()
```

The core of the business logic will be the execution of some particular
strategy, this could be accomplished by a `CustomerSupport` class:

```python
import random
from dataclasses import dataclass, field
from typing import List, Any

from .ticket import SupportTicket

@dataclass
class CustomerSupport:
    tickets: List[SupportTicket] = field(default_factory=list)

    def add_ticket(self, ticket: SupportTicket) -> None:
        self.tickets.append(ticket)

    def process_tickets(
        self, 
        processing_strategy: ProcessingTypes = ProcessingTypes.FIFO, 
        **kwargs: Any,
    ) -> None:
        if len(self.tickets) == 0:
            print("There are no tickets to process. Well done!")
            return

        if processing_strategy is ProcessingTypes.FIFO:
            for ticket in self.tickets:
                ticket.process()
            return

        if processing_strategy is ProcessingTypes.FILO:
            for ticket in reversed(self.tickets):
                ticket.process()
            return

        if processing_strategy is ProcessingTypes.RANDOM:
            seed = kwargs.get("seed")

            if seed is None:
                random.seed(seed)

            random_list = random.sample(self.tickets, len(self.tickets))
            for ticket in random_list:
                ticket.process()

            return

        raise NotImplementedError
```

Finally, a `main` script to run the application:


```python
from .support import CustomerSupport, ProcessingTypes, SupportTicket


def main() -> None:
    app = CustomerSupport()

    tickets = [
        SupportTicket("John Smith", "My computer makes strange sounds!"),
        SupportTicket("Linus Sebastian", "I can't upload any videos, please help."),
        SupportTicket("Arjan Codes", "VSCode doesn't automatically solve my bugs."),
    ]

    for ticket in tickets:
        app.add_ticket(ticket)

    app.process_tickets(ProcessingTypes.RANDOM, seed=5)


if __name__ == "__main__":
    main()

```


Some of the problems with this solution are:

- It requires to modify `CustomerSupport` each time there is a new approach
- The function `process_tickets` will become larger and larger
- Managing optional parameters for different strategies will produce many
  validations in `process_tickets`

Below are different solutions to this problem, the first one is the one
proposed in the GoF Book and the following ones are incremental updates to
incorporate Python native Features such as Duck Typing (`Protocols`), Class
callables (`__call__`), and stateful functions (`closures`), then the an
alternative to closures is presented in the form of partial evaluation, finally
a way to parse user input is introduced.

## Solution 1: GoF Approach


The solution that GoF proposes is to abstract the logic of the strategy to
follow into an Abstract Class, and then create concrete classes that overwrites
the specific method of the abstract class they inherit from.

This introduces some changes to the `app.py`

### `app.py`


The new abstract class is added:


```diff
+from abc import ABC, abstractmethod
+from typing import List, Optional

+class TicketOrderingStrategy(ABC):
+    @abstractmethod
+    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
+        ...
```

The strategies are rewritten as concrete implementations of the abstract class
and the enum is removed.

```diff
-class ProcessingTypes(Enum):
-    FIFO = auto()
-    FILO = auto()
-    RANDOM = auto()
+
+class FIFOOrderingStrategy(TicketOrderingStrategy):
+    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
+        return tickets.copy()
+
+
+class FILOOrderingStrategy(TicketOrderingStrategy):
+    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
+        return list(reversed(tickets))
+
+
+@dataclass
+class RandomOrderingStrategy(TicketOrderingStrategy):
+    seed: Optional[int] = None
+
+    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
+        if self.seed is not None:
+            random.seed(self.seed)
+        return random.sample(tickets, len(tickets))
```

Finally the `CustomerSupport` class is refactored to take the new
implementation. This change makes the `CustomerSupport` class fully agnostic of
the particular strategy that it is going to be executed.

```diff

@dataclass
class CustomerSupport:
    ...

    def process_tickets(
        self,
-       processing_strategy: ProcessingTypes = ProcessingTypes.FIFO,
-       **kwargs: Any,
+       processing_strategy: TicketOrderingStrategy
    ) -> None:

        if len(self.tickets) == 0:
            print("There are no tickets to process. Well done!")
            return

-        if processing_strategy is ProcessingTypes.FIFO:
-            for ticket in self.tickets:
-                ticket.process()
-            return
-
-        if processing_strategy is ProcessingTypes.FILO:
-            for ticket in reversed(self.tickets):
-                ticket.process()
-            return
-
-        if processing_strategy is ProcessingTypes.RANDOM:
-            seed = kwargs.get("seed")
-
-            if seed is None:
-                random.seed(seed)
-
-            random_list = random.sample(self.tickets, len(self.tickets))
-            for ticket in random_list:
-                ticket.process()
-            return
-
-        raise NotImplementedError

+        ticket_list = processing_strategy.create_ordering(self.tickets)

+        for ticket in ticket_list:
+            ticket.process()
```

There are also some minor modifications needed in the `main.py` script.

### `main.py`

```diff
-from .support.app import CustomerSupport, ProcessingTypes
+from .support.app import CustomerSupport, RandomOrderingStrategy
from .support.ticket import SupportTicket


def main() -> None:
    ...

-    app.process_tickets(ProcessingTypes.RANDOM, seed=5)
+    app.process_tickets(RandomOrderingStrategy(seed=5))


if __name__ == "__main__":
    main()
```

## Solution 2: Using Protocol

One minor modification of the GoF solution is to use *static duck typing* this
is similar to what in other languages is known as Interfaces, however it is not
the same. 

In the case of interfaces, the concrete class must explicit *implement* a class
whereas Protocols are only known by the caller, the concrete class does not
need to know it is compliant with a certain protocol.

One example of practical difference, one cannot add Interfaces to third party
code, but it is possible to add Protocols to that code.

This is not a huge change in the code, it basically removes the inheritance
relationship and replace the type of `TicketOrderingStrategy` with `Protocol`
instead of `ABC`.

### `app.py`

```diff
-from abc import ABC, abstractmethod
+from typing import List, Optional, Protocol


+class TicketOrderingStrategy(Protocol):
-class TicketOrderingStrategy(ABC):
-    @abstractmethod
    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        ...


-class FIFOOrderingStrategy(TicketOrderingStrategy):
+class FIFOOrderingStrategy:
    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        return tickets.copy()


-class FILOOrderingStrategy(TicketOrderingStrategy):
+class FILOOrderingStrategy:
    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        return list(reversed(tickets))


@dataclass
-class RandomOrderingStrategy(TicketOrderingStrategy):
+class RandomOrderingStrategy:
    seed: Optional[int] = None

    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        if self.seed is not None:
            random.seed(self.seed)
        return random.sample(tickets, len(tickets))
```

This change is minimal and requires no modification in the `main.py` file.

## Solution 3: Using __call__

When dealing with classes of a single method and little to no state, it is
possible to leverage the `__call__` method in Python. This method is called
when the instance is called with `()`.


That means that the methods should no longer have a particular name:

```diff
class TicketOrderingStrategy(Protocol):
-    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
+    def __call__(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        ...


class FIFOOrderingStrategy:
-    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
+    def __call__(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        return tickets.copy()


class FILOOrderingStrategy:
-    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
+    def __call__(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        return list(reversed(tickets))


@dataclass
class RandomOrderingStrategy:
    seed: Optional[int] = None

-    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
+    def __call__(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        if self.seed is not None:
            random.seed(self.seed)
        return random.sample(tickets, len(tickets))

```

And to execute, one could directly pass the parameters to the instance itself.

```diff
@dataclass
class CustomerSupport:
    ...

    def process_tickets(self, processing_strategy: TicketOrderingStrategy) -> None:
        ...

-       ticket_list = processing_strategy.create_ordering(self.tickets)
+       ticket_list = processing_strategy(self.tickets)
        for ticket in ticket_list:
            ticket.process()
```

This change is minimal and requires no modification in the `main.py` file.


## Solution 4: Using pure functions

The previous solution hints a potential optimization, why having a class with a
single method instead of something simpler like a function? Indeed, there is no
need to have a class if only a single function will do the job.

This leverages one of Python's features: "Functions are first-class citizens",
meaning that they could be passed as parameters.

To keep the typing advantages, the type of the function could be explicitly defined;

```diff
-class TicketOrderingStrategy(Protocol):
-    def __call__(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
-        ...
+TicketOrderingStrategy = Callable[[List[SupportTicket]], List[SupportTicket]]
```

Now, each strategy class could be refactored into a function, since the
`CustomerSupport` class was using the instance as a callable, there is no
changes there.

```diff
-class FIFOOrderingStrategy:
-    def __call__(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
-        return tickets.copy()
+def fifo_strategy(tickets: List[SupportTicket]) -> List[SupportTicket]:
+    return tickets.copy()


-class FILOOrderingStrategy:
-    def __call__(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
-        return list(reversed(tickets))
+def filo_strategy(tickets: List[SupportTicket]) -> List[SupportTicket]:
+    return list(reversed(tickets))

```

In the special case of the `RandomStrategy`, since it uses state, a technique
called "Closure" could be used. This means that the strategy function is
wrapped into another function that takes all the necessary parameters and the
inner function is returned instead.

```diff
-@dataclass
-class RandomOrderingStrategy:
-    seed: Optional[int] = None
-
-    def __call__(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
-        if self.seed is not None:
-            random.seed(self.seed)
-        return random.sample(tickets, len(tickets))
+def random_strategy_generator(seed: Optional[int] = None) -> TicketOrderingStrategy:
+    def random_strategy(tickets: List[SupportTicket]) -> List[SupportTicket]:
+        if seed is not None:
+            random.seed(seed)
+        return random.sample(tickets, len(tickets))
+
+    return random_strategy
```

In the main file, only the class name needs to be updated


```diff
-from .support.app import CustomerSupport, RandomOrderingStrategy
+from .support.app import CustomerSupport, random_strategy_generator
from .support.ticket import SupportTicket

...

-    app.process_tickets(RandomOrderingStrategy(seed=5))
+    app.process_tickets(random_strategy_generator(seed=5))
```

## Solution 5: Using pure functions and Partial Evaluation

Mostly similar to the previous solution but avoid using closures by using
partial evaluation. This removes the nested function and places all parameters
into a single function.

```diff
-def random_strategy_generator(seed: Optional[int] = None) -> TicketOrderingStrategy:
-    def random_strategy(tickets: List[SupportTicket]) -> List[SupportTicket]:
-        if seed is not None:
-            random.seed(seed)
-        return random.sample(tickets, len(tickets))
-
-    return random_strategy

+def random_strategy(tickets: List[SupportTicket], seed: Optional[int] = None) -> List[SupportTicket]:
+    if seed is not None:
+        random.seed(seed)
+    return random.sample(tickets, len(tickets))
```

To evaluate this function, the `partial` function from the `functools` module
from the standard library is used. 

```diff
+from functools import partial

-from .support import CustomerSupport, random_strategy_generator, SupportTicket
+from .support import CustomerSupport, random_strategy, SupportTicket


def main() -> None:
    ...

-    app.process_tickets(random_strategy_generator(seed=5))
+    random_strategy_with_seed = partial(random_strategy, seed=5)
+    app.process_tickets(random_strategy_with_seed)

```


## Solution 6: User input as Strategy

Often enough, the strategy could be determined by some user input. In that
case, it may be useful to re-use the enumerator from earlier and create a
mapping to each of the functions.

```diff
+from enum import Enum, auto

+class ProcessingTypes(Enum):
+    FIFO = auto()
+    FILO = auto()
+    RANDOM = auto()
```

This Enum and the functions can be encapsulated in the `__init__` by using a
dictionary.

```diff
+STRATEGIES = {
+    ProcessingTypes.FIFO: fifo_strategy,
+    ProcessingTypes.FILO: filo_strategy,
+    ProcessingTypes.RANDOM: random_strategy,
+}


__all__ = [
    "CustomerSupport",
    "SupportTicket",
+    "STRATEGIES",
+    "ProcessingTypes"
]
```

This modifies that `main.py` in a way that it does not know exactly which
strategies are available, achieving a fully decouple implementation.

```diff
-from .support import CustomerSupport, random_strategy, SupportTicket
+from typing import Any, Dict
+from .support import CustomerSupport, STRATEGIES, SupportTicket, ProcessingTypes


-def main() -> None:
+def main(strategy: str, strategy_args: Dict[str, Any]) -> None:
    app = CustomerSupport()

    tickets = [
        SupportTicket("John Smith", "My computer makes strange sounds!"),
        SupportTicket("Linus Sebastian", "I can't upload any videos, please help."),
        SupportTicket("Arjan Codes", "VSCode doesn't automatically solve my bugs."),
    ]

    for ticket in tickets:
        app.add_ticket(ticket)

-    random_strategy_with_seed = partial(random_strategy, seed=5)
+    if strategy.upper() not in ProcessingTypes.__members__:
+        raise ValueError(f"Not Valid Strategy: {strategy}")

+    strategy_type = ProcessingTypes[strategy]
+    strategy_function = STRATEGIES[strategy_type]

+    random_strategy_with_seed = partial(strategy_function, **strategy_args)

    app.process_tickets(random_strategy_with_seed)


if __name__ == "__main__":
-    main()
+    main(strategy="random", strategy_args={"seed": 5})
```
