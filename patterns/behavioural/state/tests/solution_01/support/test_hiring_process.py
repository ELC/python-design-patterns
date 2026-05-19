from collections.abc import Sequence
from datetime import date, datetime
from decimal import Decimal

import pytest

from patterns.behavioural.state.solution_01 import (
    Applied,
    Hired,
    HiringProcess,
    Interviewed,
    Interviewer,
    InvalidTransition,
    OfferExtended,
    Screened,
)


def test_screen_from_applied_transition(
    alex_applied_process: HiringProcess,
    applied_screen_score: float,
    screening_at: datetime,
) -> None:
    alex_applied_process.screen(score=applied_screen_score, at=screening_at)

    assert isinstance(alex_applied_process.state, Screened)
    assert "direct" in str(alex_applied_process)


def test_screen_from_sourced_transition(
    sam_sourced_process: HiringProcess,
    sourced_screen_score: float,
    second_screening_at: datetime,
    recruiter: str,
) -> None:
    sam_sourced_process.screen(score=sourced_screen_score, at=second_screening_at)

    assert isinstance(sam_sourced_process.state, Screened)
    assert recruiter in str(sam_sourced_process)


def test_interview_transition(
    screened_applied_process: HiringProcess,
    interviewers: Sequence[Interviewer],
    first_interview_at: datetime,
    alex_second_interview_at: datetime,
) -> None:
    screened_applied_process.interview(
        panel=interviewers,
        notes="Strong systems design.",
        at=first_interview_at,
    )
    screened_applied_process.interview(
        panel=interviewers,
        notes="Culture fit confirmed.",
        at=alex_second_interview_at,
    )

    assert isinstance(screened_applied_process.state, Interviewed)
    assert len(screened_applied_process.state.rounds) == 2


def test_make_offer_transition(
    interviewed_applied_process: HiringProcess,
    offer_salary: Decimal,
    offer_expires_at: datetime,
    offer_at: datetime,
) -> None:
    interviewed_applied_process.make_offer(
        offer_salary=offer_salary,
        offer_expires_at=offer_expires_at,
        at=offer_at,
    )

    assert isinstance(interviewed_applied_process.state, OfferExtended)


def test_hire_transition(
    offered_applied_process: HiringProcess,
    alex_hired_employee_id: str,
    start_date: date,
    hire_at: datetime,
) -> None:
    offered_applied_process.hire(
        start_date=start_date,
        employee_id=alex_hired_employee_id,
        at=hire_at,
    )

    assert isinstance(offered_applied_process.state, Hired)


def test_reject_transition(
    interviewed_sam_sourced_process: HiringProcess,
    role_put_on_hold_reason: str,
    rejection_at: datetime,
) -> None:
    interviewed_sam_sourced_process.reject(
        reason=role_put_on_hold_reason,
        at=rejection_at,
    )

    assert "rejected" in str(interviewed_sam_sourced_process)


def test_screen_from_rejected_transition(
    re_rejected_sourced_process: HiringProcess,
    screening_at: datetime,
) -> None:
    re_rejected_sourced_process.screen(score=8.9, at=screening_at)

    assert isinstance(re_rejected_sourced_process.state, Screened)


def test_interview_from_rejected_transition(
    rejected_sourced_process: HiringProcess,
    interviewers: Sequence[Interviewer],
    reinterview_at: datetime,
) -> None:
    rejected_sourced_process.interview(
        panel=interviewers,
        notes="Re-opened after reorg.",
        at=reinterview_at,
    )

    assert isinstance(rejected_sourced_process.state, Interviewed)


def test_abandon_transition(
    screened_applied_process: HiringProcess,
    abandon_at: datetime,
) -> None:
    screened_applied_process.abandon(at=abandon_at)

    assert (
        str(screened_applied_process)
        == f"abandoned ({abandon_at.strftime('%Y-%m-%d')})"
    )


def test_abandon_rejects_terminal_hired(
    hired_applied_process: HiringProcess,
    rejection_at: datetime,
) -> None:
    with pytest.raises(InvalidTransition, match="abandon is not allowed"):
        hired_applied_process.abandon(at=rejection_at)


def test_str_interviewed_with_empty_rounds_raises_value_error(
    interviewed_applied_process: HiringProcess,
) -> None:
    state = interviewed_applied_process.state
    assert isinstance(state, Interviewed)
    state.rounds.clear()

    with pytest.raises(ValueError, match="at least one interview round"):
        str(interviewed_applied_process)


def test_second_abandon_is_invalid(
    abandoned_screened_process: HiringProcess,
    abandon_at: datetime,
) -> None:
    with pytest.raises(InvalidTransition, match="abandon is not allowed"):
        abandoned_screened_process.abandon(at=abandon_at)


@pytest.mark.parametrize(
    "violator_fn",
    (
        pytest.param(
            lambda panel, fst, applied_at: Applied(
                candidate_name="ghost",
                role="eng",
                applied_at=applied_at,
            ).interview(panel=panel, notes="no", at=fst),
            id="bad-interview",
        ),
        pytest.param(
            lambda panel, fst, applied_at: Applied(
                candidate_name="wrong",
                role="role",
                applied_at=applied_at,
            ).reject(reason="no", at=fst),
            id="bad-reject",
        ),
    ),
)
def test_invalid_transition(
    violator_fn,
    interviewers: Sequence[Interviewer],
    first_interview_at: datetime,
    applied_at: datetime,
) -> None:
    with pytest.raises(InvalidTransition):
        violator_fn(tuple(interviewers), first_interview_at, applied_at)
