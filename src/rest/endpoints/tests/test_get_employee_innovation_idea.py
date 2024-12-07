from datetime import datetime, timedelta

from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from repository.tests.helpers import (
    create_some_organization,
    create_some_business_unit,
    create_some_employee,
    create_some_employee_survey_campaign,
    get_campaign_participant_ids,
    create_some_innovation_idea,
)
from rest.endpoints.tests.helpers import URLs, get_access_token


def test_get_employee_innovation_idea(cleanup_database, fast_client, cleanup_media):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    e = create_some_employee(
        email="test1@example.com",
        organization_id=org.id,
        business_unit_id=bu.id,
    )
    sc = create_some_employee_survey_campaign(
        organization_id=org.id,
        participant_ids=[e.id],
    )
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(
        campaign_id=sc.id,
    )[0]
    create_some_innovation_idea(participation_id=p_id)
    token = get_access_token(e.user)
    response = fast_client.get(
        url=URLs.employee_idea.format(id=e.id),
        headers=dict(Authorization=token),
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
        "created_at",
        "updated_at",
    }


def test_get_employee_innovation_idea_without_submitting_to_the_last_campaign(
    cleanup_database, fast_client, cleanup_media
):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    e = create_some_employee(
        email="test1@example.com",
        organization_id=org.id,
        business_unit_id=bu.id,
    )
    sc1 = create_some_employee_survey_campaign(
        start_date=datetime.now() - timedelta(days=100),
        end_date=datetime.now() - timedelta(days=70),
        organization_id=org.id,
        participant_ids=[e.id],
    )
    create_some_employee_survey_campaign(
        start_date=datetime.now() - timedelta(days=60),
        end_date=datetime.now() - timedelta(days=20),
        organization_id=org.id,
        participant_ids=[e.id],
    )
    assert isinstance(sc1.id, int)
    p_id = get_campaign_participant_ids(
        campaign_id=sc1.id,
    )[0]
    create_some_innovation_idea(participation_id=p_id)
    token = get_access_token(e.user)
    response = fast_client.get(
        url=URLs.employee_idea.format(id=e.id),
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json() == {
        "error": f"Innovation Idea with Employee ID ({e.id}) not found."
    }
