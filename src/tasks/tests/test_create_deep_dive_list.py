from repository.tests.helpers import (
    create_some_employee,
    create_some_employee_survey_campaign,
    get_campaign_participant_ids,
)
from ..create_deep_dive_list import CreateDeepDiveListTask
from repository import DeepDiveRepository


def test_create_deep_dive_list(
    cleanup_database,
    cleanup_media,
    cleanup_redis,
    mock_etl_get_answer_endpoint,
):
    e = create_some_employee()
    sc = create_some_employee_survey_campaign(
        organization_id=e.organization_id,
        participant_ids=[e.id],
    )
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(campaign_id=sc.id)[0]
    CreateDeepDiveListTask.execute(participant_id=p_id)
    s = DeepDiveRepository.get_deep_dive_strategy(participation_id=p_id)
    assert set(s) == {
        "test_answer_1",
    }
