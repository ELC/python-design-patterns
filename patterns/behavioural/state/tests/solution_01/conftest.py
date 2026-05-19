from collections.abc import Sequence
from datetime import date, datetime
from decimal import Decimal

import pytest

from patterns.behavioural.state.solution_01 import (
    Applied,
    HiringProcess,
    Interviewer,
    Sourced,
)


@pytest.fixture
def alex_applied_process(
    applied_candidate_name: str,
    applied_role: str,
    applied_at: datetime,
) -> HiringProcess:
    return HiringProcess(
        Applied(
            candidate_name=applied_candidate_name,
            role=applied_role,
            applied_at=applied_at,
        )
    )


@pytest.fixture
def sam_sourced_process(
    sourced_candidate_name: str,
    sourced_role: str,
    recruiter: str,
    sourced_at: datetime,
) -> HiringProcess:
    return HiringProcess(
        Sourced(
            candidate_name=sourced_candidate_name,
            role=sourced_role,
            recruiter=recruiter,
            sourced_at=sourced_at,
        )
    )


@pytest.fixture
def screened_applied_process(
    alex_applied_process: HiringProcess,
    applied_screen_score: float,
    screening_at: datetime,
) -> HiringProcess:
    alex_applied_process.screen(score=applied_screen_score, at=screening_at)
    return alex_applied_process


@pytest.fixture
def screened_sam_sourced_process(
    sam_sourced_process: HiringProcess,
    sourced_screen_score: float,
    second_screening_at: datetime,
) -> HiringProcess:
    sam_sourced_process.screen(score=sourced_screen_score, at=second_screening_at)
    return sam_sourced_process


@pytest.fixture
def interviewed_applied_process(
    screened_applied_process: HiringProcess,
    interviewers: Sequence[Interviewer],
    first_interview_at: datetime,
) -> HiringProcess:
    screened_applied_process.interview(
        panel=interviewers,
        notes="Strong systems design.",
        at=first_interview_at,
    )
    return screened_applied_process


@pytest.fixture
def offered_applied_process(
    interviewed_applied_process: HiringProcess,
    offer_salary: Decimal,
    offer_expires_at: datetime,
    offer_at: datetime,
) -> HiringProcess:
    interviewed_applied_process.make_offer(
        offer_salary=offer_salary,
        offer_expires_at=offer_expires_at,
        at=offer_at,
    )
    return interviewed_applied_process


@pytest.fixture
def hired_applied_process(
    offered_applied_process: HiringProcess,
    alex_hired_employee_id: str,
    start_date: date,
    hire_at: datetime,
) -> HiringProcess:
    offered_applied_process.hire(
        start_date=start_date,
        employee_id=alex_hired_employee_id,
        at=hire_at,
    )
    return offered_applied_process


@pytest.fixture
def interviewed_sam_sourced_process(
    screened_sam_sourced_process: HiringProcess,
    interviewers: Sequence[Interviewer],
    sam_first_interview_at: datetime,
) -> HiringProcess:
    screened_sam_sourced_process.interview(
        panel=interviewers,
        notes="Deep backend experience.",
        at=sam_first_interview_at,
    )
    return screened_sam_sourced_process


@pytest.fixture
def rejected_sourced_process(
    interviewed_sam_sourced_process: HiringProcess,
    role_put_on_hold_reason: str,
    rejection_at: datetime,
) -> HiringProcess:
    interviewed_sam_sourced_process.reject(
        reason=role_put_on_hold_reason,
        at=rejection_at,
    )
    return interviewed_sam_sourced_process


@pytest.fixture
def re_rejected_sourced_process(
    interviewed_sam_sourced_process: HiringProcess,
    rejection_at: datetime,
) -> HiringProcess:
    interviewed_sam_sourced_process.reject(
        reason="Need another look",
        at=rejection_at,
    )
    return interviewed_sam_sourced_process


@pytest.fixture
def abandoned_screened_process(
    screened_applied_process: HiringProcess,
    abandon_at: datetime,
) -> HiringProcess:
    screened_applied_process.abandon(at=abandon_at)
    return screened_applied_process
