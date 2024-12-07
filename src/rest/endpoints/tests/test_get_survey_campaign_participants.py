from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_employee_survey_campaign,
    create_some_business_unit,
    get_campaign_participant_ids,
    change_participant_status,
)
from rest.endpoints.tests.helpers import get_admin_token, URLs
from settings import ParticipationStatus


def test_get_survey_campaign_participants(
    fast_client, cleanup_database, cleanup_redis, cleanup_media
):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(name="test bu", organization_id=org.id)
    employee1 = create_some_employee(
        email="test1@example.com", organization_id=org.id, business_unit_id=bu.id
    )
    employee2 = create_some_employee(
        email="test12@example.com", organization_id=org.id, business_unit_id=bu.id
    )
    sc = create_some_employee_survey_campaign(
        participant_ids=[employee1.id, employee2.id], organization_id=org.id
    )
    token = get_admin_token()
    response = fast_client.get(
        url=URLs.survey_campaign_participants.format(id=sc.id),
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert response.json()["total_count"] == 2
    assert len(data) == 2
    assert (
        set(data[0].keys())
        == set(data[1])
        == {
            "id",
            "email",
            "first_name",
            "last_name",
            "location",
            "role_title",
            "status",
            "business_unit",
        }
    )


def test_status_filter_works(
    fast_client, cleanup_database, cleanup_redis, cleanup_media
):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(name="test bu", organization_id=org.id)
    employee1 = create_some_employee(
        email="test1@example.com", organization_id=org.id, business_unit_id=bu.id
    )
    employee2 = create_some_employee(
        email="test12@example.com", organization_id=org.id, business_unit_id=bu.id
    )
    sc = create_some_employee_survey_campaign(
        participant_ids=[employee1.id, employee2.id], organization_id=org.id
    )
    token = get_admin_token()
    response = fast_client.get(
        url=URLs.survey_campaign_participants.format(id=sc.id) + "?status=canceled",
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert len(data) == 0
    assert isinstance(sc.id, int)
    participant_ids = get_campaign_participant_ids(sc.id)
    change_participant_status(
        participant_id=participant_ids[0], status=ParticipationStatus.CANCELED
    )
    response = fast_client.get(
        url=URLs.survey_campaign_participants.format(id=sc.id) + "?status=canceled",
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert len(data) == 1
    assert data[0]["status"] == "canceled"
