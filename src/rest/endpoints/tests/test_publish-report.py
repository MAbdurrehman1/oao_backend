from datetime import datetime, timedelta

from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_management_position,
    create_some_business_unit,
    create_some_employee_survey_campaign,
    create_some_report,
    get_campaign_participant_ids,
    change_participant_status,
)
from settings import ParticipationStatus
from .helpers import get_admin_token, URLs


def test_publish_report(
    cleanup_database, fast_client, mock_post_request, cleanup_media
):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id, name="BU1")
    e1 = create_some_employee(
        email="test1@example.org", business_unit_id=bu.id, organization_id=org.id
    )
    e2 = create_some_employee(
        email="test2@example.org", business_unit_id=bu.id, organization_id=org.id
    )
    assert isinstance(e1.id, int)
    assert isinstance(e2.id, int)
    assert isinstance(bu.id, int)
    mp = create_some_management_position(
        organization_id=org.id, role_ids=[bu.id], manager_ids=[e1.id]
    )
    assert isinstance(mp.id, int)
    sc = create_some_employee_survey_campaign(
        start_date=datetime.now() - timedelta(days=99),
        end_date=datetime.now() - timedelta(days=95),
        organization_id=org.id,
        participant_ids=[e2.id],
    )
    assert isinstance(sc.id, int)
    participant = get_campaign_participant_ids(sc.id)[0]
    change_participant_status(
        participant_id=participant, status=ParticipationStatus.RESPONDED
    )
    start_date = datetime.now() - timedelta(days=100)
    end_date = start_date + timedelta(days=10)
    report = create_some_report(end_date=end_date, position_id=mp.id)
    assert isinstance(report.id, int)
    token = get_admin_token()
    response = fast_client.post(
        URLs.publish_report.format(id=report.id),
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Report Published Successfully"}
