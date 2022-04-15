# Strategy Pattern

## Problem

A Company's service desk wants to incorporate several approaches to handle
support tickets, each ticket has a name, a description called issue and an
unique id. Moreover, the tickets should have a meaningful console
representation.

At the moment there are only three approaches planned: FIFO, FILO and Random.
However, the system should be able to incorporate more complex approaches in
the feature without changing the code for the existing ones.

**Develop a solution for the stated problem before continue reading**

## Naive Solution

Without knowledge of this pattern, one may develop a solution that looks like
the one in `./problem`. It requires to modify `CustomerSupport` each time there
is a new approach, which is not compliant with the requirements. Moreover, the
complexity of the `process_tickets` will increase as more approaches are
incorporated, which will make the code harder to mantain in the future.

Below are four different solutions to this problem, the first one is the one
proposed in the GoF Book and the following ones are incremental updates to
incorporate Python native Features such as Duck Typing (`Protocols`), Class
callables (`__call__`), and stateful functions (`closures`).

## Solution 1: GoF Approach

### `app.py`

```diff
import random
+from abc import ABC, abstractmethod
from dataclasses import dataclass, field
+from typing import List, Optional
-from typing import List, Literal, Dict, Any
from .ticket import SupportTicket


+class TicketOrderingStrategy(ABC):
+    @abstractmethod
+    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
+        ...
+
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


-class ProcessingTypes(Enum):
-    FIFO = auto()
-    FILO = auto()
-    RANDOM = auto()


@dataclass
class CustomerSupport:
    tickets: List[SupportTicket] = field(default_factory=list)

    def add_ticket(self, ticket: SupportTicket) -> None:
        self.tickets.append(ticket)

-    def process_tickets(
-        self,
-        self, processing_strategy: ProcessingTypes = ProcessingTypes.FIFO, **kwargs: Any
-    ) -> None:
+    def process_tickets(self, processing_strategy: TicketOrderingStrategy) -> None:
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
-        raise NotImplementedError()

+        ticket_list = processing_strategy.create_ordering(self.tickets)

+        for ticket in ticket_list:
+            ticket.process()

```

### `main.py`

```diff
-from .support.app import CustomerSupport, ProcessingTypes
+from .support.app import CustomerSupport, RandomOrderingStrategy
from .support.ticket import SupportTicket


def main():
    app = CustomerSupport()

    tickets = [
        SupportTicket("John Smith", "My computer makes strange sounds!"),
        SupportTicket("Linus Sebastian", "I can't upload any videos, please help."),
        SupportTicket("Arjan Codes", "VSCode doesn't automatically solve my bugs."),
    ]

    for ticket in tickets:
        app.add_ticket(ticket)

-    app.process_tickets(ProcessingTypes.RANDOM, seed=5)
+    app.process_tickets(RandomOrderingStrategy(seed=5))


if __name__ == "__main__":
    main()
```

## Solution 2: Using Protocol

### `app.py`

```diff
import random
from dataclasses import dataclass, field
-from abc import ABC, abstractmethod
-from typing import List, Optional, Protocol
+from typing import List, Optional, Protocol

from .ticket import SupportTicket


+class TicketOrderingStrategy(Protocol):
-class TicketOrderingStrategy(ABC):
-    @abstractmethod
    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        ...


-class FIFOOrderingStrategy:
+class FIFOOrderingStrategy:
    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        return tickets.copy()


-class FILOOrderingStrategy:
+class FILOOrderingStrategy:
    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        return list(reversed(tickets))


@dataclass
-class RandomOrderingStrategy:
+class RandomOrderingStrategy:
    seed: Optional[int] = None

    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        if self.seed is not None:
            random.seed(self.seed)
        return random.sample(tickets, len(tickets))


@dataclass
class CustomerSupport:
    tickets: List[SupportTicket] = field(default_factory=list)

    def add_ticket(self, ticket: SupportTicket) -> None:
        self.tickets.append(ticket)

    def process_tickets(self, processing_strategy: TicketOrderingStrategy) -> None:
        if len(self.tickets) == 0:
            print("There are no tickets to process. Well done!")
            return

        ticket_list = processing_strategy.create_ordering(self.tickets)
        for ticket in ticket_list:
            ticket.process()

```


### `main.py`

No Changes

## Solution 3: Using __call__

### `app.py`

```diff
import random
from dataclasses import dataclass, field
from typing import List, Optional, Protocol

from .ticket import SupportTicket


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


@dataclass
class CustomerSupport:
    tickets: List[SupportTicket] = field(default_factory=list)

    def add_ticket(self, ticket: SupportTicket) -> None:
        self.tickets.append(ticket)

    def process_tickets(self, processing_strategy: TicketOrderingStrategy) -> None:
        if len(self.tickets) == 0:
            print("There are no tickets to process. Well done!")
            return

-        ticket_list = processing_strategy.create_ordering(self.tickets)
+        ticket_list = processing_strategy(self.tickets)
        for ticket in ticket_list:
            ticket.process()
```

### `main.py`

No Changes

## Solution 4: Using pure functions


### `app.py`

```diff
import random
from dataclasses import dataclass, field
from typing import List, Optional, Protocol

from .ticket import SupportTicket


-class TicketOrderingStrategy(Protocol):
-    def __call__(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
-        ...
+TicketOrderingStrategy = Callable[[List[SupportTicket]], List[SupportTicket]]


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


@dataclass
class CustomerSupport:
    tickets: List[SupportTicket] = field(default_factory=list)

    def add_ticket(self, ticket: SupportTicket) -> None:
        self.tickets.append(ticket)

    def process_tickets(self, processing_strategy: TicketOrderingStrategy) -> None:
        if len(self.tickets) == 0:
            print("There are no tickets to process. Well done!")
            return

        ticket_list = processing_strategy(self.tickets)
        for ticket in ticket_list:
            ticket.process()
```

### `main.py`

```diff
-from .support.app import CustomerSupport, RandomOrderingStrategy
+from .support.app import CustomerSupport, random_strategy_generator
from .support.ticket import SupportTicket


def main():
    app = CustomerSupport()

    tickets = [
        SupportTicket("John Smith", "My computer makes strange sounds!"),
        SupportTicket("Linus Sebastian", "I can't upload any videos, please help."),
        SupportTicket("Arjan Codes", "VSCode doesn't automatically solve my bugs."),
    ]

    for ticket in tickets:
        app.add_ticket(ticket)

-    app.process_tickets(RandomOrderingStrategy(seed=5))
+    app.process_tickets(random_strategy_generator(seed=1))


if __name__ == "__main__":
    main()
```
