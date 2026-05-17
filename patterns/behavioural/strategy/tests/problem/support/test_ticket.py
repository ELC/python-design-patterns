import pytest

from patterns.behavioural.strategy.problem import SupportTicket


def test_process_prints_banner(
    support_ticket: SupportTicket,
    capsys: pytest.CaptureFixture[str],
) -> None:
    support_ticket.process()
    output = capsys.readouterr().out
    assert "Processing ticket id:" in output
    assert support_ticket.customer in output
    assert support_ticket.issue in output
