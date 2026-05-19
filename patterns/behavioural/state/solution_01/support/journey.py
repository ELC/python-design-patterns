from datetime import date, datetime
from decimal import Decimal

from .hiring_process import HiringProcess
from .ids import employee_id
from .interview import Interviewer
from .states import Applied, Sourced

SECOND_SCREENING_AT = datetime(2026, 2, 1, 9, 0)
FIRST_REJECTION_AT = datetime(2026, 2, 5, 11, 0)
RESCREEN_AT = datetime(2026, 2, 8, 9, 0)
FIRST_INTERVIEW_AT = datetime(2026, 2, 10, 14, 0)
SECOND_REJECTION_AT = datetime(2026, 2, 12, 11, 0)
REINTERVIEW_AT = datetime(2026, 2, 18, 14, 0)
SECOND_INTERVIEW_AT = datetime(2026, 2, 20, 14, 0)
OFFER_AT = datetime(2026, 2, 21, 10, 0)
HIRE_AT = datetime(2026, 2, 27, 9, 0)
SAM_SOURCED_AT = datetime(2026, 1, 25, 10, 0)
CASEY_APPLIED_AT = datetime(2026, 1, 5, 9, 0)
OFFER_EXPIRES_AT = datetime(2026, 2, 25, 23, 59)
START_DATE = date(2026, 3, 1)
CASEY_SCREEN_AT = datetime(2026, 1, 10, 9, 0)
CASEY_ABANDON_AT = datetime(2026, 1, 11, 16, 0)

OFFER_SALARY = Decimal("165000.00")


def run_hiring_demo() -> None:
    panel = (
        Interviewer("Taylor Kim", "Engineering Manager"),
        Interviewer("Riley Park", "Tech Lead"),
    )

    process = HiringProcess(
        Sourced(
            candidate_name="Sam Chen",
            role="Staff Engineer",
            recruiter="Jordan Lee",
            sourced_at=SAM_SOURCED_AT,
        )
    )
    process = process.screen(score=9.0, at=SECOND_SCREENING_AT)
    print(process)
    process = process.reject(reason="Role put on hold", at=FIRST_REJECTION_AT)
    print(process)
    process = process.screen(score=8.8, at=RESCREEN_AT)
    print(process)
    process = process.interview(
        panel=panel,
        notes="Deep backend experience.",
        at=FIRST_INTERVIEW_AT,
    )
    print(process)
    process = process.reject(reason="Budget freeze", at=SECOND_REJECTION_AT)
    print(process)
    process = process.interview(
        panel=panel,
        notes="Re-opened after reorg.",
        at=REINTERVIEW_AT,
    )
    print(process)
    process = process.interview(
        panel=panel,
        notes="Panel debrief.",
        at=SECOND_INTERVIEW_AT,
    )
    print(process)
    process = process.make_offer(
        offer_salary=OFFER_SALARY,
        offer_expires_at=OFFER_EXPIRES_AT,
        at=OFFER_AT,
    )
    print(process)
    process = process.hire(
        start_date=START_DATE,
        employee_id=employee_id("Sam Chen"),
        at=HIRE_AT,
    )
    print(process)

    process = HiringProcess(
        Applied(
            candidate_name="Casey Lee",
            role="Product Manager",
            applied_at=CASEY_APPLIED_AT,
        )
    )
    process = process.screen(score=8.2, at=CASEY_SCREEN_AT)
    print(process)
    process = process.abandon(at=CASEY_ABANDON_AT)
    print(process)
