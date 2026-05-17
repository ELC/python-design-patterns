import pytest

from patterns.behavioural.strategy.solution_03 import (
    CustomerSupport,
    FIFOOrderingStrategy,
    FILOOrderingStrategy,
    RandomOrderingStrategy,
    SupportTicket,
    TicketOrderingStrategy,
)


def test_fifo_ordering_strategy(
    fifo_ordering_strategy: FIFOOrderingStrategy,
    support_tickets: list[SupportTicket],
    fifo_ticket_order: list[SupportTicket],
) -> None:
    ordered = fifo_ordering_strategy(support_tickets)

    assert ordered == fifo_ticket_order


def test_filo_ordering_strategy(
    filo_ordering_strategy: FILOOrderingStrategy,
    support_tickets: list[SupportTicket],
    filo_ticket_order: list[SupportTicket],
) -> None:
    ordered = filo_ordering_strategy(support_tickets)

    assert ordered == filo_ticket_order


def test_random_ordering_strategy_with_seed(
    random_ordering_strategy: RandomOrderingStrategy,
    support_tickets: list[SupportTicket],
    expected_random_tickets: list[SupportTicket],
) -> None:
    ordered = random_ordering_strategy(support_tickets)

    assert ordered == expected_random_tickets


def test_random_ordering_strategy_without_seed(
    random_ordering_strategy_no_seed: RandomOrderingStrategy,
    support_tickets: list[SupportTicket],
    expected_unseeded_random_tickets: list[SupportTicket],
) -> None:
    ordered = random_ordering_strategy_no_seed(support_tickets)

    assert sorted(ordered, key=lambda t: t.id) == expected_unseeded_random_tickets


def test_process_tickets_empty_queue(
    customer_support: CustomerSupport,
    fifo_ordering_strategy: FIFOOrderingStrategy,
    empty_queue_message: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    customer_support.process_tickets(fifo_ordering_strategy)

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
