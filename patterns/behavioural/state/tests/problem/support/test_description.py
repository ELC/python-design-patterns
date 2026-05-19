from datetime import datetime

import pytest

from patterns.behavioural.state.problem import (
    HiringProcess,
    HiringProcessDescription,
    InvalidCandidateState,
)


def test_applied_process_renders_application_date(
    applied_process: HiringProcess,
    applied_at: datetime,
    applied_candidate_name: str,
    applied_role: str,
) -> None:
    description = HiringProcessDescription(applied_process)

    assert str(description) == (
        f"{applied_candidate_name} applied for {applied_role} "
        f"({applied_at.strftime('%Y-%m-%d')})"
    )


def test_sourced_process_renders_recruiter_and_sourcing_date(
    sourced_process: HiringProcess,
    sourced_at: datetime,
    sourced_candidate_name: str,
    sourced_role: str,
    recruiter: str,
) -> None:
    description = HiringProcessDescription(sourced_process)

    assert str(description) == (
        f"{sourced_candidate_name} sourced by {recruiter} for {sourced_role} "
        f"({sourced_at.strftime('%Y-%m-%d')})"
    )


def test_applied_process_without_timestamp_cannot_be_described(
    applied_without_timestamp_process: HiringProcess,
) -> None:
    description = HiringProcessDescription(applied_without_timestamp_process)

    with pytest.raises(
        InvalidCandidateState,
        match="APPLIED cannot be described: requires an application timestamp",
    ):
        str(description)


def test_sourced_process_without_timestamp_cannot_be_described(
    sourced_without_timestamp_process: HiringProcess,
) -> None:
    description = HiringProcessDescription(sourced_without_timestamp_process)

    with pytest.raises(
        InvalidCandidateState,
        match="SOURCED cannot be described: requires a recruiter and sourcing timestamp",
    ):
        str(description)


def test_screened_process_without_timestamp_cannot_be_described(
    screened_without_timestamp_process: HiringProcess,
) -> None:
    description = HiringProcessDescription(screened_without_timestamp_process)

    with pytest.raises(
        InvalidCandidateState,
        match="SCREENED cannot be described: requires a screening timestamp",
    ):
        str(description)


def test_screened_process_without_source_cannot_be_described(
    screened_without_source_process: HiringProcess,
) -> None:
    description = HiringProcessDescription(screened_without_source_process)

    with pytest.raises(
        InvalidCandidateState,
        match="SCREENED cannot be described: requires a screening source",
    ):
        str(description)


def test_offered_process_without_offer_details_cannot_be_described(
    offered_without_offer_details_process: HiringProcess,
) -> None:
    description = HiringProcessDescription(offered_without_offer_details_process)

    with pytest.raises(
        InvalidCandidateState,
        match=(
            "OFFER_EXTENDED cannot be described: "
            "requires offer salary, offer timestamp, and expiry"
        ),
    ):
        str(description)


def test_hired_process_without_hire_details_cannot_be_described(
    hired_without_hire_details_process: HiringProcess,
) -> None:
    description = HiringProcessDescription(hired_without_hire_details_process)

    with pytest.raises(
        InvalidCandidateState,
        match=(
            "HIRED cannot be described: "
            "requires employee id, hire timestamp, and start date"
        ),
    ):
        str(description)


def test_abandoned_process_without_timestamp_cannot_be_described(
    abandoned_without_timestamp_process: HiringProcess,
) -> None:
    description = HiringProcessDescription(abandoned_without_timestamp_process)

    with pytest.raises(
        InvalidCandidateState,
        match="ABANDONED cannot be described: requires an abandonment timestamp",
    ):
        str(description)


def test_interviewed_process_without_rounds_cannot_be_described(
    interviewed_without_rounds_process: HiringProcess,
) -> None:
    description = HiringProcessDescription(interviewed_without_rounds_process)

    with pytest.raises(
        InvalidCandidateState,
        match="INTERVIEWED cannot be described: requires at least one interview round",
    ):
        str(description)


def test_rejected_process_without_rejection_history_cannot_be_described(
    rejected_without_rejections_process: HiringProcess,
) -> None:
    description = HiringProcessDescription(rejected_without_rejections_process)

    with pytest.raises(
        InvalidCandidateState,
        match="REJECTED cannot be described: requires at least one rejection",
    ):
        str(description)
