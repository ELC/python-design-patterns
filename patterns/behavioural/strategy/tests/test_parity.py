import importlib
from typing import Any

import pytest

from patterns.behavioural.strategy.problem import main as problem_main


@pytest.mark.parametrize(
    "solution,main_kwargs",
    [
        ("solution_01", {}),
        ("solution_02", {}),
        ("solution_03", {}),
        ("solution_04", {}),
        ("solution_05", {}),
        ("solution_06", {"strategy": "random", "strategy_args": {"seed": 5}}),
    ],
)
def test_solution_stdout_matches_problem(
    solution: str,
    main_kwargs: dict[str, Any],
    capsys: pytest.CaptureFixture[str],
) -> None:
    problem_main()
    problem_out = capsys.readouterr().out

    solution_module = importlib.import_module(
        f"patterns.behavioural.strategy.{solution}.main"
    )
    solution_module.main(**main_kwargs)
    solution_out = capsys.readouterr().out

    assert solution_out == problem_out
