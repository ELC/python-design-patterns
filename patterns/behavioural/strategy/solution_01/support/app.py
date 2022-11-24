import random
from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass, field

from .ticket import SupportTicket


class TicketOrderingStrategy(ABC):
    @abstractmethod
    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        ...


class FIFOOrderingStrategy(TicketOrderingStrategy):
    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        return tickets.copy()


class FILOOrderingStrategy(TicketOrderingStrategy):
    def create_ordering(self, tickets: List[SupportTicket]) -> List[SupportTicket]:
        return list(reversed(tickets))


@dataclass
class RandomOrderingStrategy(TicketOrderingStrategy):
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
