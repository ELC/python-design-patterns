import random
from typing import List, Optional, Callable
from dataclasses import dataclass, field

from .ticket import SupportTicket

TicketOrderingStrategy = Callable[[List[SupportTicket]], List[SupportTicket]]


def fifo_strategy(tickets: List[SupportTicket]) -> List[SupportTicket]:
    return tickets.copy()


def filo_strategy(tickets: List[SupportTicket]) -> List[SupportTicket]:
    return list(reversed(tickets))


def random_strategy(tickets: List[SupportTicket], seed: Optional[int] = None) -> List[SupportTicket]:
    if seed is not None:
        random.seed(seed)
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
