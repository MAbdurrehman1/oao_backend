from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_employee_survey_campaign,
    create_some_business_unit,
    get_campaign_participant_ids,
    get_participant_status,
)
from rest.endpoints.tests.helpers import URLs, get_access_token
from settings import ParticipationStatus


def test_create_innovation_idea(cleanup_database, fast_client, cleanup_media):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    e = create_some_employee(
        email="test@example.com", organization_id=org.id, business_unit_id=bu.id
    )
    assert isinstance(e.id, int)
    assert isinstance(bu.id, int)
    sc = create_some_employee_survey_campaign(
        organization_id=org.id, participant_ids=[e.id]
    )
    assert isinstance(sc.id, int)
    participation_id = get_campaign_participant_ids(campaign_id=sc.id)[0]
    data = dict(
        title="test title",
        description="test description",
        feasibility_score=3,
        confidence_score=2,
        impact_score=1,
    )
    employee_token = get_access_token(user=e.user)
    response = fast_client.post(
        URLs.participant_ideas.format(p_id=participation_id),
        headers=dict(Authorization=employee_token),
        json=data,
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Innovation Idea Created Successfully"}
    status = get_participant_status(participant_id=participation_id)
    assert status == ParticipationStatus.IDEA_SUBMITTED
