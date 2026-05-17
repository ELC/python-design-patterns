import pytest

from patterns.behavioural.strategy.solution_06 import main
from patterns.behavioural.strategy.tests.utils import assert_customers_in_order


def test_main_runs_demo(
    capsys: pytest.CaptureFixture[str],
    sample_ticket_data: list[tuple[str, str]],
    expected_random_order: list[str],
) -> None:
    main(strategy="random", strategy_args={"seed": 5})

    output = capsys.readouterr().out

    for customer, _ in sample_ticket_data:
        assert customer in output

    assert_customers_in_order(output, expected_random_order)


def test_main_invalid_strategy_raises() -> None:
    with pytest.raises(ValueError, match="Not Valid Strategy"):
        main(strategy="invalid", strategy_args={})
