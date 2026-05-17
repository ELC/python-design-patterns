from typing import Any

import pytest

from patterns.behavioural.strategy.problem import (
    CustomerSupport,
    ProcessingTypes,
    SupportTicket,
)
from patterns.behavioural.strategy.tests.utils import assert_customers_in_order


def test_add_ticket_appends_to_queue(
    customer_support: CustomerSupport,
    support_ticket: SupportTicket,
) -> None:
    customer_support.add_ticket(support_ticket)

    assert customer_support.tickets == [support_ticket]


def test_process_tickets_empty_queue(
    customer_support: CustomerSupport,
    empty_queue_message: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    customer_support.process_tickets()

    output = capsys.readouterr().out

    assert empty_queue_message in output


@pytest.mark.usefixtures("_populate_tickets")
def test_process_tickets_fifo(
    customer_support: CustomerSupport,
    fifo_customer_order: list[str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    customer_support.process_tickets(ProcessingTypes.FIFO)

    output = capsys.readouterr().out

    assert_customers_in_order(output, fifo_customer_order)


@pytest.mark.usefixtures("_populate_tickets")
def test_process_tickets_filo(
    customer_support: CustomerSupport,
    filo_customer_order: list[str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    customer_support.process_tickets(ProcessingTypes.FILO)

    output = capsys.readouterr().out

    assert_customers_in_order(output, filo_customer_order)


@pytest.mark.usefixtures("_populate_tickets")
def test_process_tickets_random_with_seed(
    customer_support: CustomerSupport,
    expected_random_order: list[str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    customer_support.process_tickets(ProcessingTypes.RANDOM, seed=5)

    output = capsys.readouterr().out

    assert_customers_in_order(output, expected_random_order)


@pytest.mark.usefixtures("_populate_tickets")
def test_process_tickets_all_strategies(
    customer_support: CustomerSupport,
    processing_strategy: tuple[ProcessingTypes, dict[str, Any]],
    support_tickets: list[SupportTicket],
    capsys: pytest.CaptureFixture[str],
) -> None:
    strategy, kwargs = processing_strategy
    customer_support.process_tickets(strategy, **kwargs)

    output = capsys.readouterr().out

    for ticket in support_tickets:
        assert ticket.customer in output


@pytest.mark.usefixtures("_populate_ticket")
def test_process_tickets_random_without_seed(
    customer_support: CustomerSupport,
    support_ticket: SupportTicket,
    capsys: pytest.CaptureFixture[str],
) -> None:
    customer_support.process_tickets(ProcessingTypes.RANDOM)

    output = capsys.readouterr().out

    assert support_ticket.customer in output


@pytest.mark.usefixtures("_populate_ticket")
def test_process_tickets_invalid_strategy_raises(
    customer_support: CustomerSupport,
) -> None:
    with pytest.raises(NotImplementedError):
        customer_support.process_tickets("invalid")  # type: ignore[arg-type]
