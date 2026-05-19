from collections.abc import Sequence
from datetime import datetime
from decimal import Decimal

import pytest

from patterns.behavioural.state.problem import (
    DirectApplication,
    HiringProcess,
    HiringState,
    Interviewer,
    employee_id,
)


@pytest.fixture
def applied_process(
    applied_candidate_name: str,
    applied_role: str,
    applied_at: datetime,
) -> HiringProcess:
    return HiringProcess.applied(
        candidate_name=applied_candidate_name,
        role=applied_role,
        at=applied_at,
    )


@pytest.fixture
def sourced_process(
    sourced_candidate_name: str,
    sourced_role: str,
    recruiter: str,
    sourced_at: datetime,
) -> HiringProcess:
    return HiringProcess.sourced(
        candidate_name=sourced_candidate_name,
        role=sourced_role,
        recruiter=recruiter,
        at=sourced_at,
    )


@pytest.fixture
def screened_without_source_process(
    applied_candidate_name: str,
    applied_role: str,
    screening_at: datetime,
) -> HiringProcess:
    return HiringProcess(
        state=HiringState.SCREENED,
        candidate_name=applied_candidate_name,
        role=applied_role,
        screened_at=screening_at,
    )


@pytest.fixture
def screened_without_timestamp_process(
    applied_candidate_name: str,
    applied_role: str,
) -> HiringProcess:
    return HiringProcess(
        state=HiringState.SCREENED,
        candidate_name=applied_candidate_name,
        role=applied_role,
        source=DirectApplication(),
    )


@pytest.fixture
def offered_without_offer_details_process(
    applied_candidate_name: str,
    applied_role: str,
) -> HiringProcess:
    return HiringProcess(
        state=HiringState.OFFER_EXTENDED,
        candidate_name=applied_candidate_name,
        role=applied_role,
    )


@pytest.fixture
def hired_without_hire_details_process(
    applied_candidate_name: str,
    applied_role: str,
) -> HiringProcess:
    return HiringProcess(
        state=HiringState.HIRED,
        candidate_name=applied_candidate_name,
        role=applied_role,
    )


@pytest.fixture
def abandoned_without_timestamp_process(
    applied_candidate_name: str,
    applied_role: str,
) -> HiringProcess:
    return HiringProcess(
        state=HiringState.ABANDONED,
        candidate_name=applied_candidate_name,
        role=applied_role,
    )


@pytest.fixture
def applied_without_timestamp_process(
    applied_candidate_name: str,
    applied_role: str,
) -> HiringProcess:
    return HiringProcess(
        state=HiringState.APPLIED,
        candidate_name=applied_candidate_name,
        role=applied_role,
    )


@pytest.fixture
def sourced_without_timestamp_process(
    sourced_candidate_name: str,
    sourced_role: str,
    recruiter: str,
) -> HiringProcess:
    return HiringProcess(
        state=HiringState.SOURCED,
        candidate_name=sourced_candidate_name,
        role=sourced_role,
        recruiter=recruiter,
    )


@pytest.fixture
def rejected_without_rejections_process(
    applied_candidate_name: str,
    applied_role: str,
) -> HiringProcess:
    return HiringProcess(
        state=HiringState.REJECTED,
        candidate_name=applied_candidate_name,
        role=applied_role,
    )


@pytest.fixture
def interviewed_without_rounds_process(
    applied_candidate_name: str,
    applied_role: str,
) -> HiringProcess:
    return HiringProcess(
        state=HiringState.INTERVIEWED,
        candidate_name=applied_candidate_name,
        role=applied_role,
    )


@pytest.fixture
def alex_applied_process(
    applied_candidate_name: str,
    applied_role: str,
    applied_at: datetime,
) -> HiringProcess:
    return HiringProcess.applied(
        candidate_name=applied_candidate_name,
        role=applied_role,
        at=applied_at,
    )


@pytest.fixture
def sam_sourced_process(
    sourced_candidate_name: str,
    sourced_role: str,
    recruiter: str,
    sourced_at: datetime,
) -> HiringProcess:
    return HiringProcess.sourced(
        candidate_name=sourced_candidate_name,
        role=sourced_role,
        recruiter=recruiter,
        at=sourced_at,
    )


@pytest.fixture
def screened_applied_process(
    alex_applied_process: HiringProcess,
    screening_at: datetime,
    applied_screen_score: float,
) -> HiringProcess:
    return alex_applied_process.screen(
        score=applied_screen_score,
        at=screening_at,
    )


@pytest.fixture
def interviewed_applied_process(
    screened_applied_process: HiringProcess,
    interviewers: Sequence[Interviewer],
    first_interview_at: datetime,
) -> HiringProcess:
    return screened_applied_process.interview(
        panel=interviewers,
        notes="Strong systems design.",
        at=first_interview_at,
    )


@pytest.fixture
def offered_applied_process(
    interviewed_applied_process: HiringProcess,
    offer_salary: Decimal,
    offer_expires_at: datetime,
    offer_at: datetime,
) -> HiringProcess:
    return interviewed_applied_process.make_offer(
        offer_salary=offer_salary,
        offer_expires_at=offer_expires_at,
        at=offer_at,
    )


