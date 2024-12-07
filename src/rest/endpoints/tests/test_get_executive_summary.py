import httpx
from starlette.status import HTTP_200_OK

from entity import Report, Employee, User
from repository.tests.helpers import (
    create_some_organization,
    create_some_business_unit,
    create_some_employee,
    create_some_management_position,
    create_some_report,
    create_some_report_goal,
    create_some_innovation_idea,
    create_some_employee_survey_campaign,
    get_campaign_participant_ids,
    add_participants_to_report,
    publish_report,
    rate_idea,
)
from rest.endpoints.tests.helpers import get_access_token, get_admin_token, URLs


def _create_report_executive_summaries(publish: bool) -> tuple[Report, Employee]:
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    e1 = create_some_employee(
        email="test1@example.com", organization_id=org.id, business_unit_id=bu.id
    )
    e2 = create_some_employee(
        email="test2@example.com", organization_id=org.id, business_unit_id=bu.id
    )
    assert isinstance(e2.id, int)
    sc = create_some_employee_survey_campaign(
        organization_id=org.id,
        participant_ids=[e2.id],
    )
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(campaign_id=sc.id)[0]
    assert isinstance(e1.id, int)
    assert isinstance(e2.id, int)
    assert isinstance(bu.id, int)
    mp = create_some_management_position(
        manager_ids=[e1.id],
        name="Test Position",
        role_ids=[bu.id],
        organization_id=org.id,
    )
    assert isinstance(mp.id, int)
    r = create_some_report(position_id=mp.id)
    assert isinstance(r.id, int)
    create_some_report_goal(report_id=r.id, manager_id=e1.id, title="Title1")
    create_some_report_goal(report_id=r.id, manager_id=e1.id, title="Title2")
    idea1 = create_some_innovation_idea(participation_id=p_id)
    idea2 = create_some_innovation_idea(participation_id=p_id)
    create_some_innovation_idea(participation_id=p_id)
    assert isinstance(idea1.id, int)
    assert isinstance(idea2.id, int)
    add_participants_to_report(participation_ids=[p_id], report_id=r.id)
    rate_idea(idea_id=idea1.id, manager_id=e1.id, rate=2)
    rate_idea(idea_id=idea2.id, manager_id=e1.id, rate=2)
    if publish:
        publish_report(report_id=r.id)
    return r, e1


def _assert_response_data(response: httpx.Response):
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert set(data.keys()) == {
        "snapshots",
        "key_insights",
        "speed_of_transformation",
        "recommendations_generated",
        "ideas_reviewed",
    }
    assert data["ideas_reviewed"] == 2


def test_get_executive_summary(cleanup_database, fast_client, cleanup_media):
    r, e1 = _create_report_executive_summaries(publish=True)
    assert isinstance(e1.user, User)
    manager_token = get_access_token(e1.user)
    response = fast_client.get(
        URLs.executive_summary.format(_id=r.id),
        headers=dict(Authorization=manager_token),
    )
    _assert_response_data(response)


def test_get_executive_summary_as_admin(cleanup_database, fast_client, cleanup_media):
    r, _ = _create_report_executive_summaries(publish=False)
    manager_token = get_admin_token()
    response = fast_client.get(
        URLs.executive_summary.format(_id=r.id),
        headers=dict(Authorization=manager_token),
    )
    _assert_response_data(response)
