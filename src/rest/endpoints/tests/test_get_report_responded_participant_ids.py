from datetime import datetime, timedelta
from uuid import UUID

from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_employee_survey_campaign,
    create_some_management_position,
    create_some_business_unit,
    get_campaign_participant_ids,
    change_participant_status,
)
from settings import ParticipationStatus
from .helpers import get_admin_token, URLs


def test_get_report_responded_participant_ids(
    cleanup_database, fast_client, cleanup_media
):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id, name="BU1")
    create_some_business_unit(organization_id=org.id, name="BU2", parent_id=bu.id)
    assert isinstance(bu.id, int)
    e1 = create_some_employee(
        email="test1@example.org", business_unit_id=bu.id, organization_id=org.id
    )
    e2 = create_some_employee(
        email="test2@example.org", business_unit_id=bu.id, organization_id=org.id
    )
    assert isinstance(e1.id, int)
    assert isinstance(e2.id, int)
    sc = create_some_employee_survey_campaign(
        organization_id=org.id,
        participant_ids=[e1.id],
        start_date=datetime.now() - timedelta(days=30),
        end_date=datetime.now() - timedelta(days=25),
    )
    assert isinstance(sc.id, int)
    participant_ids = get_campaign_participant_ids(campaign_id=sc.id)
    change_participant_status(
        participant_id=participant_ids[0], status=ParticipationStatus.RESPONDED
    )
    mp = create_some_management_position(
        organization_id=org.id, role_ids=[bu.id], manager_ids=[e2.id]
    )
    token = get_admin_token()
    response = fast_client.get(
        URLs.management_position_report_participants.format(id=mp.id),
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert isinstance(data, list)
    assert len(data) == 1
    assert isinstance(UUID(data[0]), UUID)
