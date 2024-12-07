from datetime import datetime
from uuid import UUID

from celery_app import celery_app
from cexceptions import (
    NotFoundException,
    DoesNotBelongException,
    LessThanOrEqualException,
    ValidationException,
)
from entity import Participant
from repository import (
    SurveyCampaignRepository,
    ParticipationRepository,
    EmployeeRepository,
)
from settings import ParticipationStatus


def get_survey_campaign_participants(
    campaign_id: int, offset: int, limit: int, status: ParticipationStatus | None = None
) -> tuple[int, list[Participant]]:
    if not SurveyCampaignRepository.exists(_id=campaign_id):
        raise NotFoundException(
            entity="Survey Campaign", arg="ID", value=str(campaign_id)
        )
    (
        total_count,
        participants,
    ) = ParticipationRepository.get_survey_campaign_participants(
        campaign_id=campaign_id,
        offset=offset,
        limit=limit,
        status=status,
    )
    return total_count, participants


def add_participant_to_survey_campaign(campaign_id: int, employee_email: str) -> UUID:
    organization_id = SurveyCampaignRepository.get_organization_id(_id=campaign_id)
    employee_id = EmployeeRepository.get_id_by_email(email=employee_email)
    if not EmployeeRepository.check_employee_exists_in_organization(
        employee_id=employee_id, organization_id=organization_id
    ):
        raise DoesNotBelongException(
            first_entity="Email",
            first_value=str(employee_email),
            second_entity="Organization",
            second_value=str(organization_id),
        )
    start_date = SurveyCampaignRepository.get_start_date(_id=campaign_id)
    end_date = SurveyCampaignRepository.get_end_date(_id=campaign_id)
    participant_id = ParticipationRepository.add_participant_to_campaign(
        campaign_id=campaign_id, employee_id=employee_id
    )
    if end_date < datetime.now():
        raise LessThanOrEqualException(
            first_entity="Campaign End Time",
            second_entity="Current Time",
        )
    if start_date < datetime.now():
        celery_app.send_task(
            "tasks.send_survey_campaign_emails.send_individual_campaign_email_task",
            args=[campaign_id, participant_id],
        )
    return participant_id


def _assert_valid_status(status: ParticipationStatus) -> None:
    if status not in (ParticipationStatus.DUE, ParticipationStatus.CANCELED):
        raise ValidationException(entities="Status", values=status.value)


def update_survey_campaign_participant_status(
    participant_id: UUID, campaign_id: int, status: ParticipationStatus
):
    start_date: datetime = SurveyCampaignRepository.get_start_date(_id=campaign_id)
    if start_date < datetime.now():
        raise LessThanOrEqualException(
            first_entity="Current Time", second_entity="Start Date"
        )
    if not ParticipationRepository.belongs_to_survey_campaign(
        participant_id=participant_id, campaign_id=campaign_id
    ):
        raise DoesNotBelongException(
            first_entity="Participant ID",
            first_value=str(participant_id),
            second_entity="SurveyCampaign ID",
            second_value=str(campaign_id),
        )
    _assert_valid_status(status=status)
    ParticipationRepository.update_status(
        _id=participant_id,
        status=status,
    )


def get_employee_survey_campaign_end_date(employee_id: int) -> datetime:
    return ParticipationRepository.employee_survey_campaign_end_date(
        employee_id=employee_id
    )
