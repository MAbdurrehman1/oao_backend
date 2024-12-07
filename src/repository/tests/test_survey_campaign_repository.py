from datetime import datetime, timedelta

from entity import SurveyCampaign
from .helpers import create_some_organization, create_some_employee
from ..survey_campaign_repository import SurveyCampaignRepository


def test_survey_campaign_repository(cleanup_database, cleanup_media):
    title = "Test SurveyCampaign"
    organization = create_some_organization()
    employee = create_some_employee(organization_id=organization.id)
    start_date = datetime.now()
    end_date = start_date.now() + timedelta(days=2)
    survey_campaign = SurveyCampaign(
        title=title,
        start_date=start_date,
        end_date=end_date,
        organization=organization,
        participants=[employee],
    )
    stored_survey_campaign = SurveyCampaignRepository.store(survey_campaign)
    assert isinstance(stored_survey_campaign.id, int)
    assert isinstance(stored_survey_campaign.created_at, datetime)
    assert isinstance(stored_survey_campaign.updated_at, datetime)
    assert stored_survey_campaign.title == title
    assert stored_survey_campaign.start_date == start_date
    assert stored_survey_campaign.end_date == end_date
    assert stored_survey_campaign.organization_id == organization.id
    assert stored_survey_campaign.participant_ids == survey_campaign.participant_ids
