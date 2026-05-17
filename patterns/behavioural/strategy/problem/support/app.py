import random
from collections.abc import MutableSequence
from dataclasses import dataclass, field
from typing import Any
from enum import Enum, auto

from .ticket import SupportTicket


class ProcessingTypes(Enum):
    FIFO = auto()
    FILO = auto()
    RANDOM = auto()


@dataclass
class CustomerSupport:
    tickets: MutableSequence[SupportTicket] = field(default_factory=list[SupportTicket])

    def add_ticket(self, ticket: SupportTicket) -> None:
        self.tickets.append(ticket)

    def process_tickets(
        self, processing_strategy: ProcessingTypes = ProcessingTypes.FIFO, **kwargs: Any
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

            if seed is not None:
                random.seed(seed)

            random_list = random.sample(self.tickets, len(self.tickets))
            for ticket in random_list:
                ticket.process()

            return

        raise NotImplementedError
