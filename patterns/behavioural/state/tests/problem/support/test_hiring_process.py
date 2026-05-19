from collections.abc import Sequence
from datetime import date, datetime
from decimal import Decimal

import pytest

from patterns.behavioural.state.problem import (
    DirectApplication,
    HiringProcess,
    HiringState,
    Interviewer,
    InvalidTransition,
    Rejection,
    SourcedFromRecruiter,
    employee_id,
)


def test_applied_factory_describes_applicant(
    applied_candidate_name: str,
    applied_role: str,
    applied_at: datetime,
) -> None:
    process = HiringProcess.applied(
        candidate_name=applied_candidate_name,
        role=applied_role,
        at=applied_at,
    )

    assert str(process) == (
        f"{applied_candidate_name} applied for {applied_role} "
        f"({applied_at.strftime('%Y-%m-%d')})"
    )


def test_sourced_factory_describes_recruiter_sourced_applicant(
    sourced_candidate_name: str,
    sourced_role: str,
    recruiter: str,
    sourced_at: datetime,
) -> None:
    process = HiringProcess.sourced(
        candidate_name=sourced_candidate_name,
        role=sourced_role,
        recruiter=recruiter,
        at=sourced_at,
    )

    assert str(process) == (
        f"{sourced_candidate_name} sourced by {recruiter} for {sourced_role} "
        f"({sourced_at.strftime('%Y-%m-%d')})"
    )


def test_direct_applicant_moves_to_screened(
    applied_process: HiringProcess,
    screening_at: datetime,
    applied_screen_score: float,
) -> None:
    applied_process.screen(score=applied_screen_score, at=screening_at)

    assert applied_process.state is HiringState.SCREENED
    assert applied_process.source == DirectApplication()
    assert str(applied_process) == (
        f"screened (direct, {screening_at.strftime('%Y-%m-%d')})"
    )


def test_recruiter_sourced_applicant_moves_to_screened(
    sourced_process: HiringProcess,
    second_screening_at: datetime,
    sourced_screen_score: float,
    recruiter: str,
) -> None:
    sourced_process.screen(score=sourced_screen_score, at=second_screening_at)

    assert sourced_process.state is HiringState.SCREENED
    assert sourced_process.source == SourcedFromRecruiter(recruiter=recruiter)
    assert str(sourced_process) == (
        f"screened (via {recruiter}, {second_screening_at.strftime('%Y-%m-%d')})"
    )


@pytest.mark.usefixtures("_sourced_screened_and_rejected")
def test_rejected_applicant_can_be_rescreened_after_role_on_hold(
    sourced_process: HiringProcess,
    screening_at: datetime,
    rejection_at: datetime,
    recovery_screen_score: float,
    role_put_on_hold_reason: str,
    recruiter: str,
) -> None:
    sourced_process.screen(score=recovery_screen_score, at=screening_at)

    assert sourced_process.state is HiringState.SCREENED
    assert sourced_process.source == SourcedFromRecruiter(recruiter=recruiter)
    assert sourced_process.screening_score == recovery_screen_score
    assert sourced_process.screened_at == screening_at
    assert str(sourced_process) == (
        f"screened (via {recruiter}, {screening_at.strftime('%Y-%m-%d')})"
    )
    assert sourced_process.rejections == [
        Rejection(reason=role_put_on_hold_reason, at=rejection_at),
    ]


@pytest.mark.usefixtures("_sourced_screened_and_rejected")
def test_rescreened_applicant_can_schedule_first_interview_round(
    sourced_process: HiringProcess,
    screening_at: datetime,
    recovery_screen_score: float,
    interviewers: Sequence[Interviewer],
    second_screening_at: datetime,
) -> None:
    sourced_process.screen(score=recovery_screen_score, at=screening_at)
    sourced_process.interview(
        panel=interviewers,
        notes="Back after recovery screen.",
        at=second_screening_at,
    )

    assert sourced_process.state is HiringState.INTERVIEWED
    assert len(sourced_process.rounds) == 1
    assert sourced_process.rounds[0].at == second_screening_at
    assert str(sourced_process) == (
        f"interviewed -- rounds: {second_screening_at.strftime('%Y-%m-%d')}"
    )


