from collections.abc import Sequence
from datetime import datetime

import pytest

from patterns.behavioural.state.problem import (
    HiringProcess,
    Interviewer,
    InvalidTransition,
)
from patterns.behavioural.state.problem import main as problem_main
from patterns.behavioural.state.tests.utils import assert_journey


def test_main_runs_demo(
    expected_journey: Sequence[str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    problem_main()
    output = capsys.readouterr().out
    assert_journey(output, expected_journey)


def test_main_invalid_transition_raises_value_error(
    applied_process: HiringProcess,
    interviewers: Sequence[Interviewer],
    screening_at: datetime,
) -> None:
    with pytest.raises(
        InvalidTransition,
        match=(
            r"interview is not allowed from APPLIED; "
            r"allowed states: SCREENED, INTERVIEWED, REJECTED"
        ),
    ):
        applied_process.interview(
            panel=interviewers,
            notes="n",
            at=screening_at,
        )
