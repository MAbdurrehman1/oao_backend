from datetime import datetime, timedelta

from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_employee_survey_campaign,
    create_some_business_unit,
)
from services.tests.helpers import tribble
from settings import configs
from .helpers import get_admin_token, URLs, string_to_file_tuple


def test_create_survey_campaign(
    cleanup_database, fast_client, mock_send_mail, cleanup_media
):
    organization = create_some_organization()
    employee = create_some_employee(
        organization_id=organization.id, email="test@employee.example"
    )
    df = tribble(
        ["email"],
        employee.user.email,
    )
    start_date = datetime.now()
    end_date = start_date + timedelta(days=2)
    params_data = dict(
        title="test_title",
        survey_url="test_url",
        organization_id=organization.id,
        start_date_str=start_date.strftime(configs.date_time_format),
        end_date_str=end_date.strftime(configs.date_time_format),
    )
    file = string_to_file_tuple(df.to_csv())
    token = get_admin_token()
    response = fast_client.post(
        url=URLs.survey_campaign,
        files=dict(file=file),
        params=params_data,
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Survey Campaign Created Successfully"}


def test_create_survey_campaign_when_some_users_are_on_another_campaign(
    cleanup_database, fast_client
):
    organization = create_some_organization()
    assert isinstance(organization.id, int)
    bu = create_some_business_unit(organization_id=organization.id)
    employees = [
        create_some_employee(
            organization_id=organization.id,
            email=f"test{i+1}@employee.example",
            business_unit_id=bu.id,
        )
        for i in range(3)
    ]
    df = tribble(["email"], *[e.user.email for e in employees])
    create_some_employee_survey_campaign(
        start_date=datetime.now() - timedelta(days=10),
        end_date=datetime.now() + timedelta(days=10),
        organization_id=organization.id,
        participant_ids=[employees[0].id],
    )
    start_date = datetime.now()
    end_date = start_date + timedelta(days=2)
    params_data = dict(
        title="test_title",
        survey_url="test_url",
        organization_id=organization.id,
        start_date_str=start_date.strftime(configs.date_time_format),
        end_date_str=end_date.strftime(configs.date_time_format),
    )
    file = string_to_file_tuple(df.to_csv())
    token = get_admin_token()
    response = fast_client.post(
        url=URLs.survey_campaign,
        files=dict(file=file),
        params=params_data,
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json() == {
        "error": "User with email('s) "
        "('test1@employee.example',) already "
        "belong to a SurveyCampaign"
    }
