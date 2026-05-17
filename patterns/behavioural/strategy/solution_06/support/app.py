from enum import Enum, auto
import random
from collections.abc import Callable, MutableSequence, Sequence
from dataclasses import dataclass, field

from .ticket import SupportTicket

TicketOrderingStrategy = Callable[[Sequence[SupportTicket]], list[SupportTicket]]


class ProcessingTypes(Enum):
    FIFO = auto()
    FILO = auto()
    RANDOM = auto()


def fifo_strategy(tickets: Sequence[SupportTicket]) -> list[SupportTicket]:
    return list(tickets)


def filo_strategy(tickets: Sequence[SupportTicket]) -> list[SupportTicket]:
    return list(reversed(tickets))


def random_strategy(
    tickets: Sequence[SupportTicket], seed: int | None = None
) -> list[SupportTicket]:
    if seed is not None:
        random.seed(seed)
    return random.sample(tickets, len(tickets))


@dataclass
class CustomerSupport:
    tickets: MutableSequence[SupportTicket] = field(default_factory=list[SupportTicket])

    def add_ticket(self, ticket: SupportTicket) -> None:
        self.tickets.append(ticket)

    def process_tickets(self, processing_strategy: TicketOrderingStrategy) -> None:
        if len(self.tickets) == 0:
            print("There are no tickets to process. Well done!")
            return

        ticket_list = processing_strategy(self.tickets)
        for ticket in ticket_list:
            ticket.process()
