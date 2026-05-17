from typing import Any

import pytest

from patterns.behavioural.strategy.problem import (
    CustomerSupport,
    ProcessingTypes,
    SupportTicket,
)


@pytest.fixture(
    params=[
        pytest.param((ProcessingTypes.FIFO, {}), id="fifo"),
        pytest.param((ProcessingTypes.FILO, {}), id="filo"),
        pytest.param((ProcessingTypes.RANDOM, {"seed": 5}), id="random-seed-5"),
    ],
)
def processing_strategy(
    request: pytest.FixtureRequest,
) -> tuple[ProcessingTypes, dict[str, Any]]:
    return request.param


@pytest.fixture
def customer_support() -> CustomerSupport:
    return CustomerSupport()


@pytest.fixture
def support_ticket(sample_ticket_data: list[tuple[str, str]]) -> SupportTicket:
    customer, issue = sample_ticket_data[0]
    return SupportTicket(customer, issue)


@pytest.fixture
def support_tickets(sample_ticket_data: list[tuple[str, str]]) -> list[SupportTicket]:
    return [SupportTicket(customer, issue) for customer, issue in sample_ticket_data]


@pytest.fixture
def _populate_ticket(
    customer_support: CustomerSupport,
    support_ticket: SupportTicket,
) -> None:
    customer_support.add_ticket(support_ticket)


@pytest.fixture
def _populate_tickets(
    _populate_ticket: None,
    customer_support: CustomerSupport,
    support_tickets: list[SupportTicket],
) -> None:
    for ticket in support_tickets[1:]:
        customer_support.add_ticket(ticket)
