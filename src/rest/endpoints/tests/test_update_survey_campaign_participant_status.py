from starlette.status import HTTP_200_OK

from rest.endpoints.tests.helpers import URLs, get_admin_token
from services.tests.helpers import get_campaign_participant_ids
from repository.tests.helpers import (
    create_some_employee_survey_campaign,
    create_some_employee,
    create_some_organization,
    create_some_business_unit,
)
from settings import ParticipationStatus


def test_update_survey_campaign_participant_status(
    cleanup_database, fast_client, cleanup_media
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
        organization_id=org.id,
        participant_ids=[employee1.id, employee2.id],
    )
    assert isinstance(sc.id, int)
    participant_ids = get_campaign_participant_ids(campaign_id=sc.id)
    token = get_admin_token()
    response = fast_client.put(
        url=URLs.survey_campaign_participants.format(id=sc.id)
        + f"{participant_ids[0]}/",
        headers=dict(Authorization=token),
        json=dict(status=ParticipationStatus.CANCELED.value),
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Participant Status Changed successfully"}
