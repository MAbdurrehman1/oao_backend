from entity import InnovationIdeaRate
from repository import InnovationIdeaRateRepository
from .helpers import (
    create_some_employee,
    create_some_innovation_idea,
    create_some_organization,
    create_some_business_unit,
    create_some_employee_survey_campaign,
    get_campaign_participant_ids,
)


def test_store_innovation_idea_rate(cleanup_database):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    e = create_some_employee(
        email="test@example.com", organization_id=org.id, business_unit_id=bu.id
    )
    e1 = create_some_employee(
        email="manager@example.com", organization_id=org.id, business_unit_id=bu.id
    )
    assert isinstance(e.id, int)
    assert isinstance(e1.id, int)
    assert isinstance(bu.id, int)
    sc = create_some_employee_survey_campaign(
        organization_id=org.id, participant_ids=[e.id]
    )
    assert isinstance(sc.id, int)
    participation_id = get_campaign_participant_ids(campaign_id=sc.id)[0]
    idea = create_some_innovation_idea(participation_id=participation_id)
    assert isinstance(idea.id, int)
    test_rate = 3
    innovation_idea_rate = InnovationIdeaRate(
        innovation_idea_id=idea.id, rate=test_rate, manager_id=e1.id
    )
    stored_rate = InnovationIdeaRateRepository.store(
        innovation_idea_rate=innovation_idea_rate
    )
    assert stored_rate.manager_id == e1.id
    assert stored_rate.rate == test_rate
    assert stored_rate.innovation_idea_id == idea.id
