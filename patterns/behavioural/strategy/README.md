# Strategy Pattern

## Problem

## Solution 1: GoF Approach

### `app.py`

```diff
import random
+from abc import ABC, abstractmethod
+from typing import List, Optional
from dataclasses import dataclass, field
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
+        if self.seed is None:
+            random.seed(self.seed)
+        return random.sample(tickets, len(tickets))


@dataclass
class CustomerSupport:
    tickets: List[SupportTicket] = field(default_factory=list)

    def add_ticket(self, ticket: SupportTicket) -> None:
        self.tickets.append(ticket)

-    def process_tickets(
-        self,
-        processing_strategy: Literal["fifo", "filo", "random"] = "fifo",
-        **kwargs: Dict[str, Any]
-    ) -> None:
+    def process_tickets(self, processing_strategy: TicketOrderingStrategy) -> None:
        if len(self.tickets) == 0:
            print("There are no tickets to process. Well done!")
            return

-        if processing_strategy == "fifo":
-            for ticket in self.tickets:
-                ticket.process()
-            return
-
-        if processing_strategy == "filo":
-            for ticket in reversed(self.tickets):
-                ticket.process()
-            return
-
-        if processing_strategy == "random":
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
-from .support.app import CustomerSupport
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

-    app.process_tickets("random", seed=5)
+    app.process_tickets(RandomOrderingStrategy(seed=5))


if __name__ == "__main__":
    main()

```

## Solution 2: Using Protocol


## Solution 3: Using __call__

## Solution 4: Using pure functions


    if len(self.tickets) == 0:
        print("There are no tickets to process. Well done!")
        return

    if processing_strategy == "fifo":
        for ticket in self.tickets:
            ticket.process()
        return

    if processing_strategy == "filo":
        for ticket in reversed(self.tickets):
            ticket.process()
        return

    if processing_strategy == "random":
        seed = kwargs.get("seed")

        if seed is None:
            random.seed(seed)

        random_list = random.sample(self.tickets, len(self.tickets))
        for ticket in random_list:
            ticket.process()

        return

    raise NotImplementedError()