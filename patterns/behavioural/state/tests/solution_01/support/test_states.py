from datetime import date, datetime
from decimal import Decimal

import pytest

from patterns.behavioural.state.solution_01 import (
    Abandoned,
    Applied,
    CandidateData,
    DirectApplication,
    Hired,
    InterviewRound,
    Interviewed,
    Interviewer,
    OfferExtended,
    Rejected,
    Rejection,
    Screened,
    Sourced,
    SourcedFromRecruiter,
)


def test_applied_renders_application_date(
    applied_candidate_name: str,
    applied_role: str,
    applied_at: datetime,
) -> None:
    state = Applied(
        candidate_name=applied_candidate_name,
        role=applied_role,
        applied_at=applied_at,
    )

    assert str(state) == (
        f"{applied_candidate_name} applied for {applied_role} "
        f"({applied_at.strftime('%Y-%m-%d')})"
    )


def test_sourced_renders_recruiter_and_sourcing_date(
    sourced_candidate_name: str,
    sourced_role: str,
    recruiter: str,
    sourced_at: datetime,
) -> None:
    state = Sourced(
        candidate_name=sourced_candidate_name,
        role=sourced_role,
        recruiter=recruiter,
        sourced_at=sourced_at,
    )

    assert str(state) == (
        f"{sourced_candidate_name} sourced by {recruiter} for {sourced_role} "
        f"({sourced_at.strftime('%Y-%m-%d')})"
    )


def test_screened_direct_renders_screening_date(
    applied_candidate_name: str,
    applied_role: str,
    screening_at: datetime,
    applied_screen_score: float,
) -> None:
    state = Screened(
        data=CandidateData(
            candidate_name=applied_candidate_name,
            role=applied_role,
            source=DirectApplication(),
            screening_score=applied_screen_score,
            screened_at=screening_at,
        )
    )

    assert str(state) == f"screened (direct, {screening_at.strftime('%Y-%m-%d')})"


def test_screened_via_recruiter_renders_recruiter_and_date(
    sourced_candidate_name: str,
    sourced_role: str,
    recruiter: str,
    second_screening_at: datetime,
    sourced_screen_score: float,
) -> None:
    state = Screened(
        data=CandidateData(
            candidate_name=sourced_candidate_name,
            role=sourced_role,
            source=SourcedFromRecruiter(recruiter=recruiter),
            screening_score=sourced_screen_score,
            screened_at=second_screening_at,
        )
    )

    assert str(state) == (
        f"screened (via {recruiter}, {second_screening_at.strftime('%Y-%m-%d')})"
    )


def test_interviewed_with_empty_rounds_raises_value_error(
    second_screening_at: datetime,
) -> None:
    with pytest.raises(ValueError, match="at least one interview round"):
        Interviewed(
            data=CandidateData(
                candidate_name="Pat",
                role="Analyst",
                source=DirectApplication(),
                screening_score=7.0,
                screened_at=second_screening_at,
            ),
            rounds=(),
        )


def test_interviewed_with_rounds_renders_round_dates(
    applied_candidate_name: str,
    applied_role: str,
    screening_at: datetime,
    applied_screen_score: float,
    first_interview_at: datetime,
    alex_second_interview_at: datetime,
) -> None:
    state = Interviewed(
        data=CandidateData(
            candidate_name=applied_candidate_name,
            role=applied_role,
            source=DirectApplication(),
            screening_score=applied_screen_score,
            screened_at=screening_at,
        ),
        rounds=(
            InterviewRound(
                panel=(Interviewer("Taylor Kim", "Engineering Manager"),),
                notes="Strong systems design.",
                at=first_interview_at,
            ),
            InterviewRound(
                panel=(Interviewer("Riley Park", "Tech Lead"),),
                notes="Culture fit confirmed.",
                at=alex_second_interview_at,
            ),
        ),
    )

    assert str(state) == (
        "interviewed -- rounds: "
        f"{first_interview_at.strftime('%Y-%m-%d')}, "
        f"{alex_second_interview_at.strftime('%Y-%m-%d')}"
    )


def test_offer_extended_renders_salary_and_expiry(
    applied_candidate_name: str,
    applied_role: str,
    screening_at: datetime,
    applied_screen_score: float,
    offer_salary: Decimal,
    offer_at: datetime,
    offer_expires_at: datetime,
    first_interview_at: datetime,
) -> None:
    state = OfferExtended(
        data=CandidateData(
            candidate_name=applied_candidate_name,
            role=applied_role,
            source=DirectApplication(),
            screening_score=applied_screen_score,
            screened_at=screening_at,
        ),
        rounds=[
            InterviewRound(
                panel=(Interviewer("Taylor Kim", "Engineering Manager"),),
                notes="Strong systems design.",
                at=first_interview_at,
            )
        ],
        offer_salary=offer_salary,
        offer_at=offer_at,
        offer_expires_at=offer_expires_at,
    )

    assert str(state) == (
        f"offer extended ({offer_salary}, {offer_at.strftime('%Y-%m-%d')}, "
        f"expires {offer_expires_at.strftime('%Y-%m-%d')})"
    )


def test_rejected_renders_latest_reason_and_date(
    sourced_candidate_name: str,
    sourced_role: str,
    screening_at: datetime,
    sourced_screen_score: float,
    role_put_on_hold_reason: str,
    rejection_at: datetime,
) -> None:
    state = Rejected(
        data=CandidateData(
            candidate_name=sourced_candidate_name,
            role=sourced_role,
            source=DirectApplication(),
            screening_score=sourced_screen_score,
            screened_at=screening_at,
            rejections=[Rejection(reason=role_put_on_hold_reason, at=rejection_at)],
        ),
        rounds=[],
    )

    assert str(state) == (
        f"rejected: {role_put_on_hold_reason} ({rejection_at.strftime('%Y-%m-%d')})"
    )


def test_hired_renders_employee_id_hire_date_and_start_date(
    applied_candidate_name: str,
    applied_role: str,
    screening_at: datetime,
    applied_screen_score: float,
    offer_salary: Decimal,
    offer_at: datetime,
    offer_expires_at: datetime,
    alex_hired_employee_id: str,
    start_date: date,
    hire_at: datetime,
    first_interview_at: datetime,
) -> None:
    state = Hired(
        data=CandidateData(
            candidate_name=applied_candidate_name,
            role=applied_role,
            source=DirectApplication(),
            screening_score=applied_screen_score,
            screened_at=screening_at,
        ),
        rounds=[
            InterviewRound(
                panel=(Interviewer("Taylor Kim", "Engineering Manager"),),
                notes="Strong systems design.",
                at=first_interview_at,
            )
        ],
        offer_salary=offer_salary,
        offer_at=offer_at,
        offer_expires_at=offer_expires_at,
        start_date=start_date,
        employee_id=alex_hired_employee_id,
        hire_at=hire_at,
    )

    assert str(state) == (
        f"hired ({alex_hired_employee_id}, {hire_at.strftime('%Y-%m-%d')}, "
        f"starts {start_date.strftime('%Y-%m-%d')})"
    )


def test_abandoned_renders_abandonment_date(
    applied_candidate_name: str,
    applied_role: str,
    abandon_at: datetime,
) -> None:
    state = Abandoned(
        candidate_name=applied_candidate_name,
        role=applied_role,
        abandoned_at=abandon_at,
    )

    assert str(state) == f"abandoned ({abandon_at.strftime('%Y-%m-%d')})"
