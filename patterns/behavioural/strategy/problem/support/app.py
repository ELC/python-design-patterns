import random
from dataclasses import dataclass, field
from typing import List, Literal, Dict, Any

from .ticket import SupportTicket


@dataclass
class CustomerSupport:
    tickets: List[SupportTicket] = field(default_factory=list)

    def add_ticket(self, ticket: SupportTicket) -> None:
        self.tickets.append(ticket)

    def process_tickets(
        self,
        processing_strategy: Literal["fifo", "filo", "random"] = "fifo",
        **kwargs: Dict[str, Any]
    ) -> None:
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
