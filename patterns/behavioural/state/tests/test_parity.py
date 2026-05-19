import importlib

import pytest

from patterns.behavioural.state.problem import main as problem_main


@pytest.mark.parametrize(
    "solution",
    [pytest.param(f"solution_{i:02d}", id=f"solution_{i:02d}") for i in range(1, 10)],
)
def test_solution_stdout_matches_problem(
    solution: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    problem_main()
    expected = capsys.readouterr().out

    solution_module = importlib.import_module(
        f"patterns.behavioural.state.{solution}.main"
    )
    solution_module.main()
    actual = capsys.readouterr().out

    assert actual == expected
