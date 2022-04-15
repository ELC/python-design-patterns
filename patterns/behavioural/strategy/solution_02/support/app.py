import random
from dataclasses import dataclass, field
from typing import Optional, Protocol, List

from .ticket import SupportTicket


class TicketOrderingStrategy(Protocol):
    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        ...


class FIFOOrderingStrategy:
    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        return tickets.copy()


class FILOOrderingStrategy:
    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        tickets_copy = tickets.copy()
        tickets_copy.reverse()
        return tickets_copy


@dataclass
class RandomOrderingStrategy:
    seed: Optional[int] = None

    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        tickets_copy = tickets.copy()

        if self.seed is not None:
            random.seed(self.seed)

        random.shuffle(tickets_copy)
        return tickets_copy


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
