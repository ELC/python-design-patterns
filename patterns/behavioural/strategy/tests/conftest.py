import random
from operator import attrgetter

import pytest

from patterns.behavioural.strategy.problem import SupportTicket

_ticket_id = attrgetter("id")


@pytest.fixture
def sample_ticket_data() -> list[tuple[str, str]]:
    return [
        ("John Smith", "My computer makes strange sounds!"),
        ("Linus Sebastian", "I can't upload any videos, please help."),
        ("Arjan Codes", "VSCode doesn't automatically solve my bugs."),
    ]


@pytest.fixture
def expected_random_tickets(
    support_tickets: list[SupportTicket],
) -> list[SupportTicket]:
    random.seed(5)
    return random.sample(support_tickets, len(support_tickets))


@pytest.fixture
def expected_random_order(expected_random_tickets: list[SupportTicket]) -> list[str]:
    return [ticket.customer for ticket in expected_random_tickets]


@pytest.fixture
def empty_queue_message() -> str:
    return "There are no tickets to process. Well done!"


@pytest.fixture
def fifo_ticket_order(support_tickets: list[SupportTicket]) -> list[SupportTicket]:
    return support_tickets


@pytest.fixture
def fifo_customer_order(fifo_ticket_order: list[SupportTicket]) -> list[str]:
    return [ticket.customer for ticket in fifo_ticket_order]


@pytest.fixture
def filo_ticket_order(support_tickets: list[SupportTicket]) -> list[SupportTicket]:
    return list(reversed(support_tickets))


@pytest.fixture
def filo_customer_order(filo_ticket_order: list[SupportTicket]) -> list[str]:
    return [ticket.customer for ticket in filo_ticket_order]


@pytest.fixture
def expected_unseeded_random_tickets(
    support_tickets: list[SupportTicket],
) -> list[SupportTicket]:
    return sorted(support_tickets, key=_ticket_id)