@pytest.mark.usefixtures("_sourced_reopened_after_rejection_for_offer")
def test_reopened_applicant_can_be_offered_and_hired(
    sourced_process: HiringProcess,
    sourced_candidate_name: str,
    reinterview_at: datetime,
    offer_at: datetime,
    offer_expires_at: datetime,
    hire_at: datetime,
    second_offer_salary: Decimal,
    start_date: date,
    rejection_at: datetime,
    role_put_on_hold_reason: str,
) -> None:
    assert sourced_process.rejections == [
        Rejection(reason=role_put_on_hold_reason, at=rejection_at),
    ]

    sourced_process.make_offer(
        offer_salary=second_offer_salary,
        offer_expires_at=offer_expires_at,
        at=offer_at,
    )
    sourced_process.hire(
        start_date=start_date,
        employee_id=employee_id(sourced_candidate_name),
        at=hire_at,
    )

    assert sourced_process.state is HiringState.HIRED
    assert len(sourced_process.rounds) == 2
    assert sourced_process.rounds[1].at == reinterview_at


@pytest.mark.usefixtures("_applied_screened")
def test_screened_applicant_can_abandon_pipeline(
    applied_process: HiringProcess,
    screening_at: datetime,
    abandon_at: datetime,
) -> None:
    applied_process.abandon(at=abandon_at)

    assert applied_process.state is HiringState.ABANDONED

    with pytest.raises(
        InvalidTransition,
        match=(
            r"abandon is not allowed from ABANDONED; allowed states: "
            r"APPLIED, SOURCED, SCREENED, INTERVIEWED, OFFER_EXTENDED, REJECTED"
        ),
    ):
        applied_process.abandon(at=screening_at)


@pytest.mark.usefixtures("_applied_screened")
def test_screened_applicant_cannot_receive_offer_without_interview(
    applied_process: HiringProcess,
    offer_at: datetime,
    offer_expires_at: datetime,
    offer_salary: Decimal,
) -> None:
    with pytest.raises(
        InvalidTransition,
        match=r"make_offer is not allowed from SCREENED; allowed states: INTERVIEWED",
    ):
        applied_process.make_offer(
            offer_salary=offer_salary,
            offer_expires_at=offer_expires_at,
            at=offer_at,
        )


@pytest.mark.usefixtures("_applied_screened_and_interviewed")
def test_interviewed_applicant_cannot_be_hired_without_offer(
    applied_process: HiringProcess,
    start_date: date,
    hire_at: datetime,
) -> None:
    with pytest.raises(
        InvalidTransition,
        match=r"hire is not allowed from INTERVIEWED; allowed states: OFFER_EXTENDED",
    ):
        applied_process.hire(
            start_date=start_date,
            employee_id="missing-offer",
            at=hire_at,
        )


@pytest.mark.usefixtures("_sourced_screened_once")
def test_already_screened_applicant_cannot_be_screened_again(
    sourced_process: HiringProcess,
    screening_at: datetime,
) -> None:
    with pytest.raises(
        InvalidTransition,
        match=(
            r"screen is not allowed from SCREENED; "
            r"allowed states: APPLIED, SOURCED, REJECTED"
        ),
    ):
        sourced_process.screen(score=9.0, at=screening_at)


def test_applied_applicant_cannot_be_rejected_before_screening(
    applied_process: HiringProcess,
    screening_at: datetime,
) -> None:
    with pytest.raises(
        InvalidTransition,
        match=(
            r"reject is not allowed from APPLIED; "
            r"allowed states: SCREENED, INTERVIEWED, OFFER_EXTENDED"
        ),
    ):
        applied_process.reject(reason="Early pass", at=screening_at)


def test_applied_applicant_cannot_be_interviewed_before_screening(
    applied_process: HiringProcess,
    screening_at: datetime,
    interviewers: Sequence[Interviewer],
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
            notes="too soon",
            at=screening_at,
        )


@pytest.mark.usefixtures("_applied_screened_and_interviewed_for_reject")
def test_rejection_after_interview_keeps_completed_rounds(
    applied_process: HiringProcess,
    screening_at: datetime,
) -> None:
    applied_process.reject(reason="no time", at=screening_at)

    assert applied_process.state is HiringState.REJECTED
    assert len(applied_process.rounds) == 1
    assert applied_process.rounds[0].notes == "Initial conversation."


