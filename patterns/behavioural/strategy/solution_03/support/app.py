import random
from typing import List, Optional, Protocol
from dataclasses import dataclass, field

from .ticket import SupportTicket


class TicketOrderingStrategy(Protocol):
    def __call__(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        """Returns an ordered list of tickets."""


class FIFOOrderingStrategy:
    def __call__(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        return tickets.copy()


class FILOOrderingStrategy:
    def __call__(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        return list(reversed(tickets))


@dataclass
class RandomOrderingStrategy:
    seed: Optional[int] = None

    def __call__(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
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

        ticket_list = processing_strategy(self.tickets)
        for ticket in ticket_list:
            ticket.process()
