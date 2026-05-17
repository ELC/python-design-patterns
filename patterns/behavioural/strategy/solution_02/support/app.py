import random
from collections.abc import MutableSequence, Sequence
from dataclasses import dataclass, field
from typing import Protocol

from .ticket import SupportTicket


class TicketOrderingStrategy(Protocol):
    def create_ordering(
        self, tickets: Sequence[SupportTicket]
    ) -> list[SupportTicket]: ...


class FIFOOrderingStrategy:
    def create_ordering(self, tickets: Sequence[SupportTicket]) -> list[SupportTicket]:
        return list(tickets)


class FILOOrderingStrategy:
    def create_ordering(self, tickets: Sequence[SupportTicket]) -> list[SupportTicket]:
        return list(reversed(tickets))


@dataclass
class RandomOrderingStrategy:
    seed: int | None = None

    def create_ordering(self, tickets: Sequence[SupportTicket]) -> list[SupportTicket]:
        if self.seed is not None:
            random.seed(self.seed)
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

        ticket_list = processing_strategy.create_ordering(self.tickets)
        for ticket in ticket_list:
            ticket.process()
