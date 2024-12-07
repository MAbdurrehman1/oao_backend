from datetime import datetime, timedelta
from uuid import UUID

from starlette.status import HTTP_200_OK

from rest.endpoints.tests.helpers import URLs, get_admin_token
from repository.tests.helpers import (
    create_some_employee_survey_campaign,
    create_some_employee,
    create_some_organization,
    create_some_business_unit,
)


def test_add_survey_campaign_participant(
    cleanup_database,
    fast_client,
    cleanup_media,
    cleanup_redis,
    mock_send_mail,
):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    employee1 = create_some_employee(
        organization_id=org.id, email="test1@example.com", business_unit_id=bu.id
    )
    employee2 = create_some_employee(
        organization_id=org.id, email="test2@example.com", business_unit_id=bu.id
    )
    sc = create_some_employee_survey_campaign(
        start_date=datetime.now() - timedelta(seconds=20 * 60),
        organization_id=org.id,
        participant_ids=[employee1.id],
    )
    data = dict(employee_email=employee2.user.email)
    token = get_admin_token()
    response = fast_client.post(
        url=URLs.survey_campaign_participants.format(id=sc.id),
        headers=dict(Authorization=token),
        json=data,
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert isinstance(UUID(data["participant_id"]), UUID)
