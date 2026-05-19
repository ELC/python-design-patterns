from collections.abc import Sequence

import pytest

from patterns.behavioural.state.solution_01 import main
from patterns.behavioural.state.tests.utils import assert_journey


def test_main_runs_demo(
    expected_journey: Sequence[str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    main()

    output = capsys.readouterr().out
    assert_journey(output, expected_journey)