@pytest.mark.usefixtures("_sourced_screened_interviewed_and_rejected")
def test_interview_after_rejection_preserves_prior_rejection(
    sourced_process: HiringProcess,
    interviewers: Sequence[Interviewer],
    sam_first_interview_at: datetime,
    rejection_at: datetime,
    role_put_on_hold_reason: str,
) -> None:
    sourced_process.interview(
        panel=interviewers,
        notes="Re-opened after reorg.",
        at=sam_first_interview_at,
    )

    assert sourced_process.state is HiringState.INTERVIEWED
    assert sourced_process.rejections == [
        Rejection(reason=role_put_on_hold_reason, at=rejection_at),
    ]


@pytest.mark.usefixtures("_sourced_before_second_rejection")
def test_second_rejection_appends_to_rejection_history(
    sourced_process: HiringProcess,
    reinterview_at: datetime,
    rejection_at: datetime,
    role_put_on_hold_reason: str,
    budget_freeze_reason: str,
) -> None:
    sourced_process.reject(reason=budget_freeze_reason, at=reinterview_at)

    assert sourced_process.rejections == [
        Rejection(reason=role_put_on_hold_reason, at=rejection_at),
        Rejection(reason=budget_freeze_reason, at=reinterview_at),
    ]
    assert str(sourced_process) == (
        f"rejected: {budget_freeze_reason} ({reinterview_at.strftime('%Y-%m-%d')})"
    )


def test_screen_mutates_process_with_screened_description(
    sam_sourced_process: HiringProcess,
    recruiter: str,
    second_screening_at: datetime,
    sourced_screen_score: float,
) -> None:
    after = sam_sourced_process.screen(
        score=sourced_screen_score,
        at=second_screening_at,
    )

    assert sam_sourced_process is after
    assert str(after) == (
        f"screened (via {recruiter}, {second_screening_at.strftime('%Y-%m-%d')})"
    )


def test_interview_mutates_process_with_round_dates(
    screened_applied_process: HiringProcess,
    interviewers: Sequence[Interviewer],
    first_interview_at: datetime,
) -> None:
    after = screened_applied_process.interview(
        panel=interviewers,
        notes="Strong systems design.",
        at=first_interview_at,
    )

    assert screened_applied_process is after
    assert str(after) == (
        f"interviewed -- rounds: {first_interview_at.strftime('%Y-%m-%d')}"
    )


def test_make_offer_mutates_process_with_expiry(
    interviewed_applied_process: HiringProcess,
    offer_salary: Decimal,
    offer_expires_at: datetime,
    offer_at: datetime,
) -> None:
    after = interviewed_applied_process.make_offer(
        offer_salary=offer_salary,
        offer_expires_at=offer_expires_at,
        at=offer_at,
    )

    assert interviewed_applied_process is after
    assert str(after) == (
        f"offer extended ({offer_salary}, {offer_at.strftime('%Y-%m-%d')}, "
        f"expires {offer_expires_at.strftime('%Y-%m-%d')})"
    )


def test_hire_mutates_process_with_start_date(
    offered_applied_process: HiringProcess,
    alex_hired_employee_id: str,
    start_date: date,
    hire_at: datetime,
) -> None:
    after = offered_applied_process.hire(
        start_date=start_date,
        employee_id=alex_hired_employee_id,
        at=hire_at,
    )

    assert offered_applied_process is after
    assert str(after) == (
        f"hired ({alex_hired_employee_id}, {hire_at.strftime('%Y-%m-%d')}, "
        f"starts {start_date.strftime('%Y-%m-%d')})"
    )


def test_reject_mutates_process_with_rejection_timestamp(
    screened_sam_sourced_process: HiringProcess,
    role_put_on_hold_reason: str,
    rejection_at: datetime,
) -> None:
    after = screened_sam_sourced_process.reject(
        reason=role_put_on_hold_reason,
        at=rejection_at,
    )

    assert screened_sam_sourced_process is after
    assert str(after) == (
        f"rejected: {role_put_on_hold_reason} ({rejection_at.strftime('%Y-%m-%d')})"
    )


def test_abandon_mutates_process_with_abandonment_timestamp(
    screened_applied_process: HiringProcess,
    abandon_at: datetime,
) -> None:
    after = screened_applied_process.abandon(at=abandon_at)

    assert screened_applied_process is after
    assert str(after) == f"abandoned ({abandon_at.strftime('%Y-%m-%d')})"
