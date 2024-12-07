from starlette.status import HTTP_200_OK

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
    rate_idea,
)
from .helpers import URLs, get_access_token


def test_get_innovation_idea(cleanup_database, fast_client, cleanup_media):
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
    assert isinstance(e2.id, int)
    sc = create_some_employee_survey_campaign(
        organization_id=org.id,
        participant_ids=[e1.id],
    )
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(
        campaign_id=sc.id,
    )[0]
    idea = create_some_innovation_idea(participation_id=p_id)
    assert isinstance(idea.id, int)
    mp = create_some_management_position(
        organization_id=org.id, manager_ids=[e2.id], role_ids=[bu.id]  # type: ignore
    )
    assert isinstance(mp.id, int)
    r = create_some_report(position_id=mp.id)
    assert isinstance(r.id, int)
    add_participants_to_report(report_id=r.id, participation_ids=[p_id])
    manager_token = get_access_token(e2.user)
    response = fast_client.get(
        url=URLs.innovation_ideas + f"{idea.id}/",
        headers=dict(Authorization=manager_token),
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert set(data.keys()) == {
        "title",
        "description",
        "feasibility_score",
        "confidence_score",
        "impact_score",
        "participation_id",
        "participant_first_name",
        "participant_last_name",
        "participant_email",
        "id",
        "rate",
        "created_at",
        "updated_at",
    }
    assert data["rate"] is None
    rate_idea(idea_id=idea.id, manager_id=e2.id, rate=3)
    response = fast_client.get(
        url=URLs.innovation_ideas + f"{idea.id}/",
        headers=dict(Authorization=manager_token),
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert data["rate"] == 3
