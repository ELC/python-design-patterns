from collections.abc import Sequence
from datetime import date, datetime
from decimal import Decimal

import pytest

from patterns.behavioural.state.problem import Interviewer, employee_id


@pytest.fixture
def applied_candidate_name() -> str:
    return "Alex Rivera"


@pytest.fixture
def applied_role() -> str:
    return "Software Engineer"


@pytest.fixture
def sourced_candidate_name() -> str:
    return "Sam Chen"


@pytest.fixture
def sourced_role() -> str:
    return "Staff Engineer"


@pytest.fixture
def recruiter() -> str:
    return "Jordan Lee"


@pytest.fixture
def interviewers() -> Sequence[Interviewer]:
    return (
        Interviewer("Taylor Kim", "Engineering Manager"),
        Interviewer("Riley Park", "Tech Lead"),
    )


@pytest.fixture
def applied_at() -> datetime:
    return datetime(2026, 1, 5, 9, 0)


@pytest.fixture
def sourced_at() -> datetime:
    return datetime(2026, 1, 25, 10, 0)


@pytest.fixture
def offer_at() -> datetime:
    return datetime(2026, 2, 21, 10, 0)


@pytest.fixture
def hire_at() -> datetime:
    return datetime(2026, 2, 27, 9, 0)


@pytest.fixture
def screening_at() -> datetime:
    return datetime(2026, 1, 10, 9, 0)


@pytest.fixture
def first_interview_at() -> datetime:
    return datetime(2026, 1, 15, 14, 0)


@pytest.fixture
def alex_second_interview_at() -> datetime:
    return datetime(2026, 1, 22, 14, 0)


@pytest.fixture
def second_screening_at() -> datetime:
    return datetime(2026, 2, 1, 9, 0)


@pytest.fixture
def sam_first_interview_at() -> datetime:
    return datetime(2026, 2, 10, 14, 0)


@pytest.fixture
def rejection_at() -> datetime:
    return datetime(2026, 2, 5, 11, 0)


@pytest.fixture
def reinterview_at() -> datetime:
    return datetime(2026, 2, 18, 14, 0)


@pytest.fixture
def offer_expires_at() -> datetime:
    return datetime(2026, 2, 25, 23, 59)


@pytest.fixture
def start_date() -> date:
    return date(2026, 3, 1)


@pytest.fixture
def abandon_at() -> datetime:
    return datetime(2026, 1, 8, 16, 0)


@pytest.fixture
def expected_journey() -> Sequence[str]:
    return (
        "screened (via Jordan Lee, 2026-02-01)",
        "rejected: Role put on hold (2026-02-05)",
        "screened (via Jordan Lee, 2026-02-08)",
        "interviewed -- rounds: 2026-02-10",
        "rejected: Budget freeze (2026-02-12)",
        "interviewed -- rounds: 2026-02-10, 2026-02-18",
        "interviewed -- rounds: 2026-02-10, 2026-02-18, 2026-02-20",
        "offer extended (165000.00, 2026-02-21, expires 2026-02-25)",
        "hired (EMP-ef6737c2-f000-57fc-80a6-0dac8ab6a56a, 2026-02-27, starts 2026-03-01)",
        "screened (direct, 2026-01-10)",
        "abandoned (2026-01-11)",
    )


@pytest.fixture
def offer_salary() -> Decimal:
    return Decimal("145000.00")


@pytest.fixture
def second_offer_salary() -> Decimal:
    return Decimal("165000.00")


@pytest.fixture
def applied_screen_score() -> float:
    return 8.2


@pytest.fixture
def sourced_screen_score() -> float:
    return 9.0


@pytest.fixture
def role_put_on_hold_reason() -> str:
    return "Role put on hold"


@pytest.fixture
def alex_hired_employee_id(applied_candidate_name: str) -> str:
    return employee_id(applied_candidate_name)
