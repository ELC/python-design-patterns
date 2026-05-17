from functools import partial

import pytest

from patterns.behavioural.strategy.solution_06 import (
    CustomerSupport,
    SupportTicket,
    TicketOrderingStrategy,
    fifo_strategy,
    filo_strategy,
    random_strategy,
)


def test_fifo_strategy(
    support_tickets: list[SupportTicket],
    fifo_ticket_order: list[SupportTicket],
) -> None:
    ordered = fifo_strategy(support_tickets)

    assert ordered == fifo_ticket_order


def test_filo_strategy(
    support_tickets: list[SupportTicket],
    filo_ticket_order: list[SupportTicket],
) -> None:
    ordered = filo_strategy(support_tickets)

    assert ordered == filo_ticket_order


def test_random_strategy_with_seed(
    support_tickets: list[SupportTicket],
    expected_random_tickets: list[SupportTicket],
) -> None:
    ordered = partial(random_strategy, seed=5)(support_tickets)

    assert ordered == expected_random_tickets


def test_random_strategy_without_seed(
    support_tickets: list[SupportTicket],
    expected_unseeded_random_tickets: list[SupportTicket],
) -> None:
    ordered = random_strategy(support_tickets)

    assert sorted(ordered, key=lambda t: t.id) == expected_unseeded_random_tickets


def test_process_tickets_empty_queue(
    customer_support: CustomerSupport,
    empty_queue_message: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    customer_support.process_tickets(fifo_strategy)

    output = capsys.readouterr().out

    assert empty_queue_message in output


@pytest.mark.usefixtures("_populate_tickets")
def test_process_tickets_all_strategies(
    customer_support: CustomerSupport,
    processing_strategy: TicketOrderingStrategy,
    support_tickets: list[SupportTicket],
    capsys: pytest.CaptureFixture[str],
) -> None:
    customer_support.process_tickets(processing_strategy)

    output = capsys.readouterr().out

    for ticket in support_tickets:
        assert ticket.customer in output