@pytest.fixture
def screened_sam_sourced_process(
    sam_sourced_process: HiringProcess,
    second_screening_at: datetime,
    sourced_screen_score: float,
) -> HiringProcess:
    return sam_sourced_process.screen(
        score=sourced_screen_score,
        at=second_screening_at,
    )


@pytest.fixture
def alex_hired_employee_id(applied_candidate_name: str) -> str:
    return employee_id(applied_candidate_name)


@pytest.fixture
def role_put_on_hold_reason() -> str:
    return "Role put on hold"


@pytest.fixture
def budget_freeze_reason() -> str:
    return "Budget freeze"


@pytest.fixture
def applied_screen_score() -> float:
    return 8.2


@pytest.fixture
def sourced_screen_score() -> float:
    return 9.0


@pytest.fixture
def recovery_screen_score() -> float:
    return 8.8


@pytest.fixture
def _sourced_screened(
    sourced_process: HiringProcess,
    second_screening_at: datetime,
    sourced_screen_score: float,
) -> None:
    sourced_process.screen(score=sourced_screen_score, at=second_screening_at)


@pytest.fixture
def _sourced_screened_and_rejected(
    _sourced_screened: None,
    sourced_process: HiringProcess,
    rejection_at: datetime,
    role_put_on_hold_reason: str,
) -> None:
    sourced_process.reject(reason=role_put_on_hold_reason, at=rejection_at)


@pytest.fixture
def _applied_screened(
    applied_process: HiringProcess,
    screening_at: datetime,
) -> None:
    applied_process.screen(score=8.0, at=screening_at)


@pytest.fixture
def _applied_screened_and_interviewed(
    _applied_screened: None,
    applied_process: HiringProcess,
    interviewers: Sequence[Interviewer],
    first_interview_at: datetime,
) -> None:
    applied_process.interview(
        panel=interviewers,
        notes="solo",
        at=first_interview_at,
    )


@pytest.fixture
def _sourced_screened_once(
    sourced_process: HiringProcess,
    screening_at: datetime,
) -> None:
    sourced_process.screen(score=7.7, at=screening_at)


@pytest.fixture
def _applied_screened_and_interviewed_for_reject(
    applied_process: HiringProcess,
    screening_at: datetime,
    interviewers: Sequence[Interviewer],
    first_interview_at: datetime,
) -> None:
    applied_process.screen(score=9.0, at=screening_at)
    applied_process.interview(
        panel=interviewers,
        notes="Initial conversation.",
        at=first_interview_at,
    )


@pytest.fixture
def _sourced_screened_interviewed_and_rejected(
    sourced_process: HiringProcess,
    screening_at: datetime,
    sam_first_interview_at: datetime,
    interviewers: Sequence[Interviewer],
    rejection_at: datetime,
    role_put_on_hold_reason: str,
) -> None:
    sourced_process.screen(score=9.0, at=screening_at)
    sourced_process.interview(
        panel=interviewers,
        notes="Initial conversation.",
        at=sam_first_interview_at,
    )
    sourced_process.reject(reason=role_put_on_hold_reason, at=rejection_at)


@pytest.fixture
def _sourced_reopened_after_rejection_for_offer(
    sourced_process: HiringProcess,
    second_screening_at: datetime,
    sam_first_interview_at: datetime,
    interviewers: Sequence[Interviewer],
    rejection_at: datetime,
    reinterview_at: datetime,
    role_put_on_hold_reason: str,
) -> None:
    sourced_process.screen(score=9.0, at=second_screening_at)
    sourced_process.interview(
        panel=interviewers,
        notes="Deep backend experience.",
        at=sam_first_interview_at,
    )
    sourced_process.reject(reason=role_put_on_hold_reason, at=rejection_at)
    sourced_process.interview(
        panel=interviewers,
        notes="Re-opened after reorg.",
        at=reinterview_at,
    )


@pytest.fixture
def _sourced_before_second_rejection(
    sourced_process: HiringProcess,
    screening_at: datetime,
    sam_first_interview_at: datetime,
    interviewers: Sequence[Interviewer],
    rejection_at: datetime,
    reinterview_at: datetime,
    role_put_on_hold_reason: str,
) -> None:
    sourced_process.screen(score=9.0, at=screening_at)
    sourced_process.interview(
        panel=interviewers,
        notes="First pass.",
        at=sam_first_interview_at,
    )
    sourced_process.reject(reason=role_put_on_hold_reason, at=rejection_at)
    sourced_process.interview(
        panel=interviewers,
        notes="Re-opened after reorg.",
        at=reinterview_at,
    )


@pytest.fixture
def _applied_interviewed(
    applied_process: HiringProcess,
    screening_at: datetime,
    interviewers: Sequence[Interviewer],
    first_interview_at: datetime,
) -> None:
    applied_process.screen(score=8.0, at=screening_at)
    applied_process.interview(
        panel=interviewers,
        notes="notes",
        at=first_interview_at,
    )
