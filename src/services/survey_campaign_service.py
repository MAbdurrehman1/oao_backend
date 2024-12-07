from typing import BinaryIO
from uuid import UUID
from datetime import datetime

import pytz

from celery_app import celery_app
from entity import SurveyCampaign
from cexceptions import (
    MissingValuesException,
    MissingEntityException,
    LessThanOrEqualException,
    NotFoundException,
    AlreadyBelongException,
)
from repository import (
    EmployeeRepository,
    OrganizationRepository,
    CeleryTaskRepository,
    ParticipationRepository,
)
from repository import SurveyCampaignRepository
from .utils import uploaded_csv_to_df
from settings import configs
from utils.validation_helpers import string_to_date


def submit_survey_campaign(
    emails_csv_file: BinaryIO,
    title: str,
    organization_id: int,
    start_date_str: str,
    end_date_str: str,
) -> SurveyCampaign:
    df = uploaded_csv_to_df(emails_csv_file)
    if "email" not in df.columns:
        raise MissingEntityException(entity="email column")
    emails_list = list(set(df["email"].to_list()))
    emails_list = [email.lower() for email in emails_list]
    organization = OrganizationRepository.get_by_id(organization_id)
    existing_email_data = EmployeeRepository.get_exiting_ids_by_email(
        emails=emails_list, organization_id=organization_id
    )
    emails_with_survey_campaigns = (
        ParticipationRepository.filter_employees_with_in_progress_survey_campaign(
            emails=emails_list,
        )
    )
    if emails_with_survey_campaigns:
        raise AlreadyBelongException(
            owned_entity="User",
            owner_entity="SurveyCampaign",
            arg="email",
            values=str(tuple(emails_with_survey_campaigns)),
        )
    missing_emails = list(set(emails_list) - set(existing_email_data.keys()))
    if missing_emails:
        raise MissingValuesException(
            entities="Organization Contacts", values=str(tuple(missing_emails))
        )
    start_date = string_to_date(start_date_str, configs.date_time_format)
    end_date = string_to_date(end_date_str, configs.date_time_format)
    if end_date < start_date:
        raise LessThanOrEqualException(
            first_entity="Start Date", second_entity="End Date"
        )

    survey_campaign = SurveyCampaign(  # noqa: F841
        title=title,
        organization_id=organization_id,
        start_date=start_date,
        end_date=end_date,
        participant_ids=[int(_id) for _id in existing_email_data.values()],
        organization=organization,
    )
    submitted_survey_campaign = SurveyCampaignRepository.store(survey_campaign)
    result = celery_app.send_task(
        "tasks.send_survey_campaign_emails.send_survey_campaign_emails_task",
        args=[submitted_survey_campaign.id],
        eta=pytz.utc.localize(start_date),
    )
    assert isinstance(submitted_survey_campaign.id, int)
    CeleryTaskRepository.set_task_id(
        post_fix="survey_campaign:send_email_task:",
        identifier=submitted_survey_campaign.id,
        task_id=UUID(result.id),
    )
    return submitted_survey_campaign


def update_survey_campaign(
    campaign_id: int,
    title: str = None,
    start_date_str: str = None,
    end_date_str: str = None,
) -> SurveyCampaign:
    start_date = None
    end_date = None
    survey_campaign = SurveyCampaignRepository.get(campaign_id=campaign_id)
    if start_date_str:
        if survey_campaign.start_date <= datetime.now():
            raise LessThanOrEqualException(
                first_entity="Current Time", second_entity="Start Date"
            )
        start_date = string_to_date(start_date_str, configs.date_time_format)
        survey_campaign.start_date = start_date
    if end_date_str:
        if survey_campaign.end_date <= datetime.now():
            raise LessThanOrEqualException(
                first_entity="Current Time", second_entity="End Date"
            )
        end_date = string_to_date(end_date_str, configs.date_time_format)
        survey_campaign.end_date = end_date
    if (start_date and end_date) and (start_date > end_date):
        raise LessThanOrEqualException(
            first_entity="Start Date", second_entity="End Date"
        )
    if title:
        survey_campaign.title = title
    updated_survey_campaign = SurveyCampaignRepository.update(
        survey_campaign=survey_campaign
    )
    if start_date:
        task_id = CeleryTaskRepository.get_task_id(
            post_fix="survey_campaign:send_email_task:",
            identifier=campaign_id,
        )
        assert isinstance(task_id, UUID)
        celery_app.control.revoke(task_id, terminate=True)
        result = celery_app.send_task(
            "tasks.send_survey_campaign_emails.send_survey_campaign_emails_task",
            args=[campaign_id],
            eta=pytz.utc.localize(start_date),
        )
        CeleryTaskRepository.set_task_id(
            post_fix="survey_campaign:send_email_task:",
            identifier=campaign_id,
            task_id=UUID(result.id),
        )
    return updated_survey_campaign


def get_survey_campaign(campaign_id: int) -> SurveyCampaign:
    survey_campaign = SurveyCampaignRepository.get(campaign_id)
    return survey_campaign


def get_organization_survey_campaigns(
    organization_id: int, offset: int, limit: int
) -> tuple[int, list[SurveyCampaign]]:
    if not OrganizationRepository.exists(organization_id=organization_id):
        raise NotFoundException(
            entity="Organization", arg="ID", value=str(organization_id)
        )
    total_count, survey_campaigns = SurveyCampaignRepository.get_list(
        offset=offset, limit=limit, organization_id=organization_id
    )
    return total_count, survey_campaigns
