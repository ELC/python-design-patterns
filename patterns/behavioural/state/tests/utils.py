from collections.abc import Sequence


def assert_journey(output: str, expected: Sequence[str]) -> None:
    lines = [line.strip() for line in output.strip().splitlines()]
    assert lines == list(expected)
