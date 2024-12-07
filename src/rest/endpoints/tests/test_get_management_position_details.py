from datetime import datetime, timedelta

from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_business_unit,
    create_some_management_position,
    create_some_employee_survey_campaign,
    change_participant_status,
)
from rest.endpoints.tests.helpers import get_admin_token, URLs
from services.tests.helpers import get_campaign_participant_ids
from settings import ParticipationStatus, configs


def assert_response_data(response_data: dict):
    assert isinstance(response_data["id"], int)
    assert isinstance(response_data["name"], str)
    assert isinstance(response_data["roles"], list)
    assert {"name", "id"} == set(response_data["roles"][0].keys())
    assert isinstance(response_data["managers"], list)
    assert response_data["pending_participants_count"] == 1
    assert isinstance(
        datetime.strptime(
            response_data["last_report_end_date"], configs.date_time_format
        ),
        datetime,
    )


def test_get_management_position_details(cleanup_database, fast_client, cleanup_media):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    e = create_some_employee(
        email="test1@example.com", organization_id=org.id, business_unit_id=bu.id
    )
    sc = create_some_employee_survey_campaign(
        organization_id=org.id,
        participant_ids=[e.id],
        start_date=datetime.now() - timedelta(days=30),
        end_date=datetime.now() - timedelta(days=25),
    )
    assert isinstance(sc.id, int)
    participant_ids = get_campaign_participant_ids(campaign_id=sc.id)
    change_participant_status(
        participant_id=participant_ids[0], status=ParticipationStatus.RESPONDED
    )
    assert isinstance(e.id, int)
    assert isinstance(bu.id, int)
    mp = create_some_management_position(
        manager_ids=[e.id],
        name="Test Position",
        role_ids=[bu.id],
        organization_id=org.id,
    )
    token = get_admin_token()
    response = fast_client.get(
        URLs.organization_management_positions.format(id=org.id) + f"{mp.id}/",
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert_response_data(response.json()["result"])
