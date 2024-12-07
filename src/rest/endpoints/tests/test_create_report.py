from datetime import datetime, timedelta

from starlette.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_management_position,
    create_some_business_unit,
    create_some_employee_survey_campaign,
    get_campaign_participant_ids,
    change_participant_status,
)
from settings import configs, ParticipationStatus
from .helpers import get_admin_token, URLs


def _create_report_requirements() -> tuple[dict, int]:
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
    sc = create_some_employee_survey_campaign(
        start_date=datetime.now() - timedelta(days=99),
        end_date=datetime.now() - timedelta(days=95),
        organization_id=org.id,
        participant_ids=[e2.id],
    )
    assert isinstance(sc.id, int)
    participant = get_campaign_participant_ids(sc.id)
    assert len(participant) == 1
    change_participant_status(
        participant_id=participant[0], status=ParticipationStatus.RESPONDED
    )
    start_date = datetime.now() - timedelta(days=100)
    end_date = start_date + timedelta(days=10)
    data = dict(
        title="Test Report 1",
        management_position_id=mp.id,
        start_date=start_date.strftime(configs.date_time_format),
        end_date=end_date.strftime(configs.date_time_format),
    )
    return data, sc.id


def test_create_report_with_failing_etl_response(
    cleanup_database, fast_client, mock_post_request_failure, cleanup_media
):
    data, campaign_id = _create_report_requirements()
    token = get_admin_token()
    response = fast_client.post(
        URLs.report,
        json=data,
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE
    assert response.json() == {
        "error": "etl failed with message: (Service unavailable)"
    }
    # make sure the participant is not removed
    participant = get_campaign_participant_ids(campaign_id)
    assert len(participant) == 1


def test_create_report(cleanup_database, fast_client, mock_post_request, cleanup_media):
    data, _sc = _create_report_requirements()
    token = get_admin_token()
    response = fast_client.post(
        URLs.report,
        json=data,
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Report Creation Request Submitted"}
