from datetime import datetime, timedelta

import httpx
from starlette.status import HTTP_200_OK

from entity import Employee, Report, User

from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_business_unit,
    create_some_employee_survey_campaign,
    create_some_innovation_idea,
    get_campaign_participant_ids,
    create_some_management_position,
    create_some_report,
    add_participants_to_report,
    publish_report,
)
from .helpers import URLs, get_access_token


def _create_innovation_idea_for_report(publish: bool) -> tuple[Report, Employee]:
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    e1 = create_some_employee(
        email="test1@example.com",
        organization_id=org.id,
        business_unit_id=bu.id,
    )
    e2 = create_some_employee(
        email="test2@example.com",
        organization_id=org.id,
        business_unit_id=bu.id,
    )
    assert isinstance(e1.id, int)
    sc = create_some_employee_survey_campaign(
        organization_id=org.id,
        participant_ids=[e1.id],
        start_date=datetime.now() - timedelta(days=365),
        end_date=datetime.now() - timedelta(days=20),
    )
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(
        campaign_id=sc.id,
    )[0]
    create_some_innovation_idea(participation_id=p_id)
    mp = create_some_management_position(
        organization_id=org.id, manager_ids=[e2.id], role_ids=[bu.id]  # type: ignore
    )
    assert isinstance(mp.id, int)
    r = create_some_report(position_id=mp.id)
    assert isinstance(r.id, int)
    add_participants_to_report(report_id=r.id, participation_ids=[p_id])
    if publish:
        publish_report(report_id=r.id)
    return r, e2


def _assert_response_data(response: httpx.Response):
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert len(data) == 1
    assert set(data[0].keys()) == {
        "id",
        "title",
        "feasibility_score",
        "confidence_score",
        "impact_score",
    }


def test_get_report_matrix_innovation_ideas_list(
    cleanup_database, fast_client, cleanup_media
):
    report, manager = _create_innovation_idea_for_report(publish=True)
    assert isinstance(manager.user, User)
    manager_token = get_access_token(manager.user)
    response = fast_client.get(
        url=URLs.report_ideas_matrix.format(id=report.id),
        headers=dict(Authorization=manager_token),
    )
    _assert_response_data(response)
