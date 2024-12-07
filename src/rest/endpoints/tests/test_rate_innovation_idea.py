from starlette.status import HTTP_200_OK

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
)
from rest.endpoints.tests.helpers import get_access_token, URLs


def test_rate_innovation_idea(cleanup_database, fast_client, cleanup_media):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    e1 = create_some_employee(
        email="test1@example.com", organization_id=org.id, business_unit_id=bu.id
    )
    e2 = create_some_employee(
        email="test2@example.com", organization_id=org.id, business_unit_id=bu.id
    )
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
    add_participants_to_report(report_id=r.id, participation_ids=[p_id])
    idea = create_some_innovation_idea(participation_id=p_id)
    assert isinstance(idea.id, int)
    manager_token = get_access_token(e1.user)
    response = fast_client.post(
        URLs.rate_idea.format(_id=idea.id),
        headers=dict(Authorization=manager_token),
        json={"rate": 2},
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Innovation Idea Rated Successfully"}
