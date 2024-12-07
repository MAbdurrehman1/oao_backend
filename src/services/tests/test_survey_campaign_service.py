import re
from datetime import datetime, timedelta
from io import BytesIO
from uuid import UUID

import pytest

from cexceptions import (
    MissingEntityException,
    NotFoundException,
    MissingValuesException,
    LessThanOrEqualException,
)
from repository import CeleryTaskRepository
from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_business_unit,
)
from settings import configs
from .helpers import tribble
from ..survey_campaign_service import submit_survey_campaign


def test_submit_survey_campaign_with_invalid_columns(cleanup_database, cleanup_media):
    organization = create_some_organization()
    # fmt: off
    df = tribble(
        ["invalid_key",],
        "test_value",
    )
    # fmt: on
    assert isinstance(organization.id, int)
    with pytest.raises(
        MissingEntityException, match=re.escape("email column must be provided.")
    ):
        submit_survey_campaign(
            emails_csv_file=BytesIO(df.to_csv().encode("utf-8")),
            title="Test Title",
            organization_id=organization.id,
            start_date_str=datetime.now().strftime(configs.date_time_format),
            end_date_str=(datetime.now() + timedelta(days=2)).strftime(
                configs.date_time_format
            ),
        )


def test_invalid_end_date(cleanup_database, cleanup_media):
    organization = create_some_organization()
    employee = create_some_employee(organization_id=organization.id)
    end_date = datetime.now()
    start_date = end_date + timedelta(days=2)
    # fmt: off
    df = tribble(
        ["email",],
        employee.user.email,
    )
    assert isinstance(organization.id, int)
    # fmt: on
    with pytest.raises(
        LessThanOrEqualException,
        match=re.escape("Start Date must be less than or equal to End Date"),
    ):
        submit_survey_campaign(
            emails_csv_file=BytesIO(df.to_csv().encode("utf-8")),
            title="Test Title",
            organization_id=organization.id,
            start_date_str=start_date.strftime(configs.date_time_format),
            end_date_str=end_date.strftime(configs.date_time_format),
        )


def test_submit_survey_campaign_with_invalid_organization(cleanup_media):
    # fmt: off
    df = tribble(
        ["email",],
        "johndoe@gmail.com",
    )
    # fmt: on
    with pytest.raises(
        NotFoundException, match=re.escape("Organization with ID (1) not found.")
    ):
        submit_survey_campaign(
            emails_csv_file=BytesIO(df.to_csv().encode("utf-8")),
            title="Test Title",
            organization_id=1,
            start_date_str=datetime.now().strftime(configs.date_time_format),
            end_date_str=(datetime.now() + timedelta(days=2)).strftime(
                configs.date_time_format
            ),
        )


def test_submit_survey_campaign_with_invalid_email_address(
    cleanup_database, cleanup_media
):
    organization = create_some_organization(
        logo_user_email="test_org@example.com",
        logo_name="test_org.png",
    )
    employee = create_some_employee(email="test1@gmail.com")
    # fmt: off
    df = tribble(
        ["email", ],
          employee.user.email,  # noqa: E131
    )
    emails = (employee.user.email,)
    # fmt: on
    assert isinstance(organization.id, int)
    with pytest.raises(
        MissingValuesException,
        match=re.escape(f"{emails} is/are missing in Organization Contacts."),
    ):
        submit_survey_campaign(
            emails_csv_file=BytesIO(df.to_csv().encode("utf-8")),
            title="Test Title",
            organization_id=organization.id,
            start_date_str=datetime.now().strftime(configs.date_time_format),
            end_date_str=(datetime.now() + timedelta(days=2)).strftime(
                configs.date_time_format
            ),
        )


def test_submit_survey_campaign_successfully(
    cleanup_database, mock_send_mail, cleanup_media
):
    organization = create_some_organization()
    assert isinstance(organization.id, int)
    bu = create_some_business_unit(organization_id=organization.id)
    employee1 = create_some_employee(
        email="test1@gmail.com", organization_id=organization.id, business_unit_id=bu.id
    )
    employee2 = create_some_employee(
        email="test2@gmail.com", organization_id=organization.id, business_unit_id=bu.id
    )
    title = "Test Title"
    start_date = datetime(2024, 5, 22, 12, 30, 1)
    end_date = start_date + timedelta(days=2)
    # fmt: off
    df = tribble(
        ["email", ],
        employee1.user.email,
        employee2.user.email,
    )
    # fmt: on
    assert isinstance(organization.id, int)
    submitted_survey_campaign = submit_survey_campaign(
        emails_csv_file=BytesIO(df.to_csv().encode("utf-8")),
        title=title,
        organization_id=organization.id,
        start_date_str=start_date.strftime(configs.date_time_format),
        end_date_str=end_date.strftime(configs.date_time_format),
    )
    assert isinstance(submitted_survey_campaign.id, int)
    assert isinstance(submitted_survey_campaign.created_at, datetime)
    assert isinstance(submitted_survey_campaign.updated_at, datetime)
    assert submitted_survey_campaign.title == title
    assert submitted_survey_campaign.organization_id == organization.id
    assert submitted_survey_campaign.start_date == start_date
    assert submitted_survey_campaign.end_date == end_date
    assert isinstance(submitted_survey_campaign.participant_ids, list)
    assert set(submitted_survey_campaign.participant_ids) == {
        employee1.id,
        employee2.id,
    }
    task_id = CeleryTaskRepository.get_task_id(
        post_fix="survey_campaign:send_email_task:",
        identifier=submitted_survey_campaign.id,
    )
    assert isinstance(task_id, UUID)
